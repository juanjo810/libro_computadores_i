"""Genera las figuras SVG de la sesion 9 (ALU 74181).

Uso (desde la raiz del proyecto):
    python diagram_sources/verilog/sesion_09_figuras.py

Reutiliza el estilo de las sesiones anteriores y escribe los SVG en
book/_static/verilog/sesion_09/svg/.
"""

from pathlib import Path

from sesion_03_figuras import ACCENT, GATE_FILL, INK, MUTED, SANS, arrow, over, svg_doc, text, wire
from sesion_04_figuras import arrow_down
from sesion_05_figuras import subc

OUT_DIR = Path(__file__).resolve().parents[2] / "book" / "_static" / "verilog" / "sesion_09" / "svg"


def bus_mark(x, y, vertical=True):
    """Marca de bus de cuatro bits sobre un cable."""
    if vertical:
        return wire((x - 6, y + 6), (x + 6, y - 6), width=1.5) + text(x - 12, y + 5, "4", size=12, color=MUTED, anchor="end")
    return wire((x - 6, y + 6), (x + 6, y - 6), width=1.5) + text(x, y - 10, "4", size=12, color=MUTED, anchor="middle")


def fig_alu():
    w, h = 470, 240
    b = []
    # Cuerpo de la ALU: trapecio con muesca superior
    pts = [(130, 80), (210, 80), (230, 115), (250, 80), (330, 80), (290, 160), (170, 160)]
    b.append(f'<path d="M{" L".join(f"{x},{y}" for x, y in pts)} Z" fill="{GATE_FILL}" stroke="{INK}" '
             f'stroke-width="2" stroke-linejoin="round"/>')
    b.append(text(230, 145, "ALU", size=18, anchor="middle", weight="bold", family=SANS))
    # Operandos
    for x, lab in ((170, "A"), (290, "B")):
        b.append(wire((x, 30), (x, 71)))
        b.append(arrow_down(x, 80))
        b.append(bus_mark(x, 52))
        b.append(text(x, 22, lab, size=16, anchor="middle"))
    # Entradas de control (borde izquierdo inclinado)
    def x_izq(y):
        return 130 + (y - 80) * 40 / 80

    for y, lab in ((92, "S"), (115, "M"), (138, subc(over("C"), "n", size=16))):
        b.append(wire((62, y), (x_izq(y) - 9, y)))
        b.append(arrow(x_izq(y), y))
        b.append(text(54, y + 6, lab, size=16, anchor="end"))
    b.append(bus_mark(88, 92, vertical=False))

    # Salidas (borde derecho inclinado)
    def x_der(y):
        return 330 - (y - 80) * 40 / 80

    for y, lab in ((100, "AEB"), (135, subc(over("C"), "n+4", size=16))):
        b.append(wire((x_der(y), y), (381, y)))
        b.append(arrow(390, y))
        b.append(text(398, y + 6, lab, size=16, color=ACCENT, weight="bold"))
    b.append(wire((230, 160), (230, 199)))
    b.append(arrow_down(230, 208))
    b.append(bus_mark(230, 180))
    b.append(text(230, 230, "F", size=16, color=ACCENT, weight="bold", anchor="middle"))
    return svg_doc(w, h, "\n".join(b), "Esquema de la ALU 74181")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "74181.svg").write_text(fig_alu(), encoding="utf-8")
    print("ok 74181.svg")


if __name__ == "__main__":
    main()
