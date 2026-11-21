"""Hand-built Pillow illustrations, one function per scene. Each draws into its own tile
(so nothing leaks outside the box), in local units where the tile is w x h (1024-px units).
Deterministic: no randomness; repeated elements use fixed index arithmetic."""
import math

from PIL import Image, ImageDraw

NIGHT = (24, 32, 58)
SKY = (206, 226, 236)
SAND = (236, 222, 190)
WIN = (250, 208, 96)
WHITE = (255, 255, 255)
INK = (34, 34, 40)


class Pen:
    def __init__(self, w, h, s, bg):
        self.w, self.h, self.s = w, h, s
        self.img = Image.new("RGB", (round(w * s), round(h * s)), bg)
        self.d = ImageDraw.Draw(self.img)

    def p(self, *v):
        return [round(x * self.s) for x in v]

    def rect(self, x0, y0, x1, y1, fill, outline=None, width=1):
        self.d.rectangle(self.p(x0, y0, x1, y1), fill=fill, outline=outline, width=round(width * self.s))

    def rrect(self, x0, y0, x1, y1, r, fill, outline=None, width=1):
        self.d.rounded_rectangle(self.p(x0, y0, x1, y1), radius=round(r * self.s), fill=fill,
                                 outline=outline, width=round(width * self.s))

    def ell(self, cx, cy, rx, ry, fill, outline=None, width=1):
        self.d.ellipse(self.p(cx - rx, cy - ry, cx + rx, cy + ry), fill=fill, outline=outline,
                       width=round(width * self.s))

    def poly(self, pts, fill, outline=None):
        self.d.polygon([(round(x * self.s), round(y * self.s)) for x, y in pts], fill=fill, outline=outline)

    def line(self, pts, fill, width=1.5):
        self.d.line([(round(x * self.s), round(y * self.s)) for x, y in pts], fill=fill,
                    width=max(1, round(width * self.s)), joint="curve")

    def dashed(self, x0, y0, x1, y1, fill, width=1.5, dash=5, gap=4):
        n = math.hypot(x1 - x0, y1 - y0)
        t = 0
        while t < n:
            a, b = t / n, min(t + dash, n) / n
            self.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)],
                      fill, width)
            t += dash + gap

    def arc(self, cx, cy, r, a0, a1, fill, width=2):
        self.d.arc(self.p(cx - r, cy - r, cx + r, cy + r), a0, a1, fill=fill, width=round(width * self.s))

    def star(self, cx, cy, r, fill, n=8):
        pts = []
        for i in range(2 * n):
            rr = r if i % 2 == 0 else r * 0.45
            a = math.pi * i / n
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.poly(pts, fill)


# ---------- reusable pieces ----------

def skyline(p, base, cols, lit=WIN, dark=(14, 20, 40), seed=0):
    """Row of buildings; heights from a fixed pattern."""
    hs = [0.42, 0.62, 0.35, 0.78, 0.5, 0.66, 0.4, 0.86, 0.55, 0.3, 0.7, 0.46]
    x, i = 0, seed
    while x < p.w:
        bw = 18 + (i * 7) % 14
        bh = (base - 8) * hs[i % len(hs)]
        p.rect(x, base - bh, x + bw - 2, base, dark)
        for wy in range(int(base - bh + 5), int(base - 4), 7):
            for wx in range(int(x + 4), int(x + bw - 6), 6):
                if (wx + wy + i) % 3:
                    p.rect(wx, wy, wx + 2.5, wy + 3, lit)
        x += bw
        i += 1
    p.rect(0, base, p.w, p.h, dark)


def flag(p, x, y, w, h, kind):
    """Simplified flags drawn from rectangles and circles."""
    if kind == "UA":
        p.rect(x, y, x + w, y + h / 2, (0, 87, 183)); p.rect(x, y + h / 2, x + w, y + h, (255, 215, 0))
    elif kind == "RU":
        for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 43, 30)]):
            p.rect(x, y + i * h / 3, x + w, y + (i + 1) * h / 3, c)
    elif kind == "US":
        for i in range(7):
            p.rect(x, y + i * h / 7, x + w, y + (i + 0.5) * h / 7, (178, 34, 52))
            p.rect(x, y + (i + 0.5) * h / 7, x + w, y + (i + 1) * h / 7, WHITE)
        p.rect(x, y, x + w * 0.42, y + h * 0.54, (60, 59, 110))
    elif kind == "CN":
        p.rect(x, y, x + w, y + h, (222, 41, 16)); p.star(x + w * 0.2, y + h * 0.3, h * 0.18, (255, 222, 0), 5)
    elif kind == "JP":
        p.rect(x, y, x + w, y + h, WHITE); p.ell(x + w / 2, y + h / 2, h * 0.3, h * 0.3, (188, 0, 45))
    elif kind == "EU":
        p.rect(x, y, x + w, y + h, (0, 51, 153))
        for k in range(12):
            a = 2 * math.pi * k / 12
            p.star(x + w / 2 + h * 0.32 * math.cos(a), y + h / 2 + h * 0.32 * math.sin(a), h * 0.06, (255, 204, 0), 5)
    elif kind == "TR":
        p.rect(x, y, x + w, y + h, (227, 10, 23))
        p.ell(x + w * 0.38, y + h / 2, h * 0.25, h * 0.25, WHITE)
        p.ell(x + w * 0.43, y + h / 2, h * 0.2, h * 0.2, (227, 10, 23))
        p.star(x + w * 0.6, y + h / 2, h * 0.1, WHITE, 5)
    elif kind == "SA":
        p.rect(x, y, x + w, y + h, (0, 108, 53)); p.rect(x + w * 0.25, y + h * 0.62, x + w * 0.75, y + h * 0.67, WHITE)
        p.rect(x + w * 0.22, y + h * 0.3, x + w * 0.78, y + h * 0.48, (40, 140, 80))
    elif kind == "IN":
        for i, c in enumerate([(255, 153, 51), WHITE, (19, 136, 8)]):
            p.rect(x, y + i * h / 3, x + w, y + (i + 1) * h / 3, c)
        p.ell(x + w / 2, y + h / 2, h * 0.13, h * 0.13, None, (0, 0, 128), 1)
    elif kind == "NZ":
        p.rect(x, y, x + w, y + h, (1, 33, 105))
        for sx, sy in [(0.72, 0.3), (0.62, 0.55), (0.82, 0.5), (0.72, 0.78)]:
            p.star(x + w * sx, y + h * sy, h * 0.08, (200, 16, 46), 5)
    elif kind == "AU":
        p.rect(x, y, x + w, y + h, (1, 33, 105))
        p.star(x + w * 0.25, y + h * 0.72, h * 0.12, WHITE, 7)
        for sx, sy in [(0.75, 0.25), (0.65, 0.5), (0.85, 0.45), (0.75, 0.8)]:
            p.star(x + w * sx, y + h * sy, h * 0.07, WHITE, 7)
    elif kind == "KR":
        p.rect(x, y, x + w, y + h, WHITE); p.ell(x + w / 2, y + h / 2, h * 0.25, h * 0.25, (205, 46, 58))
        p.d.pieslice(p.p(x + w / 2 - h * 0.25, y + h / 2 - h * 0.25, x + w / 2 + h * 0.25, y + h / 2 + h * 0.25),
                     0, 180, fill=(0, 71, 160))
    elif kind == "UK":
        p.rect(x, y, x + w, y + h, (1, 33, 105))
        p.line([(x, y), (x + w, y + h)], WHITE, h * 0.18); p.line([(x + w, y), (x, y + h)], WHITE, h * 0.18)
        p.rect(x + w * 0.42, y, x + w * 0.58, y + h, WHITE); p.rect(x, y + h * 0.36, x + w, y + h * 0.64, WHITE)
        p.rect(x + w * 0.45, y, x + w * 0.55, y + h, (200, 16, 46)); p.rect(x, y + h * 0.41, x + w, y + h * 0.59, (200, 16, 46))
    elif kind == "IR":
        for i, c in enumerate([(35, 159, 64), WHITE, (218, 0, 0)]):
            p.rect(x, y + i * h / 3, x + w, y + (i + 1) * h / 3, c)
    elif kind == "IL":
        p.rect(x, y, x + w, y + h, WHITE)
        p.rect(x, y + h * 0.12, x + w, y + h * 0.24, (0, 56, 184)); p.rect(x, y + h * 0.76, x + w, y + h * 0.88, (0, 56, 184))
        p.poly([(x + w / 2, y + h * 0.32), (x + w / 2 + h * 0.17, y + h * 0.62), (x + w / 2 - h * 0.17, y + h * 0.62)], None, (0, 56, 184))
        p.poly([(x + w / 2, y + h * 0.68), (x + w / 2 + h * 0.17, y + h * 0.38), (x + w / 2 - h * 0.17, y + h * 0.38)], None, (0, 56, 184))
    elif kind == "NG":
        for i, c in enumerate([(0, 135, 81), WHITE, (0, 135, 81)]):
            p.rect(x + i * w / 3, y, x + (i + 1) * w / 3, y + h, c)
    elif kind == "ZA":
        p.rect(x, y, x + w, y + h / 2, (222, 56, 49)); p.rect(x, y + h / 2, x + w, y + h, (0, 35, 149))
        p.rect(x, y + h * 0.36, x + w, y + h * 0.64, WHITE); p.rect(x, y + h * 0.42, x + w, y + h * 0.58, (0, 122, 77))
        p.poly([(x, y), (x + w * 0.4, y + h / 2), (x, y + h)], (0, 0, 0))
    else:
        p.rect(x, y, x + w, y + h, (180, 180, 180))
    p.rect(x, y, x + w, y + h, None, (60, 60, 60), 0.6)


def pole_flag(p, x, base, kind, fw=30, fh=20):
    p.rect(x - 1, base - fh - 22, x + 1, base, (90, 90, 90))
    flag(p, x + 1, base - fh - 22, fw, fh, kind)


# ---------- scenes ----------

def missiles_night(p):
    """City at night, interceptor trails and bursts in the sky."""
    p.ell(p.w * 0.88, 18, 9, 9, (240, 236, 210))
    skyline(p, p.h - 10, 0)
    for i, (sx, ex) in enumerate([(0.05, 0.3), (0.35, 0.55), (0.7, 0.82)]):
        x0, y0, x1, y1 = p.w * sx, p.h * 0.85, p.w * ex, p.h * 0.18 + i * 6
        p.dashed(x0, y0, x1, y1, (255, 190, 90), 1.6)
        p.star(x1, y1, 12, (255, 150, 40), 9)
        p.star(x1, y1, 6, (255, 240, 160), 9)


def strike_building(p):
    """Apartment blocks hit by fire, ambulance in front."""
    p.rect(0, 0, p.w, p.h, (60, 66, 84))
    for bx, bw, bh in [(30, 70, 80), (120, 60, 64), (200, 80, 90), (300, 70, 70)]:
        if bx > p.w:
            continue
        p.rect(bx, p.h - 12 - bh, bx + bw, p.h - 12, (120, 124, 138))
        for wy in range(int(p.h - 12 - bh + 6), int(p.h - 18), 10):
            for wx in range(bx + 6, bx + bw - 8, 11):
                p.rect(wx, wy, wx + 5, wy + 5, (70, 74, 90))
    for fx, fy in [(150, p.h - 12 - 64), (240, p.h - 12 - 90)]:
        p.ell(fx, fy - 8, 16, 12, (90, 90, 96))
        p.poly([(fx - 9, fy + 2), (fx, fy - 18), (fx + 9, fy + 2)], (240, 110, 30))
        p.poly([(fx - 4, fy + 2), (fx, fy - 9), (fx + 4, fy + 2)], (255, 220, 90))
    p.rect(0, p.h - 12, p.w, p.h, (40, 42, 50))
    ax = p.w - 70
    p.rrect(ax, p.h - 30, ax + 46, p.h - 12, 3, WHITE)
    p.rect(ax + 18, p.h - 25, ax + 22, p.h - 15, (220, 30, 30)); p.rect(ax + 15, p.h - 22, ax + 25, p.h - 18, (220, 30, 30))
    p.ell(ax + 10, p.h - 12, 4, 4, INK); p.ell(ax + 36, p.h - 12, 4, 4, INK)


def climate_talks(p):
    """Globe, thermometer, clock past deadline, stack of drafts."""
    p.rect(0, 0, p.w, p.h, (212, 232, 226))
    cx, cy = p.w * 0.18, p.h * 0.5
    p.ell(cx, cy, 34, 34, (64, 132, 200))
    p.poly([(cx - 18, cy - 20), (cx + 4, cy - 26), (cx + 8, cy - 6), (cx - 8, cy + 6), (cx - 22, cy - 4)], (90, 170, 100))
    p.poly([(cx + 10, cy + 6), (cx + 26, cy + 2), (cx + 20, cy + 22), (cx + 8, cy + 20)], (90, 170, 100))
    tx = p.w * 0.4
    p.rrect(tx - 6, 18, tx + 6, p.h - 34, 6, WHITE, INK, 1.2)
    p.rect(tx - 2.5, 36, tx + 2.5, p.h - 30, (200, 40, 40))
    p.ell(tx, p.h - 24, 11, 11, (200, 40, 40), INK, 1.2)
    kx, ky = p.w * 0.62, p.h * 0.48
    p.ell(kx, ky, 30, 30, WHITE, INK, 2.5)
    for k in range(12):
        a = math.pi * 2 * k / 12
        p.line([(kx + 24 * math.cos(a), ky + 24 * math.sin(a)), (kx + 27 * math.cos(a), ky + 27 * math.sin(a))], INK, 1.2)
    p.line([(kx, ky), (kx, ky - 21)], INK, 2.2); p.line([(kx, ky), (kx + 13, ky + 7)], INK, 2.2)
    dx = p.w * 0.8
    for k in range(3):
        p.rect(dx - 22 + k * 5, 22 + k * 6, dx + 18 + k * 5, 78 + k * 6, WHITE, INK, 1)
        for ly in range(32 + k * 6, 72 + k * 6, 7):
            p.line([(dx - 16 + k * 5, ly), (dx + 12 + k * 5, ly)], (150, 150, 150), 1)


def seismo(p):
    """Seismograph trace over tilted houses."""
    p.rect(0, 0, p.w, p.h, (240, 232, 214))
    pts = []
    for i in range(0, int(p.w) + 1, 3):
        amp = 30 * math.exp(-((i - p.w * 0.45) / (p.w * 0.12)) ** 2) + 2
        pts.append((i, p.h * 0.38 + amp * math.sin(i * 0.9)))
    p.line(pts, (190, 30, 30), 1.6)
    p.rect(0, p.h * 0.78, p.w, p.h, (150, 120, 90))
    for k, hx in enumerate([p.w * 0.6, p.w * 0.78]):
        base = p.h * 0.78
        p.rect(hx, base - 26, hx + 34, base, (250, 246, 236), INK, 1)
        p.poly([(hx - 4, base - 26), (hx + 17, base - 42), (hx + 38, base - 26)], (170, 60, 50))
        p.rect(hx + 12, base - 14, hx + 21, base, (110, 80, 60))
    p.line([(p.w * 0.3, p.h * 0.8), (p.w * 0.34, p.h * 0.9), (p.w * 0.31, p.h * 0.95), (p.w * 0.35, p.h)], INK, 1.5)


def talks(p, flags):
    """Two flags on poles either side of a table."""
    p.rect(0, 0, p.w, p.h, (232, 228, 218))
    p.rect(0, p.h * 0.72, p.w, p.h, (176, 150, 120))
    p.rect(p.w * 0.2, p.h * 0.55, p.w * 0.8, p.h * 0.62, (120, 84, 54))
    n = len(flags)
    for i, k in enumerate(flags):
        fx = p.w * (0.08 + 0.84 * i / max(1, n - 1)) - (34 if i == n - 1 and n > 1 else 0)
        pole_flag(p, fx, p.h * 0.72, k, 32, 21)
    p.ell(p.w * 0.42, p.h * 0.42, 7, 7, (90, 70, 60)); p.rrect(p.w * 0.42 - 9, p.h * 0.48, p.w * 0.42 + 9, p.h * 0.6, 4, (50, 60, 90))
    p.ell(p.w * 0.58, p.h * 0.42, 7, 7, (200, 160, 130)); p.rrect(p.w * 0.58 - 9, p.h * 0.48, p.w * 0.58 + 9, p.h * 0.6, 4, (70, 70, 74))


def tanker(p):
    """Tanker at sea with a fire plume."""
    p.rect(0, 0, p.w, p.h * 0.62, (196, 214, 228))
    p.rect(0, p.h * 0.62, p.w, p.h, (40, 96, 150))
    for k in range(0, int(p.w), 22):
        p.arc(k + 11, p.h * 0.8, 8, 200, 340, (150, 190, 220), 1)
    hx = p.w * 0.18
    p.poly([(hx, p.h * 0.5), (hx + p.w * 0.62, p.h * 0.5), (hx + p.w * 0.58, p.h * 0.66), (hx + 6, p.h * 0.66)], (150, 40, 36))
    p.rect(hx + p.w * 0.48, p.h * 0.3, hx + p.w * 0.58, p.h * 0.5, WHITE)
    for k in range(4):
        p.rect(hx + 14 + k * p.w * 0.1, p.h * 0.45, hx + 10 + (k + 1) * p.w * 0.1, p.h * 0.5, (90, 90, 96))
    fx = hx + p.w * 0.22
    p.ell(fx + 10, p.h * 0.22, 20, 12, (110, 110, 116))
    p.poly([(fx - 10, p.h * 0.48), (fx, p.h * 0.26), (fx + 10, p.h * 0.48)], (240, 110, 30))


def drone_sea(p):
    """Drone over water with a question-mark style dashed path (claim)."""
    p.rect(0, 0, p.w, p.h, (200, 216, 228))
    p.rect(0, p.h * 0.7, p.w, p.h, (52, 104, 150))
    cx, cy = p.w * 0.5, p.h * 0.36
    p.poly([(cx - 40, cy), (cx + 40, cy), (cx + 6, cy + 5), (cx - 6, cy + 5)], (70, 74, 84))
    p.rrect(cx - 26, cy - 6, cx + 24, cy + 4, 4, (90, 94, 104))
    p.poly([(cx + 20, cy - 4), (cx + 30, cy - 14), (cx + 32, cy - 2)], (70, 74, 84))
    p.dashed(cx, cy + 8, cx + 30, p.h * 0.7, (200, 40, 40), 1.4)


def plane(p, sky=SKY):
    p.rect(0, 0, p.w, p.h, sky)
    p.rect(0, p.h * 0.8, p.w, p.h, (120, 124, 130))
    for k in range(0, int(p.w), 26):
        p.rect(k, p.h * 0.89, k + 12, p.h * 0.91, WHITE)
    cx, cy = p.w * 0.5, p.h * 0.45
    p.rrect(cx - 52, cy - 6, cx + 52, cy + 6, 6, WHITE, (90, 90, 96), 1)
    p.poly([(cx - 8, cy), (cx + 14, cy), (cx - 14, cy + 26), (cx - 26, cy + 26)], (200, 200, 206))
    p.poly([(cx - 46, cy - 4), (cx - 38, cy - 4), (cx - 50, cy - 22), (cx - 56, cy - 22)], (200, 40, 40))
    for k in range(6):
        p.ell(cx - 26 + k * 10, cy - 1, 1.6, 1.6, (60, 90, 140))


def cricket(p):
    p.rect(0, 0, p.w, p.h, (200, 226, 200))
    for k in range(0, int(p.w), 30):
        p.rect(k, 0, k + 15, p.h, (186, 214, 186))
    p.rect(p.w * 0.42, p.h * 0.2, p.w * 0.58, p.h, (222, 204, 160))
    for k in range(3):
        p.rect(p.w * 0.47 + k * 5, p.h * 0.3, p.w * 0.47 + k * 5 + 2, p.h * 0.62, WHITE)
    p.line([(p.w * 0.7, p.h * 0.85), (p.w * 0.84, p.h * 0.25)], (196, 150, 90), 7)
    p.line([(p.w * 0.84, p.h * 0.25), (p.w * 0.86, p.h * 0.12)], (60, 50, 40), 3)
    p.ell(p.w * 0.28, p.h * 0.36, 6, 6, (180, 20, 30))


def racecar(p):
    p.rect(0, 0, p.w, p.h, (30, 30, 44))
    for k in range(0, int(p.w), 9):
        p.ell(k + 4, 8 + (k * 7) % 14, 1.2, 1.2, WIN)
    p.rect(0, p.h * 0.62, p.w, p.h, (70, 70, 78))
    for k in range(0, int(p.w), 20):
        p.rect(k, p.h * 0.62, k + 10, p.h * 0.66, (220, 40, 40) if (k // 20) % 2 else WHITE)
    cx, cy = p.w * 0.5, p.h * 0.72
    p.poly([(cx - 50, cy), (cx + 50, cy), (cx + 40, cy - 9), (cx - 10, cy - 12), (cx - 46, cy - 10)], (0, 160, 150))
    p.rect(cx - 54, cy - 16, cx - 46, cy - 6, (0, 160, 150)); p.rect(cx + 44, cy - 4, cx + 56, cy, (0, 160, 150))
    p.ell(cx - 6, cy - 12, 5, 4, INK)
    p.ell(cx - 34, cy + 2, 7, 7, INK); p.ell(cx + 32, cy + 2, 7, 7, INK)


def chart_down(p, color=(220, 50, 50)):
    p.rect(0, 0, p.w, p.h, (24, 30, 44))
    for k in range(1, 4):
        p.line([(0, p.h * k / 4), (p.w, p.h * k / 4)], (50, 58, 76), 1)
    vals = [0.3, 0.25, 0.35, 0.3, 0.45, 0.42, 0.55, 0.6, 0.58, 0.72, 0.8]
    pts = [(8 + i * (p.w - 16) / (len(vals) - 1), 8 + v * (p.h - 20)) for i, v in enumerate(vals)]
    for i, (x, y) in enumerate(pts):
        p.rect(x - 3, y - 6, x + 3, y + 6, color if i % 3 else (60, 170, 110))
    p.line(pts, color, 2)
    x, y = pts[-1]
    p.poly([(x - 7, y - 4), (x + 7, y - 4), (x, y + 6)], color)


def robot(p):
    p.rect(0, 0, p.w, p.h, (220, 226, 236))
    cx, cy = p.w * 0.5, p.h * 0.52
    p.rrect(cx - 22, cy - 30, cx + 22, cy, 6, (150, 156, 170), INK, 1)
    p.ell(cx - 9, cy - 16, 5, 5, (220, 40, 40)); p.ell(cx + 9, cy - 16, 5, 5, (220, 40, 40))
    p.line([(cx, cy - 30), (cx, cy - 40)], INK, 1.5); p.ell(cx, cy - 42, 3, 3, (220, 40, 40))
    p.rrect(cx - 28, cy + 2, cx + 28, cy + 34, 4, (120, 126, 140), INK, 1)
    p.ell(cx + 70, cy, 22, 22, None, (200, 40, 40), 3)
    p.line([(cx + 55, cy - 15), (cx + 85, cy + 15)], (200, 40, 40), 3)
    p.line([(cx - 92, cy - 14), (cx - 52, cy - 14)], INK, 1); p.line([(cx - 92, cy - 4), (cx - 52, cy - 4)], INK, 1)


def bottle(p):
    p.rect(0, 0, p.w, p.h, (234, 226, 236))
    for k, bx in enumerate([p.w * 0.35, p.w * 0.5, p.w * 0.65]):
        p.rrect(bx - 10, p.h * 0.35, bx + 10, p.h * 0.88, 4, (110, 150, 90) if k != 1 else (150, 110, 60), INK, 1)
        p.rect(bx - 4, p.h * 0.18, bx + 4, p.h * 0.36, (110, 150, 90) if k != 1 else (150, 110, 60), INK, 1)
        p.rect(bx - 8, p.h * 0.5, bx + 8, p.h * 0.66, WHITE)
    p.line([(p.w * 0.47, p.h * 0.53), (p.w * 0.53, p.h * 0.63)], (200, 30, 30), 1.5)
    p.line([(p.w * 0.53, p.h * 0.53), (p.w * 0.47, p.h * 0.63)], (200, 30, 30), 1.5)


def fire_plant(p):
    p.rect(0, 0, p.w, p.h, (70, 60, 64))
    p.rect(0, p.h * 0.8, p.w, p.h, (50, 44, 44))
    for k, sx in enumerate([0.2, 0.32, 0.44]):
        p.rect(p.w * sx, p.h * 0.2, p.w * sx + 10, p.h * 0.8, (130, 120, 116))
    p.rect(p.w * 0.5, p.h * 0.45, p.w * 0.85, p.h * 0.8, (110, 104, 100))
    for k, fx in enumerate([0.58, 0.7, 0.8]):
        p.poly([(p.w * fx - 12, p.h * 0.48), (p.w * fx, p.h * (0.12 + 0.06 * k)), (p.w * fx + 12, p.h * 0.48)], (240, 110, 30))
        p.poly([(p.w * fx - 6, p.h * 0.48), (p.w * fx, p.h * 0.3), (p.w * fx + 6, p.h * 0.48)], (255, 220, 90))


def gavel(p):
    p.rect(0, 0, p.w, p.h, (226, 214, 196))
    p.rect(p.w * 0.25, p.h * 0.74, p.w * 0.75, p.h * 0.84, (120, 80, 50))
    p.line([(p.w * 0.42, p.h * 0.66), (p.w * 0.7, p.h * 0.2)], (140, 94, 58), 4)
    p.poly([(p.w * 0.3, p.h * 0.5), (p.w * 0.42, p.h * 0.36), (p.w * 0.56, p.h * 0.5), (p.w * 0.44, p.h * 0.64)], (110, 70, 40))
    for k in range(4):
        p.rect(p.w * 0.08, p.h * (0.2 + k * 0.17), p.w * 0.2, p.h * (0.2 + k * 0.17) + 4, (170, 160, 140))


def train(p):
    p.rect(0, 0, p.w, p.h, (214, 222, 214))
    p.rect(0, p.h * 0.8, p.w, p.h, (140, 120, 100))
    p.line([(0, p.h * 0.8), (p.w, p.h * 0.8)], (90, 90, 90), 2)
    for k, (dx, ang) in enumerate([(10, 0), (70, 0), (130, -10), (175, 18)]):
        if dx > p.w - 20:
            break
        cx, cy = dx + 28, p.h * 0.6
        a = math.radians(ang)
        pts = [(-26, -14), (26, -14), (26, 14), (-26, 14)]
        p.poly([(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts],
               [(120, 60, 40), (90, 90, 110), (130, 70, 40), (70, 80, 100)][k])


def boat(p):
    p.rect(0, 0, p.w, p.h * 0.5, (206, 222, 230))
    p.rect(0, p.h * 0.5, p.w, p.h, (80, 110, 100))
    p.poly([(p.w * 0.32, p.h * 0.55), (p.w * 0.68, p.h * 0.66), (p.w * 0.64, p.h * 0.76), (p.w * 0.3, p.h * 0.64)], (110, 74, 44))
    for k in range(0, int(p.w), 24):
        p.arc(k + 12, p.h * 0.88, 8, 200, 340, (150, 180, 170), 1)
    for k in range(3):
        p.ell(p.w * (0.2 + 0.3 * k), p.h * 0.72, 3, 3, (220, 120, 30))


def ballot(p, color=(36, 84, 160)):
    p.rect(0, 0, p.w, p.h, (226, 230, 238))
    bx, by = p.w * 0.5, p.h * 0.62
    p.rect(bx - 36, by - 18, bx + 36, by + 26, color, INK, 1)
    p.rect(bx - 22, by - 21, bx + 22, by - 17, INK)
    p.rect(bx - 12, by - 52, bx + 12, by - 18, WHITE, INK, 1)
    p.line([(bx - 6, by - 36), (bx - 1, by - 30), (bx + 7, by - 44)], (30, 140, 60), 2)


def space(p):
    p.rect(0, 0, p.w, p.h, (10, 12, 26))
    for k in range(40):
        p.ell((k * 37) % p.w, (k * 23) % p.h, 0.8, 0.8, WHITE)
    p.ell(p.w * 0.7, p.h * 0.55, 30, 30, (150, 140, 130))
    p.ell(p.w * 0.66, p.h * 0.5, 5, 5, (120, 112, 104)); p.ell(p.w * 0.76, p.h * 0.62, 4, 4, (120, 112, 104))
    p.rect(p.w * 0.25 - 5, p.h * 0.35 - 4, p.w * 0.25 + 5, p.h * 0.35 + 4, (200, 180, 90))
    p.rect(p.w * 0.25 - 26, p.h * 0.35 - 2, p.w * 0.25 - 6, p.h * 0.35 + 2, (60, 90, 170))
    p.rect(p.w * 0.25 + 6, p.h * 0.35 - 2, p.w * 0.25 + 26, p.h * 0.35 + 2, (60, 90, 170))


def football(p):
    p.rect(0, 0, p.w, p.h, (60, 140, 70))
    for k in range(0, int(p.w), 24):
        p.rect(k, 0, k + 12, p.h, (70, 152, 80))
    p.line([(p.w / 2, 0), (p.w / 2, p.h)], WHITE, 1.5)
    p.ell(p.w / 2, p.h / 2, 18, 18, None, WHITE, 1.5)
    p.ell(p.w * 0.7, p.h * 0.6, 9, 9, WHITE, INK, 1)
    p.ell(p.w * 0.7, p.h * 0.6, 3, 3, INK)


def coins(p):
    p.rect(0, 0, p.w, p.h, (30, 34, 46))
    for k in range(4):
        p.ell(p.w * 0.2 + k * 8, p.h * 0.75 - k * 7, 16, 6, (230, 170, 40), (150, 100, 20), 1)
    p.ell(p.w * 0.36, p.h * 0.4, 20, 20, (240, 160, 30), (160, 100, 20), 1.5)
    chart = [(p.w * 0.55, p.h * 0.25), (p.w * 0.65, p.h * 0.35), (p.w * 0.72, p.h * 0.3), (p.w * 0.84, p.h * 0.62)]
    p.line(chart, (230, 60, 60), 2.2)
    x, y = chart[-1]
    p.poly([(x - 7, y - 6), (x + 6, y - 2), (x + 2, y + 8)], (230, 60, 60))


def hospital(p):
    p.rect(0, 0, p.w, p.h, (226, 236, 240))
    p.rect(p.w * 0.25, p.h * 0.25, p.w * 0.75, p.h * 0.92, WHITE, INK, 1)
    p.rect(p.w * 0.47, p.h * 0.32, p.w * 0.53, p.h * 0.56, (200, 30, 40))
    p.rect(p.w * 0.41, p.h * 0.41, p.w * 0.59, p.h * 0.47, (200, 30, 40))
    for k in range(4):
        p.rect(p.w * 0.3 + k * p.w * 0.11, p.h * 0.66, p.w * 0.3 + k * p.w * 0.11 + 10, p.h * 0.76, (150, 190, 220))


def protest(p, colour=(200, 40, 40)):
    p.rect(0, 0, p.w, p.h, (232, 228, 222))
    for k in range(9):
        x = 14 + k * (p.w - 28) / 8
        p.ell(x, p.h * 0.62, 6, 6, (80 + k * 10, 60, 50))
        p.rrect(x - 7, p.h * 0.7, x + 7, p.h, 4, [(60, 80, 130), (130, 60, 60), (60, 110, 80)][k % 3])
    for k, x in enumerate([0.2, 0.5, 0.8]):
        p.line([(p.w * x, p.h * 0.55), (p.w * x, p.h * 0.3)], (90, 70, 50), 1.5)
        p.rect(p.w * x - 18, p.h * 0.12, p.w * x + 18, p.h * 0.32, WHITE if k != 1 else colour, INK, 1)


def cyclone(p):
    """Satellite-style spiral over ocean with a small island."""
    p.rect(0, 0, p.w, p.h, (36, 92, 140))
    cx, cy = p.w * 0.45, p.h * 0.5
    for arm in range(3):
        pts = []
        for k in range(60):
            t = k / 59
            a = arm * 2 * math.pi / 3 + t * 3.2
            r = 4 + t * 44
            pts.append((cx + r * math.cos(a) * 1.3, cy + r * math.sin(a)))
        p.line(pts, (236, 242, 248), 5)
    p.ell(cx, cy, 4, 4, (36, 92, 140))
    p.ell(p.w * 0.84, p.h * 0.72, 12, 6, (214, 196, 140))
    p.ell(p.w * 0.84, p.h * 0.7, 6, 3, (80, 150, 90))


SCENES = {
    "cyclone": cyclone,
    "missiles_night": missiles_night, "strike_building": strike_building, "climate_talks": climate_talks,
    "seismo": seismo, "tanker": tanker, "drone_sea": drone_sea, "plane": plane, "cricket": cricket,
    "racecar": racecar, "chart_down": chart_down, "robot": robot, "bottle": bottle, "fire_plant": fire_plant,
    "gavel": gavel, "train": train, "boat": boat, "ballot": ballot, "space": space, "football": football,
    "coins": coins, "hospital": hospital, "protest": protest,
}


def draw(img, spec, box, s):
    """spec: scene name, or (scene name, args...). Flags-on-poles scenes: ("talks", ["UA", "US"])."""
    name, args = (spec, ()) if isinstance(spec, str) else (spec[0], spec[1:])
    x, y, w, h = box
    pen = Pen(w, h, s, (230, 230, 230))
    (talks if name == "talks" else SCENES[name])(pen, *args)
    img.paste(pen.img, (round(x * s), round(y * s)))
