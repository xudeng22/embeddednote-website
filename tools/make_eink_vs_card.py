"""OG card for the e-paper vs E Ink article."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(r"D:\Deepseek\en-site\public\og")
W, H = 1200, 630
BG = (251, 248, 242)
INK = (23, 33, 30)
MUTED = (89, 100, 94)
ACCENT = (166, 57, 39)
LINE = (208, 200, 187)

FONTS = [r"C:\Windows\Fonts\seguisb.ttf", r"C:\Windows\Fonts\arialbd.ttf"]
REGULAR = [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"]


def font(size: int, bold: bool = True):
    for candidate in (FONTS if bold else REGULAR):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


image = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(image)
draw.rectangle([0, 0, W, 6], fill=ACCENT)

draw.text((64, 60), "EMBEDDEDNOTE · E-PAPER", font=font(20), fill=ACCENT)

draw.text((64, 120), "E-paper", font=font(78), fill=INK)
draw.text((64, 214), "the category", font=font(30), fill=MUTED)
draw.text((64, 256), "reflective · bistable · pigment", font=font(22, False), fill=MUTED)

draw.line([64, 318, W - 64, 318], fill=LINE, width=2)

draw.text((64, 356), "E Ink", font=font(78), fill=ACCENT)
draw.text((64, 450), "a company, and its trademark", font=font(30), fill=MUTED)
draw.text((64, 492), "Spectra 6 · Kaleido · Gallery · Carta", font=font(22, False), fill=MUTED)

draw.text((64, 556), "Every E Ink panel is e-paper. Not every e-paper panel is E Ink.",
          font=font(24, False), fill=INK)

OUT.mkdir(parents=True, exist_ok=True)
path = OUT / "epaper-vs-eink.webp"
image.save(path, "WEBP", quality=88, method=6)
print(path.name, path.stat().st_size // 1024, "KB")
