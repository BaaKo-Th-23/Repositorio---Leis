"""Baixa atos infralegais federais do Diário Oficial da União e grava em `reguladores/`.

Por que o DOU e não um raspador por órgão: todo ato infralegal federal com efeito externo —
resolução do CONTRAN, RDC da ANVISA, instrução normativa da Receita, resolução do CMN, portaria do
Ministério da Saúde — nasce publicado no DOU. Um portal por órgão significaria sessenta raspadores,
cada um com seu formato e sua instabilidade; o DOU é uma fonte só, estável e aberta, e já traz o
tipo do ato (`artType`) e a cadeia do órgão emissor (`hierarchyList`) prontos para classificar.

A LexML seria o índice ideal, por já normalizar a URN, mas está atrás de um desafio anti-bot do
Senado — e este repositório não contorna bloqueio de acesso automatizado.

Como funciona: `leiturajornal?data=DD-MM-AAAA&secao=do1` devolve, num `<script id="params">`, o
JSON de todos os atos publicados naquele dia. Para cada ato do tipo que interessa, busca-se o texto
integral em `/web/dou/-/<urlTitle>`.

O que entra: só a Seção 1, que é a dos atos normativos. A Seção 2 é pessoal (nomeações,
exonerações) e a 3 é licitação e contrato — nenhuma das duas é norma. Dentro da Seção 1, só os
tipos de TIPOS_NORMATIVOS: despacho, decisão, pauta de julgamento e extrato de ata ficam de fora
pelo mesmo motivo.

    python3 -I scripts/baixar_dou.py --de 2026-01-01 --ate 2026-10-15
    python3 -I scripts/baixar_dou.py --de 2024-01-01 --ate 2024-12-31 --orgaos anvisa,contran
    python3 -I scripts/baixar_dou.py --de 2026-10-01 --ate 2026-10-15 --listar   # só conta

O texto online do DOU começa em 2002; antes disso a Imprensa Nacional só tem a imagem digitalizada
da edição, que é outro problema (ver as pendências de OCR no README).
"""
import argparse
import datetime as dt
import gzip
import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import CANONICO, Limitador, normalizar_chave, slugify, yaml_str  # noqa: E402
from datas import data_do_texto  # noqa: E402
from html2md import convert  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reguladores"))
DIA = "https://www.in.gov.br/leiturajornal?data={}&secao=do1"
ATO = "https://www.in.gov.br/web/dou/-/{}"
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"

# Tipos de ato (campo artType) que são norma. O DOU publica muito que não é: despacho, decisão em
# processo, pauta de julgamento, extrato de ata, aviso, edital. Esses não entram.
TIPOS_NORMATIVOS = {
    "resolução": "resolucao",
    "resolução normativa": "resolucao normativa",
    "resolução de diretoria colegiada": "resolucao da diretoria colegiada",
    "portaria": "portaria",
    "portaria normativa": "portaria",
    "instrução normativa": "instrucao normativa",
    "deliberação": "deliberacao",
    "circular": "circular",
    "provimento": "provimento",
    "parecer normativo": "parecer normativo",
    "súmula": "sumula",
    "decreto": "decreto",
}

# Órgãos que têm identidade normativa própria e merecem pasta própria, mesmo aparecendo sob um
# ministério na hierarquia do DOU. A chave casa por substring, sem acento e em minúsculas, contra
# qualquer nível de `hierarchyList` — do mais específico para o mais geral.
ORGAOS = {
    "agencia nacional de vigilancia sanitaria": "anvisa",
    "agencia nacional de energia eletrica": "aneel",
    "agencia nacional do petroleo": "anp",
    "agencia nacional de telecomunicacoes": "anatel",
    "agencia nacional de saude suplementar": "ans",
    "agencia nacional de aviacao civil": "anac",
    "agencia nacional de transportes terrestres": "antt",
    "agencia nacional de transportes aquaviarios": "antaq",
    "agencia nacional de aguas": "ana",
    "agencia nacional do cinema": "ancine",
    "agencia nacional de mineracao": "anm",
    "agencia nacional de telecomunicac": "anatel",
    "banco central do brasil": "bcb",
    "conselho monetario nacional": "bcb",
    "comissao de valores mobiliarios": "cvm",
    "superintendencia de seguros privados": "susep",
    "superintendencia nacional de previdencia complementar": "previc",
    "secretaria especial da receita federal": "rfb",
    "receita federal do brasil": "rfb",
    "procuradoria-geral da fazenda nacional": "pgfn",
    "secretaria do tesouro nacional": "stn",
    "conselho administrativo de recursos fiscais": "carf",
    "conselho nacional de politica fazendaria": "confaz",
    "instituto brasileiro do meio ambiente": "ibama",
    "instituto chico mendes": "icmbio",
    "conselho nacional do meio ambiente": "conama",
    "conselho nacional de transito": "contran",
    "secretaria nacional de transito": "senatran",
    "departamento nacional de transito": "senatran",
    "instituto nacional do seguro social": "inss",
    "instituto nacional de metrologia": "inmetro",
    "conselho nacional de saude": "cns",
    "conselho nacional de educacao": "cne",
    "instituto nacional de estudos e pesquisas": "inep",
    "coordenacao de aperfeicoamento de pessoal": "capes",
    "instituto do patrimonio historico": "iphan",
    "conselho administrativo de defesa economica": "cade",
    "conselho de controle de atividades financeiras": "coaf",
    "controladoria-geral da uniao": "cgu",
    "servico florestal brasileiro": "sfb",
}

# Ministérios: a pasta de recuo quando nenhum órgão específico casa. Mantém o número de pastas
# limitado — sem isso, cada superintendência estadual viraria uma pasta.
MINISTERIOS = {
    "ministerio da saude": "ms",
    "ministerio da educacao": "mec",
    "ministerio do trabalho": "mte",
    "ministerio da previdencia social": "sprev",
    "ministerio da fazenda": "fazenda",
    "ministerio da agricultura": "mapa",
    "ministerio do meio ambiente": "mma",
    "ministerio dos transportes": "transportes",
    "ministerio de minas e energia": "mme",
    "ministerio da justica": "mj",
    "ministerio da defesa": "defesa",
    "ministerio das comunicacoes": "comunicacoes",
    "ministerio do desenvolvimento agrario": "mda",
    "ministerio da cultura": "cultura",
    "ministerio do turismo": "turismo",
    "ministerio das cidades": "cidades",
    "ministerio da integracao": "integracao",
    "ministerio da ciencia": "mcti",
    "ministerio do desenvolvimento social": "mds",
    "ministerio das mulheres": "mulheres",
    "ministerio dos direitos humanos": "mdh",
    "ministerio dos povos indigenas": "mpi",
    "ministerio da igualdade racial": "igualdade-racial",
    "ministerio do esporte": "esporte",
    "ministerio do planejamento": "planejamento",
    "ministerio da gestao": "gestao",
    "ministerio de portos e aeroportos": "portos-aeroportos",
    "ministerio do desenvolvimento industria": "mdic",
    "ministerio do desenvolvimento e assisten": "mds",
    "ministerio publico da uniao": "mpu",
    "ministerio das relacoes exteriores": "mre",
    "ministerio do empreendedorismo": "empreendedorismo",
    "ministerio da pesca": "pesca",
    "presidencia da republica": "presidencia",
    "advocacia-geral da uniao": "agu",
    "banco nacional de desenvolvimento": "bndes",
}


def sem_acento(s):
    return normalizar_chave(s)


def orgao_de(hierarquia):
    """Decide a pasta do órgão: o mais específico que reconhecemos, senão o ministério, senão outros."""
    niveis = [sem_acento(n) for n in hierarquia or []]
    for nivel in reversed(niveis):  # do mais específico para o mais geral
        for chave, slug in ORGAOS.items():
            if chave in nivel:
                return slug
    for nivel in niveis:
        for chave, slug in MINISTERIOS.items():
            if chave in nivel:
                return slug
    return slugify(niveis[0])[:40] if niveis else "outros"


def http(url, limite, accept="text/html", tentativas=4):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept,
                                               "Accept-Encoding": "identity"})
    import time
    ultimo = None
    for n in range(tentativas):
        limite.esperar()
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (400, 404, 410):
                return e.code, b""
            ultimo = e
        except Exception as e:
            ultimo = e
        time.sleep(3 * (n + 1) ** 2)
    raise RuntimeError(f"falhou após {tentativas} tentativas: {url}: {ultimo}")


def atos_do_dia(data, limite):
    """Lista de atos publicados na Seção 1 em `data` (date), do JSON embutido na página."""
    st, bruto = http(DIA.format(data.strftime("%d-%m-%Y")), limite)
    if st != 200 or not bruto:
        return []
    html = bruto.decode("utf-8", errors="replace")
    m = re.search(r'<script[^>]+id="params"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return []
    try:
        return json.loads(m.group(1)).get("jsonArray") or []
    except json.JSONDecodeError:
        return []


NUMERO = re.compile(r"n[ºo°]\s*([\d.]+)", re.I)


def processar(ato, data, limite, orgaos_alvo):
    tipo_bruto = (ato.get("artType") or "").strip().lower()
    if tipo_bruto not in TIPOS_NORMATIVOS:
        return "ignorado", None
    orgao = orgao_de(ato.get("hierarchyList"))
    if orgaos_alvo and orgao not in orgaos_alvo:
        return "ignorado", None

    pasta, tipo_nome = CANONICO[TIPOS_NORMATIVOS[tipo_bruto]]
    ano = data.strftime("%Y")
    slug = slugify(ato["urlTitle"])[:120]
    md = os.path.join(RAIZ, orgao, pasta, ano, slug + ".md")
    if os.path.exists(md):
        return "pulado", None

    url = ATO.format(ato["urlTitle"])
    st, bruto = http(url, limite)
    if st != 200 or not bruto:
        return "sem_texto", {"urlTitle": ato["urlTitle"], "titulo": ato.get("title"), "http": st}
    html = bruto.decode("utf-8", errors="replace")
    m = re.search(r'<div[^>]+class="[^"]*texto-dou[^"]*".*?</div>\s*(?=<div|</section|</main)', html, re.S)
    if not m:
        return "sem_texto", {"urlTitle": ato["urlTitle"], "titulo": ato.get("title"), "motivo": "sem bloco texto-dou"}

    fonte = os.path.join(RAIZ, "_fonte", orgao, ano, slug + ".html.gz")
    os.makedirs(os.path.dirname(fonte), exist_ok=True)
    with gzip.open(fonte, "wb") as f:
        f.write(bruto)

    titulo = (ato.get("title") or "").strip()
    num = NUMERO.search(titulo)
    # o título do DOU é a própria epígrafe, e traz a data de assinatura — que não é a da
    # publicação: um ato assinado no dia 13 costuma sair no dia 14. O acervo data a norma pela
    # assinatura, como nas leis; a publicação fica nos campos `publicacao`/`data_publicacao`.
    assinatura = data_do_texto(titulo, linhas=1) or data.isoformat()
    corpo = convert(m.group(0))
    cab = ["---", f"titulo: {yaml_str(titulo)}", f"orgao: {yaml_str(ato.get('hierarchyStr') or '')}",
           f"tipo: {yaml_str(tipo_nome)}", f"numero: {yaml_str(num.group(1).replace('.', '') if num else '')}",
           f"data: {assinatura}", "revogada: false", 'versao_texto: "publicação original"',
           f"publicacao: {yaml_str('DOU de ' + data.strftime('%d/%m/%Y') + ', seção 1, p. ' + str(ato.get('numberPage') or ''))}",
           f"data_publicacao: {data.isoformat()}", f"edicao: {yaml_str(ato.get('editionNumber') or '')}",
           f"fonte: {yaml_str(url)}", f"baixado_em: {dt.date.today().isoformat()}", "---", ""]
    os.makedirs(os.path.dirname(md), exist_ok=True)
    tmp = md + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(cab) + f"# {titulo}\n\n" + corpo)
    os.replace(tmp, md)
    return "ok", None


def dias(de, ate):
    d = de
    while d <= ate:
        yield d
        d += dt.timedelta(days=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--de", required=True, help="AAAA-MM-DD")
    ap.add_argument("--ate", required=True, help="AAAA-MM-DD")
    ap.add_argument("--orgaos", default="", help="só estes (ex.: anvisa,contran); vazio = todos")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--rps", type=float, default=3)
    ap.add_argument("--listar", action="store_true", help="conta o que seria baixado, sem baixar")
    a = ap.parse_args()

    de = dt.date.fromisoformat(a.de)
    ate = dt.date.fromisoformat(a.ate)
    alvo = {s.strip() for s in a.orgaos.split(",") if s.strip()}
    limite = Limitador(a.rps)
    os.makedirs(RAIZ, exist_ok=True)
    falhas_path = os.path.join(RAIZ, "_falhas.jsonl")
    cont = {"ok": 0, "pulado": 0, "sem_texto": 0, "ignorado": 0, "erro": 0}
    por_orgao = {}

    with open(falhas_path, "a", encoding="utf-8") as falhas:
        for data in dias(de, ate):
            try:
                lista = atos_do_dia(data, limite)
            except Exception as e:
                print(f"{data} erro no índice do dia: {str(e)[:120]}", flush=True)
                cont["erro"] += 1
                continue
            if a.listar:
                for ato in lista:
                    if (ato.get("artType") or "").strip().lower() in TIPOS_NORMATIVOS:
                        o = orgao_de(ato.get("hierarchyList"))
                        if not alvo or o in alvo:
                            por_orgao[o] = por_orgao.get(o, 0) + 1
                            cont["ok"] += 1
                print(f"{data} {len(lista)} atos, {cont['ok']} normativos acumulados", flush=True)
                continue
            with ThreadPoolExecutor(a.workers) as ex:
                futs = {ex.submit(processar, ato, data, limite, alvo): ato for ato in lista}
                for fut in as_completed(futs):
                    ato = futs[fut]
                    try:
                        st, extra = fut.result()
                    except Exception as e:
                        st, extra = "erro", {"urlTitle": ato.get("urlTitle"), "erro": str(e)[:300]}
                    cont[st] += 1
                    if extra:
                        extra["status"] = st
                        extra["data"] = data.isoformat()
                        falhas.write(json.dumps(extra, ensure_ascii=False) + "\n")
                        falhas.flush()
            print(f"{data} {cont}", flush=True)

    if a.listar:
        for o, n in sorted(por_orgao.items(), key=lambda x: -x[1]):
            print(f"  {n:6} {o}")
    print("FIM", cont, flush=True)


if __name__ == "__main__":
    main()
