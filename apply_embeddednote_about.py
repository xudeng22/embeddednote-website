#!/usr/bin/env python3
"""Merge EmbeddedNote welcome posts into About; run in repository root."""
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
required = [ROOT/'astro.config.mjs', ROOT/'src/components/Home.astro', ROOT/'src/pages/[lang]/about.astro', ROOT/'scripts/check-dist.mjs']
missing = [str(p) for p in required if not p.is_file()]
if missing:
    raise SystemExit('Not the expected EmbeddedNote repository; missing: '+', '.join(missing))

# One-file payloads: upload only this Python file, run inside the repo.
PAYLOADS = {
  'src/content/about/en.md': "---\ntitle: About EmbeddedNote\ndescription: Learn about EmbeddedNote's technical coverage, editorial approach, source attribution, and contact information.\nlocale: en\n---\n# About EmbeddedNote\n\nWelcome to **EmbeddedNote**, a bilingual publication for engineers, developers, and curious makers working with embedded systems and electronics.\n\nWe cover the details behind real hardware and open-source projects: the chips they use, the schematics and software that make them work, and the design decisions worth understanding. Our goal is to make useful engineering information easier to find, read, and put into practice.\n\n## What we cover\n\nOur six technical sections are:\n\n- **Open Source Projects** — GitHub projects, firmware, schematics, bills of materials, and implementation details.\n- **MCU & SoC** — Microcontrollers, processors, development platforms, and their software ecosystems.\n- **Hardware Design** — Circuit design, PCBs, power supplies, interfaces, and component selection.\n- **Connectivity** — BLE, Wi-Fi, NFC, CAN, and related embedded communication technologies.\n- **Display Technology** — E-paper, TFT, Mini LED, and display driving systems.\n- **Development Tools** — Debugging hardware, test equipment, simulators, and engineering workflows.\n\nRather than stopping at a project's headline features, we try to explain **how it works, which components matter, what trade-offs were made, and where the limitations lie**.\n\n## Editorial approach\n\nTechnical accuracy comes first. Where possible, our articles draw on original repositories, manufacturer documentation, datasheets, and other primary sources. We distinguish a project's stated specifications from independently verified results and from our own analysis.\n\nOur Chinese and English editions aim to preserve the same technical meaning while using clear, natural language for each readership. Component names, numerical specifications, and implementation details should not change in translation.\n\n## Sources, rights, and corrections\n\nWe credit original projects and source materials wherever practicable and respect applicable licenses. Open-source availability does not, by itself, grant unrestricted rights to every image, document, or brand. Third-party names and trademarks belong to their respective owners, and our coverage does not imply endorsement by project maintainers or manufacturers.\n\nIf you spot a technical error, broken reference, or attribution issue, please let us know so we can review and correct it.\n\n## Contact\n\nWe welcome project suggestions, technical corrections, and relevant editorial or partnership enquiries.\n\n**Email:** [xden2019@gmail.com](mailto:xden2019@gmail.com)\n",
  'src/content/about/zh.md': '---\ntitle: 关于 EmbeddedNote\ndescription: 了解 EmbeddedNote（嵌入式杂谈）的技术内容、编辑原则、资料引用与联系方式。\nlocale: zh\n---\n# 关于 EmbeddedNote\n\n欢迎来到 **EmbeddedNote · 嵌入式杂谈**。\n\nEmbeddedNote 是一份面向工程师、硬件开发者与技术爱好者的中英双语技术媒体，关注嵌入式系统、半导体器件、电子设计和开源项目。我们希望把有价值的项目资料、硬件细节与工程经验整理成便于检索、阅读和参考的内容。\n\n## 我们关注什么\n\n网站目前设有六个技术频道：\n\n- **开源项目**：从 GitHub 仓库、项目结构、源代码与硬件资料中理解设计思路。\n- **MCU 与 SoC**：微控制器、处理器、开发平台以及相关软硬件生态。\n- **硬件设计**：原理图、PCB、电源、接口电路和器件选型。\n- **通信技术**：BLE、Wi-Fi、NFC、CAN 等协议与工程应用。\n- **显示技术**：电子纸、TFT、Mini LED 与显示驱动相关技术。\n- **开发工具**：调试设备、仿真工具、开发环境及测试方法。\n\n除了介绍项目做了什么，我们也尽可能回答它**如何实现、使用了哪些关键器件、有哪些设计取舍，以及还存在哪些限制**。\n\n## 编辑原则\n\n我们重视准确性、可读性和工程价值。文章会尽可能参考原始项目仓库、官方文档、数据手册和公开技术资料；对于尚未独立验证的性能数据或产品声明，会区分原作者提供的信息与我们的分析，不把未经验证的描述写成实测结论。\n\n中英文内容以技术含义准确为先，必要时根据不同读者的表达习惯调整语言，但不改变技术参数、原理和原始资料的含义。\n\n## 资料来源、版权与修订\n\n开源不代表可以忽略许可要求。涉及第三方源代码、图片、原理图、数据或商标时，我们会尽可能注明原始来源与适用的许可条件。第三方项目及商标归各自权利人所有，文章中的分析不代表项目原作者或相关厂商的官方立场。\n\n如果发现技术错误、失效链接或素材归属问题，欢迎联系我们核对并进行必要修订。\n\n## 联系我们\n\n欢迎交流技术选题、文章勘误、项目推荐及合作事宜。\n\n**邮箱：** [xden2019@gmail.com](mailto:xden2019@gmail.com)\n',
  'public/_redirects': '/ /en/ 302\n/en/articles/embeddednote-launch/ /en/about/ 301\n/zh/articles/embeddednote-launch/ /zh/about/ 301\n/articles/embeddednote-launch/ /zh/about/ 301\n',
  'scripts/check-dist.mjs': 'import { existsSync, readFileSync, readdirSync } from \'node:fs\';\nimport { join } from \'node:path\';\n\nconst root = \'dist\';\nconst languages = [\'en\', \'zh\'];\nconst categories = [\'open-source\', \'mcu-soc\', \'hardware\', \'connectivity\', \'display\', \'tools\'];\nlet failures = 0;\nlet checks = 0;\n\nfunction check(condition, label) {\n  checks++;\n  console.log(`${condition ? \'PASS\' : \'FAIL\'} ${label}`);\n  if (!condition) failures++;\n}\nfunction has(path) { return existsSync(join(root, path)); }\nfunction read(path) { return readFileSync(join(root, path), \'utf8\'); }\n\nfor (const file of [\'index.html\', \'rss.xml\', \'robots.txt\', \'sitemap-index.xml\',\n  \'_redirects\', \'pagefind/pagefind.js\', \'pagefind/pagefind-ui.js\', \'pagefind/pagefind-ui.css\']) {\n  check(has(file), `Base file: ${file}`);\n}\n\nfor (const lang of languages) {\n  const home = `${lang}/index.html`;\n  const about = `${lang}/about/index.html`;\n  const oldWelcome = `${lang}/articles/embeddednote-launch/index.html`;\n  for (const path of [home, about, ...categories.map(c => `${lang}/category/${c}/index.html`)]) {\n    check(has(path), `Route: ${path}`);\n  }\n  check(!has(oldWelcome), `Old welcome article removed: ${lang}`);\n  if (has(home)) {\n    const html = read(home);\n    check(new RegExp(`<html[^>]*lang=["\']${lang === \'zh\' ? \'zh-CN\' : \'en\'}["\']`, \'i\').test(html), `${lang} homepage language`);\n    check(html.includes(\'rel="canonical"\'), `${lang} homepage canonical`);\n    check(!html.includes(`/articles/embeddednote-launch/`), `${lang} homepage without welcome article`);\n    for (const c of [\'display\', \'connectivity\']) {\n      check(html.includes(`/${lang}/category/${c}/`), `${lang} homepage category ${c}`);\n    }\n  }\n  if (has(about)) {\n    const html = read(about);\n    const other = lang === \'en\' ? \'zh\' : \'en\';\n    check(html.includes(\'rel="canonical"\') && html.includes(`/${lang}/about/`), `${lang} about canonical`);\n    check(html.includes(\'hreflang=\') && html.includes(`/${other}/about/`), `${lang} about alternate`);\n    check(html.includes(\'data-pagefind-body\'), `${lang} about indexed content`);\n  }\n  const articleDir = join(root, lang, \'articles\');\n  check(existsSync(articleDir) && readdirSync(articleDir, {withFileTypes: true}).some(e => e.isDirectory()),\n    `${lang} technical articles remain`);\n}\n\nif (has(\'rss.xml\')) {\n  check(!read(\'rss.xml\').includes(\'/articles/embeddednote-launch/\'), \'Welcome article removed from RSS\');\n}\nif (has(\'_redirects\')) {\n  const rules = read(\'_redirects\');\n  check(/^\\/\\s+\\/en\\/\\s+302\\s*$/m.test(rules), \'Root default language redirect\');\n  for (const [source, target] of [\n    [\'/en/articles/embeddednote-launch/\', \'/en/about/\'],\n    [\'/zh/articles/embeddednote-launch/\', \'/zh/about/\'],\n    [\'/articles/embeddednote-launch/\', \'/zh/about/\']\n  ]) {\n    check(rules.split(/\\r?\\n/).some(line => line.trim() === `${source} ${target} 301`), `301: ${source}`);\n  }\n}\n\nconsole.log(`\\nTotal checks: ${checks}; Passed: ${checks - failures}; Failed: ${failures}`);\nif (failures) process.exitCode = 1;\n',
}
for target, content in PAYLOADS.items():
    destination = ROOT / target
    if not destination.parent.is_dir():
        raise SystemExit(f'Missing destination parent: {destination.parent}')
    destination.write_text(content, encoding='utf-8')
    print('Updated:', target)

for target in [
    'src/content/articles/en/embeddednote-launch.md',
    'src/content/articles/zh/embeddednote-launch.md',
    'src/src/content/articles/en/embeddednote-launch.md',
    'src/src/content/articles/zh/embeddednote-launch.md',
]:
    path = ROOT / target
    if path.is_file():
        path.unlink()
        print('Deleted:', target)

# Fix a broken optional source checker reference; this does not affect site UI.
checker = ROOT / 'scripts/check-source.py'
if checker.is_file():
    original = checker.read_text(encoding='utf-8')
    corrected = original.replace('src/components/Giscus.astro', 'src/components/GiscusComments.astro')
    if original != corrected:
        checker.write_text(corrected, encoding='utf-8')
        print('Fixed:', 'scripts/check-source.py')

# Repair the existing Jumper Chinese/English translation pair without
# renaming either article URL or changing the English Giscus discussion key.
jumper = ROOT / 'src/content/articles/zh/github-22-jumper.md'
if jumper.is_file():
    content = jumper.read_text(encoding='utf-8')
    old_key = 'translationKey: github-22-jumper'
    if old_key in content:
        jumper.write_text(content.replace(old_key, 'translationKey: Open-Source Project - Jumper', 1), encoding='utf-8')
        print('Fixed:', 'src/content/articles/zh/github-22-jumper.md (translationKey)')

print('Finished. Please inspect git diff and run npm run build before pushing.')
