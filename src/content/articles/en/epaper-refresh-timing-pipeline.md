---
title: 'Why a Fast SPI Bus Does Not Make E-Paper Refresh Fast'
description: 'Separate e-paper image transport from controller preparation, waveform driving and optical settling; a reproducible timing budget and measurement protocol.'
locale: en
translationKey: epaper-refresh-timing-pipeline
pubDate: '2026-11-06'
category: display
tags: [E-Paper, SPI, Refresh, Timing, Waveform, Measurement]
author: EmbeddedNote
draft: false
contentType: deep
series: epaper
seoTitle: 'E-Paper Refresh Time — SPI Transfer vs BUSY and Waveform Timing'
seoDescription: 'Learn how to budget SPI transport, command overhead, panel drive, BUSY time and optical settling, with sample calculations and a real-hardware logging checklist.'
---

A display can accept its pixel data over SPI in a fraction of a second and still take many seconds to update. That is not necessarily a driver bug. E-paper must move charged pigment particles using controlled voltage waveforms, and the panel's update behavior is a separate physical process from moving bytes into controller memory.

A useful performance report should answer **three distinct questions**: How long did it take to *send the image*? How long was the controller *busy driving the panel*? When did the *visible image become stable enough for the application*? One “refresh time” number hides the distinction.

![Timing stages of an e-paper refresh](/images/p0/epaper-refresh-timing-pipeline-cover.webp)

## A timing equation with explicit boundaries

For a sequential implementation, a first-order accounting model is:

`T_total = T_prepare + T_transfer + T_trigger + T_busy + T_settle`

- **Prepare:** resize, palette mapping, pixel packing, file read and any device-specific buffer copy.
- **Transfer:** SPI transactions carrying image bytes, including command/address overhead and software gaps.
- **Trigger:** controller command sequence, power sequencing or hand-off before waveform execution.
- **Busy:** the controller's reported update period, interpreted using the correct panel/driver BUSY polarity.
- **Settle:** any additional visible change after the controller reports completion, measured separately if relevant.

These terms should not be blindly added if a real implementation overlaps them. Some controllers can receive partial image data while another operation proceeds. The only defensible total is the observed start-to-finish interval with clear timestamp boundaries.

## The byte transfer has an easily checked lower-bound calculation

Take **800 × 540** pixels with a hypothetical *continuous* 4-bit index buffer. That is `800 × 540 × 4 / 8 = 216,000 B`. At an assumed SPI clock of **20 MHz** and ideal continuous clocking, the time to clock out that many bits is:

`216,000 × 8 / 20,000,000 = 0.0864 s`

At 4 MHz the same arithmetic is **0.432 s**; at 1 MHz it is **1.728 s**. These are **ideal serial clock-time calculations**, not measured MCU-to-controller transfer durations. Bus setup, chip-select gaps, conversion, DMA setup, required per-line metadata, and controller throughput may increase the actual time. Some displays accept completely different frame formats, so 216,000 B cannot be treated as a universal update size.

| Assumed SPI clock | Ideal 216,000-byte clocking time |
|---|---:|
| 1 MHz | 1.728 s |
| 4 MHz | 0.432 s |
| 20 MHz | 0.0864 s |

The dramatic difference in this table says **nothing** by itself about pigment-motion time. Increasing SPI speed from 4 MHz to 20 MHz can save, at most, roughly 0.346 seconds of ideal bus clocking for this example; it cannot eliminate a separate 12-second waveform phase.

## Why the BUSY signal is not the whole story

A controller's BUSY output is a digital view of its internal state. The logic level, transitions and meaning of “ready” depend on the specific driver. Some modules may also require a delay or power-down sequence. A visible panel can show transient flashes, intermediate colors or residual change during and sometimes after the reported busy interval.

Therefore publish both **electrical completion** and, when useful, an **optical criterion** (for example, a repeatable camera or photodiode threshold) instead of treating the BUSY edge as automatic proof that every pixel reached its final appearance. A smartphone video can illustrate behavior but is a poor substitute for calibrated timing without a timestamped reference and controlled lighting.

Do not copy fast-refresh waveforms, write undocumented OTP commands or change drive voltages merely to achieve an attractive headline. Waveform safety, ghosting, temperature compensation and panel lifetime are hardware-specific and require the panel manufacturer's guidance.

## A worked model—clearly not an oscilloscope result

Suppose an illustrative system has 0.12 s preparation, 0.30 s transfer, 0.08 s trigger overhead, 15.00 s BUSY and 0.20 s additional observed settling. The purely **hypothetical** sequential budget is `0.12+0.30+0.08+15.00+0.20 = 15.70 s`. The waveform/BUSY stage accounts for `15/15.70 = 95.54%` of that example.

That suggests where optimization effort would go **if those numbers were actually measured**: improving SPI by 100 ms does little compared with changing the waveform policy—yet changing the waveform may reduce image quality or harm hardware. Real product trade-offs must begin with verified device limits, not just maximizing update speed.

## How to measure without misleading yourself

Set up a GPIO or logic-analyzer channel at each software milestone, together with SPI clock/chip select, controller BUSY, supply enable if accessible, and a synchronized optical view when feasible. Record:

1. `t0` — user/app requests update (include BLE/Wi-Fi transfer only if this is the intended metric).
2. `t1` — color quantization and frame packing complete.
3. `t2` — first SPI data byte; `t3` — final SPI byte completed.
4. `t4` — refresh trigger issued.
5. `t5` — BUSY deasserted, using the controller-specific polarity.
6. `t6` — defined visible completion criterion, if measured.

Test full updates and permitted partial updates separately, at documented ambient/panel temperatures, on the same content and power conditions. Record the panel part number, controller ID, waveform version, full/partial mode, previous displayed image, SPI clock and firmware revision. Repeat at least ten times, report median plus spread, and include outliers rather than averaging them away.

A measurement report should include a scope trace or raw log, timestamps, definitions, and a photo of the actual test configuration. Without that evidence, call the numbers calculations or preliminary estimates—not “benchmarked” results.

## Where to optimize after measuring

If preparation dominates, profile image conversion and memory copies. If SPI dominates, examine effective transaction sizes, DMA, clocks and extra framing while respecting device timing limits. If BUSY dominates, check whether the selected manufacturer-supported update mode matches the use case. If a wireless transfer precedes every update, measure radio time separately with the [BLE Transfer Planner](/en/tools/ble-throughput-calculator/). If incorrect colors or layout are the problem, start with the [RAW4 and palette checklist](/en/articles/epaper-palette-raw4-packing-guide/) rather than shortening a waveform.

**Evidence boundary:** SPI times and the 15.70-second split are auditable calculations with explicit assumptions. This article does not present unrecorded real-world timings, undocumented panel commands, or universal claims about any E Ink technology family.

**Background:** [E Ink—How it works](https://www.eink.com/tech/detail/How_it_works) · [EmbeddedNote RAW4 conversion guide](/en/articles/epaper-palette-raw4-packing-guide/) · [EmbeddedNote BLE planner](/en/tools/ble-throughput-calculator/).
