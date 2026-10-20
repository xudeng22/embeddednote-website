---
title: 'NumWorks: A Surprisingly Cool Graphing Calculator, Inside and Out'
description: 'Inside the NumWorks graphing calculator: STM32F730 reference hardware, LCD timing, PCB design, Epsilon
  software, and firmware licensing.'
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
seoTitle: 'NumWorks Graphing Calculator: STM32 Hardware and Epsilon OS'
seoDescription: Explore NumWorks hardware and Epsilon software, including STM32F730 schematics, LCD interface,
  PCB design, and firmware licensing limits.
---

Graphing calculators have long been associated with dense menus and crowded keypads. NumWorks takes a different approach: a white enclosure, rounded keys, and an app-based home screen. For embedded developers, though, the hardware documentation is just as interesting as the industrial design. NumWorks publishes schematics, component details, and PCB information alongside source code for its Epsilon calculator operating system.

Founded in France in **2016**, NumWorks introduced its first graphing calculator in 2017. The published specifications list a **320 × 240 IPS LCD** (140 PPI, 262,144 colors) and a **1,450 mAh lithium-polymer battery**. NumWorks rates battery life at approximately **20 hours** under a classroom-use profile that alternates between full brightness and a dimmed display—not 20 hours at maximum brightness.

![NumWorks graphing calculator beside The Board desktop math workspace](/uploads/numworks/numworks-cover.webp)

![NumWorks handheld graphing calculator with its white enclosure and rounded buttons](/uploads/numworks/numworks-01.webp)

## Inside the STM32F730-based design

The app grid makes functions easier to find, but the [NumWorks engineering documentation](https://www.numworks.com/engineering/) is where the hardware gets interesting. It includes circuit descriptions, schematics, component datasheets, PCB layer views, and mechanical-design information.

![NumWorks The Board software alongside the handheld calculator](/uploads/numworks/numworks-02.webp)

In the hardware design documented on NumWorks' engineering pages, the main processor is an **STMicroelectronics STM32F730V8T6** in a 100-pin LQFP package. Its Cortex-M7 core runs at up to **216 MHz**, with **256 KB of on-chip SRAM**. Those figures are useful when studying the published reference design; they should not be taken as a guarantee that every production revision uses an identical board.

Nonvolatile storage comes from an **Adesto AT25SF641**, a 64-Mbit (8 MB) NOR flash device connected over Quad-SPI at up to 104 MHz. That external storage holds software and persistent data, while the MCU handles the user interface, numerical calculations and peripheral control. The Quad-SPI interface gives the firmware access to 8 MB of nonvolatile storage without requiring a wide external memory bus.

## A closer look at the schematics

The first schematic sheet centers on the STM32F730 and its support circuitry. It covers decoupling, reset, boot configuration and the clocking needed for USB. The documentation also covers the boot and reset circuitry used when working with the board at firmware level.

![STM32F730 microcontroller, decoupling, reset and boot circuitry](/uploads/numworks/numworks-03.png)

The next sheet shows the matrix keyboard and LCD connections. The matrix keyboard reduces the number of GPIO pins required, although the schematic notes an ambiguity when multiple keys in the same group are pressed. The **ST7789V** display controller is connected through a **16-bit parallel bus** and has its own display RAM. NumWorks quotes a minimum bus write cycle of 66 ns, equivalent to a theoretical ceiling of roughly 200 frame writes per second. That is a bus-timing calculation, **not a measured 200 fps application refresh rate**.

![Keypad matrix and 16-bit parallel LCD interface](/uploads/numworks/numworks-04.png)

The peripheral sheet includes the external flash, USB protection, oscillator and RGB status indicator. A **USBLC6-2SC6** protects the USB lines against electrostatic discharge. A glow-through RGB indicator uses red, green and blue channels behind the enclosure.

![External flash, USB ESD protection, oscillator and RGB indicator circuits](/uploads/numworks/numworks-05.png)

Battery charging is handled by an **RT9526A** using a constant-current/constant-voltage charging profile. An **RT9078 low-dropout regulator** supplies the 2.8 V logic rail from a 3.0–5.5 V input. The power schematics also cover battery-voltage sensing and the charge-pump circuitry used for the LCD backlight. The schematics show how charging, backlight power, and the 2.8 V logic rail are supplied from the same battery.

![Battery measurement, charger, LCD backlight supply and logic regulator schematics](/uploads/numworks/numworks-06.png)

NumWorks also makes the PCB layers available for inspection. The illustrated board is a two-layer design, about 0.8 mm thick, with fine traces running between the processor, display interface and other components. The routing has to fit around the full keypad, display connections, battery interface, USB connector, and power circuitry.

![NumWorks two-layer PCB routing and top-layer layout](/uploads/numworks/numworks-07.png)

## Epsilon: a five-layer OS for a memory-constrained MCU

**Epsilon** is written primarily in C++ and has five main layers: **Ion** abstracts the hardware; **Kandinsky** provides graphics primitives; **Escher** handles UI widgets; **Poincaré** implements mathematical operations; and the application layer brings those capabilities together for graphing, calculation, statistics and other tasks.

The documented STM32F730 platform has just **256 KB of SRAM**. NumWorks reserved **32 KB for the stack** and avoided general-purpose `malloc`/`free`, using static allocation and a pool of relocatable, garbage-collected nodes to handle mathematical expressions. That allocation strategy makes the memory constraints visible in the source code.

Epsilon can also be built for desktop simulation, making it possible to inspect its architecture, experiment with the math engine and debug application code without first buying a calculator. The official [Epsilon repository](https://github.com/numworks/epsilon) includes build documentation and a simulator workflow.

## The Board, Python, and third-party firmware

Separate from the Epsilon calculator simulator, **The Board** is NumWorks' large-screen math workspace. It lets students and teachers work with graphs, tables, and equations side by side in a browser. The accompanying image shows The Board next to the handheld calculator.

![The Board workspace showing equations, a graph and a table of values](/uploads/numworks/numworks-08.jpeg)

On the handheld side, Epsilon includes math applications intended for school use as well as Python programming support. NumWorks offers an [online calculator simulator](https://www.numworks.com/simulator/) for anyone who wants to try the interface. Community firmware projects have taken Epsilon in other directions. Development of **Omega** is on hold; **Upsilon**, a fork of Omega, continues that work for supported calculator models.

One caveat matters for anyone planning to modify the firmware: **source-available is not the same as open source**. NumWorks changed its software terms in 2021 and restricted access to some hardware features when unofficial firmware is installed, partly to protect exam mode. Under its current end-user license, software modification is permitted for personal, non-commercial use, while redistribution is restricted. Epsilon code remains public and the platform supports external applications, but developers should check the terms and installation options for their particular hardware and firmware version.

For embedded developers, the published STM32F730 reference design offers plenty to inspect: a 16-bit LCD interface, matrix keyboard, Quad-SPI flash, battery management, and a carefully budgeted software stack. The Epsilon source provides a view of the implementation, although modifying and distributing firmware remains subject to NumWorks' licensing and device restrictions.

**Project resources:** [NumWorks](https://www.numworks.com/) · [Engineering documentation](https://www.numworks.com/engineering/) · [Epsilon source](https://github.com/numworks/epsilon) · [Software license](https://www.numworks.com/legal/end-user-license-agreement/)
