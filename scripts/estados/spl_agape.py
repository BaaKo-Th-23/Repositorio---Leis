"""Sistema de legislação usado pela ALES (ES) e pela ALESE (SE) — mesmas páginas ASP.NET.

Índice: consulta-legislacao.aspx?tipo=T&ano=A com 100 itens por página (postback) e exportação CSV de cada página;
        cada ano é guardado em _indice/anos/ para retomar sem refazer.
Texto: link /Arquivo/Documents/legislacao/html/... da página norma.aspx?id=N; se não houver, tenta o padrão
       {PREFIXO}{numero}{ano}.html.

Uso: python3 -I scripts/estados/spl_agape.py ES|SE [N]
"""
import csv
import html as htmllib
import http.cookiejar
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, UA, Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402

CONFIG = {
    "ES": {
        "base": "https://www3.al.es.gov.br",
        "tipos": {
            "1": ("constituicao", "Constituição Estadual", ["CON", "CE"]),
            "2": ("emendas-constitucionais", "Emenda à Constituição Estadual", ["EMC", "EC"]),
            "4": ("leis-complementares", "Lei Complementar", ["LEC", "LC"]),
            "3": ("leis-ordinarias", "Lei Ordinária", ["LEI"]),
            "8": ("leis-delegadas", "Lei Delegada", ["LED", "LD"]),
        },
    },
    "SE": {
        "base": "https://aleselegis.al.se.leg.br",
        "tipos": {
            "1": ("constituicao", "Constituição Estadual", ["CE"]),
            "2": ("emendas-constitucionais", "Emenda Constitucional", ["EC", "E"]),
            "3": ("leis-complementares", "Lei Complementar", ["C", "LC"]),
            "4": ("leis-ordinarias", "Lei Ordinária", ["L", "LEI"]),
            "7": ("decretos-lei", "Decreto-Lei", ["DL"]),
            "8": ("leis-delegadas", "Lei Delegada", ["LD"]),
        },
    },
}
UF = sys.argv[1].upper() if len(sys.argv) > 1 and sys.argv[1].upper() in CONFIG else "ES"
CFG = CONFIG[UF]
B = CFG["base"] + "/legislacao"
rede = Rede(rps=3)
DDL = "ctl00$ContentPlaceHolder1$ddl_ItensExibidos"


def ocultos(html):
    return {n: htmllib.unescape(v) for n, v in re.findall(r'<input type="hidden" name="([^"]+)" id="[^"]*" value="([^"]*)"', html)}


def abrir(op, url, campos=None):
    rede.limite.esperar()
    dados = urllib.parse.urlencode(campos).encode() if campos is not None else None
    h = {"User-Agent": UA, **({"Content-Type": "application/x-www-form-urlencoded"} if dados else {})}
    return op.open(urllib.request.Request(url, data=dados, headers=h), timeout=300).read()


def listar(tipo, ano):
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    url = f"{B}/consulta-legislacao.aspx?tipo={tipo}&ano={ano}"
    html = abrir(op, url).decode("utf-8", "replace")
    html = abrir(op, url, {**ocultos(html), "__EVENTTARGET": DDL, "__EVENTARGUMENT": "", DDL: "100"}).decode("utf-8", "replace")
    linhas = []
    for _ in range(200):
        lote = list(csv.DictReader(io.StringIO(
            abrir(op, url, {**ocultos(html), DDL: "100", "ctl00$ContentPlaceHolder1$btn_export_csv": "CSV"}).decode("cp1252", "replace"))))
        linhas += lote
        if len(lote) < 100 or "lbNext" not in html:
            return linhas
        html = abrir(op, url, {**ocultos(html), DDL: "100", "__EVENTTARGET": "ctl00$ContentPlaceHolder1$lbNext",
                                "__EVENTARGUMENT": ""}).decode("utf-8", "replace")
    return linhas


def indice():
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    os.makedirs(os.path.join(pasta, "anos"), exist_ok=True)
    st, dados, ctype = rede.get(f"{B}/consulta-tipo.aspx")
    pagina = decodificar(dados, ctype)
    itens = {}
    for tipo in CFG["tipos"]:
        anos = sorted(set(re.findall(rf"consulta-legislacao\.aspx\?tipo={tipo}&(?:amp;)?ano=(\d{{4}})", pagina)), reverse=True)
        for ano in anos:
            cache = os.path.join(pasta, "anos", f"{tipo}-{ano}.json")
            if os.path.exists(cache):
                linhas = json.load(open(cache, encoding="utf-8"))
            else:
                linhas = None
                for n in range(4):
                    try:
                        linhas = listar(tipo, ano)
                        break
                    except Exception as e:
                        erro = e
                        time.sleep(10 * (n + 1))
                if linhas is None:
                    # o servidor às vezes falha sempre no mesmo ano: registra e segue (sem cache, tenta na próxima rodada)
                    print(f"[{UF}] AVISO: listagem tipo {tipo} ano {ano} indisponível ({erro})", flush=True)
                    with open(os.path.join(RAIZ_ESTADUAIS, UF, "_falhas.jsonl"), "a", encoding="utf-8") as f:
                        f.write(json.dumps({"status": "indice", "tipo": tipo, "ano": ano, "erro": str(erro)[:200]}) + "\n")
                    continue
                json.dump(linhas, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
            for ln in linhas:
                cod = (ln.get("cod") or "").strip()
                if cod:
                    itens[cod] = {"tipo": tipo, **{k.strip(): (v or "").strip() for k, v in ln.items() if k and isinstance(v, str)}}
        print(f"[{UF}] índice tipo {tipo}: {sum(1 for i in itens.values() if i['tipo'] == tipo)} ({len(anos)} anos)", flush=True)
    return list(itens.values())


def localizar_texto(it, numero, ano, prefixos):
    """Link do texto na página da norma; senão, o padrão de nome de arquivo."""
    st, dados, ctype = rede.get(f"{B}/norma.aspx?id={it['cod']}", timeout=300)
    if st == 200:
        m = re.search(r"""href=\s*['"](/Arquivo/Documents/legislacao/html/[^'"?]+)""", decodificar(dados, ctype))
        if m:
            url = CFG["base"] + urllib.parse.quote(m.group(1))
            st, bruto, ctype = rede.get(url, timeout=300)
            if st == 200 and bruto:
                return url, bruto, ctype
    for pre in prefixos:
        url = f"{CFG['base']}/Arquivo/Documents/legislacao/html/{pre}{numero}{ano}.html"
        st, bruto, ctype = rede.get(url, timeout=300)
        if st == 200 and bruto:
            return url, bruto, ctype
    return None, None, None


def processar(it):
    pasta, nome, prefixos = CFG["tipos"][it["tipo"]]
    numero = re.sub(r"\D", "", it.get("Numero") or "")
    ano = it.get("Ano") or "sem-ano"
    slug = f"{prefixos[0].lower()}-{numero or 'sn'}-{ano}-id{it['cod']}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    url, bruto, ctype = localizar_texto(it, numero, ano, prefixos)
    if not bruto:
        return "sem_texto", {"cod": it["cod"], "norma": f"{nome} {numero}/{ano}", "motivo": "texto não encontrado"}
    corpo = html_para_md(decodificar(bruto, ctype))
    if len(re.sub(r"\W", "", corpo)) < 40:
        return "sem_texto", {"cod": it["cod"], "url": url, "motivo": "texto vazio"}
    situacao = next((v for k, v in it.items() if k.startswith("Situa")), "")
    d = re.match(r"(\d{2})/(\d{2})/(\d{4})", it.get("Data") or "")
    titulo = f"{nome} nº {it.get('Numero')}/{ano}" if numero else nome
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", it.get("Numero") or ""),
        ("data", f"{d.group(3)}-{d.group(2)}-{d.group(1)}" if d else ""),
        ("ementa", " ".join((it.get("Ementa") or "").split())),
        ("situacao", situacao),
        ("revogada", situacao.lower().startswith("revogad")),
        ("versao_texto", "HTML do sistema de legislação da Assembleia (compilado quando disponível)"),
        ("fonte", f"{B}/norma.aspx?id={it['cod']}"),
        ("arquivo", url),
    ]
    gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice()
    itens.sort(key=lambda i: (i.get("Ano") or "", int(re.sub(r"\D", "", i.get("Numero") or "0") or 0)), reverse=True)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    if len(sys.argv) > 2:
        itens = itens[: int(sys.argv[2])]
    executar(UF, itens, processar, workers=3)
