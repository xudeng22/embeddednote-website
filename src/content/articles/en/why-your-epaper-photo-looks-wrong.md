---
title: 'Why Your E-Paper Photo Looks Wrong: Six Causes, Checked in Order'
description: 'A layer-by-layer diagnostic for e-paper images that do not match the preview: palette mapping, byte packing, dithering, waveform and panel, with one cheap test for each.'
locale: en
translationKey: epaper-photo-looks-wrong
pubDate: '2026-11-11'
category: display
tags:
- E-Paper
- Display Drivers
- Debugging
- Image Processing
- Verification
draft: false
author: EmbeddedNote
contentType: deep
series: epaper
seoTitle: 'E-Paper Photo Looks Wrong? Six Causes, In Order'
seoDescription: 'Six causes for an e-paper image that does not match the preview, ordered by how cheaply you can test them, with a symptom table and a one-minute check for each.'
---

The browser preview looked right. The panel does not. The usual next move is to reopen the dithering code, and that is usually the wrong place to start.

An e-paper image passes through five layers before it becomes pigment: the source pixels, the palette mapping, the byte packing, the driver and waveform, and the panel itself. Each layer fails in a different shape. If you read the shape of the error before touching the code, you can skip most of the search.

<img src="/images/p0/epaper-error-layers.svg" alt="Five layers between a photo and the panel, and the error signature each layer produces" width="960" height="470" loading="lazy" decoding="async">

## Read the symptom first

| What you see | Layer to suspect | First test |
| --- | --- | --- |
| Everything is the wrong hue, but shapes are correct | Palette mapping | One solid block per palette index |
| Diagonal shear, repeated columns, mirrored or inverted image | Packing and layout | The 5 × 2 odd-width vector |
| Text is speckled, gradients band | Dithering and tone | Same image with nearest-color only |
| Colours are right but contrast is flat, or a previous image is faintly visible | Driver and waveform | Full refresh from a known previous frame |
| One band, one corner, or a different result on an identical build | Panel and environment | Same image, second unit, second temperature |

The rows are ordered by how fast you can rule them out, not by how likely they are. If the shapes are right and only the colours are off, stop reading the packing code.

## Cause 1: the image you converted is not the image you think

Browsers rescale silently. A canvas is sized by CSS in one place and by `width`/`height` attributes in another, EXIF orientation may or may not have been applied, and a "crop" in the UI can be a letterbox in the buffer.

**One-minute check.** Export the preview PNG and read its real pixel dimensions. They must equal the panel resolution exactly, not the source photo's. Then open the source at 1:1 and confirm the region you expected is the region that arrived.

**Fix.** Crop to the panel aspect ratio before conversion rather than stretching after it. Stretching costs you a resampling pass and makes every later comparison invalid.

## Cause 2: the palette is a reference, not the panel's codes

Every converter ships a palette: black, white, red, yellow. Those are RGB values chosen to look plausible on a monitor. The controller does not store RGB. It stores an index, and the panel's waveform turns that index into a pigment state. Index 3 on one controller is not index 3 on another, and on some panels index 3 is a colour you would not call red.

**One-minute check.** Convert an image that is one solid block per palette entry — index 0 through 7, each filling a labelled stripe. Compare what appears on the panel with what you expected. If two stripes are swapped, it is the mapping, not the dithering.

**Fix.** Build a measured profile that separates the controller's native code from the sRGB value you measured under a stated light source, then quantise against that profile. The [image converter](/en/tools/epaper-image-converter/) accepts that JSON directly, and the palette table on that page explains which of its presets is a reference and which is a device profile.

## Cause 3: packing and layout disagree with the driver

This is the layer that produces the most dramatic failures, and the easiest to identify. Four conventions have to match:

- **Row stride.** Does the controller expect rows padded to a byte, a word, or nothing at all?
- **Nibble order.** In 4-bit mode, is the first pixel in the high nibble or the low nibble?
- **Traversal.** Left to right, top to bottom — or rotated 90°, or mirrored on the X axis?
- **Polarity.** Is a 1 a black pixel or a white pixel?

**One-minute check.** The five-pixel-wide test vector, again:

```
Row 0:  0 1 2 3 4
Row 1:  5 0 1 2 3
```

Continuous row-major RAW4, high nibble first, no padding, gives `01 23 45 01 23`. Note `0x45`: its high nibble is the last pixel of row 0 and its low nibble is the first pixel of row 1. A driver that pads each row to whole bytes produces six bytes instead of five. That single byte difference is what a diagonal shear looks like on screen.

**Fix.** Pick one convention, write it into the interface document, and make the packer and the driver reference the same table. Do not "fix" it by adjusting the image offset — the error moves but never disappears. The [RAW4 verification guide](/en/articles/epaper-palette-raw4-packing-guide/) has the full walk-through, including the odd-width case.

## Cause 4: the dithering is fighting the content

Floyd–Steinberg on a screenshot destroys small text. Nearest-colour on a sky produces contour bands. Neither algorithm is wrong; they are being used on the wrong content.

**One-minute check.** Convert the same image twice: once with nearest-colour and edge protection on, once with Floyd–Steinberg. If the text is unreadable in the second and crisp in the first, you have found it. If both are bad, the problem is upstream.

**Fix.** Choose by content, not by preference: nearest-colour with edge protection for UI and text, error diffusion for photographs, ordered dithering when you need a pattern that repeats identically across refreshes.

## Cause 5: the refresh mode and the waveform

A panel driven in partial-refresh mode uses a different waveform from a full refresh. If you switch modes without clearing, or if the previous frame is still on the panel when the new one is written, colours can come out weak or shifted even though every byte was correct.

**One-minute check.** Force a full refresh from a known previous image before displaying the new frame. If the result is correct, the buffer was fine and the mode was not.

**Fix.** Always full-refresh after changing palette, waveform or rotation. Partial refresh is a power and latency optimisation, not a way to avoid the initial full update. The trade-offs are covered in [the ghosting article](/en/articles/epaper-ghosting-causes-and-fixes/).

## Cause 6: the panel and the room

Temperature changes how fast the pigment moves. Viewing light changes what "white" looks like. Two panels from different batches can differ more than two firmware versions. And a partly seated FPC can produce a band that looks exactly like a row-stride bug.

**One-minute check.** Display the same frame on a second identical unit, and at a second temperature. If the error moves with the hardware rather than the firmware, the remaining layer is physical.

**Fix.** There is none in software. Record the conditions and adjust the claim, not the code.

## What to write down before you file a bug

Most e-paper bug reports are unusable because they contain a photo and a complaint. Include these and you will get an answer in one round instead of five:

```
panel_model:
controller:
waveform / LUT version:
firmware commit:
palette id or profile hash:
buffer format:          (RAW4 / RAW8, stride, nibble order)
dimensions:
first 16 bytes (hex):
photo conditions:       (light source, distance, temperature)
what you expected:
what appeared:
```

The first sixteen bytes settle most packing arguments before anyone opens a datasheet.

## What this article is and is not

The layer model and the tests are engineering practice, not a measurement campaign. We have not characterised a specific panel for this article, and the byte counts are arithmetic. The order of the six causes is chosen so that each test costs less than the one after it, which is the only claim about likelihood we are making.

If you are still choosing hardware, read [the pipeline guide](/en/articles/epaper-engineering-field-guide/) first: half of these failures are decided at the point where you pick the panel, the controller and the transfer format, long before the first image is converted.
