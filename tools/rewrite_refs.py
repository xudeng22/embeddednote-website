"""Point article/source references at the optimized WebP assets.

Builds the mapping from what is actually on disk (a raster that has a smaller
WebP sibling) plus the mirrored copies of previously hotlinked images, then
rewrites the markdown and Astro sources in place.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
SRC = ROOT / "src"
EXTERNAL_DIR = PUBLIC / "uploads" / "_external"

RASTER = {".png", ".jpg", ".jpeg", ".gif"}


def build_map() -> dict[str, str]:
    mapping: dict[str, str] = {}

    # 1. rasters with a smaller webp sibling
    for path in PUBLIC.rglob("*"):
        if path.suffix.lower() not in RASTER:
            continue
        webp = path.with_suffix(".webp")
        if not webp.exists():
            continue
        if webp.stat().st_size >= path.stat().st_size:
            continue
        rel = "/" + path.relative_to(PUBLIC).as_posix()
        mapping[rel] = "/" + webp.relative_to(PUBLIC).as_posix()

    # 2. hotlinked images that now live under /uploads/_external
    pattern = re.compile(r"!\[[^\]]*\]\((https?://[^)\s]+)\)")
    for md in (ROOT / "src" / "content" / "articles").rglob("*.md"):
        for url in pattern.findall(md.read_text(encoding="utf-8")):
            if "embeddednote.com" in url:
                continue
            name = re.sub(r"[^A-Za-z0-9._-]+", "-", url.split("/")[-1])[:80]
            stem = Path(name).stem
            candidates = [EXTERNAL_DIR / f"{stem}.webp", EXTERNAL_DIR / name, EXTERNAL_DIR / f"{stem}.png"]
            for candidate in candidates:
                if candidate.exists():
                    mapping[url] = "/" + candidate.relative_to(PUBLIC).as_posix()
                    break
    return mapping


def main() -> None:
    mapping = build_map()
    changed_files = 0
    replacements = 0

    targets = [
        *SRC.rglob("*.md"),
        *SRC.rglob("*.astro"),
        *SRC.rglob("*.ts"),
        *SRC.rglob("*.js"),
    ]
    for path in targets:
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in mapping.items():
            if old in text:
                replacements += text.count(old)
                text = text.replace(old, new)
        # A mirror may still be referenced without the leading slash in markdown.
        for old, new in mapping.items():
            if old.startswith("/") and old[1:] in text:
                replacements += text.count(old[1:])
                text = text.replace(old[1:], new[1:])
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files += 1

    print(f"map entries: {len(mapping)}")
    print(f"files changed: {changed_files}, replacements: {replacements}")
    (ROOT / "tools" / "asset-map.json").write_text(
        json.dumps(mapping, indent=1, sort_keys=True), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
