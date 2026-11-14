"""OG card for the power article: the three energy terms as a bar."""

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

draw.text((64, 54), "EMBEDDEDNOTE · E-PAPER", font=font(20), fill=ACCENT)
draw.text((64, 100), "Where the energy goes", font=font(58), fill=INK)
draw.text((64, 172), "Four refreshes a day, panel left powered", font=font(26, False), fill=MUTED)

bar_x, bar_y, bar_w, bar_h = 64, 250, 1072, 62
# 0.40 J refresh vs 2.85 J standby (total 3.25 J)
refresh_w = int(bar_w * (0.40 / 3.25))
draw.rectangle([bar_x, bar_y, bar_x + refresh_w, bar_y + bar_h], fill=INK)
draw.rectangle([bar_x + refresh_w, bar_y, bar_x + bar_w, bar_y + bar_h], fill=ACCENT)

draw.text((bar_x + 12, bar_y + 18), "refresh 0.40 J", font=font(22), fill=(251, 248, 242))
draw.text((bar_x + refresh_w + 16, bar_y + 18), "standby 2.85 J  (88%)", font=font(22), fill=(251, 248, 242))

draw.line([bar_x, bar_y + bar_h + 28, bar_x + bar_w, bar_y + bar_h + 28], fill=LINE, width=2)
draw.text((bar_x, bar_y + 48), "Cut the panel rail between updates: 3.25 J/day becomes 0.97 J/day.",
          font=font(24, False), fill=INK)
draw.text((bar_x, bar_y + 92), "Same product, same refresh rate, 3.3x the battery life.",
          font=font(24, False), fill=MUTED)

OUT.mkdir(parents=True, exist_ok=True)
path = OUT / "epaper-power-model.webp"
image.save(path, "WEBP", quality=88, method=6)
print(path.name, path.stat().st_size // 1024, "KB")
