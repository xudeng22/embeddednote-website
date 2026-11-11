"""Re-encode the few very large animated GIFs as animated WebP.

A 7-8 MB GIF inside an article is the single biggest download on the page; the
WebP equivalent is usually 10-20% of the original at the same frame rate.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

MAX_WIDTH = 800
MIN_BYTES = 200_000


def convert(path: Path) -> None:
    target = path.with_suffix(".webp")
    with Image.open(path) as image:
        frames = []
        durations = []
        for index in range(getattr(image, "n_frames", 1)):
            image.seek(index)
            frame = image.convert("RGBA")
            if frame.width > MAX_WIDTH:
                ratio = MAX_WIDTH / frame.width
                frame = frame.resize((MAX_WIDTH, max(1, round(frame.height * ratio))), Image.LANCZOS)
            frames.append(frame)
            durations.append(image.info.get("duration", 100))
        duration = durations[0] if durations else 100
        frames[0].save(
            target,
            "WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=image.info.get("loop", 0),
            quality=72,
            method=6,
        )
    before = path.stat().st_size
    after = target.stat().st_size
    print(f"  {path.name}: {before // 1024} KB -> {after // 1024} KB ({len(frames)} frames)")
    if after >= before * 0.75:
        target.unlink()
        print("    kept original (no meaningful gain)")


def main() -> None:
    for path in sorted(PUBLIC.rglob("*.gif")):
        if path.stat().st_size < MIN_BYTES:
            continue
        try:
            convert(path)
        except Exception as exc:  # noqa: BLE001
            print(f"  !! {path.name}: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
