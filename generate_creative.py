"""Generate creative static assets for the GitHub profile README."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

INK = (7, 17, 26)
DEEP = (11, 21, 32)
CARD = (15, 28, 40)
LINE = (30, 41, 59)
TEAL = (94, 234, 212)
TEAL_DIM = (45, 212, 191)
FOG = (148, 163, 184)
PAPER = (241, 245, 249)
MUTED = (100, 116, 139)


def font(size: int, serif: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = r"C:\Windows\Fonts\georgia.ttf" if serif else r"C:\Windows\Fonts\segoeui.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def vertical_wash(img: Image.Image, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> None:
    d = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        t = y / max(h - 1, 1)
        c = (lerp(top[0], bottom[0], t), lerp(top[1], bottom[1], t), lerp(top[2], bottom[2], t))
        d.line([(0, y), (w, y)], fill=c)


def draw_grid(d: ImageDraw.ImageDraw, w: int, h: int, step: int = 28, alpha: int = 16) -> None:
    c = (*TEAL[:3], alpha)
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=c)
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=c)


def banner() -> None:
    w, h = 1280, 420
    img = Image.new("RGB", (w, h))
    vertical_wash(img, (7, 17, 26), (14, 40, 42))
    d = ImageDraw.Draw(img, "RGBA")
    draw_grid(d, w, h, 32, 12)

    # large watermark glyph
    d.text((880, 40), "§", fill=(*TEAL, 28), font=font(220, serif=True))

    # constellation / attack-path schematic (right)
    nodes = [(980, 90), (1080, 130), (1180, 110), (1040, 210), (1140, 250), (980, 280), (1100, 320)]
    edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (4, 6), (5, 6)]
    for a, b in edges:
        d.line([nodes[a], nodes[b]], fill=(*TEAL, 70), width=2)
    for i, (x, y) in enumerate(nodes):
        r = 6 if i in (0, 6) else 4
        d.ellipse([x - r, y - r, x + r, y + r], fill=(*TEAL, 210 if i in (0, 6) else 140))

    # orbital arc
    d.arc([860, 60, 1240, 380], start=200, end=430, fill=(*TEAL, 50), width=2)

    # left manuscript block
    d.text((64, 78), "FIELD NOTES  ·  SECURITY RESEARCH PRACTICE", fill=FOG, font=font(15, serif=True))
    d.text((64, 130), "Winston Mascarenhas", fill=PAPER, font=font(58, serif=True))
    d.rectangle([64, 208, 320, 211], fill=(*TEAL, 220))
    d.text((64, 236), "Cybersecurity is the through-line.", fill=PAPER, font=font(26, serif=True))
    d.text(
        (64, 278),
        "I study detection, hardening, and secure construction —\nand build tools that make those ideas measurable.",
        fill=FOG,
        font=font(17),
    )
    d.text((64, 360), "Germany  ·  Applied computing  ·  Lab-grounded defense", fill=MUTED, font=font(14))

    # small index tabs
    tabs = ["DETECT", "HARDEN", "ANALYZE", "BUILD"]
    x = 720
    for t in tabs:
        d.rounded_rectangle([x, 360, x + 100, 392], radius=8, fill=CARD, outline=LINE)
        d.text((x + 14, 368), t, fill=TEAL, font=font(12))
        x += 110

    img.save(OUT / "banner.png", "PNG", optimize=True)
    print("banner.png")


def radar() -> None:
    """Interest radar — creative academic diagram."""
    w, h = 560, 360
    img = Image.new("RGB", (w, h), DEEP)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([1, 1, w - 2, h - 2], radius=18, outline=LINE, width=2)
    d.text((28, 22), "Interest map", fill=TEAL, font=font(22, serif=True))
    d.text((28, 52), "Relative emphasis in public work", fill=MUTED, font=font(13))

    cx, cy, R = 280, 210, 110
    axes = [
        ("Detection", 0.95),
        ("Hardening", 0.85),
        ("Adversary\nlens", 0.8),
        ("Secure\nbuild", 0.75),
        ("Docs &\nteaching", 0.7),
        ("Systems\nthinking", 0.88),
    ]
    n = len(axes)

    # rings
    for frac in (0.35, 0.6, 0.85, 1.0):
        rr = int(R * frac)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(*TEAL, 35), width=1)

    pts = []
    for i, (_, strength) in enumerate(axes):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        x = cx + R * math.cos(ang)
        y = cy + R * math.sin(ang)
        d.line([(cx, cy), (x, y)], fill=(*TEAL, 40), width=1)
        px = cx + R * strength * math.cos(ang)
        py = cy + R * strength * math.sin(ang)
        pts.append((px, py))
        label = axes[i][0]
        lx = cx + (R + 34) * math.cos(ang) - 28
        ly = cy + (R + 34) * math.sin(ang) - 10
        d.text((lx, ly), label, fill=FOG, font=font(12))

    d.polygon(pts, fill=(*TEAL, 45), outline=(*TEAL, 200))
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=TEAL)

    img.save(OUT / "radar.png", "PNG", optimize=True)
    print("radar.png")


def lab_timeline() -> None:
    w, h = 1280, 200
    img = Image.new("RGB", (w, h), DEEP)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([1, 1, w - 2, h - 2], radius=18, outline=LINE, width=2)
    d.text((36, 24), "Lab trajectory", fill=TEAL, font=font(22, serif=True))
    d.text((36, 54), "From analysis primitives → defensive tooling → public synthesis", fill=MUTED, font=font(13))

    d.line([(80, 130), (1200, 130)], fill=(*TEAL, 80), width=2)
    stops = [
        (180, "01", "Observe", "Logs & signals"),
        (420, "02", "Probe", "Scan & inspect"),
        (660, "03", "Harden", "Baselines"),
        (900, "04", "Detect", "Alerts & traces"),
        (1120, "05", "Publish", "Portfolio & docs"),
    ]
    for x, num, title, sub in stops:
        d.ellipse([x - 8, 122, x + 8, 138], fill=TEAL)
        d.text((x - 10, 88), num, fill=TEAL_DIM, font=font(12))
        d.text((x - 34, 150), title, fill=PAPER, font=font(16, serif=True))
        d.text((x - 42, 172), sub, fill=MUTED, font=font(12))

    img.save(OUT / "timeline.png", "PNG", optimize=True)
    print("timeline.png")


def quote_band() -> None:
    w, h = 1280, 140
    img = Image.new("RGB", (w, h), INK)
    d = ImageDraw.Draw(img, "RGBA")
    vertical_wash(img, (8, 20, 28), (10, 28, 32))
    d = ImageDraw.Draw(img, "RGBA")
    d.text((64, 36), "“Effective security work demands precise models of trust,", fill=PAPER, font=font(24, serif=True))
    d.text((64, 72), "disciplined experimentation, and clear communication of risk.”", fill=PAPER, font=font(24, serif=True))
    d.text((64, 110), "— working principle", fill=TEAL, font=font(13))
    img.save(OUT / "quote.png", "PNG", optimize=True)
    print("quote.png")


def divider() -> None:
    w, h = 1280, 28
    img = Image.new("RGB", (w, h), DEEP)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(40, 14), (600, 14)], fill=(*TEAL, 40), width=1)
    d.ellipse([630, 10, 650, 18], fill=(*TEAL, 160))
    d.line([(680, 14), (1240, 14)], fill=(*TEAL, 40), width=1)
    img.save(OUT / "divider.png", "PNG", optimize=True)
    print("divider.png")


def focus_strip() -> None:
    w, h = 1280, 180
    img = Image.new("RGB", (w, h), DEEP)
    d = ImageDraw.Draw(img, "RGBA")
    cards = [
        ("01", "Detection", "Signals become findings"),
        ("02", "Hardening", "Baselines & assurance"),
        ("03", "Adversary lens", "Lab-grounded defense"),
        ("04", "Secure build", "Explicit trust edges"),
    ]
    gap, cw = 18, 300
    x = 20
    for num, title, sub in cards:
        d.rounded_rectangle([x, 18, x + cw, 162], radius=16, fill=CARD, outline=LINE, width=2)
        d.rectangle([x + 22, 40, x + 70, 43], fill=TEAL)
        d.text((x + 22, 56), num, fill=TEAL, font=font(13))
        d.text((x + 22, 86), title, fill=PAPER, font=font(24, serif=True))
        d.text((x + 22, 124), sub, fill=FOG, font=font(14))
        x += cw + gap
    img.save(OUT / "focus-strip.png", "PNG", optimize=True)
    print("focus-strip.png")


if __name__ == "__main__":
    banner()
    focus_strip()
    radar()
    lab_timeline()
    quote_band()
    divider()
    # keep existing pin/stats/langs via generate_cards
    print("creative assets ready")
