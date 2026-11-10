"""Genera las figuras SVG de la sesion 7 (registros).

Uso (desde la raiz del proyecto):
    python diagram_sources/verilog/sesion_07_figuras.py

Reutiliza el estilo de las sesiones anteriores y escribe los SVG en
book/_static/verilog/sesion_07/svg/.
"""

from pathlib import Path

from sesion_03_figuras import (ACCENT, CARD_BG, CARD_BORDER, GATE_FILL, GRID, INK, MUTED, SANS, dot, gate,
                               over, svg_doc, text, wire)
from sesion_04_figuras import dashed_box
from sesion_05_figuras import not_up, subc
from sesion_06_figuras import C_WAVE, fig_detector, wave

OUT_DIR = Path(__file__).resolve().parents[2] / "book" / "_static" / "verilog" / "sesion_07" / "svg"


# --------------------------------------------------------------- utilidades
def ff(x, y, w, h, left, right, clk=None, clr=False, stub=20):
    """Biestable con reloj por flanco de bajada y CLR opcional (activo por nivel bajo).

    left/right: listas de (etiqueta, fraccion_vertical); clk: fraccion de la
    entrada de reloj. Devuelve (svg, pines) con el extremo libre de cada pin.
    """
    b = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{GATE_FILL}" stroke="{INK}" stroke-width="2"/>']
    pins = {}
    for lab, f in left:
        yy = y + f * h
        b.append(wire((x - stub, yy), (x, yy)))
        b.append(text(x + 8, yy + 5, lab, size=13, color=MUTED))
        pins[lab] = (x - stub, yy)
    for lab, f in right:
        yy = y + f * h
        b.append(wire((x + w, yy), (x + w + stub, yy)))
        b.append(text(x + w - 8, yy + 5, lab, size=13, color=MUTED, anchor="end"))
        pins[lab] = (x + w + stub, yy)
    r = 5
    if clk is not None:
        yy = y + clk * h
        b.append(f'<circle cx="{x - r}" cy="{yy}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
        b.append(wire((x - stub, yy), (x - 2 * r, yy)))
        b.append(f'<path d="M{x},{yy - 7} L{x + 10},{yy} L{x},{yy + 7}" fill="none" stroke="{INK}" '
                 f'stroke-width="2" stroke-linejoin="round"/>')
        b.append(text(x + 15, yy + 5, "C", size=13, color=MUTED))
        pins["C"] = (x - stub, yy)
    if clr:
        cx = x + w / 2
        b.append(f'<circle cx="{cx}" cy="{y - r}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
        b.append(wire((cx, y - 2 * r), (cx, y - stub)))
        b.append(text(cx, y + 17, "CLR", size=11, color=MUTED, anchor="middle"))
        pins["CLR"] = (cx, y - stub)
    return "\n".join(b), pins


def vgate(kind, xl, y, w, n_in=2, direction="down"):
    """Puerta girada. xl: borde izquierdo; y: lado de las entradas.

    Devuelve (svg, entradas ordenadas de izquierda a derecha, salida).
    """
    g, ins, out = gate(kind, 0, 0, h=w, n_in=n_in)
    if direction == "down":
        svg = f'<g transform="translate({xl + w},{y}) rotate(90)">{g}</g>'
        T = lambda p: (round(xl + w - p[1], 1), round(y + p[0], 1))  # noqa: E731
    else:
        svg = f'<g transform="translate({xl},{y}) rotate(-90)">{g}</g>'
        T = lambda p: (round(xl + p[1], 1), round(y - p[0], 1))  # noqa: E731
    return svg, sorted((T(p) for p in ins), key=lambda p: p[0]), T(out)


def label_in(x, y, content, size=16):
    return text(x, y + 6, content, size=size, anchor="end")


def label_out(x, y, content, size=16, anchor="start"):
    return text(x, y + 6, content, size=size, color=ACCENT, weight="bold", anchor=anchor)


# ------------------------------------------------------------- biestable D
def fig_d():
    w, h = 260, 160
    svg, _ = ff(85, 25, 90, 110, left=[("D", 0.25)], right=[("Q", 0.25)], clk=0.65)
    return svg_doc(w, h, svg, "Biestable D activo por flanco de bajada")


# ------------------------------------------- biestable D activo por nivel
def d_latch(ox=0, low=False, names=False, labels=True):
    """Biestable D activo por nivel alto (o bajo) hecho con puertas, en un recuadro discontinuo."""
    b = [dashed_box(ox + 80, 18, 305, 178)]
    g1, i1, o1 = gate("and", ox + 180, 36, h=48, label="a1" if names else None)
    g2, i2, o2 = gate("and", ox + 180, 116, h=48, label="a2" if names else None)
    g3, i3, o3 = gate("or", ox + 275, 101, h=52, label="o" if names else None)
    b += [g1, g2, g3]
    b.append(wire(o1, (ox + 252, o1[1]), (ox + 252, i3[0][1]), i3[0]))
    b.append(wire(o2, i3[1]))
    # Salida Q y realimentacion
    xq = ox + 360
    b.append(wire(o3, (ox + 420, o3[1]))); b.append(dot(xq, o3[1]))
    b.append(wire((xq, o3[1]), (xq, 180), (ox + 150, 180), (ox + 150, i2[1][1]), i2[1]))
    # Entradas D y C
    b.append(wire((ox + 40, i1[0][1]), i1[0]))
    xd, yc = ox + 105, i2[0][1]
    b.append(dot(xd, yc))
    if low:
        gn, inn, onn = gate("not", ox + 118, i1[1][1] - 11, h=22, n_in=1)
        b.append(gn)
        b.append(wire((ox + 40, yc), i2[0]))
        b.append(wire((xd, yc), (xd, i1[1][1]), inn[0]))
        b.append(wire(onn, i1[1]))
    else:
        gn, inn, onn = gate("not", ox + 118, yc - 11, h=22, n_in=1)
        b.append(gn)
        b.append(wire((ox + 40, yc), inn[0]))
        b.append(wire((xd, yc), (xd, i1[1][1]), i1[1]))
        b.append(wire(onn, i2[0]))
    if names:
        b.append(text(ox + 122, 98, "n", size=12, color=MUTED))
        b.append(text(ox + 160, 92, "wn", size=12, color=MUTED, anchor="middle"))
        b.append(text(ox + 258, 88, "wa1", size=12, color=MUTED))
        b.append(text(ox + 255, 160, "wa2", size=12, color=MUTED, anchor="middle"))
    if labels:
        b.append(label_in(ox + 32, i1[0][1], "D"))
        b.append(label_in(ox + 32, yc, "C"))
    b.append(label_out(ox + 428, o3[1], "Q"))
    return "\n".join(b)


def fig_d_nivel(low=False, names=False):
    nivel = "bajo" if low else "alto"
    extra = " con nombres de puertas y cables" if names else ""
    return svg_doc(470, 210, d_latch(low=low, names=names), f"Biestable D activo por nivel {nivel}{extra}")


def fig_ddownedge():
    """Detector de flanco con OR antepuesto al biestable D activo por nivel bajo."""
    ox = 200
    b = [d_latch(ox, low=True, labels=False)]
    b.append(wire((40, 48), (ox + 40, 48))); b.append(label_in(32, 48, "D"))
    b.append(dashed_box(48, 78, 172, 88))
    gn, inn, onn = gate("not", 78, 103, h=26, n_in=1)
    go, io, oo = gate("or", 150, 104, h=48)
    b += [gn, go]
    b.append(wire((40, 116), inn[0])); b.append(label_in(32, 116, "C"))
    b.append(dot(62, 116))
    b.append(wire((62, 116), (62, io[1][1]), io[1]))
    b.append(wire(onn, io[0]))
    b.append(text(90, 97, "#(1)", size=12, color=MUTED, anchor="middle"))
    b.append(text(114, 108, subc("C", "nr", size=13), size=13, color=MUTED))
    b.append(wire(oo, (ox + 40, oo[1])))
    return svg_doc(ox + 470, 210, "\n".join(b), "Biestable D activo por flanco de bajada: detector y biestable activo por nivel bajo")


# ------------------------------------------------------------ registro SISO
def fig_siso(named=False):
    w, h = 770, 240
    b = []
    xs = [140 + i * 160 for i in range(4)]
    y_clr, y_ff, y_clk = 34, 76, 216
    pins = []
    for k, x in enumerate(xs):
        svg, p = ff(x, y_ff, 80, 104, left=[("D", 0.3)], right=[("Q", 0.3)], clk=0.68, clr=True)
        b.append(svg)
        pins.append(p)
        if named:
            b.append(text(x + 40, y_ff + 58, f"B{k + 1}", size=15, color=ACCENT, anchor="middle", weight="bold"))
            if k > 0:
                b.append(text(x - 40, p["D"][1] - 8, f"C{k}", size=13, color=MUTED, anchor="middle"))
    # CLR
    b.append(wire((50, y_clr), (pins[-1]["CLR"][0], y_clr), pins[-1]["CLR"]))
    b.append(label_in(42, y_clr, over("CLR")))
    for p in pins[:-1]:
        b.append(wire((p["CLR"][0], y_clr), p["CLR"]))
        b.append(dot(p["CLR"][0], y_clr))
    # Datos
    b.append(wire((80, pins[0]["D"][1]), pins[0]["D"]))
    b.append(label_in(72, pins[0]["D"][1], "I"))
    for a, c in zip(pins, pins[1:]):
        b.append(wire(a["Q"], c["D"]))
    b.append(wire(pins[-1]["Q"], (pins[-1]["Q"][0] + 20, pins[-1]["Q"][1])))
    b.append(label_out(pins[-1]["Q"][0] + 28, pins[-1]["Q"][1], "O"))
    # Reloj
    risers = [p["C"][0] - 12 for p in pins]
    b.append(wire((50, y_clk), (risers[-1], y_clk), (risers[-1], pins[-1]["C"][1]), pins[-1]["C"]))
    b.append(label_in(42, y_clk, "C"))
    for xr, p in zip(risers[:-1], pins[:-1]):
        b.append(wire((xr, y_clk), (xr, p["C"][1]), p["C"]))
        b.append(dot(xr, y_clk))
    extra = " con nombres de biestables y cables" if named else ""
    return svg_doc(w, h, "\n".join(b), f"Registro SISO de cuatro bits con biestables D{extra}")


def fig_siso_prueba():
    """Modulo de prueba: registros conectados al modulo SISO."""
    w, h = 720, 250
    b = []
    xb, yb, wb, hb = 220, 20, 380, 210
    b.append(f'<rect x="{xb}" y="{yb}" width="{wb}" height="{hb}" rx="8" fill="{GATE_FILL}" stroke="{INK}" stroke-width="2"/>')
    b.append(text(xb + wb / 2, yb + 34, "SISO", size=22, anchor="middle", weight="bold", family=SANS))
    b.append(text(xb + wb / 2, yb + hb / 2 + 6, "hector", size=16, color=ACCENT, anchor="middle", weight="bold"))
    for nombre, pin, y in (("lorena", "I", 70), ("angelica", "C", 125), ("pato", "nCLR", 180)):
        b.append(f'<rect x="20" y="{y - 17}" width="150" height="34" rx="6" fill="{CARD_BG}" stroke="{INK}" stroke-width="1.6"/>')
        b.append(text(95, y + 5, nombre, size=15, color=MUTED, anchor="middle"))
        if pin == "C":
            b.append(wire((170, y), (xb - 10, y)))
            b.append(f'<circle cx="{xb - 5}" cy="{y}" r="5" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
            b.append(f'<path d="M{xb},{y - 7} L{xb + 10},{y} L{xb},{y + 7}" fill="none" stroke="{INK}" '
                     f'stroke-width="2" stroke-linejoin="round"/>')
            b.append(text(xb + 15, y + 5, "C", size=13, color=MUTED))
        else:
            b.append(wire((170, y), (xb, y)))
            b.append(text(xb + 8, y + 5, pin, size=13, color=MUTED))
    b.append(wire((xb + wb, 125), (xb + wb + 40, 125)))
    b.append(text(xb + wb - 8, 130, "O", size=13, color=MUTED, anchor="end"))
    b.append(text(xb + wb + 48, 130, "javi", size=15, color=MUTED))
    return svg_doc(w, h, "\n".join(b), "Modulo de prueba del registro SISO")


# ------------------------------------------------- selector serie/paralelo
def fig_selector():
    w, h = 470, 220
    b = []
    g1, i1, o1 = gate("and", 150, 26, h=44)
    g2, i2, o2 = gate("and", 150, 116, h=44)
    g3, i3, o3 = gate("nor", 245, 68, h=50)
    b += [g1, g2, g3]
    b.append(wire((40, i1[0][1]), i1[0]))
    b.append(text(32, i1[0][1] + 6, subc("I", "p", size=16), size=16, anchor="end"))
    b.append(wire((40, i2[0][1]), i2[0]))
    b.append(label_in(32, i2[0][1], f"S/{over('P')}"))
    xs = 100
    b.append(dot(xs, i2[0][1]))
    gn, inn, onn = not_up(xs, 110, h=24)
    b.append(gn)
    b.append(wire((xs, i2[0][1]), inn))
    b.append(wire(onn, (xs, i1[1][1]), i1[1]))
    b.append(wire((120, 192), (120, i2[1][1]), i2[1]))
    b.append(text(120, 210, subc("I", "s", size=16), size=16, anchor="middle"))
    b.append(wire(o1, (222, o1[1]), (222, i3[0][1]), i3[0]))
    b.append(wire(o2, (232, o2[1]), (232, i3[1][1]), i3[1]))
    # Salidas Q y Q negada
    xq = 345
    gq, iq, oq = gate("not", 362, o3[1] - 11, h=22, n_in=1)
    b.append(gq)
    b.append(wire(o3, iq[0])); b.append(dot(xq, o3[1]))
    b.append(wire((xq, o3[1]), (xq, 40)))
    b.append(label_out(xq, 26, "Q", anchor="middle"))
    b.append(wire(oq, (425, oq[1])))
    b.append(label_out(433, oq[1], over("Q")))
    return svg_doc(w, h, "\n".join(b), "Modulo selector serie/paralelo")


# ------------------------------------------------------------ registro SIPO
def fig_sipo():
    w, h = 800, 290
    b = []
    xs = [170 + i * 160 for i in range(4)]
    y_lab, y_clr, y_ff, y_clk = 22, 64, 110, 264
    pins = []
    for x in xs:
        svg, p = ff(x, y_ff, 80, 104, left=[("D", 0.3)], right=[("Q", 0.3)], clk=0.68, clr=True)
        b.append(svg)
        pins.append(p)
    # CLR
    b.append(wire((50, y_clr), (pins[-1]["CLR"][0], y_clr), pins[-1]["CLR"]))
    b.append(label_in(42, y_clr, over("CLR")))
    for p in pins[:-1]:
        b.append(wire((p["CLR"][0], y_clr), p["CLR"]))
        b.append(dot(p["CLR"][0], y_clr))
    # Entrada: AND de E e I
    yd = pins[0]["D"][1]
    ga, ia, oa = gate("and", 82, yd - 21, h=42)
    b.append(ga)
    b.append(wire(oa, pins[0]["D"]))
    b.append(wire((50, ia[0][1]), ia[0])); b.append(label_in(42, ia[0][1], "E"))
    b.append(wire((50, ia[1][1]), ia[1])); b.append(label_in(42, ia[1][1], "I"))
    # Datos y salidas paralelo
    for k, (a, c) in enumerate(zip(pins, pins[1:])):
        b.append(wire(a["Q"], c["D"]))
        xt = a["Q"][0] + 14
        b.append(wire((xt, a["Q"][1]), (xt, y_lab + 10)))
        b.append(dot(xt, a["Q"][1]))
        b.append(label_out(xt, y_lab - 6, subc("O", 3 - k, size=16), anchor="middle"))
    xt = pins[-1]["Q"][0] + 14
    b.append(wire(pins[-1]["Q"], (xt, pins[-1]["Q"][1]), (xt, y_lab + 10)))
    b.append(label_out(xt, y_lab - 6, subc("O", 0, size=16), anchor="middle"))
    # Reloj
    risers = [p["C"][0] - 12 for p in pins]
    b.append(wire((50, y_clk), (risers[-1], y_clk), (risers[-1], pins[-1]["C"][1]), pins[-1]["C"]))
    b.append(label_in(42, y_clk, "C"))
    for xr, p in zip(risers[:-1], pins[:-1]):
        b.append(wire((xr, y_clk), (xr, p["C"][1]), p["C"]))
        b.append(dot(xr, y_clk))
    return svg_doc(w, h, "\n".join(b), "Registro SIPO de cuatro bits con biestables D")


# ----------------------------------------------------------- registro PISISO
def fig_pisiso():
    w, h = 930, 530
    b = []
    pitch = 210
    y_lab, y_sp, y_ser, y_and = 22, 62, 88, 112
    y_or, y_clr, y_ff, y_clk = 176, 252, 278, 420
    ff_pins = []
    for i in range(4):
        ox = 80 + i * pitch
        # Puertas AND (serie a la izquierda, paralelo a la derecha)
        g1, in1, out1 = vgate("and", ox - 9, y_and, 36)
        g2, in2, out2 = vgate("and", ox + 62, y_and, 36)
        go, ino, outo = vgate("nor", ox - 1, y_or, 40)
        b += [g1, g2, go]
        # S/P negada: rama a la AND serie y, invertida, a la AND paralelo
        xs = in1[1][0]
        y_br = 80
        b.append(wire((xs, y_sp), in1[1])); b.append(dot(xs, y_br))
        if i < 3:
            b.append(dot(xs, y_sp))
        gn, inn, outn = gate("not", ox + 30, y_br - 11, h=22, n_in=1)
        b.append(gn)
        b.append(wire((xs, y_br), inn[0]))
        b.append(wire(outn, (in2[0][0], y_br), in2[0]))
        # Entrada paralelo I_k desde arriba
        b.append(wire((in2[1][0], y_lab + 10), in2[1]))
        b.append(text(in2[1][0], y_lab, subc("I", 3 - i, size=16), size=16, anchor="middle"))
        # AND -> NOR
        b.append(wire(out1, ino[0]))
        b.append(wire(out2, (out2[0], out2[1] + 12), (ino[1][0], out2[1] + 12), ino[1]))
        # Biestable RS
        svg, p = ff(ox + 60, y_ff, 80, 110, left=[("R", 0.2), ("S", 0.8)], right=[("Q", 0.2)], clk=0.5, clr=True)
        b.append(svg)
        ff_pins.append(p)
        xr = outo[0]
        b.append(wire(outo, (xr, p["R"][1]), p["R"])); b.append(dot(xr, p["R"][1]))
        gv, inv, outv = vgate("not", xr - 11, p["R"][1] + 12, 22, n_in=1)
        b.append(gv)
        b.append(wire((xr, p["R"][1]), inv[0]))
        b.append(wire(outv, (xr, p["S"][1]), p["S"]))
        # Q -> entrada serie de la etapa siguiente (o salida O)
        if i < 3:
            nx = 80 + (i + 1) * pitch
            b.append(wire(p["Q"], (p["Q"][0] + 15, p["Q"][1]), (p["Q"][0] + 15, y_ser), (nx, y_ser), (nx, in1[0][1])))
        else:
            b.append(wire(p["Q"], (p["Q"][0] + 20, p["Q"][1])))
            b.append(label_out(p["Q"][0] + 28, p["Q"][1], "O"))
        if i == 0:
            b.append(wire((50, y_ser), (ox, y_ser), in1[0]))
            b.append(label_in(42, y_ser, "I"))
        # Reloj
        xc = p["C"][0] - 12
        b.append(wire((xc, y_clk), (xc, p["C"][1]), p["C"]))
        if i < 3:
            b.append(dot(xc, y_clk))
        if i == 0:
            xc0 = xc
        x_last_sp = xs
    # Railes S/P y CLR
    b.append(wire((50, y_sp), (x_last_sp, y_sp)))
    b.append(label_in(42, y_sp, f"S/{over('P')}"))
    b.append(wire((50, y_clr), (ff_pins[-1]["CLR"][0], y_clr), ff_pins[-1]["CLR"]))
    b.append(label_in(42, y_clr, over("CLR")))
    for p in ff_pins[:-1]:
        b.append(wire((p["CLR"][0], y_clr), p["CLR"]))
        b.append(dot(p["CLR"][0], y_clr))
    # Reloj: C AND CE
    x_last = ff_pins[-1]["C"][0] - 12
    b.append(wire((xc0, y_clk), (x_last, y_clk)))
    ga, ia, oa = vgate("and", xc0 - 18, 478, 36, direction="up")
    b.append(ga)
    b.append(wire(oa, (xc0, y_clk)))
    b.append(wire((50, 494), (ia[0][0], 494), ia[0])); b.append(label_in(42, 494, "C"))
    b.append(wire((50, 514), (ia[1][0], 514), ia[1])); b.append(label_in(42, 514, "CE"))
    return svg_doc(w, h, "\n".join(b), "Registro de desplazamiento de cuatro bits con carga paralela")


# ------------------------------------------------- cronogramas tipo GTKwave
def tramos(n, *rangos):
    """Senal de n muestras que vale 1 en los intervalos [a, c) indicados."""
    return [1 if any(a <= k < c for a, c in rangos) else 0 for k in range(n)]


def cronograma(names, vals, unit, t_unit, tick, label_every, suffix, title):
    """Cronograma con el aspecto de GTKwave. Cada muestra dura t_unit unidades de tiempo."""
    n = len(vals[0])
    x0, y0, row = 150, 62, 38
    w = x0 + n * unit + 30
    h = y0 + len(names) * row + 20
    b = [f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="10" fill="{CARD_BG}" '
         f'stroke="{CARD_BORDER}" stroke-width="1.5"/>']
    b.append(text(24, 36, "Signals", size=13, color=MUTED, weight="bold"))
    b.append(text(x0, 36, "Waves", size=13, color=MUTED, weight="bold"))
    for t in range(0, n * t_unit + 1, tick):
        x = x0 + t / t_unit * unit
        b.append(wire((x, y0 - 8), (x, h - 22), color=GRID, width=1))
        if t % label_every == 0:
            b.append(text(x + 3, y0 - 12, f"{t} {suffix}" if t else "0", size=11, color=MUTED))
    for k, (name, v) in enumerate(zip(names, vals)):
        yb = y0 + (k + 1) * row - 8
        b.append(text(x0 - 16, yb - 7, name, size=14, anchor="end"))
        b.append(wave(x0, yb, v, unit, amp=22, color=C_WAVE))
    return svg_doc(w, h, "\n".join(b), title)


def fig_cronograma():
    n = 37                      # franjas de 5 ns: de 0 a 185 ns
    vals = [
        [k % 2 for k in range(n)],
        [0 if k < 4 else 1 for k in range(n)],
        tramos(n, (8, 12), (16, 24), (28, 32), (36, 37)),
        tramos(n, (9, 13), (17, 25), (29, 33)),
        tramos(n, (11, 15), (19, 27), (31, 35)),
        tramos(n, (13, 17), (21, 29), (33, 37)),
        tramos(n, (15, 19), (23, 31), (35, 37)),
    ]
    return cronograma(["C", "nCLEAR", "I", "w01", "w12", "w23", "O"], vals, 18, 5, 10, 50, "ns",
                      "Cronograma de las senales del registro SISO visto con GTKwave")


SISO_NAMES = ["nCLR", "C", "I", "C1", "C2", "C3", "O"]


def reloj7(n):
    """Reloj que empieza en 1 y cambia cada 7 unidades de tiempo."""
    return [1 - (k // 7) % 2 for k in range(n)]


def fig_crono_sol(caso):
    """Cronogramas de la solucion del SISO: 1 = erroneo, 2 = con retardo, 3 = entrada cada 14."""
    if caso in (1, 2):
        n = 72
        i = tramos(n, (0, 12), (19, 26), (33, 54))
        if caso == 1:   # propagacion instantanea: la senal salta varios biestables de golpe
            c1, c2, c3, o = tramos(n, (7, 63)), tramos(n, (21, n)), tramos(n, (21, n)), tramos(n, (21, n))
            title = "Cronograma erroneo del registro SISO"
        else:           # retardo de una unidad en cada biestable
            c1, c2, c3, o = tramos(n, (8, 64)), tramos(n, (22, n)), tramos(n, (36, n)), tramos(n, (50, n))
            title = "Cronograma del registro SISO con retardo en los biestables"
        vals = [tramos(n, (5, n)), reloj7(n), i, c1, c2, c3, o]
        return cronograma(SISO_NAMES, vals, 9, 1, 10, 10, "s", title)
    n = 139
    vals = [
        tramos(n, (12, n)), reloj7(n),
        tramos(n, (0, 26), (40, 54), (68, 110)),
        tramos(n, (22, 36), (50, 64), (78, 120)),
        tramos(n, (36, 50), (64, 78), (92, 134)),
        tramos(n, (50, 64), (78, 92), (106, n)),
        tramos(n, (64, 78), (92, 106), (120, n)),
    ]
    return cronograma(SISO_NAMES, vals, 5, 1, 10, 50, "s",
                      "Cronograma del registro SISO con la entrada cambiando cada 14 unidades")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "d.svg": fig_d(),
        "dnivel.svg": fig_d_nivel(),
        "dbajo.svg": fig_d_nivel(low=True),
        "dbajo_nombres.svg": fig_d_nivel(low=True, names=True),
        "det_or.svg": fig_detector("or"),
        "ddownedge.svg": fig_ddownedge(),
        "siso.svg": fig_siso(),
        "siso_nombres.svg": fig_siso(named=True),
        "siso_prueba.svg": fig_siso_prueba(),
        "selector.svg": fig_selector(),
        "sipo.svg": fig_sipo(),
        "pisiso.svg": fig_pisiso(),
        "cronograma_siso.svg": fig_cronograma(),
        "sol_siso_1.svg": fig_crono_sol(1),
        "sol_siso_2.svg": fig_crono_sol(2),
        "sol_siso_3.svg": fig_crono_sol(3),
    }
    for name, content in files.items():
        (OUT_DIR / name).write_text(content, encoding="utf-8")
        print("ok", name)


if __name__ == "__main__":
    main()
