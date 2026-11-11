"""Genera subtítulos (.srt) con lo que se dice en la sección 5 del guion.

Uso: python guion_a_srt.py GUION.md SALIDA.srt [--fin MM:SS]
Cada fila de tabla con minuto «MM:SS» aporta su diálogo (última columna).
El texto se trocea en frases de ≤ 2 líneas y se reparte desde el minuto de
la fila a ~2,3 palabras/s; si no cabe antes de la fila siguiente, se comprime.
"""
import re
import sys

PPS = 2.3          # palabras por segundo
MAXC = 84          # caracteres por subtítulo (2 líneas de ~42)


def seg(t):
    m, s = t.split(":")
    return int(m) * 60 + float(s)


def ts(x):
    ms = int(round(x * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def filas(md):
    sec = md.split("## 5.", 1)[1].split("\n## 6.", 1)[0]
    for ln in sec.splitlines():
        m = re.match(r"\|\s*(\d{2}:\d{2})\s*\|", ln)
        if not m:
            continue
        txt = ln.strip().strip("|").split("|")[-1].strip()
        txt = re.sub(r"\[[^\]]*\]", "", txt).replace("«", "").replace("»", "")
        txt = re.sub(r"\s+", " ", txt).strip()
        if txt:
            yield seg(m.group(1)), txt


def trozos(txt):
    out, cur = [], ""
    for w in re.split(r"(?<=[.;:!?,])\s+", txt):
        for p in ([w] if len(w) <= MAXC else _cortar(w)):
            if cur and len(cur) + 1 + len(p) > MAXC:
                out.append(cur)
                cur = p
            else:
                cur = f"{cur} {p}".strip()
    if cur:
        out.append(cur)
    return out


def _cortar(w):
    res, cur = [], ""
    for x in w.split():
        if cur and len(cur) + 1 + len(x) > MAXC:
            res.append(cur)
            cur = x
        else:
            cur = f"{cur} {x}".strip()
    return res + [cur]


def main():
    md = open(sys.argv[1], encoding="utf-8").read()
    fin = seg(sys.argv[sys.argv.index("--fin") + 1]) if "--fin" in sys.argv else 1e9
    rows = list(filas(md))
    n, out = 1, []
    for i, (t0, txt) in enumerate(rows):
        t1 = rows[i + 1][0] if i + 1 < len(rows) else fin
        ch = trozos(txt)
        durs = [max(1.2, len(c.split()) / PPS) for c in ch]
        k = min(1.0, (t1 - t0 - 0.2) / sum(durs))
        t = t0
        for c, d in zip(ch, durs):
            out.append(f"{n}\n{ts(t)} --> {ts(t + d * k)}\n{c}\n")
            t += d * k
            n += 1
        if k < 1:
            print(f"AVISO {ts(t0)}: texto comprimido al {k:.0%}", file=sys.stderr)
    open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out))
    print(f"{n - 1} subtítulos")


if __name__ == "__main__":
    main()
