"""Santa Catarina — Legislação SC (ALESC, leis.alesc.sc.gov.br).

Não há índice estruturado público: percorre os IDs de /ato-normativo/legislativo/{id}, que devolvem o
documento (Word convertido, com anotações de alterações) e classifica pelo título.
"""
import html as htmllib
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402

UF = "SC"
BASE = "https://leis.alesc.sc.gov.br"
ID_MAX = 56000
# (regex do título, pasta, nome, prefixo) — a ordem importa
TIPOS = [
    (r"^CONSTITUI", "constituicao", "Constituição Estadual", "ce"),
    (r"^EMENDA", "emendas-constitucionais", "Emenda Constitucional", "ec"),
    (r"^LEI COMPLEMENTAR", "leis-complementares", "Lei Complementar", "lc"),
    (r"^LEI DELEGADA", "leis-delegadas", "Lei Delegada", "ld"),
    (r"^DECRETO[- ]LEI", "decretos-lei", "Decreto-Lei", "dl"),
    (r"^LEI\b", "leis-ordinarias", "Lei Ordinária", "lei"),
]
MESES = {m: i for i, m in enumerate(
    "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split(), 1)}
MESES["marco"] = 3
rede = Rede(rps=3)


def classificar(titulo):
    t = titulo.upper()
    for rx, pasta, nome, prefixo in TIPOS:
        if re.match(rx, t):
            return pasta, nome, prefixo
    return None


def data_do_texto(texto):
    m = re.search(r"de (\d{1,2})[ºo°]? de ([a-zçA-ZÇ]+) de (\d{4})", texto[:1500], re.I)
    if m and m.group(2).lower() in MESES:
        return f"{m.group(3)}-{MESES[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    return ""


def processar(id_):
    url = f"{BASE}/ato-normativo/legislativo/{id_}"
    st, bruto, ctype = rede.get(url, timeout=180)
    if st == 404:
        return "inexistente", None
    if st != 200 or not bruto:
        return "sem_texto", {"id": id_, "http": st}
    html = decodificar(bruto, ctype)
    # a ALESC usa <s> para o "º/°" sobrescrito, não para texto riscado
    html = re.sub(r"<s>\s*(&deg;|&ordm;|&ordf;|°|º|ª|o|a)\s*</s>", r"\1", html)
    m = re.search(r'<meta name="dc:title" content="([^"]*)"', html)
    titulo = " ".join(htmllib.unescape(m.group(1)).split()) if m else ""
    corpo = html_para_md(html)
    if not titulo:
        titulo = re.sub(r"[*\\]", "", corpo.strip().split("\n", 1)[0])[:150]
    tipo = classificar(titulo) or classificar(re.sub(r"[*\\]", "", corpo.strip())[:80])
    if not tipo:
        return "fora_escopo", None
    pasta, nome, prefixo = tipo
    texto_plano = re.sub(r"[*\\#]", "", corpo)
    data = data_do_texto(texto_plano)
    ano = data[:4] or "sem-ano"
    num = re.search(r"N[º°o.]*\s*([\d.]+)", titulo, re.I)
    numero = num.group(1).replace(".", "") if num else ""
    slug = f"{prefixo}-{numero or 'sn'}-{ano}-id{id_}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    if len(re.sub(r"\W", "", corpo)) < 40:
        return "sem_texto", {"id": id_, "motivo": "texto vazio"}
    cabeca = texto_plano[:800].upper()
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", num.group(1) if num else ""),
        ("data", data),
        ("revogada", "lei-revogada" in html[:20000] or bool(re.search(r"\bREVOGAD[AO] (PELA|PELO|INTEGRALMENTE)", cabeca))),
        ("versao_texto", "texto anotado da ALESC"),
        ("fonte", f"{BASE}/ato-normativo/{id_}"),
    ]
    gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    ids = list(range(ID_MAX, 0, -1))
    if len(sys.argv) > 1:
        ids = [int(x) for x in sys.argv[1].split(",")] if "," in sys.argv[1] else ids[-int(sys.argv[1]):]
    executar(UF, ids, processar, workers=3)
