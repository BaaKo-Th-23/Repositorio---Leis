"""Baixa legislação municipal dos diários oficiais das associações estaduais de municípios.

O direito municipal é a maior lacuna do acervo — 5.570 municípios, nenhum índice nacional. Mas ele
não está espalhado em 5.570 portais: a maioria dos municípios publica no **diário oficial da
associação estadual** a que pertence, e todas essas associações usam a mesma plataforma, reunida
em `diariomunicipal.com.br`. São ~24 diários que, somados, cobrem milhares de municípios — o
equivalente municipal do que o DOU é para a União.

Cada edição é um PDF único com todos os atos do dia, de todos os municípios daquela associação,
na forma:

    ESTADO DO RIO GRANDE DO SUL
    PREFEITURA MUNICIPAL DE SANTA CRUZ DO SUL
    ...
    PROCURADORIA GERAL DO MUNICÍPIO
    LEI Nº 10.574, DE 14 DE OUTUBRO DE 2026.
    <ementa e texto>
    Publicado por:
    <nome>
    Código Identificador:481AA0F1

O `Código Identificador` fecha cada ato e é único — é por ele que a edição se divide. O município
vem do cabeçalho de seção mais recente.

**O PDF é convertido sem `-layout`, de propósito.** A edição é diagramada em duas colunas, e o
`-layout` entrelaça as colunas: a epígrafe de uma lei sai na mesma linha do "Publicado por:" da
outra. Sem ele, o pdftotext respeita a ordem de leitura do próprio PDF e o texto sai correto.

**Limitação de origem: só a edição do dia é alcançável.** A página de cada associação expõe o link
da edição corrente; o acervo retroativo existe, mas só pela busca do site, que é montada por
JavaScript, e os PDFs antigos ficam atrás de uma URL com hash por edição. Então este script
acumula para a frente: rodado todo dia, constrói o acervo municipal a partir de hoje. O retroativo
exige automação de navegador, que não está no ferramental deste repositório.

    python3 -I scripts/baixar_municipal.py              # a edição de hoje de todas as associações
    python3 -I scripts/baixar_municipal.py --listar     # só mostra as associações e o que acharia
    python3 -I scripts/baixar_municipal.py --assoc famurs,amm-mg
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import CANONICO, Limitador, normalizar_chave, slugify, yaml_str  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "municipais"))
PORTAL = "https://www.diariomunicipal.com.br/"
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"

UFS = {
    "acre": "AC", "alagoas": "AL", "amapa": "AP", "amazonas": "AM", "bahia": "BA", "ceara": "CE",
    "distrito federal": "DF", "espirito santo": "ES", "goias": "GO", "maranhao": "MA",
    "mato grosso": "MT", "mato grosso do sul": "MS", "minas gerais": "MG", "para": "PA",
    "paraiba": "PB", "parana": "PR", "pernambuco": "PE", "piaui": "PI", "rio de janeiro": "RJ",
    "rio grande do norte": "RN", "rio grande do sul": "RS", "rondonia": "RO", "roraima": "RR",
    "santa catarina": "SC", "sao paulo": "SP", "sergipe": "SE", "tocantins": "TO",
}

# Só o que é norma. A edição municipal é dominada por extrato de contrato, aviso de licitação,
# portaria de nomeação e resultado de concurso — nenhum deles é norma de caráter geral.
TIPOS = [
    (re.compile(r"^LEI\s+COMPLEMENTAR\s+N", re.I), "lei complementar"),
    (re.compile(r"^LEI\s+ORG[ÂA]NICA", re.I), "lei organica"),
    (re.compile(r"^EMENDA\s+[ÀA]\s+LEI\s+ORG[ÂA]NICA", re.I), "emenda a lei organica"),
    (re.compile(r"^LEI\s+(?:MUNICIPAL\s+)?N", re.I), "lei ordinaria"),
    (re.compile(r"^DECRETO\s+(?:MUNICIPAL\s+)?N", re.I), "decreto"),
]

CODIGO = re.compile(r"^Código Identificador:\s*(\w+)\s*$", re.M)
# Os cabeçalhos variam por diário: "ESTADO DE MINAS GERAIS", "ESTADO DO RIO GRANDE DO SUL",
# "ESTADO DA BAHIA"; e "PREFEITURA MUNICIPAL DO CARPINA" ao lado de "MUNICÍPIO DE ALEXÂNIA-GO".
# A preposição entra como D[AEO]S? e o nome do estado é validado contra UFS — assim uma linha que
# só começa igual ("ESTADO DE GOIÁS, E A EMPRESA...") não vira cabeçalho.
ENTIDADE = re.compile(r"^(?:PREFEITURA\s+MUNICIPAL|PREFEITURA|MUNIC[ÍI]PIO|C[ÂA]MARA\s+MUNICIPAL"
                      r"|C[ÂA]MARA|GOVERNO\s+MUNICIPAL)\s+D[AEO]S?\s+(.+?)\s*$", re.M)
ESTADO = re.compile(r"^ESTADO\s+D[AEO]S?\s+(.+?)\s*$", re.M)
# "ALEXÂNIA-GO", "SÃO PAULO/SP": a sigla do estado no fim do nome do município
SUFIXO_UF = re.compile(r"\s*[-/]\s*[A-Z]{2}\s*$")
NUMERO = re.compile(r"\bN[.ºo°\s]{0,4}(\d[\d.]*)", re.I)
DATA_EXTENSO = re.compile(r"(\d{1,2})\s+DE\s+([A-ZÀ-Ÿa-zà-ÿ]+)\s+DE\s+(\d{4})", re.I)
DATA_BARRA = re.compile(r"\b(\d{1,4})\s*/\s*(\d{4})\b")
MESES = {m: i + 1 for i, m in enumerate(
    "janeiro fevereiro marco abril maio junho julho agosto setembro outubro novembro dezembro".split())}


def http(url, limite, tentativas=3, timeout=300):
    import time
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*",
                                               "Accept-Encoding": "identity"})
    ultimo = None
    for n in range(tentativas):
        limite.esperar()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except Exception as e:
            ultimo = e
            time.sleep(3 * (n + 1) ** 2)
    raise RuntimeError(f"falhou após {tentativas} tentativas: {url}: {ultimo}")


def associacoes(limite):
    """Os diários listados no portal: ('famurs', 'https://…/famurs/')."""
    st, bruto = http(PORTAL, limite, timeout=90)
    pagina = bruto.decode("utf-8", errors="replace")
    vistos, saida = set(), []
    for href in re.findall(r'href="(https://www\.diariomunicipal\.com\.br/([a-z0-9-]+)/)"', pagina):
        url, slug = href
        if slug not in vistos:
            vistos.add(slug)
            saida.append((slug, url))
    return saida


def link_da_edicao(url_assoc, limite):
    """A URL do PDF da edição corrente, que a página da associação expõe."""
    st, bruto = http(url_assoc, limite, timeout=90)
    pagina = bruto.decode("utf-8", errors="replace")
    for href in re.findall(r'href="([^"]*voxtecnologia[^"]*\.pdf[^"]*)"', pagina):
        return html.unescape(href)
    return None


def data_do_link(link):
    m = re.search(r"_(\d{4}-\d{2}-\d{2})_", link)
    return dt.date.fromisoformat(m.group(1)) if m else dt.date.today()


def texto_do_pdf(caminho):
    """Sem -layout: a edição é de duas colunas e o -layout entrelaça as colunas."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as t:
        saida = t.name
    try:
        subprocess.run(["pdftotext", caminho, saida], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(saida, encoding="utf-8", errors="replace") as f:
            return f.read()
    finally:
        os.unlink(saida)


def atos(texto):
    """Divide a edição em atos, carregando a UF e o município da seção corrente."""
    uf = municipio = None
    pos = 0
    for m in CODIGO.finditer(texto):
        bloco = texto[pos:m.start()]
        pos = m.end()
        # os cabeçalhos de seção que aparecerem dentro deste bloco valem a partir daqui
        for e in ESTADO.finditer(bloco):
            uf = UFS.get(normalizar_chave(e.group(1))) or uf
        for e in ENTIDADE.finditer(bloco):
            nome = SUFIXO_UF.sub("", e.group(1).strip())
            if 2 < len(nome) <= 60:
                municipio = nome
        yield uf, municipio, bloco, m.group(1)


def epigrafe(bloco):
    """(epígrafe, tipo canônico, posição) da primeira linha do bloco que abre uma norma.

    A posição importa: o bloco começa onde terminou o ato anterior, então traz na frente o rodapé
    dele — assinatura, cidade, nome da secretaria. O texto da norma começa na epígrafe.
    """
    pos = 0
    for bruta in bloco.split("\n"):
        linha = bruta.strip()
        if 6 <= len(linha) <= 160 and e_epigrafe(linha):
            for padrao, chave in TIPOS:
                if padrao.match(linha):
                    return linha, chave, pos
        pos += len(bruta) + 1
    return None, None, 0


def e_epigrafe(linha):
    """Distingue a epígrafe de uma citação à mesma norma no meio de uma frase.

    O texto corrido quebra onde calha, e uma linha pode começar em "Lei Orgânica do Município e
    Constituição Federal, FAZ SABER que" — que casa com o padrão de tipo mas não é epígrafe
    nenhuma. Duas exigências separam uma coisa da outra: a epígrafe municipal é escrita em caixa
    alta, e traz o número da norma. A lei orgânica é a exceção ao número, porque não tem; dela se
    exige, em troca, que a linha seja curta — citação costuma continuar a frase.
    """
    if linha != linha.upper():
        return False
    if NUMERO.search(linha) or DATA_BARRA.search(linha):
        return True
    return len(linha) <= 60 and not linha.rstrip().endswith((",", ";", ":", "E", "QUE", "DO", "DE"))


def data_da_epigrafe(linha, ano_padrao):
    m = DATA_EXTENSO.search(linha)
    if m:
        mes = MESES.get(normalizar_chave(m.group(2)))
        if mes:
            return f"{int(m.group(3)):04d}-{mes:02d}-{int(m.group(1)):02d}"
    # "LEI MUNICIPAL Nº 4120/2026": só o ano é afirmado pela fonte
    m = DATA_BARRA.search(linha)
    if m and 1800 <= int(m.group(2)) <= ano_padrao:
        return ""
    return ""


def gravar(uf, municipio, titulo, chave, bloco, codigo, data_edicao, link):
    pasta, tipo_nome = CANONICO[chave]
    num = NUMERO.search(titulo)
    numero = num.group(1).replace(".", "") if num else ""
    data = data_da_epigrafe(titulo, data_edicao.year)
    ano = (data[:4] if data else str(data_edicao.year))
    # o nome do arquivo sai da chave canônica ("lei ordinaria"), não da pasta no plural; e o
    # nome do município perde o acento, para que o caminho seja o mesmo em qualquer sistema
    slug = slugify(f"{slugify(chave)}-{numero or codigo}-{ano}-{codigo}")[:110]
    md = os.path.join(RAIZ, uf, slugify(normalizar_chave(municipio))[:60], pasta, ano, slug + ".md")
    if os.path.exists(md):
        return False
    corpo = re.sub(r"\n{3,}", "\n\n", bloco.strip())
    cab = ["---", f"titulo: {yaml_str(titulo)}", f"uf: {yaml_str(uf)}",
           f"municipio: {yaml_str(municipio)}", f"tipo: {yaml_str(tipo_nome)}",
           f"numero: {yaml_str(numero)}", f"data: {data}", f"ano: {yaml_str(ano)}",
           "revogada: false", 'versao_texto: "publicação original"',
           f"publicacao: {yaml_str('Diário Oficial de ' + data_edicao.strftime('%d/%m/%Y'))}",
           f"data_publicacao: {data_edicao.isoformat()}",
           f"codigo_identificador: {yaml_str(codigo)}", f"fonte: {yaml_str(link)}",
           f"baixado_em: {dt.date.today().isoformat()}", "---", ""]
    os.makedirs(os.path.dirname(md), exist_ok=True)
    tmp = md + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(cab) + f"# {titulo}\n\n" + corpo + "\n")
    os.replace(tmp, md)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--assoc", default="", help="só estas associações (ex.: famurs,amm-mg)")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--rps", type=float, default=1, help="o portal é lento; uma por segundo basta")
    a = ap.parse_args()

    limite = Limitador(a.rps)
    alvo = {s.strip() for s in a.assoc.split(",") if s.strip()}
    lista = [(s, u) for s, u in associacoes(limite) if not alvo or s in alvo]
    print(f"{len(lista)} diários: {', '.join(s for s, _ in lista)}", flush=True)
    if a.listar:
        return

    os.makedirs(RAIZ, exist_ok=True)
    falhas_path = os.path.join(RAIZ, "_falhas.jsonl")
    total = {"ok": 0, "pulado": 0, "sem_norma": 0, "sem_edicao": 0, "erro": 0}
    with open(falhas_path, "a", encoding="utf-8") as falhas:
        for slug, url in lista:
            try:
                link = link_da_edicao(url, limite)
            except Exception as e:
                total["erro"] += 1
                print(f"{slug}: erro na página: {str(e)[:110]}", flush=True)
                continue
            if not link:
                total["sem_edicao"] += 1
                falhas.write(json.dumps({"assoc": slug, "status": "sem_edicao",
                                         "data": dt.date.today().isoformat()}, ensure_ascii=False) + "\n")
                print(f"{slug}: sem edição publicada hoje", flush=True)
                continue
            data_edicao = data_do_link(link)
            pdf = os.path.join(RAIZ, "_fonte", slug, f"{data_edicao.isoformat()}.pdf")
            if not os.path.exists(pdf):
                st, dados = http(link, limite)
                if not dados.startswith(b"%PDF"):
                    total["erro"] += 1
                    print(f"{slug}: a edição não veio como PDF", flush=True)
                    continue
                os.makedirs(os.path.dirname(pdf), exist_ok=True)
                with open(pdf + ".tmp", "wb") as f:
                    f.write(dados)
                os.replace(pdf + ".tmp", pdf)

            n_ok = n_pulado = n_sem = 0
            for uf, municipio, bloco, codigo in atos(texto_do_pdf(pdf)):
                titulo, chave, inicio = epigrafe(bloco)
                if not titulo or not uf or not municipio:
                    n_sem += 1
                    continue
                if gravar(uf, municipio, titulo, chave, bloco[inicio:], codigo, data_edicao, link):
                    n_ok += 1
                else:
                    n_pulado += 1
            total["ok"] += n_ok
            total["pulado"] += n_pulado
            total["sem_norma"] += n_sem
            print(f"{slug} {data_edicao}: {n_ok} normas novas, {n_pulado} já tinha, "
                  f"{n_sem} atos que não são norma", flush=True)
    print("FIM", total, flush=True)


if __name__ == "__main__":
    main()
