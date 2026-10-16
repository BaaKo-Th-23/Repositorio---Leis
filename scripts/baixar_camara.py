"""Coleta resoluções da Câmara na busca oficial e textos Legin, com cache e retomada.

    python3 -I scripts/baixar_camara.py --rps 2 --workers 4
"""
import argparse
import datetime as dt
import gzip
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import Rede, decodificar, yaml_str
from html2md import convert

RAIZ = Path(__file__).resolve().parent.parent / "federal"
CACHE = RAIZ / "_fonte" / "camara"
INDICE = RAIZ / "_indice" / "camara"
BUSCA = "https://www.camara.leg.br/legislacao/busca"
MESES = {m: n for n, m in enumerate(("janeiro", "fevereiro", "marco", "abril", "maio", "junho",
                                    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"), 1)}
TIPOS = {
    "camara": ("Resolução da Câmara dos Deputados", "resolucoes-camara", "rcd", "resolucaodacamaradosdeputados"),
    "senado": ("Resolução do Senado Federal", "resolucoes-senado", "rsf", "resolucao"),
    "congresso": ("Resolução do Congresso Nacional", "resolucoes-congresso", "rcn", "resolucao"),
}


def texto(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def gravar_json(path, valor):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(valor, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def obter(rede, url):
    if urllib.parse.urlparse(url).hostname not in {"www.camara.leg.br", "www2.camara.leg.br"}:
        raise ValueError(f"fonte não autorizada: {url}")
    path = CACHE / (hashlib.sha256(url.encode()).hexdigest() + ".html.gz")
    if path.exists():
        return gzip.decompress(path.read_bytes()).decode("utf-8")
    st, bruto, ct = rede.get(url, timeout=60)
    if st != 200 or not bruto:
        raise RuntimeError(f"HTTP {st}, {len(bruto)} bytes: {url}")
    s = decodificar(bruto, ct)
    if any(x in s.lower() for x in ("verify you are human", "verifique que você é humano", "captcha-container")):
        raise RuntimeError(f"bloqueio da fonte: {url}")
    CACHE.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(gzip.compress(s.encode("utf-8")))
    tmp.replace(path)
    return s


def pagina(rede, numero, tipo="camara"):
    url = BUSCA + "?" + urllib.parse.urlencode({"tipo": TIPOS[tipo][0],
                                                "ordenacao": "data:DESC", "pagina": numero})
    s = obter(rede, url)
    total = re.search(r"Exibindo resultados de\s+[\d.]+\s+a\s+[\d.]+\s+de\s+([\d.]+)", s)
    if not total:
        raise ValueError(f"busca sem total reconhecível: {url}")
    docs = []
    for item in re.findall(r'<li class="busca-resultados__item[^\"]*">(.*?)</li>', s, re.S):
        link = re.search(r'<a[^>]+href="([^"]+/legin/[^"]+)"[^>]*>(.*?)</a>', item, re.S)
        ementa = re.search(r'busca-resultados__descricao[^>]*>(.*?)</p>', item, re.S)
        situacao = re.search(r'busca-resultados__situacao[^>]*>(.*?)</p>', item, re.S)
        if not link:
            raise ValueError("resultado sem link Legin")
        docs.append({"url": html.unescape(link[1]), "titulo": texto(link[2]),
                     "ementa": re.sub(r"^Ementa:\s*", "", texto(ementa[1])) if ementa else "",
                     "situacao": re.sub(r"^Situação:\s*", "", texto(situacao[1])) if situacao else ""})
    if not docs:
        raise ValueError(f"busca vazia: {url}")
    return int(total[1].replace(".", "")), docs


def corpo_norma(s):
    inicio = re.search(r'<div\b[^>]*class=["\']textoNorma["\'][^>]*>', s)
    if not inicio:
        # O Legin também publica compilações como HTML autônomo exportado do Word/LibreOffice.
        if re.search(r'<meta\b[^>]*name=["\']generator["\'][^>]*content=["\'][^"\']*(?:LibreOffice|Microsoft Word)', s, re.I):
            body = re.search(r'<body\b[^>]*>(.*?)</body>', s, re.I | re.S)
            if body and not re.search(r'id=["\'](?:portal-header|main-nav)["\']', body[1]):
                return body[1]
        raise ValueError("página sem textoNorma")
    nivel = 1
    for tag in re.finditer(r"</?div\b[^>]*>", s[inicio.end():], re.I):
        nivel += -1 if tag[0].startswith("</") else 1
        if nivel == 0:
            return s[inicio.end():inicio.end() + tag.start()]
    raise ValueError("textoNorma incompleto")


def processar(rede, d, tipo="camara"):
    nome_tipo, pasta, prefixo, prefixo_url = TIPOS[tipo]
    m = re.search(re.escape(prefixo_url) + r'-([\w.-]+?)-(\d+)-([a-z]+)-(\d{4})-(\d+)-norma', d["url"])
    if not m:
        raise ValueError(f"data/número ausentes da URL: {d['url']}")
    numero, dia, mes, ano, ident = m.groups()
    data = dt.date(int(ano), MESES[mes], int(dia)).isoformat()
    slug = f"{prefixo}-{numero}-{data}" + (f"-{ident}" if tipo == "camara" else "")
    path = RAIZ / pasta / ano / (slug + ".md")
    if path.exists():
        return "pulado"
    s = obter(rede, d["url"])
    links = [html.unescape(u) for u in re.findall(r'href=["\']([^"\']+)["\']', s)]
    candidatos = [u for u in links if "-normaatualizada-" in u and u.endswith(".html")]
    compilada = bool(candidatos)
    if not candidatos:
        candidatos = [u for u in links if "-publicacaooriginal-" in u and u.endswith(".html")]
    if not candidatos:
        raise ValueError(f"norma sem texto HTML: {d['url']}")
    url_texto = urllib.parse.urljoin(d["url"], candidatos[0])
    corpo = convert(corpo_norma(obter(rede, url_texto)))
    if len(corpo.strip()) < 80:
        raise ValueError(f"texto insuficiente: {url_texto}")
    valores = {"titulo": d["titulo"], "tipo": nome_tipo, "numero": numero,
               "data": data, "ementa": d["ementa"], "situacao": d["situacao"],
               "revogada": d["situacao"].lower() == "revogada",
               "versao_texto": "compilada" if compilada else "original", "fonte": url_texto,
               "url_metadados": d["url"], "baixado_em": dt.date.today().isoformat()}
    linhas = ["---"]
    for k, v in valores.items():
        linhas.append(f"{k}: {str(v).lower() if isinstance(v, bool) else v if k in ('data', 'baixado_em') else yaml_str(v)}")
    linhas += ["---", "", "# " + d["titulo"], "", corpo]
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text("\n".join(linhas), encoding="utf-8")
    tmp.replace(path)
    return "ok"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rps", type=float, default=2)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--paginas", type=int, default=0, help="limita páginas para amostra")
    ap.add_argument("--tipo", choices=TIPOS, default="camara")
    a = ap.parse_args()
    if not 0 < a.rps <= 4 or a.workers < 1:
        ap.error("rps deve estar entre 0 e 4; workers deve ser positivo")
    rede = Rede(a.rps)
    cont = {"ok": 0, "pulado": 0, "erro": 0}
    docs, vistos, n, paginas = [], set(), 1, 1
    indice = INDICE if a.tipo == "camara" else INDICE.with_name("camara-" + a.tipo)
    indice.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(a.workers) as ex, (RAIZ / "_falhas_camara.jsonl").open("a", encoding="utf-8") as falhas:
        while n <= paginas:
            total, lote = pagina(rede, n, a.tipo)
            paginas = math.ceil(total / 20)
            if a.paginas:
                paginas = min(paginas, a.paginas)
            for d in lote:
                if d["url"] not in vistos:
                    vistos.add(d["url"])
                    docs.append(d)
            gravar_json(indice / f"pagina-{n:04}.json", {"total_fonte": total, "documentos": lote})
            gravar_json(indice / "indice.json", {"total_fonte": total, "paginas_coletadas": n,
                                                 "completo": n == math.ceil(total / 20), "documentos": docs})
            futs = {ex.submit(processar, rede, d, a.tipo): d for d in lote}
            for fut in as_completed(futs):
                try:
                    cont[fut.result()] += 1
                except Exception as e:
                    cont["erro"] += 1
                    falhas.write(json.dumps({**futs[fut], "fonte": a.tipo, "erro": str(e)}, ensure_ascii=False) + "\n")
                    falhas.flush()
                    if "HTTP 403" in str(e) or "bloqueio da fonte" in str(e):
                        raise
            print(f"{a.tipo} página {n}/{paginas}, índice {len(docs)}/{total}: {cont}", flush=True)
            n += 1
    print("FIM", cont, flush=True)


if __name__ == "__main__":
    main()
