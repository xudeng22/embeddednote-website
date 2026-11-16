---
locale: en
translationKey: lightink-watch
pubDate: '2026-11-16'
updatedDate: '2026-11-16'
category: display
draft: false
contentType: deep
series: epaper
supplyCta: true
author: EmbeddedNote
sourceUrl: https://github.com/DarkZeros/LightInk
title: 'LightInk: A Solar E-Ink Watch That Wakes in Microseconds'
description: 'LightInk is an ESP32-PICO-D4 e-paper watch that refreshes from the RTC wake stub instead of a full boot. The author reports months on a 100 mAh cell; here is the design and its limits.'
tags:
- LightInk
- ESP32-PICO-D4
- E-Paper
- Solar Power
- Low Power
- Watchy
- TPS63900
- Open Hardware
seoTitle: 'LightInk: Solar E-Ink Watch With a 2 µA Refresh'
seoDescription: 'Inside LightInk: ESP32-PICO-D4, 1.54-inch e-paper, TPS63900, RTC wake-stub SPI and the power math behind a solar watch that runs for months.'
---

An e-paper watch is not a new idea. Watchy put an ESP32 and a 1.54-inch black-and-white panel on an open PCB years ago. LightInk takes the same shape and asks a harder question: can the watch behave like a 1990s solar digital watch, where a small cell keeps it alive without a charging routine? Daniel Ansorregui has been building it since 2019, with long gaps, a dozen PCB builds and ten case iterations. The repository is at v4, licensed GPL-3.0, and the Hackaday page has the build log and two demo videos.

![LightInk black and white versions on a desk](/uploads/lightink/lightink-hero.webp)

*Two LightInk units. The solar cell sits above the 1.54-inch 200 × 200 monochrome e-paper panel. Image: Daniel Ansorregui / LightInk.*

## What the watch is

The board is **31 × 41 mm**, **two layers**, **0.6 mm thick**, and single-sided. The display rests on the back of the PCB, which means no components are allowed there. The main parts are an **ESP32-PICO-D4**, a **1.54-inch 200 × 200** e-paper panel (SSD1681, GDEH0154D67 / 0154BN-D67 class), a **TPS63900** buck-boost converter with 2.7 V and 3.0 V settings, a **PCF8563** RTC with a 32.768 kHz crystal, a **TP4054** charger, and a **Wio-SX1262** LoRa module. There is also a GPS receiver, a piezo buzzer, a vibration motor, an LED, and four capacitive touch pads.

The solar cell is a **Panasonic Amorton 5815**: 31.2 × 10.8 × 1.1 mm, 4.5–5.2 V, 1.1–2.5 mA. It is wired directly across the battery. There is no MPPT tracker and no separate solar charger.

| Block | Part | Notes |
| --- | --- | --- |
| MCU | ESP32-PICO-D4 | Dual-core, Wi-Fi/BLE, 28 ms cold boot |
| Display | 1.54 in, 200 × 200, SSD1681 | Black/white, FPC, mounted on PCB back |
| Power | TPS63900 | 75 nA quiescent, 1 A, 1.8–5 V, two output voltages |
| RTC | PCF8563 + 32.768 kHz | Keeps time while the ESP32 is off |
| Charger | TP4054 | USB charging |
| Radio | Wio-SX1262 | LoRa, power-gated |
| Position | GPS module | Power-gated, slot needs filing on v4 |
| Extras | Buzzer, motor, LED, touch | All off unless used |

## The 28 ms problem

The interesting engineering is not the BOM. It is the boot time.

An ESP32-PICO-D4 takes about **28 ms** to boot from flash and draws roughly **1 mAs** doing it. According to the author, that boot alone was about **60% of the total energy** of a display update. You can optimize the application, shrink the binary and slow the SPI clock, but the ROM and flash load still happen before your code runs.

LightInk moves the display update into the **RTC wake stub**. The stub is a function pointer kept in RTC memory; on wake, the ESP32 jumps to it before loading the application from flash. The catch is that the stub cannot call normal code or use the usual SPI driver. Everything has to be reimplemented against registers: a small SPI engine, the panel command sequence, the partial-update window and the deep-sleep exit.

The author wrote that **uSPI** by hand, with no logs and no debugger in RTC memory, and used a PicoScope to check the waveforms. Once it worked, the ESP32 could wake, write the changed region of the display controller, start the panel refresh and go back to deep sleep in **under 1 ms**. The panel finishes the refresh while the ESP32 is already off, which also removes the 1 mA light-sleep current that a normal driver would burn while waiting.

![LightInk disassembled units showing solar cell, PCB, display and battery](/uploads/lightink/lightink-internals.webp)

*Two units opened up: solar cell and main board on the left, display, FPC and battery on the right. Image: Daniel Ansorregui / Hackaday.io.*

## The power math

With the wake-stub path, the author reports an average of about **2 µA** for a time update. A **100 mAh** cell is quoted at **6–10 months**; his own unit ran for **9 months** before he retired it for newer hardware. The README also notes that a **200 mAh** Watchy-style cell could last around **400 days** in theory. For comparison, the original Watchy was measured in weeks, and the author’s patched Watchy reached about a month.

Those numbers are the author’s measurements, not an independent lab result. They depend on how often the display updates, how much the RTC and touch circuitry draw, temperature, cell age, and whether Wi-Fi or LoRa is used. The 400-day figure is an extrapolation from a smaller cell, not a recorded run.

The voltage choice is part of the same budget. The author tested the TPS63900 down to **2.7 V**: 3.3 V and 3.0 V worked, 2.6 V left the display dead, and 2.7 V worked until Wi-Fi started. The final design keeps the rail at **2.7 V** and switches to **3.0 V** only when Wi-Fi or another high-current task needs it. The lower rail cut roughly **15%** from the measured consumption.

He also tried an **ESP32-S3** version. The S3 did not like 2.7 V, its RTC wake path took about **10 ms**, and its RTC oscillator current was much higher than the PICO-D4 plus external 32 kHz crystal. That branch is preserved as HWv10 and abandoned. The PICO-D4 is not the lowest-power MCU available, but it is the one whose wake path fits this design.

## Solar, battery and the parts that bite

The solar cell is connected directly to the battery. That is simple and cheap, but it has consequences. Under direct sun the cell can reach about **6 V**, and a fully charged cell can keep pushing energy into the battery. The PCB notes warn that a long, fully charged exposure can stress the battery; this is not a product with a solar charge controller.

The v4 board packs LoRa, GPS, buzzer, motor and LED into the same shell, leaving room for a cell of roughly **30 mAh**. A 30 mAh cell cannot absorb the **100 mA** peaks from the display and Wi-Fi without the rail sagging, so the author recommends at least **50 mAh**, or more decoupling. The BOM and PCB notes also list two hardware traps: the Wio-SX1262 antenna pad is tied to ground, so the PCB antenna has to be soldered manually or an external antenna used; and the GPS module slot needs filing to fit.

The case is two 3D-printed pieces, glued together. It is not waterproof, and the touch pads may false-trigger when wet. The author describes the project as a personal build, not a product; there is no certification, no environmental testing and no production test.

[![LightInk solar demo video](/uploads/lightink/lightink-case.webp)](https://youtu.be/erjeWSajqhQ)

*▶ The solar demo on YouTube. The long part in the case is the Amorton 5815 cell, wired directly across the battery. Image: Daniel Ansorregui / Hackaday.io.*

## What the firmware does

The firmware is an ESP-IDF project. It handles touch settings and sensitivity, NTP time sync and time zones, moon phase, sunrise and sunset, the LED, vibration, the buzzer, LoRa receive and BPSK transmit, and GPS. There is an Android companion app for BLE pairing and settings sync, plus a BLE protocol document in the repository.

The repository also includes the EasyEDA PCB project, BOM, Gerber files, case STL files, the schematic in PDF and SVG, and a detailed `HISTORY.md` that records the dead ends. That history is unusually useful: it explains why the S3 failed, why the board moved to 2.7 V, and why the display driver had to be rewritten instead of tuned.

[![LightInk feature demo video](/uploads/lightink/lightink-panel.webp)](https://youtu.be/qBj7sOVVzNI)

*▶ The feature demo on YouTube. The panel is a 0154BN-D67, 200 × 200 black/white, driven by an SSD1681. Image: Daniel Ansorregui / Hackaday.io.*

![LightInk v4 schematic](/uploads/lightink/lightink-schematic.webp)

*The v4 schematic: ESP32-PICO-D4, TPS63900, PCF8563, Wio-SX1262, charger, display and the power-gated peripherals. Image: LightInk repository, GPL-3.0.*

## What we checked

This article is based on the repository, the Hackaday project page and the two demo videos. We did not receive a unit, a power profile or a production file set beyond what is public.

| Claim | Where it comes from | What it means |
| --- | --- | --- |
| 2 µA average update, 6–10 months on 100 mAh | README and Hackaday build log | Author’s measurement on his units, not a lab test |
| 9 months of use | Hackaday log | One watch, one cell, one usage pattern |
| 400 days on 200 mAh | README | Extrapolation, not a recorded run |
| 28 ms boot / 60% of energy | Hackaday log | Matches the author’s power traces |
| Under 1 ms wake-stub update | README and Hackaday log | Depends on the partial-update size and panel |
| 12 PCB revisions / 10 cases | HISTORY.md | Project history, not a quality claim |
| GPL-3.0 | Repository license | Open hardware/firmware, attribution required |

The useful takeaway is not “solar watches are back.” It is that the ESP32’s boot cost is part of the power budget, and moving one display update into the wake stub changes the energy equation more than another round of application-level optimization. That idea is reusable even if the watch itself is not.

![LightInk display wiring and panel label](/uploads/lightink/lightink-panel-wiring.webp)

*The display FPC and battery wiring around the 31 × 41 mm board. Image: Daniel Ansorregui / Hackaday.io.*
