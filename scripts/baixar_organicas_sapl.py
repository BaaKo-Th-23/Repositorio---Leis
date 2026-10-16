"""Leis orgânicas e emendas integrais em SAPLs municipais oficiais; cache retomável."""
import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Rede, documento_para_md, normalizar_chave, yaml_str

RAIZ = Path(__file__).resolve().parent.parent / "municipais"
FONTES = [("Lapa", "PR", "sapl.lapa.pr.leg.br"),
          ("Santo Antônio do Paraíso", "PR", "sapl.santoantoniodoparaiso.pr.leg.br"),
          ("Bariri", "SP", "sapl.bariri.sp.leg.br"),
          ("Registro", "SP", "sapl.registro.sp.leg.br"),
          ("Jardinópolis", "SP", "sapl.jardinopolis.sp.leg.br"),
          ("Igarapava", "SP", "sapl.igarapava.sp.leg.br")]


def escrever(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(b)
    tmp.replace(p)


def executar(fontes, rps):
    ibge = json.loads((RAIZ / "_indice/ibge-municipios.json").read_text())
    registro_path = RAIZ / "_indice/organicas-sapl/municipios.json"
    registro = json.loads(registro_path.read_text()) if registro_path.exists() else {
        str(x["id"]): {"municipio": x["nome"], "uf": x["regiao-imediata"]["regiao-intermediaria"]["UF"]["sigla"],
                       "estado_descoberta": "fonte ainda não localizada", "fontes": {}} for x in ibge}
    erros = 0
    for nome, uf, host in fontes:
        rede = Rede(rps=rps)
        cache = RAIZ / "_indice/organicas-sapl" / host
        def obter(url, destino):
            if destino.exists():
                return destino.read_bytes()
            st, b, ct = rede.get(url, tentativas=1)
            if st != 200:
                raise RuntimeError(f"HTTP {st}: {url}")
            escrever(destino, b)
            return b
        def api(caminho):
            url = f"https://{host}/api/{caminho}"
            destino = cache / (hashlib.sha256(url.encode()).hexdigest() + ".json")
            d = json.loads(obter(url, destino))
            return d
        try:
            matches = [x for x in ibge if normalizar_chave(x["nome"]) == normalizar_chave(nome) and
                       x["regiao-imediata"]["regiao-intermediaria"]["UF"]["sigla"] == uf]
            if len(matches) != 1:
                raise RuntimeError("identidade municipal IBGE ambígua")
            codigo = matches[0]["id"]
            nome = matches[0]["nome"]
            casa = api("base/casalegislativa/")
            if not any(normalizar_chave(c["municipio"]) == normalizar_chave(nome) and c["uf"] == uf
                       for c in casa["results"]):
                raise RuntimeError("identidade da casa SAPL diverge do município IBGE")
            registro[str(codigo)]["estado_descoberta"] = "fonte oficial identificada"
            registro[str(codigo)]["fontes"][host] = {"identidade": f"https://{host}/api/base/casalegislativa/",
                                                  "estado": "índice em processamento"}
            escrever(registro_path, json.dumps(registro, ensure_ascii=False).encode())
            tipos = []
            page = 1
            while True:
                d = api(f"norma/tiponormajuridica/?page_size=100&page={page}")
                tipos += [t for t in d["results"] if "organica" in normalizar_chave(t["descricao"]) and
                          not re.search("projeto|proposta", t["descricao"], re.I)]
                if not d["pagination"].get("next_page"):
                    break
                page += 1
            ok = pulado = 0
            indice = []
            eq_path = cache / "equivalencias.json"
            equivalencias = json.loads(eq_path.read_text()) if eq_path.exists() else {}
            pasta_municipio = RAIZ / uf / normalizar_chave(nome).replace(" ", "-")
            for tipo in tipos:
                page = 1
                while True:
                    d = api(f"norma/normajuridica/?tipo={tipo['id']}&page_size=100&page={page}")
                    indice.extend(d["results"])
                    for n in d["results"]:
                        try:
                            emenda = "emenda" in tipo["descricao"].lower()
                            categoria = "emendas-lei-organica" if emenda else "lei-organica"
                            identity = f"https://{host}/norma/{n['id']}"
                            existentes = list(pasta_municipio.glob(f"{categoria}/**/*.md"))
                            if any(f"fonte: {yaml_str(identity)}\n" in x.read_text() for x in existentes):
                                pulado += 1
                                continue
                            url = n.get("texto_integral")
                            if not url:
                                raise RuntimeError("norma sem texto integral")
                            if urlsplit(url).hostname == host:
                                url = "https://" + url.split("://", 1)[1]
                            fonte = RAIZ / "_fonte/organicas-sapl" / host / f"{n['id']}.bin"
                            b = obter(url, fonte)
                            corpo, motivo = documento_para_md(b, url)
                            if motivo:
                                raise RuntimeError(motivo)
                            if not (re.search(r"art(?:igo)?\.?\s*1(?:[º°o]|\b)", corpo, re.I) or
                                    (emenda and len(corpo) > 500 and re.search("promulgo", corpo, re.I) and
                                     re.search(r"vigorar|vigor", corpo, re.I))):
                                raise RuntimeError("texto sem artigo inicial reconhecível; revisar integralidade")
                            # Guarda versões iguais uma vez por município, preservando o índice original.
                            digest = hashlib.sha256(corpo.encode()).hexdigest()
                            iguais = [x for x in existentes if f'sha256_texto: "{digest}"' in x.read_text()]
                            if iguais:
                                equivalencias[str(n["id"])] = {"arquivo": str(iguais[0].relative_to(RAIZ)),
                                    "fonte": identity, "fonte_texto": url, "sha256_texto": digest}
                                escrever(eq_path, json.dumps(equivalencias, ensure_ascii=False).encode())
                                pulado += 1
                                continue
                            data = n.get("data") or ""
                            data_cadastro = data
                            ano_documento = str(n["ano"])
                            observacao_data = ""
                            if host == "sapl.lapa.pr.leg.br" and n["id"] == 3799:
                                if "Edifício da Câmara Municipal da Lapa, em 4 de abril de 1990" not in corpo:
                                    raise RuntimeError("assinatura da lei orgânica Lapa não confirmada")
                                data = "1990-04-04"
                                observacao_data = "Data da assinatura no texto integral; cadastro SAPL usa a data da Emenda 01/2020."
                            if host == "sapl.igarapava.sp.leg.br" and n["id"] == 1373:
                                if "Igarapava/SP, ano de 1990." not in corpo:
                                    raise RuntimeError("ano da assinatura de Igarapava não confirmado")
                                data = ""
                                ano_documento = "1990"
                                observacao_data = "Texto integral assinado apenas com ano de 1990; cadastro apresenta 2011-11-04, sem confirmação no documento."
                            ano = data[:4] if data else ano_documento
                            numero = str(n["numero"])
                            titulo = n["__str__"]
                            meta = {"titulo": titulo, "tipo": "Emenda à Lei Orgânica" if emenda else "Lei Orgânica",
                                    "numero": numero, "data": data, "municipio": nome, "uf": uf,
                                    "codigo_ibge": str(codigo), "versao_texto": "texto integral anexado no SAPL municipal; " + n.get("observacao", ""),
                                    "fonte": identity, "fonte_texto": url,
                                    "sha256_fonte": hashlib.sha256(b).hexdigest(), "sha256_texto": digest,
                                    "baixado_em": dt.date.today().isoformat()}
                            if data != data_cadastro:
                                meta["data_no_cadastro"] = data_cadastro
                                meta["observacao_data"] = observacao_data
                                meta["ano_na_fonte"] = ano_documento
                                titulo = "Lei Orgânica do Município da Lapa, de 4 de abril de 1990" if host == "sapl.lapa.pr.leg.br" else "Lei Orgânica do Município de Igarapava, de 1990"
                                meta["titulo"] = titulo
                            cab = ["---"] + [f"{k}: {yaml_str(v)}" for k, v in meta.items()] + ["---", "", f"# {titulo}", "", corpo, ""]
                            arq = pasta_municipio / categoria / ano / f"{categoria}-{normalizar_chave(numero)}-{ano}-sapl-{n['id']}.md"
                            escrever(arq, "\n".join(cab).encode())
                            ok += 1
                        except Exception as e:
                            erros += 1
                            cache.mkdir(parents=True, exist_ok=True)
                            with (cache / "falhas.jsonl").open("a") as f:
                                f.write(json.dumps({"id": n["id"], "erro": str(e), "quando": dt.datetime.now().isoformat()}) + "\n")
                            print(host, n["id"], "FALHA", e, flush=True)
                    if not d["pagination"].get("next_page"):
                        break
                    page += 1
            escrever(cache / "indice.json", json.dumps({"fonte": f"https://{host}/api/norma/normajuridica/",
                     "municipio": nome, "uf": uf, "codigo_ibge": codigo, "tipos": tipos,
                     "normas": indice, "consultado_em": dt.date.today().isoformat()}, ensure_ascii=False).encode())
            presentes = {n["id"] for n in indice if any(
                "fonte: " + yaml_str("https://" + host + "/norma/" + str(n["id"])) + "\n" in x.read_text()
                for x in pasta_municipio.glob("**/*sapl*.md"))}
            registro[str(codigo)]["fontes"][host].update({"estado": "índice orgânico completo capturado",
                "registros": len(indice), "textos_md": len(presentes), "ids_equivalentes": list(equivalencias), "ids_sem_md": [n["id"] for n in indice if n["id"] not in presentes and str(n["id"]) not in equivalencias], "normas_distintas": len({(n["tipo"], n["numero"], n["ano"]) for n in indice}),
                "leis_organicas_distintas": len({(n["numero"], n["ano"]) for n in indice if not
                    any(t["id"] == n["tipo"] and "emenda" in t["descricao"].lower() for t in tipos)}),
                "consultado_em": dt.date.today().isoformat()})
            escrever(registro_path, json.dumps(registro, ensure_ascii=False).encode())
            print(host, "IBGE", codigo, "novos", ok, "já existentes", pulado, flush=True)
        except Exception as e:
            erros += 1
            cache.mkdir(parents=True, exist_ok=True)
            with (cache / "falhas.jsonl").open("a") as f:
                f.write(json.dumps({"erro": str(e), "quando": dt.datetime.now().isoformat()}) + "\n")
            print(host, "FALHA", e, flush=True)
    return bool(erros)


def catalogo_sigi(rps):
    ibge = json.loads((RAIZ / "_indice/ibge-municipios.json").read_text())
    lookup = {(normalizar_chave(x["nome"]), x["regiao-imediata"]["regiao-intermediaria"]["UF"]["sigla"]): str(x["id"]) for x in ibge}
    rede = Rede(rps=rps)
    pasta = RAIZ / "_indice/organicas-sapl/sigi"
    url = "https://sigi.interlegis.leg.br/api/servicos/"
    registros = []
    pagina = 1
    while url:
        arquivo = pasta / f"pagina-{pagina}.json"
        if arquivo.exists():
            b = arquivo.read_bytes()
        else:
            st, b, _ = rede.get(url, tentativas=1)
            if st != 200:
                raise RuntimeError(f"SIGI HTTP {st}: {url}")
            json.loads(b)
            escrever(arquivo, b)
        d = json.loads(b)
        registros += d["results"]
        url = d["next"]
        pagina += 1
    if len(registros) != d["count"]:
        raise RuntimeError("catálogo SIGI mudou durante paginação; revisão necessária")
    candidatos = []
    nao_vinculados = []
    for r in registros:
        c = r["casa_legislativa"]
        if r["tipo_servico_sigla"] != "SAPL" or c["tipo_orgao_sigla"] != "CM":
            continue
        codigo = lookup.get((normalizar_chave(c["municipio"]), c["uf"]))
        item = {"municipio": c["municipio"], "uf": c["uf"], "url": r["url"],
                "codigo_ibge": codigo, "estado": "candidato oficial SIGI; API municipal ainda não validada"}
        (candidatos if codigo else nao_vinculados).append(item)
    escrever(pasta / "catalogo.json", json.dumps({"fonte": "https://sigi.interlegis.leg.br/api/servicos/",
        "consultado_em": dt.date.today().isoformat(), "total_servicos": len(registros),
        "candidatos_sapl": candidatos, "municipios_nao_vinculados": nao_vinculados}, ensure_ascii=False).encode())
    print("SIGI:", len(registros), "serviços;", len(candidatos), "SAPLs municipais vinculados;",
          len(nao_vinculados), "pendências IBGE", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--catalogo-sigi", action="store_true", help="captura catálogo oficial de candidatos, sem baixar normas")
    ap.add_argument("--rps", type=float, default=1)
    ap.add_argument("--host", help="reexecuta uma fonte já identificada")
    ap.add_argument("--descobrir", metavar="HOST", help="valida um SAPL oficial e registra sua identidade IBGE")
    a = ap.parse_args()
    if not 0 < a.rps <= 4:
        ap.error("rps deve ser maior que zero e no máximo 4")
    if a.catalogo_sigi:
        catalogo_sigi(a.rps)
        raise SystemExit(0)
    registro_path = RAIZ / "_indice/organicas-sapl/municipios.json"
    fontes = list(FONTES)
    if registro_path.exists():
        for municipio in json.loads(registro_path.read_text()).values():
            fontes.extend((municipio["municipio"], municipio["uf"], host) for host in municipio["fontes"])
    if a.descobrir:
        if not re.fullmatch(r"[a-z0-9.-]+\.leg\.br", a.descobrir):
            ap.error("informe um host legislativo oficial .leg.br")
        url = f"https://{a.descobrir}/api/base/casalegislativa/"
        st, bruto, _ = Rede(rps=a.rps).get(url, tentativas=1)
        if st != 200:
            ap.error(f"fonte indisponível: HTTP {st}")
        casas = json.loads(bruto)["results"]
        if len(casas) != 1:
            ap.error("fonte sem identidade única")
        c = casas[0]
        fontes = [(c["municipio"], c["uf"], a.descobrir)]
        escrever(RAIZ / "_indice/organicas-sapl" / a.descobrir / (hashlib.sha256(url.encode()).hexdigest() + ".json"), bruto)
    fontes = list(dict.fromkeys(fontes))
    if a.host and not any(f[2] == a.host for f in fontes):
        ap.error("host não identificado; use --descobrir")
    raise SystemExit(executar([f for f in fontes if not a.host or f[2] == a.host], a.rps))
