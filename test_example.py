import sys
import time
from handwriting import Pen, focus_workspace, active_window_title, move_cursor, preview_image


def draw(pen):
    pen.text("№1", 400, 250, 44)
    pen.system("1)", ["2x-4>0", "x+1≤5"], 400, 340)
    pen.system(None, ["x>2", "x≤4"], 860, 340)
    pen.number_line(1100, 1560, 460, [(2, False, True), (4, True, False)], {2: "2", 4: "4"})
    pen.text("x∈(2;4]", 1130, 560, 46)


if __name__ == "__main__":
    if "--draw" not in sys.argv:
        image, canvas = preview_image()
        with Pen(preview=canvas) as pen:
            draw(pen)
        image.save("test_example_preview.png")
        print(f"preview saved, {pen.strokes} strokes")
        sys.exit()
    focus_workspace(1)
    time.sleep(0.5)
    title = active_window_title()
    if "tldraw" not in title:
        sys.exit(f"active window is not tldraw: {title}")
    with Pen() as pen:
        draw(pen)
    print(f"done, {pen.strokes} strokes")
