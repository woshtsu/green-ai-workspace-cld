"""Convierte el .srt en .ass con subtítulos apilados (el más reciente abajo).

Uso: python srt_a_ass_apilado.py ENTRADA.srt SALIDA.ass
libass apila los solapes poniendo el nuevo arriba; aquí se calcula la
posición de cada subtítulo en cada intervalo para que el orden se lea de
arriba (antiguo) a abajo (nuevo). Caja semitransparente, 1920×1080.
"""
import re
import sys

BASE = 135        # margen inferior del piso más bajo (px)
LINEA = 50        # alto de una línea con caja (px)
HUECO = 12        # separación entre pisos (px)
CPL = 40          # caracteres por línea

CAB = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Segoe UI,40,&H00FFFFFF,&H00FFFFFF,&H55000000,&H55000000,1,0,0,0,100,100,0,0,3,10,0,2,400,400,135,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def seg(x):
    h, m, r = x.split(":")
    return int(h) * 3600 + int(m) * 60 + float(r.replace(",", "."))


def ts(x):
    cs = int(round(x * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def partir(txt):
    lin, cur = [], ""
    for w in txt.split():
        if cur and len(cur) + 1 + len(w) > CPL:
            lin.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lin + [cur]


def main():
    s = open(sys.argv[1], encoding="utf-8").read()
    subs = []
    for a, e, txt in re.findall(r"\d+\n(\S+) --> (\S+)\n(.*?)(?:\n\n|\Z)", s, re.S):
        lin = partir(" ".join(txt.split()))
        subs.append((seg(a), seg(e), lin))
    cortes = sorted({t for a, e, _ in subs for t in (a, e)})
    out = []
    for t0, t1 in zip(cortes, cortes[1:]):
        act = sorted((x for x in subs if x[0] <= t0 and x[1] >= t1), key=lambda x: -x[0])
        y = BASE
        for a, e, lin in act:          # del más nuevo (abajo) al más antiguo
            out.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Default,,0,0,{y},,{'\\N'.join(lin)}")
            y += len(lin) * LINEA + HUECO
    open(sys.argv[2], "w", encoding="utf-8").write(CAB + "\n".join(out) + "\n")
    print(f"{len(subs)} subtítulos, {len(out)} eventos")


if __name__ == "__main__":
    main()
