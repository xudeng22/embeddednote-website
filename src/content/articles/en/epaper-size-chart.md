---
title: 'E-Paper Resolution and Size Chart: 15 Sizes, Real Numbers'
description: 'Every E6 size from 1.18 to 31.5 inch with resolution, pixel count and packed bytes, plus how ppi works and why the same diagonal carries two different resolutions.'
seoTitle: 'E-Paper Resolution and Size Chart (E6 to 31.5 in)'
seoDescription: 'A reference table of e-paper sizes: 15 E6 panels with resolution, pixels, RAW4 and RAW8 bytes, the ppi formula, and the one-diagonal-two-resolutions trap.'
locale: en
translationKey: epaper-size-chart
pubDate: 2026-11-14
category: display
tags: ['e-paper', 'resolution', 'ppi', 'selection', 'e6']
contentType: deep
series: epaper
supplyCta: true
---

A panel's diagonal tells you almost nothing. A 13.3-inch e-paper module can be 960 × 680 or 1200 × 1600, and the difference decides your frame buffer, your font sizes and whether your artwork survives the conversion. This page is the table we keep open when quoting: every six-colour size we handle, with the arithmetic already done.

**In one sentence:** for a six-colour E6 panel, bytes per frame = width × height ÷ 2, and ppi = the long edge in pixels ÷ the long edge of the active area in inches.

## How to read these numbers

Three quantities get confused, so they are separated here:

- **Resolution** is the pixel matrix, written width × height. It is fixed by the glass and printed on the datasheet.
- **Active area** is the lit region in millimetres. It is smaller than the outline, which includes the bezel and the FPC bond.
- **PPI** is pixels per inch across the active area: `long edge in pixels ÷ (long edge in mm ÷ 25.4)`.

Worked example, 10.1-inch E6: the active area is 203.2 × 152.4 mm, so the long edge is 203.2 ÷ 25.4 = 8.0 inch, and 1600 ÷ 8.0 = **200 ppi**. The same resolution at 13.3 inch gives 1600 ÷ (270.4 ÷ 25.4) = **150 ppi**. Same pixels, different density.

## The six-colour family, all 15 sizes

E6 is E Ink's Spectra 6: six colours (black, white, yellow, red, blue, green), three bits of colour per pixel carried as a 4-bit nibble. PPI is listed only where the panel datasheet states it or gives an active area; a dash means "not published for that part", not "unknown quality".

| Size | Resolution | Pixels | RAW4 | RAW8 | PPI |
| --- | --- | ---: | ---: | ---: | ---: |
| 1.18 in | 240 × 206 | 49,440 | 24,720 B | 49,440 B | — |
| 1.54 in | 200 × 200 | 40,000 | 20,000 B | 40,000 B | — |
| 2.61 in | 400 × 400 | 160,000 | 80,000 B | 160,000 B | 217 |
| 3.68 in | 528 × 792 | 418,176 | 209,088 B | 418,176 B | — |
| 3.98 in | 552 × 768 | 423,936 | 211,968 B | 423,936 B | — |
| 4.0 in | 570 × 800 | 456,000 | 228,000 B | 456,000 B | — |
| 4.38 in | 560 × 800 | 448,000 | 224,000 B | 448,000 B | — |
| 6.19 in | 494 × 1,490 | 736,060 | 368,030 B | 736,060 B | — |
| 7.09 in | 1,200 × 1,600 | 1,920,000 | 960,000 B | 1,920,000 B | 282 |
| 9.7 in | 1,120 × 784 | 878,080 | 439,040 B | 878,080 B | — |
| 10.1 in | 1,600 × 1,200 | 1,920,000 | 960,000 B | 1,920,000 B | 200 |
| 13.3 in | 1,200 × 1,600 | 1,920,000 | 960,000 B | 1,920,000 B | 150 |
| 16.36 in | 3,840 × 1,490 | 5,721,600 | 2,860,800 B | 5,721,600 B | — |
| 18.56 in | 400 × 3,200 | 1,280,000 | 640,000 B | 1,280,000 B | — |
| 28.5 in | 2,160 × 3,060 | 6,609,600 | 3,304,800 B | 6,609,600 B | — |
| 31.5 in | 2,560 × 1,440 | 3,686,400 | 1,843,200 B | 3,686,400 B | 94 |

Two rows punish a careless assumption. The 31.5-inch panel is the largest and the *lowest* density at 94 ppi, because 2560 pixels spread over a 696 mm width. The 7.09-inch is the densest at 282 ppi — a small frame with a 1600-pixel edge. If your text was designed for one, it will not fit the other unchanged.

## Four-colour and monochrome, for contrast

The same diagonal appears in other colour sets, with different byte widths. These are the ones that come up most often in module catalogues:

| Family | Common sizes | Typical resolutions | Bits per pixel | Bytes per frame |
| --- | --- | --- | ---: | --- |
| Monochrome | 0.97, 1.31, 1.54, 2.13, 2.66, 2.9, 3.46, 3.5 in | 88 × 184, 152 × 152, 200 × 200, 122 × 250, 152 × 296, 176 × 480, 184 × 384 | 1 | w × h ÷ 8 |
| BWR / BWRY (E5) | 1.54, 2.13, 3.7, 3.97, 4.0, 17.06 in | 200 × 200, 122 × 250, 240 × 416, 480 × 800, 540 × 800, 164 × 2400 | 2 | w × h ÷ 4 |
| E6 (Spectra 6) | 1.18 to 31.5 in | see the table above | 3 (stored in 4) | w × h ÷ 2 |

A 4.0-inch BWRY panel at 540 × 800 therefore needs 108,000 bytes, while the same area in E6 needs 216,000. Half the colours, half the buffer.

## Why one diagonal carries two resolutions

This is the most common reason a quote comes back wrong:

- **2.13 inch** ships as 122 × 250 and as 250 × 128 (the same matrix, rotated).
- **7.5 inch** exists as 800 × 480 and as 640 × 384.
- **13.3 inch** exists as 960 × 680 (a plain mono part) and as 1200 × 1600 (the E6 module).

Diagonal is an outline measurement. Resolution is a glass measurement. They correlate, they do not determine each other, and no formula turns one into the other.

## The byte maths, once

- 1 bit per pixel (monochrome): `w × h ÷ 8`
- 2 bits per pixel (BWR, BWRY): `w × h ÷ 4`
- 4 bits per pixel (E6 frames): `w × h ÷ 2`
- 8 bits per pixel (RAW8, one index per byte): `w × h`

Round up when the product is not divisible by the divisor, and check whether your driver expects row padding — some do, some refuse it. The [image converter](/en/tools/epaper-image-converter/) shows both numbers as you change the panel size, so you can sanity-check a datasheet before trusting it. For the naming behind these numbers, see [E-paper names decoded](/en/articles/epaper-names-decoded/) and the [glossary](/en/e-paper/glossary/).

## What to check before you order

1. **The panel model on the flex** — `ED2208-NCA`, `GDEY075T7`. That string is the only one that fixes size and resolution together.
2. **The active area in the datasheet**, not the outline. PPI is computed from the former.
3. **The controller**, because the same glass can ship with different drivers, and that decides your code.
4. **The interface**: SPI is the default below 13 inch; larger panels move to parallel or a TCON board.

## What this page is not

It is not a catalogue of everything in production, and it does not rank panels by quality. The resolutions and active areas come from module datasheets we read; where a datasheet does not state ppi, the table leaves it blank rather than estimating from the diagonal. The arithmetic is reproducible: every byte figure is `pixels × bits ÷ 8`, rounded up.

## Sources

- E Ink, [Spectra 6](https://www.eink.com/brand/detail/Spectra6) — the six-colour family this table covers.
- Module datasheets for the 7.09, 10.1, 13.3 and 31.5 inch panels, which state the active area used to compute ppi.
