"""Genera las figuras SVG de la sesion 6 (biestables).

Uso (desde la raiz del proyecto):
    python diagram_sources/verilog/sesion_06_figuras.py

Reutiliza el estilo de las sesiones anteriores y escribe los SVG en
book/_static/verilog/sesion_06/svg/.
"""

from pathlib import Path

from sesion_03_figuras import ACCENT, GATE_FILL, INK, MUTED, dot, gate, over, svg_doc, text, wire
from sesion_04_figuras import sub
from sesion_05_figuras import subc

OUT_DIR = Path(__file__).resolve().parents[2] / "book" / "_static" / "verilog" / "sesion_06" / "svg"

C_WAVE = "#2563EB"


# --------------------------------------------------------------- utilidades
def ff_block(x, y, w, h, left, right, top=None, bottom=None):
    """Simbolo de bloque de un biestable.

    left/right: listas de (etiqueta, fraccion_vertical). top/bottom: etiqueta de
    una entrada con circulo de negacion por arriba o por abajo.
    """
    b = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{GATE_FILL}" stroke="{INK}" stroke-width="2"/>']
    for lab, f in left:
        yy = y + f * h
        b.append(wire((x - 26, yy), (x, yy)))
        b.append(text(x + 8, yy + 5, lab, size=13, color=MUTED))
    for lab, f in right:
        yy = y + f * h
        b.append(wire((x + w, yy), (x + w + 26, yy)))
        b.append(text(x + w - 8, yy + 5, lab, size=13, color=MUTED, anchor="end"))
    r = 5
    if top:
        cx = x + w / 2
        b.append(f'<circle cx="{cx}" cy="{y - r}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
        b.append(wire((cx, y - 2 * r), (cx, y - 26)))
        b.append(text(cx, y + 17, top, size=11, color=MUTED, anchor="middle"))
    if bottom:
        cx = x + w / 2
        b.append(f'<circle cx="{cx}" cy="{y + h + r}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
        b.append(wire((cx, y + h + 2 * r), (cx, y + h + 26)))
        b.append(text(cx, y + h - 8, bottom, size=11, color=MUTED, anchor="middle"))
    return "\n".join(b)


def nor_latch(x, y, gh=50, gap=100, xdot=None):
    """Pareja de NOR con realimentacion cruzada.

    Devuelve (svg, entrada_R, entrada_S, salida_Q, salida_nQ) donde las salidas
    son los puntos de union desde los que se toman Q y Q negada.
    """
    b = []
    g1, i1, o1 = gate("nor", x, y, h=gh)
    g2, i2, o2 = gate("nor", x, y + gap, h=gh)
    b += [g1, g2]
    xd = xdot or o1[0] + 30
    b.append(wire(o1, (xd, o1[1])))
    b.append(wire(o2, (xd, o2[1])))
    b.append(dot(xd, o1[1]))
    b.append(dot(xd, o2[1]))
    xm = x + 0.55 * gh + 20
    ya, yb = o1[1] + 20, o2[1] - 20
    yl1, yl2 = y + gh + 18, y + gap - 18
    # Q realimenta la segunda NOR; Q negada la primera (cruce en X)
    b.append(wire((xd, o1[1]), (xd, ya), (xm, yl2), (x - 15, yl2), (x - 15, i2[0][1]), i2[0]))
    b.append(wire((xd, o2[1]), (xd, yb), (xm, yl1), (x - 22, yl1), (x - 22, i1[1][1]), i1[1]))
    return "\n".join(b), i1[0], i2[1], (xd, o1[1]), (xd, o2[1])


# ---------------------------------------------------------------- RS con NOR
def fig_rs():
    w, h = 600, 200
    b = []
    latch, in_r, in_s, q, nq = nor_latch(120, 25)
    b.append(latch)
    b.append(wire((40, in_r[1]), in_r)); b.append(text(32, in_r[1] + 6, "R", size=16, anchor="end"))
    b.append(wire((40, in_s[1]), in_s)); b.append(text(32, in_s[1] + 6, "S", size=16, anchor="end"))
    for p, lab in ((q, "Q"), (nq, over("Q"))):
        b.append(wire(p, (p[0] + 36, p[1])))
        b.append(text(p[0] + 44, p[1] + 6, lab, size=16, color=ACCENT, weight="bold"))
    b.append(ff_block(440, 40, 90, 120, left=[("R", 0.22), ("S", 0.78)],
                      right=[("Q", 0.22), (over("Q"), 0.78)]))
    return svg_doc(w, h, "\n".join(b), "Biestable RS con dos puertas NOR y su simbolo")


# ------------------------------------------------------- RS con reloj
def fig_rsc():
    w, h = 660, 240
    b = []
    latch, in_r, in_s, q, nq = nor_latch(230, 30)
    b.append(latch)
    ga, ia, oa = gate("and", 110, in_r[1] - 22, h=44)
    gb, ib, ob = gate("and", 110, in_s[1] - 22, h=44)
    b += [ga, gb]
    b.append(wire(oa, in_r))
    b.append(wire(ob, in_s))
    b.append(wire((40, ia[0][1]), ia[0])); b.append(text(32, ia[0][1] + 6, "R", size=16, anchor="end"))
    b.append(wire((40, ib[1][1]), ib[1])); b.append(text(32, ib[1][1] + 6, "S", size=16, anchor="end"))
    yc = (ia[1][1] + ib[0][1]) / 2
    xc = 80
    b.append(wire((40, yc), (xc, yc))); b.append(text(32, yc + 6, "C", size=16, anchor="end"))
    b.append(wire((xc, ia[1][1]), (xc, ib[0][1])))
    b.append(wire((xc, ia[1][1]), ia[1]))
    b.append(wire((xc, ib[0][1]), ib[0]))
    b.append(dot(xc, yc))
    for p, lab in ((q, "Q"), (nq, over("Q"))):
        b.append(wire(p, (p[0] + 36, p[1])))
        b.append(text(p[0] + 44, p[1] + 6, lab, size=16, color=ACCENT, weight="bold"))
    b.append(ff_block(510, 50, 90, 140, left=[("R", 0.2), ("C", 0.5), ("S", 0.8)],
                      right=[("Q", 0.2), (over("Q"), 0.8)]))
    return svg_doc(w, h, "\n".join(b), "Biestable RS con entrada de reloj y su simbolo")


# ------------------------------------------------ detector de flanco de subida
def wave(x0, ybase, values, unit, amp=26, color=C_WAVE):
    pts = []
    prev = None
    for t, v in enumerate(values):
        y = ybase - v * amp
        x = x0 + t * unit
        if prev is not None and prev != y:
            pts.append((x, prev))
        pts.append((x, y))
        prev = y
    pts.append((x0 + len(values) * unit, prev))
    return wire(*pts, color=color, width=2.2)


def fig_detector():
    w, h = 820, 220
    b = []
    yc = 80
    gn, inn, onn = gate("not", 95, yc - 13, h=26, n_in=1)
    ga, ia, oa = gate("and", 200, yc - 14, h=56)
    b += [gn, ga]
    b.append(wire((40, yc), inn[0]))
    b.append(text(32, yc + 6, "C", size=16, anchor="end"))
    b.append(dot(65, yc))
    b.append(wire(onn, ia[0]))
    b.append(wire((65, yc), (65, ia[1][1]), ia[1]))
    b.append(text(104, yc - 20, "#(1)", size=12, color=MUTED, anchor="middle"))
    b.append(text(140, yc - 8, subc("C", "nr", size=14), size=14, color=MUTED))
    b.append(wire(oa, (oa[0] + 40, oa[1])))
    b.append(text(oa[0] + 48, oa[1] + 6, "DET", size=16, color=ACCENT, weight="bold"))
    # Cronograma: periodo 8 unidades, retardo de la NOT = 1 unidad
    unit, n = 11, 34
    clk = [1 if (t % 8) in (2, 3, 4, 5) else 0 for t in range(n)]
    cnr = [1 - clk[t - 1] if t >= 1 else 1 for t in range(n)]
    det = [clk[t] & cnr[t] for t in range(n)]
    x0 = 440
    rows = ((50, clk, "C"), (125, cnr, subc("C", "nr", size=14)), (200, det, "DET"))
    for ybase, vals, lab in rows:
        b.append(text(x0 - 12, ybase, lab, size=14, anchor="end"))
        b.append(wave(x0, ybase, vals, unit))
    return svg_doc(w, h, "\n".join(b), "Detector de flanco de subida y su cronograma")


# ---------------------------------------------- JK con PRESET y CLEAR
def fig_jk():
    w, h = 700, 330
    b = []
    xg1, xg2 = 150, 340
    n1, i1, o1 = gate("nand", xg1, 40, h=72, n_in=4)    # J, C, CLEAR, nQ
    n2, i2, o2 = gate("nand", xg1, 196, h=72, n_in=4)   # PRESET, Q, C, K
    n3, i3, o3 = gate("nand", xg2, 46, h=60, n_in=3)    # PRESET, n1, nQ  -> Q
    n4, i4, o4 = gate("nand", xg2, 202, h=60, n_in=3)   # Q, n2, CLEAR    -> nQ
    b += [n1, n2, n3, n4]
    # Entradas J, C, K
    b.append(wire((40, i1[0][1]), i1[0])); b.append(text(32, i1[0][1] + 6, "J", size=16, anchor="end"))
    b.append(wire((40, i2[3][1]), i2[3])); b.append(text(32, i2[3][1] + 6, "K", size=16, anchor="end"))
    yc, xc = 150, 100
    b.append(wire((40, yc), (xc, yc))); b.append(text(32, yc + 6, "C", size=16, anchor="end"))
    b.append(wire((xc, i1[1][1]), (xc, i2[2][1])))
    b.append(wire((xc, i1[1][1]), i1[1]))
    b.append(wire((xc, i2[2][1]), i2[2]))
    b.append(dot(xc, yc))
    # Primer nivel -> segundo nivel
    b.append(wire(o1, i3[1]))
    b.append(wire(o2, i4[1]))
    # Salidas y realimentacion
    xq, xnq = 440, 455
    b.append(wire(o3, (xq, o3[1]), (510, o3[1]))); b.append(dot(xq, o3[1]))
    b.append(wire(o4, (xnq, o4[1]), (510, o4[1]))); b.append(dot(xnq, o4[1]))
    b.append(text(518, o3[1] + 6, "Q", size=16, color=ACCENT, weight="bold"))
    b.append(text(518, o4[1] + 6, over("Q"), size=16, color=ACCENT, weight="bold"))
    yq, ynq = 170, 138
    b.append(wire((xq, o3[1]), (xq, yq), (130, yq), (130, i2[1][1]), i2[1]))
    b.append(wire((318, yq), (318, i4[0][1]), i4[0])); b.append(dot(318, yq))
    b.append(wire((xnq, o4[1]), (xnq, ynq), (120, ynq), (120, i1[3][1]), i1[3]))
    b.append(wire((318, ynq), (318, i3[2][1]), i3[2])); b.append(dot(318, ynq))
    # PRESET (desde arriba)
    xp = 280
    b.append(wire((xp, 18), (xp, 188), (140, 188), (140, i2[0][1]), i2[0]))
    b.append(wire((xp, i3[0][1]), i3[0])); b.append(dot(xp, i3[0][1]))
    b.append(text(xp, 14, over("PRESET"), size=13, anchor="middle"))
    # CLEAR (desde abajo)
    xl = 292
    b.append(wire((xl, 312), (xl, 120), (140, 120), (140, i1[2][1]), i1[2]))
    b.append(wire((xl, i4[2][1]), i4[2])); b.append(dot(xl, i4[2][1]))
    b.append(text(xl, 328, over("CLEAR"), size=13, anchor="middle"))
    # Simbolo
    b.append(ff_block(590, 95, 80, 140, left=[("J", 0.2), ("C", 0.5), ("K", 0.8)],
                      right=[("Q", 0.2), (over("Q"), 0.8)], top="CLR", bottom="PR"))
    return svg_doc(w, h, "\n".join(b), "Biestable JK con PRESET y CLEAR y su simbolo")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "rs.svg": fig_rs(),
        "rsc.svg": fig_rsc(),
        "det.svg": fig_detector(),
        "jk.svg": fig_jk(),
    }
    for name, content in files.items():
        (OUT_DIR / name).write_text(content, encoding="utf-8")
        print("ok", name)


if __name__ == "__main__":
    main()
