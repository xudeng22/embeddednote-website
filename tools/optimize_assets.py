"""One-off asset pipeline for embeddednote.com.

1. downloads images that the articles hotlink from third-party hosts
2. re-encodes large PNG/JPEG uploads as WebP
3. adds a 640px variant for wide article images (used by srcset)
4. rebuilds the width/height manifest consumed by the rehype plugin
5. renders a 1200x630 social card per translation key

Run with the bundled Python that ships Pillow:
  %DSH%\\python.exe tools\\optimize_assets.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ARTICLES = ROOT / "src" / "content" / "articles"
OG_DIR = PUBLIC / "og"

PROXY = os.environ.get("HTTPS_PROXY") or "http://127.0.0.1:33210"
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
)

REPORT = {"downloaded": [], "converted": [], "variants": [], "og": [], "rewrites": {}}


def log(msg: str) -> None:
    print(msg, flush=True)


# ---------------------------------------------------------------- 1. download

def download_external_images() -> None:
    """Mirror third-party images into public/uploads/_external/."""
    pattern = re.compile(r"!\[[^\]]*\]\((https?://[^)\s]+)\)")
    targets: dict[str, str] = {}
    for path in sorted(ARTICLES.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for url in pattern.findall(text):
            if "embeddednote.com" in url:
                continue
            targets[url] = path.relative_to(ARTICLES).parts[0]

    dest_dir = PUBLIC / "uploads" / "_external"
    dest_dir.mkdir(parents=True, exist_ok=True)

    for url, _locale in targets.items():
        name = re.sub(r"[^A-Za-z0-9._-]+", "-", url.split("/")[-1])[:80]
        if not name.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
            name += ".webp"
        dest = dest_dir / name
        if dest.exists() and dest.stat().st_size > 1024:
            REPORT["rewrites"][url] = f"/uploads/_external/{name}"
            continue
        payload = None
        for attempt in range(3):
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with opener.open(request, timeout=60) as response:
                    payload = response.read()
                break
            except Exception as exc:  # noqa: BLE001
                log(f"  .. retry {attempt + 1} for {url.split('/')[-1]}: {exc}")
        if payload is None:
            log(f"  !! failed {url}")
            continue
        dest.write_bytes(payload)
        REPORT["rewrites"][url] = f"/uploads/_external/{name}"
        REPORT["downloaded"].append(url)
        log(f"  downloaded {name} ({len(payload) // 1024} KB)")

    # Animated GIFs are re-encoded as animated WebP so they stop dominating the page weight.
    for path in sorted(dest_dir.glob("*.gif")):
        target = path.with_suffix(".webp")
        try:
            with Image.open(path) as image:
                frames = []
                for frame in range(getattr(image, "n_frames", 1)):
                    image.seek(frame)
                    frames.append(image.convert("RGBA"))
                frames[0].save(
                    target,
                    "WEBP",
                    save_all=True,
                    append_images=frames[1:],
                    duration=image.info.get("duration", 100),
                    loop=image.info.get("loop", 0),
                    quality=80,
                    method=6,
                )
            old = f"/uploads/_external/{path.name}"
            new = f"/uploads/_external/{target.name}"
            for url, value in list(REPORT["rewrites"].items()):
                if value == old:
                    REPORT["rewrites"][url] = new
            path.unlink()
            REPORT["converted"].append([path.name, 0, target.stat().st_size])
            log(f"  gif -> webp {target.name} ({target.stat().st_size // 1024} KB)")
        except Exception as exc:  # noqa: BLE001
            log(f"  !! gif failed {path.name}: {exc}")


# ---------------------------------------------------------------- 2. convert

def convert_rasters(min_bytes: int = 45_000) -> None:
    for path in sorted(PUBLIC.rglob("*")):
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            continue
        if path.stat().st_size < min_bytes:
            continue
        target = path.with_suffix(".webp")
        if target.exists() and target.stat().st_size < path.stat().st_size:
            REPORT["rewrites"][f"/{path.relative_to(PUBLIC).as_posix()}"] = (
                f"/{target.relative_to(PUBLIC).as_posix()}"
            )
            continue
        try:
            with Image.open(path) as image:
                if image.mode not in {"RGB", "RGBA"}:
                    image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
                image.save(target, "WEBP", quality=86, method=6)
        except Exception as exc:  # noqa: BLE001
            log(f"  !! convert failed {path.name}: {exc}")
            continue
        if target.stat().st_size < path.stat().st_size * 0.9:
            REPORT["rewrites"][f"/{path.relative_to(PUBLIC).as_posix()}"] = (
                f"/{target.relative_to(PUBLIC).as_posix()}"
            )
            REPORT["converted"].append(
                [
                    path.name,
                    path.stat().st_size,
                    target.stat().st_size,
                ]
            )
            log(
                f"  {path.name}: {path.stat().st_size // 1024} KB -> "
                f"{target.stat().st_size // 1024} KB"
            )
        else:
            target.unlink(missing_ok=True)


# ---------------------------------------------------------------- 3. variants

def make_variants(max_width: int = 640, min_width: int = 1000) -> None:
    for path in sorted(PUBLIC.rglob("*.webp")):
        if path.name.endswith(f"-{max_width}.webp") or path.parent.name == "og":
            continue
        try:
            with Image.open(path) as image:
                width, height = image.size
        except Exception:  # noqa: BLE001
            continue
        if width < min_width or path.stat().st_size < 55_000:
            continue
        target = path.with_name(f"{path.stem}-{max_width}.webp")
        if not target.exists():
            try:
                with Image.open(path) as image:
                    ratio = max_width / image.width
                    resized = image.resize(
                        (max_width, max(1, round(image.height * ratio))),
                        Image.LANCZOS,
                    )
                    resized.save(target, "WEBP", quality=82, method=6)
            except Exception as exc:  # noqa: BLE001
                log(f"  !! variant failed {path.name}: {exc}")
                continue
        REPORT["variants"].append(
            f"/{target.relative_to(PUBLIC).as_posix()}"
        )


# ---------------------------------------------------------------- 4. logo

def make_logo() -> None:
    source = PUBLIC / "images" / "embeddednote-logo.webp"
    if not source.exists():
        return
    with Image.open(source) as image:
        for width in (480, 960):
            ratio = width / image.width
            resized = image.convert("RGBA").resize(
                (width, max(1, round(image.height * ratio))), Image.LANCZOS
            )
            out = PUBLIC / "images" / f"embeddednote-logo-{width}.webp"
            resized.save(out, "WEBP", quality=88, method=6)
            log(f"  logo {width}w: {out.stat().st_size // 1024} KB")


# ---------------------------------------------------------------- 5. manifest

def rebuild_manifest() -> None:
    manifest: dict[str, list[int]] = {}
    for path in sorted(PUBLIC.rglob("*")):
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        try:
            with Image.open(path) as image:
                manifest[f"/{path.relative_to(PUBLIC).as_posix()}"] = list(image.size)
        except Exception:  # noqa: BLE001
            continue
    target = ROOT / "src" / "data" / "performance-image-manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, indent=0, sort_keys=True), encoding="utf-8")
    log(f"  manifest: {len(manifest)} images")


# ---------------------------------------------------------------- 6. og cards

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\seguisb.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont | None:
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:  # noqa: BLE001
                continue
    return None


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def first_image(markdown: str) -> str | None:
    for match in re.finditer(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)>?", markdown):
        url = match.group(1)
        if url.startswith("/"):
            return url
    return None


def render_og() -> None:
    OG_DIR.mkdir(parents=True, exist_ok=True)
    font_title = load_font(46)
    font_kicker = load_font(20)
    if font_title is None:
        log("  !! no font found, skipping og text")
    hero = PUBLIC / "images" / "embeddednote-hero.webp"

    for path in sorted(ARTICLES.glob("en/*.md")):
        text = path.read_text(encoding="utf-8")
        key_match = re.search(r"^translationKey:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text, re.M)
        title_match = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", text, re.M)
        if not key_match or not title_match:
            continue
        key = key_match.group(1).strip()
        title = title_match.group(1).strip().replace("''", "'")

        candidate = first_image(text)
        source = PUBLIC / candidate.lstrip("/") if candidate else None
        if source is None or not source.exists():
            source = hero
        if not source.exists():
            continue

        try:
            with Image.open(source) as image:
                image = image.convert("RGB")
                # cover-crop to 1200x630
                target_ratio = 1200 / 630
                src_ratio = image.width / image.height
                if src_ratio > target_ratio:
                    new_w = round(image.height * target_ratio)
                    left = (image.width - new_w) // 2
                    image = image.crop((left, 0, left + new_w, image.height))
                else:
                    new_h = round(image.width / target_ratio)
                    top = max(0, (image.height - new_h) // 3)
                    image = image.crop((0, top, image.width, top + new_h))
                image = image.resize((1200, 630), Image.LANCZOS)
        except Exception as exc:  # noqa: BLE001
            log(f"  !! og failed {key}: {exc}")
            continue

        canvas = image.convert("RGBA")
        overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for i in range(300):
            alpha = int(232 * (i / 300) ** 0.85)
            draw.rectangle([0, 630 - 300 + i, 1200, 630 - 300 + i + 1], fill=(12, 18, 16, alpha))
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)

        if font_kicker:
            draw.text((56, 372), "EMBEDDEDNOTE", font=font_kicker, fill=(255, 176, 138, 255))
        if font_title:
            lines = wrap(draw, title, font_title, 1080)[:3]
            y = 630 - 62 - len(lines) * 56
            for line in lines:
                draw.text((56, y), line, font=font_title, fill=(255, 255, 255, 255))
                y += 56

        out = OG_DIR / f"{key}.webp"
        canvas.convert("RGB").save(out, "WEBP", quality=82, method=6)
        REPORT["og"].append(key)


def main() -> None:
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in {"all", "download"}:
        log("downloading external images")
        download_external_images()
    if step in {"all", "convert"}:
        log("converting large rasters")
        convert_rasters()
    if step in {"all", "logo"}:
        log("logo variants")
        make_logo()
    if step in {"all", "variants"}:
        log("responsive variants")
        make_variants()
    if step in {"all", "manifest"}:
        log("manifest")
        rebuild_manifest()
    if step in {"all", "og"}:
        log("og cards")
        render_og()

    report_path = ROOT / "tools" / "asset-report.json"
    report_path.write_text(json.dumps(REPORT, indent=1), encoding="utf-8")
    log(
        f"done: {len(REPORT['downloaded'])} downloaded, "
        f"{len(REPORT['converted'])} converted, {len(REPORT['variants'])} variants, "
        f"{len(REPORT['og'])} og cards"
    )


if __name__ == "__main__":
    main()
