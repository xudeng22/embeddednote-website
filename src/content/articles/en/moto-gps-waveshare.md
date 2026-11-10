---
locale: en
translationKey: moto-gps-waveshare
pubDate: '2026-11-10'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/mx3353672833-debug/moto-gps-waveshare
title: 'MOTO GPS: A Round-Screen Motorcycle Navigator With the Phone in Your Pocket'
description: 'MOTO GPS pairs a Waveshare ESP32-S3 AMOLED board with an iPhone app, a custom BLE protocol and a round PCB. The phone plans; the screen shows the next turn.'
tags:
- MOTO GPS
- ESP32-S3
- Waveshare
- AMOLED
- BLE
- Motorcycle Navigation
- LVGL
- Open Source
seoTitle: 'MOTO GPS: ESP32-S3 Round-Screen Motorcycle Navigator'
seoDescription: 'Inside MOTO GPS: Waveshare ESP32-S3 AMOLED hardware, CO5300 pins, a BLE v1 frame format, a shared C++ navigation core and a round PCB.'
---

A 1.75-inch circle sits on the handlebar. The phone stays in a jacket pocket. The screen shows a white route, the next turn and a distance — not a mirrored phone display. **[MOTO GPS](https://github.com/mx3353672833-debug/moto-gps-waveshare)**, by Maler X, is built around the **Waveshare ESP32-S3-Touch-AMOLED-1.75C**, but the board is only half the story. The repository also contains an iPhone app, an Android app, a routing gateway, a shared C++ navigation core, a custom BLE protocol and a four-layer round PCB that has been designed but not fabricated.

![MOTO GPS round-screen navigator mounted on a motorcycle handlebar](/uploads/moto-gps-waveshare/moto-gps-hero.webp)

*A design render of the V3 enclosure on a handlebar. The current build uses the Waveshare dev board, not the custom housing.*

At the time of writing it has more than 500 stars and 96 forks. It is not a product. There is no App Store build, no prebuilt firmware and no finished enclosure for sale. What exists is a source-available prototype with a long README and a separate DIY guide.

## One repository, the whole chain

Most hobby navigation projects stop at a screen and a GPS module. This one keeps the chain: ESP32 firmware for the Waveshare board, an iOS app with Core Location and MapKit, a native Android client, a Node gateway that hides the AMap key, a shared C++ core for route progress and map projection, a WebAssembly preview, and KiCad files for a 52 mm round board. The breadth is the point — and so is the documentation of where each piece stops.

<video controls muted loop playsinline poster="/uploads/moto-gps-waveshare/moto-gps-nav-poster.jpg" style="display:block;width:100%;max-width:620px;margin:26px auto 10px;border-radius:12px;background:#0b0f12;">
  <source src="/uploads/moto-gps-waveshare/moto-gps-nav.mp4" type="video/mp4">
</video>

*The navigation page recording published on the project's Glimpse site. Route, distance and speed-limit values are demo data.*

## The hardware: a dev board now, a round PCB on paper

The current build uses a ready-made Waveshare board: an **ESP32-S3** with **32 MB of flash and 8 MB of PSRAM**, a **1.75-inch 466 × 466 AMOLED** driven by a **CO5300** over QSPI, a **CST9217** touch controller, a **QMI8658** six-axis IMU and an **AXP2101** PMIC. USB-C and a battery connector are already on the board.

The public Waveshare schematic makes the display bus easy to audit. On J3, `LCD_CS` is **GPIO12**, `QSPI_SCLK` is **GPIO38**, `QSPI_D0` through `QSPI_D3` are **GPIO4–GPIO7**, `LCD_RST` is **GPIO1**, and `LCD_TE` is **GPIO13**. Touch sits on a separate I²C pair: `TP_SDA` **GPIO15**, `TP_SCL` **GPIO14**, `TP_INT` **GPIO11**, `TP_RST` **GPIO2**.

The TE line is the one people skip. A display can light up without it, but the map will tear when it rotates quickly. The firmware waits for the panel's frame-start pulse before starting a QSPI transfer, then schedules the next render around a 25 ms target. That is a display-synchronisation problem, not a graphics-library setting.

<p><a href="/uploads/moto-gps-waveshare/moto-gps-board-en.webp" target="_blank" rel="noopener"><img src="/uploads/moto-gps-waveshare/moto-gps-board-en.webp" alt="MOTO GPS board-level wiring diagram" style="width:100%;"></a></p>

*Display, touch, IMU and PMIC signal assignments. Pin names follow Waveshare's J3 and the project BSP; this is a reading aid, not a fabrication drawing. Open full size.*

<p><a href="/uploads/moto-gps-waveshare/moto-gps-schematic-j3.webp" target="_blank" rel="noopener"><img src="/uploads/moto-gps-waveshare/moto-gps-schematic-j3.webp" alt="Waveshare ESP32-S3-Touch-AMOLED-1.75C schematic, J3 detail" style="width:100%;"></a></p>

*The J3 detail from the public Waveshare schematic. The display uses QSPI plus a dedicated TE line; touch uses I²C with interrupt and reset. Open full size.*

The custom **H0175 EVT A1** board is a different story. It is a **52 mm four-layer** design built around an **ESP32-S3-WROOM-1U-N16R8**, with an **LC76GABMD** GNSS receiver, **QMI8658A** and **IIS2MDCTR** sensors, a **BQ25628E** charger, a **TPS63070** buck-boost converter and a **TUSB320LAI** USB-C controller. The V3 enclosure is **61 mm in diameter and 16 mm thick**, with a Garmin-compatible quarter-turn mount.

None of that is ready to order. The hardware folder is marked **DO NOT ORDER**. The KiCad ERC and DRC pass, but the display FPC, power-path switching, RF behavior, thermal margin and vibration resistance have not been validated. The A1 and V3 work is paused while the Waveshare build is developed. Treat the files as an engineering record, not a production release.

<p><a href="/uploads/moto-gps-waveshare/moto-gps-a1-pcb.webp" target="_blank" rel="noopener"><img src="/uploads/moto-gps-waveshare/moto-gps-a1-pcb.webp" alt="H0175 EVT A1 custom round PCB" style="width:100%;"></a></p>

*The A1 PCB preview. A 52 mm four-layer round board with GNSS, IMU, magnetometer and charging hardware. It remains an engineering candidate.*

## The split: the phone plans, the screen presents

The architecture is deliberately asymmetric. The phone is the authority for position, search and route progress. iOS uses Core Location, sends search and route requests through the author's HTTPS gateway to AMap, and keeps the AMap key on the server. A shared C++ `NavCore` runs route progress, off-route detection and reroute logic on the phone. The full route never moves to the display.

What the display receives is a projection: a navigation snapshot, a local slice of route geometry, and an optional map window with roads and buildings around the current position. The window is capped at **24 road polylines / 192 road points** and **16 building footprints / 128 building points**. That is enough for the next few hundred meters, not for a city.

<p><a href="/uploads/moto-gps-waveshare/moto-gps-system-en.webp" target="_blank" rel="noopener"><img src="/uploads/moto-gps-waveshare/moto-gps-system-en.webp" alt="MOTO GPS system data path" style="width:100%;"></a></p>

*The phone keeps the route and the routing state. The ESP32 receives a cropped display projection and renders it. Open full size.*

Coordinate systems are part of that boundary. Search and positioning use WGS84; route geometry is normalized to GCJ-02 for the Chinese map source. Mixing the two without conversion shifts the route against the background. The repository documents the conversion points rather than hiding them in a helper function.

On the device, `PhoneNavBridge` decodes and reassembles frames, adapts them to `moto::nav::NavSnapshot`, and hands them to `NavPresenter`. The presenter keeps the arrow fixed and translates and rotates the map underneath it. `LVGL` draws the result. The QMI8658 supplies short-term angular rate so the heading page can respond between position updates; the phone's course remains the long-term reference. The ESP32 does not run a second route state machine, and it does not call AMap.

## The BLE link is a protocol, not a UART bridge

The radio link is where hobby projects usually stop at a characteristic UUID and a JSON string. MOTO GPS defines a GATT service with an encrypted write characteristic (`PhoneToDevice`) and an encrypted notify characteristic (`DeviceToPhone`). The device is the peripheral; the phone is the central. LE Secure Connections with bonding is the baseline; Just Works pairing means there is no MITM protection, a limitation the documentation states plainly.

Every GATT operation carries one complete protocol frame. The v1 header is ten bytes: magic `0xB7`, protocol version `1`, message type, flags, a 16-bit sequence number, a 16-bit fragment offset and a 16-bit total message length. The payload follows, then a two-byte CRC-16/CCITT-FALSE. Flags carry `START`, `END`, `ACK_REQUESTED` and `URGENT`; every fragment is checked independently.

<p><a href="/uploads/moto-gps-waveshare/moto-gps-ble-en.webp" target="_blank" rel="noopener"><img src="/uploads/moto-gps-waveshare/moto-gps-ble-en.webp" alt="MOTO GPS BLE v1 frame format" style="width:100%;"></a></p>

*The v1 frame: a ten-byte header, N payload bytes and a CRC16. At MTU 23 the payload is only eight bytes, so the protocol fragments and reassembles its own messages. Open full size.*

The frame size is not the ATT MTU. It is `min(local ATT_MTU − 3, peer max_frame_size, 512)`. At an MTU of 23, the characteristic value is 20 bytes and the payload is only **8 bytes**, so a 300-byte route window becomes 38 fragments. The protocol handles that fragmentation itself instead of relying on Prepare Write or Long Write, which behave differently across stacks.

Reassembly is strict: one unfinished logical message per direction, contiguous fragment offsets, a one-second timeout, and a duplicate check that does not refresh the timer. A newer `START` can replace a stuck message. Sequence number zero is reserved, and a new session clears the sequence baseline and any partial fragments. Commands that request an ACK are retried after **750 ms**, twice, with the same sequence and identical fragments. A `NavigationSnapshot` does not request an ACK; a newer snapshot replaces the old one. The heartbeat is a session timer, not the phone's uptime, and three seconds without a valid frame marks the protocol link as lost.

| Type | Message | Direction |
| --- | --- | --- |
| `0x01` | ConnectionStatus | Both |
| `0x02` | Heartbeat | Both |
| `0x10` | NavigationSnapshot | Phone → device |
| `0x11` | RouteGeometry | Phone → device |
| `0x12` | TrafficDeviation | Phone → device |
| `0x14` | MapScene | Phone → device |
| `0x20` | DeviceCommand | Device → phone |

## Drawing a map on a 466 × 466 circle

The firmware uses two **320-row PSRAM draw buffers**. LVGL renders into one while the QSPI DMA sends the other, and the TE interrupt gates the start of a transfer to the panel's active scan. The firmware targets ESP-IDF 5.5.5 and the Waveshare BSP 3.0.0, with LVGL pinned at 9.5.0. The target cadence is 25 ms per frame, about 40 Hz, but the code treats that as a scheduling target rather than a measured guarantee. The README does not claim a frame rate.

The UI is built around the circle. A fixed arrow marks the rider's position; the route and surrounding roads move and rotate beneath it. The bottom half carries the turn icon, distance and a progress arc. Speed, heading and music each get a page, switched by a horizontal swipe. The page indicator hides after five seconds, and the PWR button requests a software shutdown through the PMIC after a three-second hold.

<p><a href="/uploads/moto-gps-waveshare/moto-gps-ui-pages.webp" target="_blank" rel="noopener"><img src="/uploads/moto-gps-waveshare/moto-gps-ui-pages.webp" alt="MOTO GPS four round-screen pages" style="width:100%;"></a></p>

*Navigation, speed, heading and music. The same LVGL UI builds for the device and the WebAssembly preview.*

<video controls muted loop playsinline poster="/uploads/moto-gps-waveshare/moto-gps-speed-poster.jpg" style="display:block;width:100%;max-width:620px;margin:26px auto 10px;border-radius:12px;background:#0b0f12;">
  <source src="/uploads/moto-gps-waveshare/moto-gps-speed.mp4" type="video/mp4">
</video>

*The speed page recording. The arc and numerals are driven by the phone's location updates, with sample data in the demo.*

The music page is a remote, not a player. The ESP32 sends previous, play/pause and next commands over BLE; iOS performs the media action and sends the current track and playback state back. Audio stays on the phone's existing output, such as a helmet headset. On Android, the app targets players that publish a system media session.

<video controls muted loop playsinline poster="/uploads/moto-gps-waveshare/moto-gps-music-poster.jpg" style="display:block;width:100%;max-width:620px;margin:26px auto 10px;border-radius:12px;background:#0b0f12;">
  <source src="/uploads/moto-gps-waveshare/moto-gps-music.mp4" type="video/mp4">
</video>

*The music page recording. The round screen displays state and sends transport commands; it does not decode audio.*

## Offline maps are background, not offline routing

The map layer is easy to misread. The phone downloads roads and buildings from OpenStreetMap/Protomaps, caches tiles, and sends the device a small window around the current position. The bundled Jinan SQLite fallback is **9.73 MiB** and contains **47,468 road polylines**, **266,985 road nodes**, **26,702 building footprints** and **148,140 building nodes**. Automatic caching is capped at **128 MB**; manual downloads at **512 MB**.

That data is background only. Place search, new route planning, off-route recalculation and live traffic still require the network. The offline package does not contain a routing graph, and the README says so directly. Coverage also depends on local OSM density: an area with sparse building data will look sparse, not fabricated.

<p><a href="/uploads/moto-gps-waveshare/moto-gps-app-maps.webp" target="_blank" rel="noopener"><img src="/uploads/moto-gps-waveshare/moto-gps-app-maps.webp" alt="MOTO GPS iPhone map and offline download settings" style="display:block;width:100%;max-width:520px;margin-left:auto;margin-right:auto;"></a></p>

*The iPhone map-management screen. Offline downloads store roads and buildings, not a routing engine or live traffic.*

Traffic comes from AMap through the gateway. The current route is drawn as a white line; per-segment traffic coloring and stale/unknown states are still being refined. Real road speed limits and traffic-light countdowns are not connected. The speed-limit sign in the UI is a display element waiting for a trustworthy data source, not a live reading.

## What works, and what is still a prototype

The current build is a Waveshare board plus an iPhone. The iPhone app requires iOS 17 or later, Xcode 16 or later and a Swift 6 toolchain; there is no App Store release. An unsigned **v0.3.1 IPA** is published for sideloading, but it must be re-signed with the user's own Apple account, and free signatures expire after seven days. The Android app is native Kotlin/Compose, requires Android 8.0 or later and does not need Google Play services; its real-device pairing and riding validation is still in progress.

The unfinished list is longer than the feature list:

- Real speed limits and traffic-light countdowns are not connected.
- AMap driving routes do not guarantee motorcycle restrictions are avoided.
- BLE reconnect after lock screen, network changes and long rides is still being regression-tested.
- Cross-city route consistency and online/offline map switching remain active work.
- Frame rate, power consumption, thermal behavior and vibration resistance have no published acceptance data.
- The A1 board and V3 enclosure are paused; the hardware is marked **DO NOT ORDER**.

The automated checks are real but narrow. As of the September 2026 update, the project reports 9 C++ native test groups, 60 backend tests, 12 Swift core tests and 13 BLE policy tests, plus demo-fixture and map-database validation. Those check code and data paths. They do not prove a motorcycle ride, a locked phone, a weak-signal reconnect or a long battery run.

<p><a href="/uploads/moto-gps-waveshare/moto-gps-app-routes.webp" target="_blank" rel="noopener"><img src="/uploads/moto-gps-waveshare/moto-gps-app-routes.webp" alt="MOTO GPS iPhone route selection screen" style="display:block;width:100%;max-width:520px;margin-left:auto;margin-right:auto;"></a></p>

*The iPhone route picker. Up to three AMap candidates are compared by time, distance and traffic before navigation starts.*

*Images and screen recordings come from the MOTO GPS repository and the Glimpse site (Maler X); the Waveshare schematic excerpt is from the board's public documentation. The block diagrams were redrawn for this article.*

The license is **PolyForm Noncommercial 1.0.0**. The source is available for personal study, research and non-commercial use; distributing a modified firmware or a preinstalled device requires the license notice and attribution to Maler X. Commercial use needs separate permission. Map data carries its own ODbL attribution, and AMap services are used under their own terms.

The reusable idea is not the round screen. It is the boundary: keep route progress where the map and network already are, send the device a projection it can draw deterministically, and treat the radio link as a protocol with sessions, sequence numbers, CRC and explicit message lifetimes. That is the part worth reading in the repository — along with the pin table, the TE timing and the list of things the author has not yet proven.
