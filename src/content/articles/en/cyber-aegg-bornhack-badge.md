---
title: 'Cyber Ægg: An E-Paper Conference Badge That Lives On After BornHack'
description: Cyber Ægg is a BornHack 2026 badge with nRF52840, tricolor e-paper, SX1262 LoRa, NFC tag capabilities and MeshCore networking.
locale: en
translationKey: cyber-aegg-bornhack-badge
pubDate: '2026-08-04'
category: open-source
tags:
- nRF52840
- E-Paper
- LoRa
- MeshCore
draft: false
seoTitle: 'Cyber Ægg: BornHack E-Paper Badge and MeshCore'
seoDescription: Cyber Ægg is a BornHack 2026 badge with nRF52840, tricolor e-paper, SX1262 LoRa, NFC tag capabilities and MeshCore networking.
---

BornHack 2026's electronic badge is called Cyber Ægg, and its hardware files are hosted on Codeberg.

Unlike many conference badges that are put away when an event ends, Cyber Ægg is intended to remain useful as a desk clock, calendar, or MeshCore node. That's also what makes it an interesting design beyond its unusual appearance.

![cyber aegg bornhack badge — figure 1](/uploads/cyber-aegg-bornhack-badge/cyber-aegg-bornhack-badge-01.webp)

The PCB has the outline of half an egg and fits into a 3D-printed case, giving it something of an electronic-pet aesthetic. During the event it can run a Tamagotchi-style virtual pet, display the schedule, and participate in RFID-token games. Back at home, it can stand on a desk as a low-power e-paper terminal.

![cyber aegg bornhack badge — figure 2](/uploads/cyber-aegg-bornhack-badge/cyber-aegg-bornhack-badge-02.webp)

**Badge.Team documentation:** https://badge.team/docs/badges/bornhack-2026/  
**Hardware (KiCad, including MCU, NFC, and LoRa schematics):** https://codeberg.org/Ranzbak/bornhack2026-hardware  
**Firmware (Rust / Embassy):** https://codeberg.org/Ranzbak/bornhack-firmware-2026

The main controller is a Nordic nRF52840 with an Arm Cortex-M4F core, Bluetooth Low Energy, and NFC tag hardware. There's no need for a separate Bluetooth chip. NFC uses the nRF52840's tag function and a PCB antenna coil that the documentation describes as roughly 2.8 µH, tuned with capacitors to 13.56 MHz. One limitation is important: the nRF52840 can act as an NFC tag here, not an NFC reader.

The display is a 1.54-inch, 152 × 152 three-color e-paper panel (black, white, and red) with an SSD1675/SSD1675B controller over SPI. E-paper is particularly suitable outdoors because it remains readable in sunlight and holds its image without continuous display power. The project's stated battery-life goal was to last the full week of the BornHack camp on a single charge.

For longer-range communication the board adds a Semtech SX1262 LoRa transceiver over SPI. Its matching network and balun draw on Semtech application notes, while the antenna design references TI material. The software runs MeshCore, making the badge a node on the event's mesh network rather than just a standalone gadget.

![cyber aegg bornhack badge — figure 3](/uploads/cyber-aegg-bornhack-badge/cyber-aegg-bornhack-badge-03.webp)

## Main components

| Function | Hardware | Interface |
| --- | --- | --- |
| MCU | Nordic nRF52840 | — |
| Display | 1.54-inch tricolor e-paper, SSD1675/SSD1675B | SPI |
| LoRa | Semtech SX1262 | SPI |
| Bluetooth | Integrated nRF52840 BLE | — |
| NFC | nRF52840 NFC tag PHY + PCB coil | — |
| Inputs | Five-way joystick, Execute and Cancel buttons | GPIO |
| Feedback | RGB LED, piezo buzzer | GPIO / PWM |
| Power | Lithium battery, USB-C, slide switch | — |
| Expansion | Qwiic / I²C | I²C |

The KiCad repository includes separate schematics for the controller, LoRa, display, power, NFC, and Qwiic interface.

There is a notable hardware warning in the official documentation: **3.3 V and GND are swapped on the Qwiic connector.** A standard Qwiic cable therefore cannot be used directly with peripherals. A corrected cable needs to cross the two power conductors at one end. The documentation also notes that some NFC, LoRa, and Bluetooth RF circuits retain U.FL/I-PEX connectors for debugging and antenna tuning, and that the PCB antennas have not yet been fully characterized. This is not a design to send directly to production without additional RF work.

The real attraction is the idea of making an event souvenir into a device that remains useful. The nRF52840 handles BLE, NFC, and control; the SX1262 handles long-range mesh connectivity; e-paper keeps the interface visible; the joystick and buttons provide local control; and USB-C and the battery cover charging, data, and untethered operation. None of those parts is remarkable alone, but the combination is thoughtfully put together.
