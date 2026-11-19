#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: 'GTA VI IS OUT / 13 YEARS LATER... /
MY AGENT GOT PAID ON make.fun'.

The picture is drawn from scratch with Pillow (local only, no network, no
randomness, no clock): a Vice City sunset street, Jason and Lucia walking in
as the two protagonists, and the make.fun ghost floating beside them as the
third protagonist, holding its magenta star coin. The ghost is drawn from
the press-kit's mark description (white body, thick black outline, two black
four-pointed sparkle eyes, round little hand, magenta coin with a white
star) -- the press-kit PNG/SVG files are reference only and are never copied
into this repository.

Run:  python3 draw_meme.py   ->  writes meme.png (1024x1024) next to it.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme.png")
W, H = 1024, 1024

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)
YELLOW = (255, 233, 168)


def font(size):
    return ImageFont.truetype(BOLD, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def sparkle_points(cx, cy, r):
    """A four-pointed sparkle: diamond with pinched sides."""
    return [
        (cx, cy - r),
        (cx + r * 0.28, cy - r * 0.28),
        (cx + r, cy),
        (cx + r * 0.28, cy + r * 0.28),
        (cx, cy + r),
        (cx - r * 0.28, cy + r * 0.28),
        (cx - r, cy),
        (cx - r * 0.28, cy - r * 0.28),
    ]


def text_outline(draw, xy, text, fnt, fill, outline=INK, width=6):
    x, y = xy
    for dx in range(-width, width + 1):
        for dy in range(-width, width + 1):
            if dx * dx + dy * dy <= width * width:
                draw.text((x + dx, y + dy), text, font=fnt, fill=outline)
    draw.text((x, y), text, font=fnt, fill=fill)


def text_centred(draw, y, text, fnt, fill, outline=INK, width=6):
    w = draw.textlength(text, font=fnt)
    text_outline(draw, ((W - w) / 2, y), text, fnt, fill, outline, width)


def draw_palm(draw, x, base_y, scale, flip=False):
    """A black palm-tree silhouette."""
    s = scale
    top_x, top_y = x, base_y - 210 * s
    # trunk: slightly curved, drawn as a thick polyline
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((x + (14 * s * t * t) * (1 if not flip else -1),
                    base_y - 210 * s * t))
    draw.line(pts, fill=INK, width=int(16 * s))
    # fronds: long tapered triangles fanning from the crown
    for ang_deg, ln in [(-165, 120), (-135, 140), (-105, 150),
                        (-75, 150), (-45, 140), (-15, 120)]:
        ang = math.radians(ang_deg if not flip else -180 - ang_deg)
        tip = (top_x + ln * s * math.cos(ang), top_y + ln * s * math.sin(ang) * 0.55)
        side = math.radians(ang_deg + 90)
        wdt = 13 * s
        base1 = (top_x + wdt * math.cos(side), top_y + wdt * math.sin(side) * 0.5)
        base2 = (top_x - wdt * math.cos(side), top_y - wdt * math.sin(side) * 0.5)
        draw.polygon([base1, tip, base2], fill=INK)
    # coconuts
    draw.ellipse([top_x - 12 * s, top_y - 2 * s, top_x + 2 * s, top_y + 12 * s],
                 fill=INK)
    draw.ellipse([top_x + 2 * s, top_y - 2 * s, top_x + 16 * s, top_y + 12 * s],
                 fill=INK)


def draw_ghost(draw, cx, top_y, w, h):
    """The make.fun ghost, drawn from scratch.

    White body with a thick black outline, two black four-pointed sparkle
    eyes, a round little white hand, and a magenta coin with a white star
    held up at its side. (cx, top_y) is the top-centre of the body; w/h
    are the body width/height, coin included in the width.
    """
    x0, y0 = cx - w / 2, top_y
    x1, y1 = cx + w / 2, top_y + h
    ow = max(7, int(w * 0.055))  # outline width
    # --- black outline silhouette, then white body inset by ow ---
    for inset, col in [(0, INK), (ow, WHITE)]:
        bx0, by0 = x0 + inset, y0 + inset
        bx1, by1 = x1 - inset, y1 - inset
        bw, bh = bx1 - bx0, by1 - by0
        draw.ellipse([bx0, by0, bx1, by0 + bw * 0.95], fill=col)
        draw.rectangle([bx0, by0 + bw * 0.45, bx1, by1 - bh * 0.10], fill=col)
        # wavy bottom: three bumps
        bump_r = bw / 6
        for i in range(3):
            bcx = bx0 + bw * (1 / 6 + i / 3)
            draw.ellipse([bcx - bump_r, by1 - bh * 0.16 - bump_r,
                          bcx + bump_r, by1 - bh * 0.16 + bump_r], fill=col)
    # --- sparkle eyes ---
    eye_y = top_y + h * 0.38
    for ex in (cx - w * 0.20, cx + w * 0.13):
        draw.polygon(sparkle_points(ex, eye_y, w * 0.085), fill=INK)
    # --- magenta coin with white star, upper right ---
    coin_cx, coin_cy, coin_r = cx + w * 0.42, top_y + h * 0.30, w * 0.19
    draw.ellipse([coin_cx - coin_r - 6, coin_cy - coin_r - 6,
                  coin_cx + coin_r + 6, coin_cy + coin_r + 6], fill=INK)
    draw.ellipse([coin_cx - coin_r, coin_cy - coin_r,
                  coin_cx + coin_r, coin_cy + coin_r], fill=MAGENTA)
    draw.polygon(star_points(coin_cx, coin_cy, coin_r * 0.72, coin_r * 0.30),
                 fill=WHITE)
    # --- round little hand under the coin ---
    hand_cx, hand_cy, hand_r = cx + w * 0.34, top_y + h * 0.62, w * 0.115
    draw.ellipse([hand_cx - hand_r - 5, hand_cy - hand_r - 5,
                  hand_cx + hand_r + 5, hand_cy + hand_r + 5], fill=INK)
    draw.ellipse([hand_cx - hand_r, hand_cy - hand_r,
                  hand_cx + hand_r, hand_cy + hand_r], fill=WHITE)


def draw_man(draw, cx, feet_y, h):
    """Jason: flat dark silhouette with a teal shirt and cap."""
    u = h / 100.0
    # legs
    draw.polygon([(cx - 13 * u, feet_y), (cx - 4 * u, feet_y),
                  (cx - 7 * u, feet_y - 46 * u), (cx - 15 * u, feet_y - 46 * u)],
                 fill=(30, 30, 46))
    draw.polygon([(cx + 4 * u, feet_y), (cx + 13 * u, feet_y),
                  (cx + 15 * u, feet_y - 46 * u), (cx + 7 * u, feet_y - 46 * u)],
                 fill=(30, 30, 46))
    # torso (teal shirt)
    draw.polygon([(cx - 17 * u, feet_y - 44 * u), (cx + 17 * u, feet_y - 44 * u),
                  (cx + 13 * u, feet_y - 82 * u), (cx - 13 * u, feet_y - 82 * u)],
                 fill=(16, 120, 130))
    # arms
    draw.line([(cx - 15 * u, feet_y - 78 * u), (cx - 22 * u, feet_y - 48 * u)],
              fill=(16, 120, 130), width=int(9 * u))
    draw.line([(cx + 15 * u, feet_y - 78 * u), (cx + 22 * u, feet_y - 48 * u)],
              fill=(16, 120, 130), width=int(9 * u))
    # head + cap
    draw.ellipse([cx - 10 * u, feet_y - 100 * u, cx + 10 * u, feet_y - 80 * u],
                 fill=(214, 164, 120))
    draw.pieslice([cx - 12 * u, feet_y - 104 * u, cx + 12 * u, feet_y - 84 * u],
                  180, 360, fill=(30, 30, 46))
    draw.rectangle([cx - 12 * u, feet_y - 94 * u, cx + 16 * u, feet_y - 90 * u],
                   fill=(30, 30, 46))


def draw_woman(draw, cx, feet_y, h):
    """Lucia: flat silhouette, pink hair, magenta top, dark jeans."""
    u = h / 100.0
    # legs (jeans)
    draw.polygon([(cx - 12 * u, feet_y), (cx - 3 * u, feet_y),
                  (cx - 6 * u, feet_y - 46 * u), (cx - 14 * u, feet_y - 46 * u)],
                 fill=(28, 28, 52))
    draw.polygon([(cx + 3 * u, feet_y), (cx + 12 * u, feet_y),
                  (cx + 14 * u, feet_y - 46 * u), (cx + 6 * u, feet_y - 46 * u)],
                 fill=(28, 28, 52))
    # torso (magenta top)
    draw.polygon([(cx - 15 * u, feet_y - 44 * u), (cx + 15 * u, feet_y - 44 * u),
                  (cx + 11 * u, feet_y - 80 * u), (cx - 11 * u, feet_y - 80 * u)],
                 fill=MAGENTA)
    # arms
    draw.line([(cx - 13 * u, feet_y - 76 * u), (cx - 20 * u, feet_y - 48 * u)],
              fill=MAGENTA, width=int(8 * u))
    draw.line([(cx + 13 * u, feet_y - 76 * u), (cx + 20 * u, feet_y - 48 * u)],
              fill=MAGENTA, width=int(8 * u))
    # head
    draw.ellipse([cx - 10 * u, feet_y - 100 * u, cx + 10 * u, feet_y - 80 * u],
                 fill=(232, 184, 150))
    # pink hair: bob framing the face, falling to the shoulders
    draw.pieslice([cx - 14 * u, feet_y - 104 * u, cx + 14 * u, feet_y - 76 * u],
                  180, 360, fill=(255, 90, 140))
    draw.rectangle([cx - 14 * u, feet_y - 92 * u, cx - 8 * u, feet_y - 74 * u],
                   fill=(255, 90, 140))
    draw.rectangle([cx + 8 * u, feet_y - 92 * u, cx + 14 * u, feet_y - 74 * u],
                   fill=(255, 90, 140))


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # --- sunset sky: orange -> pink -> magenta -> purple, horizon ~640 ---
    stops = [(0.0, (255, 154, 61)), (0.35, (255, 94, 122)),
             (0.65, (196, 28, 131)), (1.0, (91, 42, 134))]
    for y in range(660):
        t = y / 660.0
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                tt = (t - stops[i][0]) / (stops[i + 1][0] - stops[i][0])
                draw.line([(0, y), (W, y)], fill=lerp(stops[i][1], stops[i + 1][1], tt))
                break

    # --- sun + glow ---
    draw.ellipse([610, 150, 830, 370], fill=(255, 214, 130))
    draw.ellipse([640, 180, 800, 340], fill=YELLOW)

    # --- clouds ---
    for (cx, cy, rx, ry) in [(180, 200, 120, 26), (260, 230, 90, 20),
                             (880, 120, 110, 22), (120, 420, 130, 24)]:
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                     fill=(255, 200, 210))

    # --- skyline (dark purple) + lit windows + VICE CITY sign ---
    buildings = [(0, 470, 90, 640), (90, 520, 170, 640), (170, 440, 260, 640),
                 (260, 500, 330, 640), (760, 480, 850, 640), (850, 430, 940, 640),
                 (940, 510, 1024, 640)]
    for (x0, y0, x1, y1) in buildings:
        draw.rectangle([x0, y0, x1, y1], fill=(42, 23, 64))
        for wy in range(y0 + 18, y1 - 12, 34):
            for wx in range(x0 + 14, x1 - 12, 32):
                if (wx // 32 + wy // 34) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 10, wy + 12], fill=(255, 214, 130))
    # neon sign on the right-hand block, clear of the palm trees
    draw.rectangle([766, 494, 848, 528], fill=(25, 20, 25))
    draw.text((774, 500), "VICE CITY", font=font(20), fill=(255, 120, 200))

    # --- ocean strip ---
    draw.rectangle([0, 640, W, 668], fill=(27, 127, 142))
    for x in range(0, W, 64):
        draw.line([(x, 654), (x + 34, 654)], fill=(255, 255, 255), width=3)

    # --- road ---
    draw.rectangle([0, 668, W, H], fill=(34, 30, 51))
    draw.rectangle([0, 668, W, 678], fill=(90, 80, 120))
    for x in range(20, W, 110):
        draw.rectangle([x, 838, x + 58, 850], fill=(255, 214, 130))

    # --- palms ---
    draw_palm(draw, 96, 700, 1.05)
    draw_palm(draw, 936, 700, 0.95, flip=True)

    # --- pavement strip so the walkers' legs read against the road ---
    draw.rectangle([0, 856, W, 928], fill=(74, 67, 96))

    # --- the three protagonists, walking toward the city ---
    draw_man(draw, 285, 920, 285)
    draw_woman(draw, 505, 920, 280)
    draw_ghost(draw, 735, 640, 215, 265)

    # --- caption: top title + subline, bottom band ---
    text_centred(draw, 36, "GTA VI IS OUT", font(104), WHITE, width=8)
    text_centred(draw, 168, "13 YEARS LATER...", font(46), YELLOW, width=5)
    draw.rectangle([0, 928, W, H], fill=(25, 20, 25))
    draw.rectangle([0, 928, W, 934], fill=MAGENTA)
    text_centred(draw, 948, "MY AGENT GOT PAID ON make.fun", font(44),
                 WHITE, width=5)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
