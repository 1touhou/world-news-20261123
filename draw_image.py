#!/usr/bin/env python3
"""Draw the world-news infographic for Monday 23 November 2026.

Fresh code written for the news-image-20261123 entry. Renders a
1024x1024 PNG with six stories reported on 23 November 2026.
Run:  python3 draw_image.py   (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (13, 22, 38)          # deep navy
CARD = (26, 39, 63)        # slate blue
CARD_EDGE = (52, 74, 110)
WHITE = (245, 247, 250)
MUTED = (196, 208, 224)
GOLD = (255, 176, 32)
RED = (226, 62, 62)
TEAL = (45, 190, 170)

TAG_COLORS = {
    "CLIMATE": (46, 160, 90),
    "USA": (66, 103, 210),
    "AFRICA": (214, 128, 32),
    "EUROPE": (150, 90, 200),
    "ASIA": (200, 60, 90),
    "TRAVEL": (40, 150, 190),
}

STORIES = [
    ("CLIMATE", "COP31 collapses with no deal",
     "Nearly 200 nations leave the climate talks in Turkiye "
     "empty-handed after almost 48 hours of overtime."),
    ("USA", "Democrats clinch the House",
     "At least 258 seats won - the party's largest House "
     "majority since 1992."),
    ("AFRICA", "Drones hit Khartoum",
     "Strikes damage homes and a UN building; four people "
     "killed in and around Sudan's capital."),
    ("EUROPE", "Strikes kill six near Kyiv",
     "Russian attacks hit the Kyiv region; 14 people missing "
     "after a drone strike on a building."),
    ("ASIA", "Factory fire kills 24 in Indonesia",
     "A blaze at a candy plant in Banten leaves dozens "
     "missing; the search resumes on Monday."),
    ("TRAVEL", "Delta delays hit 1,000 flights",
     "A systems glitch snarls Atlanta, the world's busiest "
     "hub, days before Thanksgiving."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- subtle background globe, top right ---
    cx, cy, r = 928, 76, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(38, 58, 92), width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(38, 58, 92), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(38, 58, 92), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(38, 58, 92), width=2)

    # --- header ---
    d.rectangle([40, 42, 52, 150], fill=RED)
    f_kicker = font(BOLD, 26)
    d.text((72, 44), "MONDAY  \u2022  THE WORLD IN ONE PICTURE", font=f_kicker, fill=GOLD)
    f_date = font(BOLD, 68)
    d.text((70, 76), "23 NOVEMBER 2026", font=f_date, fill=WHITE)
    f_sub = font(BOLD, 34)
    d.text((72, 152), "WORLD NEWS", font=f_sub, fill=TEAL)
    d.line([40, 200, 984, 200], fill=CARD_EDGE, width=3)

    # --- story cards: 2 columns x 3 rows ---
    margin, gap = 40, 20
    cw = (W - 2 * margin - gap) // 2
    ch = 234
    top = 220
    f_tag = font(BOLD, 19)
    f_head = font(BOLD, 28)
    f_body = font(REG, 21)

    for i, (tag, head, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (cw + gap)
        y0 = top + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD,
                            outline=CARD_EDGE, width=2)
        accent = TAG_COLORS[tag]
        d.rounded_rectangle([x0, y0, x0 + 10, y1], radius=5, fill=accent)
        # tag chip
        tw = d.textlength(tag, font=f_tag) + 22
        d.rounded_rectangle([x0 + 28, y0 + 18, x0 + 28 + tw, y0 + 48],
                            radius=8, fill=accent)
        d.text((x0 + 39, y0 + 22), tag, font=f_tag, fill=WHITE)
        # headline (up to 2 lines)
        head_lines = wrap(d, head, f_head, cw - 56)
        hy = y0 + 62
        for line in head_lines[:2]:
            d.text((x0 + 28, hy), line, font=f_head, fill=WHITE)
            hy += 36
        # body
        body_lines = wrap(d, body, f_body, cw - 56)
        by = hy + 6
        for line in body_lines[:3]:
            d.text((x0 + 28, by), line, font=f_body, fill=MUTED)
            by += 28

    # --- footer ---
    fy = top + 3 * ch + 2 * gap + 14
    d.line([40, fy, 984, fy], fill=CARD_EDGE, width=2)
    f_foot = font(REG, 19)
    d.text((40, fy + 14),
           "Six stories reported on 23 November 2026  \u2022  Sources: Reuters, AP, AFP, Xinhua",
           font=f_foot, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
