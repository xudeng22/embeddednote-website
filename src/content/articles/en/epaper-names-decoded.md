---
title: 'E-Paper Names Decoded: E6, 1680 and 8151, and What They Mean'
description: 'The three naming systems behind an e-paper module — E Ink brand names, controller IC numbers, and vendor part numbers — and how to find yours in two minutes.'
locale: en
translationKey: epaper-names-decoded
pubDate: '2026-11-11'
category: display
tags:
- E-Paper
- Display Drivers
- Reference
- Buying Guide
draft: false
author: EmbeddedNote
contentType: deep
series: epaper
seoTitle: 'E-Paper Names Decoded: E6, SSD1680, UC8151'
seoDescription: 'E6 means Spectra 6, 1680 means SSD1680, 8151 means UC8151. How the three naming systems fit together, and where to find your own module number.'
---

Someone asks about an "E6 7.3 inch panel" and gets an answer about "SSD1680" and a datasheet for a 2.13-inch module. Three different naming systems are in play, and none of them is the same as the product title you bought.

This is the decoder. It is short on purpose: you need the right search term in the next two minutes, not a catalogue.

## Three naming systems

| What it names | Example | Where you meet it |
| --- | --- | --- |
| E Ink's brand and technology | Spectra 6, Gallery, Carta | Marketing pages, panel datasheet cover |
| The controller IC on the flex | SSD1680, UC8151 | Demo code, driver libraries, register maps |
| The module vendor's part number | GDEY075T7, 2.13inch e-Paper HAT | Shop listing, silkscreen, invoice |

A module has all three, and they do not imply each other. Two modules sold as "2.13 inch e-paper" can carry different controllers; a panel family can ship with a new controller in a later revision without changing the size in the title.

## The brand names and their shorthand

| Official name | What people write | What it is |
| --- | --- | --- |
| E Ink [Spectra 6](https://www.eink.com/brand/detail/Spectra6) | **E6** | Six-colour panel family for signage. 0–50 °C, up to 200 ppi |
| E Ink [Spectra 3100](https://www.eink.com/brand/detail/Spectra3100) | BWRY, "four colour" | Black, white, red, yellow |
| E Ink [Gallery](https://www.eink.com/brand/detail/Gallery) | **ACeP** | Advanced Colour ePaper, the older full-colour family |
| E Ink [Kaleido](https://www.eink.com/brand) | — | Colour filter over a Carta backplane; the reader-style colour |
| E Ink [Carta](https://www.eink.com/brand) | — | The black-and-white baseline |
| E Ink [Marquee](https://www.eink.com/brand/detail/marquee) | — | Four-particle colour, −20 to 65 °C, 5–7 s transitions |

`E6` is the one that trips people up most often, because it looks like a controller number and it is not. If you are searching for a six-colour panel, search both "Spectra 6" and "E6" — vendors use the short form in titles and the long form in datasheets.

## The E6 family, by size

E6 is not one panel; it is a family that runs from a 1.18-inch badge to a 31.5-inch sign, all six-colour (black, white, yellow, red, blue, green), and all carrying three bits of colour information per pixel inside a four-bit nibble. The sizes below come from a 2025 product catalogue and three datasheets we read on 2026-11-12.

| Size | Resolution | Pixels | RAW4 | Status |
| --- | --- | ---: | ---: | --- |
| 1.18 in | 240 × 206 | 49,440 | 24,720 B | in production |
| 1.54 in | 200 × 200 | 40,000 | 20,000 B | in production |
| 2.61 in | 400 × 400 | 160,000 | 80,000 B | in production |
| 3.68 in | 528 × 792 | 418,176 | 209,088 B | in production |
| 3.98 in | 552 × 768 | 423,936 | 211,968 B | in production |
| 4.0 in | 570 × 800 | 456,000 | 228,000 B | in production |
| 4.38 in | 560 × 800 | 448,000 | 224,000 B | in production |
| 6.19 in | 494 × 1,490 | 736,060 | 368,030 B | in production |
| 9.7 in | 1,120 × 784 | 878,080 | 439,040 B | in production |
| 10.1 in | 1,600 × 1,200 | 1,920,000 | 960,000 B | in production |
| 13.3 in | 1,200 × 1,600 | 1,920,000 | 960,000 B | in production |
| 16.36 in | 3,840 × 1,490 | 5,721,600 | 2,860,800 B | in production |
| 18.56 in | 400 × 3,200 | 1,280,000 | 640,000 B | in production |
| 28.5 in | 2,160 × 3,060 | 6,609,600 | 3,304,800 B | in production |
| 31.5 in | 2,560 × 1,440 | 3,686,400 | 1,843,200 B | in production |

Four things the table does not tell you:

- **The pixel count is not the byte count.** Six colours need three bits, but E6 frames are carried as 4-bit indices, so a frame is `width × height ÷ 2` bytes when packed — the catalogue's own capacity sheet uses that arithmetic. The 31.5-inch panel needs 1.84 MB per frame; the 1.18-inch badge needs 24,720 bytes.
- **Orientation is a datasheet convention, not a rule.** The 13.3-inch panel is listed as 1200 × 1600 because that is how the flex is oriented; you will see the same module sold as 1600 × 1200.
- **Interface changes with size.** The 10.1-inch module is 16-bit parallel; the 31.5-inch is SPI with single/dual/quad data lines and QSPI for pixel data.
- **0–50 °C is the commercial range** on every E6 datasheet we opened. Storage is −25 to +60 °C on the two that state it.

### How many bytes a frame really takes

Colour depth and storage width are two different numbers, and only the second one decides your buffer size.

| Panel type | Colours | Bits of information | Stored as | 200 × 200 | 800 × 480 |
| --- | --- | --- | --- | ---: | ---: |
| Monochrome | 2 | 1 | 1 bit per pixel, eight to a byte | 5,000 B | 48,000 B |
| BWR (3 colours) | 3 | 2 | two 1-bit planes, sent one after the other | 10,000 B | 96,000 B |
| BWRY (E5, 4 colours) | 4 | 2 | 2 bits per pixel, four to a byte | 10,000 B | 96,000 B |
| E6 (6 colours) | 6 | 3 | 4 bits per pixel, two to a byte | 20,000 B | 192,000 B |

BWR and BWRY land on the same byte count for different reasons: the three-colour panel sends two full-size bitplanes, while the four-colour panel packs two bits into every pixel. The totals agree; the layouts do not, and one cannot be fed to a controller that expects the other.

Two consequences follow:

- **Do not compute an E6 frame as `pixels × 3 ÷ 8`.** For a 31.5-inch panel that gives 1.38 MB; the real frame is 1.84 MB, because the controller takes a nibble per pixel and leaves the spare bit unused.
- **The nibble codes are not always 0–5.** At least one public implementation assigns black 0, white 1, yellow 2, red 3, blue 5 and green 6, leaving 4 unused. A converter that emits sequential 0–5 indices needs a mapping table before the bytes reach the controller.

E5 is the four-colour sibling (black, white, red, yellow) at 2 bits per pixel, so a 540 × 800 area needs 108,000 bytes — half of what a six-colour panel of the same size carries.

## What a product catalogue actually tells you

A 2025 product catalogue we work from lists 67 modules. It gives resolution, outline, active area, colour set, operating temperature, storage temperature, interface and connector for every one — and it has **no controller column at all**. That is normal: the controller is a choice made with the panel, not a property of the panel.

Representative rows, including two that show why the model number cannot be decoded from the size:

| Model | Size | Resolution | Colours | Operating temperature |
| --- | --- | --- | --- | --- |
| P15415S | 1.54 in | 200 × 200 | BWRY | 0–40 °C |
| P213167 | 2.13 in | 122 × 250 | BW | 0–50 °C |
| P21335S | 2.13 in | 122 × 250 | BWRY | 0–40 °C |
| P29005S | 2.9 in | 128 × 296 | BW | 0–50 °C |
| P350024 | 3.5 in | 184 × 384 | BW | 0–50 °C |
| P397012 | 3.97 in | 480 × 800 | BWRY | 0–40 °C |
| PL133040 | 13.3 in | 960 × 680 | BW | 0–50 °C |

Two things fall out of the whole list, not just the rows above:

- **Adding colour costs ten degrees.** Every black/white part is rated 0–50 °C; every BWR and BWRY part is 0–40 °C. Across 67 models there are only two black/white exceptions. One N-Color part is narrower still, at 15–35 °C.
- **The size prefix is not the resolution.** `PL133040` is a 13.3-inch panel at 960 × 680, while the 13.3-inch E6 module is 1200 × 1600. Same diagonal, different product.

## Controllers, where we could confirm one

The catalogue does not name controllers, so this column only exists where the vendor shipped a demo whose filename states it. A missing entry means "not stated in the files we have", not "unsupported".

| Vendor demo | Panel | Resolution | Controller | Partial example |
| --- | --- | --- | --- | --- |
| `CODE_Partial_P290051_296x128_SSD1680` | 2.9 in | 128 × 296 | SSD1680 | yes |
| `CODE_Partial_P426010_480x800_SSD1677` | 4.26 in | 480 × 800 | SSD1677 | yes |
| `4.26&3.97CODE_800×480_E5_SSD2677` | 3.97 / 4.26 in | 480 × 800 | SSD2677 | no |
| `1.18CODE_206×240_E6_HX5325` | 1.18 in | 206 × 240 | HX5325 | no |
| `4色价签 296x128 SSD2680` | 2.9 in | 128 × 296 | SSD2680 | no |
| `4色价签 250x128 SSD2682` | 2.13 in | 122 × 250 | SSD2682 | no |
| `4色价签 300x400 SSD2683` | 3.0 in | 300 × 400 | SSD2683 | no |

The pattern worth noticing: the only two partial-refresh demos are the two that say `Partial` in the filename, and they target SSD1680 and SSD1677. If your panel ships a driver from a different family, treat partial refresh as something to prove rather than assume.

## The controller numbers in the code

Demo folders are named after the controller, not the panel, so the number in the filename is your real search key:

| What you see | Full part | Note |
| --- | --- | --- |
| `1680` | SSD1680 | Very common on small black/white modules |
| `8151` | UC8151 (and UC8151D) | Common alternative on similar sizes |
| `1675` | SSD1675 | Older sibling of the 1680 |
| `0373` | IL0373 | Older three-colour designs |
| `3897` | IL3897 | Another legacy part you will find in old demos |

Searching the short number gets you register-level answers; searching "2.13 inch e-paper" gets you shops. If you are debugging an init sequence, you want the first one.

## How to find yours in two minutes

1. **Read the flex cable.** Most modules silkscreen the controller or the vendor part number on the FPC. It is small, and it is the fastest source of truth.
2. **Look at the demo folder name.** If the vendor ships `epd2in13_V3`, the trailing revision matters more than the size: V2 and V3 of the same panel often use different controllers.
3. **Open the datasheet's first page.** The controller is listed in the feature table, not in the title.
4. **Check the product page's specification table**, not its marketing paragraph.

If those four disagree, the FPC wins.

## Why the mismatch matters

Every one of these is a real support thread:

- A driver written for the 1680 register map does not initialise an 8151 panel, even at the same resolution.
- Two "2.13 inch" modules can differ in resolution: 250 × 122 is the current common size, 212 × 104 is the older one. The byte counts differ, so a buffer sized for one overruns on the other.
- A six-colour panel is not "an eight-colour one with two colours missing". The palette and the native codes come from the panel, not from the colour count.

None of this is visible in a product title. That is the whole reason the decoder exists.

## What this page is not

We are not publishing a controller-to-panel table, because that table changes with every hardware revision and a stale entry is worse than no entry. What is stable is the naming logic and the two-minute procedure above.

For the byte-level consequences of getting the buffer format wrong, see [why your e-paper photo looks wrong](/en/articles/why-your-epaper-photo-looks-wrong/) and the [RAW4 packing guide](/en/articles/epaper-palette-raw4-packing-guide/). To convert an image against a specific palette, the [image converter](/en/tools/epaper-image-converter/) accepts an imported device profile.

## Questions that come after the table

### A module is sold only as "2.13 inch e-paper". Which resolution is it?

Display a frame with a one-pixel border and count the pixels along an edge, or read the demo directory: `epd2in13` is the 212 × 104 part, `epd2in13_V3` is usually 250 × 122. If neither is available, the first page of the datasheet always states it. The physical outline is the same for both panels, so size alone cannot tell you.

### Does the controller number tell me whether partial refresh will work?

No. The controller exposes the command, but the panel needs a matching partial waveform. A module can carry an SSD1680 and still support full refresh only. Look for a partial example in the vendor demo that targets this exact revision — if there is none, treat partial as unavailable.

### Two 7.5-inch projects quote different byte counts. Which one is wrong?

Probably neither. 7.5-inch panels exist in 800 × 480 and 640 × 384, and the buffer may be RAW4 or RAW8. That is four legitimate numbers: 192,000 / 384,000 for the larger panel and 122,880 / 245,760 for the smaller. Check which resolution and which format the project used before comparing.

## Sources

- E Ink brand pages for [Spectra 6](https://www.eink.com/brand/detail/Spectra6), [Spectra 3100](https://www.eink.com/brand/detail/Spectra3100), [Gallery](https://www.eink.com/brand/detail/Gallery) and [Marquee](https://www.eink.com/brand/detail/marquee) — brand names, temperature ranges and the Spectra 6 resolution ceiling.
- Waveshare's [2.13-inch e-Paper HAT](https://www.waveshare.com/2.13inch-e-paper-hat.htm) product page — 250 × 122 for the current module, which is why the older 212 × 104 resolution is marked legacy.
- A 2025 product catalogue (not public) supplied the E6 size and resolution columns; the three datasheets above are the public cross-check. Where the two disagree, the table follows the datasheet.
- Controller part numbers are the ones used in the vendors' own demo directory names; always confirm against the datasheet that ships with your panel.
