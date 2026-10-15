---
title: 'ArbWave30: An Open-Source 30 MHz Arbitrary Waveform Generator'
description: ArbWave30 is an open-source 30 MHz signal generator built around a Gowin FPGA, 16-bit DAC, SCPI control and a thoroughly documented analog output path.
locale: en
translationKey: arbwave30-waveform-generator
pubDate: '2026-09-14'
category: open-source
tags:
- FPGA
- Arbitrary Waveform Generator
- DAC
- SCPI
draft: false
seoTitle: 'ArbWave30: Open-Source 30 MHz Waveform Generator'
seoDescription: ArbWave30 is an open-source 30 MHz signal generator built around a Gowin FPGA, 16-bit DAC, SCPI control and a thoroughly documented analog output path.
---

ArbWave30 is an open-source instrument project aiming to build a 30 MHz arbitrary waveform generator.

**GitHub:** https://github.com/EERNINUO/ArbWave30

This is more involved than connecting a DDS module to a connector and calling it a signal source. The design separates high-speed DDS and DAC timing in the FPGA from USB communications and SCPI (Standard Commands for Programmable Instruments) in the MCU. After the DAC come reconstruction filtering, differential-to-single-ended conversion, attenuation, and an output amplifier. The repository contains code, architecture notes, specifications, KiCad schematics, simulations, measured waveforms, a user manual, and an SCPI reference.

![arbwave30 waveform generator — figure 1](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-01.webp)

ArbWave30 is currently a single-channel source supporting sine, square, triangle, noise, and DC outputs. Target specifications include sine waves up to 30 MHz and square waves up to 5 MHz. Into a high-impedance load, the stated amplitude limits are 20 Vpp from DC to 10 MHz, 14 Vpp from 10 to 20 MHz, and 10 Vpp from 20 to 30 MHz. The nominal output impedance is 50 Ω. An internal 10 MHz TCXO provides the reference, with an external 10 MHz reference input planned.

The project is at the minimum viable prototype (MVP) tuning stage. PCBs have been fabricated, the core MCU and FPGA firmware has been validated, and the output can be controlled using SCPI, while the analog front end remains under adjustment. From a 10 MHz sine-wave FFT captured on an oscilloscope, the author estimates THD at approximately −60.2 dBc and SFDR at 63.26 dBc. Those are preliminary estimates: harmonics from the oscilloscope itself may affect the result, and a spectrum analyzer is needed for confirmation.

![arbwave30 waveform generator — figure 2](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-02.webp)

![arbwave30 waveform generator — figure 3](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-03.webp)

The hardware is split into a control board and an analog board. The control board uses an STM32F411CEU6 for USB communication, SCPI parsing, parameter updates, EEPROM settings, and debugging. USB CDC is implemented now; USBTMC is noted as a possible future interface. It also converts a 24 V input into rails for the analog board, including +17 V, −17 V, +7 V, −7 V, and digital 3.3 V.

![arbwave30 waveform generator — figure 4](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-04.webp)

The analog board holds the more demanding parts of the design. A Gowin GW2A/GW2AR-LV18 FPGA in LQFP-144 implements DDS, waveform ROM/RAM, amplitude and phase controls, parallel DAC timing, and analog-front-end controls. The DDS core uses a 48-bit phase accumulator for fine frequency resolution. The selected AD9747 is a dual-channel, 16-bit DAC rated to 250 MSPS. The current design uses one channel at a 150 MSPS sample rate.

![arbwave30 waveform generator — figure 5](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-05.webp)

A CDCI6214 clock generator takes the 10 MHz TCXO reference and delivers 150 MHz LVDS to the DAC, as well as clocks for the FPGA. Clock quality and the analog front end largely determine how clean the output can be. The documents also discuss an RMS jitter target for the CDCI6214, external reference input, and a 10 MHz sync output.

![arbwave30 waveform generator — figure 6](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-06.webp)

The DAC does not drive the output connector directly. Its signal passes through I/V conversion, a seventh-order elliptic low-pass reconstruction filter, differential-to-single-ended conversion, an attenuation network, and an output amplifier. The filter's design cutoff is 60 MHz, with less than 0.5 dB passband ripple and more than 60 dB attenuation at 115 MHz. Those choices favor sine-wave fidelity, but filter group delay affects square-wave edges. The README reports around 13.5% overshoot on a 5 MHz square wave and notes that further channel optimization is needed.

![arbwave30 waveform generator — figure 7](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-07.webp)

The differential-to-single-ended stage is documented in considerable detail. With a 50 Ω input impedance and a gain of 6 V/V, the calculated resistor values are about 560 Ω for feedback and 93.1 Ω at the input. To simplify channel-one routing, the op-amp input and DAC output connections were reversed, requiring the software to invert the data. This is the kind of PCB-level compromise that rarely makes it into a polished product brochure.

![arbwave30 waveform generator — figure 8](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-08.webp)

The planned output stage uses a THS3095, targeting ±10 V into a high-impedance load. The analog board also needs several rails: ±15 V, ±5 V, 3.3 V_A, 1.8 V_A, 1.8 V_D, and 1.0 V_D. Low-noise LDOs such as TPS7A4701 and TPS7A9101 power the DAC, clocking, and analog circuits, while a TPS62933 supplies the FPGA's 1.0 V core. On a signal generator, the power supply is part of the signal path in all but name; many noise problems ultimately trace back to its rails.

![arbwave30 waveform generator — figure 9](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-09.webp)

## Main components

| Function | Part |
| --- | --- |
| MCU | STM32F411CEU6 |
| FPGA | Gowin GW2A/GW2AR-LV18 |
| DAC | AD9747BCPZ |
| Clock generator | CDCI6214 |
| SPI flash | GD25Q32 |
| Differential-to-single-ended amplifier | LMH6609 |
| Output amplifier | THS3095 |
| Common-mode feedback | NE5532 |
| Low-noise analog LDOs | TPS7A4701, TPS7A9101 |
| DC-DC converters | TPS54360, TPS62933 |
| EEPROM | M24C64 |

The useful part of this repository isn't simply the possibility of building another waveform generator. It's how openly the author documents the decisions from system architecture and component selection through clock distribution, power rails, filtering, analog circuitry, SCPI, and test scripts.

It is not yet a finished instrument. The analog front end still needs work, and the measured specifications require better test equipment for confirmation. But that's what makes the project instructive. A 30 MHz signal generator may not sound particularly fast, yet DAC clocking, filter group delay, power-supply noise, amplifier stability, PCB return paths, and output-stage heating all make it a demanding mixed-signal design.
