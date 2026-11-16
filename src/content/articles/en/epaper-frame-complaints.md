---
title: 'Colour E-Paper Frames: Which Complaints Are Physics, Which Are Firmware'
description: 'The five complaints that show up in every review of a colour e-paper frame, sorted into the layer each one belongs to: panel physics, waveform, firmware or product decision.'
seoTitle: 'Colour E-Paper Frames: Physics vs Firmware Complaints'
seoDescription: 'Why colour e-paper frames get bad reviews: muted colour and slow refresh are panel physics, ghosting is waveform policy, and app failures are product decisions. Buyers guide.'
locale: en
translationKey: epaper-frame-complaints
pubDate: 2026-11-16
category: display
tags: ['e-paper', 'colour', 'photo frame', 'reviews', 'selection']
contentType: deep
series: epaper
supplyCta: true
---

Read enough reviews of colour e-paper photo frames and the same sentences come back: the colour looks grey, changing a picture takes too long, the app will not connect, a mark stays on the screen after a while. They read like one problem. They are four different problems, and knowing which is which decides whether you are buying a limitation or a bug.

**In one sentence:** muted colour and seconds-long refreshes are the panel's physics and no firmware update will remove them; ghosting is a waveform policy the product controls; and a failing app is a decision someone made, unrelated to the display.

## The five complaints, sorted

| What reviewers say | What it actually is | Can it be fixed? |
| --- | --- | --- |
| "Colours look washed out / grey" | Physics: six pigments, one colour per pixel | No — only made better in software |
| "Changing the picture takes forever" | Physics (waveform length) plus transfer | Partly — a size and TCON choice |
| "There's a mark where the old image was" | Waveform policy: partial-refresh residue | Yes — with a refresh budget |
| "The app is unusable / will not connect" | Product decision: network discovery, pairing | Yes — and it is not about the screen |
| "It costs as much as a tablet" | Panel area and yield | No, but you can choose a smaller area |

The useful part of that table is the third column. Two of the five are things a buyer must accept; three are things a supplier can get right or wrong.

## Why the colour looks grey, and why it stays that way

A colour e-paper pixel is not a small RGB emitter. It is a cavity with several pigment particles, and the panel drives one of them to the surface. Spectra 6 has six states per pixel: black, white, red, yellow, blue, green. Three bits of information, carried in a four-bit nibble.

**One pixel shows one colour.** There is no per-pixel mixing, so the "65,000 colours" or "millions of colours" figures some listings quote describe what dithering produces across neighbouring pixels, not what a pixel can do. When a photograph is converted, every pixel is snapped to one of six values and the rest is spatial averaging.

That has a physical consequence: the reachable gamut is the area spanned by those six pigments, and it sits inside sRGB. Saturated magenta and cyan — the colours that need both high luminance and high chroma — are not reachable at all. Skin tones survive because they sit near the neutral axis, but they are where a poor conversion shows first, as too-red, too-grey or blotchy faces.

This is the layer no update changes. What software can do is choose the nearest colour well and dither intelligently, which is why two frames with the same panel can look noticeably different. If a review complains about colour on one product and praises it on another, suspect the pipeline, not the panel.

## Why a new picture takes seconds

An e-paper refresh is a waveform: a sequence of voltage frames that moves pigment. A full refresh on a small panel is around two seconds in the worked example on this site; partial updates are around 0.4 seconds. At 30 inches and above, the same waveform runs over far more pixels and rows, and the panel is driven through a timing controller rather than straight from the host.

So the wait a reviewer experiences is mostly *panel time*, not download time. This is worth checking before blaming Wi-Fi: a 40.5-inch frame carries 6.30 MB per image, and at about 1.1 Mbit/s over BLE that is roughly 48 seconds of transfer alone — more than the refresh. [Refresh modes](/en/articles/epaper-refresh-modes/) explains which waveform runs; [our power model](/en/articles/epaper-power-model/) has the energy side.

## Why a mark stays behind

Ghosting is pigment that did not finish moving. Short partial waveforms leave a little behind every time, and without a policy the residue accumulates until the "old image" is visible under the new one. That is a design decision: count the partial updates, force a full refresh before the count gets uncomfortable, and at large sizes use a controller with large-format residue handling.

[E-paper ghosting](/en/articles/epaper-ghosting-causes-and-fixes/) covers the mechanism and the ten-frame test that shows how much residue your panel tolerates. A frame that shows marks after a month is usually a product without a counter.

## Why the app fails, and why that is a separate problem

The most common one-star review of a colour frame is not about the display. It is about pairing: a frame that insists on a fixed IP address, does not advertise itself on the network, or requires an account before it shows a picture.

None of that involves the panel. A frame needs to find the network, be found by the phone, accept an image and acknowledge it. Those are ordinary software decisions, and they are where a hardware team without a software team usually loses.

## What to ask before buying

Five questions, in the order that saves the most time:

1. **What is the panel, exactly?** Brand family and part number. E6 and Kaleido are different trade-offs, and a listing that only says "colour e-paper" hides which one you get. The [selection table](/en/e-paper/selection/) lists 40 panels with their active areas and frame sizes.
2. **How dense is it?** Pixels per inch. The 2:3 family sits around 131 ppi at every size; the 16:9 31.5-inch panel is 94. The [size chart](/en/articles/epaper-size-chart/) has the numbers.
3. **How big is one frame?** In megabytes. That decides how long a change takes and whether the product needs Wi-Fi or can live on BLE.
4. **How does it handle residue?** A counter, a full-refresh schedule, or a controller with large-format ghosting handling.
5. **How does it join the network?** mDNS, BLE provisioning, or a hardcoded address.

If a supplier cannot answer 1, 3 and 4, the review you will read in six months is already written. If you are comparing quotes right now, the [supply page](/en/supply/) lists the ranges we stock and how samples work.

## What this page does not do

It does not name products or repeat review quotes, and it does not measure reflectance or colour accuracy on any frame — we have not run that comparison. What it does is put each complaint in the layer where it belongs, so a buyer knows what to accept and what to demand.

## Sources

- Our [selection table](/en/e-paper/selection/) — active areas, resolutions and frame sizes for the panels discussed here.
- Our [size chart](/en/articles/epaper-size-chart/) — ppi and packed bytes per resolution.
- E Ink, [Spectra 6](https://www.eink.com/brand/detail/Spectra6) — the six-colour family, its colour set and contrast claim.
- E Ink, [Kaleido](https://www.eink.com/brand/detail/Kaleido) — the filter-based alternative used in some frames.
