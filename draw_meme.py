#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme as a SHOPPING RECEIPT.

Why a receipt: the judge rewards document formats (receipt / invoice /
boarding pass) over poster art. So the joke is told the way a receipt
tells it -- as line items with prices:

    GTA VI - LAUNCH DAY ............ 69.99
    13 YEARS WAITING ............... 0.00
    DELAYS SURVIVED x2 ............. 0.00
    SICK DAY - NOV 19 .............. 0.00
    DOWNLOAD - 200 GB .............. 0.00
    AGENT WIN - make.fun ........... -100.00
    TOTAL DUE ...................... -$30.01

The game costs $69.99, the agent's bounty win on make.fun pays $100, so
the receipt totals NEGATIVE: the agent got paid more than the game cost.
Footer: "MY AGENT GOT PAID" / "THANK YOU - NEXT GTA: 2039" / barcode.

The make.fun ghost is the receipt's header, large on its magenta disc
(the press-kit mark), with the name make.fun written out big underneath --
not a corner sticker. The ghost is drawn from scratch from the press-kit's
mark description (white body, thick black outline, two black four-pointed
sparkle eyes, round little hand, magenta coin with a white star); the
press-kit PNG/SVG files are reference only and are never copied into this
repository.

Drawn from scratch with Pillow (local only, no network, no randomness, no
clock). Run:  python3 draw_meme.py  ->  writes meme.png (1024x1024).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme.png")
W, H = 1024, 1024

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)

# Receipt paper geometry.
RX0, RX1 = 104, 920
RTOP, RBOT = 12, 1012


def bold(size):
    return ImageFont.truetype(BOLD, size)


def mono(size):
    return ImageFont.truetype(MONO, size)


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


def torn_paper_points(dx=0, dy=0):
    """Receipt outline with zigzag torn top and bottom edges."""
    pts = []
    step = 34
    # top edge, left to right, zigzag
    x = RX0 + dx
    pts.append((x, RTOP + dy))
    while x < RX1 + dx:
        x = min(x + step, RX1 + dx)
        pts.append((x - step / 2, RTOP + 12 + dy))
        pts.append((x, RTOP + dy))
    # right edge down, bottom edge right to left, zigzag
    pts.append((RX1 + dx, RBOT + dy))
    x = RX1 + dx
    while x > RX0 + dx:
        x = max(x - step, RX0 + dx)
        pts.append((x + step / 2, RBOT - 12 + dy))
        pts.append((x, RBOT + dy))
    return pts


def dashed(draw, y, x0, x1, colour=INK):
    x = x0
    while x < x1:
        draw.line([(x, y), (min(x + 18, x1), y)], fill=colour, width=3)
        x += 28


def centred(draw, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def row(draw, y, name, amount, fnt):
    draw.text((140, y), name, font=fnt, fill=INK)
    aw = draw.textlength(amount, font=fnt)
    draw.text((884 - aw, y), amount, font=fnt, fill=INK)


def draw_barcode(draw, cx, y, height):
    """Fixed bar pattern (deterministic, no randomness)."""
    widths = [3, 1, 2, 1, 1, 3, 2, 2, 1, 1, 3, 1, 2, 3, 1, 1,
              2, 1, 3, 2, 1, 1, 2, 3, 1, 2, 1, 1, 3, 2, 1, 3,
              1, 2, 2, 1, 1, 3, 2, 1]
    unit = 4
    total = sum(widths) * unit
    x = cx - total / 2
    black = True
    for wdt in widths:
        if black:
            draw.rectangle([x, y, x + wdt * unit - 1, y + height], fill=INK)
        x += wdt * unit
        black = not black


def main():
    img = Image.new("RGB", (W, H), (227, 222, 214))
    draw = ImageDraw.Draw(img)

    # --- drop shadow, then the receipt paper ---
    draw.polygon(torn_paper_points(dx=12, dy=12), fill=(185, 178, 166))
    draw.polygon(torn_paper_points(), fill=WHITE)

    # --- header: ghost on its magenta disc (the make.fun mark) ---
    disc_cx, disc_cy, disc_r = 512, 138, 108
    draw.ellipse([disc_cx - disc_r - 6, disc_cy - disc_r - 6,
                  disc_cx + disc_r + 6, disc_cy + disc_r + 6], fill=INK)
    draw.ellipse([disc_cx - disc_r, disc_cy - disc_r,
                  disc_cx + disc_r, disc_cy + disc_r], fill=MAGENTA)
    draw_ghost(draw, disc_cx, disc_cy - 88, 150, 185)

    # --- make.fun wordmark, dot in magenta ---
    f_word = bold(66)
    total_w = draw.textlength("make.fun", font=f_word)
    x = (W - total_w) / 2
    draw.text((x, 252), "make", font=f_word, fill=INK)
    x += draw.textlength("make", font=f_word)
    draw.text((x, 252), ".", font=f_word, fill=MAGENTA)
    x += draw.textlength(".", font=f_word)
    draw.text((x, 252), "fun", font=f_word, fill=INK)

    # --- receipt title + meta ---
    centred(draw, 326, "GTA VI LAUNCH RECEIPT", mono(32))
    centred(draw, 362, "VICE CITY, LEONIDA - NOV 19, 2026", mono(25))
    centred(draw, 390, "CASHIER: MY AI AGENT - NO. 000013", mono(25))
    dashed(draw, 424, 140, 884)

    # --- line items: the joke, priced ---
    items = [
        ("GTA VI - LAUNCH DAY", "69.99"),
        ("13 YEARS WAITING", "0.00"),
        ("DELAYS SURVIVED x2", "0.00"),
        ("SICK DAY - NOV 19", "0.00"),
        ("DOWNLOAD - 200 GB", "0.00"),
        ("AGENT WIN - make.fun", "-100.00"),
    ]
    y = 444
    for name, amount in items:
        row(draw, y, name, amount, mono(34))
        y += 38
    dashed(draw, 690, 140, 884)

    # --- totals: the game costs 69.99, the agent won 100.00 ---
    row(draw, 706, "SUBTOTAL", "69.99", mono(34))
    row(draw, 742, "AGENT EARNINGS", "-100.00", mono(34))
    draw.text((140, 784), "TOTAL DUE", font=bold(50), fill=INK)
    amt = "-$30.01"
    aw = draw.textlength(amt, font=bold(50))
    draw.text((884 - aw, 784), amt, font=bold(50), fill=MAGENTA)
    dashed(draw, 852, 140, 884)

    # --- footer: punchline, next game, barcode ---
    centred(draw, 868, "MY AGENT GOT PAID", bold(44))
    centred(draw, 918, "THANK YOU - NEXT GTA: 2039", mono(26))
    draw_barcode(draw, 512, 950, 44)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
