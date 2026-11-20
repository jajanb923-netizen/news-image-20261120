#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261120.

A one-page newspaper front page summing up Friday 20 November 2026:
a fresh Russian missile attack on Kyiv, GTA VI's record $2.36 billion
launch day, Asian markets plunging on AI-bubble fears, a Houthi missile
hitting the Saudi wealth-fund tower in Riyadh, and the UK-EU youth
mobility deal, plus a ticker of the day's other stories. Every panel is
drawn with Pillow primitives (no external assets), so the text stays
crisp and the picture is fully deterministic.

Run:  python3 draw.py        (writes entry.png beside this file)
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 231)
INK = (18, 18, 18)
RED = (178, 30, 42)
NAVY = (26, 40, 72)
GOLD = (178, 140, 44)
GREY = (92, 92, 88)
GREEN = (18, 130, 62)

FONTS = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONTS, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONTS, "DejaVuSerif.ttf")
SERIF_I = os.path.join(FONTS, "DejaVuSerif-Italic.ttf")
SANS = os.path.join(FONTS, "DejaVuSans.ttf")
SANS_B = os.path.join(FONTS, "DejaVuSans-Bold.ttf")


def load_font(path, size):
    """Load a TTF font, falling back to a same-family face if missing."""
    if not os.path.isfile(path):
        path = SERIF_B if path.endswith("Bold.ttf") else SERIF
    return ImageFont.truetype(path, size)


def fit_lines(text, fnt, draw, max_w):
    """Word-wrap text to the given pixel width, measured for real."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped text; return the y just below the last line."""
    for line in fit_lines(text, fnt, draw, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def vgrad(draw, box, top, bottom):
    """Fill a rectangle with a vertical two-stop gradient."""
    x0, y0, x1, y1 = box
    span = max(y1 - y0 - 1, 1)
    for row in range(y0, y1):
        t = (row - y0) / span
        col = tuple(round(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, row), (x1, row)], fill=col)


def burst(draw, cx, cy, r, core, halo):
    """A star-shaped explosion burst with a bright core."""
    pts = []
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=halo)
    pts = []
    for i in range(8):
        ang = -math.pi / 2 + i * math.pi / 4
        rr = r * 0.55 if i % 2 == 0 else r * 0.25
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=core)


def dusk_city(draw, box):
    """Kyiv at dusk: dark skyline, lit windows, two missile bursts."""
    x0, y0, x1, y1 = box
    vgrad(draw, box, (38, 44, 84), (214, 96, 44))
    rng = [0.31, 0.55, 0.42, 0.71, 0.38, 0.64, 0.47, 0.58, 0.35, 0.66,
           0.44, 0.52, 0.39, 0.61, 0.48, 0.57]
    bx = x0
    i = 0
    while bx < x1 - 24:
        bw = 30 + int(rng[i % len(rng)] * 30)
        bh = int((y1 - y0) * (0.35 + rng[(i + 3) % len(rng)] * 0.55))
        draw.rectangle([bx, y1 - bh, bx + bw, y1], fill=(14, 18, 40))
        for wy in range(y1 - bh + 8, y1 - 6, 13):
            for wx in range(bx + 5, bx + bw - 5, 12):
                if (wx * 7 + wy * 13) % 11 < 4:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 205, 105))
        bx += bw + 5
        i += 1
    burst(draw, x0 + 190, y0 + 52, 34, (255, 236, 150), (255, 128, 30))
    burst(draw, x0 + 760, y0 + 44, 26, (255, 236, 150), (255, 128, 30))
    draw.rectangle([x0, y1 - 14, x1, y1], fill=(14, 18, 40))


def vi_sunset(draw, box):
    """Vice City sunset: purple-to-orange sky, sun, palms, big VI."""
    x0, y0, x1, y1 = box
    vgrad(draw, box, (52, 18, 96), (255, 118, 44))
    draw.ellipse([x1 - 118, y0 + 10, x1 - 46, y0 + 82], fill=(255, 224, 148))
    for px, lean, tall in [(x0 + 16, -14, 66), (x1 - 26, 14, 58)]:
        base_x, base_y = px, y1
        tip_x, tip_y = px + lean, y1 - tall
        draw.line([(base_x, base_y), (tip_x, tip_y)], fill=(28, 8, 50), width=6)
        for deg in (-75, -45, -15, 15, 45, 75):
            rad = math.radians(deg - 90)
            ex = tip_x + int(32 * math.cos(rad))
            ey = tip_y + int(17 * math.sin(rad)) - 4
            draw.line([(tip_x, tip_y), (ex, ey)], fill=(28, 8, 50), width=4)
    draw.text(((x0 + x1) // 2, y0 + 6), "VI",
              font=load_font(SERIF_B, 62), fill=(255, 255, 255),
              anchor="ma", stroke_width=2, stroke_fill=(52, 18, 96))


def falling_chart(draw, box):
    """A falling market chart: red line diving across a white card."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(255, 255, 255), outline=INK, width=2)
    for gy in range(y0 + 18, y1 - 6, 20):
        draw.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(228, 228, 228), width=1)
    pts = [(x0 + 14, y0 + 26), (x0 + 52, y0 + 22), (x0 + 92, y0 + 38),
           (x0 + 132, y0 + 34), (x0 + 172, y0 + 52), (x0 + 212, y0 + 48),
           (x0 + 252, y0 + 66), (x0 + 292, y0 + 62), (x0 + 332, y0 + 84)]
    draw.line(pts, fill=(178, 30, 42), width=5, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 15, ey - 3), (ex - 3, ey + 13)],
                 fill=(178, 30, 42))
    draw.text((x0 + 12, y0 + 4), "SOFTBANK", font=load_font(SANS_B, 17),
              fill=GREY)
    draw.text((x1 - 12, y0 + 4), "-16%", font=load_font(SANS_B, 20),
              fill=(178, 30, 42), anchor="ra")


def riyadh_tower(draw, box):
    """Glass towers at night, one hit by a missile streak from the corner."""
    x0, y0, x1, y1 = box
    vgrad(draw, box, (16, 24, 52), (64, 84, 128))
    for tx, tw, top in [(x0 + 60, 110, y0 + 34), (x0 + 260, 150, y0 + 16)]:
        draw.rectangle([tx, top, tx + tw, y1], fill=(150, 178, 208))
        draw.rectangle([tx, top, tx + tw, y1], outline=(230, 238, 248), width=2)
        for wy in range(top + 8, y1 - 6, 12):
            for wx in range(tx + 8, tx + tw - 10, 14):
                if (wx + wy) % 5 < 3:
                    draw.rectangle([wx, wy, wx + 6, wy + 6], fill=(255, 224, 130))
        draw.rectangle([tx - 6, top - 6, tx + tw + 6, top], fill=(210, 220, 235))
    hx, hy = x0 + 410, y0 + 44
    draw.line([(x1 - 6, y0 + 4), (hx, hy)], fill=(255, 150, 40), width=5)
    burst(draw, hx, hy, 22, (255, 236, 150), (255, 128, 30))


def uk_eu_flags(draw, box):
    """Union Jack beside the EU circle of stars, sized to the panel."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(233, 229, 215))
    ph = y1 - y0 - 16
    ux, uy, uw, uh = x0 + 18, y0 + 8, 190, ph
    draw.rectangle([ux, uy, ux + uw, uy + uh], fill=(1, 33, 105))
    draw.line([(ux, uy), (ux + uw, uy + uh)], fill=(255, 255, 255), width=14)
    draw.line([(ux + uw, uy), (ux, uy + uh)], fill=(255, 255, 255), width=14)
    draw.line([(ux, uy), (ux + uw, uy + uh)], fill=(200, 16, 46), width=5)
    draw.line([(ux + uw, uy), (ux, uy + uh)], fill=(200, 16, 46), width=5)
    draw.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)],
              fill=(255, 255, 255), width=22)
    draw.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)],
              fill=(255, 255, 255), width=22)
    draw.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)],
              fill=(200, 16, 46), width=10)
    draw.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)],
              fill=(200, 16, 46), width=10)
    cx, cy, r = x1 - 92, y0 + (y1 - y0) // 2, (y1 - y0) // 2 - 6
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 51, 153))
    for k in range(12):
        ang = -math.pi / 2 + k * math.pi / 6
        sx, sy = cx + int((r - 8) * math.cos(ang)), cy + int((r - 8) * math.sin(ang))
        pts = []
        for i in range(10):
            a2 = -math.pi / 2 + i * math.pi / 5
            rr = 7 if i % 2 == 0 else 3
            pts.append((sx + rr * math.cos(a2), sy + rr * math.sin(a2)))
        draw.polygon(pts, fill=(255, 204, 0))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

    # ---- masthead ----
    d.text((W // 2, 12), "THE WORLD", font=load_font(SERIF_B, 88),
           fill=INK, anchor="ma")
    d.line([(28, 118), (W - 28, 118)], fill=RED, width=4)
    d.text((W // 2, 126), "FRIDAY, 20 NOVEMBER 2026",
           font=load_font(SANS_B, 27), fill=INK, anchor="ma")
    d.text((W // 2, 158), "THE DAY IN FULL  \u2022  ONE PAGE",
           font=load_font(SANS, 17), fill=GREY, anchor="ma")
    d.line([(28, 186), (W - 28, 186)], fill=INK, width=2)

    # ---- lead: Kyiv, full-width panel then headline + deck ----
    dusk_city(d, (30, 196, 994, 330))
    d.text((30, 340), "KYIV, UKRAINE  \u2014  THE WAR",
           font=load_font(SANS_B, 19), fill=RED)
    d.text((30, 362), "RUSSIAN MISSILES HIT KYIV AGAIN",
           font=load_font(SERIF_B, 44), fill=INK)
    block(d, 30, 416,
          "Fresh missile attack hits the capital on Friday; three bridges "
          "struck, embassies damaged, at least six killed.",
          load_font(SERIF, 20), 964, 26)
    d.line([(28, 478), (W - 28, 478)], fill=INK, width=2)

    # ---- row A: GTA VI | markets ----
    col_w, gap = 472, 20
    lx, rx = 30, 30 + col_w + gap
    y = 490
    vi_sunset(d, (lx, y, lx + col_w, y + 92))
    falling_chart(d, (rx, y, rx + col_w, y + 92))
    y = 590
    d.text((lx, y), "VICE CITY", font=load_font(SANS_B, 19), fill=RED)
    d.text((rx, y), "THE MARKETS", font=load_font(SANS_B, 19), fill=RED)
    y = 612
    for x, head in [(lx, "GTA VI TOPS $2.36 BILLION IN A DAY"),
                    (rx, "ASIAN STOCKS PLUNGE ON AI BUBBLE FEARS")]:
        yy = y
        for line in fit_lines(head, load_font(SERIF_B, 29), d, col_w):
            d.text((x, yy), line, font=load_font(SERIF_B, 29), fill=INK)
            yy += 34
    y = 684
    block(d, lx, y, "24.6 million copies sold in a day \u2014 the biggest "
          "entertainment launch ever.", load_font(SERIF, 17), col_w, 21)
    block(d, rx, y, "SoftBank falls more than 16% and Seoul halts selling "
          "as the S&P slides a fifth straight day.",
          load_font(SERIF, 17), col_w, 21)
    d.line([(28, 738), (W - 28, 738)], fill=INK, width=2)

    # ---- row B: Riyadh | UK-EU ----
    y = 750
    riyadh_tower(d, (lx, y, lx + col_w, y + 76))
    uk_eu_flags(d, (rx, y, rx + col_w, y + 76))
    y = 832
    d.text((lx, y), "RIYADH", font=load_font(SANS_B, 18), fill=RED)
    d.text((rx, y), "BRUSSELS", font=load_font(SANS_B, 18), fill=RED)
    y = 854
    for x, head in [(lx, "HOUTHI MISSILE DAMAGES RIYADH TOWER"),
                    (rx, "UK AND EU SET TO AGREE YOUTH MOBILITY")]:
        yy = y
        for line in fit_lines(head, load_font(SERIF_B, 27), d, col_w):
            d.text((x, yy), line, font=load_font(SERIF_B, 27), fill=INK)
            yy += 31
    y = 918
    d.text((lx, y), "Strikes hit the wealth fund tower; no injuries reported.",
           font=load_font(SERIF, 16), fill=INK)
    d.text((rx, y), "Friday's summit is set to approve the scheme.",
           font=load_font(SERIF, 16), fill=INK)

    # ---- ticker ----
    d.rectangle([28, 948, W - 28, 1008], fill=NAVY)
    d.text((W // 2, 956),
           "COP31 DROPS FOSSIL-FUEL PHASE-OUT  \u2022  NVIDIA PROBED AFTER HUANG RESIGNS",
           font=load_font(SANS_B, 20), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 982),
           "PETE ROSE PARDONED  \u2022  BUKELE SEEKS THIRD TERM  \u2022  NIGERIA ENDS SUICIDE JAIL TERMS  \u2022  ITALY STRIKES",
           font=load_font(SANS_B, 15), fill=(255, 255, 255), anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
