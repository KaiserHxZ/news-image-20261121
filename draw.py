#!/usr/bin/env python3
"""Draw the news-image-20261121 entry: a one-page newspaper front page
summing up the world's news of Saturday 21 November 2026.

All text is drawn in code with DejaVu fonts (no AI-generated text, so
nothing can garble). Output is a deterministic 1024x1024 PNG.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 235)
INK = (20, 20, 20)
RED = (179, 39, 30)
NAVY = (31, 51, 80)
GRAY = (110, 108, 100)
RULE = (60, 60, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines left-aligned; returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.18)


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- pictograms
def globe_icon(d, x, y, s, color):
    """White globe (circle + meridians) on a coloured tile."""
    d.ellipse([x, y, x + s, y + s], fill=color)
    cx, cy, r = x + s / 2, y + s / 2, s * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(255, 255, 255), width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=3)


def cyclone_icon(d, x, y, s, color):
    """White cyclone swirl (arcs) on a coloured tile."""
    d.ellipse([x, y, x + s, y + s], fill=color)
    cx, cy = x + s / 2, y + s / 2
    for i, r in enumerate((34, 25, 16)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=30 + i * 120,
              end=300 + i * 120, fill=(255, 255, 255), width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))


def cricket_icon(d, x, y, s, color):
    """White cricket bat and ball on a coloured tile."""
    d.ellipse([x, y, x + s, y + s], fill=color)
    # ball
    d.ellipse([x + s * 0.60, y + s * 0.58, x + s * 0.82, y + s * 0.80],
              fill=(255, 255, 255))
    # bat, rotated 40 degrees
    import math as _m
    ang = _m.radians(40)
    bx, by = x + s * 0.30, y + s * 0.62
    w, h = 14, 52
    corners = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    pts = []
    for px, py in corners:
        rx = px * _m.cos(ang) - py * _m.sin(ang) + bx
        ry = px * _m.sin(ang) + py * _m.cos(ang) + by
        pts.append((rx, ry))
    d.polygon(pts, fill=(255, 255, 255))


def health_icon(d, x, y, s, color):
    """White medical cross on a coloured tile."""
    d.ellipse([x, y, x + s, y + s], fill=color)
    cx, cy = x + s / 2, y + s / 2
    t, a = 10, 26
    d.rectangle([cx - t, cy - a, cx + t, cy + a], fill=(255, 255, 255))
    d.rectangle([cx - a, cy - t, cx + a, cy + t], fill=(255, 255, 255))


def lead_panel(d, x, y, w, h):
    """Night skyline over Kyiv with a missile burst: flat shapes only."""
    sky = (24, 38, 63)
    d.rectangle([x, y, x + w, y + h], fill=sky)
    # stars
    for sx, sy in ((0.08, 0.10), (0.22, 0.05), (0.35, 0.14), (0.55, 0.07),
                   (0.68, 0.16), (0.85, 0.06), (0.93, 0.20), (0.45, 0.22)):
        d.ellipse([x + w * sx - 2, y + h * sy - 2,
                   x + w * sx + 2, y + h * sy + 2], fill=(230, 230, 220))
    # explosion burst (upper right): jagged, irregular fireball
    bx, by = x + w * 0.72, y + h * 0.30
    radii = [58, 30, 52, 26, 60, 34, 48, 22, 56, 28, 50, 24, 58, 30, 54, 26]
    pts = []
    for i, r in enumerate(radii):
        ang = i * math.pi / 8 + 0.12
        pts.append((bx + r * math.cos(ang), by + r * math.sin(ang)))
    d.polygon(pts, fill=(255, 150, 24))
    radii2 = [32, 16, 30, 14, 34, 18, 28, 12, 32, 16, 30, 14, 34, 16, 28, 14]
    pts = []
    for i, r in enumerate(radii2):
        ang = i * math.pi / 8 + 0.35
        pts.append((bx + r * math.cos(ang), by + r * math.sin(ang)))
    d.polygon(pts, fill=(255, 214, 90))
    # missile streak ending at the burst
    d.line([(x + w * 0.10, y + h * 0.44), (bx - 56, by + 12)],
           fill=(255, 255, 255), width=4)
    # smoke
    for sx, sy, r in ((0.60, 0.55, 26), (0.72, 0.62, 34), (0.84, 0.52, 22)):
        d.ellipse([x + w * sx - r, y + h * sy - r,
                   x + w * sx + r, y + h * sy + r], fill=(90, 96, 112))
    # buildings
    base = y + h
    for bx0, bw, bh in ((0.00, 0.20, 0.34), (0.18, 0.16, 0.46), (0.34, 0.22, 0.30),
                        (0.54, 0.16, 0.52), (0.70, 0.18, 0.38), (0.86, 0.14, 0.44)):
        d.rectangle([x + w * bx0, base - h * bh, x + w * (bx0 + bw), base],
                    fill=(10, 16, 30))
    # lit windows
    for wx, wy in ((0.05, 0.78), (0.11, 0.84), (0.24, 0.66), (0.30, 0.76),
                   (0.40, 0.80), (0.58, 0.60), (0.64, 0.70), (0.76, 0.74),
                   (0.90, 0.66), (0.94, 0.78)):
        d.rectangle([x + w * wx, y + h * wy, x + w * wx + 7, y + h * wy + 9],
                    fill=(255, 214, 110))


# ------------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    R = W - M

    # Masthead
    y = 26
    y = centred(d, W // 2, y, "THE DAY'S NEWS", font(SERIF, 76), INK)
    hrule(d, M, R, y + 8, 3)
    hrule(d, M, R, y + 14, 1)
    y += 26
    y = centred(d, W // 2, y, "SATURDAY, 21 NOVEMBER 2026",
                font(SANS_B, 30), RED)
    hrule(d, M, R, y + 6, 1)
    y += 20

    # ---- Lead story: Kyiv strikes
    lead_top = y
    lead_h = 250
    tx, tw = M, 588
    y = lead_top + 2
    d.text((tx, y), "KYIV, UKRAINE  —  WAR", font=font(SANS_B, 19), fill=RED)
    y += 30
    f_head = font(SERIF, 40)
    lines = wrap(d, "RUSSIA'S MASSIVE OVERNIGHT STRIKES HIT KYIV", f_head, tw)
    y = text_block(d, tx, y, lines, f_head, leading=47)
    y += 8
    f_deck = font(SANS, 21)
    deck = ("More than 400 drones and 110 missiles fired. "
            "Three bridges over the Dnipro shut; "
            "power cut in 11 regions.")
    y = text_block(d, tx, y, wrap(d, deck, f_deck, tw), f_deck, leading=27)
    lead_panel(d, 648, lead_top, R - 648, lead_h)
    d.text((648, lead_top + lead_h + 6), "KYIV AFTER THE OVERNIGHT STRIKES",
           font=font(SANS_B, 13), fill=GRAY)

    y = lead_top + lead_h + 34
    hrule(d, M, R, y, 2)
    y += 18

    # ---- Grid: 2 x 2 stories
    col_w = (R - M - 24) // 2
    row_h = 168
    cells = [
        ("SHENZHEN  •  DIPLOMACY",
         "TRUMP, XI, PUTIN: PEACE PLEDGE, DEAL TALK",
         "Declaration backs UN reform, nuclear-risk talks and more oil. "
         "Trump tells allies Putin 'wants a deal'.",
         NAVY, globe_icon),
        ("ODISHA, INDIA  •  WEATHER",
         "CYCLONE AKVAN WEAKENS OVER INDIA",
         "Storm crosses the Odisha coast near Gopalpur. More than "
         "300,000 evacuated; no deaths reported.",
         (14, 110, 106), cyclone_icon),
        ("WELLINGTON  •  SPORT",
         "RAHUL'S CENTURY LIFTS INDIA ON DAY 3",
         "India reach 255 for 1, chasing New Zealand's 368 in the "
         "first Test at the Basin Reserve.",
         (46, 107, 52), cricket_icon),
        ("VIRGINIA, USA  •  HEALTH",
         "FIRST MEASLES DEATH OF 2026 IN VIRGINIA",
         "A child under five dies after testing positive. Virginia has "
         "recorded 220 measles cases this year.",
         (122, 46, 109), health_icon),
    ]
    for i, (kicker, head, deck, color, icon) in enumerate(cells):
        cx = M + (i % 2) * (col_w + 24)
        cy = y + (i // 2) * (row_h + 16)
        tile = 104
        icon(d, cx, cy + 6, tile, color)
        tx2 = cx + tile + 14
        tw2 = cx + col_w - tx2
        yy = cy + 4
        d.text((tx2, yy), kicker, font=font(SANS_B, 15), fill=RED)
        yy += 24
        f_h = font(SERIF, 23)
        hl = wrap(d, head, f_h, tw2)
        yy = text_block(d, tx2, yy, hl, f_h, leading=27)
        yy += 4
        f_d = font(SANS, 17)
        yy = text_block(d, tx2, yy, wrap(d, deck, f_d, tw2), f_d, leading=22)

    y += 2 * row_h + 16 + 14
    hrule(d, M, R, y, 1)
    y += 12

    # ---- Also today strip
    d.text((M, y), "ALSO TODAY", font=font(SANS_B, 17), fill=RED)
    y += 26
    f_a = font(SANS, 18)
    also = ("Denmark expels Russian defence attaché  •  "
            "S&P 500 in correction as AI shares slide  •  "
            "GTA VI: record $3.79bn first-day sales")
    y = text_block(d, M, y, wrap(d, also, f_a, R - M), f_a, leading=25)

    # ---- Footer
    hrule(d, M, R, H - 44, 1)
    centred(d, W // 2, H - 36,
            "Sources: AP, Reuters, BBC, India Meteorological Department, "
            "Virginia Dept. of Health",
            font(SANS, 15), GRAY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
