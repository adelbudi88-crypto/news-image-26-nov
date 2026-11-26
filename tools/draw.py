#!/usr/bin/env python3
"""Draw the 26 November 2026 front page: 1024x1024, deterministic.

v4 — built from the v3 newspaper template (25 Nov, 41 stories,
submitted, blind rounds not yet published) and from the winners'
template (superskie 864,498 / 872,350 on 19-20 Nov; v2 round 2
708,842, rank 272/9,063). 43 stories this time (3 leads + 10
picture stories + 30 briefs) because the Thu 26 Nov cycle is
news-rich in Asia and the US: tariffs, Kim's nukes, Thanksgiving.

STRICT SAME-DAY BAR (per RULES.txt: events that happened, or were
first reported, on 26 November 2026 in any time zone). Built Thu
26 Nov 08:30 WIB (01:30 UTC), so this edition covers the Thu
morning news cycle plus Thu-scheduled events (marked TODAY).
Everything first reported Wed 25 Nov or earlier is LEFT OUT and
named in the DATE CHECK footer instead of appearing as news.
Hard-won verification calls: Sudan drone strikes (Tue attack,
reported Wed) OUT; Gaza Abu al-Ouf killing (early Wed) OUT;
Ramaphosa Phala Phala win (Wed) OUT; Bangladesh wage +36% (Wed)
OUT; Shenzhou-24 / first Pakistani astronaut (Wed) OUT; PCE
+3.8% and GDP +4.3% (Wed) OUT; UCL Wed results OUT; chess Game
2 draw (Wed) OUT. Kim's tactical-nukes call counts as Thu: KCNA
reported it Thursday in Pyongyang time (22:04 UTC Wed).

VERIFIED STORIES (all checked live 26 Nov 2026, 00:00-01:30 UTC):
  Leads: Nikkei futures 57,370 (+0.6% vs Wed close 57,011.62),
  Hang Seng futures 22,149 (+0.8% vs 21,966.01) (CNBC); Dow
  +0.33% to 50,182.95 after a 1,100-point slide, Nasdaq -0.62%
  to 23,585.80 (AP); Kim: deploy tactical nukes wider, nuclear
  status "absolutely inviolable" (Reuters SEOUL Nov 26, KCNA
  Thu); Taiwan: 15% tariff, lowest tier, not stacked on MFN
  (Exec Yuan presser 08:30 Thu; Peter Lewis briefing 06:00 HKT:
  China 20% rising to 40%, EU/Japan/Korea ~15%, India up to 17%).
  Pictures: Bougainville debate continues, 89 of 118 MPs needed,
  PNG 2027 Budget due Thu (Business Melanesia); chess Game 3
  today, Sindarov White, 1-1, 15:00 CET (ChessBase); NFL
  Thanksgiving tripleheader Bears-Lions 1pm, Eagles-Cowboys
  4:30pm, Chiefs-Bills 8:20pm ET (NBC); Europa League 18 games
  tonight (Sports Mole); Wall St comeback (Reuters); Macy's
  parade + Dog Show (NBC/DIRECTV); Nepal Rs 15,000 cr package
  (26 Nov headlines); Emirates tops airline rankings (26 Nov
  headlines).
  Briefs: Kospi opens lower (Finnhub live Thu 09:12 KST);
  China tariff reply awaited tonight; ASX +0.15% at open;
  IPL 1,220 register; Flipkart CEO steps down Dec; Hasina seeks
  return Dec 16; India space economy $9bn to $45bn; PNG Budget
  balanced plan vowed; US shut Thu, short Fri session; India
  urges human control over military AI; India condemns Riyadh
  tower attack, 2 Indians hurt; Anand Kumar honoured in Japan;
  Brazil Wolbachia cuts infections 68%; chess crown $2.5m;
  Rising Stars semis today; island school takes coconuts for
  tuition; Detroit's 87th Thanksgiving game; Bills 9-1 host
  Chiefs 8-2; TCU vs Texas Tech 8pm ET; 12 chess games left,
  first to 7.5; Bougainville 97.7% yes in 2019; Black Friday
  Broncos at Steelers Fri.
DROPPED (first reported Wed 25 Nov or earlier -- named in the
DATE CHECK, not shown as news): tariff proposal itself; PCE
+3.8%, GDP +4.3%; UCL results; chess Game 2 draw; Ramaphosa
Phala Phala; Bangladesh wage +36%; Sudan strikes; Gaza
Abu al-Ouf; Shenzhou-24; Houthi Ras Tanura claim; Brent $94.61;
Saudi budget $371bn; BepiColombo at Mercury; Suez revenues
double; Petrobras $122bn; Venezuela debt $237.5bn; Steelers
release Rodgers; Deere reports; Fed Beige Book; German GDP;
BoE Bailey; Australia inflation; US 7-yr auction; Swiss envoy
expelled.

Deterministic: no randomness, no clock, no network. DejaVu
Serif + Sans from /usr/share/fonts/truetype/dejavu.
Run: python3 tools/draw.py  ->  entry.png (1024x1024, <1 MiB).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 20
CONTENT_W = W - 2 * MARGIN  # 984

PAPER = (246, 241, 227)
INK = (26, 26, 26)
INK_SOFT = (74, 74, 74)
RED = (166, 30, 30)
RED_DARK = (140, 22, 22)
BLUE = (31, 78, 121)
NAVY = (24, 44, 74)
GOLD = (176, 132, 32)
GREEN = (40, 110, 70)
GREY = (96, 96, 96)
SEA = (52, 96, 130)
SKY = (214, 228, 238)
OCEAN = (223, 233, 238)
LAND = (232, 220, 192)
CARD = (252, 250, 244)
BORDER = (180, 172, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, color=INK, width=1):
    draw.line([x0, y, x1, y], fill=color, width=width)


def tag_chip(draw, x, y, text, fill=RED, fg=(255, 255, 255), size=10):
    """Small filled label, e.g. CONFIRMED - AP. Returns its width."""
    fnt = sans_b(size)
    w = int(text_w(draw, text, fnt)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=fill)
    draw.text((x + 6, y + 2), text, font=fnt, fill=fg)
    return w


def chip_right(draw, x1, y, text, fill):
    """Certainty chip right-aligned to x1 inside an art box."""
    fnt = sans_b(8)
    w = int(text_w(draw, text, fnt)) + 10
    x0 = x1 - w - 4
    draw.rounded_rectangle([x0, y + 3, x0 + w, y + 17], radius=3, fill=fill)
    draw.text((x0 + 5, y + 5), text, font=fnt, fill=(255, 255, 255))
    return x0


# ------------------------------------------------------------------
# Lead art (90px tall boxes, 320 wide). Richer than v2: sky bands,
# figures, stamps -- closer to the winners' painted heroes.
# ------------------------------------------------------------------

def art_lead_steady(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(16, 28, 44))
    for gy in (y0 + 22, y0 + 44, y0 + 66):
        draw.line([x0 + 8, gy, x1 - 8, gy], fill=(40, 60, 84), width=1)
    # Wed slide (red, left), Thu futures bounce (green, right).
    draw.line([(x0 + 12, y1 - 62), (x0 + 110, y1 - 52), (x0 + 160, y1 - 30)],
              fill=(255, 90, 70), width=4, joint="curve")
    draw.line([(x0 + 160, y1 - 30), (x0 + 230, y1 - 48), (x1 - 14, y1 - 62)],
              fill=(74, 222, 128), width=4, joint="curve")
    draw.text((x0 + 10, y0 + 6), "NIKKEI FUT +0.6%", font=sans_b(18),
              fill=(74, 222, 128))
    draw.text((x0 + 10, y1 - 20),
              "Hang Seng fut +0.8%  ·  US shut for Thanksgiving",
              font=sans(11), fill=(190, 205, 220))


def art_lead_nukes(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(30, 16, 16))
    # Missile, centre-right, nose up.
    draw.polygon([(x0 + 210, y0 + 8), (x0 + 222, y0 + 26),
                  (x0 + 210, y0 + 30), (x0 + 198, y0 + 26)],
                 fill=(220, 220, 210))
    draw.rectangle([x0 + 200, y0 + 26, x0 + 220, y0 + 66],
                   fill=(200, 200, 190))
    draw.polygon([(x0 + 200, y0 + 66), (x0 + 192, y0 + 80),
                  (x0 + 200, y0 + 74)], fill=(166, 30, 30))
    draw.polygon([(x0 + 220, y0 + 66), (x0 + 228, y0 + 80),
                  (x0 + 220, y0 + 74)], fill=(166, 30, 30))
    draw.ellipse([x0 + 202, y1 - 12, x0 + 218, y1 - 2],
                 fill=(255, 140, 60))
    draw.text((x0 + 10, y0 + 8), "TACTICAL", font=sans_b(26),
              fill=(255, 255, 255))
    draw.text((x0 + 10, y0 + 38), "NUKES, WIDER ROLLOUT", font=sans_b(13),
              fill=(255, 120, 100))
    draw.text((x0 + 10, y1 - 20), "KCNA: status 'absolutely inviolable'",
              font=sans(11), fill=(200, 170, 160))


def art_lead_tariffs(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(214, 200, 170))
    # Brick tariff wall, bottom.
    for c in range(8):
        bx = x0 + c * 40
        draw.rectangle([bx, y1 - 22, bx + 38, y1 - 12],
                       fill=(166, 90, 60), outline=(120, 60, 40),
                       width=1)
    draw.text((x0 + 10, y0 + 6), "20%", font=sans_b(30), fill=RED_DARK)
    draw.text((x0 + 96, y0 + 12), "CHINA", font=sans_b(14), fill=INK)
    draw.text((x0 + 96, y0 + 30), "may rise to 40%", font=sans(11),
              fill=INK_SOFT)
    draw.text((x1 - 92, y0 + 6), "15%", font=sans_b(30), fill=BLUE)
    draw.text((x1 - 92, y0 + 40), "EU · JAPAN · KOREA", font=sans_b(9),
              fill=INK)
    draw.text((x0 + 10, y1 - 40), "14 partners hit  ·  Taiwan: lowest tier",
              font=sans(11), fill=INK_SOFT)


# ------------------------------------------------------------------
# Picture-story mini art (40px tall, ~190 wide). Each scene has a
# sky band, a ground band and 3-6 shapes -- richer than v2's flat
# icons, in the winners' painted-scene spirit.
# ------------------------------------------------------------------

def mini_bougainville(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(52, 120, 150))
    draw.ellipse([x0 + 14, y0 + 16, x0 + 92, y1 - 4], fill=(224, 198, 138))
    draw.line([x0 + 44, y0 + 20, x0 + 40, y0 + 6], fill=(90, 60, 30), width=4)
    draw.arc([x0 + 24, y0 + 2, x0 + 58, y0 + 16], 200, 340,
             fill=(52, 128, 74), width=4)
    # Ballot box, right.
    draw.rectangle([x1 - 64, y0 + 12, x1 - 10, y1 - 4], fill=(90, 80, 64))
    draw.rectangle([x1 - 58, y0 + 6, x1 - 16, y0 + 12], fill=(120, 110, 96))
    draw.text((x1 - 58, y0 + 16), "89", font=sans_b(14), fill=CARD)


def mini_chess(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(60, 48, 36))
    # 4x4 board.
    bs, ox, oy = 9, x0 + 14, y0 + 2
    for r in range(4):
        for c in range(4):
            col = CARD if (r + c) % 2 == 0 else (120, 100, 78)
            draw.rectangle([ox + c * bs, oy + r * bs,
                            ox + (c + 1) * bs, oy + (r + 1) * bs], fill=col)
    # Two pieces: white king + black knight (circles with letters).
    draw.ellipse([x0 + 78, y0 + 6, x0 + 104, y0 + 32], fill=CARD,
                 outline=INK, width=2)
    draw.text((x0 + 86, y0 + 9), "K", font=sans_b(16), fill=INK)
    draw.ellipse([x0 + 122, y0 + 8, x0 + 146, y0 + 32], fill=INK)
    draw.text((x0 + 130, y0 + 11), "N", font=sans_b(14), fill=CARD)
    draw.text((x1 - 32, y0 + 8), "1-1", font=sans_b(12), fill=CARD)


def mini_nfl(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(36, 110, 70))
    for i in range(3):
        draw.line([x0, y0 + 10 + i * 12, x1, y0 + 10 + i * 12],
                  fill=(52, 132, 88), width=5)
    # Brown ball, left; text right.
    bx, by = x0 + 30, y0 + 20
    draw.ellipse([bx - 12, by - 7, bx + 12, by + 7], fill=(120, 72, 32),
                 outline=CARD, width=1)
    draw.line([bx - 6, by, bx + 6, by], fill=CARD, width=1)
    draw.text((x0 + 52, y0 + 10), "3 GAMES", font=sans_b(11), fill=CARD)
    draw.text((x0 + 52, y0 + 24), "1pm ET", font=sans(9),
              fill=(200, 230, 210))


def mini_uel(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(186, 84, 22))
    for i in range(3):
        draw.line([x0, y0 + 10 + i * 12, x1, y0 + 10 + i * 12],
                  fill=(205, 105, 40), width=5)
    # Ball.
    bx, by = x0 + 30, y0 + 20
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=CARD)
    draw.polygon([(bx, by - 6), (bx + 5, by - 2), (bx + 3, by + 5),
                  (bx - 3, by + 5), (bx - 5, by - 2)], fill=INK)
    draw.text((x0 + 52, y0 + 12), "18 GAMES", font=sans_b(11), fill=CARD)


def mini_taiwan(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(226, 232, 238))
    draw.rectangle([x0 + 14, y0 + 6, x0 + 96, y1 - 6], fill=CARD,
                   outline=(150, 150, 150), width=1)
    for i in range(3):
        draw.line([x0 + 20, y0 + 12 + i * 7, x0 + 90, y0 + 12 + i * 7],
                  fill=(180, 180, 180), width=2)
    draw.text((x0 + 102, y0 + 20), "15%", font=sans_b(18), fill=RED)


def mini_india(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(255, 153, 51))
    draw.rectangle([x0, y0 + 13, x1, y0 + 27], fill=CARD)
    draw.rectangle([x0, y0 + 27, x1, y1], fill=(19, 136, 8))
    # Chakra wheel, centre of the white band.
    cx, cy = (x0 + x1) // 2, y0 + 20
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=NAVY, width=2)
    for k in range(8):
        ang = k * math.pi / 4
        draw.line([cx, cy, cx + 6 * math.cos(ang),
                   cy + 6 * math.sin(ang)], fill=NAVY, width=1)
    draw.text((x0 + 8, y1 - 12), "26 NOV", font=sans_b(9), fill=CARD)


def mini_wallst(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(16, 28, 44))
    # Sharp dip, then the claw-back.
    pts = [(x0 + 10, y0 + 12), (x0 + 70, y0 + 10), (x0 + 110, y0 + 30),
           (x0 + 150, y0 + 22), (x1 - 10, y0 + 10)]
    draw.line(pts, fill=(74, 222, 128), width=3, joint="curve")
    draw.text((x0 + 10, y1 - 16), "DOW +0.33%", font=sans_b(11),
              fill=(74, 222, 128))
    draw.text((x1 - 58, y0 + 4), "WILD DAY", font=sans_b(8),
              fill=(190, 205, 220))


def mini_parade(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    draw.rectangle([x0, y0 + 28, x1, y1], fill=(120, 110, 96))
    for bx, bh in ((x0 + 8, 16), (x0 + 30, 22), (x0 + 150, 18),
                   (x0 + 172, 12)):
        draw.rectangle([bx, y1 - 2 - bh, bx + 18, y1 - 2],
                       fill=(90, 80, 64))
    # Red balloon + strings.
    draw.ellipse([x0 + 78, y0 + 2, x0 + 118, y0 + 22], fill=RED)
    draw.line([x0 + 88, y0 + 22, x0 + 84, y0 + 30], fill=INK, width=1)
    draw.line([x0 + 108, y0 + 22, x0 + 112, y0 + 30], fill=INK, width=1)
    draw.text((x0 + 8, y0 + 4), "NYC", font=sans_b(11), fill=RED_DARK)


def mini_nepal(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    draw.polygon([(x0, y1), (x0 + 55, y0 + 4), (x0 + 110, y1)],
                 fill=(90, 80, 64))
    draw.polygon([(x0 + 40, y0 + 12), (x0 + 55, y0 + 4), (x0 + 70, y0 + 12)],
                 fill=CARD)
    draw.polygon([(x0 + 90, y1), (x0 + 140, y0 + 10), (x1, y1)],
                 fill=(120, 110, 96))
    draw.text((x0 + 8, y0 + 4), "Rs 15,000 CR", font=sans_b(11), fill=INK)


def mini_emirates(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    draw.ellipse([x0 + 8, y0 + 4, x0 + 34, y0 + 12], fill=CARD)
    draw.ellipse([x0 + 40, y0 + 8, x0 + 58, y0 + 14], fill=CARD)
    # Plane: fuselage + wing + tail.
    draw.polygon([(x0 + 60, y0 + 20), (x0 + 170, y0 + 20),
                  (x0 + 182, y0 + 25), (x0 + 60, y0 + 25)],
                 fill=(24, 44, 74))
    draw.polygon([(x0 + 100, y0 + 25), (x0 + 120, y0 + 25),
                  (x0 + 112, y0 + 34), (x0 + 96, y0 + 34)],
                 fill=(24, 44, 74))
    draw.polygon([(x0 + 62, y0 + 20), (x0 + 74, y0 + 20),
                  (x0 + 70, y0 + 10), (x0 + 64, y0 + 10)],
                 fill=(24, 44, 74))
    draw.text((x1 - 40, y0 + 26), "No.1", font=sans_b(12), fill=GOLD)


# ------------------------------------------------------------------
# World map: continents as (lon, lat) outlines, projected into the
# map box (x 20..316, y 650..852). Pins are placed by lon/lat too,
# nudged a few px where two stories share a crowded corner.
# ------------------------------------------------------------------

MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 20, 650, 316, 852


def _ll(lon, lat):
    x = MAP_X0 + (lon + 170) / 360 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (75 - lat) / 130 * (MAP_Y1 - MAP_Y0)
    return (int(x), int(y))


CONTINENTS_LL = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69),
     (-85, 66), (-80, 73), (-65, 60), (-55, 47), (-70, 42),
     (-75, 35), (-80, 26), (-85, 30), (-95, 29), (-97, 26),
     (-105, 20), (-110, 24), (-125, 40), (-125, 49), (-140, 60),
     (-155, 58), (-165, 60)],
    # Greenland
    [(-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-58, 70)],
    # South America
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-73, -40),
     (-72, -20), (-77, -12), (-80, -3)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (28, 70), (20, 70), (15, 68), (12, 65), (5, 60), (5, 58),
     (-2, 57), (-5, 50), (-9, 43), (-10, 37)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (32, 20), (38, 18), (43, 12), (48, 11), (51, 10), (44, 0),
     (40, -10), (35, -18), (32, -26), (28, -33), (20, -35),
     (15, -28), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8),
     (-17, 15), (-16, 20), (-15, 28), (-10, 31)],
    # Asia
    [(30, 62), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60),
     (160, 55), (150, 45), (142, 40), (135, 35), (127, 33),
     (122, 30), (120, 22), (110, 10), (105, 5), (100, 8), (95, 15),
     (90, 22), (85, 20), (80, 15), (75, 10), (72, 20), (66, 25),
     (60, 25), (55, 28), (50, 30), (48, 30), (43, 35), (38, 36),
     (35, 36), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -33),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
]

# Story number -> (lon, lat).
PINS_LL = {
    1: (139, 36),    # Tokyo, Nikkei futures
    2: (126, 39),    # Pyongyang, Kim nukes
    3: (-77, 39),    # Washington, tariffs
    4: (147, -9),    # Port Moresby, Bougainville
    5: (6, 46),      # Geneva, chess
    6: (-83, 42),    # Detroit, NFL Thanksgiving
    7: (2, 49),      # Paris, Europa League
    8: (121.5, 25),  # Taipei, 15% tariff
    9: (77, 28.6),   # New Delhi, Constitution Day
    10: (-74, 41),   # New York, Wall St
    11: (-74, 40.7), # New York, Macy's parade
    12: (85.3, 27.7),# Kathmandu, Nepal package
    13: (55.3, 25.2),# Dubai, Emirates
}

# Pixel nudges (dx, dy) applied after projection, to keep crowded
# European / East-African / Pacific pins from sitting on each other.
PIN_NUDGE = {
    2: (6, -4), 5: (9, 7), 6: (-8, -6), 7: (9, -7), 8: (-6, 4),
    9: (-8, -4), 10: (14, -10), 11: (-14, 10), 12: (6, 4), 13: (-6, 6),
}


def draw_map(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=OCEAN, outline=BORDER, width=1)
    for poly in CONTINENTS_LL:
        draw.polygon([_ll(lon, lat) for lon, lat in poly], fill=LAND,
                     outline=(190, 178, 148))
    for num, (lon, lat) in sorted(PINS_LL.items()):
        px, py = _ll(lon, lat)
        dx, dy = PIN_NUDGE.get(num, (0, 0))
        px, py = px + dx, py + dy
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                     outline=CARD, width=1)
        label = str(num)
        tw = text_w(draw, label, sans_b(9))
        draw.text((px - tw / 2, py - 7), label, font=sans_b(9),
                  fill=(255, 255, 255))


def num_circle(draw, x, y, num, r=11):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    label = str(num)
    tw = text_w(draw, label, sans_b(10))
    draw.text((x - tw / 2, y - 7), label, font=sans_b(10),
              fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # ---- masthead --------------------------------------------------
    d.text((MARGIN, 22), "THE WORLD ON ONE PAGE", font=sans_b(13),
           fill=RED)
    centre = "DAY 330 OF 2026"
    d.text(((W - text_w(d, centre, sans_b(12))) / 2, 23), centre,
           font=sans_b(12), fill=INK)
    right = "43 STORIES  ·  7 REGIONS  ·  THURSDAY'S NEWS"
    d.text((W - MARGIN - text_w(d, right, sans_b(12)), 23), right,
           font=sans_b(12), fill=INK)
    rule(d, MARGIN, 42, W - MARGIN, color=INK, width=2)
    d.text((MARGIN, 48), "Thursday 26 November 2026", font=serif_b(42),
           fill=INK)
    rule(d, MARGIN, 104, W - MARGIN, color=RED, width=2)

    # ---- region strip ----------------------------------------------
    regions = [
        ("ASIA 20", 160, (166, 30, 30)),
        ("EUROPE 4", 130, (31, 78, 121)),
        ("MID EAST 1", 150, (150, 90, 40)),
        ("AMERICAS 11", 150, (40, 110, 70)),
        ("AFRICA 0", 160, (120, 80, 140)),
        ("OCEANIA 5", 150, (30, 120, 130)),
        ("WORLD 2", 84, (90, 90, 90)),
    ]
    rx = MARGIN
    for label, w, col in regions:
        d.rectangle([rx, 110, rx + w, 130], fill=col)
        tw = text_w(d, label, sans_b(10))
        d.text((rx + (w - tw) / 2, 115), label, font=sans_b(10),
               fill=(255, 255, 255))
        rx += w

    # ---- THE DAY IN UTC --------------------------------------------
    d.rectangle([MARGIN, 134, MARGIN + 110, 160], fill=RED)
    d.text((MARGIN + 8, 136), "THE DAY", font=sans_b(10),
           fill=(255, 255, 255))
    d.text((MARGIN + 8, 147), "IN UTC", font=sans_b(10),
           fill=(255, 255, 255))
    slots = [
        ("00:12 UTC", "Kospi opens lower"),
        ("00:30 UTC", "Taiwan: 15% rate"),
        ("06:00 HKT", "Asia briefing: tariffs"),
        ("15:00 CET", "Chess Game 3"),
        ("17:45 GMT", "Europa League"),
        ("18:00 UTC", "NFL Thanksgiving"),
    ]
    sx = MARGIN + 116
    sw = (W - MARGIN - sx) // 6
    for i, (part, story) in enumerate(slots):
        x = sx + i * sw
        if i:
            d.line([x - 4, 136, x - 4, 158], fill=BORDER, width=1)
        d.text((x, 136), part, font=sans_b(9), fill=RED)
        d.text((x, 147), story, font=sans(9), fill=INK)

    # ---- THE DAY IN NUMBERS ----------------------------------------
    d.rectangle([MARGIN, 164, MARGIN + 150, 190], fill=INK)
    d.text((MARGIN + 8, 168), "THE DAY", font=sans_b(10),
           fill=(255, 255, 255))
    d.text((MARGIN + 8, 179), "IN NUMBERS", font=sans_b(10),
           fill=(255, 255, 255))
    numbers = [
        ("57,370", "Nikkei futures"),
        ("22,149", "Hang Seng futures"),
        ("50,183", "Dow, Wed close"),
        ("14", "tariff partners"),
        ("89", "MPs for Bougainville"),
        ("20%", "China tariff rate"),
    ]
    nx = MARGIN + 156
    nw = (W - MARGIN - nx) // 6
    for i, (num, label) in enumerate(numbers):
        x = nx + i * nw
        if i:
            d.line([x - 4, 166, x - 4, 188], fill=BORDER, width=1)
        d.text((x, 166), num, font=sans_b(16), fill=RED)
        d.text((x, 183), label, font=sans(9), fill=INK_SOFT)

    # ---- 3 leads ----------------------------------------------------
    leads = [
        (1, "MARKETS · TOKYO", "CNBC · AP", art_lead_steady,
         "REPORTED",
         "Asia steadies after Wall St fightback",
         "Nikkei futures point up 0.6% and Hang Seng futures 0.8% "
         "as Asia opens with the US shut for Thanksgiving."),
        (2, "KOREA · PYONGYANG", "REUTERS · KCNA", art_lead_nukes,
         "REPORTED",
         "Kim: deploy tactical nukes wider",
         "North Korea will deploy tactical nuclear weapons across "
         "more domains and expand nuclear-material output, KCNA "
         "reports on Thursday."),
        (3, "TRADE · WASHINGTON", "REUTERS", art_lead_tariffs,
         "REPORTED",
         "Asia counts the tariff cost",
         "Taiwan says its 15% rate is the lowest tier; China "
         "faces 20%, rising to 40% if the truce terms are broken."),
    ]
    lw = 320
    for i, (num, tag, src, art, chip, head, body) in enumerate(leads):
        x0 = MARGIN + i * (lw + 12)
        x1 = x0 + lw
        art(d, x0, 196, x1, 286)
        d.rectangle([x0, 196, x1, 286], outline=BORDER, width=1)
        num_circle(d, x0 + 11, 299, num)
        d.text((x0 + 28, 292), tag, font=sans_b(11), fill=RED)
        sw_ = text_w(d, src, sans(9))
        d.text((x1 - sw_, 293), src, font=sans(9), fill=INK_SOFT)
        hf = serif_b(20)
        hl = wrap_text(d, head, hf, lw - 4)
        draw_lines(d, x0, 312, hl[:2], hf, INK, 22)
        bf = sans(12)
        bl = wrap_text(d, body, bf, lw - 4)
        draw_lines(d, x0, 358, bl[:3], bf, INK_SOFT, 15)

    # ---- 10 picture stories, 5 x 2 ----------------------------------
    pics = [
        (4, "OCEANIA", "Bougainville debate rolls on",
         "Parliament debate continues; 89 of 118 MPs needed.",
         mini_bougainville, "BUSINESS MELANESIA", "ONGOING"),
        (5, "EUROPE", "Chess Game 3 today",
         "Sindarov White in Geneva, score 1-1, 15:00 CET.",
         mini_chess, "CHESSBASE", "TODAY"),
        (6, "AMERICAS", "Thanksgiving: 3 NFL games",
         "Bears-Lions, Eagles-Cowboys, Chiefs-Bills.",
         mini_nfl, "NBC", "TODAY"),
        (7, "EUROPE", "Europa League: 18 games",
         "Milan at Olympiacos; Palace host Real Sociedad.",
         mini_uel, "UEFA", "TODAY"),
        (8, "ASIA", "Taiwan: 15% is the floor",
         "Lowest tier with Japan, Korea, EU; not stacked.",
         mini_taiwan, "EXEC. YUAN", "REPORTED"),
        (9, "ASIA", "India marks Constitution Day",
         "IITs add 6,000 seats in robotics, AI and space.",
         mini_india, "INDIAN PRESS", "TODAY"),
        (10, "AMERICAS", "Wall St claws back",
         "Dow +0.33% after a 1,100-point slide; Nasdaq -0.62%.",
         mini_wallst, "REUTERS", "REPORTED"),
        (11, "AMERICAS", "Macy's parade steps off",
         "Balloons over NYC; Dog Show follows the football.",
         mini_parade, "NBC", "TODAY"),
        (12, "ASIA", "Nepal gets Rs 15,000 cr",
         "India package after Modi-Shah talks in Delhi.",
         mini_nepal, "INDIAN PRESS", "REPORTED"),
        (13, "MID EAST", "Emirates tops the skies",
         "Named world's best airline in global rankings.",
         mini_emirates, "GLOBAL RANKINGS", "REPORTED"),
    ]
    pw = 190
    chip_fill = {"OFFICIAL": BLUE, "REPORTED": GREEN, "ONGOING": GREY,
                 "TODAY": NAVY, "CLAIM": RED}
    for i, (num, tag, head, body, art, src, chip) in enumerate(pics):
        col, row = i % 5, i // 5
        x0 = MARGIN + col * (pw + 8)
        y0 = 410 + row * 108
        x1 = x0 + pw
        art(d, x0, y0, x1, y0 + 40)
        d.rectangle([x0, y0, x1, y0 + 40], outline=BORDER, width=1)
        chip_right(d, x1, y0, chip, chip_fill[chip])
        num_circle(d, x0 + 9, y0 + 51, num, r=9)
        d.text((x0 + 22, y0 + 44), tag, font=sans_b(9), fill=RED)
        sw_ = text_w(d, src, sans(8))
        d.text((x1 - sw_, y0 + 45), src, font=sans(8), fill=INK_SOFT)
        hf = sans_b(12)
        hl = wrap_text(d, head, hf, pw - 4)
        draw_lines(d, x0, y0 + 60, hl[:2], hf, INK, 14)
        bf = sans(10)
        bl = wrap_text(d, body, bf, pw - 4)
        draw_lines(d, x0, y0 + 88, bl[:2], bf, INK_SOFT, 12)

    # ---- map + briefs ------------------------------------------------
    d.text((MARGIN, 632), "WHERE IT HAPPENED", font=sans_b(13), fill=RED)
    draw_map(d, MARGIN, 650, MARGIN + 296, 852)
    legend = [
        ((166, 30, 30), "Asia 20"),
        ((31, 78, 121), "Europe 4"),
        ((150, 90, 40), "Mid East 1"),
        ((40, 110, 70), "Americas 11"),
        ((120, 80, 140), "Africa 0"),
        ((30, 120, 130), "Oceania 5"),
    ]
    lx, ly = MARGIN, 858
    for col, label in legend:
        d.rectangle([lx, ly + 2, lx + 10, ly + 12], fill=col)
        d.text((lx + 14, ly), label, font=sans(10), fill=INK)
        lx += 14 + int(text_w(d, label, sans(10))) + 12
        if lx > MARGIN + 260:
            lx = MARGIN
            ly += 16

    d.text((328, 632), "ALSO ON THURSDAY 26 NOVEMBER · 30 MORE",
           font=sans_b(13), fill=RED)
    briefs = [
        (14, "Kospi", "opens lower again"),
        (15, "China", "tariff reply awaited"),
        (16, "Nikkei fut", "57,370 (+0.6%)"),
        (17, "Hang Seng fut", "22,149 (+0.8%)"),
        (18, "ASX", "+0.15% at the open"),
        (19, "Taiwan", "15%, lowest tier"),
        (20, "IPL", "1,220 players register"),
        (21, "Flipkart", "CEO steps down in Dec"),
        (22, "Hasina", "seeks return Dec 16"),
        (23, "India space", "$9bn to $45bn"),
        (24, "PNG", "2027 Budget due today"),
        (25, "PNG Budget", "balanced plan vowed"),
        (26, "Dog Show", "Thanksgiving classic"),
        (27, "US markets", "shut Thu, short Fri"),
        (28, "India", "human control over war AI"),
        (29, "India", "condemns Riyadh attack"),
        (30, "Anand Kumar", "honoured in Japan"),
        (31, "Brazil", "Wolbachia cuts cases 68%"),
        (32, "Chess", "$2.5m crown at stake"),
        (33, "Cricket", "Rising Stars semis today"),
        (34, "Island school", "tuition in coconuts"),
        (35, "Detroit", "87th Thanksgiving game"),
        (36, "Bills", "9-1 host Chiefs 8-2"),
        (37, "College", "TCU vs Texas Tech 8pm ET"),
        (38, "Chess", "12 games left, first to 7.5"),
        (39, "Bougainville", "97.7% said yes in 2019"),
        (40, "Tariffs", "India up to 17%"),
        (41, "Tariffs", "EU, Japan, Korea ~15%"),
        (42, "Tariffs", "China 20%, may rise to 40%"),
        (43, "Black Friday", "Broncos at Steelers"),
    ]
    for i, (num, place, fact) in enumerate(briefs):
        col, row = i // 10, i % 10
        bx = 328 + col * 226
        by = 650 + row * 18
        d.text((bx, by), f"{num}", font=sans_b(11), fill=RED)
        nw_ = text_w(d, f"{num} ", sans_b(11))
        d.text((bx + nw_, by), place, font=sans_b(11), fill=INK)
        pw_ = text_w(d, place, sans_b(11))
        d.text((bx + nw_ + pw_, by), f": {fact}", font=sans(11),
               fill=INK_SOFT)

    # ---- DATE CHECK --------------------------------------------------
    d.rectangle([MARGIN, 910, W - MARGIN, 1000], outline=RED, width=2)
    d.rectangle([MARGIN, 910, MARGIN + 96, 926], fill=RED)
    d.text((MARGIN + 8, 913), "DATE CHECK", font=sans_b(11),
           fill=(255, 255, 255))
    dc = ("Left out as Wed 25 Nov news: US tariff proposal (14 "
          "partners) · PCE +3.8%, GDP +4.3% · UCL: Barca 4-1 Sabah, "
          "Liverpool 3-0 Brugge, Lille 2-1 Bayern, PSG 2-2 Roma · "
          "Chess Game 2 draw · Ramaphosa wins Phala Phala case · "
          "Bangladesh wage +36% · Sudan strikes (Tue attack, 19 "
          "dead) · Gaza: Abu al-Ouf killed · Shenzhou-24, first "
          "Pakistani astronaut · Houthi claim on Ras Tanura · "
          "Saudi budget $371bn · BepiColombo at Mercury · Suez "
          "revenues double · Petrobras $122bn · Venezuela debt "
          "$237.5bn · Steelers release Rodgers · Deere reports · "
          "Fed Beige Book · German GDP · BoE Bailey · Australia "
          "inflation · US 7-yr auction · Swiss envoy expelled. "
          "Not yet (drawn Thu 07:45 WIB / 00:45 UTC): Chess Game 3 15:00 CET · "
          "UEL tonight · NFL tripleheader · PNG Budget · China "
          "reply. Sources: Reuters, AP, CNBC, UEFA, ChessBase. "
          "Maps + drawings are original vector art.")
    lines = wrap_text(d, dc, sans(10), (W - MARGIN) - (MARGIN + 108))
    draw_lines(d, MARGIN + 108, 913, lines[:6], sans(10), INK, 12)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "entry.png")
    img.save(out)
    print(f"Wrote {out} ({os.path.getsize(out)} bytes, 1024x1024)")


if __name__ == "__main__":
    main()
