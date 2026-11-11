"""Split a large working-tree change into small commits and push them one by one.

The network path here tops out around 60 KB/s and drops long uploads, so a single
18 MB push never completes. Commits go to a side branch first (no Cloudflare
builds), then main fast-forwards to it with one small push.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "seo-2026-11-11"
BUCKET_BYTES = 380_000
MAX_ATTEMPTS = 6


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=check
    )


def working_changes() -> list[tuple[str, str]]:
    raw = git("status", "--porcelain", "-z").stdout
    entries: list[tuple[str, str]] = []
    for chunk in raw.split("\0"):
        if not chunk.strip():
            continue
        status, path = chunk[:2], chunk[3:]
        entries.append((status.strip(), path))
    return entries


def push_with_retry(branch: str) -> bool:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        args = ["push"]
        if branch != "main":
            args.append("-f")
        args += ["origin", branch]
        result = git(*args, check=False)
        if result.returncode == 0:
            print(f"  push ok (attempt {attempt})", flush=True)
            return True
        message = (result.stderr or result.stdout).strip().splitlines()
        tail = message[-1] if message else "unknown error"
        if "up-to-date" in tail:
            print("  remote already has this commit", flush=True)
            return True
        print(f"  push attempt {attempt} failed: {tail[:100]}", flush=True)
        time.sleep(12)
    return False


def main() -> None:
    git("reset", "--soft", "origin/main", check=False)
    git("reset", check=False)
    git("checkout", "-B", BRANCH, "origin/main", check=False)

    changes = working_changes()
    if not changes:
        print("nothing to push")
        return

    free, files = [], []
    for status, path in changes:
        full = ROOT / path
        if status.startswith("D"):
            free.append(path)
        else:
            files.append((full.stat().st_size if full.exists() else 0, path))

    groups: list[tuple[str, list[str]]] = []
    if free:
        groups.append(("Remove superseded image originals", free))

    bucket: list[str] = []
    size_so_far = 0
    index = 0
    for size, path in sorted(files):
        if bucket and size_so_far + size > BUCKET_BYTES:
            groups.append((f"Assets and sources part {index}", bucket))
            index += 1
            bucket, size_so_far = [], 0
        bucket.append(path)
        size_so_far += size
    if bucket:
        groups.append((f"Assets and sources part {index}", bucket))

    print(f"{len(groups)} commit groups on {BRANCH}", flush=True)
    for number, (message, paths) in enumerate(groups, start=1):
        total = sum((ROOT / p).stat().st_size for p in paths if (ROOT / p).exists())
        print(f"[{number}/{len(groups)}] {len(paths)} files, {total // 1024} KB", flush=True)
        git("add", "-A", "--", *paths)
        git(
            "-c", "user.name=xudeng22", "-c", "user.email=xudeng22@163.com",
            "commit", "-q", "-m", message,
        )
        if not push_with_retry(BRANCH):
            print("stopping: push failed repeatedly", flush=True)
            sys.exit(1)

    # One tiny push to production; every object already exists on the remote.
    git("checkout", "main", check=False)
    git("merge", "--ff-only", BRANCH, check=False)
    print("merging into main and pushing", flush=True)
    if not push_with_retry("main"):
        print("branch pushed but main merge push failed", flush=True)
        sys.exit(1)
    print("done", flush=True)


if __name__ == "__main__":
    main()


