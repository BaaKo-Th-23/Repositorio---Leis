"""Baixa a legislação federal (normas.leg.br) e grava em Markdown.

Índice: listas do Senado em federal/_indice/*.json.
Texto: versão compilada vigente ("Current") quando existe; senão a publicação mais recente.
Retomável: pula normas cujo .md já existe. HTML bruto fica em federal/_fonte (gzip).

Uso: python3 -I scripts/baixar_federal.py [--limite N] [--tipos LEI,LCP,...] [--workers 4] [--rps 4]
"""
import argparse
import datetime as dt
import gzip
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import AVISO_SEM_TEXTO  # noqa: E402
from html2md import convert  # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "federal")
RAIZ = os.path.abspath(RAIZ)
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"
API_NORMA = "https://normas.leg.br/api/public/normas?urn={}&tipo_documento=maior-detalhe"
API_SENADO = "https://legis.senado.leg.br/dadosabertos/legislacao/{}.json"

# tipo do Senado -> (pasta, prefixo do arquivo, tipo na URN LexML, nome legível)
TIPOS = {
    "LEI-n": ("leis-ordinarias", "lei", "lei", "Lei Ordinária"),
    "LEI-sn": ("leis-ordinarias", "lei-sn", "lei", "Lei (não numerada)"),
    "LCP": ("leis-complementares", "lcp", "lei.complementar", "Lei Complementar"),
    "LDL": ("leis-delegadas", "ldl", "lei.delegada", "Lei Delegada"),
    "LCT": ("leis-constitucionais", "lct", "lei.constitucional", "Lei Constitucional"),
    "DEL": ("decretos-lei", "del", "decreto.lei", "Decreto-Lei"),
    "DEL-mpv": ("decretos-lei", "del", "decreto.lei", "Decreto-Lei"),
}


class Limitador:
    """Limita requisições por segundo entre todas as threads."""

    def __init__(self, rps):
        self.intervalo = 1.0 / rps
        self.prox = time.monotonic()
        self.lock = threading.Lock()

    def esperar(self):
        with self.lock:
            agora = time.monotonic()
            espera = self.prox - agora
            self.prox = max(agora, self.prox) + self.intervalo
        if espera > 0:
            time.sleep(espera)


LIMITE = None


def http_get(url, accept="*/*", tentativas=4):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept, "Accept-Encoding": "gzip"})
    ultimo = None
    for n in range(tentativas):
        LIMITE.esperar()
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                dados = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    dados = gzip.decompress(dados)
                return r.status, dados
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                return e.code, b""
            ultimo = e
        except Exception as e:  # rede, IncompleteRead, timeout
            ultimo = e
        time.sleep(2 * (n + 1) ** 2)
    raise RuntimeError(f"falhou após {tentativas} tentativas: {url}: {ultimo}")


def carregar_indice(tipos):
    itens = []
    for arq in sorted(os.listdir(os.path.join(RAIZ, "_indice"))):
        if not arq.endswith(".json"):
            continue
        docs = json.load(open(os.path.join(RAIZ, "_indice", arq), encoding="utf-8"))
        docs = docs["ListaDocumento"]["documentos"]["documento"]
        for d in docs if isinstance(docs, list) else [docs]:
            if d["tipo"] not in TIPOS or (tipos and d["tipo"] not in tipos):
                continue
            itens.append(d)
    return itens


def montar(d):
    pasta, prefixo, tipo_urn, nome = TIPOS[d["tipo"]]
    dia, mes, ano = d["dataassinatura"].split("/")
    data = f"{ano}-{mes}-{dia}"
    if d["tipo"] == "LEI-sn":
        seq = d.get("sequencia", "0")
        urn = f"urn:lex:br:federal:{tipo_urn}:{data};seq-sf-{seq}"
        slug = f"{prefixo}-{data}-s{seq}"
    else:
        urn = f"urn:lex:br:federal:{tipo_urn}:{data};{d['numero']}"
        slug = f"{prefixo}-{d['numero']}-{data}"
    md = os.path.join(RAIZ, pasta, ano, slug + ".md")
    fonte = os.path.join(RAIZ, "_fonte", pasta, ano, slug + ".html.gz")
    return {"urn": urn, "slug": slug, "md": md, "fonte": fonte, "data": data, "nome": nome}


def obter_metadados(urn, id_senado):
    st, corpo = http_get(API_NORMA.format(urllib.parse.quote(urn, safe=":;@!~$-.")), "application/json")
    meta = json.loads(corpo) if st == 200 and corpo.strip() else {}
    if meta.get("encoding"):
        return urn, meta
    # URN montada não bateu: pergunta ao Senado qual é a URN oficial
    st, corpo = http_get(API_SENADO.format(id_senado), "application/json")
    if st == 200 and corpo:
        ident = json.loads(corpo)["DetalheDocumento"]["documentos"]["documento"][0]["identificacao"]
        url = ident.get("urlDocumento") or ""
        if "urn=" in url and url.split("urn=", 1)[1] and url.split("urn=", 1)[1] != urn:
            urn2 = urllib.parse.unquote(url.split("urn=", 1)[1])
            st, corpo = http_get(API_NORMA.format(urllib.parse.quote(urn2, safe=":;@!~$-.")), "application/json")
            meta = json.loads(corpo) if st == 200 and corpo.strip() else {}
            return urn2, meta
    return urn, meta


def como_lista(v):
    # JSON-LD: um único valor vem como objeto, vários como lista
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def escolher_texto(meta):
    encs = [
        e
        for e in como_lista(meta.get("encoding"))
        if isinstance(e, dict) and e.get("contentUrl") and "html" in (e.get("encodingFormat") or "text/html")
    ]
    if not encs:
        return None
    atual = [e for e in encs if e.get("version") == "Current"]
    if atual:
        return atual[0]
    return sorted(encs, key=lambda e: e.get("datePublished") or "")[-1]


def yaml_str(v):
    return json.dumps(v if v is not None else "", ensure_ascii=False)


def processar(d):
    info = montar(d)
    if os.path.exists(info["md"]):
        return "pulado", info["slug"], None
    urn, meta = obter_metadados(info["urn"], d["id"])
    enc = escolher_texto(meta)
    if not enc:
        return "sem_texto", info["slug"], {"id": d["id"], "norma": d["norma"], "urn": urn}

    url = enc["contentUrl"].replace("/api/binario/", "/api/public/binario/")
    st, html = http_get(url, "text/html")
    if st != 200 or not html:
        return "sem_texto", info["slug"], {"id": d["id"], "norma": d["norma"], "urn": urn, "url": url, "http": st}

    os.makedirs(os.path.dirname(info["fonte"]), exist_ok=True)
    with gzip.open(info["fonte"], "wb") as f:
        f.write(html)

    corpo = convert(html.decode("utf-8", errors="replace"))
    versao = {"Current": "compilada (texto vigente)", "Original": "original", "Intermediate": "republicação/retificação"}
    # o portal só marca explicitamente as normas revogadas (NotInForce)
    revogada = "NotInForce" in como_lista(meta.get("legislationLegalForce"))
    cab = [
        "---",
        f"titulo: {yaml_str(d['normaNome'].strip())}",
        f"tipo: {yaml_str(info['nome'])}",
        f"numero: {yaml_str(d.get('numero', ''))}",
        f"data: {info['data']}",
        f"ementa: {yaml_str((d.get('ementa') or '').strip())}",
        f"revogada: {'true' if revogada else 'false'}",
        f"versao_texto: {yaml_str(versao.get(enc.get('version'), enc.get('version')))}",
        f"urn: {yaml_str(urn)}",
        f"fonte: {yaml_str('https://normas.leg.br/?urn=' + urn)}",
        f"baixado_em: {dt.date.today().isoformat()}",
        "---",
        "",
    ]
    os.makedirs(os.path.dirname(info["md"]), exist_ok=True)
    tmp = info["md"] + ".tmp"
    # o corpo começa pelo título em H1, como nos arquivos estaduais
    titulo = d["normaNome"].strip()
    # o portal às vezes serve um documento vazio (só um espaço). Guarda os metadados e diz por quê.
    aviso = "" if corpo.strip() else AVISO_SEM_TEXTO
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(cab) + f"# {titulo}\n\n" + aviso + corpo)
    os.replace(tmp, info["md"])
    return "ok", info["slug"], None


def main():
    global LIMITE
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--tipos", default="")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--rps", type=float, default=4)
    ap.add_argument("--amostra", default="", help="lista de normas do Senado (ex.: LEI-10406-2002-01-10,...)")
    a = ap.parse_args()
    LIMITE = Limitador(a.rps)

    itens = carregar_indice(set(filter(None, a.tipos.split(","))))
    if a.amostra:
        alvo = set(a.amostra.split(","))
        itens = [d for d in itens if d["norma"] in alvo]
    # mais recentes primeiro: são as mais consultadas
    itens.sort(key=lambda d: d["dataassinatura"][6:] + d["dataassinatura"][3:5] + d["dataassinatura"][:2], reverse=True)
    if a.limite:
        itens = itens[: a.limite]

    falhas_path = os.path.join(RAIZ, "_falhas.jsonl")
    cont = {"ok": 0, "pulado": 0, "sem_texto": 0, "erro": 0}
    inicio = time.time()
    with ThreadPoolExecutor(a.workers) as ex, open(falhas_path, "a", encoding="utf-8") as falhas:
        futs = {ex.submit(processar, d): d for d in itens}
        for n, fut in enumerate(as_completed(futs), 1):
            d = futs[fut]
            try:
                status, slug, extra = fut.result()
            except Exception as e:
                status, slug, extra = "erro", d["norma"], {"id": d["id"], "norma": d["norma"], "erro": str(e)[:300]}
            cont[status] += 1
            if extra:
                extra["status"] = status
                falhas.write(json.dumps(extra, ensure_ascii=False) + "\n")
                falhas.flush()
            if n % 50 == 0 or n == len(itens):
                taxa = n / max(1, time.time() - inicio)
                resta = (len(itens) - n) / max(taxa, 1e-9)
                print(f"{n}/{len(itens)} {cont} ~{resta / 60:.0f} min restantes", flush=True)
    print("FIM", cont, flush=True)


if __name__ == "__main__":
    main()
