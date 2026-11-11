# 2026-11-11 — Search appearance, asset weight and editorial verification

Three workstreams shipped together: image/asset optimisation (AdSense kept), a
per-article search appearance layer, and a verification pass over six articles.
Nothing was removed from the ad setup; the loader simply moved.

## 1. Images and page weight

| Change | Detail |
| --- | --- |
| Large rasters re-encoded | 53 PNG/JPEG files over 45 KB converted to WebP (q86). Examples: `image-22.png` 1,082 KB → 632 KB, `tiwaz-10.png` 536 KB → 278 KB, `st-price-adjustment-notice-2026.png` 310 KB → 58 KB |
| Animated GIFs | 4 files re-encoded as animated WebP. `flip-card-01.gif` 7,104 KB → 1,351 KB, `tinytron-01.gif` 8,079 KB → 2,421 KB, `x-track-04.gif` 1,059 KB → 415 KB, `x-track-05.gif` 840 KB → 367 KB |
| Responsive variants | The rehype plugin supports `srcset` + `sizes` when a `-640.webp` companion exists. The 118 companions generated in this pass are **not committed yet** — they are the next push, held back because the upload path here drops large packs. Regenerate and commit with `python tools/optimize_assets.py variants` |
| Logo | 187 KB / 1628 × 253 replaced by 480w (14 KB) and 960w (32 KB) variants with `srcset`, sized for the 240 px header slot |
| Hotlinked images | 17 images previously loaded from `image.lceda.cn`, `m5stack-doc.oss-*`, `developer.espressif.com` and `raw.githubusercontent.com` mirrored into `public/uploads/_external/` |
| Originals | 79 superseded originals deleted after confirming the built HTML no longer references them |
| Total | `public/` 56 MB → 37 MB, before counting the new variants and OG cards |

`src/data/performance-image-manifest.json` is regenerated from disk (515 entries)
and now also drives the `srcset` decision.

Reproduce with:

```
python tools/optimize_assets.py all
python tools/convert_gifs.py
python tools/rewrite_refs.py
python tools/prune_originals.py
```

## 2. Search appearance (CTR)

- **Per-article social cards.** 50 × 1200 × 630 WebP cards in `public/og/<translationKey>.webp`,
  cropped from each article's own lead image with a title band. `Base.astro` takes an
  `image` prop; the article template passes `/og/<key>.webp` and declares
  `og:image:width/height/type`.
- **Title formula.** The site suffix is appended only when the combined title stays
  within 62 characters; longer headlines are published unsuffixed. This removes
  truncation on the longest articles (`Raspberry Pi H1 2026` was 105 characters
  before the suffix).
- **Article structured data.** `TechArticle` now carries `image`, `thumbnailUrl`,
  `url`, `articleSection`, `keywords` and `isPartOf`.
- **Breadcrumbs.** Visible breadcrumb plus `BreadcrumbList` JSON-LD on every article.
- **`WebSite` search action** added to the site identity graph.
- **`noindex, follow`** on paginated archives (`/en/page/N/`, `/zh/page/N/`,
  `/en/category/*/page/N/`).
- **Sitemap** now emits `xhtml:link` hreflang alternates and excludes paginated archives.

## 3. Internal linking

New `ArticleFooterNav.astro` renders three blocks after every article:

1. **In this series** — ordered list of articles sharing the `series` frontmatter
   (`ble`, `epaper`, `open-hardware`).
2. **Related reading** — three articles scored by shared tags and category.
3. **Try the tool** — the matching calculator for a series (BLE planner, e-paper converter).

This gives the 44 short project briefs a route into the long-form pages and tools
instead of ending on the byline.

## 4. Editorial verification (six articles)

Each of these now carries a "What we checked" table with the file or document that
was read, plus one derived number where the source supports it:

| Article | Verification highlights | Correction |
| --- | --- | --- |
| `apollo-h3-christmas-ornament` | LED chain, zone ranges, buzzer GPIO, button GPIOs and the 40% brightness ceiling checked against `Integrations/ESPHome/Core.yaml` (version 26.11.5.1) | The 2026 proceeds go to St. Jude Children's Research Hospital, not the two organisations named by earlier ornaments |
| `moto-gps-waveshare` | Hardware table, BLE security model, A1 board status and the test counts checked against `README.md`, `LICENSE.md` and the review packages | Licence is PolyForm Noncommercial 1.0.0: source-available, not open source. Tag corrected |
| `arbwave30-waveform-generator` | THD/SFDR provenance, 13.5% square-wave overshoot, 24 V / 24 W input, board size, and the project's paused status | Added that the author resumes work on 2026-12-25, so the specs are MVP targets |
| `...capacitor-explosion-alarm-clock` | Slot count, 10 Ω limiters, display, enclosure and the linear-regulator note checked against the README | Added the inrush arithmetic: ~1.2 A per slot at 12 V, ~3.6 A if three fire together, above the quoted 3 A budget |
| `...jumper-the-22-dof-crab-robot` | 22 DoF, Apache-2.0 scope, training stack (mjlab, rsl_rl, MuJoCo, MuJoCo Warp) | The RK3576 claim could not be confirmed in the README or the hardware document, and is now marked unverified |
| `m5stack-paperdiy-esp32-s3` | Panel, interface, ESP-IDF demo, price caveat | Four vendor schematic pages mirrored locally so the drawings survive a CDN change |

`contentType` (`news` / `deep`) and `series` were added to the content schema.
Existing articles default to `news`; the pillar pages and the six above are `deep`.

## 5. AdSense

The loader is unchanged (`ca-pub-9169011296822300`, async, crossorigin) and still
runs on every page, but it moved from the first element in `<head>` to the end of
`<body>`. Google supports the loader in either position, auto ads are unaffected,
and the first paint no longer competes with a third-party connection — which
matters for readers where `pagead2.googlesyndication.com` is unreachable.

## Verification

```
npm install --ignore-scripts
npm run build      # 135 pages, clean
```

Checked in the built output: OG image per article, `BreadcrumbList` + `TechArticle`
in the JSON-LD graph, visible breadcrumb, series/related/tool blocks, `srcset` on
article images, no dangling references to deleted originals.

## Follow-ups

- The `zh` mirrors of the six rewritten articles still carry the previous text;
  they need the same verification blocks before hreflang pairs are fully aligned.
- A handful of alt texts still say "GIF" after the animated WebP conversion.
- Remaining long `seoTitle` values (68-91 characters) need editorial shortening;
  the template no longer adds a suffix to them, but they still truncate.
