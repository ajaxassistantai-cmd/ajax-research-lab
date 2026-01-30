#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

BG = (11, 15, 20)          # #0b0f14
CARD = (15, 23, 34)        # #0f1722
TEXT = (232, 238, 246)     # #e8eef6
MUTED = (169, 180, 192)    # #a9b4c0
ACCENT = (106, 228, 255)   # #6ae4ff
ACCENT2 = (156, 255, 106)  # #9cff6a


def get_font(size, bold=False):
    # DejaVu is usually present on Ubuntu/Mint
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        fp = Path(p)
        if fp.exists():
            return ImageFont.truetype(str(fp), size=size)
    return ImageFont.load_default()


def rounded_rect(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def profile_logo(size=1024):
    img = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(img)

    pad = int(size * 0.10)
    box = (pad, pad, size - pad, size - pad)
    rounded_rect(d, box, r=int(size * 0.12), fill=CARD, outline=(255, 255, 255, 20), width=2)

    # Accent ring
    ring_pad = int(size * 0.16)
    ring = (ring_pad, ring_pad, size - ring_pad, size - ring_pad)
    d.ellipse(ring, outline=ACCENT, width=int(size * 0.02))

    # ARL monogram
    f_big = get_font(int(size * 0.22), bold=True)
    text = "ARL"
    tw, th = d.textbbox((0, 0), text, font=f_big)[2:]
    d.text(((size - tw) / 2, (size - th) / 2 - int(size * 0.03)), text, font=f_big, fill=TEXT)

    # Sub text
    f_small = get_font(int(size * 0.05), bold=False)
    sub = "Ajax Research Lab"
    sb = d.textbbox((0, 0), sub, font=f_small)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    d.text(((size - sw) / 2, int(size * 0.66)), sub, font=f_small, fill=MUTED)

    # Tiny motto
    f_tiny = get_font(int(size * 0.036), bold=False)
    motto = "Competitor intel. 48 hours. No meetings."
    mb = d.textbbox((0, 0), motto, font=f_tiny)
    mw, mh = mb[2] - mb[0], mb[3] - mb[1]
    d.text(((size - mw) / 2, int(size * 0.73)), motto, font=f_tiny, fill=(140, 150, 162))

    return img


def cover_image(w=1640, h=624):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)

    # subtle diagonal gradient-ish bands
    for i in range(0, w + h, 12):
        col = (15, 23, 34) if (i // 12) % 2 == 0 else (12, 18, 26)
        d.line([(i, 0), (0, i)], fill=col, width=10)

    # main card
    padx, pady = 80, 70
    box = (padx, pady, w - padx, h - pady)
    rounded_rect(d, box, r=26, fill=(13, 19, 28), outline=(40, 50, 60), width=2)

    # left badge circle
    cx, cy = padx + 160, h // 2
    r = 110
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CARD, outline=ACCENT, width=6)
    f_mono = get_font(64, bold=True)
    mono = "ARL"
    tw, th = d.textbbox((0, 0), mono, font=f_mono)[2:]
    d.text((cx - tw / 2, cy - th / 2 - 6), mono, font=f_mono, fill=TEXT)

    # headline
    f_h1 = get_font(56, bold=True)
    f_h2 = get_font(24, bold=False)
    x0 = padx + 320
    d.text((x0, pady + 120), "Ajax Research Lab", font=f_h1, fill=TEXT)
    d.text((x0, pady + 190), "Competitor research for local businesses", font=f_h2, fill=MUTED)

    # bullets
    f_b = get_font(22, bold=False)
    bullets = [
        "48-hour competitor snapshot (Google Doc + PDF)",
        "Offers • reviews • messaging • local visibility", 
        "No meetings — async via email",
        "https://ajaxassistantai-cmd.github.io/ajax-research-lab/",
    ]
    y = pady + 250
    for b in bullets:
        d.text((x0, y), "• " + b, font=f_b, fill=(170, 182, 195))
        y += 34

    # accent bar
    d.rectangle((x0, pady + 95, x0 + 140, pady + 101), fill=ACCENT2)

    return img


def main():
    logo = profile_logo(1024)
    logo.save(OUT / "arl_profile_1024.png", format="PNG")

    # Smaller versions handy for other platforms
    profile_logo(512).save(OUT / "arl_profile_512.png", format="PNG")

    cover = cover_image(1640, 624)
    cover.save(OUT / "arl_cover_1640x624.png", format="PNG")

    print("Wrote:")
    for p in ["arl_profile_1024.png", "arl_profile_512.png", "arl_cover_1640x624.png"]:
        print(" -", OUT / p)


if __name__ == "__main__":
    main()
