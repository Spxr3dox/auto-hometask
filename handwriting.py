import math
import os
import random
import socket
import time

SOCKET_PATH = f"{os.environ.get('XDG_RUNTIME_DIR', '/run/user/1000')}/hypr/{os.environ.get('HYPRLAND_INSTANCE_SIGNATURE', '')}/.socket.sock"


def hypr(command):
    connection = socket.socket(socket.AF_UNIX)
    connection.connect(SOCKET_PATH)
    connection.sendall(command.encode())
    reply = connection.recv(4096)
    connection.close()
    return reply


def move_cursor(x, y):
    hypr(f"eval hl.dispatch(hl.dsp.cursor.move({{ x = {int(round(x))}, y = {int(round(y))} }}))")


def focus_workspace(number):
    hypr(f"eval hl.dispatch(hl.dsp.focus({{ workspace = {number} }}))")


def active_window_title():
    import json
    return json.loads(hypr("j/activewindow").decode() or "{}").get("title", "")


def arc(cx, cy, rx, ry, a0, a1, n=14):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy - ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


GLYPHS = {}
WIDTHS = {}


def glyph(char, width, strokes):
    GLYPHS[char] = strokes
    WIDTHS[char] = width


glyph('0', .5, [arc(.25, .5, .22, .48, 90, 450, 24)])
glyph('1', .4, [[(.08, .25), (.3, 0), (.3, 1)]])
glyph('2', .5, [arc(.25, .27, .22, .25, 160, -20, 12) + [(.03, 1), (.5, 1)]])
glyph('3', .5, [arc(.25, .26, .21, .24, 150, -90, 12) + arc(.25, .74, .25, .26, 90, -150, 12)[1:]])
glyph('4', .5, [[(.38, 1), (.38, 0), (.02, .68), (.5, .68)]])
glyph('5', .5, [[(.45, 0), (.1, 0), (.06, .45)] + arc(.25, .68, .25, .3, 130, -150, 14)[1:]])
glyph('6', .5, [[(.42, .03), (.2, .22), (.06, .55)] + arc(.26, .72, .21, .26, 180, 540, 20)])
glyph('7', .5, [[(.02, 0), (.5, 0), (.16, 1)]])
glyph('8', .5, [arc(.25, .25, .19, .23, 270, 630, 18), arc(.25, .72, .24, .27, 90, 450, 20)])
glyph('9', .5, [arc(.25, .28, .21, .26, 0, 360, 20), [(.46, .3), (.36, 1)]])
glyph('x', .45, [[(.02, .4), (.42, 1)], [(.42, .4), (.02, 1)]])
glyph('y', .45, [[(.02, .4), (.22, .78)], [(.42, .4), (.1, 1.2)]])
glyph('a', .45, [arc(.2, .72, .18, .27, 60, 420, 16), [(.4, .45), (.4, 1)]])
glyph('b', .45, [[(.05, 0), (.05, 1)], arc(.22, .72, .18, .27, 180, 540, 16)])
glyph('c', .42, [arc(.24, .72, .2, .28, 50, 310, 14)])
glyph('-', .45, [[(.05, .68), (.4, .68)]])
glyph('+', .5, [[(.05, .68), (.45, .68)], [(.25, .46), (.25, .9)]])
glyph('<', .45, [[(.4, .42), (.04, .67), (.4, .92)]])
glyph('>', .45, [[(.04, .42), (.4, .67), (.04, .92)]])
glyph('≤', .45, [[(.4, .3), (.04, .55), (.4, .8)], [(.04, .98), (.4, .98)]])
glyph('≥', .45, [[(.04, .3), (.4, .55), (.04, .8)], [(.04, .98), (.4, .98)]])
glyph('=', .45, [[(.05, .55), (.4, .55)], [(.05, .8), (.4, .8)]])
glyph('.', .2, [arc(.08, .96, .03, .03, 0, 360, 6)])
glyph(',', .22, [[(.12, .9), (.04, 1.12)]])
glyph(';', .25, [arc(.1, .5, .03, .03, 0, 360, 6), [(.12, .9), (.04, 1.12)]])
glyph(':', .2, [arc(.08, .5, .03, .03, 0, 360, 6), arc(.08, .92, .03, .03, 0, 360, 6)])
glyph('(', .3, [arc(.42, .5, .3, .55, 125, 235, 10)])
glyph(')', .3, [arc(-.12, .5, .3, .55, 55, -55, 10)])
glyph('[', .3, [[(.26, -.02), (.06, -.02), (.06, 1.02), (.26, 1.02)]])
glyph(']', .3, [[(.04, -.02), (.24, -.02), (.24, 1.02), (.04, 1.02)]])
glyph('/', .35, [[(.3, 0), (.05, 1)]])
glyph('∈', .5, [arc(.42, .68, .34, .3, 90, 270, 12), [(.1, .68), (.44, .68)]])
glyph('∞', .9, [[(.45 + .42 * math.cos(t) / (1 + math.sin(t) ** 2), .68 + .5 * math.sin(t) * math.cos(t) / (1 + math.sin(t) ** 2))
                 for t in [i * 2 * math.pi / 28 for i in range(29)]]])
glyph('R', .45, [[(.06, 1), (.06, 0), (.24, 0)] + arc(.24, .25, .18, .25, 90, -90, 8)[1:] + [(.06, .5)], [(.22, .5), (.44, 1)]])
glyph('∅', .55, [arc(.27, .6, .22, .38, 0, 360, 18), [(.5, .12), (.04, 1.08)]])
glyph('№', .9, [[(.05, 1), (.05, 0), (.4, 1), (.4, 0)], arc(.64, .45, .12, .16, 0, 360, 12), [(.52, .78), (.78, .78)]])
glyph(' ', .3, [])
glyph('²', .28, [[(x * .5, y * .5 - .02) for x, y in stroke] for stroke in GLYPHS['2']])


class Pen:
    def __init__(self, transform=None, lead_in=7.0, preview=None, seed=7):
        self.transform = transform
        self.lead_in = lead_in
        self.preview = preview
        self.strokes = 0
        self.random = random.Random(seed)
        self.device = None

    def __enter__(self):
        if self.preview is None:
            import evdev
            from evdev import ecodes
            self.ecodes = ecodes
            self.device = evdev.UInput({ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT], ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y]},
                                       name="homework-pen")
            time.sleep(1.0)
        return self

    def __exit__(self, *exc):
        if self.device:
            self._button(0)
            time.sleep(0.2)
            self.device.close()

    def _button(self, down):
        self.device.write(self.ecodes.EV_KEY, self.ecodes.BTN_LEFT, down)
        self.device.syn()

    def _map(self, points):
        if not self.transform:
            return list(points)
        return [self.transform(x, y) for x, y in points]

    def stroke(self, points):
        points = self._map(points)
        if len(points) < 2:
            return
        self.strokes += 1
        if self.preview is not None:
            self.preview.line(points, fill="red", width=3)
            return
        x0, y0 = points[0]
        for x1, y1 in points[1:]:
            distance = math.hypot(x1 - x0, y1 - y0)
            if distance > 0.5:
                points.insert(0, (x0 - (x1 - x0) / distance * self.lead_in, y0 - (y1 - y0) / distance * self.lead_in))
                break
        move_cursor(*points[0])
        time.sleep(0.03)
        self._button(1)
        time.sleep(0.04)
        for i in range(1, len(points)):
            ax, ay = points[i - 1]
            bx, by = points[i]
            steps = max(2, int(math.hypot(bx - ax, by - ay) / 3))
            for k in range(1, steps + 1):
                move_cursor(ax + (bx - ax) * k / steps, ay + (by - ay) * k / steps)
                time.sleep(0.006)
        time.sleep(0.04)
        self._button(0)
        time.sleep(0.03)

    def tokens(self, text):
        i = 0
        while i < len(text):
            if text[i] == '{':
                j = text.index('}', i)
                numerator, denominator = text[i + 1:j].split('|')
                yield ('fraction', numerator, denominator)
                i = j + 1
            else:
                yield ('char', text[i])
                i += 1

    def text_width(self, text, height):
        total = 0
        for token in self.tokens(text):
            if token[0] == 'fraction':
                total += max(self.text_width(token[1], height * .72), self.text_width(token[2], height * .72)) + 4 + .16 * height
            else:
                total += (WIDTHS[token[1]] + .16) * height
        return total

    def text(self, text, x, y, height, slant=0.12):
        for token in self.tokens(text):
            if token[0] == 'fraction':
                small = height * .72
                width = max(self.text_width(token[1], small), self.text_width(token[2], small)) + 4
                self.text(token[1], x + (width - self.text_width(token[1], small)) / 2, y - height * .3, small, slant)
                self.stroke([(x, y + height * .5), (x + width, y + height * .5)])
                self.text(token[2], x + (width - self.text_width(token[2], small)) / 2, y + height * .58, small, slant)
                x += width + .16 * height
                continue
            char = token[1]
            if char not in GLYPHS:
                raise ValueError(f"no glyph for {char!r}")
            jx, jy = self.random.uniform(-1.5, 1.5), self.random.uniform(-2, 2)
            for glyph_stroke in GLYPHS[char]:
                self.stroke([(x + jx + (px + (1 - py) * slant) * height + self.random.uniform(-.6, .6),
                              y + jy + py * height + self.random.uniform(-.6, .6)) for px, py in glyph_stroke])
            x += (WIDTHS[char] + .16) * height
        return x

    def brace(self, x, top, bottom, k=1.0):
        mid = (top + bottom) / 2
        w, r = 14 * k, 12 * k
        self.stroke(arc(x + w, top + r, w * .6, r, 90, 180, 5) + [(x + w * .4, mid - r), (x, mid), (x + w * .4, mid + r)]
                    + arc(x + w, bottom - r, w * .6, r, 180, 270, 5))

    def point(self, x, y, closed, k=1.0):
        self.stroke(arc(x, y, 7 * k, 7 * k, 0, 360, 12))
        if closed:
            self.stroke(arc(x, y, 4 * k, 4 * k, 0, 720, 16))
            self.stroke([(x - 3 * k, y), (x + 3 * k, y)])

    def number_line(self, x0, x1, y, constraints, labels, k=1.0, hatch=True, axis='x'):
        self.stroke([(x0, y), (x1, y)])
        self.stroke([(x1 - 16 * k, y - 9 * k), (x1, y), (x1 - 16 * k, y + 9 * k)])
        self.text(axis, x1 - 10 * k, y + 8 * k, 26 * k)
        values = sorted({c[0] for c in constraints if c[0] is not None})
        span = x1 - x0 - 40 * k
        if len(values) == 1:
            positions = {values[0]: x0 + span * .5}
        else:
            positions = {v: x0 + span * (.32 + .36 * i / max(1, len(values) - 1)) for i, v in enumerate(values)}
        for (value, closed, right), h in zip(constraints, [44 * k, 70 * k]):
            if value is None:
                if closed == 'all':
                    self.stroke([(x0 + 8 * k, y - h), (x1 - 22 * k, y - h)])
                continue
            px = positions[value]
            end = x1 - 22 * k if right else x0 + 8 * k
            knee = px + (22 * k if right else -22 * k)
            self.stroke([(px, y - 8 * k), (knee, y - h), (end, y - h)])
        for value, closed, right in constraints:
            if value is not None:
                self.point(positions[value], y, closed, k)
        for value in values:
            label = labels[value]
            size = 34 * k if '{' in label else 28 * k
            self.text(label, positions[value] - self.text_width(label, size) / 2, y + (22 if '{' in label else 14) * k, size, .08)
        if not hatch or any(c[0] is None and c[1] == 'empty' for c in constraints):
            return
        low = [positions[c[0]] for c in constraints if c[0] is not None and c[2]]
        high = [positions[c[0]] for c in constraints if c[0] is not None and not c[2]]
        a = max(low, default=x0 + 8 * k)
        b = min(high, default=x1 - 26 * k)
        xx = a + 10 * k
        while xx < b - 4 * k:
            self.stroke([(xx, y - 3 * k), (xx + 14 * k, y - 30 * k)])
            xx += 16 * k

    def system(self, label, lines, x0, y0, k=1.0, gap=90):
        height = 42 * k
        if label:
            self.text(label, x0, y0 + (gap * k) / 2 + 12 * k, height)
            x0 += 62 * k
        self.brace(x0, y0 + 8 * k, y0 + (gap + 72) * k, k)
        for i, line in enumerate(lines):
            self.text(line, x0 + 22 * k, y0 + (14 + i * gap) * k, height)


def preview_image(width=2560, height=1440, background=None):
    from PIL import Image, ImageDraw
    image = Image.open(background).convert("RGB").resize((width, height)) if background else Image.new("RGB", (width, height), "white")
    return image, ImageDraw.Draw(image)


def affine(origin_screen, origin_design, scale):
    ox, oy = origin_screen
    dx, dy = origin_design
    return lambda x, y: (ox + (x - dx) * scale, oy + (y - dy) * scale)
