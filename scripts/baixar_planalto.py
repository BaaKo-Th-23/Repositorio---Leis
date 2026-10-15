"""Baixa do Planalto os documentos que o índice do Senado não alcança.

Duas famílias, ambas fora do serviço `legislacao/lista` do Senado:

- **as constituições anteriores a 1988**, que não são "normas" no índice e só existem como páginas
  próprias do Portal da Legislação;
- **os regulamentos consolidados** — RIR, RIPI, Regulamento Aduaneiro, RPS e afins. Esses até são
  decretos e entram pelo índice, mas o texto que importa é o compilado que o Planalto mantém, com
  as alterações já embutidas: é por ele que se trabalha, não pela publicação original.

Cada documento é declarado em DOCUMENTOS, com o caminho de destino e os metadados que a página não
traz em forma legível por máquina. Retomável: pula o que já existe. O HTML original fica em
`federal/_fonte/planalto/`.

    python3 -I scripts/baixar_planalto.py                # tudo que falta
    python3 -I scripts/baixar_planalto.py --refazer      # regrava mesmo o que já existe
"""
import argparse
import datetime as dt
import gzip
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import Limitador, decodificar  # noqa: E402
from html2md import convert  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "federal"))
BASE = "https://www.planalto.gov.br/ccivil_03/"
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"

# (pasta, nome do arquivo, URL relativa ao ccivil_03, título, tipo, número, data, ementa)
DOCUMENTOS = [
    ("constituicoes-historicas", "constituicao-1824", "constituicao/constituicao24.htm",
     "Constituição Política do Império do Brasil de 1824", "Constituição", "", "1824-03-25",
     "Constituição Política do Império do Brasil, outorgada em 25 de março de 1824."),
    ("constituicoes-historicas", "constituicao-1891", "constituicao/constituicao91.htm",
     "Constituição da República dos Estados Unidos do Brasil de 1891", "Constituição", "", "1891-02-24",
     "Constituição da República dos Estados Unidos do Brasil, de 24 de fevereiro de 1891."),
    ("constituicoes-historicas", "constituicao-1934", "constituicao/constituicao34.htm",
     "Constituição da República dos Estados Unidos do Brasil de 1934", "Constituição", "", "1934-07-16",
     "Constituição da República dos Estados Unidos do Brasil, de 16 de julho de 1934."),
    ("constituicoes-historicas", "constituicao-1937", "constituicao/constituicao37.htm",
     "Constituição dos Estados Unidos do Brasil de 1937", "Constituição", "", "1937-11-10",
     "Constituição dos Estados Unidos do Brasil, de 10 de novembro de 1937."),
    ("constituicoes-historicas", "constituicao-1946", "constituicao/constituicao46.htm",
     "Constituição dos Estados Unidos do Brasil de 1946", "Constituição", "", "1946-09-18",
     "Constituição dos Estados Unidos do Brasil, de 18 de setembro de 1946."),
    ("constituicoes-historicas", "constituicao-1967", "constituicao/constituicao67.htm",
     "Constituição da República Federativa do Brasil de 1967", "Constituição", "", "1967-01-24",
     "Constituição da República Federativa do Brasil, de 24 de janeiro de 1967."),
    ("constituicoes-historicas", "constituicao-1967-emenda-1-1969", "constituicao/constituicao67emc69.htm",
     "Constituição da República Federativa do Brasil de 1967, com a redação da Emenda Constitucional nº 1 de 1969",
     "Constituição", "", "1969-10-17",
     "Texto constitucional de 1967 com a redação dada pela Emenda Constitucional nº 1, de 17 de outubro de 1969."),

    ("regulamentos", "rir-decreto-9580-2018", "_ato2015-2018/2018/decreto/d9580.htm",
     "Regulamento do Imposto de Renda — Decreto nº 9.580 de 22/11/2018", "Decreto", "9580", "2018-11-22",
     "Regulamenta a tributação, a fiscalização, a arrecadação e a administração do Imposto sobre a Renda e Proventos de Qualquer Natureza."),
    ("regulamentos", "ripi-decreto-7212-2010", "_ato2007-2010/2010/decreto/d7212.htm",
     "Regulamento do IPI — Decreto nº 7.212 de 15/06/2010", "Decreto", "7212", "2010-06-15",
     "Regulamenta a cobrança, fiscalização, arrecadação e administração do Imposto sobre Produtos Industrializados - IPI."),
    ("regulamentos", "regulamento-aduaneiro-decreto-6759-2009", "_ato2007-2010/2009/decreto/d6759.htm",
     "Regulamento Aduaneiro — Decreto nº 6.759 de 05/02/2009", "Decreto", "6759", "2009-02-05",
     "Regulamenta a administração das atividades aduaneiras e a fiscalização, o controle e a tributação das operações de comércio exterior."),
    ("regulamentos", "rps-decreto-3048-1999", "decreto/d3048.htm",
     "Regulamento da Previdência Social — Decreto nº 3.048 de 06/05/1999", "Decreto", "3048", "1999-05-06",
     "Aprova o Regulamento da Previdência Social e dá outras providências."),
    ("regulamentos", "processo-administrativo-fiscal-decreto-70235-1972", "decreto/d70235cons.htm",
     "Processo Administrativo Fiscal — Decreto nº 70.235 de 06/03/1972 (texto consolidado)",
     "Decreto", "70235", "1972-03-06",
     "Dispõe sobre o processo administrativo fiscal e dá outras providências."),
]


def yaml_str(v):
    return json.dumps(v if v is not None else "", ensure_ascii=False)


def baixar(limite, pasta, nome, rel, titulo, tipo, numero, data, ementa, refazer):
    md = os.path.join(RAIZ, pasta, data[:4], nome + ".md")
    if os.path.exists(md) and not refazer:
        return "pulado"
    url = BASE + rel
    limite.esperar()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=180) as r:
        bruto = r.read()
        ct = r.headers.get("Content-Type") or ""

    fonte = os.path.join(RAIZ, "_fonte", "planalto", nome + ".html.gz")
    os.makedirs(os.path.dirname(fonte), exist_ok=True)
    with gzip.open(fonte, "wb") as f:
        f.write(bruto)

    corpo = convert(decodificar(bruto, ct))
    cab = ["---", f"titulo: {yaml_str(titulo)}", f"tipo: {yaml_str(tipo)}", f"numero: {yaml_str(numero)}",
           f"data: {data}", f"ementa: {yaml_str(ementa)}", "revogada: false",
           "versao_texto: \"compilada (texto vigente)\"", f"fonte: {yaml_str(url)}",
           f"baixado_em: {dt.date.today().isoformat()}", "---", ""]
    os.makedirs(os.path.dirname(md), exist_ok=True)
    tmp = md + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(cab) + f"# {titulo}\n\n" + corpo)
    os.replace(tmp, md)
    return "ok"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--rps", type=float, default=1, help="o Planalto é lento e não gosta de pressa")
    a = ap.parse_args()
    limite = Limitador(a.rps)
    cont = {"ok": 0, "pulado": 0, "erro": 0}
    for doc in DOCUMENTOS:
        try:
            st = baixar(limite, *doc, refazer=a.refazer)
        except Exception as e:
            st = "erro"
            print(f"  erro em {doc[1]}: {str(e)[:120]}", flush=True)
        cont[st] += 1
        print(f"{st:7} {doc[0]}/{doc[1]}", flush=True)
    print("FIM", cont)


if __name__ == "__main__":
    main()
