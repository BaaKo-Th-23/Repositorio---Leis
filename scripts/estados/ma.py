"""Maranhão — GED da Assembleia Legislativa (arquivos.al.ma.leg.br:8443/ged/legislacao/{TIPO}_{numero}).

Não há índice público completo: percorre a numeração de cada tipo (os inexistentes dão 404).
Texto: PDF (OCR quando escaneado). Título, data e ementa saem do próprio texto.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import Rede, caminhos, documento_para_md, executar, gravar  # noqa: E402

UF = "MA"
B = "https://arquivos.al.ma.leg.br:8443/ged/legislacao"
# prefixo no GED -> (pasta, nome, maior número a tentar)
TIPOS = {
    "EC": ("emendas-constitucionais", "Emenda Constitucional", 150),
    "LC": ("leis-complementares", "Lei Complementar", 400),
    "LEI": ("leis-ordinarias", "Lei Ordinária", 13500),
}
MESES = {m: i for i, m in enumerate(
    "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split(), 1)}
MESES["marco"] = 3
rede = Rede(rps=3)


def processar(item):
    prefixo, numero = item
    pasta, nome, _ = TIPOS[prefixo]
    url = f"{B}/{prefixo}_{numero}"
    st, doc, ctype = rede.get(url, timeout=300)
    if st == 404:
        return "inexistente", None
    if st != 200 or not doc:
        return "sem_texto", {"norma": f"{prefixo}_{numero}", "http": st}
    corpo, motivo = documento_para_md(doc, url, ctype)
    if corpo is None:
        return "sem_texto", {"norma": f"{prefixo}_{numero}", "url": url, "motivo": motivo}
    plano = re.sub(r"[*\\#>]", "", corpo)
    cab = re.search(
        r"((?:LEI COMPLEMENTAR|EMENDA CONSTITUCIONAL|EMENDA À CONSTITUIÇÃO|LEI)[^\n]{0,20}?N[º°o.]*\s*[\d.]+[^\n]{0,15}?"
        r"(\d{1,2})[º°]?\s+DE\s+([A-ZÇa-zç]+)\s+DE\s+(\d{4}))",
        plano, re.I,
    )
    data = ""
    if cab and cab.group(3).lower() in MESES:
        data = f"{cab.group(4)}-{MESES[cab.group(3).lower()]:02d}-{int(cab.group(2)):02d}"
    if not cab:  # emendas: "EMENDA CONSTITUCIONAL Nº 090/2020"
        cab = re.search(r"(EMENDA CONSTITUCIONAL|LEI COMPLEMENTAR|LEI)\s*N[º°o.]*\s*0*%s\s*/\s*(\d{4})" % numero, plano, re.I)
    ano = data[:4] or (cab.group(2) if cab and cab.lastindex == 2 else "") or "sem-ano"
    titulo = f"{nome} nº {numero}" + (f", de {data[8:10]}/{data[5:7]}/{data[:4]}" if data else "")
    md, fonte = caminhos(UF, pasta, ano, f"{prefixo.lower()}-{numero}-{ano}")
    if os.path.exists(md):
        return "pulado", None
    # ementa: primeiro parágrafo depois do cabeçalho que não seja fórmula de promulgação
    ementa = ""
    if cab:
        resto = plano[cab.end():].split("\n\n")
        for p in resto:
            p = " ".join(p.split()).lstrip(".,;:- ")
            if len(p) > 20 and not re.match(r"(O|A) (GOVERNADOR|GOVERNADORA|PRESIDENTE|MESA)|Faço saber", p, re.I):
                ementa = p[:600]
                break
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", str(numero)),
        ("data", data),
        ("ementa", ementa),
        ("versao_texto", "PDF do GED da Assembleia Legislativa"),
        ("fonte", url),
    ]
    gravar(md, fonte, doc, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = [(p, n) for p, (_, _, maximo) in TIPOS.items() for n in range(maximo, 0, -1)]
    if len(sys.argv) > 1:
        itens = [tuple(x.split("_")) for x in sys.argv[1].split(",")]
        itens = [(p, int(n)) for p, n in itens]
    executar(UF, itens, processar, workers=3)
