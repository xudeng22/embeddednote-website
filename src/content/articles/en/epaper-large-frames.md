---
title: 'Choosing an E-Paper Frame Above 20 Inches'
description: 'Six panels from 20.2 to 55 inches, and the three things that decide between them: aspect ratio, pixels per inch, and frame size in megabytes.'
seoTitle: 'E-Paper Above 20 Inches: Which Frame Size to Pick'
seoDescription: 'A decision guide for large e-paper frames: 20.2 to 55 inch panels compared by aspect ratio, ppi, frame bytes, TCON support and transfer time.'
locale: en
translationKey: epaper-large-frames
pubDate: 2026-11-16
category: display
tags: ['e-paper', 'large format', 'picture frame', 'selection', 'tcon']
contentType: deep
series: epaper
supplyCta: true
---

Above 20 inches the choice stops being about diagonal and becomes about two things: **what shape your content is** and **how many megabytes you are willing to move**. This page compares the six panels we can supply in that range, using numbers from the selection table rather than impressions.

**In one sentence:** pick the aspect ratio first (A-series √2 or 16:9), because that decides whether your artwork survives without cropping; then check ppi, which stays around 131 for the √2 family at every size but drops to 93 at 31.5 inch and 81 at 55.

## The six candidates

Everything below comes from the panel data: resolution, active area and packed frame size at four bits per pixel.

| Size | Resolution | Active area | PPI | Aspect | Frame | Family |
| --- | --- | --- | ---: | ---: | ---: | --- |
| 20.2 in | 1530 × 2160 | 297 × 420 mm | 131 | 0.708 | 1.58 MB | E6 |
| 20.3 in | 2264 × 1600 | 420 × 297 mm | 137 | 1.415 | 1.73 MB | E6 |
| 28.5 in | 2160 × 3060 | 418 × 592 mm | 131 | 0.706 | 3.15 MB | E6 |
| 31.5 in | 2560 × 1440 | 696 × 392 mm | 93 | 1.778 | 1.76 MB | E6 |
| 40.5 in | 3060 × 4320 | 595 × 839 mm | 131 | 0.708 | 6.30 MB | E6 |
| 55 in | 3840 × 2160 | 1206 × 678 mm | 81 | 1.778 | 3.96 MB | Kaleido 3 |

Two rows stand out. **20.2 and 20.3 are the same diagonal and almost the same area, rotated** — but they are not the same panel: 1530 × 2160 against 2264 × 1600, 131 ppi against 137. If your layout is portrait A-series, 20.2 is the one; if it is landscape, 20.3.

And **ppi is nearly constant at 131** across 20.2, 28.5 and 40.5, because those three scale pixel count with area. A 40.5-inch frame is not sharper than a 20.2-inch one; it is the same sharpness over four times the area — and four times the bytes.

## Why aspect ratio comes first

The √2 family (0.706–0.708) matches A-series paper, so a poster, a book page or a PDF exports to it with no crop. The 16:9 family (1.778) matches video and most signage templates.

Take an A4 sheet (aspect 1.414) and put it on 31.5 inch: the panel is 1.778, so fitted to the width the design leaves about **20% of the panel width empty**; left in portrait, it fills only 40%. On 40.5 inch the same artwork fits at 0.708 with nothing lost.

That single decision eliminates half the table before you look at price.

## What changes once you pass 20 inches

Three engineering facts, all of which cost money if discovered late:

1. **You need a TCON.** Small panels are driven directly over SPI; large ones go through a timing controller board. Our own T2000 covers 25.3, 28.5, 31.5 and 43 inch E6 with large-format ghosting removal built in. The 20.2 and 20.3 panels sit below that range, so their timing solution has to be confirmed per project rather than assumed.
2. **Power moves to 12 V.** The 31.5-inch frame we build runs from a 12 V 3 A adapter (battery optional), because the panel rails are generated on board. Do not plan a 5 V-only product at this size without checking the boost stage.
3. **Frame size grows faster than the panel.** 31.5 inch carries 1.76 MB per frame; 40.5 inch carries 6.30 MB — 3.6× the bytes for 1.7× the diagonal.

## What 6.3 MB costs you in transfer

This is the number that surprises people. At the goodput of a healthy BLE link (about 1.1 Mbit/s in our [throughput model](/en/articles/ble-throughput-model/)), 6.30 MB is 52.8 Mbit, so roughly **48 seconds per image**. Over Wi-Fi it is a couple of seconds; over BLE it is close to a minute, every time the frame changes.

| Frame | Bytes | BLE at 1.1 Mbit/s | BLE at 2 Mbit/s |
| --- | ---: | ---: | ---: |
| 20.2 in | 1.58 MB | ~12 s | ~7 s |
| 31.5 in | 1.76 MB | ~13 s | ~7 s |
| 40.5 in | 6.30 MB | ~48 s | ~26 s |

So a 40.5-inch frame is a Wi-Fi product in practice, or a BLE product that updates on a schedule rather than on demand.

## Refresh behaviour at this size

Large panels take longer to settle, and the residue from partial updates is more visible because there is more area to show it. Two consequences:

- **Do not plan partial refresh as the default.** Full refresh clears the film; at 40 inch it also clears the whole wall of your artwork, which is why scheduling matters more than speed.
- **Use a controller with large-format ghosting handling.** Ours implements it in both hardware and firmware on T2000, with normal, ripple and shutter modes; without that, a 40-inch panel accumulates visible residue faster than a badge does.

## Choosing by use case

| What you are building | Panel | Why |
| --- | --- | --- |
| Poster, book page, A-series art | 20.2, 28.5 or 40.5 in | √2 aspect, no crop, 131 ppi throughout |
| Landscape photo wall | 20.3 in | √2 landscape at 137 ppi, the sharpest in this table |
| 16:9 signage, menu board | 31.5 in | 16:9, lower bytes per square metre than 40.5 |
| Very large wall, 4K assets | 55 in Kaleido 3 | 3840 × 2160, but a colour-filter panel, so a different trade-off |
| Frame that must update often | 20.2 or 31.5 in | Smallest frames in this range |

The 55-inch deserves its own note: it is Kaleido 3, not E6. It gives 4K and a wider colour impression, but it builds colour with a filter array over a black-and-white panel, so it reflects less light than a pure E6 panel and refreshes differently. For a bright room, E6 at 40.5 is usually the safer choice; for a dark retail wall where resolution sells, the 55 is the one.

The 31.5-inch frame we build from this panel is documented in [our solution designs](/en/solutions/): TCON board, 12 V 3 A supply, acrylic enclosure and the app provisioning flow. If you are choosing between sizes, the [selection table](/en/e-paper/selection/) has all 40 panels in one view.

## What this page does not tell you

- It does not compare reflectance or colour accuracy between panels, because we have not measured them side by side.
- It does not quote prices; those move with glass and freight.
- It does not promise that a 40.5-inch panel is available from stock — that is a project question.

What it does give you is the arithmetic: aspect, ppi and bytes, all reproducible from the resolution and active area.

## Sources

- Our [E-paper selection table](/en/e-paper/selection/) — resolution, active area and image size for all 40 panels, including the six above 20 inches.
- E Ink, [Spectra 6](https://www.eink.com/brand/detail/Spectra6) — the six-colour family behind the E6 rows.
- E Ink, [Kaleido](https://www.eink.com/brand/detail/Kaleido) — the colour-filter technology in the 55-inch panel.
- T2000 support for 25.3–43 inch E6 and the 12 V 3 A supply come from our own controller and frame documentation.
