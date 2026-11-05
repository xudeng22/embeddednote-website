---
title: Make Your Old Bench Power Supply Programmable with This ESP32-S3 Project
description: PSU-EXT adds SCPI, current and voltage monitoring, relay control and a web dashboard to a bench PSU. Explore the hardware, isolation and limitations.
locale: en
translationKey: psu-ext
pubDate: '2026-11-05'
category: hardware
tags:
- ESP32-S3
- Bench Power Supply
- SCPI
- Test Automation
- Open Source Hardware
draft: false
sourceUrl: https://github.com/PSU-Ext-Org
author: EmbeddedNote
seoTitle: Make Your Old Bench Power Supply Programmable with This ESP32-S3 Project | EmbeddedNote
seoDescription: PSU-EXT adds SCPI, current and voltage monitoring, relay control and a web dashboard to a bench PSU. Explore the hardware, isolation and limitations.
---

Plenty of bench power supplies are still perfectly good at supplying a stable voltage but offer little help with automated testing. Maybe yours has no remote-control interface. Maybe it has an interface that is painful to integrate. Replacing the instrument is one answer; **PSU-EXT** offers another.

This open-source project places a small controller **between an existing bench PSU and the device under test**. It measures voltage and current, switches the output with a relay, and exposes programmable controls through SCPI, USB and Wi-Fi. The original power supply still generates and regulates the voltage. PSU-EXT adds a layer of observation, switching and test automation; it does **not** turn a fixed-output supply into an independently programmable voltage source.


![PSU-EXT hardware prototype with input/output banana connectors.](/uploads/psu-ext/psu-ext-01.webp)

*PSU-EXT hardware prototype with input/output banana connectors.*


## What the inline controller adds


PSU-EXT is designed around tasks engineers repeat all day: measure a load, turn power on or off, enforce configured limits, collect telemetry and trigger timed sequences. Its documented software interface includes **SCPI** commands, which is valuable if you already automate lab instruments with scripts.

The material supplied with the article describes an operating envelope of **0–25 V and 0–2.5 A**, a board around **100 × 50 mm**, and **USB-C** for control-side power and communications. Those figures describe the published prototype, not a certification or a guarantee that every future hardware revision will share the same limits.


![PSU-EXT PCB layout showing the power terminals and ESP32-S3 control section.](/uploads/psu-ext/psu-ext-02.webp)

*PSU-EXT PCB layout showing the power terminals and ESP32-S3 control section.*


## Inside the hardware


The main controller is an **ESP32-S3-WROOM-1-N16R8**. For current sensing, the design combines an **INA240A2** current-sense amplifier with an **ADS1115** 16-bit ADC. Rather than measuring the tiny shunt voltage directly with the microcontroller ADC, it conditions the signal first and digitizes it separately. A voltage-divider path supports voltage measurement.

The project also makes a meaningful effort to isolate the measurement side: **ISO1540** provides I²C isolation and an **RFM-0505S** isolated DC-DC module supplies the isolated domain. The hardware documentation describes galvanic isolation between the control and measurement domains. That is useful in an instrument interface, but it should not be confused with a complete safety certification or an excuse to ignore grounding and voltage limits.

A **HF49FD/005-1H12T** relay handles load switching. The supplied description identifies relay control on **GPIO38** and a default-off state at startup. Engineers should still assess the actual switching rating, startup transients and failure modes for their own device under test.


![Measurement and relay-control schematic with current shunt, INA240, ADS1115 and isolation circuitry.](/uploads/psu-ext/psu-ext-03.webp)

*Measurement and relay-control schematic with current shunt, INA240, ADS1115 and isolation circuitry.*


## Firmware and browser dashboard


On the software side, the firmware is built with **ESP-IDF** and exposes SCPI through **USB CDC** and a **Wi-Fi TCP server on port 5025**. That makes it possible to connect a PC-side test script without treating the device as a one-off Bluetooth gadget or inventing a proprietary instrument command format.

The project also includes a desktop-facing software stack: **Java 17 and Spring Boot** on the back end, with a **React** dashboard on the front end. The interface brings live voltage, current and power observations together with output control and OVP/OCP configuration. The project organization maintains separate repositories for hardware, firmware and software, instead of publishing only a PCB render and leaving the rest as an exercise.


![PSU-EXT browser dashboard displaying output state, measured voltage and current, and protection settings.](/uploads/psu-ext/psu-ext-04.webp)

*PSU-EXT browser dashboard displaying output state, measured voltage and current, and protection settings.*


## A useful EVT project, not a finished safety instrument


The supplied project description explicitly identifies the hardware as an **engineering validation (EVT) prototype** and warns that **reverse-polarity protection is absent**. That point deserves more attention than the web interface: incorrect input/output wiring could damage hardware. Use it only within documented ratings and with appropriate external protections. Do not rely on a hobby prototype as the sole protection layer for valuable equipment or unattended tests.

In particular, confirm current and voltage ratings, relay interruption behavior, OVP/OCP response, isolation boundaries and measurement calibration with the exact hardware revision before connecting expensive loads. The module is best approached as an open-source engineering platform for experimentation and test automation, not as a certified replacement for a programmable laboratory PSU.


## Who should take a look?


If you perform power-cycle tests, record a board's startup consumption, run repetitive firmware validation or want to connect a conventional bench supply to an automated test bench, PSU-EXT is an interesting starting point. Its value lies in the complete path from analog front end to networked SCPI control—not simply the presence of an ESP32-S3.

**Project organization:** https://github.com/PSU-Ext-Org

**Hardware license:** CERN-OHL-S v2. **Firmware and software licenses:** Apache-2.0, as listed by the project organization. Review current project files and hardware warnings before building.
