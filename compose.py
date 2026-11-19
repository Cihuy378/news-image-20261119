#!/usr/bin/env python3
"""Compose the news-image-20261119 front page (1024x1024 PNG).

A newspaper front page, "THE WORLD IN ONE DAY — Thursday, 19 November
2026", built with PIL from four AI-generated editorial illustrations in
assets/ plus small flat icons drawn by this script itself. Every headline,
deck and brief on the page is rendered here, so the finished image carries
no garbled AI text. The script is fully deterministic: no network, no clock,
no randomness — running it twice produces identical bytes.

Layout (1024 x 1024, 24 px margins):
  masthead -> lead story (Shenzhen trilateral) -> GTA VI + Anthropic IPO
  -> Berlin story + Gulf box -> ALSO TODAY (20 briefs, 3 columns) -> footer.
30 verified stories in total, all reported on 19 November 2026.

Usage:  python3 compose.py          (writes entry.png next to this file)
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "entry.png"

PAGE = 1024
MARGIN = 24
PAPER = (250, 246, 236)
INK = (20, 20, 20)
SOFT = (74, 74, 74)
RULE = (180, 172, 150)
RED = (179, 38, 30)
NAVY = (27, 42, 74)
TEAL = (14, 90, 86)
GOLD = (176, 132, 24)
PANEL = (240, 234, 220)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 47)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_KICK = font("DejaVuSans-Bold.ttf", 13)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 31)
F_LEAD_DECK = font("DejaVuSans.ttf", 15)
F_HEAD = font("DejaVuSerif-Bold.ttf", 20)
F_DECK = font("DejaVuSans.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_TAG = font("DejaVuSans-Bold.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 10)
F_CAP = font("DejaVuSans.ttf", 10)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, color=RED):
    draw.text((x, y), text, font=F_KICK, fill=color)
    return y + 19


def hrule(draw, y, weight=2, color=INK, x0=MARGIN, x1=PAGE - MARGIN):
    draw.line([(x0, y), (x1, y)], fill=color, width=weight)


def crop_fill(path, width, height):
    """Open an image, centre-crop to the box aspect, resize to the box."""
    img = Image.open(path).convert("RGB")
    w, h = img.size
    target = width / height
    if w / h > target:
        new_w = int(h * target)
        img = img.crop(((w - new_w) // 2, 0, (w + new_w) // 2, h))
    else:
        new_h = int(w / target)
        img = img.crop((0, (h - new_h) // 2, w, (h + new_h) // 2))
    return img.resize((width, height), Image.LANCZOS)


def frame(draw, box, color=INK, weight=2):
    draw.rectangle(box, outline=color, width=weight)


# ---------------------------------------------------------------- icons
# Small flat icons drawn with PIL primitives, one per lead section.

def icon_globe(draw, cx, cy, r=11, color=NAVY):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color,
                 width=1)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=1)


def icon_controller(draw, x, y, s=22, color=RED):
    draw.rounded_rectangle([x, y, x + s, y + s * 0.72], radius=5,
                           outline=color, width=2)
    draw.ellipse([x + 3, y + s * 0.28, x + 7, y + s * 0.28 + 4], fill=color)
    draw.ellipse([x + s - 7, y + s * 0.28, x + s - 3, y + s * 0.28 + 4],
                 fill=color)
    draw.line([(x + s // 2 - 2, y + s * 0.42), (x + s // 2 + 2, y + s * 0.42)],
              fill=color, width=2)


def icon_chart(draw, x, y, s=22, color=TEAL):
    pts = [(x, y + s * 0.8), (x + s * 0.3, y + s * 0.5),
           (x + s * 0.55, y + s * 0.62), (x + s * 0.8, y + s * 0.25),
           (x + s, y + s * 0.1)]
    draw.line(pts, fill=color, width=3, joint="curve")
    draw.polygon([(x + s, y + s * 0.1), (x + s - 6, y + s * 0.1),
                  (x + s, y + s * 0.1 + 6)], fill=color)
    draw.line([(x, y + s), (x + s, y + s)], fill=color, width=2)


def icon_flag(draw, x, y, s=22, color=GOLD):
    draw.line([(x + 2, y), (x + 2, y + s)], fill=color, width=2)
    draw.polygon([(x + 2, y + 1), (x + s, y + 5), (x + 2, y + 10)],
                 fill=color)
    draw.rectangle([x, y + s - 2, x + s, y + s], fill=color)


def icon_storm(draw, cx, cy, r=11, color=NAVY):
    for i, rr in enumerate((r, r * 0.66, r * 0.36)):
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr],
                 start=200 + i * 40, end=200 + i * 40 + 220,
                 fill=color, width=2)

# ---------------------------------------------------------------- stories
# All 30 stories were reported on Thursday 19 November 2026. Sources are
# listed in README.md; the four leads carry their decks here.

LEAD = {
    "img": "media-generation-summit-0-8e8e2db0-e1b9-4222-ac57-cf0a4acc168b.png",
    "kicker": "SHENZHEN  ·  APEC SUMMIT",
    "head": "Three leaders, one table",
    "deck": ("Trump, Xi and Putin meet today in Shenzhen — the first "
             "trilateral of the three sitting presidents. Nuclear arms "
             "cuts are on the table, and a Trump–Putin bilateral follows "
             "the APEC plenary. Officials play down hopes of a deal."),
}

SECOND = [
    {
        "img": "media-generation-vicecity-0-d07679e9-03d5-4996-a3ee-0fce98d953b4.png",
        "kicker": "VICE CITY  ·  GAMES",
        "head": "GTA VI is here — after 13 years",
        "deck": ("Out at midnight on PS5 and Xbox. 9.69m pre-orders "
                 "($942m); Metacritic 99; eight Game Awards nods."),
        "icon": "controller",
    },
    {
        "img": "media-generation-ipo-0-5bb17f91-acd5-464e-856b-bd07df98d9c2.png",
        "kicker": "WALL STREET  ·  MARKETS",
        "head": "Anthropic debuts at $1.4 trillion",
        "deck": ("Claude's maker starts trading as ANT today: 825m shares "
                 "at $70–$78, priced above $80, raising up to $64bn."),
        "icon": "chart",
    },
]

BERLIN = {
    "img": "media-generation-berlin-0-00b43721-c13e-4f67-b185-b07e8e86d536.png",
    "kicker": "BERLIN  ·  UKRAINE",
    "head": "Europe rallies for Kyiv",
    "deck": ("The Coalition of the Willing meets in Berlin today, with "
             "Witkoff and Kushner in the room, as allies fear Shenzhen "
             "could settle Ukraine's fate without them."),
}

GULF = [
    ("GULF", "2 Houthi drones aimed at Riyadh intercepted"),
    ("GULF", "Cruise missile aimed at Riyadh shot down"),
    ("GULF", "Saudi: danger passed in three southern cities"),
    ("GULF", "Hormuz war-risk insurance hits $64m"),
    ("GULF", "Saudis brace for Yemen war lasting into 2027"),
    ("GULF", "Trump: Iran may pay dearly over bomb plan"),
]

ALSO = [
    ("GAZA", "Israel threatens more land seizures"),
    ("INDIA", "Akvan: 21cm rain; landfall due Friday"),
    ("LIBYA", "Cocaine, millions of pills seized"),
    ("FRANCE", "Minister: Mélenchon could win it all"),
    ("CANADA", "Carney recalibrates China ties"),
    ("USA", "Senators: AI cyber threats outpacing US"),
    ("MYANMAR", "Military chief rethinks ASEAN ties"),
    ("SAUDI", "PIF top wealth fund brand, 3rd year"),
    ("MANILA", "Trump claims major Philippines pact"),
    ("SWEDEN", "Vigil honours children killed in Gaza"),
    ("DELHI", "‘We are journalists, not reel makers’"),
    ("INDIA", "Panel planned for professional leagues"),
    ("CRICKET", "Duckett hits 133; England dominate"),
    ("BLACK SEA", "Sunken LPG tanker was hit by shells"),
    ("TOKYO", "India, Japan to review defence ties"),
    ("USA", "Tougher rules for work green cards"),
    ("ALASKA", "Peltola win seals 56–44 Senate edge"),
    ("TECH", "Microsoft eyes AI deal with ByteDance"),
    ("OIL", "Oil falls as risk aversion grips"),
    ("TRADE", "US–China barriers keep rising"),
]

ICONS = {
    "controller": icon_controller,
    "chart": icon_chart,
}


def build():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(page)

    # ---- masthead ---------------------------------------------------
    d.text((PAGE // 2, 16), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK,
           anchor="ma")
    icon_globe(d, 78, 40)
    icon_globe(d, PAGE - 78, 40)
    d.text((PAGE // 2, 66), "THURSDAY, 19 NOVEMBER 2026", font=F_DATE,
           fill=RED, anchor="ma")
    d.text((MARGIN, 66), "30 STORIES", font=F_TAG, fill=SOFT)
    d.text((PAGE - MARGIN, 66), "WORLDWIDE", font=F_TAG, fill=SOFT,
           anchor="ra")
    hrule(d, 90, weight=3)
    hrule(d, 95, weight=1)

    # ---- lead: Shenzhen trilateral ----------------------------------
    ly = 106
    lead_img = crop_fill(ASSETS / LEAD["img"], 620, 268)
    page.paste(lead_img, (MARGIN, ly))
    frame(d, [MARGIN, ly, MARGIN + 620, ly + 268])
    d.text((MARGIN + 6, ly + 270), "The table is set in Shenzhen.",
           font=F_CAP, fill=SOFT)
    tx = MARGIN + 640
    ty = kicker(d, tx, ly + 2, LEAD["kicker"])
    ty = draw_wrapped(d, tx, ty, LEAD["head"], F_LEAD_HEAD, 360, INK, 36)
    ty += 6
    draw_wrapped(d, tx, ty, LEAD["deck"], F_LEAD_DECK, 358, SOFT, 20)
    hrule(d, 396, weight=2)

    # ---- second row: GTA VI + Anthropic IPO -------------------------
    sy = 408
    for i, story in enumerate(SECOND):
        x = MARGIN + i * 500
        img = crop_fill(ASSETS / story["img"], 472, 142)
        page.paste(img, (x, sy))
        frame(d, [x, sy, x + 472, sy + 142])
        ICONS[story["icon"]](d, x + 448, sy + 146)
        yy = kicker(d, x, sy + 150, story["kicker"],
                    RED if i == 0 else TEAL)
        yy = draw_wrapped(d, x, yy, story["head"], F_HEAD, 472, INK, 24)
        draw_wrapped(d, x, yy + 2, story["deck"], F_DECK, 472, SOFT, 17)
    hrule(d, 646, weight=2)

    # ---- third row: Berlin + Gulf box --------------------------------
    by = 658
    bimg = crop_fill(ASSETS / BERLIN["img"], 300, 150)
    page.paste(bimg, (MARGIN, by))
    frame(d, [MARGIN, by, MARGIN + 300, by + 150])
    bx = MARGIN + 316
    yy = kicker(d, bx, by + 2, BERLIN["kicker"], NAVY)
    yy = draw_wrapped(d, bx, yy, BERLIN["head"], F_HEAD, 316, INK, 24)
    draw_wrapped(d, bx, yy + 3, BERLIN["deck"], F_DECK, 316, SOFT, 17)

    gx = 676
    d.rectangle([gx, by, PAGE - MARGIN, by + 150], fill=PANEL,
                outline=RULE, width=1)
    icon_storm(d, gx + 298, by + 16)
    yy = kicker(d, gx + 12, by + 8, "THE GULF WAR", RED)
    for tag, text in GULF:
        d.text((gx + 12, yy), "▪", font=F_TAG, fill=RED)
        yy = draw_wrapped(d, gx + 28, yy, text, F_BRIEF, 268, INK, 14) + 6
    hrule(d, 820, weight=2)

    # ---- also today ---------------------------------------------------
    ay = 832
    yy = kicker(d, MARGIN, ay, "ALSO TODAY", INK)
    col_w, gap = 312, 8
    per_col = 7
    for col in range(3):
        x = MARGIN + col * (col_w + gap)
        y = yy + 2
        for tag, text in ALSO[col * per_col:(col + 1) * per_col]:
            d.text((x, y), f"{tag} — ", font=F_TAG, fill=RED)
            tw = d.textlength(f"{tag} — ", font=F_TAG)
            y = draw_wrapped(d, x + tw, y, text, F_BRIEF, col_w - tw,
                             INK, 14)
            y += 5

    # ---- footer -------------------------------------------------------
    hrule(d, 1000, weight=1, color=RULE)
    d.text((MARGIN, 1006),
           "Sources: Reuters · AP · AFP · Bloomberg · CNBC · WSJ · IMD · "
           "People · Sensor Tower",
           font=F_FOOT, fill=SOFT)
    d.text((PAGE - MARGIN, 1006), "All stories reported 19 Nov 2026",
           font=F_FOOT, fill=SOFT, anchor="ra")

    page.save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
