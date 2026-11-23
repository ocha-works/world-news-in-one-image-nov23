#!/usr/bin/env python3
"""Draw the front page of 23 November 2026 as one 1024x1024 PNG.

Every story on the page happened, or was first reported, on Monday
23 November 2026, and each was cross-checked against at least two
news outlets (see SOURCES.md). Run it to (re)generate entry.png:

    python3 generate_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
GREY = (90, 86, 78)
LIGHT = (232, 226, 212)
DARKBAND = (24, 30, 38)
ORANGE = (214, 106, 24)
GOLD = (198, 154, 38)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons

def icon_ship(draw, x, y, s):
    """Corvette at sea with an explosion burst above its stern."""
    import math
    sea_y = y + int(s * 0.66)
    draw.rectangle([x, sea_y, x + s, sea_y + 3], fill=BLUE)
    draw.rectangle([x, sea_y + 9, x + s, sea_y + 11], fill=BLUE)
    # hull: taller, with a raked bow
    draw.polygon([(x + 4, sea_y), (x + s - 4, sea_y),
                  (x + s - 22, sea_y - 22), (x + 22, sea_y - 22)], fill=INK)
    # superstructure and mast
    draw.rectangle([x + int(s * 0.34), sea_y - 46, x + int(s * 0.60), sea_y - 22],
                   fill=INK)
    draw.rectangle([x + int(s * 0.62), sea_y - 38, x + int(s * 0.74), sea_y - 22],
                   fill=INK)
    draw.line([(x + int(s * 0.47), sea_y - 46), (x + int(s * 0.47), sea_y - 62)],
              fill=INK, width=4)
    # explosion burst over the stern
    cx, cy = x + int(s * 0.80), sea_y - 52
    for r, col in ((34, ORANGE), (23, GOLD), (12, (240, 220, 120))):
        pts = []
        for i in range(12):
            ang = math.pi * i / 6
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=col)
    # small drone boat with wake, lower left
    draw.polygon([(x + 8, sea_y + 18), (x + 38, sea_y + 18),
                  (x + 32, sea_y + 27), (x + 14, sea_y + 27)], fill=RED)
    draw.line([(x + 40, sea_y + 22), (x + 58, sea_y + 22)], fill=RED, width=2)


def icon_building(draw, x, y, s):
    """Damaged apartment block with smoke."""
    bw, bh = int(s * 0.62), int(s * 0.72)
    bx, by = x + int(s * 0.1), y + s - bh
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(120, 116, 108))
    # broken corner
    draw.polygon([(bx + bw, by), (bx + bw, by + 26), (bx + bw - 26, by)],
                 fill=PAPER)
    # windows
    for r in range(3):
        for c in range(3):
            wx = bx + 8 + c * 22
            wy = by + 10 + r * 24
            draw.rectangle([wx, wy, wx + 12, wy + 14], fill=(40, 40, 40))
    # smoke
    for i, r in enumerate((10, 14, 18)):
        draw.ellipse([bx + bw - 6 + i * 8, by - 34 + i * 10,
                      bx + bw - 6 + i * 8 + r * 2, by - 34 + i * 10 + r * 2],
                     fill=(170, 166, 158))


def icon_satellite(draw, x, y, s):
    """Satellite on an orbit ring."""
    import math
    cx, cy = x + s // 2, y + s // 2
    draw.ellipse([x + 4, y + 12, x + s - 4, y + s - 12], outline=BLUE, width=3)
    # solar panels
    draw.rectangle([cx - 42, cy - 10, cx - 12, cy + 10], fill=BLUE)
    draw.rectangle([cx + 12, cy - 10, cx + 42, cy + 10], fill=BLUE)
    draw.line([(cx - 27, cy - 10), (cx - 27, cy + 10)], fill=(255, 255, 255),
              width=2)
    draw.line([(cx + 27, cy - 10), (cx + 27, cy + 10)], fill=(255, 255, 255),
              width=2)
    # body
    draw.rectangle([cx - 12, cy - 14, cx + 12, cy + 14], fill=INK)
    # antenna
    draw.line([(cx, cy - 14), (cx, cy - 28)], fill=INK, width=2)
    draw.ellipse([cx - 3, cy - 31, cx + 3, cy - 25], fill=RED)
    # small star
    sx, sy = x + s - 14, y + 10
    draw.polygon([(sx, sy - 6), (sx + 2, sy - 2), (sx + 6, sy), (sx + 2, sy + 2),
                  (sx, sy + 6), (sx - 2, sy + 2), (sx - 6, sy), (sx - 2, sy - 2)],
                 fill=GOLD)


def icon_assembly(draw, x, y, s):
    """Government building with columns."""
    bw = int(s * 0.8)
    bx = x + (s - bw) // 2
    by = y + int(s * 0.2)
    # pediment
    draw.polygon([(bx, by + 18), (bx + bw, by + 18), (bx + bw // 2, by)],
                 fill=INK)
    # columns
    for i in range(4):
        cx0 = bx + 8 + i * (bw - 16) // 3
        draw.rectangle([cx0, by + 22, cx0 + 10, by + int(s * 0.62)], fill=INK)
    # base
    draw.rectangle([bx, by + int(s * 0.62), bx + bw, by + int(s * 0.68)],
                   fill=INK)
    # flag
    draw.line([(bx + bw // 2, by - 16), (bx + bw // 2, by)], fill=INK, width=3)
    draw.polygon([(bx + bw // 2, by - 16), (bx + bw // 2 + 22, by - 11),
                  (bx + bw // 2, by - 6)], fill=RED)


def icon_care(draw, x, y, s):
    """House outline holding a heart: care for young and old."""
    import math
    hx, hy = x + s // 2, y + int(s * 0.55)
    # house
    draw.polygon([(x + 8, y + int(s * 0.45)), (x + s // 2, y + int(s * 0.18)),
                  (x + s - 8, y + int(s * 0.45))], outline=INK, width=4)
    draw.rectangle([x + 12, y + int(s * 0.45), x + s - 12, y + int(s * 0.88)],
                   outline=INK, width=4)
    # heart
    r = 12
    draw.ellipse([hx - r - 6, hy - 8, hx - 6 + r, hy + 8], fill=RED)
    draw.ellipse([hx + 6 - r, hy - 8, hx + 6 + r, hy + 8], fill=RED)
    draw.polygon([(hx - 18, hy - 2), (hx + 18, hy - 2), (hx, hy + 20)], fill=RED)
    # small figures: elder with cane, child
    draw.ellipse([x + 16, y + int(s * 0.72), x + 26, y + int(s * 0.82)],
                 fill=BLUE)
    draw.ellipse([x + s - 26, y + int(s * 0.74), x + s - 16, y + int(s * 0.84)],
                 fill=BLUE)


def icon_globe(draw, x, y, s):
    """Globe with rising heat arrow and a cracked ground line."""
    cx, cy = x + s // 2, y + int(s * 0.45)
    r = int(s * 0.3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 222, 235))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=BLUE, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=BLUE, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    # rising arrow
    ax = x + s - 16
    draw.line([(ax, y + s - 26), (ax, y + 12)], fill=RED, width=4)
    draw.polygon([(ax - 7, y + 22), (ax + 7, y + 22), (ax, y + 8)], fill=RED)
    # cracked ground
    gy = y + s - 12
    draw.line([(x + 6, gy), (x + s // 3, gy - 4), (x + s // 2, gy + 2),
               (x + 2 * s // 3, gy - 3), (x + s - 6, gy)], fill=INK, width=3)


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    X1 = W - M

    # ---- masthead
    f_title = font(SERIF_B, 66)
    f_date = font(SANS_B, 30)
    f_tag = font(SANS, 17)
    d.text((W // 2, 30), "THE WORLD TODAY", font=f_title, fill=INK,
           anchor="ma")
    rule(d, M, 108, X1, 3)
    d.text((W // 2, 118), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=RED,
           anchor="ma")
    d.text((W // 2, 152), "One day's world news, in one image  •  All events of Monday 23 November 2026",
           font=f_tag, fill=GREY, anchor="ma")
    rule(d, M, 182, X1, 2)

    # ---- lead story: Ukraine sinks Russian warship off Libya
    ly = 196
    lh = 212
    d.rectangle([M, ly, X1, ly + lh], outline=INK, width=2)
    d.rectangle([M, ly, X1, ly + lh], fill=(255, 255, 255))
    d.rectangle([M, ly, X1, ly + lh], outline=INK, width=2)
    tx = M + 18
    f_kick = font(SANS_B, 16)
    f_head = font(SERIF_B, 37)
    f_body = font(SANS, 18)
    d.text((tx, ly + 12), "UKRAINE  •  LIBYA  —  LEAD STORY", font=f_kick,
           fill=RED)
    d.text((tx, ly + 38), "Kyiv says it sank a Russian", font=f_head, fill=INK)
    d.text((tx, ly + 82), "warship off Libya", font=f_head, fill=INK)
    body = ("President Zelenskyy said seven Ukrainian sea drones sank the "
            "corvette Merkury at Benghazi and hit the cargo ship MV Angara. "
            "A Ka-27 helicopter on board was destroyed too. The strike, "
            "2,400 km from the front line, shows the war spreading far "
            "beyond Ukraine.")
    draw_wrapped(d, tx, ly + 126, body, f_body, 620, leading=22)
    icon_ship(d, X1 - 262, ly + 30, 232)

    # ---- two rows of two panels
    f_pk = font(SANS_B, 14)
    f_ph = font(SERIF_B, 23)
    f_pb = font(SANS, 16)
    panels = [
        ("RUSSIA  •  UKRAINE",
         "Russian strike kills 11 in Kyiv region",
         "Rescuers pulled bodies from a block of flats in Dymer after "
         "the attack. The toll rose to 11 on Monday, the regional "
         "governor said.", icon_building, BLUE),
        ("SPACE  •  SECURITY",
         "NATO warns of a nuclear-armed satellite",
         "German media report Russia's Sputnik-S could launch this year, "
         "perhaps in December. The Kremlin dismissed the report on "
         "Monday.", icon_satellite, BLUE),
        ("SOUTH KOREA",
         "Seoul reshuffles security chiefs",
         "President Lee named a new foreign minister, a new unification "
         "minister and Kang Kum-sil as the country's first female spy "
         "chief.", icon_assembly, BLUE),
        ("CHINA",
         "Beijing sets 2030 care targets",
         "China unveiled a plan for older people and children: community "
         "eldercare to reach 70% and childcare places to grow, with "
         "2,000 nursing homes renovated.", icon_care, BLUE),
    ]
    col_w = (W - 2 * M - 16) // 2
    row_y = [420, 606]
    row_h = 174
    for i, (kick, head, body, icon, _c) in enumerate(panels):
        col = i % 2
        row = i // 2
        x0 = M + col * (col_w + 16)
        y0 = row_y[row]
        d.rectangle([x0, y0, x0 + col_w, y0 + row_h], outline=INK, width=2)
        d.rectangle([x0, y0, x0 + col_w, y0 + row_h], fill=(255, 255, 255))
        d.rectangle([x0, y0, x0 + col_w, y0 + row_h], outline=INK, width=2)
        tx = x0 + 14
        d.text((tx, y0 + 10), kick, font=f_pk, fill=RED)
        hy = draw_wrapped(d, tx, y0 + 32, head, f_ph, col_w - 118, leading=27)
        draw_wrapped(d, tx, hy + 4, body, f_pb, col_w - 118, leading=20)
        icon(d, x0 + col_w - 104, y0 + 40, 92)

    # ---- sixth panel: COP31 fallout (full width)
    y0 = 792
    h0 = 78
    d.rectangle([M, y0, X1, y0 + h0], outline=INK, width=2)
    d.rectangle([M, y0, X1, y0 + h0], fill=(255, 255, 255))
    d.rectangle([M, y0, X1, y0 + h0], outline=INK, width=2)
    d.text((M + 14, y0 + 9), "CLIMATE  •  AFTER COP31", font=f_pk, fill=RED)
    d.text((M + 14, y0 + 30),
           "Pacific nations voice despair as the climate talks collapse",
           font=font(SERIF_B, 24), fill=INK)
    d.text((M + 14, y0 + 58),
           "Australia faced a backlash at home after negotiators left Antalya with no deal.",
           font=f_pb, fill=INK)
    icon_globe(d, X1 - 92, y0 + 4, 72)

    # ---- also today ticker
    ty = 882
    th = 96
    d.rectangle([M, ty, X1, ty + th], fill=DARKBAND)
    d.text((M + 14, ty + 10), "ALSO TODAY", font=font(SANS_B, 16),
           fill=(240, 200, 90))
    f_tick = font(SANS, 15)
    tick = ("Shuri Castle's restored main hall opens in Okinawa  •  "
            "Thailand plans to ban chemical exports to fight pollution  •  "
            "Tom Jackson, ex-Broncos star and ESPN voice, dies at 75  •  "
            "U.S. tracked Alice Huang's contacts with a Chinese spy agency, "
            "the NYT reports.")
    draw_wrapped(d, M + 14, ty + 34, tick, f_tick, X1 - M - 28,
                 fill=(235, 232, 225), leading=19)

    # ---- footer
    d.text((W // 2, 988),
           "Sources: Reuters, Al Jazeera, CNN, Yonhap, Xinhua, AFP, Japan Times  •  "
           "Drawn in code  •  Monday 23 November 2026",
           font=font(SANS, 13), fill=GREY, anchor="ma")
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
