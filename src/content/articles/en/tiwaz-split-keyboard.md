---
title: 'Tiwaz: Two Joysticks, Two Halves, One Open-Source Keyboard'
description: 'A look inside the Tiwaz split keyboard: STM32F401, swappable thumb joysticks, QMK/Vial firmware, RGB backlighting and gasket-mounted hardware.'
locale: en
translationKey: tiwaz-split-keyboard
pubDate: '2026-10-21'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/tstrube/Tiwaz
tags:
- Tiwaz
- Split Keyboard
- STM32F401
- QMK
- Vial
- Open Source Hardware
- Joystick
seoTitle: 'Tiwaz Split Keyboard: Dual Joysticks, STM32 and QMK'
seoDescription: Tiwaz combines two thumb joysticks with a fully configurable split keyboard. Explore its STM32F401 PCB, QMK/Vial firmware and gasket-mounted design.
---

Custom mechanical keyboards have no shortage of switch choices, layouts and gasket-mount experiments. Timo Strube's Tiwaz takes a different route: it puts a thumb joystick on each half of a split keyboard.

Strube, a software and electronics prototype developer, has published the PCB designs, firmware and assembly documentation on GitHub. The hardware is released under GPLv3, while the QMK-based firmware uses GPLv2. The enclosure can be 3D-printed. Tiwaz also has a Crowd Supply page, although the campaign is still listed as **Coming Soon** rather than open for pledges.

[GitHub repository and build files](https://github.com/tstrube/Tiwaz) · [Crowd Supply project page](https://www.crowdsupply.com/ts-consulting/tiwaz)

Each half works on its own as a one-handed gaming keypad, macro pad or programmable controller. Connect them with a 3.5 mm TRS cable and they form a split keyboard. That flexibility is particularly useful for gamers who use a mouse with their left hand: they can use either half without being tied to a conventional right-handed keypad layout.

The later hardware revision uses an **STM32F401RET6**, a Cortex-M4 microcontroller running at up to 84 MHz with 512 KB of flash. Each half has **38 MX-compatible hot-swap sockets**, six additional buttons normally mapped to media controls, and WS2812 RGB lighting for every switch and auxiliary button. USB-C provides the host connection.

![Tiwaz open-source split gaming keyboard with two orange thumb joysticks and blue RGB backlight](/uploads/tiwaz/tiwaz-cover.webp)

*Tiwaz connects its two halves over a 3.5 mm TRS cable.*

![Close-up of one Tiwaz keyboard half and joystick](/uploads/tiwaz/tiwaz-02.jpeg)

*The left half, with its thumb joystick at the lower right.*

![Tiwaz 3D printed keyboard case with lighting off](/uploads/tiwaz/tiwaz-03.jpeg)

*The black 3D-printed case with RGB lighting switched off.*

The joysticks are what set Tiwaz apart. There are two Alps Alpine options: the **RKJX21224001**, a tilting stick with a center-push switch, and the **RKJXU1210006**, a low-profile sliding stick similar to the one used in the PSP-3000. The latter has **no center-push switch**. Both use FPC ribbon connections, and the PCB connectors are positioned so that either stick can sit in the same location. Swapping between them involves changing the matching enclosure insert rather than redesigning the board.

The firmware supports three input modes, switched with **Fn plus the lowest auxiliary key**. Digital mode (blue indicator) produces direction-button input; analog mode (yellow) exposes gamepad axes; mouse mode (red) controls the pointer. With the RKJX21224001, pressing the stick acts as a mouse click, with firmware handling drag and right-click gestures. Mouse mode is not supported with the PSP-style joystick. The PCB also breaks out the joystick signals to solder pads marked **3V3, B, X, Y and GND**, which makes it easier to experiment with a different controller.

![Two Alps Alpine analog joysticks for the Tiwaz keyboard](/uploads/tiwaz/tiwaz-04.png)

*Two joystick options: RKJX21224001 (left) and the PSP-style RKJXU1210006 (right).*

![Tiwaz PCB FPC joystick connectors and GPIO breakouts](/uploads/tiwaz/tiwaz-05.jpeg)

*FPC connectors and joystick breakouts for 3V3, button, X/Y axes and ground.*

Earlier prototypes ran on the RP2040. Strube found that the keyboard sometimes initialized too late during a PC's initial boot, making it unreliable for entering BIOS or UEFI setup. Switching to the STM32F401 fixed that behavior in his tests. Some of the photographs in the project documentation still show the older RP2040 revision, so they should not be mistaken for the latest schematic.

The TRS cable carries both data and power between halves, and only one side normally needs a USB connection to the computer. Strube added an ideal-diode arrangement to limit backfeeding if both halves are accidentally connected over USB, plus a resettable fuse for the RGB LED load. The design also includes ESD protection on the USB and interconnect lines. These are worthwhile details to study if you're designing a DIY USB HID device rather than just assembling a keyboard.

![Tiwaz keyboard PCB top side with hot swap switch holes](/uploads/tiwaz/tiwaz-06.jpeg)

*PCB front, with 38 MX-compatible hot-swap positions and six auxiliary buttons.*

![Earlier RP2040 revision of the Tiwaz split keyboard PCB](/uploads/tiwaz/tiwaz-07.jpeg)

*An earlier PCB revision using the RP2040; the project subsequently moved to the STM32F401.*

![Tiwaz keyboard PCB top layer routing](/uploads/tiwaz/tiwaz-08.png)

*Top-layer PCB routing.*

![Tiwaz keyboard PCB bottom layer routing](/uploads/tiwaz/tiwaz-09.png)

*Bottom-layer PCB routing.*

Mechanically, Tiwaz uses a gasket-mounted switch plate with damping material between the plate and PCB, and again between the PCB and enclosure. The layered construction is intended to keep the typing feel from becoming too rigid and to reduce case vibration.

The case is 3D-printable, but Strube also designed its geometry with CNC machining in mind: no sharp internal corners, straightforward chamfers and tight-fitting interfaces. Print accuracy matters around the gaskets and joystick inserts. Keycaps are another practical constraint. A backlit, ortholinear layout made entirely of 1u keys doesn't leave many off-the-shelf options, so the builder sourced custom backlit keycaps.

![Tiwaz mechanical keyboard gasket and PCB exploded assembly](/uploads/tiwaz/tiwaz-10.png)

*Exploded assembly showing the switch plate, gasket layers, PCB and enclosure.*

![Tiwaz split keyboard components before assembly](/uploads/tiwaz/tiwaz-11.jpeg)

*Components for one keyboard half, laid out before assembly.*

![Tiwaz keyboard mechanical 3D CAD render](/uploads/tiwaz/tiwaz-12.png)

*3D rendering of one keyboard half and its joystick.*

Tiwaz runs **QMK**, with a working **Vial** firmware branch for remapping keys and layers without recompiling and reflashing every time. The upstream QMK pull request was still pending in the project documentation, so users should start with the linked project branches rather than assume it is already included in a standard QMK release. There is one quirk worth preserving: joystick-mode indicator colors are hardcoded in the firmware, and the README explicitly advises against changing the relevant key mapping.

It's not a conventional daily-driver layout. With 38 keys per half, users coming from a full-size keyboard will need to get comfortable with layers and remapping. The sliding PSP-style stick also lacks mouse-mode support, and the enclosure demands reasonably accurate printing. But for an embedded developer, the interesting part is easy to see: Tiwaz combines keyboard-matrix scanning, analog joystick inputs, USB HID, RGB control and a repairable mechanical design in one build. The publicly available PCB and firmware files make those choices inspectable—not just configurable.

Sources and images: [Tiwaz project by Timo Strube](https://github.com/tstrube/Tiwaz); [Crowd Supply](https://www.crowdsupply.com/ts-consulting/tiwaz). Joystick specifications: [RKJX21224001](https://tech.alpsalpine.com/e/products/detail/RKJX21224001/) and [RKJXU1210006](https://tech.alpsalpine.com/e/products/detail/RKJXU1210006/).
