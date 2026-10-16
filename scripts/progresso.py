"""Mede o acervo contra o plano e gera `progresso.svg` e `PROGRESSO.md`.

Conta os arquivos `.md` de cada item de `scripts/plano.py`, agrega por setor e por fase e desenha
uma barra para cada um. O SVG é escrito à mão, sem dependência: entra direto no README e funciona
no tema claro e no escuro porque o fundo é explícito.

    python3 -I scripts/progresso.py            # grava progresso.svg e PROGRESSO.md
    python3 -I scripts/progresso.py --conferir  # só imprime; não grava nada

Também audita o caminho inverso: pastas com `.md` no repositório que nenhum item do plano cobre.
Uma pasta órfã é sempre um dos dois: nome fora do padrão, ou tipo de norma que esquecemos de
planejar. As duas coisas precisam de correção humana, por isso aparecem no fim do relatório.
"""
import argparse
import collections
import datetime as dt
import fnmatch
import glob
import os
import sys
import subprocess
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plano import FASES, PLANO, por_setor  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def contar_md(caminho):
    """Arquivos .md sob um caminho, ignorando as pastas de trabalho (`_fonte`, `_indice`)."""
    if caminho.endswith(".md"):
        return 1 if os.path.isfile(caminho) else 0
    if not os.path.isdir(caminho):
        return 0
    n = 0
    for dirpath, dirs, arquivos in os.walk(caminho):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        n += sum(1 for a in arquivos if a.endswith(".md"))
    return n


def expandir(caminho_do_item):
    """Resolve os caminhos de um item: vários separados por vírgula, cada um com `*` opcional."""
    for parte in caminho_do_item.split(","):
        parte = parte.strip()
        alvos = glob.glob(os.path.join(RAIZ, parte))
        # um caminho sem `*` que não existe ainda tem de ser reportado (conta zero), e não sumir
        yield from (alvos or ([os.path.join(RAIZ, parte)] if "*" not in parte else []))


def medir():
    """[(item, atual)] na ordem do plano, mais o conjunto de pastas já cobertas."""
    medidas, cobertas = [], set()
    for item in PLANO:
        n = 0
        for alvo in expandir(item.caminho):
            n += contar_md(alvo)
            cobertas.add(os.path.relpath(alvo, RAIZ))
        medidas.append((item, n))
    return medidas, cobertas


def medir_git():
    """Conta o index que será publicado, sem incluir downloads ainda não adicionados."""
    saida = subprocess.check_output(["rtk", "proxy", "git", "ls-files", "--cached", "-z"], cwd=RAIZ)
    arquivos = {p for p in saida.decode().split("\0") if p.endswith(".md")
                and not any(c.startswith(("_", ".")) for c in p.split("/"))}
    contagem = collections.Counter()
    for path in arquivos:
        partes = path.split("/")
        contagem[path] += 1
        for n in range(1, len(partes)):
            contagem["/".join(partes[:n])] += 1
    por_profundidade = collections.defaultdict(list)
    for path in contagem:
        por_profundidade[path.count("/")].append(path)
    medidas, cobertas = [], set()
    for item in PLANO:
        alvos = set()
        for padrao in item.caminho.split(","):
            padrao = padrao.strip()
            if "*" in padrao:
                alvos.update(p for p in por_profundidade[padrao.count("/")]
                             if fnmatch.fnmatchcase(p, padrao))
            elif padrao in contagem:
                alvos.add(padrao)
        medidas.append((item, sum(contagem[p] for p in alvos)))
        cobertas.update(alvos)
    achadas = collections.Counter()
    for path in arquivos:
        partes = path.split("/")
        if len(partes) == 1:
            continue
        if not any("/".join(partes[:n]) in cobertas for n in range(1, len(partes))):
            achadas["/".join(partes[:-1][:3])] += 1
    return medidas, achadas


def orfas(cobertas):
    """Pastas com .md que o plano não menciona — nome fora do padrão ou tipo não planejado."""
    achadas = collections.Counter()
    for dirpath, dirs, arquivos in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if not d.startswith(("_", "."))]
        if not any(a.endswith(".md") for a in arquivos):
            continue
        rel = os.path.relpath(dirpath, RAIZ)
        if rel == ".":
            continue
        # uma pasta está coberta se ela, ou qualquer ancestral dela, é alvo de um item
        partes = rel.split(os.sep)
        if any(os.sep.join(partes[:i]) in cobertas for i in range(1, len(partes) + 1)):
            continue
        achadas[os.sep.join(partes[:3])] += sum(1 for a in arquivos if a.endswith(".md"))
    return achadas


# ------------------------------------------------------------------------------------------ SVG

FUNDO, CARTAO, TRILHA = "#0d1117", "#161b22", "#21262d"
TEXTO, FRACO, BORDA = "#e6edf3", "#8b949e", "#30363d"
CHEIO, PARCIAL, VAZIO = "#3fb950", "#58a6ff", "#484f58"

LARG = 1180
X_ROTULO, X_BARRA, LARG_BARRA = 24, 430, 470
X_NUM, X_PCT = X_BARRA + LARG_BARRA + 16, LARG - 24


def mil(n):
    return f"{n:,}".replace(",", ".")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cor(atual, meta):
    if atual == 0:
        return VAZIO
    return CHEIO if atual >= meta else PARCIAL


def barra(y, atual, meta, altura=9):
    frac = min(atual / meta, 1.0) if meta else 0.0
    larg = max(round(LARG_BARRA * frac), 2 if atual else 0)
    r = altura / 2
    partes = [f'<rect x="{X_BARRA}" y="{y}" width="{LARG_BARRA}" height="{altura}" rx="{r}" fill="{TRILHA}"/>']
    if larg:
        partes.append(f'<rect x="{X_BARRA}" y="{y}" width="{larg}" height="{altura}" rx="{r}" '
                      f'fill="{cor(atual, meta)}"/>')
    return "".join(partes)


def linha(y, rotulo, atual, meta, destaque=False):
    peso, tam, cl = ("600", 13, TEXTO) if destaque else ("400", 12, FRACO)
    pct = f"{min(100 * atual / meta, 100):.0f}%" if meta else "—"
    return (
        f'<text x="{X_ROTULO}" y="{y + 9}" font-size="{tam}" font-weight="{peso}" fill="{cl}">'
        f'{esc(rotulo)}</text>'
        + barra(y, atual, meta)
        + f'<text x="{X_NUM}" y="{y + 9}" font-size="11" fill="{FRACO}" font-family="ui-monospace,monospace">'
          f'{mil(atual)} / {mil(meta)}</text>'
        + f'<text x="{X_PCT}" y="{y + 9}" font-size="11.5" text-anchor="end" font-weight="600" '
          f'fill="{cor(atual, meta)}" font-family="ui-monospace,monospace">{pct}</text>'
    )


def desenhar(medidas):
    setores = por_setor()
    atual_item = {id(i): n for i, n in medidas}
    total_a = sum(n for _, n in medidas)
    total_m = sum(i.meta for i in PLANO)

    corpo, y = [], 150
    for fase in sorted(FASES):
        itens = [i for i in PLANO if i.fase == fase]
        fa, fm = sum(atual_item[id(i)] for i in itens), sum(i.meta for i in itens)
        titulo, nota = FASES[fase]
        corpo.append(f'<rect x="0" y="{y - 22}" width="{LARG}" height="1" fill="{BORDA}"/>')
        corpo.append(f'<text x="{X_ROTULO}" y="{y}" font-size="12.5" font-weight="700" fill="{TEXTO}" '
                     f'letter-spacing="0.3">{esc(titulo.upper())}</text>')
        corpo.append(f'<text x="{X_BARRA}" y="{y}" font-size="11" fill="{FRACO}">{esc(nota)}</text>')
        corpo.append(f'<text x="{X_PCT}" y="{y}" font-size="12.5" text-anchor="end" font-weight="700" '
                     f'fill="{cor(fa, fm)}" font-family="ui-monospace,monospace">'
                     f'{min(100 * fa / fm, 100):.1f}%</text>')
        y += 20
        for setor, itens_do_setor in setores.items():
            do_fase = [i for i in itens_do_setor if i.fase == fase]
            if not do_fase:
                continue
            a, m = sum(atual_item[id(i)] for i in do_fase), sum(i.meta for i in do_fase)
            corpo.append(linha(y, setor, a, m, destaque=True))
            y += 22
        y += 24

    altura = y + 34
    cab = [
        f'<rect width="{LARG}" height="{altura}" fill="{FUNDO}"/>',
        f'<text x="{X_ROTULO}" y="44" font-size="21" font-weight="700" fill="{TEXTO}">'
        'Acervo da legislação brasileira</text>',
        f'<text x="{X_ROTULO}" y="66" font-size="12.5" fill="{FRACO}">'
        f'{mil(total_a)} normas em Markdown de um universo estimado em {mil(total_m)}</text>',
        f'<rect x="{X_ROTULO}" y="88" width="{LARG - 48}" height="16" rx="8" fill="{TRILHA}"/>',
        f'<rect x="{X_ROTULO}" y="88" width="{max(round((LARG - 48) * total_a / total_m), 3)}" '
        f'height="16" rx="8" fill="{PARCIAL}"/>',
        f'<text x="{X_PCT}" y="78" font-size="13" text-anchor="end" font-weight="700" fill="{PARCIAL}" '
        f'font-family="ui-monospace,monospace">{100 * total_a / total_m:.1f}%</text>',
    ]
    pe = (f'<text x="{X_ROTULO}" y="{altura - 14}" font-size="10.5" fill="{FRACO}">'
          f'scripts/progresso.py · {dt.date.today():%d/%m/%Y} · as metas são estimativas do tamanho '
          'de cada série; as séries encerradas marcam 100%</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{LARG}" height="{altura}" '
            f'viewBox="0 0 {LARG} {altura}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">'
            + "".join(cab) + "".join(corpo) + pe + "</svg>\n")


# ----------------------------------------------------------------------------------- PROGRESSO.md

def markdown(medidas, achadas):
    total_a = sum(n for _, n in medidas)
    total_m = sum(i.meta for i in PLANO)
    L = ["# Progresso", "",
         f"Gerado por `scripts/progresso.py` em {dt.datetime.now(ZoneInfo('America/Recife')):%d/%m/%Y %H:%M:%S}"
         " (America/Recife). O escopo está em",
         "`scripts/plano.py`; os números de **meta** são estimativas do tamanho de cada série, não",
         "contagens oficiais. O percentual mede volume diante das metas; não comprova integralidade",
         "das fontes nem qualidade de cada conversão. Lacunas continuam abertas até verificação.", "",
         f"**{mil(total_a)} de ~{mil(total_m)} normas — {100 * total_a / total_m:.1f}%**", "",
         "![progresso](progresso.svg)", ""]
    atual_item = {id(i): n for i, n in medidas}
    for fase in sorted(FASES):
        itens = [i for i in PLANO if i.fase == fase]
        fa, fm = sum(atual_item[id(i)] for i in itens), sum(i.meta for i in itens)
        titulo, nota = FASES[fase]
        L += [f"## {titulo}", "", f"{nota[0].upper() + nota[1:]}. "
              f"**{mil(fa)} de ~{mil(fm)} — {100 * fa / fm:.1f}%**", ""]
        for setor, itens_do_setor in por_setor().items():
            do_fase = [i for i in itens_do_setor if i.fase == fase]
            if not do_fase:
                continue
            a, m = sum(atual_item[id(i)] for i in do_fase), sum(i.meta for i in do_fase)
            L += [f"### {setor} — {mil(a)} / ~{mil(m)} ({100 * a / m:.1f}%)", "",
                  "| | Tipo de norma | Tem | Meta | Pasta | Fonte |",
                  "| :-: | --- | ---: | ---: | --- | --- |"]
            for i in do_fase:
                n = atual_item[id(i)]
                marca = "✅" if n >= i.meta else ("🟦" if n else "⬜️")
                pasta = ", ".join(f"`{p.strip()}`" for p in i.caminho.split(","))
                L.append(f"| {marca} | {i.nome} | {mil(n)} | {mil(i.meta)} | {pasta} | {i.fonte} |")
            L.append("")
    L += ["---", "", "## Pastas fora do plano", ""]
    if achadas:
        L += ["Pastas com `.md` que nenhum item de `scripts/plano.py` cobre. Cada uma é nome fora do",
              "padrão ou tipo de norma não planejado — as duas coisas pedem correção.", "",
              "| Pasta | Arquivos |", "| --- | ---: |"]
        L += [f"| `{p}` | {mil(n)} |" for p, n in achadas.most_common()]
    else:
        L.append("Nenhuma: todo arquivo do repositório está sob um item do plano.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--conferir", action="store_true", help="só imprime o resumo, não grava arquivos")
    ap.add_argument("--git-index", action="store_true", help="mede somente arquivos adicionados ao próximo commit")
    args = ap.parse_args()

    if args.git_index:
        medidas, achadas = medir_git()
    else:
        medidas, cobertas = medir()
        achadas = orfas(cobertas)
    total_a = sum(n for _, n in medidas)
    total_m = sum(i.meta for i in PLANO)

    for setor, itens in por_setor().items():
        a, m = sum(dict((id(i), n) for i, n in medidas)[id(i)] for i in itens), sum(i.meta for i in itens)
        print(f"{100 * a / m:5.1f}%  {mil(a):>9} / {mil(m):<10} {setor}")
    print(f"\n{100 * total_a / total_m:5.1f}%  {mil(total_a):>9} / {mil(total_m):<10} TOTAL")
    for pasta, n in achadas.most_common():
        print(f"fora do plano: {pasta} ({mil(n)} arquivos)")

    if args.conferir:
        return
    with open(os.path.join(RAIZ, "progresso.svg"), "w", encoding="utf-8") as f:
        f.write(desenhar(medidas))
    with open(os.path.join(RAIZ, "PROGRESSO.md"), "w", encoding="utf-8") as f:
        f.write(markdown(medidas, achadas))
    print("\ngravados: progresso.svg, PROGRESSO.md")


if __name__ == "__main__":
    main()
