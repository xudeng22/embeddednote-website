---
locale: en
translationKey: x-track-gps-bike-computer
pubDate: '2026-01-15'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/FASTSHIFT/X-TRACK
title: 'X-TRACK: An Open-Source GPS Bike Computer with Offline Maps and GPX Logging'
description: X-TRACK is an AT32F435-based cycling computer with offline map tiles, GNSS positioning, GPX ride logs and an LVGL desktop simulator.
tags:
- X-TRACK
- AT32F435
- GPS
- GNSS
- LVGL
- GPX
- Offline Maps
- Open Source
seoTitle: 'X-TRACK: Open-Source GPS Bike Computer with Offline Maps'
seoDescription: 'Explore X-TRACK: AT32F435 hardware, 1.54-inch TFT, ATGM336H GNSS, LVGL v8, GPX ride logging, offline tile maps and a PC simulator.'
---

Building a GPS cycling computer is one thing. Releasing the schematics, firmware, offline-map pipeline and desktop UI simulator is another. **X-TRACK**, from FASTSHIFT/VIFEXTech, does both. The small handlebar-mounted unit shows speed, distance, time, heading and position over a cached map, records a live track and exports it as a standard **GPX** file. Its source history goes back to 2021, with the hardware and software still available for people who want to study or reproduce it.

The code and design files are in [FASTSHIFT/X-TRACK on GitHub](https://github.com/FASTSHIFT/X-TRACK).

![X-TRACK open-source GPS bike computer mounted on a bicycle handlebar](/uploads/x-track/x-track-cover.webp)

*X-TRACK's 1.54-inch display combines an offline map with basic ride information.*

The original hardware uses an **Artery AT32F435CGU7**, rated at up to 288 MHz with **512 KB of RAM and 1 MB of flash**, paired with a **1.54-inch 240 × 240 ST7789 IPS display** over SPI. GNSS data comes from an **ATGM336H**, which supports GPS, BeiDou, GLONASS, Galileo and other constellations. The unit uses this information for position, ground speed and heading, and can discipline the MCU's internal RTC. A microSD card stores map tiles and ride logs, while a rotary encoder handles menu input. The published parts list also includes an LSM6DSM accelerometer, an LIS3MDL magnetometer, a **700 mAh Li-ion battery**, LP5907-3.3 regulator and MCP73831 charger.

![X-TRACK hardware schematic overview](/uploads/x-track/x-track-02.webp)

![X-TRACK power and peripheral schematics](/uploads/x-track/x-track-03.webp)

*Two schematic sheets included in the source article. Consult the latest repository design files before wiring or ordering PCBs.*

X-TRACK's map is **offline**. It does not fetch road imagery as you ride. Instead, you prepare tile data on the SD card; the firmware selects the tiles around the GPS fix and renders them with **LVGL v8**. The documented newer layout uses paths of the form `/MAP/z/x/y.bin`, with separate handling for WGS84 and GCJ-02 coordinates. The map assets must match the expected tile format and coordinate system. Simply copying an arbitrary PNG into the root directory will not produce a working map.

You can zoom the map and display the current position and recorded track. The ride pages show speed, distance, elapsed time, estimated calories, altitude and heading. GPX logging makes the data useful outside the device: copy the files to a PC and open them in tools such as GPXSee. Settings, including the last known position, timezone and map location, are saved in a `SystemSave.json` file on the card.

![Animated X-TRACK startup screen](/uploads/x-track/x-track-04.gif)

![Animated X-TRACK speed display demonstration](/uploads/x-track/x-track-05.gif)

*The original startup and speed demonstrations. The high-speed test is not representative of bicycle riding.*

![X-TRACK historical GPX track plotted on a desktop map](/uploads/x-track/x-track-06.webp)

*A recorded GPX track viewed on a desktop application.*

The README quotes **roughly four hours of continuous operation with the display on**. Treat that as the project's reference figure, not an independent battery-life measurement; screen brightness, GNSS reception and cell condition all matter. The hardware notes also contain several build-critical details. Use **0.8 mm or 1.0 mm PCB thickness**, check the unusual orientation of diode **D2**, and follow the guidance to omit **D4** to avoid powering up while charging. The recommended GNSS module is the ATGM336H, and its antenna must be kept clear of the adjacent supercapacitor. The documentation says the LSM6DSM and LIS3MDL can be left unpopulated in builds that do not need them.

The desktop simulator is another reason the repository is worth exploring. Firmware builds use **Keil MDK** and the matching Artery device pack, while a Visual Studio project runs the **LVGL UI in Release x86** on a PC. This lets you work on screen layouts and data flow without a fully assembled device. The software is organized around a page-lifecycle manager (`PageManager`) and a publish/subscribe data layer (`DataCenter`), alongside GPS parsing, GPX logging and map-tile handling.

X-TRACK is published under the **MIT License**. The [main repository](https://github.com/FASTSHIFT/X-TRACK), [hardware notes](https://github.com/FASTSHIFT/X-TRACK/tree/main/Hardware) and [build documentation](https://github.com/FASTSHIFT/X-TRACK/tree/main/Software) are the places to start. The author also links to [an original demonstration](https://www.bilibili.com/video/BV1GB4y1K7VV) and a [second-generation demonstration](https://www.bilibili.com/video/BV1aS421X779).
