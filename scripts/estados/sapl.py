"""Assembleias que usam o SAPL (Interlegis): índice pela API REST e texto do PDF/arquivo anexado.

Uso:
  python3 -I scripts/estados/sapl.py indice AM        # baixa o índice e mostra a cobertura
  python3 -I scripts/estados/sapl.py baixar AM [N]    # baixa e converte os textos
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import (  # noqa: E402
    RAIZ_ESTADUAIS, Rede, _ACENTOS, caminhos, canonico, documento_para_md, executar, gravar,
)

HOSTS = {
    "AM": "sapl.al.am.leg.br",
    "PB": "sapl.al.pb.leg.br",
    "AL": "sapl.al.al.leg.br",
    "RR": "sapl.al.rr.leg.br",
    "AC": "sapl.al.ac.leg.br",
    "RO": "sapl.al.ro.leg.br",
    "PI": "sapl.al.pi.leg.br",
    "TO": "sapl.al.to.leg.br",
}
# siglas/descrições de tipos que contam como "lei" (constituição, emendas, leis e decretos-lei)
TIPO_LEI = re.compile(r"constitui|emenda|\blei\b|decreto[- ]lei", re.I)
TIPO_EXCLUIR = re.compile(r"projeto|veto|resolu|regimento|decreto legislativo|portaria|ato da mesa", re.I)
rede = Rede(rps=3)


def api(uf, caminho):
    st, dados, _ = rede.get(f"https://{HOSTS[uf]}/api/{caminho}", "application/json")
    if st != 200:
        raise RuntimeError(f"{uf} {caminho}: HTTP {st}")
    return json.loads(dados)


def tipos_lei(uf):
    tipos = {}
    pag = 1
    while True:
        d = api(uf, f"norma/tiponormajuridica/?page_size=100&page={pag}")
        for t in d["results"]:
            desc = t["descricao"].strip()
            if TIPO_LEI.search(desc) and not TIPO_EXCLUIR.search(desc):
                tipos[t["id"]] = desc
        if not d["pagination"].get("next_page"):
            return tipos
        pag += 1


def indice(uf):
    pasta = os.path.join(RAIZ_ESTADUAIS, uf, "_indice")
    arq = os.path.join(pasta, "sapl.json")
    if os.path.exists(arq):
        return json.load(open(arq, encoding="utf-8"))
    tipos = tipos_lei(uf)
    normas = []
    for tid in tipos:
        pag = 1
        while True:
            d = api(uf, f"norma/normajuridica/?tipo={tid}&page_size=100&page={pag}")
            normas += d["results"]
            if not d["pagination"].get("next_page"):
                break
            pag += 1
    os.makedirs(pasta, exist_ok=True)
    dados = {"tipos": {str(k): v for k, v in tipos.items()}, "normas": normas}
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)
    return dados


def cobertura(uf):
    d = indice(uf)
    por_tipo = collections.defaultdict(lambda: [0, 0])
    for n in d["normas"]:
        t = d["tipos"][str(n["tipo"])]
        por_tipo[t][0] += 1
        por_tipo[t][1] += bool(n.get("texto_integral"))
    anos = [n["ano"] for n in d["normas"] if n.get("texto_integral")]
    print(f"{uf}: {len(d['normas'])} normas; com arquivo: {sum(v[1] for v in por_tipo.values())}"
          f" (anos {min(anos) if anos else '-'}–{max(anos) if anos else '-'})")
    for t, (tot, com) in sorted(por_tipo.items(), key=lambda x: -x[1][0]):
        print(f"   {t}: {tot} ({com} com arquivo)")


def processar_factory(uf, tipos):
    def processar(n):
        bruto = tipos[str(n["tipo"])]
        pasta, tipo = canonico(bruto)
        # o prefixo do nome do arquivo vem do nome que a Assembleia usa, não do canônico:
        # os arquivos já gravados se chamam lei-ordinaria-N-AAAA-idX.md e precisam ser
        # reconhecidos como existentes numa nova rodada.
        prefixo = re.sub(r"[^a-z0-9]+", "-", bruto.translate(_ACENTOS).lower()).strip("-")
        slug = f"{prefixo}-{n['numero'] or 'sn'}-{n['ano']}-id{n['id']}"
        md, fonte = caminhos(uf, pasta, n["ano"], slug)
        if os.path.exists(md):
            return "pulado", None
        url = n.get("texto_integral")
        if not url:
            return "sem_texto", {"id": n["id"], "norma": n["__str__"], "motivo": "sem arquivo"}
        url = url.replace("http://", "https://")
        st, bruto, _ = rede.get(url)
        if st != 200 or not bruto:
            return "sem_texto", {"id": n["id"], "url": url, "http": st}
        corpo, motivo = documento_para_md(bruto, url)
        if corpo is None:
            return "sem_texto", {"id": n["id"], "url": url, "motivo": motivo}
        titulo = n["__str__"]
        meta = [
            ("titulo", titulo),
            ("uf", uf),
            ("tipo", tipo),
            ("numero", n.get("numero") or ""),
            ("data", n.get("data") or ""),
            ("ementa", " ".join((n.get("ementa") or "").split())),
            ("publicacao", n.get("veiculo_publicacao") or ""),
            ("versao_texto", "original (arquivo anexado ao SAPL)"),
            ("fonte", f"https://{HOSTS[uf]}/norma/{n['id']}"),
            ("arquivo", url),
        ]
        gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
        return "ok", None

    return processar


if __name__ == "__main__":
    acao, uf = sys.argv[1], sys.argv[2].upper()
    if acao == "indice":
        cobertura(uf)
    elif acao == "baixar":
        d = indice(uf)
        itens = sorted(d["normas"], key=lambda n: n.get("data") or "", reverse=True)
        if len(sys.argv) > 3:
            itens = itens[: int(sys.argv[3])]
        executar(uf, itens, processar_factory(uf, d["tipos"]), workers=3)
