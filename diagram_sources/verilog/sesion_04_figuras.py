"""Genera las figuras SVG de la sesion 4 (modulos).

Uso (desde la raiz del proyecto):
    python diagram_sources/verilog/sesion_04_figuras.py

Reutiliza el estilo y las puertas de sesion_03_figuras.py y escribe los SVG en
book/_static/verilog/sesion_04/svg/.
"""

from pathlib import Path

from sesion_03_figuras import (
    ACCENT,
    CARD_BG,
    GRID,
    INK,
    MUTED,
    SANS,
    arrow,
    dot,
    gate,
    over,
    svg_doc,
    text,
    wire,
)

OUT_DIR = Path(__file__).resolve().parents[2] / "book" / "_static" / "verilog" / "sesion_04" / "svg"

C_INPUT = "#C2410C"
C_OUTPUT = ACCENT
C_INOUT = "#7C3AED"
C_GATE = "#2563EB"
C_REG = "#B45309"
C_WIRE = MUTED

O_ACUTE = "Ó"
APPROX = "≃"


def sub(base, idx, size=15, **kw):
    return text(content=f'{base}<tspan baseline-shift="sub" font-size="{size - 4}">{idx}</tspan>', size=size, **kw)


def dashed_box(x, y, w, h):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="none" stroke="{MUTED}" '
        f'stroke-width="1.6" stroke-dasharray="7 5"/>'
    )


def arrow_left(x, y, color=INK):
    return f'<path d="M{x + 9},{y - 5} L{x},{y} L{x + 9},{y + 5} Z" fill="{color}"/>'


def arrow_up(x, y, color=INK):
    return f'<path d="M{x - 5},{y + 9} L{x},{y} L{x + 5},{y + 9} Z" fill="{color}"/>'


def arrow_down(x, y, color=INK):
    return f'<path d="M{x - 5},{y - 9} L{x},{y} L{x + 5},{y - 9} Z" fill="{color}"/>'


# ------------------------------------------------------- reglas de los puertos
def fig_modulo():
    w, h = 640, 330
    b = []
    bx, by, bw, bh = 170, 100, 300, 200
    b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="{CARD_BG}" '
             f'stroke="{MUTED}" stroke-width="1.8" stroke-dasharray="8 6"/>')
    b.append(text(bx + bw / 2, by + bh - 18, f"M{O_ACUTE}DULO", size=20, color=MUTED,
                  anchor="middle", weight="bold", family=SANS))
    # input (izquierda)
    y = 210
    b.append(wire((50, y), (bx, y), color=C_INPUT, width=2.5))
    b.append(wire((bx, y), (bx + 70, y), color=C_INPUT, width=2.5))
    b.append(arrow(bx + 4, y, C_INPUT))
    b.append(arrow(bx + 78, y, C_INPUT))
    b.append(text(50, y - 26, "reg", size=15))
    b.append(text(50, y + 26, "wire", size=15))
    b.append(text(bx - 8, y - 10, "input", size=14, color=C_INPUT, anchor="end", weight="bold"))
    b.append(text(bx + 86, y + 5, "wire", size=15))
    # output (derecha)
    xr = bx + bw
    b.append(wire((xr - 70, y), (xr, y), color=C_OUTPUT, width=2.5))
    b.append(wire((xr, y), (xr + 80, y), color=C_OUTPUT, width=2.5))
    b.append(arrow(xr + 4, y, C_OUTPUT))
    b.append(arrow(xr + 88, y, C_OUTPUT))
    b.append(text(xr - 76, y - 26, "reg", size=15))
    b.append(text(xr - 76, y + 26, "wire", size=15))
    b.append(text(xr + 8, y - 10, "output", size=14, color=C_OUTPUT, weight="bold"))
    b.append(text(xr + 96, y + 5, "wire", size=15))
    # inout (arriba)
    xm = bx + bw / 2
    b.append(wire((xm, 34), (xm, by + 62), color=C_INOUT, width=2.5))
    b.append(arrow_up(xm, 34, C_INOUT))
    b.append(arrow_down(xm, by - 4, C_INOUT))
    b.append(arrow_up(xm, by + 4, C_INOUT))
    b.append(arrow_down(xm, by + 62, C_INOUT))
    b.append(text(xm, 24, "wire", size=15, anchor="middle"))
    b.append(text(xm + 10, by - 8, "inout", size=14, color=C_INOUT, weight="bold"))
    b.append(text(xm, by + 82, "wire", size=15, anchor="middle"))
    return svg_doc(w, h, "\n".join(b), "Reglas de conexion de los puertos de un modulo")


# --------------------------------------------------- comparador de un bit
def fig_comp1(named=False):
    w, h = 580, 312
    b = [dashed_box(80, 20, 380, 266)]
    gh = 50
    g_up, i_up, o_up = gate("and", 250, 30, h=gh)
    g_dn, i_dn, o_dn = gate("and", 250, 220, h=gh)
    g_n1, i_n1, o_n1 = gate("not", 130, 92, h=28, n_in=1)
    g_n2, i_n2, o_n2 = gate("not", 130, 170, h=28, n_in=1)
    g_nor, i_nor, o_nor = gate("nor", 350, 125, h=gh, label="n" if named else None)
    b += [g_up, g_dn, g_n1, g_n2, g_nor]
    ya, yb = i_up[0][1], i_dn[1][1]
    xr = 105
    # a y b
    b.append(wire((30, ya), i_up[0]))
    b.append(wire((30, yb), i_dn[1]))
    b.append(text(22, ya + 6, "a", size=17, anchor="end"))
    b.append(text(22, yb + 6, "b", size=17, anchor="end"))
    b.append(wire((xr, ya), (xr, i_n1[0][1]), i_n1[0])); b.append(dot(xr, ya))
    b.append(wire((xr, yb), (xr, i_n2[0][1]), i_n2[0])); b.append(dot(xr, yb))
    # salidas de los inversores
    x1, x2 = 222, 202
    b.append(wire(o_n1, (x1, o_n1[1]), (x1, i_dn[0][1]), i_dn[0]))
    b.append(wire(o_n2, (x2, o_n2[1]), (x2, i_up[1][1]), i_up[1]))
    # salidas
    xs = 325
    b.append(wire(o_up, (520, o_up[1])))
    b.append(wire(o_dn, (520, o_dn[1])))
    b.append(wire((xs, o_up[1]), (xs, i_nor[0][1]), i_nor[0])); b.append(dot(xs, o_up[1]))
    b.append(wire((xs, o_dn[1]), (xs, i_nor[1][1]), i_nor[1])); b.append(dot(xs, o_dn[1]))
    b.append(wire(o_nor, (520, o_nor[1])))
    for yv, lab in ((o_up[1], "a&gt;b"), (o_nor[1], "a=b"), (o_dn[1], "a&lt;b")):
        b.append(arrow(520, yv))
        b.append(text(528, yv + 5, lab, size=15, weight="bold"))
    if named:
        lab = dict(size=12, weight="bold")
        b.append(text(275, 13, "aArriba", color=C_GATE, anchor="middle", **lab))
        b.append(text(275, 306, "aAbajo", color=C_GATE, anchor="middle", **lab))
        b.append(text(143, 134, "nArriba", color=C_GATE, anchor="middle", **lab))
        b.append(text(143, 164, "nAbajo", color=C_GATE, anchor="middle", **lab))
        b.append(text(x1 + 6, o_n1[1] - 8, "wArriba", color=C_WIRE, **lab))
        b.append(text(x2 - 6, o_n2[1] + 18, "wAbajo", color=C_WIRE, anchor="end", **lab))
        b.append(text(92, ya - 8, "a", color=ACCENT, **lab))
        b.append(text(92, yb - 8, "b", color=ACCENT, **lab))
        b.append(text(452, o_up[1] - 8, "mayor", color=ACCENT, anchor="end", **lab))
        b.append(text(452, o_nor[1] - 8, "igual", color=ACCENT, anchor="end", **lab))
        b.append(text(452, o_dn[1] - 8, "menor", color=ACCENT, anchor="end", **lab))
    title = "Comparador de un bit con los nombres de Verilog" if named else "Comparador de un bit"
    return svg_doc(w, h, "\n".join(b), title)


# ------------------------------------------------------------- jerarquia
def node(x, y, label, kind, color, highlight=False):
    width = 9 * len(label) + 9 * len(kind) + 40
    fill = "#D9F2EC" if highlight else "#FFFFFF"
    stroke = ACCENT if highlight else GRID
    return (
        f'<rect x="{x}" y="{y - 14}" width="{width}" height="28" rx="14" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{2 if highlight else 1.5}"/>'
        f'<circle cx="{x + 15}" cy="{y}" r="5" fill="{color}"/>'
        + text(x + 27, y + 5, f'{label} <tspan fill="{MUTED}" font-size="12">({kind})</tspan>', size=14,
               weight="bold" if highlight else "normal")
    ), width


def link(x1, y1, x2, y2, color=GRID, width=2):
    xm = (x1 + x2) / 2
    return (f'<path d="M{x1},{y1} C{xm},{y1} {xm},{y2} {x2},{y2}" fill="none" stroke="{color}" '
            f'stroke-width="{width}"/>')


def fig_jerarquia():
    w, h = 680, 400
    b = []
    root_svg, rw = node(20, 200, "TestComp1", "módulo raíz", ACCENT)
    rx = 20 + rw
    kids = [("c", "Comp1", ACCENT), ("a", "reg", C_REG), ("b", "reg", C_REG),
            ("M", "wire", C_WIRE), ("m", "wire", C_WIRE), ("igual", "wire", C_WIRE)]
    kx = 300
    ky = [90, 190, 230, 270, 310, 350]
    for (lab, kind, col), yv in zip(kids, ky):
        hl = lab == "c"
        b.append(link(rx, 200, kx, yv, ACCENT if hl else GRID, 2.5 if hl else 2))
        s, _ = node(kx, yv, lab, kind, col, highlight=hl)
        b.append(s)
    gx = 470
    gkids = [("nArriba", "not", C_GATE), ("nAbajo", "not", C_GATE), ("aArriba", "and", C_GATE),
             ("aAbajo", "and", C_GATE), ("n", "nor", C_GATE), ("wArriba", "wire", C_WIRE),
             ("wAbajo", "wire", C_WIRE)]
    for i, (lab, kind, col) in enumerate(gkids):
        yv = 20 + i * 30 + 10
        hl = lab == "aAbajo"
        b.append(link(kx + 100, 90, gx, yv, ACCENT if hl else GRID, 2.5 if hl else 2))
        s, _ = node(gx, yv, lab, kind, col, highlight=hl)
        b.append(s)
    b.append(root_svg)
    # Ruta c.aAbajo
    b.append(f'<rect x="20" y="335" width="200" height="40" rx="8" fill="#D9F2EC"/>')
    b.append(text(34, 361, f'ruta: <tspan font-weight="bold" fill="{ACCENT}">c.aAbajo</tspan>', size=15))
    return svg_doc(w, h, "\n".join(b), "Jerarquia de modulos de TestComp1")


# --------------------------------------------------- comparador de dos bits
def comp_block(x, y, name, idx):
    b = [f'<rect x="{x}" y="{y}" width="110" height="180" rx="8" fill="#EAF7F3" stroke="{INK}" stroke-width="2"/>',
         sub(name, idx, x=x + 55, y=y + 96, size=17, anchor="middle", weight="bold", family=SANS),
         text(x + 10, y + 46, "a", size=14), text(x + 10, y + 146, "b", size=14),
         text(x + 100, y + 35, "&gt;", size=14, anchor="end"),
         text(x + 100, y + 85, "=", size=14, anchor="end"),
         text(x + 100, y + 135, "&lt;", size=14, anchor="end")]
    return "\n".join(b)


def fig_comp2():
    w, h = 760, 490
    b = [dashed_box(90, 20, 580, 450)]
    b.append(comp_block(140, 40, "COMP", 1))
    b.append(comp_block(140, 270, "COMP", 2))
    for yv, (base, idx) in ((80, ("a", 0)), (180, ("b", 0)), (310, ("a", 1)), (410, ("b", 1))):
        b.append(wire((50, yv), (140, yv)))
        b.append(sub(base, idx, x=42, y=yv + 5, anchor="end"))
    gh = 44
    g_g, i_g, o_g = gate("and", 380, 50, h=gh)
    g_og, i_og, o_og = gate("or", 560, 70, h=gh)
    g_e, i_e, o_e = gate("and", 560, 220, h=gh)
    g_l, i_l, o_l = gate("and", 440, 330, h=gh)
    g_ol, i_ol, o_ol = gate("or", 560, 360, h=gh)
    b += [g_g, g_og, g_e, g_l, g_ol]
    # COMP1 >
    b.append(wire((250, 70), (360, 70), (360, i_g[0][1]), i_g[0]))
    # bus COMP2 =
    xb = 340
    b.append(wire((250, 350), (xb, 350)))
    b.append(wire((xb, 350), (xb, i_g[1][1]), i_g[1]))
    b.append(wire((xb, i_e[1][1]), i_e[1])); b.append(dot(xb, i_e[1][1]))
    b.append(wire((xb, 350), (400, 350), (400, i_l[1][1]), i_l[1])); b.append(dot(xb, 350))
    # COMP1 =
    b.append(wire((250, 120), (520, 120), (520, i_e[0][1]), i_e[0]))
    # COMP1 <
    b.append(wire((250, 170), (420, 170), (420, i_l[0][1]), i_l[0]))
    # OR a>b
    b.append(wire(o_g, (530, o_g[1]), (530, i_og[0][1]), i_og[0]))
    b.append(wire((250, 300), (545, 300), (545, i_og[1][1]), i_og[1]))
    # OR a<b
    b.append(wire(o_l, (530, o_l[1]), (530, i_ol[0][1]), i_ol[0]))
    b.append(wire((250, 400), (545, 400), (545, i_ol[1][1]), i_ol[1]))
    for o, lab in ((o_og, "a&gt;b"), (o_e, "a=b"), (o_ol, "a&lt;b")):
        b.append(wire(o, (700, o[1])))
        b.append(arrow(700, o[1]))
        b.append(text(708, o[1] + 5, lab, size=15, weight="bold"))
    return svg_doc(w, h, "\n".join(b), "Comparador de dos bits a partir de dos comparadores de un bit")


# ------------------------------------------------------------ codificadores
def fig_codificadores():
    w, h = 720, 270
    b = []
    gh = 40

    def inputs(ox, ys, stub_ids):
        out = []
        for i, yv in enumerate(ys):
            end = ox + 70 if i in stub_ids else None
            out.append(sub("D", i, x=ox + 2, y=yv + 5, size=14, anchor="end"))
            if end:
                out.append(wire((ox + 10, yv), (end, yv)))
        return out

    # Codificador normal
    ox = 40
    b.append(text(ox + 140, 26, "Codificador 4x2", size=14, anchor="middle", weight="bold", family=SANS))
    b.append(dashed_box(ox + 40, 40, 200, 190))
    ys = [80, 100, 160, 200]
    b += inputs(ox, ys, stub_ids={3})
    g1, i1, o1 = gate("nor", ox + 120, 70, h=gh)
    g0, i0, o0 = gate("nor", ox + 120, 130, h=gh)
    b += [g1, g0]
    b.append(wire((ox + 10, ys[0]), i1[0]))
    b.append(wire((ox + 10, ys[1]), i1[1]))
    b.append(wire((ox + 90, ys[0]), (ox + 90, i0[0][1]), i0[0])); b.append(dot(ox + 90, ys[0]))
    b.append(wire((ox + 10, ys[2]), (ox + 100, ys[2]), (ox + 100, i0[1][1]), i0[1]))
    for o, idx in ((o1, 1), (o0, 0)):
        b.append(wire(o, (ox + 270, o[1])))
        b.append(sub("a", idx, x=ox + 278, y=o[1] + 5))

    # Codificador con prioridad
    ox = 370
    b.append(text(ox + 150, 26, "Codificador 4x2 con prioridad", size=14, anchor="middle", weight="bold",
                  family=SANS))
    b.append(dashed_box(ox + 40, 40, 250, 210))
    ys = [60, 80, 150, 170]
    b += inputs(ox, ys, stub_ids={0})
    ga, ia, oa = gate("and", ox + 130, 70, h=gh)
    gn, inn, onn = gate("not", ox + 80, 98, h=22, n_in=1)
    g1, i1, o1 = gate("or", ox + 130, 140, h=gh)
    g0, i0, o0 = gate("or", ox + 200, 190, h=gh)
    b += [ga, gn, g1, g0]
    b.append(wire((ox + 10, ys[1]), i_first := ia[0]))
    b.append(wire((ox + 65, ys[2]), (ox + 65, inn[0][1]), inn[0])); b.append(dot(ox + 65, ys[2]))
    b.append(wire(onn, (ox + 115, onn[1]), (ox + 115, ia[1][1]), ia[1]))
    b.append(wire((ox + 10, ys[2]), i1[0]))
    b.append(wire((ox + 10, ys[3]), i1[1]))
    b.append(wire(oa, (ox + 190, oa[1]), (ox + 190, i0[0][1]), i0[0]))
    b.append(wire((ox + 95, ys[3]), (ox + 95, i0[1][1]), i0[1])); b.append(dot(ox + 95, ys[3]))
    for o, idx in ((o1, 1), (o0, 0)):
        b.append(wire(o, (ox + 320, o[1])))
        b.append(sub("a", idx, x=ox + 328, y=o[1] + 5))
    return svg_doc(w, h, "\n".join(b), "Codificador 4x2 y codificador 4x2 con prioridad")


# ------------------------------------------------------ AND de 4 entradas
def fig_and4():
    w, h = 700, 200
    b = []
    g, ins, out = gate("and", 90, 60, h=80, n_in=4)
    b.append(g)
    for i, p in enumerate(ins, start=1):
        b.append(wire((40, p[1]), p))
        b.append(sub("e", i, x=32, y=p[1] + 5, size=14, anchor="end"))
    b.append(wire(out, (out[0] + 40, out[1])))
    b.append(text(out[0] + 48, out[1] + 5, "s", size=16))
    b.append(text(300, out[1] + 9, APPROX, size=28, color=MUTED, anchor="middle"))
    gh = 48
    ga, ia, oa = gate("and", 430, 20, h=gh)
    gb, ib, ob = gate("and", 430, 130, h=gh)
    gc, ic, oc = gate("and", 560, 76, h=gh)
    b += [ga, gb, gc]
    for i, p in enumerate(ia + ib, start=1):
        b.append(wire((385, p[1]), p))
        b.append(sub("e", i, x=377, y=p[1] + 5, size=14, anchor="end"))
    b.append(wire(oa, (530, oa[1]), (530, ic[0][1]), ic[0]))
    b.append(wire(ob, (530, ob[1]), (530, ic[1][1]), ic[1]))
    b.append(wire(oc, (oc[0] + 30, oc[1])))
    b.append(text(oc[0] + 38, oc[1] + 5, "s", size=16))
    return svg_doc(w, h, "\n".join(b), "Puerta AND de cuatro entradas y su equivalente con puertas de dos entradas")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "modulo.svg": fig_modulo(),
        "comp1.svg": fig_comp1(named=False),
        "comp1_nombres.svg": fig_comp1(named=True),
        "jerarquia.svg": fig_jerarquia(),
        "comp2.svg": fig_comp2(),
        "codificadores.svg": fig_codificadores(),
        "and4.svg": fig_and4(),
    }
    for name, content in files.items():
        (OUT_DIR / name).write_text(content, encoding="utf-8")
        print("ok", name)


if __name__ == "__main__":
    main()
