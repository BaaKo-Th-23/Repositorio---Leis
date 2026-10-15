"""Baixa os enunciados consolidados dos tribunais superiores e grava um arquivo por enunciado.

Súmula não é lei, mas vincula: a súmula vinculante obriga a administração e o Judiciário (art.
103-A da Constituição), e as demais orientam de tal modo que ignorá-las é perder a causa. Por isso
entram no acervo.

A fonte é o **caderno oficial de cada tribunal** — o PDF consolidado que o próprio tribunal
publica e mantém. É a melhor fonte disponível: traz, além do enunciado, a data de aprovação, o
órgão julgador, a fonte de publicação, a referência legislativa e os precedentes. Os portais de
busca dos tribunais seriam melhores por serem estruturados, mas o do STF carrega por JavaScript e
o do STJ (`scon.stj.jus.br`) devolve 403 a acesso automatizado — que este repositório não contorna.

Cada caderno tem um corte próprio, então há um analisador por tribunal. Todos devolvem pares
(número, texto) e o resto do caminho é igual.

    python3 -I scripts/baixar_jurisprudencia.py              # tudo que falta
    python3 -I scripts/baixar_jurisprudencia.py --refazer

Requer `pdftotext` (poppler), o mesmo que o resto do acervo já usa.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import Limitador, yaml_str  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "jurisprudencia"))
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"


def cortar(texto, cabecalho):
    """Divide o caderno em (número, bloco) a cada linha que é só o cabeçalho de um enunciado.

    O cabeçalho precisa casar a linha inteira: nos sumários do início do PDF a mesma palavra
    aparece com o número da página ao lado ("SÚMULA 320   184   SÚMULA 354   203"), e essas linhas
    não podem virar enunciado.

    `\x0c` entra no espaço admitido à esquerda porque é o caractere de quebra de página que o
    pdftotext emite, e ele fica grudado na primeira linha da página seguinte — que é justamente
    onde um enunciado costuma começar.
    """
    marcas = [(m.start(), m.group(1)) for m in cabecalho.finditer(texto)]
    for i, (pos, numero) in enumerate(marcas):
        fim = marcas[i + 1][0] if i + 1 < len(marcas) else len(texto)
        yield numero, texto[pos:fim]


def limpar(bloco):
    """Tira numeração de página solta e espaço de layout, preservando os parágrafos."""
    linhas = []
    for ln in bloco.split("\n"):
        ln = ln.rstrip()
        if re.fullmatch(r"\s*\d{1,4}\s*", ln):  # número de página isolado
            continue
        if re.fullmatch(r"\s*(SÚMULAS?|Súmulas do Superior Tribunal de Justiça)\s*", ln):
            continue
        linhas.append(re.sub(r"[ \t]{2,}", " ", ln).strip())
    # colapsa linhas em branco repetidas
    saida = re.sub(r"\n{3,}", "\n\n", "\n".join(linhas)).strip()
    return saida


def stf_sumulas(texto):
    return cortar(texto, re.compile(r"^[ \t\x0c]*SÚMULA[ \t]+(\d+)[ \t]*$", re.M))


def stj_sumulas(texto):
    return cortar(texto, re.compile(r"^[ \t\x0c]*Súmula[ \t]+(\d+)[ \t]*$", re.M))


# O caderno do TST termina com um índice remissivo que repete todo enunciado, por assunto, em
# forma abreviada. Sem cortar ali, a remissão do índice concorre com o enunciado de verdade — e às
# vezes vence, porque o trecho do índice vem seguido do próximo verbete e fica mais longo.
INDICE_TST = re.compile(r"^[ \t\x0c]*ÍNDICE REMISSIVO[ \t]*$", re.M)


def ate_o_indice(texto):
    m = INDICE_TST.search(texto)
    return texto[: m.start()] if m else texto


def tst_sumulas(texto):
    return cortar(ate_o_indice(texto), re.compile(r"^[ \t\x0c]*SUM-(\d+)\b", re.M))


def tst_ojs(texto):
    return cortar(ate_o_indice(texto), re.compile(r"^[ \t\x0c]*OJ-([A-Z0-9]+-\d+)\b", re.M))


# (tribunal, pasta, prefixo do arquivo, url do caderno, analisador, tipo, molde do título)
CADERNOS = [
    ("stf", "sumulas", "sumula", "https://www.stf.jus.br/arquivo/cms/jurisprudenciaSumula/anexo/"
     "Enunciados_Sumulas_STF_1_a_736_Completo.pdf", stf_sumulas, "Súmula", "Súmula nº {} do STF"),
    ("stj", "sumulas", "sumula", "https://www.stj.jus.br/docs_internet/SumulasSTJ.pdf",
     stj_sumulas, "Súmula", "Súmula nº {} do STJ"),
    ("tst", "sumulas", "sumula", "https://www.tst.jus.br/documents/10157/63003/Livro-Internet.pdf",
     tst_sumulas, "Súmula", "Súmula nº {} do TST"),
    ("tst", "orientacoes-jurisprudenciais", "oj", "https://www.tst.jus.br/documents/10157/63003/Livro-Internet.pdf",
     tst_ojs, "Orientação Jurisprudencial", "Orientação Jurisprudencial {} do TST"),
]

# As súmulas vinculantes do STF ainda não têm caderno localizado: o portal responde 200 com a
# página genérica para qualquer caminho de PDF, então não há como descobrir a URL por tentativa, e
# a lista em HTML é montada por JavaScript. Ver PROGRESSO.md.

DATA_APROVACAO = re.compile(r"(?:Data de Aprovação|Data da Decisão)\s*\n\s*(?:Sessão Plenária de\s*)?"
                            r"(\d{2})/(\d{2})/(\d{4})", re.I)
# O caderno do TST não tem campo de data: a referência da redação em vigor vem no próprio
# cabeçalho do enunciado ("Res. 174/2011, DEJT divulgado em 27, 30 e 31.05.2011"). A primeira data
# do bloco é a dessa redação — é a data que o acervo registra, e não a da redação original, que
# aparece depois, no histórico.
DATA_TST = re.compile(r"\b(\d{2})\.(\d{2})\.(\d{4})\b")


def data_do_enunciado(corpo):
    m = DATA_APROVACAO.search(corpo)
    if m:
        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m = DATA_TST.search(corpo)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else ""


def baixar_pdf(url, destino, limite):
    if os.path.exists(destino):
        return
    limite.esperar()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*",
                                               "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dados = r.read()
    if not dados.startswith(b"%PDF"):
        raise RuntimeError(f"a resposta não é PDF ({len(dados)} bytes): {url}")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    tmp = destino + ".tmp"
    with open(tmp, "wb") as f:
        f.write(dados)
    os.replace(tmp, destino)


def texto_do_pdf(caminho):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as t:
        saida = t.name
    try:
        subprocess.run(["pdftotext", "-layout", caminho, saida], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(saida, encoding="utf-8", errors="replace") as f:
            return f.read()
    finally:
        os.unlink(saida)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--rps", type=float, default=1)
    a = ap.parse_args()
    limite = Limitador(a.rps)
    cont = {"ok": 0, "pulado": 0}

    for tribunal, pasta, prefixo, url, analisar, tipo, molde in CADERNOS:
        pdf = os.path.join(RAIZ, "_fonte", tribunal, os.path.basename(url.split("?")[0]))
        try:
            baixar_pdf(url, pdf, limite)
        except Exception as e:
            print(f"{tribunal}/{pasta}: falhou ao baixar o caderno: {str(e)[:140]}", flush=True)
            continue
        texto = texto_do_pdf(pdf)

        # o mesmo número aparece mais de uma vez no caderno — no sumário por assunto e no corpo.
        # Fica o bloco mais longo, que é sempre o do enunciado de verdade; os outros são remissões.
        melhor = {}
        for numero, bloco in analisar(texto):
            if len(bloco) > len(melhor.get(numero, "")):
                melhor[numero] = bloco

        n_ok = n_pulado = 0
        for numero, bloco in sorted(melhor.items(), key=lambda x: (len(x[0]), x[0])):
            slug = f"{prefixo}-{numero.lower()}"
            md = os.path.join(RAIZ, tribunal, pasta, slug + ".md")
            if os.path.exists(md) and not a.refazer:
                n_pulado += 1
                continue
            corpo = limpar(bloco)
            titulo = molde.format(numero)
            data = data_do_enunciado(corpo)
            cab = ["---", f"titulo: {yaml_str(titulo)}", f"tribunal: {yaml_str(tribunal.upper())}",
                   f"tipo: {yaml_str(tipo)}", f"numero: {yaml_str(numero)}", f"data: {data}",
                   "revogada: false", 'versao_texto: "caderno consolidado do tribunal"',
                   f"fonte: {yaml_str(url)}", f"baixado_em: {dt.date.today().isoformat()}", "---", ""]
            os.makedirs(os.path.dirname(md), exist_ok=True)
            tmp = md + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write("\n".join(cab) + f"# {titulo}\n\n" + corpo + "\n")
            os.replace(tmp, md)
            n_ok += 1
        cont["ok"] += n_ok
        cont["pulado"] += n_pulado
        print(f"{tribunal}/{pasta}: {n_ok} gravados, {n_pulado} já existiam", flush=True)
    print("FIM", cont, flush=True)


if __name__ == "__main__":
    main()
