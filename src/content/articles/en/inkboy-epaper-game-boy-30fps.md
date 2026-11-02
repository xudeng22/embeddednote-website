---
title: Game Boy at 30 FPS on E-Paper? InkBoy Shows How
description: InkBoy uses an ESP32-S3 and SSD1681-driven 1.54-inch e-paper panel
  for roughly 30 display updates a second. Here is how its per-pixel drive
  works—and what it risks.
locale: en
translationKey: inkboy-epaper-game-boy-30fps
pubDate: 2026-10-15
category: display
tags:
  - InkBoy
  - ESP32-S3
  - E-Paper
  - Game Boy
  - SSD1681
  - Display Driver
draft: false
seoTitle: "InkBoy: Game Boy at 30 FPS on a 1.54-Inch E-Paper Display"
seoDescription: An ESP32-S3, SSD1681 controller and selective pixel-driving
  scheme bring Game Boy to a 200×200 e-paper display at roughly 30 fps.
  Understand the trade-offs.
---
E-paper is an unlikely choice for a Game Boy display. Even a partial refresh on a small panel can take hundreds of milliseconds, which is fine for a price tag but disastrous for a scrolling game. Developer Bo Made It has demonstrated something rather different: an ESP32-S3 board running Game Boy games on a **1.54-inch, 200 × 200 e-paper panel**, with roughly **30 display updates per second**. Hackaday covered the experiment on October 14, 2026.

![InkBoy Game Boy emulator on 1.54-inch e-paper editorial illustration](/uploads/inkboy/inkboy-cover.webp)

*Editorial cover illustration. The project's original demonstration image and video follow.*

### Getting past the waveform bottleneck

The interesting work happens below the emulator, in the **SSD1681 display driver**. A stock partial update takes around 360 ms of controller time. InkBoy replaces the usual multi-frame waveform with a short, single-frame drive and treats each pixel independently. Before a scan, the firmware decides whether that pixel needs a pulse toward black, a pulse toward white, or **HOLD**, which leaves it alone. Unchanged pixels are not driven repeatedly just because something else on the screen is moving.

The SSD1681 has two image planes, each 5,000 bytes for this 200 × 200 panel. InkBoy sends them at **20 MHz SPI**, keeps the panel's analog supply active between scans, and reduces an individual drive scan to roughly 14–20 ms depending on the display mode. The approach draws on Wenting Zhang's PaperBoy work, but it operates through the development board's existing controller rather than directly driving bare panel electrodes.

There is an important distinction behind the headline figure. **The Game Boy emulator runs at approximately 59.7 fps; the display takes the newest completed image every 33.3 ms**, giving it about 30 update opportunities per second. It drops stale frames rather than queueing them. A busy scene can miss that pace, and a pixel may need several short pulses before reaching its intended shade. In other words, 30 fps does not mean every pixel has fully settled in 33 ms.

<iframe
  title="InkBoy — original Game Boy on e-paper demo at 30 FPS"
  src="https://www.youtube-nocookie.com/embed/XiZmM6hwwAU"
  loading="lazy"
  referrerpolicy="strict-origin-when-cross-origin"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowfullscreen
  style="display:block;width:100%;max-width:900px;aspect-ratio:16/9;border:0;border-radius:8px;"
></iframe>

*The developer's [original Game Boy-on-e-paper demonstration](https://www.youtube.com/watch?v=XiZmM6hwwAU). If the embedded player is blocked, the link opens the video on YouTube.*

InkBoy offers two distinct looks. **Fast dithered black-and-white** uses a fixed 4 × 4 Bayer pattern to represent the original Game Boy's four tones with black and white pixels. **Fast four-shade grayscale** instead applies carefully measured partial pulses, stopping the particles between their black and white endpoints. There are twelve nontrivial shade-to-shade transitions, and they do not all need the same pulse count. That gives a smoother image, but also makes trails and accumulated ghosting harder to control.

The hardware is a **Waveshare ESP32-S3-ePaper-1.54 V2** board with a built-in microSD slot and speaker. A separate, custom **ESP32-C3 controller** connects over BLE or a USB-C data cable. Generic Bluetooth HID and USB gamepads are not currently supported. The firmware runs original monochrome Game Boy games and dual-mode cartridges in DMG mode, with some cartridge and ROM-size restrictions; it is not a Game Boy Color emulator. The repository includes a freely licensed sample game, not a bundle of commercial ROMs.

One warning deserves more attention than the frame-rate number: these are **experimental drive waveforms**. The maintainer explicitly cautions that sustained high-speed operation may cause permanent image retention or panel damage, and long-term lifetime has not been validated. This is an ingenious demonstration of what careful waveform control can extract from a familiar e-paper module—not a general claim that e-paper panels can safely refresh at 30 fps.

**Further reading:** [InkBoy source and build instructions](https://github.com/kuslota/InkBoy) · [Per-pixel drive explanation](https://github.com/kuslota/InkBoy/blob/main/docs/how-it-works.md) · [Hackaday's original report](https://hackaday.com/2026/10/14/tiny-e-paper-display-delivers-30-fps-of-game-boy-fun/).

