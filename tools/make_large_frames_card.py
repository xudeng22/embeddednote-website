"""OG card for the large-frame article: the six panels on an aspect/ppi map."""

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

draw.text((64, 52), "EMBEDDEDNOTE · E-PAPER", font=font(20), fill=ACCENT)
draw.text((64, 96), "Above 20 inches, pick the shape first", font=font(44), fill=INK)
draw.text((64, 156), "Aspect ratio decides the crop; ppi is flat at 131 for the 2:3 family", font=font(23, False), fill=MUTED)

rows = [
    ("20.2 in", "1530 × 2160", "0.708", "131 ppi", "1.58 MB"),
    ("28.5 in", "2160 × 3060", "0.706", "131 ppi", "3.15 MB"),
    ("31.5 in", "2560 × 1440", "1.778", "93 ppi", "1.76 MB"),
    ("40.5 in", "3060 × 4320", "0.708", "131 ppi", "6.30 MB"),
    ("55 in", "3840 × 2160", "1.778", "81 ppi", "3.96 MB"),
]

x0 = 64
col = [x0, x0 + 150, x0 + 380, x0 + 560, x0 + 720]
y = 226
for label, x in zip(["SIZE", "RESOLUTION", "ASPECT", "DENSITY", "FRAME"], col):
    draw.text((x, y), label, font=font(15), fill=ACCENT)
y += 16
draw.line([x0, y, W - 64, y], fill=LINE, width=2)
y += 18

for size, res, aspect, ppi, frame in rows:
    draw.text((col[0], y), size, font=font(24), fill=INK)
    draw.text((col[1], y + 2), res, font=font(21, False), fill=INK)
    draw.text((col[2], y + 2), aspect, font=font(21, False), fill=INK)
    draw.text((col[3], y + 2), ppi, font=font(21, False), fill=INK)
    draw.text((col[4], y + 2), frame, font=font(21, False), fill=MUTED)
    y += 46

draw.text((64, 540), "An A4 sheet fills only 40% of a 16:9 panel left in portrait.",
          font=font(22, False), fill=INK)
draw.text((64, 574), "6.3 MB per frame is ~48 s over BLE, seconds over Wi-Fi.", font=font(22, False), fill=MUTED)

OUT.mkdir(parents=True, exist_ok=True)
path = OUT / "epaper-large-frames.webp"
image.save(path, "WEBP", quality=88, method=6)
print(path.name, path.stat().st_size // 1024, "KB")
