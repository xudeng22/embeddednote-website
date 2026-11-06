---
title: 'From Photo to E-Paper Bytes — Palette, Dithering and RAW4 Packing'
description: 'A practical engineering walk-through of limited-color conversion, continuous 4-bit pixel packing, odd-width rows, palette indexes and device-specific mappings.'
locale: en
translationKey: epaper-palette-raw4-packing-guide
pubDate: '2026-11-06'
category: display
tags: [E-Paper, Image Processing, Dithering, RAW4, Color Palette, Firmware]
author: EmbeddedNote
draft: false
seoTitle: 'E-Paper RAW4 Format — Dithering, Index Packing and Test Vectors'
seoDescription: 'Understand 4-bit e-paper image data, packed nibble order, unpadded rows, calibration limits and a reproducible odd-width RAW4 test vector.'
---

A photograph can look convincing in an RGB browser preview and still appear wrong on a color e-paper panel. The failure is not always “bad dithering.” Three separate mappings are involved: **the source image to a restricted color palette**, **palette indexes to bytes**, and **those indexes to the panel's actual controller codes and drive waveforms**. Confusing any two of them can create swapped colors, mirrored text, or an incorrect frame size.

This guide treats each mapping separately. Its sample data is **synthetic and reproducible**; no device-specific color fidelity or reflective-panel measurement is claimed.

![5×2 RAW4 nibble packing: five bytes with no row padding](/images/p0/epaper-palette-raw4-packing-guide-cover.webp)

## 1. Establish the target before choosing a dithering algorithm

Start by recording the active display width and height, supported physical inks, orientation, input pixel format, row stride and firmware color codes. “Four-color e-paper” is not one interoperable file format. Even panels marketed with a similar number of colors can have different native palettes, controller interfaces and waveform requirements.

A display with 800 × 540 active pixels contains **432,000 pixels**. If each pixel is stored as an 8-bit palette index, the unpadded file requires **432,000 bytes**. If an index needs only four bits, two pixels fit in a byte, so a continuous packed stream requires **216,000 bytes**. Those are storage calculations, not proof of a controller-native framebuffer format. A 416 × 240 panel similarly requires **49,920 bytes** at a tightly packed 4 bpp.

| 800 × 540 working representation | Bytes | Notes |
|---|---:|---|
| 1 bpp | 54,000 | Only two indexes, if that mapping is appropriate |
| 2 bpp | 108,000 | Four index values; not a universal four-color wire format |
| 4 bpp | 216,000 | Up to 16 index values; useful for six or eight entries |
| 8 bpp | 432,000 | One palette index per pixel |
| RGB888 | 1,296,000 | Source/intermediate representation, not indexed |

Some controller protocols instead require separate planes, row padding, line headers or non-linear addressing. Never upload an exported RAW file until its semantics are matched against the driver's expectations.

## 2. The palette is both a numerical and physical problem

Palette quantization assigns every source pixel to one of a finite set of reference colors. A simple nearest-color algorithm in sRGB uses squared Euclidean distance, but sRGB values are gamma encoded and are not perceptually uniform. Converting samples to CIE Lab and comparing ΔE76 is often a more useful baseline when approximating colors; ΔE76 is not equivalent to the more elaborate CIEDE2000 method.

For reflective e-paper, even an accurate Lab calculation is only as good as its *reference palette*. RGB swatches sampled from a manufacturer presentation are not measurements of the actual display. A defensible calibrated palette requires panel readings under a documented illuminant, temperature, drive waveform and instrument setup. A JSON field marked “measured” does not turn guessed RGB values into real measurements.

The [EmbeddedNote E-Paper Image Converter](/en/tools/epaper-image-converter/) deliberately distinguishes illustrative reference palettes from locally imported measured profiles. Its eight-color option is a **demonstration palette**, not a certified calibration for any E Ink E6 panel.

## 3. Dithering changes spatial error, not the number of physical inks

Nearest-color mapping avoids diffusion artifacts but can produce broad flat patches. Floyd–Steinberg propagates quantization error to neighboring pixels and is often useful for photographs. Atkinson spreads less of the error and can preserve a different tonal balance. Ordered Bayer 4×4 uses a fixed periodic threshold; it is deterministic and can be useful for patterns but may produce visible texture. None of these is always best.

Test with the **same** resized input: (a) grayscale gradient, (b) skin-tone or warm-neutral sample, (c) fine black text on white, (d) saturated color blocks, and (e) checkerboard edges. Keep resize mode, contrast, saturation and palette fixed when comparing methods. Judging a dither using different crops or color adjustments makes the comparison meaningless.

A preview PNG can verify the **selected reference RGB values and geometry**. It cannot predict a panel's measured brightness, color saturation, viewing-angle behavior, ghosting or refresh artifacts without hardware evidence.

## 4. RAW4 packing—an odd-width test vector

The converter's RAW4 export is a sequence of **zero-based palette indexes**, not device color codes. Under its documented packing rule, pixels are traversed row-major, two indexes per byte, with the **first** pixel in the high nibble and **no row padding**. This is different from a format that starts each scanline on a new byte.

Take a deliberately odd-width 5 × 2 test image:

```text
Row 0: 0 1 2 3 4
Row 1: 5 0 1 2 3
Continuous sequence: 0 1 2 3 4 5 0 1 2 3
Packed bytes (hex): 01 23 45 01 23
File length: 5 bytes
```

[Open the complete RAW4 byte-layout diagram (SVG)](/images/p0/raw4-odd-width.svg)

The third byte, `0x45`, crosses the row boundary: its high nibble is the last pixel of row 0, and its low nibble is the first pixel of row 1. A row-aligned encoder would instead emit six bytes for this 5 × 2 sample, assuming it pads each odd-length row. Mixing these formats produces a progressively shifted picture.

Verify with code rather than visual intuition:

```python
pixels = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3]
assert all(0 <= x < 16 for x in pixels)
packed = bytes((pixels[i] << 4) | (pixels[i+1] if i+1 < len(pixels) else 0)
               for i in range(0, len(pixels), 2))
assert packed.hex(' ') == '01 23 45 01 23'
assert len(packed) == 5
```

When writing a driver, document whether indexes are remapped before packing or whether the controller needs a lookup table, bit-plane split, vertical scan ordering or byte reversal. Check each with a known pixel pattern. A file with the expected byte count can still be completely wrong on screen.

## 5. A small test suite before sending a real photograph

Use a single black pixel at the first, last and row-boundary positions to verify orientation and stride. Next render a checkerboard to expose nibble order. Then show solid swatches for every valid palette index, explicitly mapping index → intended color → controller-native code. Finally test lines and small text with and without dithering. Save a manifest with width, height, palette, packing rule, source file hash, exported file hash and converter version.

Be particularly careful when display firmware expects **2 bpp** or planar data: packing the same four colors in RAW4 doubles the data size versus a native 2 bpp stream. There is no general lossless “just upload RAW4” rule across vendors.

## 6. What this article does—and does not—establish

The example verifies the arithmetic and byte ordering for a documented software export format. It does not establish color accuracy on a physical EPD, manufacturer-specific bit assignments, safe waveform timing, or end-to-end device operation. For those claims, record source code versions, physical panel identifiers, waveform/driver versions, temperature and unedited photos of actual screen results. See also [why SPI speed is not E-Paper refresh time](/en/articles/epaper-refresh-timing-pipeline/).

**References:** [EmbeddedNote converter: algorithm and export rules](/en/tools/epaper-image-converter/) · [E Ink technology overview](https://www.eink.com/tech/detail/How_it_works). The test vector and byte calculations above are generated specifically for this article.
