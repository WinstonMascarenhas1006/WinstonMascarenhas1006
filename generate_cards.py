"""Generate static profile cards (replaces broken github-readme-stats)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "assets"

BG = (11, 21, 32)
CARD = (15, 28, 40)
BORDER = (30, 41, 59)
TEAL = (94, 234, 212)
TEXT = (226, 232, 240)
MUTED = (148, 163, 184)


def fonts() -> dict:
    try:
        return {
            "title": ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 22),
            "body": ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14),
            "small": ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 12),
            "label": ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13),
        }
    except OSError:
        f = ImageFont.load_default()
        return {k: f for k in ("title", "body", "small", "label")}


F = fonts()


def make_pin(filename: str, name: str, desc: str, lang: str, lang_color: tuple[int, int, int]) -> None:
    w, h = 400, 120
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([1, 1, w - 2, h - 2], radius=14, fill=CARD, outline=BORDER, width=2)
    d.text((20, 18), name, fill=TEAL, font=F["title"])

    words = desc.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=F["small"]) < 360:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)

    y = 52
    for line in lines[:2]:
        d.text((20, y), line, fill=MUTED, font=F["small"])
        y += 16

    d.ellipse([20, h - 28, 30, h - 18], fill=lang_color)
    d.text((36, h - 32), lang, fill=TEXT, font=F["label"])
    img.save(OUT / filename, "PNG", optimize=True)
    print("wrote", filename)


def make_stats() -> None:
    w, h = 420, 200
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([1, 1, w - 2, h - 2], radius=14, fill=CARD, outline=BORDER, width=2)
    d.text((22, 18), "GitHub activity", fill=TEAL, font=F["title"])
    rows = [
        ("Commits (recent year)", "5.1k+"),
        ("Pull requests", "271"),
        ("Issues", "421"),
        ("Code reviews", "280"),
        ("Public repositories", "5"),
    ]
    y = 58
    for label, val in rows:
        d.text((22, y), label, fill=MUTED, font=F["body"])
        d.text((300, y), val, fill=TEXT, font=F["body"])
        y += 26
    img.save(OUT / "stats.png", "PNG", optimize=True)
    print("wrote stats.png")


def make_langs() -> None:
    w, h = 360, 200
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([1, 1, w - 2, h - 2], radius=14, fill=CARD, outline=BORDER, width=2)
    d.text((22, 18), "Most used languages", fill=TEAL, font=F["title"])
    langs = [
        ("Python", 26.1, (53, 114, 165)),
        ("Go", 23.7, (0, 173, 216)),
        ("TypeScript", 14.4, (49, 120, 198)),
        ("CSS", 8.8, (86, 61, 124)),
        ("Shell", 8.5, (137, 224, 81)),
    ]
    y = 58
    bar_x, bar_w = 22, 316
    for name, pct, color in langs:
        d.text((bar_x, y), name, fill=TEXT, font=F["small"])
        d.text((bar_x + 250, y), f"{pct}%", fill=MUTED, font=F["small"])
        y += 16
        d.rounded_rectangle([bar_x, y, bar_x + bar_w, y + 8], radius=4, fill=(30, 41, 59))
        fill_w = max(8, int(bar_w * pct / 100))
        d.rounded_rectangle([bar_x, y, bar_x + fill_w, y + 8], radius=4, fill=color)
        y += 16
    img.save(OUT / "langs.png", "PNG", optimize=True)
    print("wrote langs.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    make_pin(
        "pin-cyber.png",
        "cybersecurity-projects",
        "15-tool security lab corpus: detection, hardening, analysis.",
        "Python",
        (53, 114, 165),
    )
    make_pin(
        "pin-portfolio.png",
        "Portfolio",
        "Academic-professional site for cybersecurity and engineering work.",
        "TypeScript",
        (49, 120, 198),
    )
    make_stats()
    make_langs()
