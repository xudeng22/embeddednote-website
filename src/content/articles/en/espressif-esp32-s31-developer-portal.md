---
title: Espressif Updates Its ESP32-S31 Developer Site in English and Chinese
description: ESP32-S31 has a bilingual developer portal covering the dual-core RISC-V SoC, Wi-Fi 6, Bluetooth 5.4, Thread, Zigbee and gigabit Ethernet.
locale: en
translationKey: espressif-esp32-s31-developer-portal
pubDate: '2026-06-01'
category: mcu-soc
tags:
- Espressif
- ESP32-S31
- RISC-V
- Wi-Fi 6
- Bluetooth
draft: false
seoTitle: 'ESP32-S31: Espressif’s Bilingual Developer Portal'
seoDescription: ESP32-S31 has a bilingual developer portal covering the dual-core RISC-V SoC, Wi-Fi 6, Bluetooth 5.4, Thread, Zigbee and gigabit Ethernet.
author: EmbeddedNote
sourceUrl: https://esp32-s31.espressif.com/en
updatedDate: '2026-11-06'
---

Espressif's ESP32-S31 developer portal is available in English and Simplified Chinese. It collects chip documentation and board resources in one place, which is useful because the S31 combines several peripheral and radio features that engineers would normally compare across different MCU families.

The published specifications describe a **dual-core 32-bit RISC-V SoC at up to 320 MHz**, with **512 KB on-chip SRAM** and an interface for external high-speed PSRAM. Its communications include **2.4 GHz Wi-Fi 6, Bluetooth 5.4 (LE and Classic), and IEEE 802.15.4** for Thread/Zigbee applications. The presence of multiple standards is a hardware capability; application coexistence, stack maturity, certification requirements and achieved throughput still need project-specific verification.

![Espressif ESP32-S31 processor promotional image](/uploads/espressif-esp32-s31-developer-portal/espressif-esp32-s31-developer-portal-01.webp)

## Why the peripheral mix matters

Besides conventional UART, SPI and I²C work, the S31 includes **USB 2.0 High-Speed OTG**, camera and RGB display interfaces, JPEG support, a **Pixel Processing Accelerator (PPA)** and a **Gigabit Ethernet MAC**. The Ethernet MAC is not an integrated RJ45 port: a board still needs a suitable external PHY, magnetics and connector, plus driver and PCB work. Likewise, attaching a camera or display does not remove memory-bandwidth and buffer-allocation constraints.

For a multimedia interface, the first engineering question is not simply whether the chip has a JPEG block. It is whether the chosen camera, display, PSRAM, storage path and wireless workload fit the actual memory and bus budget. A 24-bit RGB interface refers to a pixel data bus width; it is not a promise of a particular panel resolution or frame rate.

| Feature | Design implication to check |
|---|---|
| 512 KB on-chip SRAM | Budget stacks, DMA buffers and real-time paths separately from external PSRAM |
| External PSRAM support | Confirm module pinout, actual bandwidth and memory allocation strategy |
| Wi-Fi 6 / BT / 802.15.4 | Verify coexistence and the selected SDK/protocol versions on the target board |
| 1000 Mbps Ethernet MAC | Include external PHY and board-level signal-integrity work |
| Camera, RGB, PPA and JPEG | Test end-to-end memory traffic, not merely isolated peripheral enablement |

## A sensible evaluation path

Start from the **official datasheet and the specific development-board schematic**, not only the feature diagram. Identify flash/PSRAM wiring, power rails, pins reserved by the module, USB clocking, PHY connections and SDK examples that are actually available for the chosen revision. Then bring up one interface at a time, measure memory use, and test concurrent radio plus display/camera operation. No throughput or power measurements on an ESP32-S31 board are claimed in this article.

**Original sources:** [ESP32-S31 product page](https://www.espressif.com/en/products/socs/esp32-s31) · [Official developer documentation](https://esp32-s31.espressif.com/en/docs) · [Series datasheet](https://documentation.espressif.com/esp32-s31_datasheet_en.html).

![Screenshot of the Chinese ESP32-S31 developer portal](/uploads/espressif-esp32-s31-developer-portal/espressif-esp32-s31-developer-portal-02.webp)

<!-- editorial-v3-20261106 -->
