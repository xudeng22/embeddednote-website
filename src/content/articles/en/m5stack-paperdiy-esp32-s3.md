---
title: 'M5Stack PaperDIY: A $25 ESP32-S3 E-Paper Kit with Schematics'
description: 'M5Stack PaperDIY pairs a 4.7-inch grayscale e-paper display with an ESP32-S3, an 8-bit parallel interface and switchable display power.'
locale: en
translationKey: m5stack-paperdiy-esp32-s3
pubDate: '2026-10-21'
category: display
tags:
  - M5Stack
  - ESP32-S3
  - E-Paper
  - PaperDIY
  - Hardware Design
draft: false
contentType: deep
series: epaper
seoTitle: 'M5Stack PaperDIY: $25 ESP32-S3 E-Paper Kit and Schematics'
seoDescription: 'Inside M5Stack PaperDIY: a 4.7-inch, 960 × 540 e-paper display, ESP32-S3, parallel data interface, power management and ESP-IDF firmware.'
updatedDate: '2026-11-11'
supplyCta: true
---

M5Stack sells its PaperDIY e-paper development platform in two versions. The $25 Assembly Kit includes a 4.7-inch display, controller board, 140 mAh battery and acrylic retaining plate for user assembly. The $29.90 Complete Kit uses the same core electronics, preassembled in a 3D-printed enclosure. Either version provides a practical starting point for a desk calendar, status display or other device that updates only occasionally. The display connection, power circuitry and basic mounting hardware are already part of the design.

[![M5Stack PaperDIY Complete Kit: front and rear hardware overview](/uploads/paperdiy/paperdiy-cover.webp)](/uploads/paperdiy/paperdiy-cover.webp)

*PaperDIY Complete Kit, showing the front and rear hardware layout, display, battery and connectors. Image: M5Stack.*

[![PaperDIY Assembly Kit components](/uploads/_external/K159-PaperDIY-Assembly-Kit_main_pictures_02.webp)](/uploads/_external/K159-PaperDIY-Assembly-Kit_main_pictures_02.webp)

*The Assembly Kit includes the display, retaining plate, controller PCB and battery. Image: M5Stack.*

Both kits use a 4.7-inch, 960 × 540 e-paper panel with 16 grayscale levels. The screen has no touch layer, and PaperDIY omits the sensors fitted to the older M5Paper. Users can interact through two buttons or add peripherals via the expansion connectors. The ESP32-S3-WROOM-1-N16R8 module provides a dual-core MCU, 16 MB of flash, 8 MB of PSRAM, 2.4 GHz Wi-Fi and Bluetooth LE. The board also includes a microSD slot, USB-C port and two 12-pin FPC expansion connectors carrying interfaces such as SPI and I²S.

The included 140 mAh battery is better suited to applications that sleep between updates than to continuously connected displays. M5Stack specifies an operating current of 40.95 mA at 4.2 V, with peaks up to 161 mA. Those figures do not establish battery life, which depends heavily on sleep current, Wi-Fi duty cycle and refresh frequency.

[![M5Stack PaperDIY Complete Kit front view](/uploads/_external/K159-B_PaperDIY_Complete_Kit_main_pictures_02.webp)](/uploads/_external/K159-B_PaperDIY_Complete_Kit_main_pictures_02.webp)

*Complete Kit in its 3D-printed enclosure. Image: M5Stack.*

[![PaperDIY ESP32-S3 controller board](/uploads/_external/K159-PaperDIY-Assembly-Kit_main_pictures_06.webp)](/uploads/_external/K159-PaperDIY-Assembly-Kit_main_pictures_06.webp)

*Controller board showing the FPC connectors, microSD slot, USB-C port and buttons. Image: M5Stack.*

Unlike many smaller e-paper modules that use SPI, PaperDIY drives the panel over an 8-bit parallel data bus. DB0 through DB7 connect to GPIO 6, 14, 7, 12, 9, 11, 8 and 10, respectively; additional GPIOs provide the panel clock and control signals. M5Stack's schematics document the MCU, display, power domains, microSD interface and expansion connectors.

The pin allocation matters when adding peripherals. GPIO 39, 38 and 40 are used for microSD SPI signals and also appear on the external SPI connector. Any device sharing those lines needs its own chip-select arrangement and coordinated access to the bus.

[![PaperDIY power states and architecture schematic](/uploads/_external/K159-B_PaperDIY_sche_01.webp)](/uploads/_external/K159-B_PaperDIY_sche_01.webp)

*Official schematic, sheet 1: functional blocks and power-state overview.*

[![PaperDIY eight-bit parallel e-paper interface schematic](/uploads/_external/K159-B_PaperDIY_sche_02.webp)](/uploads/_external/K159-B_PaperDIY_sche_02.webp)

*Schematic sheet 2: ESP32-S3 and the eight-bit e-paper interface.*

The power circuitry is split into separate domains. An M5PM1 power-management unit, together with a PY32L020F15U6 shown in the schematic, handles system power states. An LGS4056 manages battery charging, while an SY8089 supplies a switched 3.3 V rail alongside a separate always-on supply. The display's boost circuitry appears on its own schematic sheet.

Two control signals are particularly relevant during bring-up: M5PM1 output PYG2 controls `EPD_PWR`, and ESP32-S3 GPIO 46 controls the boost enable, `BST_EN`. If the panel fails to update, check both signals before assuming the flex cable or panel is faulty.

[![PaperDIY USB charging and power management schematic](/uploads/_external/K159-B_PaperDIY_sche_03.webp)](/uploads/_external/K159-B_PaperDIY_sche_03.webp)

*Schematic sheet 3: USB input, battery charging, power management and regulation.*

[![PaperDIY display power and microSD schematic](/uploads/_external/K159-B_PaperDIY_sche_04.webp)](/uploads/_external/K159-B_PaperDIY_sche_04.webp)

*Schematic sheet 4: display power, microSD and expansion connectors.*

M5Stack provides the ESP-IDF source for its factory test firmware, including checks for battery voltage, Wi-Fi scanning, microSD read/write access and button input. Arduino support is available through M5Unified, M5GFX and M5PM1, and M5Stack also publishes a UiFlow2 tutorial.

To enter firmware download mode, connect a USB-C data cable, hold the power button for approximately two seconds and release it when the red LED blinks. Running the factory test before developing a custom application helps verify the hardware, storage and power controls independently of application code.

M5Stack's official store listed the Assembly Kit (K159) at **US$25.00** and the Complete Kit (K159-B) at **US$29.90** on October 21, 2026, excluding shipping and applicable taxes. The Complete Kit's PLA enclosure measures 120 × 68.2 × 6.3 mm, and M5Stack provides 3D model files for enclosure modifications. The rear mounting points use M2 screws; the manufacturer specifies a **thread length of less than 3 mm** to avoid damaging the display.

[![PaperDIY Complete Kit rear mounting detail](/uploads/_external/K159-B_PaperDIY_Complete_Kit_main_pictures_08.webp)](/uploads/_external/K159-B_PaperDIY_Complete_Kit_main_pictures_08.webp)

*Rear of the Complete Kit enclosure with the mounting points. Image: M5Stack.*

**Hardware and software references:** [Assembly Kit documentation](https://docs.m5stack.com/en/core/PaperDIY_Assembly_Kit) · [Complete Kit documentation](https://docs.m5stack.com/en/core/PaperDIY_Complete_Kit) · [Full schematics (PDF)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche.pdf) · [ESP-IDF factory test source](https://github.com/m5stack/M5PaperDIY-UserDemo) · [Assembly Kit store listing](https://shop.m5stack.com/products/paperdiy-assembly-kit-esp32-s3) · [Complete Kit store listing](https://shop.m5stack.com/products/paperdiy-complete-kit-esp32-s3)

<!-- embeddednote-p0-20261106:start -->

## What we checked

| Claim | Where we looked | Result |
| --- | --- | --- |
| 4.7-inch, 960 x 540 grayscale panel | Product listing and the demo repository | Consistent across both |
| 8-bit parallel display interface | Published schematic pages for the K159 and K159-B kits | Confirmed on the schematic we mirrored |
| ESP32-S3 with an ESP-IDF demo that pins its components | `m5stack/M5PaperDIY-UserDemo` | Confirmed |
| Price around $25 | Retail listing at publication | A snapshot, not a current price |

We mirrored the four schematic pages for the complete kit into this site rather than hotlinking the vendor CDN, so the drawings stay readable if the listing changes. What we have not done is measure the panel: refresh timing, ghosting and the actual current draw of the board in each power state remain vendor figures and should be re-measured on the bench.

## Engineering check: memory size, power gating and first bring-up

The 960 × 540 display has **518,400 pixels**. A hypothetical 1-bit packed image is **64,800 bytes**; a hypothetical 4-bit indexed buffer is **259,200 bytes**. These are straightforward framebuffer-size calculations, **not** a statement that PaperDIY's shipping driver uses either format. Check the actual driver data path before deciding how many buffers can coexist with fonts, network stacks and image decoders.

For a low-duty-cycle dashboard, three different power states matter: the MCU in sleep, the display controller/PMIC with its power rails enabled, and the panel actively updating. E-paper image persistence does not mean the entire development board consumes zero power while idle. Measure board current in each state, including the battery measurement path, pull-ups, and any accessories. In an ESP32-S3 product, the power-management design can matter more to battery life than a small difference in framebuffer-copy speed.

A reproducible first-bring-up sequence is to flash the **manufacturer's matching factory demo**, verify display activity and SD/battery features if fitted, then record the exact ESP-IDF revision, board SKU, firmware commit and observed current in sleep and refresh. M5Stack's [PaperDIY demo repository](https://github.com/m5stack/M5PaperDIY-UserDemo) specifies an ESP-IDF build flow with pinned components. Preserve this baseline before changing drivers or display waveforms. The original article's listed prices refer to its publication date and should not be treated as current offers.

For pixel-format debugging, see our [RAW4 and palette test-vector guide](/en/articles/epaper-palette-raw4-packing-guide/); for refresh latency, see the [SPI vs. BUSY timing breakdown](/en/articles/epaper-refresh-timing-pipeline/).
<!-- embeddednote-p0-20261106:end -->
