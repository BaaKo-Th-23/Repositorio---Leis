"""Distrito Federal — SINJ-DF (Sistema Integrado de Normas Jurídicas do DF).

Índice: ResultadoDePesquisaNormaDatatable.ashx filtrando por tipo (Lei, LC, Lei Orgânica, Emendas, Decreto-Lei).
Texto: /sinj/Norma/{ch_norma}/{arquivo}, preferindo o texto compilado (ar_atualizado).
"""
import json
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, documento_para_md, executar, gravar  # noqa: E402

UF = "DF"
BASE = "https://www.sinj.df.gov.br/sinj"
TIPOS = {
    "48000000": ("lei-organica", "Lei Orgânica", "lodf"),
    "36000000": ("emendas-lei-organica", "Emenda à Lei Orgânica", "elo"),
    "47000000": ("leis-complementares", "Lei Complementar", "lc"),
    "46000000": ("leis-ordinarias", "Lei Ordinária", "lei"),
    "30000000": ("decretos-lei", "Decreto-Lei", "dl"),
}
rede = Rede(rps=3)


def post_datatable(ch_tipo, inicio, tamanho):
    import urllib.request

    url = f"{BASE}/ashx/Datatable/ResultadoDePesquisaNormaDatatable.ashx?tipo_pesquisa=norma&ch_tipo_norma={ch_tipo}"
    corpo = urllib.parse.urlencode(
        {"bbusca": "sinj_norma", "sEcho": "1", "iDisplayStart": inicio, "iDisplayLength": tamanho}
    ).encode()
    rede.limite.esperar()
    req = urllib.request.Request(url, data=corpo, headers={**rede.headers, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        dados = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            import gzip

            dados = gzip.decompress(dados)
    return json.loads(dados)


def indice():
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "sinj.json")
    if os.path.exists(arq):
        return json.load(open(arq, encoding="utf-8"))
    normas = {}
    for ch, (_, nome, _) in TIPOS.items():
        inicio = 0
        while True:
            d = post_datatable(ch, inicio, 1000)
            lote = [x["_source"] for x in d.get("aaData") or []]
            for s in lote:
                if s.get("nm_tipo_norma") == nome:
                    s["_ch_tipo"] = ch
                    normas[s["ch_norma"]] = s
            inicio += len(lote)
            if not lote or inicio >= int(d.get("iTotalDisplayRecords") or 0):
                break
        print(f"[{UF}] índice {nome}: {sum(1 for s in normas.values() if s['_ch_tipo'] == ch)}", flush=True)
    itens = list(normas.values())
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False)
    return itens


def arquivo_texto(s):
    """Prefere o texto compilado; senão, o arquivo da publicação mais recente."""
    at = s.get("ar_atualizado") or {}
    if at.get("filename"):
        return at["filename"], True
    for f in reversed(s.get("fontes") or []):
        ar = f.get("ar_fonte") or {}
        if ar.get("filename"):
            return ar["filename"], False
    return None, False


def processar(s):
    pasta, nome, prefixo = TIPOS[s["_ch_tipo"]]
    d, m, a = (s.get("dt_assinatura") or "01/01/0000").split("/")
    numero = s.get("nr_norma") or ""
    slug = f"{prefixo}-{numero or 'sn'}-{a}-{m}-{d}"
    if s.get("nr_sequencial"):
        slug += f"-s{s['nr_sequencial']}"
    md, fonte = caminhos(UF, pasta, a, slug)
    if os.path.exists(md):
        return "pulado", None
    nome_arq, compilado = arquivo_texto(s)
    if not nome_arq:
        return "sem_texto", {"ch": s["ch_norma"], "motivo": "sem arquivo"}
    url = f"{BASE}/Norma/{s['ch_norma']}/{urllib.parse.quote(nome_arq)}"
    st, bruto, ctype = rede.get(url, timeout=180)
    if st != 200 or not bruto:
        return "sem_texto", {"ch": s["ch_norma"], "url": url, "http": st}
    corpo, motivo = documento_para_md(bruto, url, ctype, {"Texto Compilado", "Texto Original"})
    if corpo is None:
        return "sem_texto", {"ch": s["ch_norma"], "url": url, "motivo": motivo}
    titulo = "Lei Orgânica do Distrito Federal" if nome == "Lei Orgânica" else f"{nome} nº {numero}, de {d}/{m}/{a}"
    situacao = s.get("nm_situacao") or ""
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", numero),
        ("data", f"{a}-{m}-{d}"),
        ("ementa", " ".join((s.get("ds_ementa") or "").split())),
        ("situacao", situacao),
        ("revogada", situacao.lower().startswith("revogad")),
        ("versao_texto", "compilada (SINJ-DF)" if compilado else "original"),
        ("fonte", f"{BASE}/Norma/{s['ch_norma']}/{nome_arq}"),
    ]
    gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice()
    itens.sort(key=lambda s: "".join(reversed((s.get("dt_assinatura") or "").split("/"))), reverse=True)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    if len(sys.argv) > 1:
        itens = itens[: int(sys.argv[1])]
    executar(UF, itens, processar, workers=3)
