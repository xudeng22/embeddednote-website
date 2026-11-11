"""Diagram-style social cards for the text-only e-paper articles.

These articles have no photograph, so the generic PCB hero was showing up as
their og:image. Each card is drawn to say the same thing as the article.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "og"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1200, 630
BG = (251, 248, 242)
INK = (23, 33, 30)
MUTED = (89, 100, 94)
ACCENT = (166, 57, 39)
LINE = (208, 200, 187)
CARD = (255, 255, 255)

FONTS = [
    r"C:\Windows\Fonts\seguisb.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]
REGULAR = [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"]


def font(size: int, bold: bool = True):
    for candidate in FONTS if bold else REGULAR:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def base(title_lines: list[str], kicker: str = "EMBEDDEDNOTE"):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, W, 6], fill=ACCENT)
    draw.text((64, 52), kicker, font=font(20, False), fill=ACCENT)
    y = 96
    for line in title_lines:
        draw.text((64, y), line, font=font(52), fill=INK)
        y += 64
    return image, draw


def panel(draw, box, fill=CARD):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=LINE, width=2)


def card_names() -> None:
    image, draw = base(["E-Paper names", "decoded"])
    items = [("E6", "Spectra 6"), ("1680", "SSD1680"), ("8151", "UC8151")]
    x = 64
    for code, full in items:
        panel(draw, [x, 300, x + 330, 470])
        draw.text((x + 28, 322), code, font=font(64), fill=INK)
        draw.text((x + 30, 408), full, font=font(26, False), fill=MUTED)
        x += 352
    draw.text((64, 512), "brand name  ·  controller IC  ·  vendor part number", font=font(26, False), fill=MUTED)
    image.save(OUT / "epaper-names-decoded.webp", "WEBP", quality=86, method=6)


def card_photo_wrong() -> None:
    image, draw = base(["Why your e-paper", "photo looks wrong"])
    layers = ["source", "palette", "packing", "driver", "panel"]
    y = 286
    for index, label in enumerate(layers):
        highlighted = index == 2
        panel(draw, [64, y, 700, y + 46], fill=(255, 236, 230) if highlighted else CARD)
        draw.text((88, y + 10), label, font=font(24, False), fill=ACCENT if highlighted else INK)
        if highlighted:
            draw.text((520, y + 10), "suspect", font=font(22), fill=ACCENT)
        y += 56
    draw.text((760, 300), "read the", font=font(28, False), fill=MUTED)
    draw.text((760, 340), "symptom", font=font(40), fill=INK)
    draw.text((760, 396), "first", font=font(40), fill=INK)
    image.save(OUT / "epaper-photo-looks-wrong.webp", "WEBP", quality=86, method=6)


def card_ghosting() -> None:
    image, draw = base(["E-Paper ghosting:", "residue, not cache"])
    labels = ["full", "5x", "20x", "full"]
    alphas = [0.0, 0.14, 0.34, 0.0]
    x = 64
    for label, alpha in zip(labels, alphas):
        panel(draw, [x, 300, x + 236, 452])
        draw.rectangle([x + 16, 316, x + 220, 436], fill=(244, 240, 231))
        # ghost of the previous frame: blended into the paper, never solid black
        if alpha:
            base_rgb = (244, 240, 231)
            ghost_rgb = (23, 33, 30)
            blended = tuple(int(b + (g - b) * alpha) for b, g in zip(base_rgb, ghost_rgb))
            draw.rectangle([x + 152, 316, x + 220, 436], fill=blended)
        draw.rectangle([x + 40, 340, x + 120, 350], fill=INK)
        draw.rectangle([x + 40, 362, x + 178, 370], fill=(91, 101, 95))
        draw.text((x + 4, 466), label, font=font(26, False), fill=MUTED)
        x += 258
    draw.text((64, 530), "partial refresh accumulates  ·  full refresh clears", font=font(24, False), fill=MUTED)
    image.save(OUT / "epaper-ghosting-causes-and-fixes.webp", "WEBP", quality=86, method=6)


if __name__ == "__main__":
    card_names()
    card_photo_wrong()
    card_ghosting()
    for name in ("epaper-names-decoded", "epaper-photo-looks-wrong", "epaper-ghosting-causes-and-fixes"):
        path = OUT / f"{name}.webp"
        print(f"{path.name}: {path.stat().st_size // 1024} KB")
