"""Render entry.png: the world news of Saturday 21 November 2026 as one newspaper-style page.

Deterministic: fixed fonts, fixed data, no clock, no randomness, no network. Needs Pillow.
Run: python make_image.py  (writes entry.png next to this file)
Every illustration is drawn here from Pillow shapes; the map uses Natural Earth 1:110m land
(public domain), stored in data/ne_110m_land.geojson.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from stories import BRIEFS, CARDS, DATECHECK, DECK, FOOTER, LEADS, NUMBERS, REGIONS
import art

ROOT = Path(__file__).resolve().parent
S = 3  # supersampling; all coordinates below are in 1024-px units
W = H = 1024
M = 16

PAPER = (247, 243, 233)
INK = (24, 24, 28)
GREY = (72, 72, 80)
LIGHT = (205, 198, 182)
RED = (178, 34, 34)
CONF = {"2+": ("2+ OUTLETS", (30, 110, 60)), "OFF": ("OFFICIAL", (36, 84, 160)),
        "ONE": ("ONE OUTLET", (150, 100, 20)), "CLAIM": ("CLAIM", RED)}


def serif(size, wght=700, opsz=None):
    f = ImageFont.truetype(str(ROOT / "fonts" / "SourceSerif4-Variable.ttf"), round(size * S))
    f.set_variation_by_axes([wght, min(60, max(8, opsz or size))])
    return f


def sans(name, size):
    return ImageFont.truetype(str(ROOT / "fonts" / name), round(size * S))


F = {
    "kick": sans("BarlowCondensed-Bold.ttf", 14),
    "mast": serif(76, 700, 60),
    "deck": serif(17, 400, 17),
    "num": serif(24, 700, 24),
    "numcap": sans("Barlow-Medium.ttf", 10.5),
    "reg": sans("BarlowCondensed-Bold.ttf", 12),
    "tag": sans("BarlowCondensed-ExtraBold.ttf", 15),
    "tags": sans("BarlowCondensed-ExtraBold.ttf", 11.5),
    "lab": sans("BarlowCondensed-Bold.ttf", 12),
    "labs": sans("BarlowCondensed-Bold.ttf", 10.5),
    "lhead": serif(21, 700, 21),
    "shead": serif(14.5, 700, 14),
    "lbody": sans("Barlow-Medium.ttf", 12),
    "sbody": sans("Barlow-Medium.ttf", 10.5),
    "conf": sans("BarlowCondensed-Bold.ttf", 9),
    "sect": sans("BarlowCondensed-ExtraBold.ttf", 13),
    "brief": sans("Barlow-Medium.ttf", 10.5),
    "briefb": sans("Barlow-SemiBold.ttf", 10.5),
    "pin": sans("BarlowCondensed-Bold.ttf", 9),
    "foot": sans("Barlow-Medium.ttf", 9.5),
    "dc": sans("Barlow-Medium.ttf", 10.5),
    "dcb": sans("BarlowCondensed-ExtraBold.ttf", 13),
}


def sc(*v):
    return [round(x * S) for x in v]


def tw(d, text, f):
    return d.textlength(text, font=f) / S


def text(d, x, y, s, f, fill, anchor="la"):
    d.text((round(x * S), round(y * S)), s, font=f, fill=fill, anchor=anchor)


def wrap(d, s, f, width, first_width=None):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if tw(d, trial, f) <= (first_width if first_width and not lines else width):
            cur = trial
        else:
            assert cur, f"word too wide: {word}"
            lines.append(cur)
            cur = word
    return lines + [cur]


def block(d, x, y, s, f, width, fill, lh, max_lines):
    lines = wrap(d, s, f, width)
    assert len(lines) <= max_lines, f"overflow ({len(lines)} > {max_lines} lines): {s}"
    for i, line in enumerate(lines):
        text(d, x, y + i * lh, line, f, fill)
    return y + len(lines) * lh


def fit(d, x, y, s, f, width, fill, anchor="la"):
    assert tw(d, s, f) <= width + 0.5, f"too wide ({tw(d, s, f):.0f} > {width:.0f}): {s}"
    text(d, x, y, s, f, fill, anchor)


def rich(d, x, y, parts, width):
    """One line of (text, font, colour) runs; asserts it fits."""
    total = sum(tw(d, s, f) for s, f, _ in parts)
    assert total <= width + 0.5, f"line too wide ({total:.0f} > {width:.0f}): {parts}"
    for s, f, c in parts:
        text(d, x, y, s, f, c)
        x += tw(d, s, f)


def badge(d, x, y, s, f, fg, bg, pad=4, h=None, anchor="l"):
    w = tw(d, s, f) + 2 * pad
    h = h or f.size / S * 1.25
    if anchor == "r":
        x -= w
    d.rectangle(sc(x, y, x + w, y + h), fill=bg)
    text(d, x + pad, y + h / 2 + 0.5, s, f, fg, "lm")
    return w


def conf_badge(d, xr, y, key):
    label, col = CONF[key]
    f = F["conf"]
    w = tw(d, label, f) + 8
    d.rounded_rectangle(sc(xr - w, y, xr, y + 12), radius=3 * S, outline=col, width=S, fill=PAPER)
    text(d, xr - w / 2, y + 6.5, label, f, col, "mm")
    return w


def region_col(r):
    return dict((k, c) for k, c, _ in REGIONS)[r]


def num_dot(d, x, y, n, col, r=7, f=None):
    d.ellipse(sc(x - r, y - r, x + r, y + r), fill=col, outline=PAPER, width=S)
    text(d, x, y + 0.5, str(n), f or F["pin"], (255, 255, 255), "mm")


def card(img, d, x, y, w, h_art, story, big):
    """Illustration + label + headline + fact line + source. Returns bottom y."""
    col = region_col(story["region"])
    art.draw(img, story["art"], (x, y, w, h_art), S)
    d = ImageDraw.Draw(img)
    # overlay tag on the illustration
    ft = F["tag"] if big else F["tags"]
    th = 20 if big else 15
    tag_w = tw(d, story["tag"], ft) + 10
    assert tag_w <= w - 8, f"tag too wide: {story['tag']}"
    d.rectangle(sc(x, y + h_art - th, x + tag_w, y + h_art), fill=col)
    text(d, x + 5, y + h_art - th / 2 + 0.5, story["tag"], ft, (255, 255, 255), "lm")
    yy = y + h_art + 5
    fl = F["lab"] if big else F["labs"]
    num_dot(d, x + 7, yy + 6, story["n"], col, 7 if big else 6.5)
    bw = conf_badge(d, x + w, yy, story["conf"])
    fit(d, x + 18, yy, story["label"], fl, w - 18 - bw - 4, col)
    yy += 16 if big else 15
    if big:
        yy = block(d, x, yy, story["head"], F["lhead"], w, INK, 23, 2) + 3
        yy = block(d, x, yy, story["body"] + f" ({story['src']})", F["lbody"], w, GREY, 15, 3)
    else:
        yy = block(d, x, yy, story["head"], F["shead"], w, INK, 16.5, 2) + 2
        yy = block(d, x, yy, story["body"] + f" ({story['src']})", F["sbody"], w, GREY, 13, 2)
    return yy


def load_land():
    gj = json.loads((ROOT / "data" / "ne_110m_land.geojson").read_text(encoding="utf-8"))
    polys = []
    for feat in gj["features"]:
        g = feat["geometry"]
        for poly in ([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]):
            polys.append(poly[0])  # outer ring; 110m land has no lakes worth drawing
    return polys


def world_map(img, box, pins):
    x0, y0, w, h = box
    lon0, lon1, lat0, lat1 = -170, 190, -50, 75  # shifted so New Zealand and the Pacific stay whole

    def proj(lon, lat):
        return (lon - lon0) / (lon1 - lon0) * w * S, (lat1 - lat) / (lat1 - lat0) * h * S

    tile = Image.new("RGB", (round(w * S), round(h * S)), (214, 226, 232))
    t = ImageDraw.Draw(tile)
    for ring in load_land():
        for shift in (0, 360):
            t.polygon([tuple(round(v) for v in proj(lon + shift, lat)) for lon, lat in ring],
                      fill=(232, 222, 196), outline=(190, 178, 150))
    img.paste(tile, (round(x0 * S), round(y0 * S)))
    d = ImageDraw.Draw(img)
    d.rectangle(sc(x0, y0, x0 + w, y0 + h), outline=LIGHT, width=S)
    for n, lon, lat, region, dx, dy in pins:
        px, py = proj(lon if lon >= lon0 else lon + 360, lat)
        px, py = x0 + px / S, y0 + py / S
        if dx or dy:
            d.line(sc(px, py, px + dx, py + dy), fill=INK, width=S)
            d.ellipse(sc(px - 1.5, py - 1.5, px + 1.5, py + 1.5), fill=INK)
        num_dot(d, px + dx, py + dy, n, region_col(region), 6.5)


def render():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)
    total = len(LEADS) + len(CARDS) + len(BRIEFS)
    assert total == sum(n for _, _, n in REGIONS), "region tally must match story count"

    # Top line + masthead
    text(d, M, 9, "ONE PAGE, ONE DAY", F["kick"], RED)
    right = f"{total} STORIES FROM 7 REGIONS  ·  ALL REPORTED SATURDAY 21 NOVEMBER 2026"
    text(d, W - M, 9, right, F["kick"], INK, "ra")
    d.line(sc(M, 27, W - M, 27), fill=INK, width=2 * S)
    mast = "Saturday 21 November 2026"
    fit(d, W / 2, 28, mast, F["mast"], W - 2 * M, INK, "ma")
    fit(d, W / 2, 120, DECK, F["deck"], W - 2 * M, (60, 60, 66), "ma")
    d.line(sc(M, 145, W - M, 145), fill=INK, width=S)
    d.line(sc(M, 148, W - M, 148), fill=INK, width=S)

    # Key numbers strip
    y = 154
    cw = (W - 2 * M) / len(NUMBERS)
    for i, (num, cap) in enumerate(NUMBERS):
        x = M + i * cw
        d.rectangle(sc(x, y, x + 3, y + 40), fill=RED)
        fit(d, x + 9, y - 3, num, F["num"], cw - 14, INK)
        lines = wrap(d, cap, F["numcap"], cw - 14)
        assert len(lines) <= 2, cap
        for j, ln in enumerate(lines):
            text(d, x + 9, y + 23 + j * 11, ln, F["numcap"], GREY)

    # Region tally bar
    y = 205
    x = M
    for i, (name, col, n) in enumerate(REGIONS):
        seg = (W - 2 * M) * n / total
        x1 = W - M if i == len(REGIONS) - 1 else x + seg
        d.rectangle(sc(x, y, x1 - 1, y + 15), fill=col)
        lab = f"{name.upper()} {n}"
        if tw(d, lab, F["reg"]) > x1 - x - 6:
            lab = str(n)
        fit(d, (x + x1) / 2, y + 8, lab, F["reg"], x1 - x - 4, (255, 255, 255), "mm")
        x = x1

    # Three lead cards
    y = 228
    gap = 14
    lw = (W - 2 * M - 2 * gap) / 3
    bottoms = []
    for i, st in enumerate(LEADS):
        bottoms.append(card(img, d, M + i * (lw + gap), y, lw, 104, st, True))
        d = ImageDraw.Draw(img)
    lead_bottom = 452
    assert max(bottoms) <= lead_bottom - 4, f"lead overflow {max(bottoms)}"
    d.line(sc(M, lead_bottom, W - M, lead_bottom), fill=LIGHT, width=S)

    # Ten smaller cards, 2 rows of 5
    gap = 10
    sw = (W - 2 * M - 4 * gap) / 5
    row_h = 146
    for i, st in enumerate(CARDS):
        cx = M + (i % 5) * (sw + gap)
        cy = lead_bottom + 7 + (i // 5) * row_h
        b = card(img, d, cx, cy, sw, 56, st, False)
        d = ImageDraw.Draw(img)
        assert b <= cy + row_h - 4, f"card {st['n']} overflow {b}"
    y = lead_bottom + 7 + 2 * row_h
    d.line(sc(M, y, W - M, y), fill=INK, width=S)

    # Map + also-list
    y += 6
    text(d, M, y, "WHERE IT HAPPENED", F["sect"], INK)
    map_w, map_h = 300, 150
    pins = [(st["n"], *st["pin"], st["region"], *st.get("off", (0, 0))) for st in LEADS + CARDS if st["pin"]]
    world_map(img, (M, y + 18, map_w, map_h), pins)
    d = ImageDraw.Draw(img)
    text(d, M, y + 18 + map_h + 3, "Numbered pins match the stories above (8 has no place).", F["foot"], GREY)

    lx = M + map_w + 16
    text(d, lx, y, f"ALSO ON SATURDAY 21 NOVEMBER  —  {len(BRIEFS)} MORE STORIES", F["sect"], INK)
    colw = (W - M - lx - 12) / 2
    per_col = (len(BRIEFS) + 1) // 2
    lh = 14
    for i, (n, place, line, src, region) in enumerate(BRIEFS):
        bx = lx + (i // per_col) * (colw + 12)
        by = y + 19 + (i % per_col) * lh
        col = region_col(region)
        d.rectangle(sc(bx, by + 1, bx + 15, by + 13), fill=col)
        text(d, bx + 7.5, by + 7.5, str(n), F["pin"], (255, 255, 255), "mm")
        rich(d, bx + 19, by, [(place + " ", F["briefb"], INK), (line + " ", F["brief"], INK),
                               (f"({src})", F["brief"], GREY)], colw - 19)
    list_bottom = y + 19 + per_col * lh
    y = max(list_bottom, y + 18 + map_h + 14) + 3

    # Date check
    dc_h = 1024 - 22 - y
    d.rectangle(sc(M, y, W - M, y + dc_h), outline=RED, width=S, fill=(251, 248, 240))
    text(d, M + 8, y + 5, "DATE CHECK", F["dcb"], RED)
    lab_w = tw(d, "DATE CHECK", F["dcb"]) + 8  # label sits inline at the start of line 1
    lines = wrap(d, DATECHECK, F["dc"], W - 2 * M - 16, W - 2 * M - 16 - lab_w)
    assert 6 + 13.5 * len(lines) + 2 <= dc_h, f"date check overflow: {len(lines)} lines in {dc_h}px"
    for j, ln in enumerate(lines):
        text(d, M + 8 + (lab_w if j == 0 else 0), y + 6.5 + j * 13.5, ln, F["dc"], INK)
    fit(d, W / 2, 1024 - 17, FOOTER, F["foot"], W - 2 * M, GREY, "ma")

    out = img.resize((W, H), Image.LANCZOS)
    out.save(ROOT / "entry.png", optimize=True)
    out.resize((300, 300), Image.LANCZOS).save(ROOT / "preview-300.png")
    size = (ROOT / "entry.png").stat().st_size
    assert size <= 1024 * 1024, f"entry.png too big: {size}"
    print(f"entry.png {W}x{H}, {size} bytes, {total} stories")


if __name__ == "__main__":
    render()
