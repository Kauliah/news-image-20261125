#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news image (1024x1024 PNG).

Front-page hierarchy: a centred masthead, one dark hero block for the
day's lead story, then five full-width wire rows, then a footer.
Every story was verified against at least two independent sources and
happened or was first reported on Wednesday 25 November 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_KICKER = font("DejaVuSans-Bold.ttf", 24)
F_DATE = font("DejaVuSans-Bold.ttf", 86)
F_SUBDATE = font("DejaVuSans.ttf", 22)
F_HERO_TAG = font("DejaVuSans-Bold.ttf", 22)
F_HERO_HEAD = font("DejaVuSans-Bold.ttf", 42)
F_HERO_SUB = font("DejaVuSans.ttf", 21)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 28)
F_SUB = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 20)
F_SRC = font("DejaVuSans.ttf", 16)

INK = (20, 28, 48)
NAVY = (22, 35, 63)
PAPER = (253, 252, 248)
GREY = (90, 96, 110)
LIGHT = (214, 219, 230)
RED = (192, 57, 43)
AMBER = (232, 163, 61)
ORANGE = (230, 126, 34)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(s, f):
    return d.textlength(s, font=f)

def centred(y, s, f, fill, cx=W // 2):
    d.text((cx - text_w(s, f) / 2, y), s, font=f, fill=fill)

def wrap(s, f, max_w):
    lines, cur = [], ""
    for word in s.split(" "):
        trial = (cur + " " + word).strip()
        if text_w(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def letterspaced(y, s, f, fill, spacing=7):
    total = sum(text_w(c, f) for c in s) + spacing * (len(s) - 1)
    x = (W - total) / 2
    for c in s:
        d.text((x, y), c, font=f, fill=fill)
        x += text_w(c, f) + spacing

# ---------- masthead ----------
letterspaced(30, "THE WORLD IN ONE DAY", F_KICKER, RED)
centred(62, "25 NOVEMBER 2026", F_DATE, INK)
centred(152, "WEDNESDAY  ·  SIX STORIES  ·  FIVE REGIONS", F_SUBDATE, GREY)
d.rectangle([36, 182, W - 36, 186], fill=RED)
d.rectangle([36, 190, W - 36, 192], fill=RED)

# ---------- hero: Strait of Hormuz ----------
HX0, HY0, HX1, HY1 = 36, 204, W - 36, 430
d.rounded_rectangle([HX0, HY0, HX1, HY1], radius=10, fill=NAVY)
d.text((HX0 + 28, HY0 + 18), "STRAIT OF HORMUZ  ·  ENERGY WAR", font=F_HERO_TAG, fill=AMBER)
hero_head = wrap("TWO OIL TANKERS HIT MINES AND CATCH FIRE", F_HERO_HEAD, 620)
y = HY0 + 50
for line in hero_head:
    d.text((HX0 + 28, y), line, font=F_HERO_HEAD, fill=(255, 255, 255))
    y += 48
hero_sub = wrap("Iran's Revolutionary Guards say the ships tried an "
                "unauthorised route; no ships named, no casualties given.",
                F_HERO_SUB, 620)
y += 8
for line in hero_sub:
    d.text((HX0 + 28, y), line, font=F_HERO_SUB, fill=LIGHT)
    y += 27

# tanker pictogram, right side of the hero block
px, py = 800, 240
# flames above the tanker
d.polygon([(px + 30, py + 58), (px + 52, py + 6), (px + 74, py + 58)], fill=(230, 126, 34))
d.polygon([(px + 44, py + 58), (px + 58, py + 22), (px + 72, py + 58)], fill=(241, 196, 15))
d.polygon([(px + 88, py + 58), (px + 104, py + 18), (px + 120, py + 58)], fill=(230, 126, 34))
d.polygon([(px + 96, py + 58), (px + 106, py + 32), (px + 116, py + 58)], fill=(241, 196, 15))
# hull
d.polygon([(px, py + 62), (px + 150, py + 62), (px + 138, py + 96), (px + 12, py + 96)],
          fill=(232, 163, 61))
# deck containers + bridge
d.rectangle([px + 18, py + 40, px + 52, py + 62], fill=(255, 255, 255))
d.rectangle([px + 58, py + 40, px + 92, py + 62], fill=(200, 208, 220))
d.rectangle([px + 112, py + 26, px + 140, py + 62], fill=(255, 255, 255))
d.rectangle([px + 118, py + 32, px + 134, py + 40], fill=NAVY)
# waves
for i, wx in enumerate([px - 6, px + 52, px + 110]):
    d.arc([wx, py + 104, wx + 44, py + 122], 0, 180, fill=(120, 160, 210), width=4)

# ---------- wire rows ----------
ROWS = [
    dict(tag="SPACE  ·  CHINA–PAKISTAN", color=(14, 124, 123),
         head="PAKISTAN'S FIRST ASTRONAUT REACHES TIANGONG",
         sub="Muhammad Zeeshan Ali flies on Shenzhou-24, the first foreigner on Tiangong.",
         icon="rocket"),
    dict(tag="AFRICA  ·  DISASTER", color=(192, 57, 43),
         head="31 KILLED IN CAIRO FUEL TANKER FIRE",
         sub="Tanker overturned on the Ring Road in Al-Warraq, Giza; 21 hurt, cars burned.",
         icon="fire"),
    dict(tag="PACIFIC  ·  DIPLOMACY", color=(37, 99, 168),
         head="SOLOMON ISLANDS BARS FOREIGN BASES",
         sub="Treaty names Australia primary security partner; A$740m in aid over 10 years.",
         icon="flags"),
    dict(tag="ASIA  ·  WORK", color=(46, 125, 50),
         head="BANGLADESH RAISES GARMENT PAY 36%",
         sub="After weeks of protests, pay rises to 17,000 taka, about $139 a month.",
         icon="shirt"),
    dict(tag="EUROPE  ·  BUDGET", color=(106, 76, 147),
         head="EU APPROVES €199.7 BILLION BUDGET",
         sub="Parliament votes 406–184: €199.7bn in commitments, €211.5bn in payments.",
         icon="parliament"),
]

def draw_icon(box, kind, color):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=12, fill=color)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    white = (255, 255, 255)
    if kind == "rocket":
        d.polygon([(cx, cy - 26), (cx + 11, cy - 4), (cx + 11, cy + 12),
                   (cx - 11, cy + 12), (cx - 11, cy - 4)], fill=white)
        d.ellipse([cx - 5, cy - 12, cx + 5, cy - 2], fill=color)
        d.polygon([(cx - 11, cy + 8), (cx - 19, cy + 20), (cx - 11, cy + 16)], fill=white)
        d.polygon([(cx + 11, cy + 8), (cx + 19, cy + 20), (cx + 11, cy + 16)], fill=white)
        d.polygon([(cx - 6, cy + 14), (cx, cy + 30), (cx + 6, cy + 14)], fill=(241, 196, 15))
        for sx, sy in [(cx - 26, cy - 22), (cx + 26, cy - 18), (cx + 24, cy + 22)]:
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=white)
    elif kind == "fire":
        d.polygon([(cx - 16, cy + 16), (cx - 2, cy - 22), (cx + 4, cy - 2),
                   (cx + 14, cy - 14), (cx + 18, cy + 16)], fill=white)
        d.polygon([(cx - 7, cy + 16), (cx, cy - 4), (cx + 8, cy + 16)], fill=(241, 196, 15))
        d.rectangle([cx - 22, cy + 18, cx + 22, cy + 24], fill=white)
    elif kind == "flags":
        d.rectangle([cx - 22, cy - 20, cx - 20, cy + 24], fill=white)
        d.rectangle([cx + 20, cy - 20, cx + 22, cy + 24], fill=white)
        d.polygon([(cx - 20, cy - 20), (cx + 2, cy - 14), (cx - 20, cy - 8)], fill=white)
        d.polygon([(cx + 20, cy - 20), (cx - 2, cy - 14), (cx + 20, cy - 8)], fill=(241, 196, 15))
        d.rectangle([cx - 24, cy + 24, cx + 24, cy + 28], fill=white)
    elif kind == "shirt":
        d.polygon([(cx - 10, cy - 20), (cx + 10, cy - 20), (cx + 24, cy - 8),
                   (cx + 16, cy + 2), (cx + 12, cy - 2), (cx + 12, cy + 22),
                   (cx - 12, cy + 22), (cx - 12, cy - 2), (cx - 16, cy + 2),
                   (cx - 24, cy - 8)], fill=white)
        d.polygon([(cx - 2, cy - 20), (cx + 2, cy - 20), (cx, cy - 12)], fill=color)
        d.polygon([(cx + 16, cy - 26), (cx + 26, cy - 16), (cx + 20, cy - 16),
                   (cx + 20, cy - 6), (cx + 14, cy - 6), (cx + 14, cy - 16),
                   (cx + 8, cy - 16)], fill=(241, 196, 15))
    elif kind == "parliament":
        d.polygon([(cx - 26, cy - 14), (cx, cy - 26), (cx + 26, cy - 14)], fill=white)
        for bx in (-20, -7, 6, 19):
            d.rectangle([cx + bx - 3, cy - 12, cx + bx + 3, cy + 18], fill=white)
        d.rectangle([cx - 28, cy + 18, cx + 28, cy + 24], fill=white)
        d.rectangle([cx - 2, cy - 30, cx + 2, cy - 26], fill=white)

ROW_H = 104
y = 446
for i, row in enumerate(ROWS):
    draw_icon((36, y + 14, 114, y + 92), row["icon"], row["color"])
    tx = 134
    d.text((tx, y + 10), row["tag"], font=F_TAG, fill=row["color"])
    d.text((tx, y + 34), row["head"], font=F_HEAD, fill=INK)
    sub_lines = wrap(row["sub"], F_SUB, W - 36 - tx)
    sy = y + 68
    for line in sub_lines[:2]:
        d.text((tx, sy), line, font=F_SUB, fill=GREY)
        sy += 25
    if i < len(ROWS) - 1:
        d.line([36, y + ROW_H - 4, W - 36, y + ROW_H - 4], fill=(222, 220, 210), width=2)
    y += ROW_H

# ---------- footer ----------
fy = y + 8
centred(fy, "Every story above happened or was first reported on 25 November 2026.",
        F_FOOT, GREY)
centred(fy + 28, "Sources: Reuters · AP · Xinhua · AFP · European Parliament",
        F_SRC, (150, 155, 165))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, img.size, os.path.getsize(out), "bytes")
