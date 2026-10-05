"""Genera las figuras SVG de la sesion 3 (puertas logicas).

Uso (desde la raiz del proyecto):
    python diagram_sources/verilog/sesion_03_figuras.py

Escribe los SVG en book/_static/verilog/sesion_03/svg/. Los SVG solo usan
trazos y <text> normales (sin foreignObject), por lo que funcionan en HTML y
se convierten sin problemas al exportar el PDF.
"""

from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[2] / "book" / "_static" / "verilog" / "sesion_03" / "svg"

# Paleta (modo claro; en modo oscuro custom.css invierte la imagen)
INK = "#1E293B"
MUTED = "#64748B"
ACCENT = "#00876F"
ACCENT_BG = "#D9F2EC"
GATE_FILL = "#EAF7F3"
CARD_BG = "#F8FAFC"
CARD_BORDER = "#E2E8F0"
HEAD_BG = "#EEF2F7"
GRID = "#CBD5E1"
MONO = "'JetBrains Mono','DejaVu Sans Mono',Consolas,Menlo,monospace"
SANS = "Inter,'Segoe UI','DejaVu Sans',Arial,sans-serif"

DOT = "·"
OPLUS = "⊕"


# ---------------------------------------------------------------- utilidades
def svg_doc(width, height, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img">\n'
        f"<title>{title}</title>\n{body}\n</svg>\n"
    )


def text(x, y, content, size=14, color=INK, anchor="start", weight="normal", family=MONO):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}" font-weight="{weight}">{content}</text>'
    )


def over(s):
    """Texto con barra superior (negacion)."""
    return f'<tspan text-decoration="overline">{s}</tspan>'


def wire(*pts, color=INK, width=2):
    d = " ".join(f"{x},{y}" for x, y in pts)
    return (
        f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
    )


def dot(x, y):
    return f'<circle cx="{x}" cy="{y}" r="3.5" fill="{INK}"/>'


def arrow(x, y, color=INK):
    return f'<path d="M{x - 9},{y - 5} L{x},{y} L{x - 9},{y + 5} Z" fill="{color}"/>'


# ------------------------------------------------------------------- puertas
def gate(kind, x, y, h=60, n_in=2, label=None):
    """Dibuja una puerta con esquina superior izquierda (x, y) y altura h.

    Devuelve (svg, entradas, salida) con las coordenadas de los pines.
    """
    base = kind.replace("n", "", 1) if kind in ("nand", "nor") else kind
    if kind == "xnor":
        base = "xor"
    if kind == "not":
        base = "buf"
    bubble = kind in ("nand", "nor", "xnor", "not")

    def P(u, v):
        return f"{x + u * h:.1f},{y + v * h:.1f}"

    parts = []
    if base == "and":
        path = f"M{P(0, 0)} H{x + 0.55 * h:.1f} A{0.5 * h:.1f},{0.5 * h:.1f} 0 0 1 {P(0.55, 1)} H{x:.1f} Z"
        out_u = 1.05

        def in_u(v):
            return 0.0
    elif base in ("or", "xor"):
        s = 0.16 if base == "xor" else 0.0
        path = (
            f"M{P(s, 0)} Q{P(s + 0.3, 0.5)} {P(s, 1)} "
            f"Q{P(s + 0.75, 1)} {P(s + 1.15, 0.5)} Q{P(s + 0.75, 0)} {P(s, 0)} Z"
        )
        out_u = s + 1.15
        if base == "xor":
            parts.append(
                f'<path d="M{P(0, 0)} Q{P(0.3, 0.5)} {P(0, 1)}" fill="none" stroke="{INK}" '
                f'stroke-width="2" stroke-linecap="round"/>'
            )

        def in_u(v):
            return 2 * v * (1 - v) * 0.3
    else:  # buf
        path = f"M{P(0, 0.06)} L{P(0.9, 0.5)} L{P(0, 0.94)} Z"
        out_u = 0.9

        def in_u(v):
            return 0.0

    parts.insert(
        0,
        f'<path d="{path}" fill="{GATE_FILL}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>',
    )
    if bubble:
        r = 0.085 * h
        parts.append(
            f'<circle cx="{x + out_u * h + r:.1f}" cy="{y + 0.5 * h:.1f}" r="{r:.1f}" '
            f'fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>'
        )
        out_u += 2 * 0.085
    if label:
        cx = x + (0.42 if base == "and" else 0.5 if base == "or" else 0.62 if base == "xor" else 0.32) * h
        parts.append(text(f"{cx:.1f}", f"{y + 0.5 * h + 4.5:.1f}", label, size=12, color=ACCENT,
                          anchor="middle", weight="bold"))

    if n_in == 1:
        vs = [0.5]
    else:
        vs = [0.25, 0.75]
    ins = [(round(x + in_u(v) * h, 1), round(y + v * h, 1)) for v in vs]
    out = (round(x + out_u * h, 1), round(y + 0.5 * h, 1))
    return "\n".join(parts), ins, out


# ------------------------------------------------------- fichas de cada puerta
GATES = {
    "and": ("AND", f"a{DOT}b", lambda a, b: a & b, 2),
    "or": ("OR", "a+b", lambda a, b: a | b, 2),
    "not": ("NOT", over("a"), lambda a: 1 - a, 1),
    "nand": ("NAND", over(f"a{DOT}b"), lambda a, b: 1 - (a & b), 2),
    "nor": ("NOR", over("a+b"), lambda a, b: 1 - (a | b), 2),
    "xor": ("XOR", f"a{OPLUS}b", lambda a, b: a ^ b, 2),
    "xnor": ("XNOR", over(f"a{OPLUS}b"), lambda a, b: 1 - (a ^ b), 2),
    "buf": ("BUFFER", "a", lambda a: a, 1),
}


def gate_card(kind):
    name, expr, fn, n = GATES[kind]
    rows = [(0,), (1,)] if n == 1 else [(0, 0), (0, 1), (1, 0), (1, 1)]
    row_h, head_h = 26, 28
    table_h = head_h + row_h * len(rows)
    width = 470
    height = max(168, table_h + 40)
    body = [
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="12" '
        f'fill="{CARD_BG}" stroke="{CARD_BORDER}" stroke-width="2"/>',
        text(22, 36, name, size=17, weight="bold", family=SANS),
        text(22, 56, f"{kind}(salida,{'a' if n == 1 else 'a,b'})", size=12, color=MUTED),
    ]

    # Simbolo
    gh = 56
    gx, gy = 92, height / 2 - gh / 2 + 12
    g, ins, out = gate(kind, gx, gy, h=gh, n_in=n)
    names = ["a"] if n == 1 else ["a", "b"]
    for (px, py), nm in zip(ins, names):
        body.append(wire((44, py), (px, py)))
        body.append(text(30, py + 5, nm, size=15, color=INK, anchor="middle"))
    body.append(g)
    body.append(wire(out, (out[0] + 26, out[1])))
    body.append(text(out[0] + 34, out[1] + 5, expr, size=15, color=ACCENT, weight="bold"))

    # Tabla de verdad
    cols = names + [name]
    col_w = [36] * len(names) + [max(64, 11 * len(name) + 22)]
    tw = sum(col_w)
    tx = width - tw - 22
    ty = (height - table_h) / 2
    body.append(
        f'<rect x="{tx}" y="{ty}" width="{tw}" height="{table_h}" rx="8" fill="#FFFFFF" '
        f'stroke="{GRID}" stroke-width="1.5"/>'
    )
    body.append(
        f'<path d="M{tx},{ty + head_h} V{ty + 8} Q{tx},{ty} {tx + 8},{ty} H{tx + tw - 8} '
        f'Q{tx + tw},{ty} {tx + tw},{ty + 8} V{ty + head_h} Z" fill="{HEAD_BG}"/>'
    )
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
        vals = list(r) + [fn(*r)]
        cx = tx
        for k, (v, w) in enumerate(zip(vals, col_w)):
            is_out = k == len(vals) - 1
            mid = cx + w / 2
            if v == 1:
                body.append(
                    f'<rect x="{mid - 12}" y="{yv + 4}" width="24" height="{row_h - 8}" rx="5" fill="{ACCENT_BG}"/>'
                )
            body.append(
                text(mid, yv + 18, str(v), size=14, color=ACCENT if v == 1 else MUTED,
                     anchor="middle", weight="bold" if is_out or v == 1 else "normal")
            )
            cx += w
    return svg_doc(width, height, "\n".join(body), f"Puerta {name}: simbolo y tabla de verdad")


# ---------------------------------------------------------------- circuitos
def fig_andvar():
    w, h = 440, 150
    b = []
    g, ins, out = gate("and", 170, 40, h=64, label="a1")
    b.append(g)
    for (px, py), nm in zip(ins, ["a", "b"]):
        b.append(wire((70, py), (px, py)))
        b.append(f'<rect x="34" y="{py - 13}" width="34" height="26" rx="6" fill="{CARD_BG}" stroke="{GRID}" stroke-width="1.5"/>')
        b.append(text(51, py + 5, nm, size=15, anchor="middle"))
    b.append(wire(out, (330, out[1])))
    b.append(arrow(330, out[1]))
    b.append(text(340, out[1] + 5, "salida", size=15))
    b.append(text(51, 30, "reg", size=11, color=ACCENT, anchor="middle", weight="bold"))
    b.append(text(340, out[1] - 14, "wire", size=11, color=ACCENT, weight="bold"))
    b.append(text(w / 2, 138, "and a1( salida , a , b );", size=13, color=MUTED, anchor="middle"))
    return svg_doc(w, h, "\n".join(b), "Instancia and a1(salida,a,b)")


def fig_f2(named=False):
    w, h = 520, 170 if named else 160
    b = []
    ga, ia, oa = gate("and", 110, 70, h=56, label="a1" if named else None)
    go, io, oo = gate("or", 300, 30, h=56, label="o1" if named else None)
    b += [ga, go]
    la = ["r[2]", "r[1]"] if named else ["a", "b"]
    lc = "r[0]" if named else "c"
    for (px, py), nm in zip(ia, la):
        b.append(wire((60, py), (px, py)))
        b.append(text(52, py + 5, nm, size=15, anchor="end"))
    # c hacia la OR
    b.append(wire((60, io[0][1]), io[0]))
    b.append(text(52, io[0][1] + 5, lc, size=15, anchor="end"))
    # cable intermedio
    xm = 250
    b.append(wire(oa, (xm, oa[1]), (xm, io[1][1]), io[1]))
    if named:
        b.append(text(xm - 44, oa[1] - 8, "ab", size=13, color=ACCENT, weight="bold"))
        b.append(text(xm - 44, oa[1] + 22, "wire", size=11, color=MUTED))
    else:
        b.append(text(xm - 46, oa[1] + 22, f"a{DOT}b", size=14, color=MUTED))
    b.append(wire(oo, (oo[0] + 50, oo[1])))
    b.append(arrow(oo[0] + 50, oo[1]))
    b.append(text(oo[0] + 60, oo[1] + 5, "salida" if named else "ab+c", size=15,
                  color=INK if named else ACCENT, weight="normal" if named else "bold"))
    if named:
        b.append(text(oo[0] + 60, oo[1] + 26, "ab+c", size=13, color=ACCENT, weight="bold"))
    return svg_doc(w, h, "\n".join(b), "Circuito de f2 = ab + c")


def fig_f3():
    w, h = 760, 470
    b = []
    b.append(text(w / 2, 30, f"f<tspan baseline-shift=\"sub\" font-size=\"11\">3</tspan>(a,b,c) = b{DOT}c + a{DOT}b{DOT}{over('c')} + {over('b')}{DOT}c + c",
                  size=16, anchor="middle", weight="bold"))
    # Rieles de entrada
    xa, xb, xc = 50, 90, 130
    xnb, xnc = 230, 270
    top, bottom = 70, 440
    for x, nm in ((xa, "a"), (xb, "b"), (xc, "c")):
        b.append(text(x, top - 10, nm, size=16, anchor="middle", weight="bold"))
    b.append(wire((xa, top), (xa, 410)))
    b.append(wire((xb, top), (xb, 332.5)))
    b.append(wire((xc, top), (xc, 277.5)))
    # Inversores
    gnb, inb, onb = gate("not", 150, 70, h=36, n_in=1)
    gnc, inc, onc = gate("not", 150, 120, h=36, n_in=1)
    b += [gnb, gnc]
    b.append(wire((xb, inb[0][1]), inb[0])); b.append(dot(xb, inb[0][1]))
    b.append(wire((xc, inc[0][1]), inc[0])); b.append(dot(xc, inc[0][1]))
    b.append(wire(onb, (xnb, onb[1]), (xnb, 182.5)))
    b.append(wire(onc, (xnc, onc[1]), (xnc, 357.5)))
    b.append(text(xnb + 6, onb[1] - 8, over("b"), size=14, color=ACCENT, weight="bold"))
    b.append(text(xnc + 6, onc[1] - 8, over("c"), size=14, color=ACCENT, weight="bold"))

    gx, gh = 330, 50
    # AND1 = notB.c
    g1, i1, o1 = gate("and", gx, 170, h=gh)
    b.append(g1)
    b.append(wire((xnb, i1[0][1]), i1[0]))
    b.append(wire((xc, i1[1][1]), i1[1])); b.append(dot(xc, i1[1][1]))
    # AND2 = b.c
    g2, i2, o2 = gate("and", gx, 240, h=gh)
    b.append(g2)
    b.append(wire((xb, i2[0][1]), i2[0])); b.append(dot(xb, i2[0][1]))
    b.append(wire((xc, i2[1][1]), i2[1]))
    # AND3 = b.notC
    g3, i3, o3 = gate("and", gx, 320, h=gh)
    b.append(g3)
    b.append(wire((xb, i3[0][1]), i3[0]))
    b.append(wire((xnc, i3[1][1]), i3[1]))
    # AND4 = (b.notC).a
    g4, i4, o4 = gate("and", 450, 340, h=gh)
    b.append(g4)
    b.append(wire(o3, (420, o3[1]), (420, i4[0][1]), i4[0]))
    b.append(wire((xa, 410), (430, 410), (430, i4[1][1]), i4[1]))
    # OR1 = c + notB.c
    gr1, ir1, or1 = gate("or", 520, 100, h=gh)
    b.append(gr1)
    b.append(wire((xc, ir1[0][1]), ir1[0])); b.append(dot(xc, ir1[0][1]))
    b.append(wire(o1, (480, o1[1]), (480, ir1[1][1]), ir1[1]))
    # OR2 = b.c + a.b.notC
    gr2, ir2, or2 = gate("or", 560, 250, h=gh)
    b.append(gr2)
    b.append(wire(o2, ir2[0]) if o2[1] == ir2[0][1] else wire(o2, (500, o2[1]), (500, ir2[0][1]), ir2[0]))
    b.append(wire(o4, (530, o4[1]), (530, ir2[1][1]), ir2[1]))
    # OR final
    gf, if_, of = gate("or", 650, 160, h=gh)
    b.append(gf)
    b.append(wire(or1, (630, or1[1]), (630, if_[0][1]), if_[0]))
    b.append(wire(or2, (636, or2[1]), (636, if_[1][1]), if_[1]))
    b.append(wire(of, (of[0] + 22, of[1])))
    b.append(text(of[0] + 4, of[1] - 12, "f<tspan baseline-shift=\"sub\" font-size=\"11\">3</tspan>", size=16, weight="bold", color=ACCENT))

    # Etiquetas de las salidas intermedias
    lab = dict(size=13, color=MUTED)
    b.append(text(o1[0] + 8, o1[1] + 20, f"{over('b')}{DOT}c", **lab))
    b.append(text(o2[0] + 8, o2[1] + 20, f"b{DOT}c", **lab))
    b.append(text(o3[0] + 4, o3[1] + 22, f"b{DOT}{over('c')}", **lab))
    b.append(text(o4[0] + 6, o4[1] + 24, f"a{DOT}b{DOT}{over('c')}", **lab))
    b.append(text(or1[0] - 40, or1[1] - 32, f"c+{over('b')}{DOT}c", **lab))
    b.append(text(or2[0] - 10, or2[1] + 44, f"b{DOT}c+a{DOT}b{DOT}{over('c')}", **lab))
    return svg_doc(w, h, "\n".join(b), "Diagrama con puertas de f3")


def fig_f3nand():
    w, h = 560, 200
    b = []
    g1, i1, o1 = gate("nand", 110, 30, h=56)
    g2, i2, o2 = gate("nand", 160, 110, h=56)
    g3, i3, o3 = gate("nand", 360, 60, h=56)
    b += [g1, g2, g3]
    for (px, py), nm in zip(i1, ["a", "b"]):
        b.append(wire((60, py), (px, py)))
        b.append(text(50, py + 5, nm, size=15, anchor="end"))
    # c a las dos entradas de la segunda NAND
    yc = (i2[0][1] + i2[1][1]) / 2
    b.append(wire((60, yc), (130, yc)))
    b.append(text(50, yc + 5, "c", size=15, anchor="end"))
    b.append(wire((130, i2[0][1]), (130, i2[1][1])))
    b.append(dot(130, yc))
    b.append(wire((130, i2[0][1]), i2[0]))
    b.append(wire((130, i2[1][1]), i2[1]))
    b.append(wire(o1, (320, o1[1]), (320, i3[0][1]), i3[0]))
    b.append(wire(o2, (320, o2[1]), (320, i3[1][1]), i3[1]))
    b.append(text(o1[0] + 14, o1[1] - 10, over(f"a{DOT}b"), size=14, color=MUTED))
    b.append(text(o2[0] + 14, o2[1] + 24, over("c"), size=14, color=MUTED))
    b.append(wire(o3, (o3[0] + 50, o3[1])))
    b.append(arrow(o3[0] + 50, o3[1]))
    b.append(text(o3[0] + 60, o3[1] + 6, "f<tspan baseline-shift=\"sub\" font-size=\"11\">3</tspan>", size=17, weight="bold", color=ACCENT))
    return svg_doc(w, h, "\n".join(b), "f3 solo con puertas NAND")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = {f"{k}.svg": gate_card(k) for k in GATES}
    files["andvar.svg"] = fig_andvar()
    files["f2.svg"] = fig_f2(named=False)
    files["f2var.svg"] = fig_f2(named=True)
    files["f3.svg"] = fig_f3()
    files["f3nand.svg"] = fig_f3nand()
    for name, content in files.items():
        (OUT_DIR / name).write_text(content, encoding="utf-8")
        print("ok", name)


if __name__ == "__main__":
    main()
