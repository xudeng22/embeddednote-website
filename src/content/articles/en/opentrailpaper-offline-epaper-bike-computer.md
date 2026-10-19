---
title: OpenTrailPaper Turns a LILYGO E-Paper Board into an Offline Bike Computer
description: An ESP32-S3 bike computer with offline maps, GPX navigation, FIT ride recording and BLE cycling sensors, built on LILYGO’s
  4.7-inch e-paper board.
locale: en
translationKey: opentrailpaper-offline-epaper-bike-computer
pubDate: '2026-09-08'
category: open-source
tags:
- OpenTrailPaper
- ESP32-S3
- LILYGO
- E-Paper
- Cycling
- Open Source
draft: false
seoTitle: 'OpenTrailPaper: An Offline ESP32-S3 E-Paper Bike Computer'
seoDescription: How OpenTrailPaper turns LILYGO’s T5 E-Paper S3 Pro into a standalone cycling computer with offline maps, GPX routes,
  FIT logs and BLE sensors.
---

A development board with GPS, LoRa and a 4.7-inch e-paper display would make a perfectly serviceable weather station. [OpenTrailPaper](https://github.com/RaemondBW/OpenTrailPaper) takes it in a different direction: it turns the **LILYGO T5 E-Paper S3 Pro** into a bicycle computer that works without a phone or mobile data connection.

It can follow a GPX route, show locally stored maps, record rides in FIT format and display readings from Bluetooth heart-rate monitors and cycling power meters. The hardware is an off-the-shelf ESP32-S3 development board; the work is in the firmware and the supporting software.

![OpenTrailPaper e-paper bike computer showing power, speed, heart rate, cadence and distance](/uploads/opentrailpaper/opentrailpaper-cover.webp)

Power, speed, heart rate, cadence, ride time and distance are visible on the same screen.

**GitHub:** [RaemondBW/OpenTrailPaper](https://github.com/RaemondBW/OpenTrailPaper)

The T5 E-Paper S3 Pro uses an **ESP32-S3-WROOM-1**, with a dual-core Xtensa LX7 processor running at up to 240 MHz, 16 MB of SPI flash and 8 MB of PSRAM. Its **ED047TC1** panel is a 4.7-inch, 960 × 540 monochrome e-paper display with 16 grayscale levels. A GT911 controller provides capacitive touch input, while the TPS65185 handles the panel's display power rails.

Alongside the ESP32-S3's 2.4 GHz Wi-Fi and Bluetooth LE, the board carries an **SX1262 LoRa transceiver**. Board variants are offered for different regional frequency bands, including 433, 868 and 915 MHz. Position data comes from a u-blox MIA-M10Q or an L76K/CASIC GNSS receiver, depending on the hardware revision; the firmware detects the installed receiver. There is also a **PCF85063 RTC**, a BQ25896 battery charger and a BQ27220 fuel gauge. The 3.7 V, 1,500 mAh battery and 129 × 69 × 11 mm enclosure make the board reasonably compact for handlebar mounting.

![LILYGO T5 E-Paper S3 Pro hardware overview and pin mapping](/uploads/opentrailpaper/opentrailpaper-hardware.webp)

## The ESP32-S3 handles the ride; the phone handles setup

The head unit owns the jobs that cannot stop when cellular coverage disappears: GNSS positioning, speed and sensor updates, navigation cues, map drawing and writing ride logs to the microSD card. A route and its map data can be loaded before departure; the ride itself does not require the companion app to remain connected.

The phone is better suited to tasks that are cumbersome on an e-paper touchscreen. The SwiftUI iOS app handles destination searches, route planning, GPX transfer, map preparation, ride history, settings and firmware updates. An Android companion built with Jetpack Compose was also being developed. The division is deliberate: prepare the route on the phone, then leave the head unit to navigate and record it.

Offline maps deserve a closer look. The main phone workflow divides an area into **Uber H3 hexagonal cells**, generates compact map files from OpenStreetMap data and transfers them to the device. Those files are stored under `/maps/tiles/` on the SD card, where the firmware can retrieve the cells covering the current position. Elevation grids can be included in the phone-generated tiles.

There are two other ways to prepare a map without the iOS app. The repository provides a Python script, and the project website has a JavaScript-based browser generator. These produce a **whole-region EBM2 map** for the `/maps/` directory, used as a fallback when H3 tiles are unavailable. They are not simply interchangeable H3 tile generators. The site also offers a browser-based firmware flasher, so getting the device running does not necessarily require installing PlatformIO.

Rides are recorded as FIT files on the microSD card and can be imported into compatible cycling analysis services. GPX routes and offline maps are stored separately, rather than being bundled with each activity recording.

![Generating offline maps and following turn cues on the e-paper display](/uploads/opentrailpaper/opentrailpaper-maps.webp)

The browser map generator and on-device navigation view show the two ends of that workflow.

## Sensors and battery life

OpenTrailPaper can pair over BLE with heart-rate straps, cycling power meters and speed/cadence sensors. ANT/ANT+ experiments are being pursued separately in the `esp32-ant` repository, but they should not be treated as a finished feature of this build. The developer also acknowledges using Claude to help write code, with human review and testing rather than unattended generation.

The early battery-life estimate was **under eight hours without the front light**, with further power optimization planned. Runtime depends heavily on GNSS reception, BLE activity, e-paper updates, backlight settings and firmware behavior, so that estimate is not a measured guarantee for every ride.

![OpenTrailPaper iOS companion screens for route planning, ride history and settings](/uploads/opentrailpaper/opentrailpaper-companion.webp)

The companion app covers route planning, recorded rides, device settings and firmware delivery.

## Where the design makes compromises

The T5 S3 Pro is not waterproof. An exposed handlebar mount needs protection in rain, particularly around its connectors. There is no barometric altimeter, so climbing figures rely on elevation data associated with the map rather than direct atmospheric-pressure measurements. The single-frequency GNSS receiver also lacks the resilience of a multi-band unit.

Without a magnetometer, the display cannot determine which way the stationary bike is facing from heading alone. Small physical buttons and touch controls are less convenient with winter gloves or wet hands. These are real limitations for a device used outdoors rather than on a workbench.

Even so, the combination has a practical advantage: e-paper remains readable in strong sunlight, and the screen needs very little power while holding a static image. It is a sensible display choice for a head unit whose main job is to show ride metrics and an occasional map update, not animate a full-color interface.

No custom hardware assembly is required: the project targets the standard LILYGO T5 E-Paper S3 Pro. In early September 2026, the board was listed at roughly **$90 on Amazon** and **$103 on AliExpress**, depending on the seller. Prices and availability will vary. The repository is published under **Apache-2.0** and, as of September 7, had around **146 GitHub stars**. It was still evolving rapidly, which is worth keeping in mind before relying on it for a long ride.
