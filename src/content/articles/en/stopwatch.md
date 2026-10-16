---
title: M5Stack Core StopWatch Pairs an ESP32-S3 with a 1.75-Inch AMOLED
description: 'A look at M5Stack’s compact Core StopWatch development board: ESP32-S3R8, 466×466 AMOLED touch display,
  audio, IMU, RTC, and a 450mAh battery.'
locale: en
translationKey: stopwatch
pubDate: '2026-05-25'
category: hardware
tags:
- M5Stack
- ESP32-S3
- AMOLED
- Development Board
- Wearables
draft: false
author: EmbeddedNote
sourceUrl: https://docs.m5stack.com/en/core/StopWatch
seoTitle: 'M5Stack Core StopWatch: ESP32-S3 AMOLED Development Board'
seoDescription: M5Stack Core StopWatch features an ESP32-S3R8, 1.75-inch 466×466 AMOLED, 16MB flash, 8MB PSRAM,
  450mAh battery, IMU, and published schematics.
---

M5Stack’s **Core StopWatch** looks more like a finished gadget than a conventional development board. Its circular enclosure is built around a **1.75-inch AMOLED touchscreen**, with an **ESP32-S3R8** handling the application. It is a sensible starting point for a wearable interface, electronic badge or compact IoT control panel.

The display has a **466 × 466** resolution. Inside are **16MB of flash** and **8MB of PSRAM**. M5Stack lists **2.4GHz Wi-Fi** as the product’s wireless interface. The ESP32-S3 family also has Bluetooth capability at the silicon level, although actual software support depends on the firmware stack. Two programmable buttons, a separate power button and a vibration motor round out the basic interface.

![M5Stack Core StopWatch product feature diagram](/uploads/stopwatch/stopwatch-01.webp)

Documentation: [Core StopWatch hardware reference](https://docs.m5stack.com/en/core/StopWatch) and [factory firmware guide](https://docs.m5stack.com/en/guide/display_device/stopwatch/usage).

## More than a display board

The rest of the hardware is useful for interactive prototypes. There is a **MEMS microphone**, an **ES8311 audio codec**, a **1W speaker**, a **BMI270 six-axis IMU** and an **RX8130CE real-time clock**. An HY2.0-4P connector and rear expansion headers provide access to external hardware. The enclosure also includes a lanyard hole and magnetic mounting provisions.

Power comes from a **450mAh battery** managed by M5Stack’s **M5PM1** power subsystem, with USB-C for power and charging. That integration removes much of the usual wiring involved in putting together a battery-powered prototype with a display, motion sensing and basic audio interaction.

## Schematics are available

![M5Stack Core StopWatch schematic and functional overview](/uploads/stopwatch/stopwatch-02.webp)

![M5Stack Core StopWatch power and interface diagram](/uploads/stopwatch/stopwatch-03.webp)

M5Stack publishes schematics and pin maps, so developers can check the display interface, expansion pins and power domains before writing firmware. The source article quoted a price of around **US$45**; that is a historical reference rather than a live price.

*Hardware revision note: M5Stack has documented a labeling error on some early v1.0 units. A pin marked “BAT” on the affected label is actually a 5V input. Check the documentation for your exact board revision before connecting external power.*
