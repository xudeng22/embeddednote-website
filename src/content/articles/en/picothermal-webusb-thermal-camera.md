---
title: 'Picothermal: A Practical USB-C Thermal Camera, No App Required'
description: Picothermal combines a FLIR Lepton 3.5 and RP2040 in a browser-controlled USB-C thermal camera, with open hardware, KiCad schematics and Rust firmware.
locale: en
translationKey: picothermal-webusb-thermal-camera
pubDate: '2026-10-23'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/icamaster/picothermal
tags:
- Picothermal
- WebUSB
- FLIR Lepton 3.5
- RP2040
- Thermal Imaging
- Rust
- Open Source Hardware
seoTitle: 'Picothermal: Open-Source USB-C Thermal Camera with WebUSB'
seoDescription: Explore Picothermal, a practical RP2040 and FLIR Lepton 3.5 thermal camera with browser-based WebUSB, open KiCad hardware and Rust firmware.
---

A thermal camera is useful when a spot thermometer cannot tell the whole story. It can reveal an overheating component on a PCB, a warm connector, or a temperature difference across a wall. Clip-on thermal cameras already exist, but many depend on a companion app that the manufacturer must continue to maintain. Cezar Chirila's **Picothermal** takes a different approach: connect a small USB-C camera board to a compatible phone or computer, open a browser that supports WebUSB, and view the thermal image without installing a dedicated app.

[Picothermal hardware and design files](https://github.com/icamaster/picothermal) · [Rust firmware](https://github.com/icamaster/picothermal-fw)

The design combines a **FLIR Lepton 3.5** radiometric infrared module with a **Raspberry Pi RP2040** microcontroller. The sensor produces 160 × 120 thermal pixels—19,200 temperature samples per frame—with a nominal 57° horizontal field of view. FLIR specifies a scene temperature range of **−10°C to 140°C in high-gain mode**, extending to **−10°C to 400°C in low-gain mode** at room temperature. Its typical operating power is **150 mW for the Lepton module**, not the complete camera board. The commercial Lepton 3.5 is also limited to roughly **8.6 frames per second**. Temperature readings still depend on the measurement conditions and surface emissivity.

![Picothermal USB-C thermal camera PCB with FLIR Lepton sensor and RP2040](/uploads/picothermal/picothermal-cover.webp)

*Picothermal puts the thermal sensor, controller and USB-C connection on a single compact PCB. Image: Cezar Chirila.*

![Picothermal browser WebUSB interface showing a thermal image of a hand](/uploads/picothermal/picothermal-webusb.png)

*The WebUSB interface displays the radiometric image, a colour scale and camera controls without a companion app.*

Chirila had already built a thermal camera around the **Melexis MLX90640**, whose 32 × 24 array contains 768 sensing elements. The Lepton 3.5 raises that to 19,200 pixels, or **25 times as many**. More thermal pixels make it easier to distinguish nearby objects and identify where heat is concentrated. The newer board drops the dedicated display, battery and storage entirely: the phone or PC supplies power, runs the interface and shows the image, while the RP2040 moves sensor data over USB.

The hardware files are available under the MIT licence. The repository includes the **KiCad project, schematic PDF, Gerbers, BOM, assembly drawing and enclosure STL files**. On the PCB, USB enters through a **USB4155-03-C** Type-C connector, with an **ESD3C3.3ST5G** protection device and **MPZ1608S101ATA0** ferrite bead. The RP2040 boots from a **W25Q16JV 16-Mbit external QSPI flash**. The Lepton has a dedicated **25 MHz ECS-2520MV-250-CL oscillator**, and a **Tag-Connect TC2030-CTX** footprint provides SWD access.

The power schematic is worth studying if you are designing a small USB-powered peripheral with several supply rails. The incoming 5 V feeds two **TLV62569A buck regulators**, producing 3.0 V and 1.2 V rails rated at 1 A, along with two **AP7330 LDOs** producing 3.3 V and 2.8 V rails rated at 300 mA. Test points make the supplies accessible during bring-up. Chirila tried **0.8 mm and 1.6 mm PCBs**, then used the thicker board because it was easier to handle and solder. The printed enclosure has matching base variants for both thicknesses.

![Picothermal schematic with RP2040 USB-C connector QSPI flash and FLIR Lepton interface](/uploads/picothermal/picothermal-schematic-main.png)

*The main schematic brings together USB-C, RP2040, external flash and the Lepton module.*

![Picothermal power schematic with two buck regulators and two LDOs](/uploads/picothermal/picothermal-schematic-power.png)

*The USB 5 V input supplies two buck converters and two LDO-regulated rails.*

![Picothermal assembly drawing and PCB component placement](/uploads/picothermal/picothermal-assembly.png)

*The assembly drawing and manufacturing files are available in the hardware repository.*

The firmware lives in a [separate repository](https://github.com/icamaster/picothermal-fw). It is written in **Rust using Embassy**, after an earlier plan to use C and TinyUSB was abandoned. Chirila openly notes that much of the working firmware was produced with coding agents and may be difficult to maintain. That caveat matters for anyone planning to fork the project: working hardware is not the same thing as a mature, well-maintained firmware stack.

The software separates the sensor driver and USB protocol into a host-testable **`no_std` core**. Lepton control commands use the **CCI interface over I²C**, while thermal frames arrive over **VoSPI (Video over SPI)**. The RP2040 firmware can be built as a **UF2 image** and copied through its USB bootloader; **probe-rs** supports SWD debugging, and **defmt over RTT** handles logs. There is deliberately no USB serial console, leaving the USB connection available for thermal data.

The browser interface is the project's main practical feature. On Windows, **Microsoft OS 2.0 descriptors** let the device bind to **WinUSB** without a separate driver installer. The author reports testing **Edge on Windows** and **Chrome on Android**; other Chromium-based browsers are expected to work. A Linux host may need a **udev rule** before an ordinary user can claim the device. **Firefox and Safari do not implement WebUSB**, and the project's current browser approach does not work on iPhone or iPad. You can try the [Picothermal WebUSB interface](https://www.cezarchirila.com/webusb/picothermal.html) with compatible hardware and a supported browser.

Builders also need to pay attention to USB identification. The prototype firmware uses **VID 0x1209 / PID 0x0001**, a shared **pid.codes test ID**. Those identifiers are not suitable for distributing multiple independent products; a separately assigned PID is needed before sharing or selling boards. The author has mentioned **USB Video Class (UVC)** as a possible future addition, but the published firmware currently uses WebUSB, not UVC.

For engineers working on WebUSB peripherals, the useful details are the USB descriptors, the browser-to-device protocol, and the separation between Lepton frame capture and the web interface. Picothermal shows how far a small RP2040-based instrument can go without its own display or mobile app—provided the browser compatibility limits suit the application.

**Project links:** [Hardware, KiCad and enclosure](https://github.com/icamaster/picothermal) · [Firmware and build instructions](https://github.com/icamaster/picothermal-fw) · [WebUSB app](https://www.cezarchirila.com/webusb/picothermal.html) · [FLIR Lepton 3.5 specifications](https://oem.flir.com/en-150/products/lepton/?model=500-0771-01&segment=oem&vertical=microcam).
