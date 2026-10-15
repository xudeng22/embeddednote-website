---
title: 'A Pocket-Sized Bench Power Supply: 1–20 V, 5 A, and USB-C PD Charging'
description: A portable 1–20 V, 5 A battery-powered bench supply with USB-C PD charging. A detailed look at its schematics, charger, buck-boost output stage and protection.
locale: en
translationKey: pocket-lab-power-supply
pubDate: '2026-09-24'
category: hardware
tags:
- Power Supply
- USB PD
- TPS55289
- Open Hardware
draft: false
seoTitle: 'Pocket Lab Power Supply: 20 V, 5 A and USB-C PD'
seoDescription: A portable 1–20 V, 5 A battery-powered bench supply with USB-C PD charging. A detailed look at its schematics, charger, buck-boost output stage and protection.
---

A bench power supply is indispensable when you're debugging a board, but it isn't much use once you leave the workbench. Field testing, rewiring something in a car, or simply working somewhere else usually means carrying the supply, a power strip, and a handful of test leads. Ben, who goes by BenMakesEverything on GitHub, took another approach: build an adjustable bench supply around a 4S lithium-ion battery pack. The result fits in the palm of your hand and had picked up more than a hundred GitHub stars shortly after it appeared.

![pocket lab power supply — figure 1](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-01.webp)

The enclosure is roughly 10 cm long. On the front are a rotary encoder, an eight-character LED dot-matrix display, USB-C for charging, and a DC output connector. Power comes from a 4S pack of 21700 cells rated at 4,500 mAh, with a battery-management system (BMS). Output voltage is adjustable from 1 to 20 V in 100 mV increments; the current limit runs from 0.1 to 5 A in 50 mA increments. The USB-C port accepts USB Power Delivery input but does not supply power to external devices. You can charge and operate the supply at the same time, provided the load current remains below the charging current.

**GitHub:** https://github.com/BenMakesEverything/Pocket-Lab-Power-Supply

The repository includes schematics, Gerbers, a bill of materials, pick-and-place files, enclosure models, and firmware. Most BOM entries have LCSC part numbers, making it relatively straightforward to source parts for a build. There are two important caveats. First, the board has no built-in BMS; the battery pack must have its own protection circuit. Second, Ben removed a previously recommended battery link after a BMS failure in one of the packs. Battery selection matters. The hardware uses the CERN-OHL-S-2.0 license, which permits commercial use under its reciprocal sharing conditions.

## System architecture

![pocket lab power supply — figure 2](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-02.webp)

USB-C input passes through a PD negotiation controller and a power MOSFET before reaching the charger. The charger manages both battery charging and system power. After a switched P-channel MOSFET, the system rail splits into three branches: two DC-DC converters generate 3.3 V and 5 V, while a buck-boost converter produces the user-selected output. An eFuse protects that output, with current sensing ahead of the output connector. A separate, always-on LDO supplies the microcontroller.

## Schematics: seven functional blocks

![pocket lab power supply — figure 3](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-03.webp)

The PD input stage uses a TVS2200 surge suppressor and ESD122 protection. Negotiation is handled by TI's TPS25730, which can request a voltage without MCU intervention: resistor dividers on ADCIN1 and ADCIN2 configure the PD contract, set to 20 V here. Its GATE_VBUS output drives a CSD87501L back-to-back dual N-channel MOSFET. VBUS is connected downstream only after negotiation succeeds.

![pocket lab power supply — figure 4](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-04.webp)

Battery charging and system power are handled by the BQ25792, a buck-boost charger for one to four lithium-ion cells with up to 24 V input, an I²C interface, and NVDC power-path management. That lets the system charge a 16.8 V 4S pack from USB inputs ranging from 5 to 20 V. On the schematic, a 27 kΩ resistor on PROG configures the cell count and default settings. The README warns that this resistor must be changed if the number of series-connected cells changes; otherwise the pack could be overcharged. The system cuts off discharge below 12 V (3 V per cell). A 103AT thermistor on TS monitors temperature. The FDS6679AZ P-channel MOSFET after SYS is controlled by slide switch SW1, which also governs output, charging state, and the display.

![pocket lab power supply — figure 5](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-05.webp)

The adjustable output stage uses a TPS55289 four-switch buck-boost converter. Its output range is 0.8–22 V, with an internal DAC programmable over I²C in 10 mV steps. It also supports current limiting through an external sense resistor; R32 between ISP and ISN is 10 mΩ. The inductor is a 4.7 µH Coilcraft XAL7070, and a 49.9 kΩ resistor on FSW sets the switching frequency. With a battery varying between 12 and 16.8 V and an output reaching 20 V, buck-boost conversion is a natural fit.

![pocket lab power supply — figure 6](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-06.webp)

The firmware converts the requested output voltage in millivolts to a register value, then writes the low and high bytes:

```cpp
int code = constrain((millivolts - 800) / 10, 0, 0x7FF);
writeReg8(tpsAddr, REG_REF_LSB, code & 0xFF);
writeReg8(tpsAddr, REG_REF_MSB, (code >> 8) & 0x07);
```

For the current-limit register, bit 7 enables limiting and the lower seven bits encode 50 mA steps: `0x80 | ((mA + 25) / 50)`. The IC's nominal limits are 22 V and 6.35 A, but the project's FAQ says its compensation network prevents reliable operation at 22 V. The firmware therefore caps the output at 20 V and 5 A, with a recommendation to stay around or below 50 W for prolonged operation.

An eFuse, TPS259474, follows the TPS55289; a 560 Ω resistor on ILM sets its current-limit point. An SMBJ24A TVS and an INA226 monitor follow. The schematic notes that C60 (220 µF) and C62 were added after the video was published to reduce ripple—a useful example of a design being revised after measurement.

![pocket lab power supply — figure 7](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-07.webp)

There are two INA226 current monitors, one on the battery side and one at the output, each with a 10 mΩ 2512-size shunt. The battery-side measurement includes the power consumed by the MCU and display. The firmware also uses current direction to detect charging and shows “Charging” on the display.

![pocket lab power supply — figure 8](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-08.webp)

An ATtiny3216 runs the control firmware, written with Arduino and flashed through UPDI. The display is a Broadcom HCMS-297x-series eight-character, 5×7 LED dot-matrix module on a separate small board. Pressing the PEC12R rotary encoder switches between setting voltage and setting current limit. During operation, the display cycles through battery voltage, actual output voltage, load current, and power. Faults from the TPS55289 appear as `TPS SCP`, `OCP`, or `OVP`.

![pocket lab power supply — figure 9](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-09.webp)

Two Silergy SY8253 regulators provide the auxiliary 3.3 V and 5 V rails; the 5 V rail also powers the TPS55289 VCC pin. A separate low-quiescent-current TPS70933 LDO keeps the MCU powered when the main switch is off.

![pocket lab power supply — figure 10](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-10.webp)

The PCB has four layers, with dedicated internal power and ground planes. Its long, narrow layout follows the enclosure and places the main power path along the board.

![pocket lab power supply — figure 11](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-11.webp)

![pocket lab power supply — figure 12](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-12.webp)

![pocket lab power supply — figure 13](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-13.webp)

![pocket lab power supply — figure 14](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-14.webp)

The 3D-printed enclosure consists of a main shell, front panel, and spacer. Both STL and STEP files are available, and assembly uses M3 heat-set inserts and four screws.

![pocket lab power supply — figure 15](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-15.webp)
