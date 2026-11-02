---
locale: en
translationKey: tinytron-esp32-mini-tv
pubDate: '2026-01-15'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/t0mg/tinytron
title: 'Tinytron: A Tiny ESP32 Television You Can Build for Under €30'
description: Tinytron turns a Waveshare ESP32-S3 board into a retro miniature TV with MJPEG playback, browser streaming and a fast 3D-printed case.
tags:
- tinytron
- ESP32-S3
- Waveshare
- MJPEG
- Retro TV
- 3D Printing
- Open Source
seoTitle: 'Tinytron: Build a Tiny ESP32-S3 TV for Under €30'
seoDescription: 'Inside tinytron: Waveshare ESP32-S3-LCD-1.69, MJPEG on microSD, Wi-Fi video streaming, 3D-printed enclosure, browser flasher and wiring
  caveats.'
---

Most ESP32-S3 boards end up as weather stations, clocks or photo frames. Tom G.'s **tinytron** takes a different route: it turns Waveshare's ESP32-S3-LCD-1.69 into a miniature television, complete with a 3D-printed case modeled after late-1990s TV/VCR combos. It plays actual video, even if the screen is barely larger than a postage stamp.

The [GitHub repository](https://github.com/t0mg/tinytron) has the firmware and printable case files, along with a [video demonstration](https://www.youtube.com/watch?v=HspYfg55T3A).

![Tinytron ESP32-S3 miniature retro television](/uploads/tinytron/tinytron-cover.webp)

*Tinytron packages the Waveshare display board in a four-piece, 3D-printed TV enclosure.*

There are two playback paths. Insert a FAT32-formatted microSD card with MJPEG-encoded AVI files or JPEGs in its root directory and tinytron starts playing them alphabetically—videos first, then images. Without a card, it switches to Wi-Fi mode so a desktop browser can stream local video. Screen and window mirroring are also implemented, although that mode comes with a browser-security caveat.

![Tinytron running an animated video from microSD](/uploads/tinytron/tinytron-01.gif)

*SD-card playback of Blender Studio's short film WING IT!.*

The base board is the **non-touch Waveshare ESP32-S3-LCD-1.69**, with a **1.69-inch 240 × 280 ST7789V2 display**. Despite the size, the controls go beyond a basic frame player: battery operation, a Wi-Fi setup page, OTA updates, brightness and on-screen display settings, and a configurable automatic shutdown timer. Everything on the device itself uses one button. A short press pauses or resumes playback, a double press advances to the next file, and a long press powers the unit on or off. There is deliberately **no audio playback**; the design has neither an amplifier nor a speaker.

![Side view of the printed Tinytron enclosure](/uploads/tinytron/tinytron-02.jpeg)

*The display snaps into the front section of the printed shell.*

The proposed build uses just three main components: the Waveshare board, an SPI microSD breakout and a **3.7 V, 400 mAh LiPo battery**. You can omit the card for Wi-Fi playback or initially power the board over USB-C. The author's **under-€30 target** refers to the principal DIY parts, not a guaranteed delivered price after shipping, printing and labor. The SD breakout requires a six-pin header. One easy-to-miss detail is the battery connector: a typical PH2.0 lead does not fit the board's **JST 1.25 mm** connector, so check it before ordering.

The enclosure borrows its proportions from sets such as Sony's KV-14V6D. Designed in Onshape, it comprises a front shell, rear shell, bezel and button. The author's PLA test print took about 30 minutes and 16 g of filament on a Prusa MK4S at 0.28 mm layer height. The bezel is glued to the front; the rest uses close-fitting snap joints. The tolerances make assembly quick but unforgiving. Flex the printed shell when seating the display, not the glass, and check that the battery is clear before closing the back.

![Tinytron 3D case rendering](/uploads/tinytron/tinytron-03.png)

![Tinytron exploded case with its four parts](/uploads/tinytron/tinytron-04.png)

*The four printed pieces are designed to assemble without screws.*

![Tinytron PrusaSlicer arrangement](/uploads/tinytron/tinytron-05.png)

![Support locations for Tinytron 3D printed enclosure](/uploads/tinytron/tinytron-06.png)

*Selected features need painted-on supports, marked green in the slicer images. The author also provides an [uncut assembly video](https://www.youtube.com/watch?v=-QKKTKMmSjw).*

The microSD reader connects over SPI. Tinytron reuses the breakout cable supplied with the development board, keeping six conductors for 3.3 V, chip select, MOSI, clock, MISO and ground. The default firmware maps these to **GPIO10 (CS), GPIO17 (MOSI), GPIO11 (CLK) and GPIO18 (MISO)**. You can remove and rearrange the crimped wires instead of cutting them, but verify the connector orientation carefully: reversing the makeshift plug swaps power and ground and can damage the board. The repository's wiring table and `platformio.ini` are the references to follow.

With no card inserted, tinytron attempts to rejoin the saved Wi-Fi network. If that fails, it starts an open access point named `Tinytron-XXXX`; the configuration page is available at `192.168.4.1`. Once connected, its browser interface can stream video, display battery status, adjust brightness and OSD settings, set automatic shutdown and upload OTA firmware. The project also offers browser-based initial flashing and local video conversion, so a full development toolchain is optional for a straightforward build.

![Tinytron browser video streaming interface](/uploads/tinytron/tinytron-07.png)

![Tinytron Wi-Fi and display settings interface](/uploads/tinytron/tinytron-08.png)

*The web interface is styled after a VCR on-screen display.*

For offline playback, the output must be **MJPEG in an AVI container**. The browser transcoder uses `ffmpeg.wasm` locally and advertises a 2 GB output limit. Its sample FFmpeg pipeline removes audio and generates 25 fps frames cropped to **288 × 240**. The extra width is an encoder/decoder alignment choice; it is not the display's native resolution. The source video stays on the user's computer during conversion.

Screen mirroring is the awkward part. Browser capture APIs normally require secure origins, while tinytron's stream endpoint is HTTP/WebSocket without TLS. The documented workaround involves Chrome's *Insecure origins treated as secure* flag on desktop. **That weakens a browser security boundary**, so it is not a setting to enable casually, and the author does not support mobile screen mirroring through that route. There is also a hardware-revision trap: the code targets Waveshare's **V2** board, using GPIO41/40 for `SYS_EN`/`SYS_OUT`; a **V1** board requires GPIO35/36 in `platformio.ini`. The device cannot currently be switched off while charging.

The project is released under the **MIT License** and builds on ideas from atomic14's `esp32-tv` and moononournation's `MiniTV`, using libraries including TFT_eSPI, JPEGDEC, ArduinoJson and ESPAsyncWebServer. The best place to start is the [repository](https://github.com/t0mg/tinytron), particularly its wiring table, web flasher and [three-minute assembly video](https://www.youtube.com/watch?v=-QKKTKMmSjw).
