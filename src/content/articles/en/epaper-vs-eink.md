---
title: 'E-Paper vs E Ink: What the Two Words Actually Mean'
description: 'E-paper is the category; E Ink is a company. Why the two get used interchangeably, what actually makes a display "e-paper", and how to read the four names on one module.'
seoTitle: 'E-Paper vs E Ink: What the Names Really Mean'
seoDescription: 'E-paper vs E Ink explained: one is a display category, the other a company and a trademark. What makes a display e-paper, the families inside E Ink, and how to read a module label.'
locale: en
translationKey: epaper-vs-eink
pubDate: 2026-11-12
category: display
tags: ['e-paper', 'e-ink', 'reflective display', 'naming', 'selection']
contentType: deep
series: epaper
supplyCta: true
---

Someone asks for an "e-ink screen" and gets quoted a "2.13-inch e-paper module with SSD1680". Both sides think they are talking about the same thing, and mostly they are — but the words are not synonyms, and the difference decides what you can ask for and what you will get.

## The short answer

**E-paper is the category. E Ink is a company.**

E-paper describes a way of making a display: reflective, bistable, built from pigment that moves. E Ink Holdings is one company that makes displays that way, and "E Ink" is its trademark. So every E Ink display is e-paper, while not every e-paper display is E Ink.

The confusion has a mechanical cause: for about two decades E Ink supplied the film inside almost every small e-paper module, so "e-ink" became the generic word for the category, the way "hoover" did for vacuum cleaners. Sellers then wrote "E-ink screen" on listings that carry no E Ink trademark at all.

| Word | What it actually is | Can you use it as a category name? |
| --- | --- | --- |
| E-paper / electronic paper | Display category: reflective, bistable, particle-based | Yes |
| E Ink | Company (E Ink Holdings) and its trademark | No — it is a brand |
| e-ink (lower case, generic) | Colloquial shorthand for the category | In speech, yes; in a specification, no |
| Electronic ink | The material: microcapsules of charged pigment in fluid | It is a material, not a display |
| EPD | "Electronic paper display" — the module, in component catalogues | Yes |

## What makes a display e-paper

Four properties together. Miss one and you are looking at something else wearing the name.

1. **Reflective.** It uses ambient light. There is no backlight, so contrast depends on how much light falls on the surface, and reading in the dark needs an external lamp.
2. **Bistable.** The image stays with the power removed. Energy is spent moving pigment, not holding a picture — which is why a shelf label can run for years on one cell.
3. **Particle-based.** The optical state comes from pigment position, not from a liquid crystal twisting or an LED emitting. This is what makes the viewing angle wide and the image look like print.
4. **Slow.** Moving pigment takes tens to hundreds of milliseconds. That is a property of the mechanism, not a firmware problem, and it is the reason e-paper is used for pages rather than video.

Technologies that satisfy all four but are not E Ink exist: cholesteric LCD, electrochromic, electrowetting and MEMS shutter displays are all sold as e-paper. They are rare in small modules and common in signage and architecture, which is another reason "e-paper" is the safer word when you are specifying.

## Inside the E Ink family

E Ink does not sell one product; it sells several families, and the family name is what appears on the datasheet cover. The ones you will meet in a module:

| Family | What it changes | What we can state |
| --- | --- | --- |
| Carta | Black and white, the baseline reading panel | Mono, the reference for contrast |
| Kaleido | A colour filter array printed over a Carta panel | Colour comes from the filter, so reflectance drops |
| Gallery (ACeP) | Four pigments, no filter; colour from particle position | Full colour, slower refresh, signage-oriented |
| Spectra 6 (**E6**) | Six colours: black, white, yellow, red, blue, green | 0–50 °C, 30:1 contrast on the pages we read |
| Spectra 3100 (**BWRY**) | Four colours: black, white, red, yellow | The "four colour" tag family |
| Marquee | Large-format signage | −20 to 65 °C, 5–7 s transitions |

Two entries in that table are worth remembering because they are the ones people misquote. **E6 is not a product line of its own** — it is the shorthand for Spectra 6, and it appears in shop titles because it is shorter. And **BWRY is a colour set, not a technology**: it says which four pigments are present, not how they are driven.

## Four names on one module

The reason "e-paper vs E Ink" keeps coming up in procurement is that a single module carries four different names, and only one of them is the brand.

| Layer | Example | What it tells you |
| --- | --- | --- |
| Brand / family | E Ink Spectra 6 | Which technology family the film belongs to |
| Panel model | ED2208-NCA | The glass: size, resolution, temperature range |
| Controller IC | SSD1680, UC8151 | Which driver code and command set you need |
| Module part number | P29005S, GDEY075T7 | The vendor's assembly: FPC, connector, optional board |

A quotation that gives you only the first name is not a quotation. Ask for the panel model and the controller; those two decide whether your existing firmware works.

## How to tell what you actually have

Three checks, in this order.

1. **Read the flex.** The panel model is usually printed on the FPC or the back of the glass. A string like `ED2208-NCA` or `GDEY075T7` is the panel; a string like `SSD1680` is the controller.
2. **Look at the demo code.** If the vendor's example folder is named after the controller, the controller is what the demo drives. That is the most reliable evidence you will get without a datasheet.
3. **Count the colours you can address.** Two states means one bit per pixel; four means two bits; six means three bits of information, usually stored as four. That byte width, not the marketing name, decides your frame buffer.

## What this page is not

It does not measure contrast, reflectance or lifetime on any panel, and it does not compare brands on quality. The temperature and refresh figures above come from E Ink's own brand pages; the byte widths come from arithmetic you can repeat. Where a number is a vendor claim rather than a measurement, this page says so.

If you are choosing between an E Ink panel and a non-electrophoretic e-paper panel, the deciding questions are usually reflectance, colour gamut, refresh time and the temperature range you must survive — not the brand on the box.

## Sources

- E Ink, [Spectra 6](https://www.eink.com/brand/detail/Spectra6) — six-colour family, 30:1 contrast, 0–50 °C.
- E Ink, [Marquee](https://www.eink.com/brand/detail/marquee) — large-format signage, −20 to 65 °C, 5–7 s transitions.
- E Ink, [Gallery](https://www.eink.com/brand/detail/Gallery) — Advanced Color ePaper (ACeP), four-pigment full colour.
- E Ink, [Kaleido](https://www.eink.com/brand/detail/Kaleido) — colour filter array over a Carta panel.
- E Ink, [Carta](https://www.eink.com/brand/detail/Carta) — the black-and-white reading panel.
