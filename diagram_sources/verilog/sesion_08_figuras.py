"""Genera las figuras SVG de la sesion 8 (contadores).

Uso (desde la raiz del proyecto):
    python diagram_sources/verilog/sesion_08_figuras.py

Reutiliza el estilo de las sesiones anteriores y escribe los SVG en
book/_static/verilog/sesion_08/svg/.
"""

from pathlib import Path

from sesion_03_figuras import (ACCENT, CARD_BG, CARD_BORDER, GATE_FILL, GRID, INK, MUTED, SANS, dot, gate,
                               over, svg_doc, text, wire)
from sesion_05_figuras import subc
from sesion_06_figuras import C_WAVE, wave
from sesion_07_figuras import ff, label_in, label_out, tramos, vgate

OUT_DIR = Path(__file__).resolve().parents[2] / "book" / "_static" / "verilog" / "sesion_08" / "svg"

NQ = over("Q")


# --------------------------------------------------------------- utilidades
def gate_left(kind, xr, y, h):
    """Puerta que apunta hacia la izquierda. xr: lado de las entradas.

    Devuelve (svg, entradas de arriba abajo, salida).
    """
    g, ins, out = gate(kind, 0, 0, h=h)
    svg = f'<g transform="translate({xr},{y}) scale(-1,1)">{g}</g>'
    T = lambda p: (round(xr - p[0], 1), round(y + p[1], 1))  # noqa: E731
    return svg, [T(p) for p in ins], T(out)


def name(x, y, content, anchor="middle", size=13):
    """Nombre de puerta o biestable usado en el codigo Verilog."""
    return text(x, y, content, size=size, color=ACCENT, anchor=anchor, weight="bold")


def cable(x, y, content, anchor="start", size=12):
    """Nombre de cable usado en el codigo Verilog."""
    return text(x, y, content, size=size, color=MUTED, anchor=anchor)


# ------------------------------------------------- biestables T y JK
def fig_biestables():
    b = []
    svg, p = ff(90, 25, 80, 110, left=[], right=[("Q", 0.25)], clk=0.5, clk_label="T")
    b.append(svg)
    b.append(label_in(62, p["C"][1], "C"))
    svg, _ = ff(300, 25, 90, 110, left=[("J", 0.2), ("K", 0.8)], right=[("Q", 0.2), (NQ, 0.8)], clk=0.5)
    b.append(svg)
    return svg_doc(450, 160, "\n".join(b), "Simbolos de los biestables T y JK")


# ------------------------------------- contador ascendente/descendente
def fig_contador(named=False):
    w, h = 900, 200
    b = []
    y_rail = 172
    xs = [130 + i * 200 for i in range(4)]
    for i, x in enumerate(xs):
        svg, p = ff(x, 40, 80, 100, left=[], right=[("Q", 0.25)], clk=0.55, clk_label="T")
        b.append(svg)
        xq, yq = p["Q"]
        b.append(text(xq + 6, yq - 6, subc("Q", i + 1, size=16), size=16, color=ACCENT, weight="bold"))
        if named:
            b.append(name(x + 50, 122, f"T{i + 1}"))
            b.append(cable(xq + 6, yq - 26, f"Q[{i}]"))
        if i == 0:
            b.append(wire((95, p["C"][1]), p["C"]))
            b.append(label_in(88, p["C"][1], "C"))
        if i < 3:
            g, ins, out = gate("xor", x + 124, 75, h=40, label=f"x{i + 1}" if named else None)
            b.append(g)
            b.append(wire((xq, yq), (xq, ins[0][1]), ins[0]))
            xr = x + 110
            b.append(wire((xr, y_rail), (xr, ins[1][1]), ins[1]))
            if i < 2:
                b.append(dot(xr, y_rail))
            b.append(wire(out, (x + 180, out[1])))
            if named:
                b.append(cable(x + 180, out[1] - 9, f"b{i + 1}", anchor="middle"))
    b.append(wire((95, y_rail), (xs[2] + 110, y_rail)))
    b.append(label_in(88, y_rail, f"DEC/{over('INC')}"))
    if named:
        b.append(cable(105, y_rail - 8, "DECnINC"))
    extra = " con nombres" if named else ""
    return svg_doc(w, h, "\n".join(b), f"Contador ascendente/descendente de cuatro bits{extra}")


# --------------------------------------- biestable T con CLEAR y PRESET
def t_block(x, y, w, h, y_c, y_q, y_nq, x_clr, x_pre):
    b = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{GATE_FILL}" stroke="{INK}" stroke-width="2"/>']
    b.append(text(x + w / 2, y + 28, "T", size=22, anchor="middle", weight="bold", family=SANS))
    b.append(f'<circle cx="{x - 5}" cy="{y_c}" r="5" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
    b.append(wire((x - 30, y_c), (x - 10, y_c)))
    b.append(f'<path d="M{x},{y_c - 7} L{x + 10},{y_c} L{x},{y_c + 7}" fill="none" stroke="{INK}" '
             f'stroke-width="2" stroke-linejoin="round"/>')
    b.append(text(x + 15, y_c + 5, "C", size=13, color=MUTED))
    b.append(label_in(x - 38, y_c, "C"))
    b.append(text(x + w - 8, y_q + 5, "Q", size=13, color=MUTED, anchor="end"))
    b.append(text(x + w - 8, y_nq + 5, "nQ", size=13, color=MUTED, anchor="end"))
    b.append(text(x_clr, y + h - 8, "nCLEAR", size=12, color=MUTED, anchor="middle"))
    b.append(text(x_pre, y + h - 8, "nPRESET", size=12, color=MUTED, anchor="middle"))
    return "\n".join(b)


def fig_t_completo():
    b = [t_block(100, 20, 300, 140, 95, 65, 115, 200, 300)]
    for yy in (65, 115):
        b.append(wire((400, yy), (430, yy)))
    for xx in (200, 300):
        b.append(wire((xx, 160), (xx, 190)))
    return svg_doc(470, 200, "\n".join(b), "Biestable T con lineas nCLEAR y nPRESET y salida nQ")


def fig_thold(named=False):
    w, h = 610, 510
    x_clr, x_pre, y_q, y_nq = 180, 300, 70, 130
    b = [t_block(70, 20, 360, 170, 100, y_q, y_nq, x_clr, x_pre)]
    # Salidas
    xdq, xdn, x_hold = 500, 465, 480
    for yy, lab, xd in ((y_q, "Q", xdq), (y_nq, "nQ", xdn)):
        b.append(wire((430, yy), (545, yy)))
        b.append(label_out(553, yy, lab))
        b.append(dot(xd, yy))
    # Puertas AND hacia nCLEAR y nPRESET
    ga, ia, oa = vgate("and", x_clr - 22, 290, 44, direction="up")
    gp, ip, op = vgate("and", x_pre - 22, 290, 44, direction="up")
    b += [ga, gp]
    b.append(wire(oa, (x_clr, 190)))
    b.append(wire(op, (x_pre, 190)))
    b.append(wire(ia[0], (ia[0][0], 470))); b.append(text(ia[0][0], 492, "nCLEAR", size=14, anchor="middle"))
    b.append(wire(ip[0], (ip[0][0], 470))); b.append(text(ip[0][0], 492, "nPRESET", size=14, anchor="middle"))
    # Puertas OR con nHOLD
    gop, iop, oop = gate_left("or", 440, 330, 44)
    goc, ioc, ooc = gate_left("or", 440, 400, 44)
    b += [gop, goc]
    b.append(wire(oop, (ip[1][0], oop[1]), ip[1]))
    b.append(wire(ooc, (ia[1][0], ooc[1]), ia[1]))
    b.append(wire((xdn, y_nq), (xdn, iop[0][1]), iop[0]))
    b.append(wire((xdq, y_q), (xdq, ioc[0][1]), ioc[0]))
    b.append(wire((x_hold, 470), (x_hold, iop[1][1]), iop[1]))
    b.append(wire((x_hold, ioc[1][1]), ioc[1])); b.append(dot(x_hold, ioc[1][1]))
    b.append(text(x_hold, 492, "nHOLD", size=14, anchor="middle"))
    if named:
        b.append(name(250, 105, "jose", size=15))
        b.append(cable(x_clr + 8, 216, "cCLEAR"))
        b.append(cable(x_pre + 8, 216, "cPRESET"))
        b.append(name(x_clr, 275, "aC"))
        b.append(name(x_pre, 275, "aP"))
        b.append(name(414, oop[1] + 5, "oP"))
        b.append(name(414, ooc[1] + 5, "oC"))
        b.append(cable(350, oop[1] - 8, "cOP", anchor="middle"))
        b.append(cable(350, ooc[1] - 8, "cOC", anchor="middle"))
    extra = " con nombres" if named else ""
    return svg_doc(w, h, "\n".join(b), f"Biestable T con linea de HOLD{extra}")


# ------------------------------------------------- contador sincrono
def fig_contsinc():
    w, h = 880, 275
    b = []
    y_clk, y_q1, y_q2, y_q3 = 250, 30, 42, 54
    xs = [120 + i * 200 for i in range(4)]
    pins = []
    for i, x in enumerate(xs):
        svg, p = ff(x, 110, 80, 110, left=[("J", 0.2), ("K", 0.8)], right=[("Q", 0.2)], clk=0.5)
        b.append(svg)
        pins.append(p)
        # J y K unidas
        xt = x - 45
        b.append(wire((xt, p["J"][1]), p["J"]))
        b.append(wire((xt, p["J"][1]), (xt, p["K"][1]), p["K"]))
        b.append(dot(xt, p["J"][1]))
        # Reloj
        xc = x - 30
        b.append(wire((xc, y_clk), (xc, p["C"][1]), p["C"]))
        if i < 3:
            b.append(dot(xc, y_clk))
        b.append(text(p["Q"][0] + 8, p["Q"][1] + 20, subc("Q", i + 1, size=16), size=16, color=ACCENT,
                      weight="bold", anchor="middle"))
    yj = pins[0]["J"][1]
    b.append(wire((50, y_clk), (xs[3] - 30, y_clk)))
    b.append(label_in(42, y_clk, "C"))
    b.append(wire((50, yj), (xs[0] - 45, yj)))
    b.append(label_in(42, yj, "1"))
    # Q1: a J/K del segundo biestable y a las dos AND
    xq1 = pins[0]["Q"][0] + 15
    b.append(wire(pins[0]["Q"], (xs[1] - 45, yj)))
    b.append(dot(xq1, yj))
    # AND de dos y de tres entradas
    x_a1, x_a2 = xs[2] - 45, xs[3] - 45
    g1, in1, o1 = vgate("and", x_a1 - 18, 62, 36)
    g2, in2, o2 = vgate("and", x_a2 - 24, 62, 48, n_in=3)
    b += [g1, g2]
    b.append(wire(o1, (x_a1, yj)))
    b.append(wire(o2, (x_a2, yj)))
    b.append(wire((xq1, yj), (xq1, y_q1), (in2[2][0], y_q1), in2[2]))
    b.append(wire((in1[1][0], y_q1), in1[1])); b.append(dot(in1[1][0], y_q1))
    # Q2
    xq2 = pins[1]["Q"][0] + 15
    b.append(wire(pins[1]["Q"], (xq2, yj), (xq2, y_q2), (in2[1][0], y_q2), in2[1]))
    b.append(wire((in1[0][0], y_q2), in1[0])); b.append(dot(in1[0][0], y_q2))
    # Q3
    xq3 = pins[2]["Q"][0] + 15
    b.append(wire(pins[2]["Q"], (xq3, yj), (xq3, y_q3), (in2[0][0], y_q3), in2[0]))
    b.append(wire(pins[3]["Q"], (pins[3]["Q"][0] + 15, yj)))
    return svg_doc(w, h, "\n".join(b), "Contador sincrono de cuatro bits con biestables JK")


# --------------------------------------- contador de cuenta arbitraria
def fig_analisis():
    w, h = 930, 415
    b = []
    y_clk = 230
    xs = [150, 420, 690]
    pins = []
    for i, x in enumerate(xs):
        svg, p = ff(x, 80, 90, 120, left=[("J", 0.2), ("K", 0.8)], right=[("Q", 0.2), (NQ, 0.8)], clk=0.5)
        b.append(svg)
        pins.append(p)
        xc = x - 40
        b.append(wire((xc, y_clk), (xc, p["C"][1]), p["C"]))
        if i < 2:
            b.append(dot(xc, y_clk))
        b.append(text(p["Q"][0] + 3, p["Q"][1] + 21, subc("Q", i, size=16), size=16, color=ACCENT, weight="bold"))
    p0, p1, p2 = pins
    yq, ynq = p0["Q"][1], p0[NQ][1]
    b.append(wire((40, y_clk), (xs[2] - 40, y_clk)))
    b.append(label_in(32, y_clk, "C"))
    # J1 = 1
    b.append(wire((392, yq), p1["J"]))
    b.append(text(386, yq + 5, "1", size=15, anchor="end"))
    # Q0: a J2 (por arriba) y a la AND
    b.append(wire(p0["Q"], (300, yq), (300, 345), (380, 345), (380, 330)))
    b.append(dot(275, yq))
    b.append(wire((275, yq), (275, 30), (640, 30), (640, yq), p2["J"]))
    # Q0 negada: a K2
    b.append(wire(p0[NQ], (285, ynq), (285, 260), (660, 260), (660, ynq), p2["K"]))
    # AND -> K1
    ga, ia, oa = vgate("and", 370, 330, 40, direction="up")
    b.append(ga)
    b.append(wire(oa, (390, ynq), p1["K"]))
    b.append(wire(ia[1], (400, 365))); b.append(dot(400, 365))
    # Q2 negada: a J0 y a la AND
    b.append(wire(p2[NQ], (830, ynq), (830, 365), (60, 365), (60, yq), p0["J"]))
    # Q1 negada: sin conectar
    b.append(wire(p1[NQ], (p1[NQ][0] + 15, ynq)))
    # XOR de Q2 y Q1 -> K0
    gx, ix, ox = vgate("xor", 850, 120, 40)
    b.append(gx)
    b.append(wire(p2["Q"], (ix[0][0], yq), ix[0]))
    b.append(wire(p1["Q"], (555, yq), (555, 50), (ix[1][0], 50), ix[1]))
    b.append(wire(ox, (ox[0], 395), (85, 395), (85, ynq), p0["K"]))
    return svg_doc(w, h, "\n".join(b), "Contador de cuenta arbitraria con tres biestables JK")


# ------------------------------------------------------- cronogramas
def bus(x0, ybase, segs, unit, amp=22):
    """Senal de varios bits: tramos (inicio, fin, etiqueta) dibujados como en GTKwave."""
    b = []
    ym, yt = ybase - amp / 2, ybase - amp
    for a, c, lab in segs:
        xa, xc = x0 + a * unit, x0 + c * unit
        b.append(f'<path d="M{xa},{ym} L{xa + 4},{yt} L{xc - 4},{yt} L{xc},{ym} L{xc - 4},{ybase} '
                 f'L{xa + 4},{ybase} Z" fill="none" stroke="{C_WAVE}" stroke-width="2" stroke-linejoin="round"/>')
        b.append(text((xa + xc) / 2, ym + 4.5, lab, size=12, anchor="middle"))
    return "\n".join(b)


def fig_crono(hold):
    """Cronograma del contador: sin HOLD (con salto en t=100) o con HOLD."""
    n, unit = 200, 3.6
    x0, y0, row = 150, 62, 38
    reloj = [(k // 5) % 2 for k in range(n)]
    dec = tramos(n, (0, 100))
    if hold:
        cuenta = [15 - k for k in range(9)] + [6] + [7 + k for k in range(9)]
        cortes = [10 * k for k in range(10)] + [110 + 10 * k for k in range(10)]
        rows = [("C", reloj), ("DECnINC", dec), ("nHOLD", tramos(n, (0, 99), (101, n)))]
        title = "Cronograma del contador con linea de HOLD"
    else:
        cuenta = [15 - k for k in range(10)] + [9, 10, 11, 12, 13, 14, 15, 0, 1, 2]
        cortes = [10 * k for k in range(21)]
        rows = [("C", reloj), ("DECnINC", dec)]
        title = "Cronograma del contador con salto al cambiar el modo de cuenta"
    segs = [(a, c, str(v)) for a, c, v in zip(cortes, cortes[1:], cuenta)]
    w = x0 + n * unit + 50
    h = y0 + (len(rows) + 1) * row + 20
    b = [f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="10" fill="{CARD_BG}" '
         f'stroke="{CARD_BORDER}" stroke-width="1.5"/>']
    b.append(text(24, 36, "Signals", size=13, color=MUTED, weight="bold"))
    b.append(text(x0, 36, "Waves", size=13, color=MUTED, weight="bold"))
    for t in range(0, n + 1, 10):
        x = x0 + t * unit
        b.append(wire((x, y0 - 8), (x, h - 22), color=GRID, width=1))
        if t % 100 == 0:
            b.append(text(x + 3, y0 - 12, str(t), size=11, color=MUTED))
    for k, (lab, v) in enumerate(rows):
        yb = y0 + (k + 1) * row - 8
        b.append(text(x0 - 16, yb - 7, lab, size=14, anchor="end"))
        b.append(wave(x0, yb, v, unit, amp=22))
    yb = y0 + (len(rows) + 1) * row - 8
    b.append(text(x0 - 16, yb - 7, "Q[3:0]", size=14, anchor="end"))
    b.append(bus(x0, yb, segs, unit))
    return svg_doc(w, h, "\n".join(b), title)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "biestables.svg": fig_biestables(),
        "contador.svg": fig_contador(),
        "contador_nombres.svg": fig_contador(named=True),
        "t_completo.svg": fig_t_completo(),
        "thold.svg": fig_thold(),
        "thold_nombres.svg": fig_thold(named=True),
        "contsinc.svg": fig_contsinc(),
        "analisis.svg": fig_analisis(),
        "cron_salto.svg": fig_crono(hold=False),
        "cron_contador.svg": fig_crono(hold=True),
    }
    for fname, content in files.items():
        (OUT_DIR / fname).write_text(content, encoding="utf-8")
        print("ok", fname)


if __name__ == "__main__":
    main()
