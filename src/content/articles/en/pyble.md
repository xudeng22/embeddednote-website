---
title: PyBLE Turns Your iPad into a Wireless MicroPython IDE for ESP32
description: PyBLE is an open-source tablet-first MicroPython IDE over BLE. See how PBLE/1 handles editing, files, console, firmware targets and recovery.
locale: en
translationKey: pyble
pubDate: '2026-11-04'
category: open-source
tags:
- PyBLE
- MicroPython
- ESP32
- BLE
- Flutter
draft: false
sourceUrl: https://github.com/PyBLE-dev/PyBLE
author: EmbeddedNote
seoTitle: PyBLE Turns Your iPad into a Wireless MicroPython IDE for ESP32 | EmbeddedNote
seoDescription: PyBLE is an open-source tablet-first MicroPython IDE over BLE. See how PBLE/1 handles editing, files, console, firmware targets and recovery.
---

An ESP32 board on your workbench is easy to reprogram when a laptop and USB cable are within reach. It becomes less convenient once the board is attached to a robot, installed in an enclosure or sitting across a classroom. **PyBLE** proposes a different everyday workflow: use a tablet to edit and run **MicroPython** code over Bluetooth Low Energy.

This is more than a Bluetooth serial terminal. The open-source project combines a Flutter tablet app, a board-side MicroPython agent, a documented **PBLE/1** protocol, testing tools and a browser-based firmware installer. Once provisioned, a supported board can be used without a USB data cable for routine edits and experiments.


![PyBLE project and device provisioning interface.](/uploads/pyble/pyble-02.webp)

*PyBLE project and device provisioning interface.*


## What you can do from the tablet


The tablet application brings together a code editor, board file browser, run/stop commands, soft reboot and a live console. File transfers include integrity checking, resumable upload mechanisms and publication controls designed to reduce the chance of leaving a half-written program behind after a wireless interruption.

There is also an offline **Blockly** workspace for visual programming. GPIO and NeoPixel blocks can generate MicroPython, making PyBLE useful when teaching physical computing or rapidly checking an idea without opening a full desktop toolchain. The normal local development workflow does not require a cloud account or telemetry service.


![PyBLE Blockly workspace for building MicroPython code on a tablet.](/uploads/pyble/pyble-01.webp)

*PyBLE Blockly workspace for building MicroPython code on a tablet.*


## The architecture: PBLE/1 plus a board-side agent


The central design decision is that the board runs a dedicated **PyBLE agent**. The tablet discovers the target BLE GATT service, negotiates capabilities and exchanges commands and data through the PBLE/1 protocol. Its documented GATT characteristics include RX, TX and INFO; the protocol defines framing, fragmentation, operation identities, results and version handling.

That makes features such as listing files, uploading a script, stopping a running program or recovering a broken transfer explicit protocol operations rather than ad hoc control strings. The published agent also separates application code from the transport and recovery machinery. In other words, PyBLE's simplicity at the user interface depends on fairly deliberate engineering on the device.


![System architecture: Flutter app, PBLE/1 over BLE GATT and the MicroPython agent running on the target.](/uploads/pyble/pyble-03.webp)

*System architecture: Flutter app, PBLE/1 over BLE GATT and the MicroPython agent running on the target.*


## Hardware compatibility: check the exact profile


**Stock MicroPython and a BLE-capable chip are not enough.** The target needs a compatible, installed PyBLE agent and a matching firmware profile. This distinction is critical for anyone trying the project on spare development boards.

The current public repository describes **v0.6.1** provisioning for five specific profiles: classic **ESP32 with 4 MiB flash**, **ESP32-S3 N16R8** (16 MiB flash and 8 MiB Octal PSRAM), the exact **Waveshare ESP32-S3-LCD-1.47B B-version**, **ESP32-C3 with 4 MiB flash** (revision v0.3 or newer), and **Raspberry Pi Pico 2 W**. These are exact release profiles, not a blanket guarantee for all boards in a chip family. The separate Waveshare S3 image includes board-specific display features that the generic S3 image does not.

These profiles refer to the published v0.6.1 firmware, rather than universal chip-family support. Confirm the exact board, memory configuration and firmware release before flashing.


## Getting started—and what still requires a cable


Start with the project website and its **/flash** page, then select the profile matching the exact board and memory configuration. For supported ESP32 profiles, initial provisioning uses a desktop Chromium browser and Web Serial. Pico 2 W has a different UF2/BOOTSEL installation process. Back up the board first: initial provisioning can erase the existing firmware, files and settings.

For the app, the project lists an **iPad TestFlight beta** and **invited Android testing**. Availability is therefore different from a broadly released App Store or Google Play product. After the one-time firmware install, ordinary editing and control can take place over BLE—but firmware recovery, destructive flashing and deeper debugging may still need a wired connection.


## Why the project matters


A tablet-based IDE is not going to replace a desktop debugger for every embedded problem. For quick classroom demonstrations, field diagnostics, interactive exhibits and portable MicroPython experiments, however, eliminating the daily USB cable can make development noticeably more approachable.

For embedded engineers, the most reusable part may be the architecture rather than the UI: a versioned BLE protocol, capability negotiation, bounded transfers, recovery behavior and an agent that acknowledges the resource constraints of different microcontrollers.


## Project links


**GitHub:** https://github.com/PyBLE-dev/PyBLE

**Official site and installer:** https://pyble.dev/

**License:** MIT. Check the release page and the compatibility documentation for the latest tested profiles.
