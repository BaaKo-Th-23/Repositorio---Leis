"""Pernambuco — Alepe Legis (legis.alepe.pe.gov.br).

Índice: lista.aspx?tiponorma=N, um ano por vez (postback ASP.NET do seletor ddlAno).
Texto: texto.aspx?id=N&tipo=TEXTOATUALIZADO (quando existe) ou TEXTOORIGINAL; conteúdo em div#divTexto.
"""
import html as htmllib
import http.cookiejar
import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, UA, Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402

UF = "PE"
BASE = "https://legis.alepe.pe.gov.br"
TIPOS = {
    "13": ("emendas-constitucionais", "Emenda Constitucional", "ec"),
    "2": ("leis-complementares", "Lei Complementar", "lc"),
    "1": ("leis-ordinarias", "Lei Ordinária", "lei"),
    "11": ("decretos-lei", "Decreto-Lei", "dl"),
}
rede = Rede(rps=2)
LINHA = re.compile(
    r"nome-norma\"><a href='texto\.aspx\?id=(\d+)[^>]*>([^<]+)</a></span>\s*<span class=\"publicacao\">([^<]*)</span>(.*?)</tr>",
    re.S,
)


def listar_ano(op, tipo, ano, campos):
    dados = dict(campos, __EVENTTARGET="ctl00$conteudo$ddlAno", __EVENTARGUMENT="")
    dados["ctl00$conteudo$ddlAno"] = ano
    url = f"{BASE}/lista.aspx?tiponorma={tipo}"
    rede.limite.esperar()
    req = urllib.request.Request(
        url, data=urllib.parse.urlencode(dados).encode(), headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"}
    )
    return op.open(req, timeout=180).read().decode("utf-8", "replace")


def campos_ocultos(html):
    return {n: htmllib.unescape(v) for n, v in re.findall(r'<input type="hidden" name="([^"]+)" id="[^"]*" value="([^"]*)"', html)}


def linhas(html, tipo):
    for id_, nome, pub, resto in LINHA.findall(html):
        textos = re.findall(r"tipo=(TEXTO[A-Z]+)", resto)
        ementa = re.search(r'class="ementa-norma[^"]*">\s*<div class="fLeft">(.*?)</div>', resto, re.S)
        yield {
            "id": id_,
            "tipo": tipo,
            "nome": " ".join(htmllib.unescape(nome).split()),
            "publicacao": " ".join(htmllib.unescape(pub).split()),
            "textos": sorted(set(textos)),
            "ementa": " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", ementa.group(1))).split()) if ementa else "",
        }


def indice():
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "lista.json")
    if os.path.exists(arq):
        return json.load(open(arq, encoding="utf-8"))
    itens = {}
    for tipo in TIPOS:
        op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        rede.limite.esperar()
        pagina = op.open(urllib.request.Request(f"{BASE}/lista.aspx?tiponorma={tipo}", headers={"User-Agent": UA}), timeout=180)
        html = pagina.read().decode("utf-8", "replace")
        anos = re.findall(r'<option[^>]*value="(\d{4})"', html.split('id="ddlAno"', 1)[1].split("</select>", 1)[0]) if 'id="ddlAno"' in html else []
        if not anos:
            for it in linhas(html, tipo):
                itens[it["id"]] = it
        for ano in anos:
            h = listar_ano(op, tipo, ano, campos_ocultos(html))
            for it in linhas(h, tipo):
                it["ano"] = ano
                itens[it["id"]] = it
        print(f"[{UF}] índice tipo {tipo}: {sum(1 for i in itens.values() if i['tipo'] == tipo)}", flush=True)
    lista = list(itens.values())
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False)
    return lista


def processar(it):
    pasta, nome, prefixo = TIPOS[it["tipo"]]
    num = re.search(r"n[°º]\s*([\d.]+)", it["nome"])
    numero = num.group(1).replace(".", "") if num else "sn"
    ano = it.get("ano") or "sem-ano"
    slug = f"{prefixo}-{numero}-{ano}-id{it['id']}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    tipo_txt = "TEXTOATUALIZADO" if "TEXTOATUALIZADO" in it["textos"] else "TEXTOORIGINAL"
    url = f"{BASE}/texto.aspx?id={it['id']}&tipo={tipo_txt}"
    st, bruto, ctype = rede.get(url, timeout=180)
    if st != 200:
        return "sem_texto", {"id": it["id"], "http": st}
    html = decodificar(bruto, ctype)
    ini = html.find('id="divTexto"')
    if ini < 0:
        return "sem_texto", {"id": it["id"], "motivo": "sem divTexto"}
    fim = html.find('id="nota"', ini)
    trecho = html[html.find(">", ini) + 1 : fim if fim > 0 else None]
    corpo = html_para_md(trecho)
    if len(re.sub(r"\W", "", corpo)) < 40:
        return "sem_texto", {"id": it["id"], "motivo": "texto vazio"}
    data = re.search(r"(\d{2})/(\d{2})/(\d{4})", it["publicacao"])
    titulo = it["nome"]
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", num.group(1) if num else ""),
        ("ano", ano),
        ("ementa", it["ementa"]),
        ("publicacao", it["publicacao"]),
        ("data_publicacao", f"{data.group(3)}-{data.group(2)}-{data.group(1)}" if data else ""),
        ("versao_texto", "atualizada" if tipo_txt == "TEXTOATUALIZADO" else "original"),
        ("fonte", url),
    ]
    gravar(md, fonte, trecho, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice()
    itens.sort(key=lambda i: (i.get("ano") or "", int(i["id"])), reverse=True)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    if len(sys.argv) > 1:
        itens = itens[: int(sys.argv[1])]
    executar(UF, itens, processar, workers=2)
