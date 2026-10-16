---
title: 'FERRIT: An Open-Source 256MB F-RAM Archive Designed for 200-Year Retention'
description: Machdyne’s FERRIT is a modular ferroelectric-RAM archive with removable cards, an RP2040 USB controller,
  and a claimed retention target of up to 200 years.
locale: en
translationKey: ferrit
pubDate: '2026-06-15'
category: open-source
tags:
- GitHub
- F-RAM
- FRAM
- RP2040
- Storage
- KiCad
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/machdyne/ferrit
seoTitle: 'FERRIT Open-Source F-RAM Archive: 256MB and RP2040'
seoDescription: 'Inside Machdyne FERRIT: removable F-RAM cards, a 16-slot backplane, RP2040, QSPI address decoding,
  USB mass storage, and 256MB target capacity.'
---

Most storage products compete on capacity. Machdyne’s **FERRIT** takes a different approach: it trades gigabytes for longevity, using **ferroelectric RAM (F-RAM)** in a modular archival system. The project describes a **data-retention target of up to 200 years**.

The capacity figure is worth getting right. Although the original article’s headline said 250MB, the published design target is **up to 256MB**. That is tiny by modern storage standards, but sufficient for calibration records, device certificates, cryptographic material and small archival datasets.

![Modular FERRIT digital archival hardware](/uploads/ferrit/ferrit-01.webp)

## Three replaceable hardware modules

FERRIT is divided into a controller, removable memory cards and a backplane. The **FERRIT-CY** controller handles USB and bus access; the **FERRIT-M8** card carries the F-RAM devices; and the **FERRIT-16** backplane provides **16 card slots**.

![FERRIT-16 backplane and removable memory cards](/uploads/ferrit/ferrit-02.webp)

Separating those functions is practical. A failed controller can be replaced without discarding the memory cards. If the host interface eventually becomes obsolete, a different controller can be developed while leaving the storage media in place.

Source files: [machdyne/ferrit on GitHub](https://github.com/machdyne/ferrit) and the [Machdyne FERRIT project page](https://machdyne.com/ferrit/). The repository includes KiCad schematics, PCB layouts, a bill of materials and firmware.

## Storage designed for a long service life

Machdyne lists long retention, high write endurance, modularity, standard USB mass-storage compatibility and auditable open hardware among FERRIT’s goals. The **200-year retention and radiation-resistance figures are project claims**, not evidence that an assembled system has undergone two centuries of real-world testing. Checksums, controlled storage conditions and independent backups remain important for any serious archive.

## RP2040 control and two-stage address decoding

The **FERRIT-CY** controller uses an **RP2040** and presents the array to a host as a conventional USB mass-storage device over USB Full-Speed. A **TLV62568** steps the USB 5V rail down to 3.3V. An **M95P32 32Mbit SPI NOR** stores controller firmware rather than the archived user data.

![FERRIT-CY RP2040 controller card](/uploads/ferrit/ferrit-03.webp)

On the memory card, eight F-RAM chips share QSPI clock and data lines; a **3-to-8 decoder** generates the chip selects. There is a distinction between the current **FERRIT-M8 card with eight mounted devices** and the repository’s **maximum addressable count of 16 devices per card**. The latter corresponds to the proposed double-sided capacity configuration.

![FERRIT-M8 memory card schematic](/uploads/ferrit/ferrit-04.webp)

The backplane adds an **SN74HC154** for 16-way slot selection. First the controller selects a card, then the decoder on that card selects a memory IC. At the documented addressable limit, **16 slots × 16 devices × 1MB per device** gives 256MB.

## Components and firmware

- **RP2040:** dual-core Cortex-M0+ microcontroller handling USB MSC, address mapping and QSPI transactions.
- **MB85RQ8MXPF:** 1MB QSPI F-RAM used for the archived data.
- **M95P32:** 32Mbit SPI NOR used for controller firmware.
- **74LS138 / SN74HC154:** chip-select and slot-select decoding.
- **TLV62568:** synchronous step-down conversion from 5V to 3.3V.

The firmware uses the **Pico SDK** and **TinyUSB**. On each read or write, `mapper.c` maps the logical block address to a slot, a chip select and an offset within the selected device. Requests that span a chip boundary are split before the transfer continues on the next IC. The mapping code is published alongside the hardware files.

FERRIT is interesting less for its capacity than for its maintainability: replaceable modules, a familiar USB interface and a transparent address-mapping scheme make the underlying memory technology easier to inspect and evolve.
