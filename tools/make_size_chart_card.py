"""OG card for the size-chart article: a miniature size table."""

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

draw.text((64, 56), "EMBEDDEDNOTE · E-PAPER", font=font(20), fill=ACCENT)
draw.text((64, 106), "Resolution and size", font=font(62), fill=INK)
draw.text((64, 180), "15 E6 sizes, 1.18 to 31.5 inch", font=font(28, False), fill=MUTED)

rows = [
    ("7.09 in", "1200 × 1600", "282 ppi", "960,000 B"),
    ("10.1 in", "1600 × 1200", "200 ppi", "960,000 B"),
    ("13.3 in", "1200 × 1600", "150 ppi", "960,000 B"),
    ("31.5 in", "2560 × 1440", "94 ppi", "1,843,200 B"),
]

x0 = 64
col = [x0, x0 + 190, x0 + 470, x0 + 640]
y = 250
draw.text((col[0], y), "SIZE", font=font(15), fill=ACCENT)
draw.text((col[1], y), "RESOLUTION", font=font(15), fill=ACCENT)
draw.text((col[2], y), "DENSITY", font=font(15), fill=ACCENT)
draw.text((col[3], y), "RAW4 FRAME", font=font(15), fill=ACCENT)
y += 16
draw.line([x0, y, W - 64, y], fill=LINE, width=2)
y += 18

for size, res, ppi, raw in rows:
    draw.text((col[0], y), size, font=font(24), fill=INK)
    draw.text((col[1], y), res, font=font(24, False), fill=INK)
    draw.text((col[2], y), ppi, font=font(24, False), fill=INK)
    draw.text((col[3], y), raw, font=font(24, False), fill=INK)
    y += 40

draw.text((64, 560), "Same diagonal, different glass: 13.3 in is also sold as 960 × 680.",
          font=font(22, False), fill=MUTED)

OUT.mkdir(parents=True, exist_ok=True)
path = OUT / "epaper-size-chart.webp"
image.save(path, "WEBP", quality=88, method=6)
print(path.name, path.stat().st_size // 1024, "KB")
