"""Minas Gerais — ALMG (dadosabertos.almg.gov.br).

Índice: CSV anual da "Legislação mineira" (desde 1947), com links para texto original e atualizado.
Texto: API v2 da ALMG; XML com o HTML da norma em <conteudo>.
"""
import csv
import datetime as dt
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, executar, gravar, html_para_md  # noqa: E402

UF = "MG"
CSV_URL = "https://dadosabertos.almg.gov.br/arquivo/legislacao-mineira/download?ano={}"
TIPOS = {
    "CON": ("constituicao", "Constituição Estadual"),
    "EMC": ("emendas-constitucionais", "Emenda Constitucional"),
    "LCO": ("leis-constitucionais", "Lei Constitucional"),
    "LCP": ("leis-complementares", "Lei Complementar"),
    "LEI": ("leis-ordinarias", "Lei Ordinária"),
    "LDL": ("leis-delegadas", "Lei Delegada"),
    "LEA": ("leis-adicionais", "Lei Adicional"),
    "DEL": ("decretos-lei", "Decreto-Lei"),
}
rede = Rede(rps=4)


def indice():
    itens = []
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    os.makedirs(pasta, exist_ok=True)
    for ano in range(1947, dt.date.today().year + 1):
        arq = os.path.join(pasta, f"{ano}.csv")
        if not os.path.exists(arq):
            st, dados, _ = rede.get(CSV_URL.format(ano))
            if st != 200 or not dados.strip():
                continue
            with open(arq, "wb") as f:
                f.write(dados)
        with open(arq, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["Tipo"] in TIPOS:
                    itens.append(r)
    return itens


def processar(r):
    pasta, nome = TIPOS[r["Tipo"]]
    comp = f"-{r['Complemento']}" if r["Complemento"] else ""
    slug = f"{r['Tipo'].lower()}-{r['Numero']}{comp}-{r['Ano']}"
    md, fonte = caminhos(UF, pasta, r["Ano"], slug)
    if os.path.exists(md):
        return "pulado", None
    url = r["LinkTextoAtualizado"] or r["LinkTextoOriginal"]
    if not url:
        return "sem_texto", {"norma": slug, "motivo": "sem link"}
    st, dados, _ = rede.get(url, "application/xml")
    if st != 200 or not dados:
        return "sem_texto", {"norma": slug, "url": url, "http": st}
    conteudo = ET.fromstring(dados).findtext(".//conteudo") or ""
    if not conteudo.strip():
        return "sem_texto", {"norma": slug, "url": url, "motivo": "conteúdo vazio"}
    corpo = html_para_md(conteudo)
    d, m, a = r["DataLegislacao"].split("/") if r["DataLegislacao"] else ("", "", "")
    numero = r["Numero"] + (f"-{r['Complemento']}" if r["Complemento"] else "")
    titulo = f"{nome} nº {numero}, de {r['DataLegislacao']}" if r["Tipo"] != "CON" else f"Constituição do Estado de Minas Gerais ({r['Ano']})"
    situacao = (r.get("Situacao") or "").strip()
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", numero),
        ("data", f"{a}-{m}-{d}" if a else ""),
        ("ementa", " ".join((r["Ementa"] or "").split())),
        ("situacao", situacao.capitalize()),
        ("revogada", situacao.upper().startswith("REVOGAD")),
        ("versao_texto", "atualizada" if r["LinkTextoAtualizado"] else "original"),
        ("fonte", url.replace("conteudo=true&", "")),
    ]
    gravar(md, fonte, conteudo, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice()
    itens.sort(key=lambda r: (r["Ano"], r["DataLegislacao"][3:5], r["DataLegislacao"][:2]), reverse=True)
    if len(sys.argv) > 1:
        itens = itens[: int(sys.argv[1])]
    executar(UF, itens, processar)
