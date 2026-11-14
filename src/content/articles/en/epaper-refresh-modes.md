---
title: 'E-Paper Refresh Modes: GC16, GL16, DU and A2, Explained'
description: 'A refresh mode is not a setting, it is a waveform table. What GC16, GL16, DU and A2 actually change, why A2 ruins photos and suits clocks, and how to pick one without guessing.'
seoTitle: 'E-Paper Refresh Modes: GC16, GL16, DU, A2'
seoDescription: 'What e-paper refresh modes mean: grayscale depth, clearing phase and frame count. When to use GC16, GL16, DU or A2, and why DU and A2 accumulate ghosting.'
locale: en
translationKey: epaper-refresh-modes
pubDate: 2026-11-14
category: display
tags: ['e-paper', 'waveform', 'refresh mode', 'gc16', 'a2', 'driver']
contentType: deep
series: epaper
supplyCta: true
---

You set a mode, call update, and the same image comes out three different ways: crisp but flickering, fast but dirty, or clean but slow. That is not a bug in the driver. A mode is a waveform table, and the table decides everything.

**In one sentence:** a refresh mode selects a LUT — how many frames the panel drives, which voltages each frame applies, and whether a clearing phase runs before the new image — so GC16 trades time for clean grayscale, while DU and A2 trade cleanliness for speed.

## What a mode actually changes

The controller does not "draw" pixels. It applies a sequence of voltage frames to the panel, one frame per panel scan. The LUT says, for each starting state and each target state, what voltage to apply in each frame.

So a mode is three decisions bundled together:

| Decision | Effect on the image |
| --- | --- |
| How many frames | Longer sequences settle the pigment further: cleaner image, slower update |
| Which voltages per frame | Determines whether intermediate grey levels are reachable at all |
| Whether a clearing phase runs | A black/white flush before writing erases history and removes residue |

The flicker you see during a full refresh is the clearing phase. It is not decoration; it is the panel erasing what was there before.

## The four families you will meet

Mode names come from the controller vendors and their demo code, and the families below appear across the UC-series and SSD-series parts. The exact LUT contents are per panel and often loaded from OTP, so treat the names as classes of behaviour, not as register values.

| Mode | Grey levels | Clearing phase | Relative speed | Where it belongs |
| --- | ---: | --- | --- | --- |
| GC16 | 16 | Yes | Slowest | Photos, colour, anything with gradients |
| GL16 | 16 | Reduced or none | Medium | Text pages, UI screens that need grey |
| DU | 2 | No | Fast | Small black/white changes: counters, cursors, partial windows |
| A2 | 2 | No | Fastest | Animation, menus, anything that changes every frame |

Two rows are worth staring at. **GC16 and GL16 have the same grey depth**; the difference is the clearing phase, and that is why one flickers and the other does not. **DU and A2 are both 1-bit**; A2 is shorter still, which is why it is the one that smears.

## Why A2 ruins photos and suits clocks

A 16-level image in a 1-bit mode is quantised to pure black or pure white before it ever reaches the panel. A photograph becomes a high-contrast stencil; a clock face does not care, because it is already black on white.

The same property explains the residue. A short waveform does not finish the transition for every pixel, so a little pigment stays where it was. Run A2 for a thousand frames and the "little" adds up; that is the ghost you see on a menu that has been open for an hour.

So the rule is not "A2 is bad". It is: **A2 is correct for content that is 1-bit and short-lived, wrong for content that is 4-bit or long-lived.**

## The history problem

Every partial or fast update leaves the film slightly off its ideal state. Two mechanisms help:

1. **A counter.** After N fast updates, force one GC16. The counter value comes from your tolerance: a clock might accept 100, a photo frame 20.
2. **Mode escalation by content.** If the incoming frame contains grey levels, use GL16 even if the last ten updates were DU.

Neither is optional in a product. Without a counter, a device that works perfectly in a demo will look dirty after a day on a desk — which is exactly the failure the [ghosting article](/en/articles/epaper-ghosting-causes-and-fixes/) describes from the physics side.

## Choosing by content, not by habit

| Content | Mode | Why |
| --- | --- | --- |
| Photo, artwork, colour | GC16 | Needs all 16 levels and a clean history |
| Text page, menu with icons | GL16 | Grey text stays grey, less flicker |
| Counter, cursor, small 1-bit region | DU | Fast, area-limited, acceptable residue |
| Animation, live UI | A2 | Only if you accept residue and schedule a full refresh |
| After a mode change or power loss | GC16 | Never trust the panel's state |

One more rule that saves debugging time: **after changing modes, do a full refresh before trusting the image**. The panel's film state does not follow your software's idea of it.

## How to verify on your own panel

You do not need a lab. A phone camera and five minutes:

1. Display a 16-step grey ramp in GC16 and photograph it. That is your reference.
2. Same ramp in GL16. If steps merge, the mode is not giving you 16 levels.
3. Display a black frame, then a white frame in DU, ten times. Photograph after the tenth: any grey left is residue.
4. Repeat with A2 and count how many cycles until the residue is obvious. That number is your counter budget.
5. Switch back to GC16 and confirm the residue clears. If it does not, the waveform is not the one the panel expects.

The photographs are the evidence; the numbers in a datasheet are the specification. Where they disagree, believe the panel.

## Where the names come from, and where they stop

The names GC16, GL16, DU and A2 come from controller families and the demo code vendors ship with their modules. They describe behaviour; they are not a standard.

- Two controllers can both offer "DU" with different frame counts.
- Some panels ship a LUT in OTP that you cannot modify; others expect you to upload one over SPI.
- Colour panels (Spectra 6) use their own waveform sets, and the mode names above do not map onto them one to one.

So the datasheet for your controller is the only authority for register values. This page is about choosing the behaviour you need before you go looking.

## Sources

- E Ink, [Spectra 6](https://www.eink.com/brand/detail/Spectra6) — the six-colour family whose waveform sets differ from the mono modes described here.
- E Ink, [Carta](https://www.eink.com/brand/detail/Carta) — the monochrome panel where GC16, GL16, DU and A2 are most often discussed.
- Mode names and their grayscale depth follow the LUT definitions shipped in the controller vendor demo code for these panels.
