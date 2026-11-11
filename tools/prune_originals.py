"""Remove original PNG/JPEG files once the built site no longer references them."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DIST = ROOT / "dist"

mapping = json.loads((ROOT / "tools" / "asset-map.json").read_text(encoding="utf-8"))

dist_blob = "\n".join(
    path.read_text(encoding="utf-8", errors="ignore") for path in DIST.rglob("*.html")
)

removed = 0
freed = 0
kept = []
for old, new in mapping.items():
    if not old.startswith("/"):
        continue
    source = PUBLIC / old.lstrip("/")
    if not source.exists() or source.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif"}:
        continue
    name = source.name
    if name in dist_blob:
        kept.append(old)
        continue
    freed += source.stat().st_size
    source.unlink()
    removed += 1

print(f"removed {removed} originals, freed {freed // (1024 * 1024)} MB")
if kept:
    print("still referenced:", kept)
