---
title: 'Particle Snowflake: A Christmas PCB That Lights Up When You Say "Sparkle"'
description: 'Inside Particle Snowflake: a Christmas-themed open-source PCB with a P2 Wi-Fi module, 36 RGB LEDs, a speaker, and on-device keyword detection.'
locale: en
translationKey: particle-snowflake
pubDate: '2026-10-28'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/particle-iot/snowflake
tags:
  - Particle Snowflake
  - Particle P2
  - Christmas
  - RGB LEDs
  - Edge Impulse
  - Open Source Hardware
seoTitle: 'Particle Snowflake: An Open-Source Christmas PCB with Voice-Triggered LEDs'
seoDescription: 'Explore Particle Snowflake, a Christmas-themed P2 PCB with 36 addressable RGB LEDs, a speaker, PDM microphone and on-device Sparkle keyword detection.'
---

Most holiday electronics projects start with a development board and an LED strip. Particle went a different way: it designed the decoration itself as a snowflake-shaped PCB, complete with 36 RGB LEDs, a speaker, a microphone and its P2 Wi-Fi module. The hardware and firmware files are available on GitHub, so it is more than a one-off ornament.

![Front and back of the Particle Snowflake Christmas PCB with P2 module and 36 LEDs](/uploads/particle-snowflake/particle-snowflake-cover.webp)

*The two sides of the Snowflake board. The P2 module and audio circuitry are mounted on the back. Image: Particle.*

[GitHub repository](https://github.com/particle-iot/snowflake) · [Particle's Snowflake project page](https://www.particle.io/snowflake/)

## A Wi-Fi module inside a snowflake

At its center is the **Particle P2**, built around Realtek's **RTL8721DM**. The module combines a 200 MHz Arm Cortex-M33 application core with dual-band 2.4/5 GHz Wi-Fi and Bluetooth Low Energy 5.0. It is a capable platform for a decoration that spends much of its time driving lights and playing music.

The 36 individually addressable RGB LEDs run out along six branches of the snowflake. Rather than driving a few LEDs directly from the MCU, the design uses a serial chain of addressable devices. A **74AHC1G125** buffers the control signal and provides the level shift from 3.3 V logic to the 5 V LED domain. Anyone who has chased intermittent WS2812 glitches will recognize why that detail matters: a marginal data-high voltage can produce unpredictable colors and flicker.

Audio comes through a **TPA6211A1**, a mono **Class-AB** amplifier rated for up to 3.1 W under the manufacturer's specified load and supply conditions. It drives the small onboard speaker for short tunes and sound effects; the 3.1 W rating is not a measurement of the ornament's actual acoustic output or continuous speaker power.

The board also has an ST **MP34DT05TR-2 PDM MEMS microphone**, capacitive-touch input at the central Particle logo, a 3.3 V regulator, reset-monitoring circuitry, an NTC temperature-sensing circuit and USB-C power. Packing all of that onto an irregular PCB makes the design worth studying even if you never intend to hang one on a Christmas tree.

![Front side of the Particle Snowflake PCB showing the addressable LED layout](/uploads/particle-snowflake/particle-snowflake-front.webp)

*The front-side LED arrangement and central Particle touch area. Image: Particle.*

## From falling snow to a spoken command

The basic interaction is simple. Apply power and the board starts running LED patterns. Tap the Particle logo to cycle through effects; press and hold it to play a holiday tune. The firmware repository includes the audio playback code and MP3 assets, making it possible to change the music rather than being limited to the supplied tracks.

A firmware update adds the feature behind the most memorable part of the project: say **“sparkle”** and the Snowflake can switch to a special light animation. Particle uses a keyword model developed with **Edge Impulse**, with TensorFlow Lite Micro handling inference on the device. The microphone audio does not need to be uploaded to a cloud speech-recognition service for that keyword detection.

There is one setup detail worth knowing before trying it. In the published firmware, the voice callback checks a `sparkleEnable` setting that defaults to disabled. Installing the newer firmware alone does not guarantee that spoken commands will trigger the animation; the feature also needs to be enabled in the device configuration. The application otherwise uses Particle's platform for connected functions, so local inference should not be confused with a completely cloud-free system.

![Particle Snowflake hardware schematic showing P2, LED chain, touch, microphone and power](/uploads/particle-snowflake/particle-snowflake-schematic.png)

*Particle's schematic brings the LED chain, power rails, touch input and audio sections onto one sheet. Image: Particle.*

## A useful open-source reference design

The repository includes more than the application code. Its `hardware` directory contains schematic and PCB layout files, a bill of materials, silkscreen artwork and manufacturing resources. Under `firmware`, you can find the LED effects, button handling, audio playback, and the Edge Impulse inference integration. The project is released under **Apache License 2.0**, with the usual attribution and notice obligations when redistributing modified files.

The PCB also exposes pads for an additional addressable LED strip. Particle mentions adapting the project into a clock, which is a reasonable next step for a board that already handles lighting, animations and connectivity. For a developer, the interesting part is seeing the LED driver, touch input, MP3 playback and a small keyword-recognition model coexist in a single firmware project.

![Rear view of Particle Snowflake PCB with module, speaker and supporting components](/uploads/particle-snowflake/particle-snowflake-back.webp)

*The reverse side with the P2 module, speaker and the expansion connections. Image: Particle.*

[Watch Particle's LED-effects demo](https://github.com/particle-iot/snowflake/blob/main/media/Snowflake_Action.mp4)

![Particle Snowflake illuminated in the official LED effects demo](/uploads/particle-snowflake/particle-snowflake-lights.webp)

*The Snowflake running an illuminated effect. Image: Particle.*

This was a limited-edition holiday board, not a continuously stocked development kit. Building your own also means sourcing a P2 module and assembling an unusually shaped PCB. The small speaker suits simple tunes better than music playback, while a different wake word or more reliable speech detection would require retraining and testing the model.

Still, as a **Christmas project that doubles as a hardware reference**, Snowflake is unusually well documented. The files are there to inspect, adapt or rebuild—and the firmware contains practical examples of addressable LEDs, touch sensing, audio playback and on-device inference.

Sources: [Particle Snowflake repository](https://github.com/particle-iot/snowflake) · [Official project guide](https://www.particle.io/snowflake/) · [Particle P2 datasheet](https://docs.particle.io/reference/datasheets/wi-fi/p2-datasheet/).
