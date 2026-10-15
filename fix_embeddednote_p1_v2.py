#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EmbeddedNote P1: repair checked article summaries and placeholder Markdown image alt text.

No third-party Python dependencies. Run from repository root (or put the file beside package.json).
Preview: py .\fix_embeddednote_p1_v2.py
Apply:   py .\fix_embeddednote_p1_v2.py --apply
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
ARTICLE_DIR = ROOT / 'src' / 'content' / 'articles'

# A narrowly scoped, human-edited correction list based on the live repository on 2026-10-15.
# v2: resolves /uploads/... URLs to public/uploads/... in the Astro repository.
# No unrelated SEO metadata, text, publication date, or article body is rewritten.
DESCRIPTIONS = {
    'en/a-hardcore-new-open-source-project-on-github-jumper-the-22-dof-crab-robot-fully-open-source-from-training-to-on-device-deployment.md':
        'Jumper is a 22-DoF open-source robot with four walking legs and two claws. We examine its RK3576 controller, MuJoCo training, ONNX export and on-device deployment.',
    'en/an-explosive-embedded-project-on-github-esp32-c3-based-capacitor-explosion-alarm-clock.md':
        'An ESP32-C3 alarm-clock parody uses intentional capacitor failure. We examine the PCB, firmware and serious safety risks without recommending reproduction.',
    'zh/github-22-jumper.md':
        'Jumper 是一款 22 自由度开源机器人。本文分析 RK3576 主控、四足与双钳结构、MuJoCo 仿真训练、ONNX 导出及板端部署。',
    'zh/github-ai-meta-muse-gadget-sdk-ai-esp32.md':
        'Meta Muse Gadget SDK 为 ESP32 和 Linux 设备提供 AI 交互反馈。本文介绍开发板支持、交互状态与嵌入式实现思路。',
}

# Safe contextual descriptions: they indicate editorial context rather than claiming that a
# particular image is a schematic, PCB photo, screenshot, or hardware block diagram.
ALT_CONTEXT = {
    'en/a-hardcore-new-open-source-project-on-github-jumper-the-22-dof-crab-robot-fully-open-source-from-training-to-on-device-deployment.md': [
        'Jumper open-source robot — introductory project image',
        'Jumper robot — figure accompanying the 22-DoF joint layout discussion',
        'Jumper robot — figure accompanying RK3576 hardware specifications',
        'Jumper robot — figure accompanying the controller and deployment discussion',
        'Jumper robot — figure accompanying AI-assisted development',
    ],
    'en/an-explosive-embedded-project-on-github-esp32-c3-based-capacitor-explosion-alarm-clock.md': [
        'ESP32-C3 capacitor alarm clock — introductory project figure',
        'ESP32-C3 capacitor alarm clock — figure accompanying enclosure design',
        'ESP32-C3 capacitor alarm clock — figure accompanying system configuration',
        'ESP32-C3 capacitor alarm clock — figure accompanying power design',
        'ESP32-C3 capacitor alarm clock — figure accompanying the user controls',
        'ESP32-C3 capacitor alarm clock — figure accompanying firmware discussion',
        'ESP32-C3 capacitor alarm clock — figure accompanying enclosure construction',
        'ESP32-C3 capacitor alarm clock — final project reference image',
    ],
    'zh/github-22-jumper.md': [
        'Jumper 22 自由度开源机器人——项目介绍配图一',
        'Jumper 22 自由度开源机器人——项目介绍配图二',
        'Jumper 机器人——关节结构与自由度分析配图',
        'Jumper 机器人——硬件配置分析配图一',
        'Jumper 机器人——硬件配置分析配图二',
        'Jumper 机器人——硬件配置分析配图三',
        'Jumper 机器人——MuJoCo 仿真训练相关配图一',
        'Jumper 机器人——MuJoCo 仿真训练相关配图二',
        'Jumper 机器人——策略部署与AI开发相关配图',
    ],
    'zh/github-ai-meta-muse-gadget-sdk-ai-esp32.md': [
        'Meta Muse Gadget SDK——项目架构和交互概览配图',
        'Meta Muse Gadget SDK——ESP32 开发板支持相关配图一',
        'Meta Muse Gadget SDK——ESP32 开发板支持相关配图二',
    ],
}

IMAGE_RE = re.compile(r'!\[(?P<alt>[^\]\n]*)\]\((?P<path>/uploads/[^)\n]+)\)')
PLACEHOLDER_RE = re.compile(r'^(?:image(?:[- _]?\d+)?(?:\.(?:png|jpg|jpeg|webp))?|img(?:[- _]?\d+)?(?:\.(?:png|jpg|jpeg|webp))?|图片(?:\d+)?|)$', re.I)
FRONT_RE = re.compile(r'\A---\r?\n(?P<front>.*?)\r?\n---\r?\n', re.S)
DESC_RE = re.compile(r'(?m)^description:[^\r\n]*(?:\r?\n[ \t]+[^\r\n]*)*')


def validate_root() -> None:
    must = [ROOT / '.git', ROOT / 'package.json', ROOT / 'astro.config.mjs', ARTICLE_DIR / 'en', ARTICLE_DIR / 'zh']
    bad = [p.name for p in must if not p.exists()]
    if bad:
        raise RuntimeError('No EmbeddedNote Git repository detected. Place the script beside package.json and run it there. Missing: ' + ', '.join(bad))


def fix_description(text: str, relative_path: str) -> tuple[str, bool]:
    if relative_path not in DESCRIPTIONS:
        return text, False
    m = FRONT_RE.match(text)
    if not m:
        raise ValueError(f'{relative_path}: invalid Markdown frontmatter')
    f = m.group('front')
    hit = DESC_RE.search(f)
    if hit is None:
        raise ValueError(f'{relative_path}: description field not found')
    replacement = 'description: ' + json.dumps(DESCRIPTIONS[relative_path], ensure_ascii=False)
    if hit.group(0) == replacement:
        return text, False
    new_f = f[:hit.start()] + replacement + f[hit.end():]
    return text[:m.start('front')] + new_f + text[m.end('front'):], True


def fix_images(text: str, relative_path: str) -> tuple[str, list[dict]]:
    imgs = []
    count = 0
    context_list = ALT_CONTEXT.get(relative_path, [])

    def sub(m: re.Match) -> str:
        nonlocal count
        old = m.group('alt').strip()
        if not PLACEHOLDER_RE.fullmatch(old):
            return m.group(0)
        if relative_path not in ALT_CONTEXT:
            return m.group(0)   # unknown projects need manual review, never guess
        suggestion = context_list[count] if count < len(context_list) else (
            f'{"嵌入式技术项目配图" if relative_path.startswith("zh/") else "Embedded project reference figure"} {count + 1}'
        )
        count += 1
        markdown_path = m.group('path')
        # Preserve the original image URL exactly; change alt text only.
        image_url = urlsplit(markdown_path).path
        abs_image = ROOT / 'public' / unquote(image_url.lstrip('/'))
        imgs.append({'article': relative_path, 'image': markdown_path, 'old_alt': old,
                     'new_alt': suggestion, 'exists': abs_image.is_file(),
                     'local_image': abs_image.as_uri()})
        return f'![{suggestion}]({markdown_path})'

    return IMAGE_RE.sub(sub, text), imgs


def make_report(items: list[dict], desc: list[str], report_path: Path, missing: list[str]) -> None:
    cards = []
    for item in items:
        img = f'<img src="{html.escape(item["local_image"], quote=True)}" alt="Thumbnail for human verification" loading="lazy">' if item['exists'] else '<p class="missing">Image asset missing from local repository</p>'
        cards.append(f'''<section class="card">{img}<div><code>{html.escape(item['article'])}</code>
          <p class="path">{html.escape(item['image'])}</p><p><b>New alt:</b> {html.escape(item['new_alt'])}</p>
          <p><small>Review the actual picture. If it is a circuit diagram, screenshot, photograph, or chart, replace this contextual label with an exact description.</small></p></div></section>''')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EmbeddedNote P1 image review</title><style>
body{max-width:1100px;margin:30px auto;padding:0 20px;background:#f7f5ef;color:#192825;font:15px system-ui;line-height:1.6}h1{margin-bottom:4px}.card{display:grid;grid-template-columns:270px 1fr;gap:22px;border:1px solid #d7d2c8;background:#fff;border-radius:12px;padding:15px;margin:14px 0;overflow-wrap:anywhere}.card img{width:100%;height:auto;max-height:240px;object-fit:contain;background:#eee}.card code{font-size:12px}small,.path{color:#57605f}.missing{color:#c45544}@media(max-width:700px){.card{grid-template-columns:1fr}}
</style></head><body><h1>EmbeddedNote P1: Image Alt Review</h1><p>Changed images: '''+str(len(items))+'''. Edited article summaries: '''+str(len(desc))+'''.</p><p><strong>Important:</strong> generated alt labels are deliberately conservative. They describe editorial context, not unverified picture contents. Visually verify each image before publishing.</p><h2>Edited article summaries</h2><ul>'''+''.join('<li><code>'+html.escape(x)+'</code></li>' for x in desc)+'''</ul><h2>Images to review</h2>'''+''.join(cards)+('<p>Missing assets: '+html.escape(', '.join(missing))+'</p>' if missing else '')+'</body></html>', encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='EmbeddedNote: review or apply targeted P1 article metadata repairs.')
    parser.add_argument('--apply', action='store_true', help='Write changes to Markdown files. By default do a read-only preview.')
    args = parser.parse_args()
    validate_root()

    candidates: list[tuple[Path, str, str]] = []
    image_changes: list[dict] = []
    description_changes: list[str] = []
    untouched = 0
    for f in sorted(ARTICLE_DIR.glob('*/*.md')):
        rel = f.relative_to(ARTICLE_DIR).as_posix()
        before = f.read_text(encoding='utf-8-sig')
        after, changed_d = fix_description(before, rel)
        after, images = fix_images(after, rel)
        if changed_d:
            description_changes.append(rel)
        image_changes.extend(images)
        if after != before:
            candidates.append((f, before, after))
        else:
            untouched += 1

    report = ROOT / '.git' / 'embeddednote-p1-image-review.html'
    missing = sorted(x['image'] for x in image_changes if not x['exists'])
    make_report(image_changes, description_changes, report, missing)
    print(f'{"APPLY" if args.apply else "PREVIEW"} | scanned {len(candidates) + untouched} article files')
    print(f'Articles that would change: {len(candidates)}')
    print(f'Article descriptions needing repair: {len(description_changes)}')
    print(f'Generic image alt labels needing repair: {len(image_changes)}')
    for f, _, _ in candidates:
        print('  - ' + f.relative_to(ROOT).as_posix())
    print('Review report (opens in browser): ' + str(report))
    if missing:
        print('WARNING: images not found under public/uploads in local checkout: ' + str(len(missing)))
    if args.apply:
        if candidates:
            backup_dir = ROOT / '.git' / 'embeddednote-p1-backups' / datetime.now().strftime('%Y%m%d-%H%M%S')
            for f, old, new in candidates:
                backup = backup_dir / f.relative_to(ROOT)
                backup.parent.mkdir(parents=True, exist_ok=True)
                backup.write_text(old, encoding='utf-8')
                f.write_text(new, encoding='utf-8')
            print('DONE. Files updated. Backup stored in: ' + str(backup_dir))
        else:
            print('Already fixed: no Markdown changes needed.')
    else:
        print('No Markdown files changed. After reviewing, run: py .\\fix_embeddednote_p1.py --apply')
    print('NOTE: only alt text is updated; no image files or technical article paragraphs are changed.')
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        sys.exit(1)
