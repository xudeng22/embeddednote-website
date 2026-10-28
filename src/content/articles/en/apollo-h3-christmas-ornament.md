---
title: 'Apollo H-3: A Christmas Snowman PCB That Doubles as a Bluetooth Proxy'
description: 'A Christmas PCB ornament with 37 LEDs, six tunes and a practical second job: running ESPHome lights and a Bluetooth proxy for Home Assistant.'
locale: en
translationKey: apollo-h3-christmas-ornament
pubDate: '2026-10-29'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/ApolloAutomation/H-3
tags:
- Apollo H-3
- ESP32-C6
- ESPHome
- Home Assistant
- Bluetooth Proxy
- Christmas
- Open-Source Hardware
seoTitle: 'Apollo H-3 Christmas Snowman PCB: 37 LEDs and Bluetooth Proxy'
seoDescription: 'Inside the Apollo H-3 Christmas ornament: ESP32-C6, 37 WS2812 LEDs, five control zones, ESPHome firmware, RTTTL music and Home Assistant Bluetooth proxy.'
---

Most Christmas ornaments don't need a firmware repository. Apollo Automation's H-3 does. The snowman-shaped PCB carries 37 individually addressable RGB LEDs, a buzzer for holiday tunes and an ESP32-C6. It works as a standalone musical decoration, but it can also become a Home Assistant light and Bluetooth proxy when flashed with the smart firmware.

The H-3 is the third entry in Apollo Automation's annual charity ornament series. The team says the proceeds support CASA of Lexington, which advocates for children involved in family-court cases, and the Open Home Foundation, which backs privacy-focused, open-source smart-home infrastructure. The hardware is intentionally playful, but the published ESPHome configuration makes it useful to anyone learning how addressable LEDs, buttons, deep sleep and Home Assistant fit together.

![Apollo H-3 Christmas snowman PCB ornament and its five programmable LED zones](/uploads/apollo-h3/apollo-h3-cover.webp)

*The H-3 uses a snowman-shaped PCB, with 37 RGB LEDs distributed across five zones.*

### Thirty-seven LEDs, five zones and six tunes

An **ESP32-C6** provides the processing and wireless connectivity: 2.4 GHz Wi-Fi 6, Bluetooth Low Energy and 8 MB of flash. The 37 **WS2812** LEDs are connected as a single addressable chain driven from **GPIO3**, but the firmware divides them into five logical zones: **body (24 LEDs), hat (5), mouth (5), eyes (2) and nose (1)**. Each zone can take its own colour or effect.

The buzzer is driven by a PWM output on **GPIO6** and plays melodies encoded as **RTTTL** strings. Three physical buttons connect to **GPIO4, GPIO5 and GPIO7**. Each button has two assigned tracks: a short press selects one, while a double press or hold selects the other. The six included tunes range from familiar Christmas songs such as *Jingle Bells* and *Rudolph the Red-Nosed Reindeer* to the less seasonal *Barbie Girl*. The lights run matching patterns during playback.

Power comes from USB-C or two AA cells. For battery operation, the firmware uses deep sleep and can wake on a song-button press. That matters because an ESP32 running Wi-Fi and continuous Bluetooth scanning is a very different power load from an ornament that wakes briefly, plays a tune and goes back to sleep. The hardware instructions specify the appropriate battery type; rechargeable cells should not be assumed interchangeable without checking that guidance.

![Apollo H-3 snowman printed circuit board on a wooden surface](/uploads/apollo-h3/apollo-h3-product-photo.webp)

*The front of the board has 37 RGB LEDs, with three song buttons on the snowman's body.*

### From a Christmas decoration to a Home Assistant device

The unit ships with **Basic firmware** for standalone music and lighting. Flashing the **Smart firmware**, built with **ESPHome**, exposes the five LED zones to Home Assistant. A red nose, blue eyes or a notification animation can then be controlled like other smart-home lights. The RTTTL strings are editable through Home Assistant as well, so adding a different melody does not require rebuilding the firmware.

The same ESP32-C6 can serve as a **Bluetooth proxy or Bluetooth tracker** for Home Assistant. In practice, that allows the ornament to scan for nearby Bluetooth devices and relay information through the smart-home setup. It's a useful second life for a seasonal decoration, especially in a room where Bluetooth coverage is limited. Continuous scanning, however, increases power consumption; USB-C is the more sensible choice for always-on operation.

The published configuration includes a Wi-Fi access point named **Apollo H3 Hotspot** for initial setup. It also supports **Improv over BLE**, a separate provisioning method. After connecting to Wi-Fi, the device can be discovered and added through Home Assistant. Apollo provides a [browser-based firmware installer](https://install.apolloautomation.com/#/h-3) for switching firmware variants.

![Front view of the Apollo H-3 snowman-shaped PCB on a light background](/uploads/apollo-h3/apollo-h3-pcb-white.webp)

*The five light zones correspond to the snowman's body, hat, mouth, eyes and nose.*

![Made for ESPHome certification badge](/uploads/apollo-h3/apollo-h3-esphome-badge.webp)

*The H-3 is listed in the Made for ESPHome device directory.*

### A useful ESPHome reference design

The repository's [ESPHome YAML files](https://github.com/ApolloAutomation/H-3) are unusually useful as a worked example. They show how the LED chain, RTTTL buzzer, physical buttons, deep-sleep wake-up, firmware updates and Bluetooth features are wired together in a real device. The song-button mappings are handled in the configuration rather than buried inside an opaque binary.

There are also two buttons on the back, marked **BOOT** and **RESET**. One detail worth checking before experimenting: in the current smart firmware, holding RESET for about **10 seconds** triggers a factory reset. A normal press has a different function, so it is worth following the firmware-specific instructions rather than treating every reset press as a configuration wipe.

The limitations are fairly straightforward. It's a seasonal, small-batch charity product, so stock can change. There is no corresponding bare Arduino example in the project repository; the main development path is ESPHome. And while the Bluetooth proxy is a genuinely useful bonus, leaving it active continuously makes much more sense on USB power than on AA batteries.

As a project to study, though, the H-3 offers more than a light show. Its public configuration covers several tasks that appear in everyday ESP32 smart-home builds, packaged in a PCB you could hang on a Christmas tree.

**Project resources:** [GitHub repository](https://github.com/ApolloAutomation/H-3) · [ESPHome device entry](https://devices.esphome.io/devices/apollo_automation_h-3/) · [Apollo documentation](https://wiki.apolloautomation.com/products/h3/introduction/) · [Firmware installer](https://install.apolloautomation.com/#/h-3).
