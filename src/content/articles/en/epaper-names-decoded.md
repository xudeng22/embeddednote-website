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

## Sources

- E Ink brand pages for [Spectra 6](https://www.eink.com/brand/detail/Spectra6), [Spectra 3100](https://www.eink.com/brand/detail/Spectra3100), [Gallery](https://www.eink.com/brand/detail/Gallery) and [Marquee](https://www.eink.com/brand/detail/marquee) — brand names, temperature ranges and the Spectra 6 resolution ceiling.
- Waveshare's [2.13-inch e-Paper HAT](https://www.waveshare.com/2.13inch-e-paper-hat.htm) product page — 250 × 122 for the current module, which is why the older 212 × 104 resolution is marked legacy.
- Controller part numbers are the ones used in the vendors' own demo directory names; always confirm against the datasheet that ships with your panel.
