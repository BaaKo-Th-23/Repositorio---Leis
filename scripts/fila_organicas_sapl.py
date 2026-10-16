"""Fila sequencial retomável de SAPLs descobertos no catálogo oficial SIGI."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import urlsplit

RAIZ = Path(__file__).resolve().parent.parent

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--aguardar-pid", type=int)
    ap.add_argument("--limite-fontes", type=int, default=0)
    a = ap.parse_args()
    if a.limite_fontes < 0:
        ap.error("limite deve ser não negativo")
    if a.aguardar_pid:
        while True:
            try:
                os.kill(a.aguardar_pid, 0)
            except ProcessLookupError:
                break
            time.sleep(5)
    pasta = RAIZ / "municipais/_indice/organicas-sapl"
    candidatos = json.loads((pasta / "sigi/catalogo.json").read_text())["candidatos_sapl"]
    arq = pasta / "fila.json"
    estado = json.loads(arq.read_text()) if arq.exists() else {}
    rodadas = 0
    for item in candidatos:
        u = urlsplit(item["url"] if "://" in item["url"] else "https://" + item["url"])
        host = u.hostname
        if item["url"] in estado:
            continue
        if a.limite_fontes and rodadas >= a.limite_fontes:
            break
        if u.path.strip("/") or not host or not host.endswith(".leg.br"):
            resultado = {"estado": "requer adaptador para URL oficial", "url": item["url"]}
        else:
            with (RAIZ / "_log_organicas_sapl.txt").open("a") as log:
                log.write(f"\nFONTE {host} IBGE {item['codigo_ibge']}\n")
                log.flush()
                r = subprocess.run([sys.executable, "-I", str(RAIZ / "scripts/baixar_organicas_sapl.py"),
                                    "--descobrir", host, "--rps", "1"], stdout=log, stderr=log)
            resultado = {"estado": "execução concluída" if r.returncode == 0 else "execução parcial; revisar falhas",
                         "exit_code": r.returncode, "url": item["url"]}
            rodadas += 1
        resultado.update({"codigo_ibge": item["codigo_ibge"], "verificado_em": dt.datetime.now().isoformat()})
        estado[item["url"]] = resultado
        tmp = arq.with_suffix(".tmp")
        tmp.write_text(json.dumps(estado, ensure_ascii=False))
        tmp.replace(arq)
        print(item["municipio"], resultado["estado"], flush=True)
    return int(any(x.get("exit_code", 0) != 0 or "adaptador" in x["estado"] for x in estado.values()))

if __name__ == "__main__":
    raise SystemExit(main())
