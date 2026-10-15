---
title: An ESP32-C3 Flight Radar on a 1.28-Inch Round Display
description: Micro Radar turns OpenSky flight data into a round ESP32-C3 radar display, with browser configuration, aircraft tracking and smooth animation.
locale: en
translationKey: micro-radar-esp32-c3
pubDate: '2026-06-22'
category: open-source
tags:
- ESP32-C3
- OpenSky
- GC9A01
- Micro Radar
draft: false
seoTitle: 'ESP32-C3 Micro Radar: Round OpenSky Flight Display'
seoDescription: Micro Radar turns OpenSky flight data into a round ESP32-C3 radar display, with browser configuration, aircraft tracking and smooth animation.
---

Micro Radar takes a 1.28-inch, 240 × 240 round IPS display module with an ESP32-C3, connects it to Wi-Fi, requests nearby aircraft state vectors from OpenSky, and draws them as an old-fashioned radar sweep.

![micro radar esp32 c3 — figure 1](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-01.webp)

This is not a conventional radio radar, nor is it a 1090 MHz ADS-B receiver. It doesn't receive aircraft transmissions directly. Instead, it turns open aviation data into a small desktop display.

| Item | Details |
| --- | --- |
| Project | Micro Radar |
| Hardware | ESP32-C3 with 1.28-inch GC9A01, 240 × 240 IPS round display |
| Data source | OpenSky REST API, `/states/all` |
| Development | PlatformIO with Arduino framework |
| Open-source materials | Source code, STL/3MF/Onshape enclosure models, assembly instructions |

**GitHub:** https://github.com/AnthonySturdy/micro-radar

The project brings several simple parts together into a finished desktop device. There's a printable housing with a front lens, a USB-C extension to the back, and an initial Wi-Fi setup hotspot. Once connected, you can open a browser to change its coordinates, radar range, display options, and OpenSky credentials.

![micro radar esp32 c3 — figure 2](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-02.webp)

## What makes it work

**One integrated module.** The ESP32-C3, round display, and wireless connectivity come on a single board. The README explicitly says “no soldering required,” which makes the build approachable.

**Aircraft positions via OpenSky.** Firmware requests `/states/all` and supplies `lamin`, `lamax`, `lomin`, and `lomax` to define a geographic bounding box. The response contains information such as aircraft position, speed, heading, altitude, and callsign.

**Browser-based setup.** WiFiManager creates a `MicroRadar-Setup` hotspot on first boot. Once connected to your network, visit `microradar.local` to configure location, range, radar sweep, aircraft labels, heading triangles, and OpenSky client credentials.

**Smooth animation.** The display is more than a periodically updated set of dots. LovyanGFX Sprites provide a 240 × 240 back buffer for drawing the radar circles, sweep, and aircraft. `TrackedAircraft` applies dead reckoning and easing between new positions.

![micro radar esp32 c3 — figure 3](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-03.webp)

The main code path is easy to follow. `main.cpp` initializes the display, Wi-Fi, and configuration server. In the loop, `aircraftManager.Update()` retrieves data before the radar UI is drawn to a back buffer. `AircraftManager` schedules requests within API limits, maintains `trackedAircraft`, and projects latitude and longitude into screen coordinates.

OpenSky doesn't provide new positions every rendered frame. If the display simply jumped whenever a fresh position arrived, aircraft would move in steps. Micro Radar predicts movement from speed and `true_track`, then interpolates toward that estimate. It's a small implementation detail with a noticeable effect on the display.

## Hardware connections

![micro radar esp32 c3 — figure 4](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-04.webp)

The integrated ESP32-C3 display module eliminates much of the wiring. In `LGFX.h`, the GC9A01 configuration uses `SPI2_HOST` with MOSI on GPIO7, SCLK on GPIO6, DC on GPIO2, CS on GPIO10, and backlight on GPIO3. SPI write frequency is 27 MHz. If you use the same display board, you can follow the project's build instructions; a different module may require pin and driver changes.

![micro radar esp32 c3 — figure 5](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-05.webp)

## Three details worth reading in the source

First is **API request pacing**. `AircraftManager::Initialise()` calculates `fetchInterval` from anonymous or authenticated OpenSky quotas, leaving a `TOKEN_BUFFER`. Instead of polling every second, the firmware works out its available daily requests and spaces them accordingly. It's a useful pattern for any device built around a rate-limited public API.

Second is **double buffering**. `main.cpp` creates an `LGFX_Sprite backbuffer`, draws the entire frame in memory, then sends it with `pushSprite`. This cuts down on flicker and makes subsequent animation work easier.

Third is **aircraft tracking**. Each aircraft is tracked by `icao24`. When the next location arrives, the rendered icon doesn't immediately snap to the new coordinates; it moves smoothly between updates. Embedded UI quality often comes down to details like these rather than raw processing power.

## What can you take from it?

An ESP32-C3 and a round screen are nothing unusual. The more interesting decision is to build a complete product around one very specific use case. Two ideas carry over to other projects: a narrowly defined purpose is easy for people to understand, and configuration should be accessible through a simple interface rather than by editing firmware.

![micro radar esp32 c3 — figure 6](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-06.webp)
