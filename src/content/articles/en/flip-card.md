---
title: A Fluid-Simulation LED Badge Built Around the RP2350
description: Nick Johnson’s flip-card runs a FLIP-inspired fluid simulation on an RP2350 and a 21×22 LED array,
  with embedded Rust firmware and open KiCad files.
locale: en
translationKey: flip-card
pubDate: '2025-09-10'
category: open-source
tags:
- GitHub
- RP2350
- LED Matrix
- Embedded Rust
- FLIP
- Embassy
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/Nicholas-L-Johnson/flip-card
seoTitle: 'RP2350 Fluid-Simulation LED Badge: Open-Source flip-card'
seoDescription: Explore flip-card, an RP2350-powered 21×22 LED badge running a fluid simulation, with Rust/Embassy
  firmware, KiCad PCB files, and an animated demo.
---

A business card covered in a **21 × 22 LED matrix** is already a good conversation starter. Nick Johnson’s *flip-card* goes a step further: tilt the board, and the illuminated particles slosh around like liquid. The effect is produced by a fluid simulation running on a **Raspberry Pi RP2350**, rather than a canned animation.

Johnson wrote the firmware in **Rust**, using the **Embassy** embedded asynchronous framework. The simulation draws on the fluid-implicit particle (FLIP) approach. It is an interesting combination of numerical simulation, tightly packed PCB design, and real-time display control on a microcontroller.

## The fluid effect in motion

![Animated FLIP fluid simulation on the badge, 93-frame GIF](/uploads/flip-card/flip-card-01.gif)

![flip-card hardware and LED matrix close-up](/uploads/flip-card/flip-card-02.webp)

The code is on GitHub: [Nicholas-L-Johnson/flip-card](https://github.com/Nicholas-L-Johnson/flip-card/).

The repository is split into useful pieces. The **`kicad-pcb`** directory contains the board design, while **`fluid_sim_crate`** holds the simulation logic as a standalone Rust crate. The RP2350 implementation lives in **`flip-card_firmware`**. There is also a WebAssembly simulator under **`sim_display`**, used to debug the fluid behavior before running it on the hardware.

Johnson credits Matthias Müller’s fluid-simulation work and cites mitxela’s fluid pendant as another inspiration. For the rechargeable-battery design and board-edge USB-C connection, he drew on cnlohr’s tiny touch LCD project. Those details matter: fitting a dense LED array, a controller and a rechargeable power system onto a card-sized PCB is a sizeable part of the engineering challenge.

## Schematics and assembled boards

![Controller and power schematic for flip-card](/uploads/flip-card/flip-card-03.webp)

![LED matrix schematic for flip-card](/uploads/flip-card/flip-card-04.webp)

The assembled PCBs show how much of the board area is devoted to the LED array, with the controller and supporting circuitry packed into the space below.

![Assembled flip-card boards](/uploads/flip-card/flip-card-05.webp)

![Close-up of the flip-card PCB and LEDs](/uploads/flip-card/flip-card-02.webp)

![Reverse side of Nick Johnson’s flip-card business card](/uploads/flip-card/flip-card-06.webp)

The KiCad files, firmware and simulation sources are available in the repository. For anyone experimenting with the RP2350, embedded Rust or LED-matrix rendering, flip-card is a project worth opening in an editor rather than just watching on a screen.
