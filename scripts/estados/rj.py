"""Rio de Janeiro — Legislação Estadual da ALERJ (Lotus Notes, alerjln1.alerj.rj.gov.br/contlei.nsf).

O servidor é muito lento (≈1 min por página) e instável: timeouts longos, poucas requisições em paralelo,
índice salvo página a página para retomar.
Índice: formulários LeiOrdInt / LeiCompInt / EmendaInt com Start/Count.
Texto: documento ?OpenDocument (texto da lei com situação).
"""
import html as htmllib
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402

UF = "RJ"
H = "http://alerjln1.alerj.rj.gov.br"
B = f"{H}/contlei.nsf"
FORMS = {
    "EmendaInt": ("emendas-constitucionais", "Emenda Constitucional", "ec"),
    "LeiCompInt": ("leis-complementares", "Lei Complementar", "lc"),
    "LeiOrdInt": ("leis-ordinarias", "Lei Ordinária", "lei"),
}
POR_PAGINA = 30  # páginas maiores derrubam a conexão
LINHA = re.compile(r'href="(/contlei\.nsf/[0-9a-f]+/[0-9a-f]+\?OpenDocument)"[^>]*>(.*?)</a>(.*?)</tr>', re.S | re.I)
rede = Rede(rps=1)


def limpar(s):
    return " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def indice():
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice", "paginas")
    os.makedirs(pasta, exist_ok=True)
    itens = {}
    for form in FORMS:
        inicio = 1
        while True:
            cache = os.path.join(pasta, f"{form}-{inicio}.json")
            if os.path.exists(cache):
                linhas = json.load(open(cache, encoding="utf-8"))
            else:
                for rodada in range(10):  # servidor instável: espera e tenta de novo
                    try:
                        st, dados, ctype = rede.get(f"{B}/{form}?OpenForm&Start={inicio}&Count={POR_PAGINA}", timeout=900, tentativas=3)
                        if st == 200:
                            break
                    except RuntimeError:
                        pass
                    time.sleep(300)
                else:
                    raise RuntimeError(f"{form} Start={inicio}: indisponível")
                linhas = []
                for href, numero, resto in LINHA.findall(decodificar(dados, ctype)):
                    cels = [limpar(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", resto, re.S)]
                    linhas.append({"form": form, "href": href, "numero": limpar(numero), "colunas": cels})
                json.dump(linhas, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
            for ln in linhas:
                itens[ln["href"]] = ln
            print(f"[{UF}] índice {form} a partir de {inicio}: +{len(linhas)} (total {len(itens)})", flush=True)
            if len(linhas) < POR_PAGINA:
                break
            inicio += POR_PAGINA
    return list(itens.values())


def processar(it):
    pasta, nome, prefixo = FORMS[it["form"]]
    cols = it["colunas"]
    ano = next((c for c in cols if re.fullmatch(r"(18|19|20)\d\d", c)), "sem-ano")
    numero = re.sub(r"\D", "", it["numero"])
    unid = it["href"].split("/")[-1].split("?")[0]
    md, fonte = caminhos(UF, pasta, ano, f"{prefixo}-{numero or 'sn'}-{ano}-{unid[:10]}")
    if os.path.exists(md):
        return "pulado", None
    url = H + it["href"]
    st, bruto, ctype = rede.get(url, timeout=900, tentativas=6)
    if st != 200 or not bruto:
        return "sem_texto", {"url": url, "http": st}
    html = decodificar(bruto, ctype)
    corpo = html_para_md(html)
    if len(re.sub(r"\W", "", corpo)) < 40:
        return "sem_texto", {"url": url, "motivo": "texto vazio"}
    plano = re.sub(r"[*\\#]", "", corpo)
    situacao = re.search(r"\[\s*([^\]]{3,40})\s*\]", plano[:1500])
    data = re.search(r"Data da Lei\s*(\d{2})/(\d{2})/(\d{4})", plano)
    ementa = next((c for c in cols if len(c) > 30), "")
    titulo = f"{nome} nº {it['numero']}" + (f"/{ano}" if ano != "sem-ano" else "")
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", it["numero"]),
        ("data", f"{data.group(3)}-{data.group(2)}-{data.group(1)}" if data else ""),
        ("ementa", ementa),
        ("situacao", situacao.group(1).strip() if situacao else ""),
        ("revogada", bool(situacao and situacao.group(1).strip().lower().startswith("revogad"))),
        ("versao_texto", "texto da base de legislação da ALERJ"),
        ("fonte", url),
    ]
    gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice()
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    if len(sys.argv) > 1:
        itens = itens[: int(sys.argv[1])]
    executar(UF, itens, processar, workers=3)
