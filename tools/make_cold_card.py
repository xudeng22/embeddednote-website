"""OG card for the cold-failure article: the rating boundary as a strip."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(r"D:\Deepseek\en-site\public\og")
W, H = 1200, 630
BG = (251, 248, 242)
INK = (23, 33, 30)
MUTED = (89, 100, 94)
ACCENT = (166, 57, 39)
LINE = (208, 200, 187)
WARM = (233, 216, 190)

FONTS = [r"C:\Windows\Fonts\seguisb.ttf", r"\Windows\Fonts\arialbd.ttf".replace("\\W", "C:\\W")]
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
draw.text((64, 96), "0 °C is a limit, not a comfort zone", font=font(46), fill=INK)
draw.text((64, 160), "What actually fails when an e-paper panel gets cold", font=font(24, False), fill=MUTED)

# temperature strip: -20 .. 65
x0, x1 = 64, W - 64
y = 240
h = 54
def pos(t):
    return int(x0 + (t + 20) / 85 * (x1 - x0))

draw.rectangle([x0, y, x1, y + h], fill=(240, 236, 228))
# rated zone 0..50
draw.rectangle([pos(0), y, pos(50), y + h], fill=WARM)
# marquee zone
draw.rectangle([pos(-20), y, pos(-20) + 2, y + h], fill=ACCENT)
draw.rectangle([pos(0), y, pos(0) + 2, y + h], fill=ACCENT)
draw.rectangle([pos(50), y, pos(50) + 2, y + h], fill=ACCENT)

for t in (-20, 0, 25, 50, 65):
    draw.line([pos(t), y + h, pos(t), y + h + 8], fill=MUTED, width=1)
    label = f"{t} °C"
    tw = draw.textlength(label, font=font(17, False))
    draw.text((pos(t) - tw / 2, y + h + 14), label, font=font(17, False), fill=MUTED)

draw.text((pos(0) + 12, y + 16), "specified 0–50 °C", font=font(20), fill=INK)
draw.text((pos(-20) + 10, y - 30), "Marquee −20 to 65", font=font(18), fill=ACCENT)

lines = [
    ("Incomplete transition", "image goes grey as the fluid thickens"),
    ("Faster ghosting", "partial updates finish less of each flip"),
    ("Interrupted waveform", "one brownout leaves a permanent patch"),
]
yy = 380
for head, tail in lines:
    draw.text((64, yy), head, font=font(24), fill=INK)
    draw.text((420, yy + 3), tail, font=font(22, False), fill=MUTED)
    yy += 48

draw.text((64, 540), "Same waveform, colder pigment: it simply travels less.",
          font=font(23, False), fill=INK)

OUT.mkdir(parents=True, exist_ok=True)
path = OUT / "epaper-cold-failure.webp"
image.save(path, "WEBP", quality=88, method=6)
print(path.name, path.stat().st_size // 1024, "KB")
