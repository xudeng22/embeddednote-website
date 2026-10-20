---
title: 'NumWorks: A Seriously Cool Graphing Calculator, Right Down to the PCB'
description: 'A closer look at NumWorks: its STM32F730 hardware, LCD interface, Epsilon firmware, published schematics,
  and the limits of firmware openness.'
locale: en
translationKey: numworks-graphing-calculator
pubDate: '2026-10-20'
category: open-source
draft: false
tags:
- NumWorks
- STM32
- Graphing Calculator
- Embedded Systems
- Open Hardware
seoTitle: 'NumWorks: A Cool Graphing Calculator, Right Down to the PCB'
seoDescription: Explore NumWorks from its STM32F730 and LCD interface to the Epsilon math engine, schematics, PCB
  design, and current firmware restrictions.
---

NumWorks looks nothing like the traditional graphing calculators that have dominated classrooms for decades. Its white enclosure, rounded keys and app-style home screen are much closer to a modern consumer device than the familiar black plastic calculators from Texas Instruments and Casio. But for embedded developers, the design is only the beginning. NumWorks has published detailed engineering material covering the MCU, memory, LCD interface, power supply and PCB layout, along with source code for its Epsilon operating system.

The company was founded in France in 2015 and set out to make graphing calculators easier to use and easier to understand. The result is a handheld calculator with a 320 × 240 IPS display, a 140 PPI pixel density, 262,144 supported colors and a 1,450 mAh rechargeable lithium-polymer battery. NumWorks quotes around 20 hours of use under its specified classroom workload, rather than 20 hours with the display continuously at full brightness.

![NumWorks graphing calculator beside The Board desktop math workspace](/uploads/numworks/numworks-cover.webp)

![NumWorks handheld graphing calculator with its white enclosure and rounded buttons](/uploads/numworks/numworks-01.webp)

## What is behind the clean exterior?

The calculator's interface uses a grid of clearly labeled apps instead of forcing users through deep menu trees. That makes it approachable for students, but the more interesting material for engineers is on the [NumWorks engineering website](https://www.numworks.com/engineering/). The company publishes schematics, explanations of individual circuits, component data sheets, PCB layer views and mechanical-design notes.

![NumWorks The Board software alongside the handheld calculator](/uploads/numworks/numworks-02.webp)

In the hardware design documented on NumWorks' engineering pages, the main processor is an **STMicroelectronics STM32F730V8T6** in a 100-pin LQFP package. Its Cortex-M7 core runs at up to **216 MHz**, with **256 KB of on-chip SRAM**. Those figures are useful when studying the published reference design; they should not be taken as a guarantee that every production revision uses an identical board.

Nonvolatile storage comes from an **Adesto AT25SF641**, a 64-Mbit (8 MB) NOR flash device connected over Quad-SPI at up to 104 MHz. That external storage holds software and persistent data, while the MCU handles the user interface, numerical calculations and peripheral control. For a calculator, keeping the external-memory interface, CPU and display well matched matters far more than chasing desktop-class processing speed.

## The schematics are worth reading

The first schematic sheet centers on the STM32F730 and its support circuitry. It covers decoupling, reset, boot configuration and the clocking needed for USB. NumWorks also documents the details of entering DFU mode, so the design can be studied from the PCB connections rather than inferred from a block diagram.

![STM32F730 microcontroller, decoupling, reset and boot circuitry](/uploads/numworks/numworks-03.png)

The next sheet shows the matrix keyboard and LCD connections. The keyboard uses a conventional row-and-column scan arrangement, which keeps GPIO usage manageable but also brings familiar key-ghosting constraints. The **ST7789V** display controller is connected through a **16-bit parallel bus** and has its own display RAM. NumWorks quotes a minimum bus write cycle of 66 ns, equivalent to a theoretical ceiling of roughly 200 frame writes per second. That is a bus-timing calculation, **not a measured 200 fps application refresh rate**.

![Keypad matrix and 16-bit parallel LCD interface](/uploads/numworks/numworks-04.png)

The peripheral sheet includes the external flash, USB protection, oscillator and RGB status indicator. A **USBLC6-2SC6** protects the USB lines against electrostatic discharge. The status light is a single RGB LED package with red, green and blue channels that shine through a thinner portion of the enclosure, providing an indicator without an obvious window in the plastic.

![External flash, USB ESD protection, oscillator and RGB indicator circuits](/uploads/numworks/numworks-05.png)

Battery charging is handled by an **RT9526A** using a constant-current/constant-voltage charging profile. An **RT9078 low-dropout regulator** supplies the 2.8 V logic rail from a 3.0–5.5 V input. The power schematics also cover battery-voltage sensing and the charge-pump circuitry used for the LCD backlight. These are small, practical choices, but together they explain how the design balances thickness, power draw and usable battery life.

![Battery measurement, charger, LCD backlight supply and logic regulator schematics](/uploads/numworks/numworks-06.png)

NumWorks also makes the PCB layers available for inspection. The illustrated board is a two-layer design, about 0.8 mm thick, with fine traces running between the processor, display interface and other components. The layout is a useful example of the compromises in a compact consumer product: the board must fit beneath a full keyboard while accommodating the LCD, battery, USB connector and power circuitry.

![NumWorks two-layer PCB routing and top-layer layout](/uploads/numworks/numworks-07.png)

## Epsilon: a calculator OS built for a constrained MCU

The firmware is another substantial part of the project. **Epsilon** is written primarily in C++ and organized around a set of distinct software layers: **Ion** abstracts the hardware; **Kandinsky** provides graphics primitives; **Escher** handles UI widgets; **Poincaré** implements mathematical operations; and the application layer brings those capabilities together for graphing, calculation, statistics and other tasks.

With only 256 KB of SRAM in the documented STM32F730 design, memory management has to be deliberate. The project has discussed a constrained stack, static allocation and a garbage-collected object pool rather than unrestricted conventional heap allocation. For readers familiar with firmware work, those design decisions are more revealing than the calculator's appearance: they show how a reasonably rich graphical interface can run on an MCU without the resources of a desktop OS.

Epsilon can also be built for desktop simulation, making it possible to inspect its architecture, experiment with the math engine and debug application code without first buying a calculator. The official [Epsilon repository](https://github.com/numworks/epsilon) includes build documentation and a simulator workflow.

## The Board, Python and community projects

NumWorks has also expanded beyond the handheld device. Its **The Board** workspace brings graphs, tables and equation-solving tools together on a larger computer screen, which is useful for teaching or comparing multiple representations of a function side by side. That desktop experience is shown alongside the calculator in the accompanying image.

![The Board workspace showing equations, a graph and a table of values](/uploads/numworks/numworks-08.jpeg)

On the handheld side, Epsilon includes math applications intended for school use as well as Python programming support. NumWorks offers an [online calculator simulator](https://www.numworks.com/simulator/) for anyone who wants to try the interface. Community firmware projects such as **Omega** and **Upsilon** have also explored modifications and added functionality on supported calculator generations.

There is an important distinction between **published source code** and software that can be freely modified and redistributed. In 2021, NumWorks tightened its firmware licensing and introduced security restrictions to protect exam mode. Unofficial software can be subject to hardware restrictions, and the official firmware is not freely redistributable under a conventional open-source license. The exact modification and installation options depend on the hardware and firmware generation. NumWorks continues to publish code and supports custom applications, but calling the current product "fully open-source hardware and software" without qualification would be misleading.

This is still an unusually accessible platform for studying a commercially manufactured calculator. You can follow the design from the STM32F730 pinout through the display timing and power rails, and then into the graphics and math libraries that run on top. The lack of a touchscreen is a deliberate trade-off in favor of a physical keypad, and 216 MHz is modest next to a modern application processor. For the work a graphing calculator needs to do, however, its carefully chosen hardware and well-documented software architecture are the bigger story.

**Project resources:** [NumWorks](https://www.numworks.com/) · [Engineering documentation](https://www.numworks.com/engineering/) · [Epsilon source](https://github.com/numworks/epsilon) · [Official software policy](https://www.numworks.com/blog/secure-software-for-exams/)
