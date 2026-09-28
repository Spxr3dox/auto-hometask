import sys
import time
from handwriting import Pen, focus_workspace, active_window_title, preview_image

K = 0.8

ITEMS = [
    ("1)", ["12x+27+5>56-7x", "19x>24", "x>{24|19}"], [(24 / 19, False, True)], {24 / 19: "{24|19}"}, "x", "x∈({24|19};+∞)"),
    ("2)", ["6-y-y²≤24+2y-y²", "6-y≤24+2y", "-3y≤18", "y≥-6"], [(-6, True, True)], {-6: "-6"}, "y", "y∈[-6;+∞)"),
    ("3)", ["y²-2y-15-y²+2y-1>-16", "-16>-16", "y∈∅"], [(None, "empty", True)], {}, "y", "y∈∅"),
    ("4)", ["9x-21-15≥10x-30", "-x≥6", "x≤-6"], [(-6, True, False)], {-6: "-6"}, "x", "x∈(-∞;-6]"),
    ("5)", ["4x-x+1-3x-6<0", "-5<0", "x∈R"], [(None, "all", True)], {}, "x", "x∈(-∞;+∞)"),
    ("6)", ["4y-4-2y-1-8y<16", "-6y<21", "y>-3,5"], [(-3.5, False, True)], {-3.5: "-3,5"}, "y", "y∈(-3,5;+∞)"),
]


def item(pen, entry, x0, y0):
    label, lines, constraints, labels, axis, answer = entry
    height = 42 * K
    pen.text(label, x0, y0 + 52 * K, height)
    step = 66 * K if len(lines) <= 3 else 50 * K
    for i, line in enumerate(lines):
        size = min(height, 400 * K / max(1, pen.text_width(line, 1)))
        pen.text(line, x0 + 62 * K, y0 + i * step + (height - size), size)
    pen.number_line(x0 + 470 * K, x0 + 880 * K, y0 + 120 * K, constraints, labels, K, axis=axis)
    pen.text(answer, x0 + 490 * K, y0 + 205 * K, 44 * K)


def draw(pen):
    pen.text("5.26", 900, 215, 40)
    for index, entry in enumerate(ITEMS):
        item(pen, entry, 900 + (index % 2) * 740, 290 + (index // 2) * 350)


if __name__ == "__main__":
    if "--draw" not in sys.argv:
        background = sys.argv[1] if len(sys.argv) > 1 else None
        image, canvas = preview_image(background=background)
        with Pen(preview=canvas) as pen:
            draw(pen)
        image.save("dz_5_26_preview.png")
        print(f"preview saved, {pen.strokes} strokes")
        sys.exit()
    title = active_window_title()
    if "tldraw" not in title:
        sys.exit(f"active window is not tldraw: {title}")
    with Pen() as pen:
        draw(pen)
    print(f"done, {pen.strokes} strokes")
