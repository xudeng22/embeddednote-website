---
title: 'Partial Refresh on E-Paper: When It Is Safe'
description: 'Partial refresh is a panel capability, not a driver flag. Three gates decide whether it is safe on your hardware, plus what content you should never send through it.'
locale: en
translationKey: epaper-partial-refresh-safe
pubDate: '2026-11-11'
category: display
tags:
- E-Paper
- Partial Refresh
- Display Drivers
- Power Management
- Verification
draft: false
author: EmbeddedNote
contentType: deep
series: epaper
seoTitle: 'E-Paper Partial Refresh: When It Is Safe'
seoDescription: 'Partial refresh is a panel capability, not a driver flag. Three gates decide whether an e-paper display can use it, and which content should never go through it.'
supplyCta: true
---

Partial refresh is sold as a speed feature — a fraction of the update time, no full-screen flash, less power. All true, and all conditional. On the wrong hardware, or after the wrong sequence of updates, it produces weak contrast, visible seams and residue that a full refresh cannot always clear.

The question is not "does my driver support partial refresh". It is "does this panel, in this mode, at this temperature, with this content".

<img src="/images/p0/epaper-partial-refresh-waveform.svg" alt="Full refresh drives many transitions; partial refresh uses a short, single-polarity sequence" width="960" height="300" loading="lazy" decoding="async">

**In one sentence:** partial refresh is safe only when the panel ships a partial waveform, the temperature is inside the rated range, and the changed area is small and infrequent. Anything else belongs on a full refresh.

## What partial refresh actually skips

A full refresh drives every pixel through several transitions so it ends in a defined state, regardless of where it started. A partial refresh skips most of that work: it addresses a region, applies a short waveform with fewer transitions, and leaves everything else untouched.

That is why it is fast and why it does not flash. It is also why the result depends on the state the pixel was already in — the subject of [the ghosting article](/en/articles/epaper-ghosting-causes-and-fixes/). Here the question is narrower: given that dependency, which updates are safe to do this way?

## Gate 1: the panel and the waveform support it

This is not a software setting you can enable. A panel either ships with a partial waveform or it does not, and the controller has to expose the addressing mode. Some modules state plainly in the datasheet that only full refresh is supported; large panels are the usual case.

Check three things before writing any code:

1. The product page or datasheet mentions partial refresh, with a temperature range.
2. The controller datasheet documents a partial/region update command and what it does to the LUT.
3. The vendor demo has a working partial example for **this** panel revision, not a sibling size.

If any of those is missing, treat partial as unsupported. A driver that sends a partial command to a panel without the waveform usually does not fail loudly — it produces a grey, low-contrast update that looks like a contrast bug.

## Gate 2: the mode has not changed since the last full refresh

Partial waveforms assume the pixel is already in the state the previous full refresh left it in. Change any of these and that assumption breaks:

- palette or colour mode
- rotation or mirroring
- display window / partial window geometry
- the waveform table (for example after a temperature band change)

After any of those, do a full refresh first. One line of policy, and it prevents most "the colours are wrong in partial mode" reports.

## Gate 3: the temperature is inside the partial range

Partial waveforms have less margin than full ones: fewer transitions, shorter settling. At low temperature the pigment moves more slowly, and the update completes without reaching the target state. The panel then shows a pale, ghosted image that looks exactly like a software error.

Every panel vendor specifies an operating range; some specify a narrower range for partial. Below it, force full refresh. Do not compensate with a longer delay — the waveform, not the timeout, is what settles the pixel.

## What content is safe

| Update | Partial? | Why |
| --- | --- | --- |
| A clock digit, a status icon | Yes | Small area, low contrast change, frequent |
| A text paragraph reflowing | Yes, with a budget | Text edges need the edge protection, not dithering |
| A photo | No | Large tonal change; residue is most visible in gradients |
| A full-screen inverted view (dark mode toggle) | No | Every pixel changes; use full refresh |
| Large solid blocks changing colour | No | The most demanding case for a short waveform |
| First frame after power-on | No | Nothing is defined yet |

The pattern: partial refresh suits **small, incremental, low-contrast** changes. It punishes anything that repaints a large area or inverts the screen.

## Seams and uneven updates

Region-based partial refresh can leave a visible boundary where the updated rectangle meets the untouched area. Two causes:

- **Different history.** The updated region went through a shorter waveform than its surroundings.
- **Different timing.** The region was driven at a different temperature than the rest of the frame was at its last full refresh.

If the seam is visible at normal viewing distance, the panel is telling you the partial budget is exhausted. A full refresh clears it; ignoring it accumulates.

## The policy that keeps it safe

Three gates, evaluated before every update:

```
if (!panel_supports_partial)          -> full
if (mode_changed_since_last_full)     -> full
if (temperature < partial_min)        -> full
if (partial_count >= PARTIAL_BUDGET)  -> full
else                                  -> partial, partial_count++
```

The budget is a product decision, not a datasheet number. Start at 10–20 and verify against your own content: a status display that changes a few glyphs per minute will tolerate a much larger budget than one that swaps photographs.

There is also an **area** gate worth adding if your controller exposes a partial window: if the changed region is more than roughly half the screen, do a full refresh. You are paying the waveform cost anyway, and the residue risk is higher.

## How to verify it on your panel

Do not trust the vendor demo. Run this sequence on your own content:

1. Full refresh a frame with a large black block and fine text. Photograph it.
2. Apply ten partial updates that change only small regions. Photograph after each.
3. Compare the untouched area across the ten frames, at fixed light and exposure.
4. Do a full refresh, photograph again, and compare with step 1.

If the untouched area is stable and the full refresh returns to the step-1 image, partial is safe at that budget. If the area drifts, lower the budget. If a full refresh no longer returns to step 1, you have found the panel's limit the hard way — reduce the budget and stop using partial for that content.

## What we do not know

We have not characterised partial-refresh lifetime for a specific panel, and the number is rarely published. The gates above are structural: they follow from how the waveform works, not from a measurement campaign. Your datasheet, your temperature range and your content decide the actual budget.

For the mechanism behind the residue, read [E-Paper Ghosting](/en/articles/epaper-ghosting-causes-and-fixes/). For the frame-size arithmetic that tells you how much data a partial update actually moves, see the [image converter](/en/tools/epaper-image-converter/) and [the pipeline guide](/en/articles/epaper-engineering-field-guide/).

## Three questions that follow the gates

### My controller supports a partial window. Should I update only the 20 × 20 area that changed?

Only if the window overhead is smaller than the saving. Every partial update pays for a command sequence, a LUT selection and a BUSY wait regardless of area. Below roughly a tenth of the screen, packing a full frame and refreshing everything is often simpler and no slower. Measure both paths before optimising the window.

### Can I use partial refresh for a 2 fps animation?

Not within any budget that keeps the panel clean. Two frames a second spends a 20-update budget in ten seconds, and the residue never gets time to clear. Panels demonstrated at that rate are usually driven with waveforms outside the vendor's rated mode; the InkBoy article explains why that is not a lifetime guarantee.

### What happens if power is lost during a partial update?

The panel keeps whatever state the waveform reached — often a half-driven region that looks like a torn image. On the next boot, do a full refresh before displaying anything, and do not trust a cached framebuffer. Some controllers also leave BUSY asserted until they are re-initialised.
