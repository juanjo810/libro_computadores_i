"""Genera las figuras SVG de la sesion 5 (encaminadores y sumadores).

Uso (desde la raiz del proyecto):
    python diagram_sources/verilog/sesion_05_figuras.py

Reutiliza el estilo de sesion_03_figuras.py y sesion_04_figuras.py y escribe
los SVG en book/_static/verilog/sesion_05/svg/.
"""

from pathlib import Path

from sesion_03_figuras import (
    ACCENT,
    ACCENT_BG,
    CARD_BG,
    CARD_BORDER,
    GATE_FILL,
    GRID,
    HEAD_BG,
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
from sesion_04_figuras import dashed_box, sub

OUT_DIR = Path(__file__).resolve().parents[2] / "book" / "_static" / "verilog" / "sesion_05" / "svg"

C_X = "#C2410C"
C_Z = "#7C3AED"
VALUE_STYLE = {
    "0": (MUTED, None),
    "1": (ACCENT, ACCENT_BG),
    "x": (C_X, "#FDE7DA"),
    "z": (C_Z, "#EDE4FD"),
}
ARROW_R = "→"


# --------------------------------------------------------------- utilidades
def subc(base, idx, size=15):
    """Contenido con subindice para usar dentro de text()."""
    return f'{base}<tspan baseline-shift="sub" font-size="{size - 4}">{idx}</tspan>'


def tri_buf(x, y, h, direction="right", ctrl_bubble=False):
    """Bufer triestado. Devuelve (svg, entrada, salida, punto_de_control)."""
    if direction == "right":
        pts = f"M{x},{y + 0.06 * h} L{x + 0.9 * h},{y + 0.5 * h} L{x},{y + 0.94 * h} Z"
        inp, out = (x, y + 0.5 * h), (x + 0.9 * h, y + 0.5 * h)
    else:
        pts = f"M{x + 0.9 * h},{y + 0.06 * h} L{x},{y + 0.5 * h} L{x + 0.9 * h},{y + 0.94 * h} Z"
        inp, out = (x + 0.9 * h, y + 0.5 * h), (x, y + 0.5 * h)
    cx, cy = x + 0.45 * h, y + 0.28 * h
    parts = [f'<path d="{pts}" fill="{GATE_FILL}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>']
    if ctrl_bubble:
        r = 0.1 * h
        parts.append(f'<circle cx="{cx}" cy="{cy - r}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
        cy -= 2 * r
    return "\n".join(parts), inp, out, (round(cx, 1), round(cy, 1))


def bubble_in(pin, r=4.5):
    """Circulo de negacion en una entrada; devuelve (svg, nuevo extremo del cable)."""
    px, py = pin
    return (f'<circle cx="{px - r}" cy="{py}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>',
            (px - 2 * r, py))


def not_up(x, ybase, h=26):
    """Inversor vertical apuntando hacia arriba. Devuelve (svg, entrada, salida)."""
    r = 0.15 * h
    tip = ybase - 0.9 * h
    svg = (f'<path d="M{x - 0.44 * h},{ybase} L{x},{tip} L{x + 0.44 * h},{ybase} Z" fill="{GATE_FILL}" '
           f'stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
           f'<circle cx="{x}" cy="{tip - r}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
    return svg, (x, ybase), (x, tip - 2 * r)


def block(x, y, w, h, title=None, idx=None, size=18):
    b = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{GATE_FILL}" stroke="{INK}" stroke-width="2"/>']
    if title and idx is not None:
        b.append(sub(title, idx, x=x + w / 2, y=y + h / 2 + 6, size=size, anchor="middle", weight="bold", family=SANS))
    elif title:
        lines = title.split("\n")
        for i, line in enumerate(lines):
            b.append(text(x + w / 2, y + 30 + i * 22, line, size=size, anchor="middle", weight="bold", family=SANS))
    return "\n".join(b)


def pin_label(x, y, content, anchor="start", size=12):
    return text(x, y, content, size=size, color=MUTED, anchor=anchor)


def reg_box(x, y, label, w=46):
    return (f'<rect x="{x}" y="{y - 13}" width="{w}" height="26" rx="6" fill="{CARD_BG}" stroke="{GRID}" '
            f'stroke-width="1.5"/>' + text(x + w / 2, y + 5, label, size=14, anchor="middle"))


# ------------------------------------------------- fichas de los buferes
def table_card(width, height, title, verilog, symbol_svg, cols, rows, extra=""):
    row_h, head_h = 26, 28
    table_h = head_h + row_h * len(rows)
    body = [
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="12" fill="{CARD_BG}" '
        f'stroke="{CARD_BORDER}" stroke-width="2"/>',
        text(22, 36, title, size=17, weight="bold", family=SANS),
        text(22, 56, verilog, size=12, color=MUTED),
        symbol_svg,
    ]
    col_w = [40] * (len(cols) - 1) + [52]
    tw = sum(col_w)
    tx = width - tw - 22
    ty = (height - table_h) / 2
    body.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{table_h}" rx="8" fill="#FFFFFF" '
                f'stroke="{GRID}" stroke-width="1.5"/>')
    body.append(f'<path d="M{tx},{ty + head_h} V{ty + 8} Q{tx},{ty} {tx + 8},{ty} H{tx + tw - 8} '
                f'Q{tx + tw},{ty} {tx + tw},{ty + 8} V{ty + head_h} Z" fill="{HEAD_BG}"/>')
    sep_x = tx + sum(col_w[:-1])
    body.append(wire((sep_x, ty), (sep_x, ty + table_h), color=GRID, width=1.5))
    body.append(wire((tx, ty + head_h), (tx + tw, ty + head_h), color=GRID, width=1.5))
    cx = tx
    for c, w in zip(cols, col_w):
        body.append(text(cx + w / 2, ty + 19, c, size=12, color=MUTED, anchor="middle", weight="bold"))
        cx += w
    for i, r in enumerate(rows):
        yv = ty + head_h + i * row_h
        if i:
            body.append(wire((tx + 6, yv), (tx + tw - 6, yv), color="#E2E8F0", width=1))
        cx = tx
        for k, (v, w) in enumerate(zip(r, col_w)):
            color, bg = VALUE_STYLE[v]
            mid = cx + w / 2
            if bg:
                body.append(f'<rect x="{mid - 12}" y="{yv + 4}" width="24" height="{row_h - 8}" rx="5" fill="{bg}"/>')
            body.append(text(mid, yv + 18, v, size=14, color=color, anchor="middle",
                             weight="bold" if bg else "normal"))
            cx += w
    body.append(extra)
    return svg_doc(width, height, "\n".join(body), title)


def bufif_card(active_high=True):
    w, h = 470, 168
    g, inp, out, ctrl = tri_buf(120, 96, 56, ctrl_bubble=not active_high)
    ctrl_name = "G" if active_high else over("G")
    sym = [g,
           wire((50, inp[1]), inp), text(36, inp[1] + 5, "A", size=15, anchor="middle"),
           wire(ctrl, (ctrl[0], ctrl[1] - 22), (ctrl[0] - 26, ctrl[1] - 22)),
           text(ctrl[0] - 34, ctrl[1] - 17, ctrl_name, size=15, anchor="end"),
           wire(out, (out[0] + 40, out[1])), text(out[0] + 48, out[1] + 5, "Y", size=15, color=ACCENT, weight="bold")]
    if active_high:
        rows = [("0", "x", "z"), ("1", "0", "0"), ("1", "1", "1")]
        title, verilog = "bufif1", "bufif1 bIzquierda(Y,A,G);"
    else:
        rows = [("0", "0", "0"), ("0", "1", "1"), ("1", "x", "z")]
        title, verilog = "bufif0", "bufif0 bDerecha(Y,A,G);"
    return table_card(w, h, title, verilog, "\n".join(sym), [ctrl_name, "A", "Y"], rows)


# --------------------------------------------------------- transceptor
def fig_transceiver(mode="teoria"):
    """mode: 'teoria' (figura de clase), 'nombres' (nombres del modulo) o 'test' (modulo de prueba)."""
    test = mode == "test"
    named = mode in ("nombres", "test")
    ox = 90 if test else 60
    w, h = (730 if test else 640), 320
    b = [dashed_box(ox + 70, 20, 400, 280)]
    gh = 44
    xg = ox + 210
    g2, i2, o2 = gate("and", xg, 40, h=gh)    # sa2 = ng.ndir (controla B -> A)
    g1, i1, o1 = gate("and", xg, 110, h=gh)   # sa1 = ng.dir  (controla A -> B)
    b += [g1, g2]
    yg, yd = i2[0][1], i1[1][1]
    xin = ox + 20
    # Entrada G (negada en las dos AND)
    bub, end = bubble_in(i2[0]); b.append(bub); b.append(wire((xin, yg), end))
    bub, end = bubble_in(i1[0]); b.append(bub)
    xjg = ox + 160
    b.append(wire((xjg, yg), (xjg, i1[0][1]), end)); b.append(dot(xjg, yg))
    # Entrada DIR (directa en sa1, negada en sa2)
    b.append(wire((xin, yd), i1[1]))
    bub, end = bubble_in(i2[1]); b.append(bub)
    xjd = ox + 180
    b.append(wire((xjd, yd), (xjd, i2[1][1]), end)); b.append(dot(xjd, yd))
    # Buferes triestado
    ya = 262
    yb = 200
    tb_ab, in_ab, out_ab, c_ab = tri_buf(ox + 300, ya - 15, 30)
    tb_ba, in_ba, out_ba, c_ba = tri_buf(ox + 350, yb - 15, 30, direction="left")
    b += [tb_ab, tb_ba]
    xa_node, xb_node = ox + 240, ox + 430
    b.append(wire((xin, ya), in_ab)); b.append(dot(xa_node, ya))
    b.append(wire(out_ab, (xb_node, ya), (xb_node, yb)))
    b.append(wire((xb_node, yb), in_ba))
    b.append(wire((xb_node, yb), (ox + 560, yb))); b.append(dot(xb_node, yb))
    b.append(wire(out_ba, (xa_node, yb), (xa_node, ya)))
    # Senales de control
    xs1 = ox + 280
    b.append(wire(o1, (xs1, o1[1]), (xs1, ya - 40), (c_ab[0], ya - 40), c_ab))
    b.append(wire(o2, (c_ba[0], o2[1]), c_ba))

    if mode == "teoria":
        for yv, lab in ((yg, over("G")), (yd, "DIR"), (ya, "A")):
            b.append(text(xin - 8, yv + 5, lab, size=15, anchor="end"))
        b.append(text(ox + 568, yb + 5, "B", size=15))
    else:
        lab = dict(size=13, color=ACCENT, weight="bold")
        b.append(text(ox + 76, yg - 7, "g", **lab))
        b.append(text(ox + 76, yd - 7, "dir", **lab))
        b.append(text(ox + 76, ya - 7, "a", **lab))
        b.append(text(ox + 520, yb - 7, "b", **lab))
        b.append(text(o1[0] + 6, o1[1] + 18, "sa1", size=13, color=MUTED, weight="bold"))
        b.append(text(o2[0] + 6, o2[1] - 8, "sa2", size=13, color=MUTED, weight="bold"))
    if test:
        for yv, lab in ((yg, "g"), (yd, "dir"), (ya, "ra")):
            b.append(reg_box(xin - 62, yv, lab))
        b.append(wire((ox + 560, yb), (ox + 575, yb)))
        b.append(reg_box(ox + 575, yb, "rb"))
    titles = {"teoria": "Transmisor/receptor de bus de un bit",
              "nombres": "Transceptor con los nombres usados en Verilog",
              "test": "Transceptor conectado al modulo de prueba"}
    return svg_doc(w, h, "\n".join(b), titles[mode])


# ------------------------------------------------------ multiplexor 8x1
def fig_mux8x1():
    w, h = 600, 500
    b = [dashed_box(70, 15, 450, 432)]
    m1x, m1y, m2x, m2y = 120, 30, 290, 210
    mw, mh = 120, 150
    b.append(block(m1x, m1y, mw, mh, "MUX\n4x1"))
    b.append(block(m2x, m2y, mw, mh, "MUX\n4x1"))
    for i in range(4):
        y1 = m1y + 30 + 30 * i
        y2 = m2y + 30 + 30 * i
        b.append(wire((30, y1), (m1x, y1)))
        b.append(wire((30, y2), (m2x, y2)))
        b.append(sub("D", i, x=22, y=y1 + 5, anchor="end"))
        b.append(sub("D", i + 4, x=22, y=y2 + 5, anchor="end"))
        b.append(sub("D", i, x=m1x + 6, y=y1 - 4, size=12, color=MUTED))
        b.append(sub("D", i, x=m2x + 6, y=y2 - 4, size=12, color=MUTED))
    # Salidas Y unidas
    y1o, y2o = m1y + 80, m2y + 80
    xj = 480
    b.append(wire((m1x + mw, y1o), (560, y1o)))
    b.append(wire((m2x + mw, y2o), (xj, y2o), (xj, y1o))); b.append(dot(xj, y1o))
    b.append(text(568, y1o + 5, "Y", size=16, weight="bold", color=ACCENT))
    b.append(pin_label(m1x + mw - 6, y1o - 6, "Y", anchor="end"))
    b.append(pin_label(m2x + mw - 6, y2o - 6, "Y", anchor="end"))
    # Patillas de control
    bottom1, bottom2 = m1y + mh, m2y + mh
    xs = [m1x + 25, m1x + 60, m1x + 95]
    xs2 = [m2x + 25, m2x + 60, m2x + 95]
    for x, lab in zip(xs, ("OE", "S1", "S0")):
        b.append(pin_label(x, bottom1 - 8, lab if lab == "OE" else subc(lab[0], lab[1], size=12), anchor="middle"))
    for x, lab in zip(xs2, ("OE", "S1", "S0")):
        b.append(pin_label(x, bottom2 - 8, lab if lab == "OE" else subc(lab[0], lab[1], size=12), anchor="middle"))
    ybot = 465
    # S2: invertida a OE del primero, directa a OE del segundo
    gnot, n_in, n_out = not_up(xs[0], 400, h=26)
    b.append(gnot)
    b.append(wire(n_out, (xs[0], bottom1)))
    b.append(wire((xs[0], ybot), n_in))
    b.append(wire((xs[0], 412), (xs2[0], 412), (xs2[0], bottom2))); b.append(dot(xs[0], 412))
    # S1 y S0 a los dos multiplexores
    for k, yb in ((1, 424), (2, 436)):
        b.append(wire((xs[k], ybot), (xs[k], bottom1)))
        b.append(wire((xs[k], yb), (xs2[k], yb), (xs2[k], bottom2))); b.append(dot(xs[k], yb))
    for x, idx in zip(xs, (2, 1, 0)):
        b.append(sub("S", idx, x=x, y=ybot + 22, anchor="middle"))
    return svg_doc(w, h, "\n".join(b), "Multiplexor 8x1 a partir de dos multiplexores 4x1 con OE")


# ---------------------------------------------------------- sumadores
def ha_block(x, y, w=90, h=110, idx=None, terminals=True):
    b = [block(x, y, w, h, "HA", idx)]
    ye1, ye2 = y + 0.3 * h, y + 0.7 * h
    b.append(pin_label(x + 6, ye1 - 5, subc("e", 1, size=12)))
    b.append(pin_label(x + 6, ye2 - 5, subc("e", 2, size=12)))
    b.append(pin_label(x + w - 6, ye1 - 5, "s", anchor="end"))
    b.append(pin_label(x + w - 6, ye2 - 5, subc("c", "o", size=12), anchor="end"))
    pins = {"e1": (x, ye1), "e2": (x, ye2), "s": (x + w, ye1), "co": (x + w, ye2)}
    return "\n".join(b), pins


def fig_semisuma():
    w, h = 600, 170
    b = []
    hb, p = ha_block(70, 30, w=100, h=110)
    b.append(hb)
    for k, lab, side in (("e1", subc("e", 1), "in"), ("e2", subc("e", 2), "in"), ("s", "s", "out"), ("co", subc("c", "o"), "out")):
        x, y = p[k]
        if side == "in":
            b.append(wire((x - 30, y), (x, y))); b.append(dot(x - 30, y))
            b.append(text(x - 38, y + 5, lab, size=15, anchor="end"))
        else:
            b.append(wire((x, y), (x + 30, y))); b.append(dot(x + 30, y))
            b.append(text(x + 38, y + 5, lab, size=15))
    # Interior
    b.append(dashed_box(330, 20, 170, 130))
    gx, ix, ox_ = gate("xor", 410, 26, h=44)
    ga, ia, oa = gate("and", 410, 92, h=44)
    b += [gx, ga]
    ye1, ye2 = ix[0][1], ix[1][1]
    b.append(wire((300, ye1), ix[0])); b.append(text(292, ye1 + 5, subc("e", 1), size=15, anchor="end"))
    b.append(wire((300, ye2), ix[1])); b.append(text(292, ye2 + 5, subc("e", 2), size=15, anchor="end"))
    b.append(wire((380, ye1), (380, ia[0][1]), ia[0])); b.append(dot(380, ye1))
    b.append(wire((360, ye2), (360, ia[1][1]), ia[1])); b.append(dot(360, ye2))
    b.append(wire(ox_, (540, ox_[1]))); b.append(text(548, ox_[1] + 5, "s", size=15, color=ACCENT, weight="bold"))
    b.append(wire(oa, (540, oa[1]))); b.append(text(548, oa[1] + 5, "c", size=15, color=ACCENT, weight="bold"))
    return svg_doc(w, h, "\n".join(b), "Semisumador: bloque e interior")


def fig_sumador1():
    w, h = 560, 210
    b = [dashed_box(70, 15, 400, 180)]
    h1, p1 = ha_block(130, 75, idx=1)
    h2, p2 = ha_block(290, 25, idx=2)
    b += [h1, h2]
    yci = p2["e1"][1]
    b.append(wire((30, yci), p2["e1"])); b.append(text(22, yci + 5, subc("c", "i"), size=16, anchor="end"))
    for k, lab in (("e1", subc("e", 1)), ("e2", subc("e", 2))):
        x, y = p1[k]
        b.append(wire((30, y), (x, y))); b.append(text(22, y + 5, lab, size=16, anchor="end"))
    b.append(wire(p1["s"], (260, p1["s"][1]), (260, p2["e2"][1]), p2["e2"]))
    b.append(wire(p2["s"], (510, p2["s"][1]))); b.append(text(518, p2["s"][1] + 5, "s", size=16, color=ACCENT, weight="bold"))
    go, io, oo = gate("or", 410, 130, h=40)
    b.append(go)
    b.append(wire(p2["co"], (395, p2["co"][1]), (395, io[0][1]), io[0]))
    b.append(wire(p1["co"], (380, p1["co"][1]), (380, io[1][1]), io[1]))
    b.append(wire(oo, (510, oo[1]))); b.append(text(518, oo[1] + 5, subc("c", "o", size=16), size=16, color=ACCENT, weight="bold"))
    return svg_doc(w, h, "\n".join(b), "Sumador completo a partir de dos semisumadores")


def fig_propaga4():
    w, h = 700, 250
    b = [dashed_box(20, 60, 660, 140)]
    bw, bh, top, step = 110, 80, 85, 165
    xs = {i: 30 + (3 - i) * step for i in range(4)}
    for i, x0 in xs.items():
        b.append(block(x0, top, bw, bh, "FA", i, size=16))
        for dx, name in ((20, ("e", 1)), (45, ("e", 2)), (80, ("c", "i"))):
            b.append(pin_label(x0 + dx, top + 16, subc(name[0], name[1], size=11), anchor="middle", size=11))
        b.append(pin_label(x0 + 25, top + bh - 6, subc("c", "o", size=11), anchor="middle", size=11))
        b.append(pin_label(x0 + 70, top + bh - 6, "s", anchor="middle", size=11))
        # Entradas e1_i, e2_i
        b.append(wire((x0 + 20, 35), (x0 + 20, top)))
        b.append(wire((x0 + 45, 35), (x0 + 45, top)))
        b.append(text(x0 + 32, 26, f'e1<tspan baseline-shift="sub" font-size="10">{i}</tspan> '
                                    f'e2<tspan baseline-shift="sub" font-size="10">{i}</tspan>',
                      size=14, anchor="middle"))
        # Salida s_i
        b.append(wire((x0 + 70, top + bh), (x0 + 70, 225)))
        b.append(sub("s", i, x=x0 + 70, y=243, size=15, anchor="middle"))
        # Acarreo hacia el siguiente bloque (a la izquierda)
        if i < 3:
            xg = x0 - 30
            b.append(wire((x0 + 25, top + bh), (x0 + 25, top + bh + 18), (xg, top + bh + 18), (xg, top - 14),
                          (x0 - step + 80, top - 14), (x0 - step + 80, top)))
    # c_i de entrada y c_o final
    b.append(wire((xs[0] + 80, 35), (xs[0] + 80, top)))
    b.append(sub("c", "i", x=xs[0] + 80, y=26, size=15, anchor="middle"))
    b.append(wire((xs[3] + 25, top + bh), (xs[3] + 25, 225)))
    b.append(sub("c", "o", x=xs[3] + 25, y=243, size=15, anchor="middle"))
    return svg_doc(w, h, "\n".join(b), "Sumador de cuatro bits con propagacion de acarreo")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "bufif1.svg": bufif_card(active_high=True),
        "bufif0.svg": bufif_card(active_high=False),
        "trans.svg": fig_transceiver("teoria"),
        "trans_nombres.svg": fig_transceiver("nombres"),
        "trans_test.svg": fig_transceiver("test"),
        "mux8x1.svg": fig_mux8x1(),
        "semisuma.svg": fig_semisuma(),
        "sumador1.svg": fig_sumador1(),
        "propaga4.svg": fig_propaga4(),
    }
    for name, content in files.items():
        (OUT_DIR / name).write_text(content, encoding="utf-8")
        print("ok", name)


if __name__ == "__main__":
    main()
