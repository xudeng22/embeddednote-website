---
title: 'E-Paper Below Zero: What Actually Fails, and Why'
description: 'A panel rated 0–50 °C is specified at 0, not comfortable there. Five low-temperature failure modes, the physics behind them, and what you can and cannot compensate.'
seoTitle: 'E-Paper at Low Temperature: Failure Modes'
seoDescription: 'Why e-paper misbehaves in the cold: pigment mobility, incomplete waveforms, ghosting, brownout during refresh and condensation. Plus the rating boundary most designs miss.'
locale: en
translationKey: epaper-cold-failure
pubDate: 2026-11-14
category: display
tags: ['e-paper', 'temperature', 'waveform', 'reliability', 'outdoor']
contentType: deep
series: epaper
supplyCta: true
---

A module datasheet says 0–50 °C and everyone reads it as "works down to zero". It means something narrower: at 0 °C the part is still **specified**, and below it the manufacturer is no longer telling you anything. The failures that appear in that gap are consistent, and they are worth knowing before a product ships to a place with winter.

**In one sentence:** cold thickens the fluid the pigment moves through, so the same waveform moves less pigment in the same time — the image gets lighter, partial updates leave more residue, and anything that interrupts a refresh mid-sequence leaves a permanent mark.

## What temperature actually changes

An electrophoretic pixel is pigment suspended in a fluid. Moving it is a matter of applying a field long enough for the particles to travel. How fast they travel depends on the fluid's viscosity, and viscosity rises steeply as temperature falls — a rule of thumb for many liquids is that viscosity roughly doubles for every 10 °C drop near room temperature.

Lower mobility means the same voltage applied for the same number of frames moves the pigment a shorter distance. If the waveform was tuned at 25 °C, then at 0 °C it may not finish the transition. That is the root of everything below; the rest is how it shows up.

The panel's answer to this is a set of temperature-compensated waveform tables, selected at run time using the panel's temperature sensor. Whether your driver uses them is a software question — and a panel with a sensor that nobody reads is a panel running the 25 °C table in a freezer.

## Five failure modes

| What you see | Mechanism | How to recognise it | What helps |
| --- | --- | --- | --- |
| Image looks washed out, text grey instead of black | Incomplete transition; pigment stops short of the target state | Contrast drops gradually as temperature falls, recovers in a warm room | Temperature-compensated LUT; longer waveform; warm the product |
| Ghosting appears after far fewer partial updates | Each partial update finishes less of its transition, so residue accumulates faster | The same update count that was clean at 25 °C leaves marks at 0 °C | Shorten the partial budget when cold; force a full refresh sooner |
| Refresh takes longer, BUSY stays high | Controller stretches the waveform for the temperature, or waits for it | Measured refresh time grows with cold; the datasheet time is a room-temperature figure | Budget the time; do not poll BUSY with a fixed timeout |
| A permanently darker or lighter patch | The waveform was interrupted — power loss, brownout, reset — leaving the film half-driven | Appears at the moment of a supply dip, often on cold batteries | Power-good gating; a full refresh after any aborted update |
| Fog or droplets on the panel, then a bad update | Condensation when a cold unit enters a warm, humid room | Happens on the first power-on after bringing a unit indoors | Let it acclimatise sealed; update only after it reaches operating temperature |

The fourth row is the one that ends up in production. A cold battery has higher internal resistance, so the peak current of a refresh pulls the rail down; the controller resets, the waveform stops at an arbitrary frame, and the panel keeps whatever state it reached. Nothing in the image tells you this happened — only the patch does, later, permanently.

## The rating boundary, read properly

The numbers below come from module catalogues and datasheets we work with, and they are not uniform:

| Family | Operating range | Note |
| --- | --- | --- |
| Black/white | 0–50 °C | The common case; two parts in a 67-model catalogue are 0–40 °C |
| BWR / BWRY (four colour) | 0–40 °C | Every four-colour part we looked at is 10 °C narrower than mono |
| E6 six colour | 0–50 °C | Datasheets for the 13.3 and 31.5 inch parts state 0 to +50 °C |
| Marquee (large signage) | −20 to 65 °C | The outlier: built for outdoor signage |
| One N-Color part | 15–35 °C | A reminder that "e-paper" is not one temperature class |

Storage is a separate number and usually much wider: −25 to +60 °C on the E6 datasheets. Storage range tells you the panel survives the trip, not that it can be written to at those temperatures.

The practical reading: **0 °C is a specification limit, not a comfort zone.** A product specified to work at 0 °C should be tested at 0 °C, with the waveform the firmware will actually select at that temperature.

## What you cannot fix in firmware

- **Raising the drive voltage** moves pigment further, and also exceeds the panel's rated waveform. The film does not forgive overdrive; it shows up as reduced lifetime and permanent residue.
- **Stretching the waveform indefinitely** works until the update takes longer than the product's power budget allows, which is a different failure: a brownout in the middle of a refresh.
- **Ignoring DC balance** while editing tables accumulates net charge in the film. Every modified waveform must keep the same charge integral as the original, which is why vendor LUTs are not a good place to experiment.

What you *can* do: select the LUT the panel already provides for that temperature, warn the user, delay the update, or warm the product. Those are product decisions, not driver tricks.

## A test you can run in a kitchen

1. Put the panel, sealed with desiccant, in a fridge at about 4 °C for an hour.
2. Power it up **still cold**, display a 16-step grey ramp plus a text block, and photograph.
3. Do ten partial updates of a black/white pattern, photograph each tenth.
4. Force a full refresh, photograph again.
5. Bring it to room temperature, repeat steps 2–4, and compare.

What you are looking for: how many grey steps merge at 4 °C, how many partial updates it takes before residue shows, and whether the full refresh still clears it. If the full refresh cannot clean the panel at cold, that is the panel telling you the waveform in use is not the cold one.

## Designing for it

- **Read the temperature sensor.** If the panel has one, the firmware should select a LUT by temperature; if it does not, the product needs its own sensor and a policy.
- **Gate updates on power, not just on time.** A supply monitor that aborts the update before it starts is cheaper than a permanent patch.
- **Plan for slower refreshes when cold.** A 2 s refresh at 25 °C can become noticeably longer; if your watchdog or user feedback assumes the warm number, it will misbehave exactly when the product matters.
- **Treat condensation as a mechanical problem.** Sealed enclosure, desiccant, and a rule that a unit coming in from the cold is not updated until it has acclimatised.

## Sources

- E Ink, [Spectra 6](https://www.eink.com/brand/detail/Spectra6) — six-colour family, 0–50 °C on the datasheets we read.
- E Ink, [Marquee](https://www.eink.com/brand/detail/marquee) — large-format signage, −20 to 65 °C, the exception that proves the rule.
- Operating and storage ranges for the mono, BWRY and E6 families come from the module datasheets and catalogues quoted above.
