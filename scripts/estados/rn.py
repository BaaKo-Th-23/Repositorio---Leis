"""Rio Grande do Norte — Assembleia Legislativa (www.al.rn.leg.br/legislacao).

Índice: páginas /legislacao/leis-ordinarias?page=N e /legislacao/leis-complementares?page=N (agrupadas por ano).
Texto: PDF de cada lei (storage/legislacao/...). O acervo do site começa em 1994.
"""
import html as htmllib
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, documento_para_md, executar, gravar  # noqa: E402

UF = "RN"
B = "https://www.al.rn.leg.br"
LISTAS = {
    "leis-ordinarias": ("leis-ordinarias", "Lei Ordinária", "lei"),
    "leis-complementares": ("leis-complementares", "Lei Complementar", "lc"),
}
CONSTITUICAO = f"{B}/documentos/Constituicao_Estadual-2023 - 2024.pdf"
ITEM = re.compile(r"<li class=\"list-group-item\">\s*<a href='([^']+)'[^>]*>\s*(?:<i[^>]*></i>)?\s*(.*?)</a>\s*(?:<br\s*/?>)?(.*?)</li>", re.S)
rede = Rede(rps=3)


def limpar(s):
    return " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def indice():
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "listas.json")
    if os.path.exists(arq):
        return json.load(open(arq, encoding="utf-8"))
    itens = {}
    for lista in LISTAS:
        p = 1
        while True:
            st, dados, ctype = rede.get(f"{B}/legislacao/{lista}?page={p}", timeout=300)
            html = decodificar(dados, ctype) if st == 200 else ""
            achados = ITEM.findall(html)
            for href, titulo, ementa in achados:
                titulo = limpar(titulo)
                if href.lower().endswith(".pdf") and not titulo.lower().startswith("razões de veto"):
                    itens[href] = {"lista": lista, "url": href, "titulo": titulo, "ementa": limpar(ementa)}
            ultima = max([int(x) for x in re.findall(rf"{lista}\?page=(\d+)", html)] or [p])
            if p >= ultima:
                break
            p += 1
        print(f"[{UF}] índice {lista}: {sum(1 for i in itens.values() if i['lista'] == lista)}", flush=True)
    lista = list(itens.values()) + [{"lista": "constituicao", "url": CONSTITUICAO, "titulo": "Constituição do Estado do Rio Grande do Norte", "ementa": ""}]
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False)
    return lista


def processar(it):
    if it["lista"] == "constituicao":
        pasta, nome, prefixo = "constituicao", "Constituição Estadual", "ce"
        numero, data, ano, slug = "", "1989-10-03", "1989", "constituicao-rn"
    else:
        pasta, nome, prefixo = LISTAS[it["lista"]]
        m = re.search(r"([\d.]+)\s+de\s+(\d{1,2})\.(\d{1,2})\.(\d{4})", it["titulo"])
        numero = m.group(1) if m else ""
        data = f"{m.group(4)}-{int(m.group(3)):02d}-{int(m.group(2)):02d}" if m else ""
        ano = data[:4] or (re.search(r"/(\d{4})/", it["url"]) or [None, "sem-ano"])[1]
        slug = f"{prefixo}-{numero.replace('.', '') or 'sn'}-{data or ano}-{os.path.splitext(os.path.basename(it['url']))[0][-10:]}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    url = it["url"].replace(" ", "%20")
    st, doc, ctype = rede.get(url, timeout=300)
    if st != 200 or not doc:
        return "sem_texto", {"url": url, "http": st}
    corpo, motivo = documento_para_md(doc, url, ctype)
    if corpo is None:
        return "sem_texto", {"url": url, "titulo": it["titulo"], "motivo": motivo}
    titulo = it["titulo"]
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", numero),
        ("data", data),
        ("ementa", it["ementa"]),
        ("versao_texto", "PDF da Assembleia Legislativa"),
        ("fonte", url),
    ]
    gravar(md, fonte, doc, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice()
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    if len(sys.argv) > 1:
        itens = itens[: int(sys.argv[1])]
    executar(UF, itens, processar, workers=3)
