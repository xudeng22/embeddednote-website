"""OG card for the refresh-modes article: four modes on a speed/quality axis."""

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
draw.text((64, 96), "A mode is a waveform table", font=font(52), fill=INK)
draw.text((64, 164), "Same image, three different results", font=font(25, False), fill=MUTED)

rows = [
    ("GC16", "16 grey levels", "clears, flashes", "photos, colour"),
    ("GL16", "16 grey levels", "no clear", "text pages"),
    ("DU", "1 bit", "fast", "counters, cursors"),
    ("A2", "1 bit", "fastest", "animation"),
]

y = 236
draw.text((64, y), "MODE", font=font(15), fill=ACCENT)
draw.text((230, y), "DEPTH", font=font(15), fill=ACCENT)
draw.text((500, y), "CLEARS?", font=font(15), fill=ACCENT)
draw.text((760, y), "USE IT FOR", font=font(15), fill=ACCENT)
y += 16
draw.line([64, y, W - 64, y], fill=LINE, width=2)
y += 20

for mode, depth, clears, use in rows:
    draw.text((64, y), mode, font=font(27), fill=INK)
    draw.text((230, y + 4), depth, font=font(23, False), fill=INK)
    draw.text((500, y + 4), clears, font=font(23, False), fill=INK)
    draw.text((760, y + 4), use, font=font(23, False), fill=MUTED)
    y += 54

draw.text((64, 512), "Short waveforms leave pigment behind: every fast mode needs a full refresh eventually.",
          font=font(23, False), fill=INK)
draw.text((64, 552), "DU and A2 are both 1-bit; A2 is simply shorter, which is why it smears.",
          font=font(23, False), fill=MUTED)

OUT.mkdir(parents=True, exist_ok=True)
path = OUT / "epaper-refresh-modes.webp"
image.save(path, "WEBP", quality=88, method=6)
print(path.name, path.stat().st_size // 1024, "KB")
