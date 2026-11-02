---
title: 'PocketMage: An ESP32-S3 PDA That Lets E-Paper and OLED Share the Work'
description: 'PocketMage pairs e-paper with a fast OLED in an ESP32-S3 clamshell PDA. Its latest open hardware files, PocketMageOS SDK and loadable ELF apps make it worth a closer look.'
locale: en
translationKey: pocketmage-pda-dual-display
pubDate: '2026-11-01'
category: open-source
tags:
  - PocketMage
  - ESP32-S3
  - E-Paper
  - OLED
  - Handheld Computing
  - Open Hardware
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/TalismanDesign/PocketMage_PDA
seoTitle: 'PocketMage PDA: ESP32-S3, E-Paper and an OLED Status Display'
seoDescription: 'PocketMage is an ESP32-S3 PDA with e-paper, OLED and a physical keyboard. Explore its latest KiCad hardware, PocketMageOS SDK and SD-card-loaded ELF apps.'
---

There is a reason most small e-paper projects avoid keyboards: a display that takes hundreds of milliseconds to update is a poor place to show every keystroke. PocketMage tackles that problem without asking the e-paper panel to do something it cannot. It gives the main display a narrow OLED companion, then puts both into a tiny clamshell computer powered by an ESP32-S3.

![PocketMage clamshell PDA with a monochrome e-paper main screen and a narrow OLED above its keyboard](/uploads/pocketmage-pda/pocketmage-cover.webp)

The result looks like a miniature laptop from another era, down to the keys and transparent enclosure. It does not run desktop Linux. PocketMageOS is a C++ application environment built with PlatformIO, and by **November 1, 2026** it had grown well beyond the original launcher, text editor and file manager. The repository now includes a standalone SDK, loadable ELF applications and editable hardware design files.

The project lives in the [PocketMage PDA repository](https://github.com/TalismanDesign/PocketMage_PDA), formerly `ashtf8/PocketMage_PDA`. The features discussed here were checked against the [November 1, 2026 commit](https://github.com/TalismanDesign/PocketMage_PDA/tree/f8b5c13fa14667dca36a54022d2cfe2217553ab5).

## Two screens, two jobs

The main display is a **3.1-inch, 320 × 240 monochrome SPI e-paper panel**, identified as GDEQ031T10. It is a good fit for text and other content that changes infrequently. The secondary display is a **256 × 32 monochrome SPI OLED**, based on the SSD1326 and listed as ER-OLED018-1W in the hardware notes. It sits just above the keyboard, where a fast-changing line of feedback is useful.

That division matters more than the individual display specifications. A cursor, an active menu or a line of typing feedback does not have to trigger a full update of the e-paper screen. The OLED can respond immediately while the e-paper panel holds the material worth reading. It is a practical workaround for one of the biggest usability problems in compact e-paper devices, rather than a claim of unusually fast e-paper refresh.

![PocketMage PDA from another angle, showing its clamshell hinge and compact keyboard](/uploads/pocketmage-pda/pocketmage-device.webp)

## What is on the boards?

PocketMage is built around an **ESP32-S3-WROOM-1** with 16 MB of flash, Wi-Fi and Bluetooth. Memory configuration now depends on the board revision: the current PlatformIO project targets an **N16R2 production board** with 2 MB of PSRAM and an **N16R8 beta board** whose 8 MB PSRAM is disabled in that build. That distinction matters if you are planning to run memory-hungry applications. A **TCA8418 I²C keypad controller** scans the physical keyboard, while an **MPR121** handles capacitive input. The hardware also includes microSD, a **PCF8563T RTC**, a piezo buzzer, USB-C and a **1,200 mAh LiPo battery**.

Battery capacity is a specification, not a runtime claim. How long a charge lasts depends on how often the e-paper is updated, what the OLED is doing, and whether the radios are running. The active production and beta hardware builds also differ, so component substitutions should be based on the matching PCB revision and BOM rather than on an older photograph.

The expansion connector breaks out 3.3 V, ground, I²C, SPI and several GPIOs. Two pins can be assigned to UART TX and RX using solder jumpers. It is the kind of detail that makes this more interesting to an embedded developer than a fixed-purpose electronic notebook. There is room for sensors and small peripherals without redesigning the entire handheld.

The original article includes both keyboard and display-board schematics. In the current repository, **editable KiCad schematics and PCB layouts are available under `Resources/PCB`**, with production exports for several revisions. STEP models for the enclosure are under `Resources/CAD`. The screenshots below show the circuit split, but use the actual source files for pinouts, footprints and fabrication work.

![PocketMage keyboard schematic overview with keypad-matrix circuit and controller connections](/uploads/pocketmage-pda/pocketmage-keyboard-schematic.webp)

*Keyboard circuitry, including the keypad interface.*

![PocketMage display and processor schematic overview showing controller and peripheral connections](/uploads/pocketmage-pda/pocketmage-display-schematic.webp)

*Display-board and processor circuitry.*

## Software that matches the hardware

PocketMageOS still uses **C++ and PlatformIO**, but its software has moved past the bare-bones interface shown in early project videos. Alongside the TXT editor and FileWiz, the current README lists calendar, tasks, journal, dictionary, settings, USB file transfer, COMM mesh chat, a scripting terminal and SSH. These are project-provided features, not claims that every feature has been independently tested or works identically on every board revision.

The home menu also accepts typed commands, including `roll dN` for a die with *N* sides, setting the time and date, and opening files by name. For developers, the repository provided a blank application template and a walkthrough for creating a PocketMage app. That is a promising starting point for anyone interested in the embedded UI and input code rather than merely the finished enclosure.

The bigger development change is how third-party apps run. **Native apps** compile into the firmware, while **ELF apps** can be built with the [PocketMage SDK](https://talismandesign.github.io/PocketMage_SDK/docs/) and loaded from microSD at runtime. PocketMageOS dispatches input and drawing to the active app through its own library layer rather than having every app talk directly to display pins. There is still unfinished work: timers, an e-book reader, Wi-Fi notes/calendar synchronization, Bluetooth keyboard support and a LoRa/Meshtastic add-on remain on the planned-feature list. The README now also links to [Crowd Supply](https://pocketmage.org/back) for builders who would rather get a kit than source the parts themselves.

The licensing picture has also changed. The repository now carries **Apache-2.0**, replacing the **CC BY-NC-SA 4.0** terms found in the November 2025 revision. If you plan to reuse a board design or ship a derivative, check the license and third-party assets in the exact revision you are using; the code license does not automatically grant rights to every photo, name or external asset.

PocketMage's most useful idea is also its simplest. Instead of spending effort trying to make e-paper handle a fast interface, it moves the fast interface onto a tiny OLED. The rest of the hardware—the keyboard, storage, RTC and accessible expansion pins—turns that display decision into something you can actually type on.

References: [PocketMage repository](https://github.com/TalismanDesign/PocketMage_PDA) · [November 1, 2026 source revision](https://github.com/TalismanDesign/PocketMage_PDA/tree/f8b5c13fa14667dca36a54022d2cfe2217553ab5) · [KiCad and enclosure files](https://github.com/TalismanDesign/PocketMage_PDA/tree/main/Resources) · [PocketMageOS architecture](https://talismandesign.github.io/PocketMage_PDA/docs/development/architecture) · [App development walkthrough](https://www.youtube.com/watch?v=3Ytc-3-BbMM).
