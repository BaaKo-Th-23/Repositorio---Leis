"""Paraná — Sistema Estadual de Legislação (Casa Civil, legislacao.pr.gov.br).

Índice: listarAtosAno.do?action=listarAtos&anoAto=AAAA (POST com codTipoAto), um ano por vez.
Texto: pesquisarAto.do?action=exibir&codAto=N&tipoVisualizacao=compilado (texto compilado).
"""
import html as htmllib
import http.cookiejar
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, UA, Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402

UF = "PR"
B = "https://www.legislacao.pr.gov.br/legislacao"
TIPOS = {
    "10": ("constituicao", "Constituição Estadual", "ce"),
    "9": ("emendas-constitucionais", "Emenda Constitucional", "ec"),
    "3": ("leis-complementares", "Lei Complementar", "lc"),
    "1": ("leis-ordinarias", "Lei Ordinária", "lei"),
}
rede = Rede(rps=1)  # o servidor bloqueou (403) com ritmo maior
_sessao = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
LINHA = re.compile(
    r"codAto=(\d+)&indice.*?_epigrafeAto\">(.*?)</div>.*?_descricaoItemAto\">(.*?)</div>.*?_dataPublicacao\">(.*?)</div>",
    re.S,
)
MESES = {m: i for i, m in enumerate(
    "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split(), 1)}


def limpar(s):
    return " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def post(caminho, dados, tentativas=4):
    req = urllib.request.Request(f"{B}/{caminho}", data=urllib.parse.urlencode(dados).encode(), headers={"User-Agent": UA})
    for n in range(tentativas):
        rede.limite.esperar()
        try:
            with _sessao.open(req, timeout=300) as r:
                return decodificar(r.read(), r.headers.get("Content-Type") or "")
        except Exception:
            if n == tentativas - 1:
                raise
            time.sleep(30 * (n + 1))


def indice():
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "atos.json")
    if os.path.exists(arq):
        return json.load(open(arq, encoding="utf-8"))
    itens = {}
    for tipo in TIPOS:
        st, dados, ctype = rede.get(f"{B}/listarAtosAno.do?action=iniciarProcesso&tipoAto={tipo}&orgaoUnidade=1100&retiraLista=true&site=1")
        html = decodificar(dados, ctype)
        anos = sorted({a for _, a in re.findall(r"listarAtos\('(\d{4})', '(\d{4})'\)", html)}, reverse=True)
        if not anos:  # tipo com um único ato (Constituição): a página já é o próprio ato
            for cod in dict.fromkeys(re.findall(r'name="codAto" value="(\d+)"', html)):
                itens[cod] = {"codAto": cod, "tipo": tipo, "epigrafe": "", "ementa": "", "publicacao": ""}
        for ano in anos:
            h = post(
                f"listarAtosAno.do?action=listarAtos&anoAto={ano}&isPaginado=false",
                dict(codTipoAto=tipo, codTipoAtoSelecionado=tipo, codOrgaoUnidade="1100", codOrgaoUnidadeSelecionado="1100",
                     pesquisou="", anoAtoPesquisado="0", paginaAtual="", isPaginado="false", site="1"),
            )
            for cod, epi, ementa, pub in LINHA.findall(h):
                itens[cod] = {"codAto": cod, "tipo": tipo, "ano": ano, "epigrafe": limpar(epi), "ementa": limpar(ementa), "publicacao": limpar(pub)}
        print(f"[{UF}] índice tipo {tipo}: {sum(1 for i in itens.values() if i['tipo'] == tipo)}", flush=True)
    lista = list(itens.values())
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False)
    return lista


def processar(it):
    pasta, nome, prefixo = TIPOS[it["tipo"]]
    url = f"{B}/pesquisarAto.do?action=exibir&codAto={it['codAto']}&codTipoAto=&tipoVisualizacao=compilado"
    epi = it.get("epigrafe") or ""
    num = re.search(r"([\d.]+)\s*-\s*(\d{1,2}) de (\w+) de (\d{4})", epi)
    ano = it.get("ano") or (num.group(4) if num else "sem-ano")
    numero = num.group(1).replace(".", "") if num else "sn"
    slug = f"{prefixo}-{numero}-{ano}-id{it['codAto']}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    st, bruto, ctype = rede.get(url, timeout=300)
    if st != 200:
        return "sem_texto", {"codAto": it["codAto"], "http": st}
    html = decodificar(bruto, ctype)
    ini = html.find("<h3>")
    fim = html.find("</form>", ini)
    if ini < 0:
        return "sem_texto", {"codAto": it["codAto"], "motivo": "sem texto"}
    trecho = html[ini : fim if fim > 0 else None]
    titulo = limpar(re.search(r"<h3>(.*?)</h3>", trecho, re.S).group(1)) or epi
    corpo = html_para_md(trecho)
    if len(re.sub(r"\W", "", corpo)) < 40:
        return "sem_texto", {"codAto": it["codAto"], "motivo": "texto vazio"}
    data = ""
    m = re.search(r"(\d{1,2}) de (\w+) de (\d{4})", titulo)
    if m and m.group(2).lower() in MESES:
        data = f"{m.group(3)}-{MESES[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", num.group(1) if num else ""),
        ("data", data),
        ("ementa", it.get("ementa") or ""),
        ("versao_texto", "compilada (Casa Civil do Paraná)"),
        ("fonte", url),
    ]
    gravar(md, fonte, trecho, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice()
    itens.sort(key=lambda i: (i.get("ano") or "", int(i["codAto"])), reverse=True)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    if len(sys.argv) > 1:
        itens = itens[: int(sys.argv[1])]
    executar(UF, itens, processar, workers=3)
