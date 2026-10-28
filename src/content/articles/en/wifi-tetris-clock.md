---
title: "ESP32 Tetris Clock: A Practical Wi-Fi LED Matrix Build"
description: Build a Tetris-style Wi-Fi clock with an ESP32 and a 64×32 RGB LED
  matrix. Explore the wiring, ezTime synchronization, animation libraries and
  power requirements.
locale: en
translationKey: wifi-tetris-clock
pubDate: 2026-10-27
category: open-source
tags:
  - ESP32
  - Wi-Fi Clock
  - RGB LED Matrix
  - Tetris Clock
  - PxMatrix
  - HUB75
  - Open Source Hardware
draft: false
seoTitle: "ESP32 Tetris Clock: Wi-Fi Time Sync and 64×32 RGB LED Matrix"
seoDescription: "How Brian Lough’s ESP32 Tetris Clock works: 64×32 RGB LED
  wiring, PxMatrix and TetrisAnimation, ezTime synchronization, power supply and
  build limitations."
---
When a conventional digital clock ticks over to the next minute, its digits simply change. Brian Lough’s **WiFi Tetris Clock** makes an event out of it. Colored tetrominoes fall across a 64×32 RGB LED matrix, settling into the numbers that show the current time. It is an uncomplicated idea with an unusually satisfying result—especially on a display large enough to sit on a desk rather than disappear into a project enclosure.

The build uses a **P3 RGB matrix** with a 3 mm pixel pitch. At 64 columns by 32 rows, the active display area is roughly 192 × 96 mm. You can see the individual LEDs up close, but the clock is easy to read from across a room. The project is by Irish maker and Arduino developer **Brian Lough**, who published the code, wiring references and component choices on GitHub. The original design is also documented on [Hackaday.io](https://hackaday.io/project/168931-wifi-tetris-clock).

![Brian Lough’s ESP32 Tetris clock showing 2:32 PM on a 64×32 RGB LED matrix](/uploads/tetris-clock/tetris-clock-cover.webp)

*The finished display uses falling, colored blocks to form the time.*

![WiFi Tetris Clock video thumbnail showing blocks forming the digits](/uploads/tetris-clock/tetris-clock-01.webp)

*The project’s video thumbnail shows the animation building a 4:30 PM readout.*

![Earlier Tetris clock prototype running on an RGB matrix panel](/uploads/tetris-clock/tetris-clock-02.webp)

*An earlier view of the clock on the workbench.*

![Colorful falling Tetris-shaped blocks on the matrix clock](/uploads/tetris-clock/tetris-clock-04.webp)

*The digits are assembled from the familiar block shapes rather than drawn all at once.*

![Unlit RGB LED matrix panel on a 3D-printed stand](/uploads/tetris-clock/tetris-clock-05.webp)

*A 3D-printed stand turns the matrix panel into a simple desktop clock.*

## The hardware is straightforward; the power supply matters

The core parts are a **TinyPICO or another compatible ESP32 board**, a **64×32 P3 RGB matrix**, wiring for the matrix connector, a suitable 5 V supply, and a stand or enclosure. The author’s repository includes connection diagrams for both TinyPICO and a generic ESP32. There is also a D1 mini/ESP8266 diagram, but the README explicitly warns that the ESP8266 sketch is unstable. For a first build, the ESP32 version is the sensible starting point.

The matrix uses a **HUB75-style connector**. A controller board has to supply the row-address, clock, latch, output-enable and color-data signals while the panel receives power separately. Brian also designed a **TinyPICO Matrix Shield** to reduce the jumper-wire work. The diagrams below are useful because GPIO assignments are not necessarily interchangeable between different ESP32 development boards.

![TinyPICO pin wiring to an RGB LED matrix HUB75 connector](/uploads/tetris-clock/tetris-clock-06.png)

*TinyPICO-to-matrix wiring. The panel input and output connectors are marked PIN and POUT.*

![Generic ESP32 GPIO-to-RGB matrix wiring diagram](/uploads/tetris-clock/tetris-clock-07.png)

*The corresponding wiring for a generic ESP32 board.*

![5 V DC jack breakout and screw-terminal wiring for LED matrix power](/uploads/tetris-clock/tetris-clock-08.webp)

*A DC jack and screw terminals provide a direct power connection to the matrix.*

Power is the detail worth checking before assembly. The project README recommends a **5 V, 8 A supply**, not the 5 V/4 A rating sometimes associated with smaller LED builds. Actual current depends on the panel, brightness and number of illuminated pixels. The supply should be sized for the panel’s worst-case demand, and the wiring and connectors must be rated accordingly. A convenient USB phone charger is not automatically an adequate substitute.

## Wi-Fi keeps time; three libraries make it work

There is **no battery-backed RTC module** in the original build. The ESP32 connects to Wi-Fi and uses the [ezTime](https://github.com/ropg/ezTime) library to synchronize its clock from the network. The firmware sets a named time zone such as `Europe/Dublin`; ezTime handles the corresponding daylight-saving rules. Following a power cycle, the device needs a network connection again to obtain the correct time.

The display code has separate jobs. [PxMatrix](https://github.com/2dom/PxMatrix) handles the LED panel’s scanning and drawing interface, with Adafruit GFX underneath. [TetrisAnimation](https://github.com/toblum/TetrisAnimation), built around its `TetrisMatrixDraw` class, animates the blocks that become digits. The ESP32 sketch brings those pieces together and updates the display as the minutes change. It includes options for **12- or 24-hour time** and whether all digits should animate on each minute change or only the ones whose values changed.

Those are compile-time settings in the original sketch, not a finished mobile configuration app. Altering brightness, animation timing, wiring or panel resolution may require edits to the sketch or the underlying libraries. The provided matrix initialization is for **64×32**; a different panel should not be assumed to work with the same settings.

## A good starting point for RGB matrix projects

Other makers have extended the idea with audio playback and browser-based settings. For example, the separate [Talking Tetris Clock](https://www.instructables.com/Talking-Tetris-Clock/) adds sound and a web interface; those features are **not part of Brian Lough’s original firmware**. Printable stands and alternate controller boards offer more room for customization.

The limitations are mostly practical. At 64×32, the digits look deliberately chunky, and full-color LED matrices demand more current than small OLED or e-paper modules. The original code also dates from an earlier generation of ESP32 libraries, so reproducing it today may involve checking library and Arduino-core compatibility. The repository still marks the ESP8266 variant as problematic.

For an engineer who wants to learn matrix-panel wiring, display scanning and network time synchronization, though, this is a useful build: the result is easy to see, the source is short enough to explore, and the animation makes the difference between correct wiring and a working clock immediately obvious.

**Project:** [WiFi-Tetris-Clock on GitHub](https://github.com/witnessmenow/WiFi-Tetris-Clock) · **License:** MIT · **Related libraries:** [PxMatrix](https://github.com/2dom/PxMatrix), [TetrisAnimation](https://github.com/toblum/TetrisAnimation), [ezTime](https://github.com/ropg/ezTime).