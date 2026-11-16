"""OG card for the complaints article: five complaints sorted into four layers."""

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
draw.text((64, 94), "Which complaint is which?", font=font(50), fill=INK)
draw.text((64, 158), "Five reviews of colour e-paper frames, sorted by layer", font=font(23, False), fill=MUTED)

rows = [
    ("Colours look grey", "physics", ACCENT),
    ("Changing takes seconds", "physics + transfer", ACCENT),
    ("A mark stays behind", "waveform policy", INK),
    ("The app will not connect", "product decision", INK),
    ("Costs like a tablet", "panel area", MUTED),
]

y = 232
for label, layer, colour in rows:
    draw.text((64, y), label, font=font(24), fill=INK)
    draw.text((620, y + 2), layer, font=font(22, False), fill=colour)
    draw.line([64, y + 38, W - 64, y + 38], fill=LINE, width=1)
    y += 54

draw.text((64, 516), "Only three of the five are someone's fault.", font=font(24), fill=INK)
draw.text((64, 556), "Six states per pixel; the rest is dithering, not a colour count.",
          font=font(21, False), fill=MUTED)

OUT.mkdir(parents=True, exist_ok=True)
path = OUT / "epaper-frame-complaints.webp"
image.save(path, "WEBP", quality=88, method=6)
print(path.name, path.stat().st_size // 1024, "KB")
