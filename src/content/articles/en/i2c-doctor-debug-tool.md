---
title: 'I²C Doctor: An Open-Hardware Tool for Diagnosing Bus Problems'
description: I²C Doctor is a standalone ESP32-based bus diagnostic tool with a color screen, rise-time measurements, address scanning and practical fault reports.
locale: en
translationKey: i2c-doctor-debug-tool
pubDate: '2026-06-10'
category: tools
tags:
- I2C
- ESP32
- Debugging
- Open Hardware
draft: false
seoTitle: 'I²C Doctor: ESP32-Based Bus Debugging Tool'
seoDescription: 'I²C Doctor uses an ESP32, address scanning, rise-time measurements and switchable pull-ups to help trace wiring and signal-integrity faults.'
author: 'EmbeddedNote'
sourceUrl: 'https://i2c-doctor.com/docs.html#downloads'
updatedDate: '2026-11-06'
---

I²C Doctor is a compact, standalone diagnostic instrument built around a 1.3-inch color TFT display. It can scan, analyze, debug, and test an I²C bus in real time. Rather than requiring you to spend hours interpreting oscilloscope traces, it presents a bus health score from 0 to 100% along with specific suggestions for what to check.

![i2c doctor debug tool — figure 1](/uploads/i2c-doctor-debug-tool/i2c-doctor-debug-tool-01.webp)

**Hardware files:** https://i2c-doctor.com/docs.html#downloads  
**Product listing:** https://www.tindie.com/products/haleng/i2c-doctor-white/

## What it does

**Bus health score (0–100%).** The tool uses measured rise time, pull-up resistance, and signal current to assess bus stability.

**Short-circuit detection.** It checks for shorts between SDA or SCL and ground, between SDA or SCL and VDD, and between SDA and SCL themselves.

**Practical recommendations.** Instead of leaving you to capture signals and calculate rise times manually, I²C Doctor offers plain-language steps to address detected issues.

**Fast address scanning.** It can find connected devices in under two seconds and identify many popular sensors using its onboard database.

**Fault injection and stress tests.** The tool can simulate difficult conditions, such as strong electrical noise, clock stretching, and extra cable capacitance, helping assess a design before production.

**Standalone operation.** With its own screen and USB-C power, it can be used on-site without a connected computer.

<!-- embeddednote-seo-p2:i2c-note:start -->
**A scan isn't a signal-integrity test.** Finding a device address only means something responded. Slow SDA/SCL edges or marginal pull-ups can still cause intermittent errors, especially as bus speed increases. Check the rise-time reading and pull-up setting before blaming the firmware.
<!-- embeddednote-seo-p2:i2c-note:end -->

## Schematic

![i2c doctor debug tool — figure 2](/uploads/i2c-doctor-debug-tool/i2c-doctor-debug-tool-02.webp)

The hardware is based on an ESP32-WROOM-32UE and a 1.3-inch, 240 × 240 color TFT. It measures the physical condition of the I²C bus and presents a health rating rather than requiring users to interpret raw scope or logic-analyzer waveforms. Recommendations might include using a lower pull-up resistance or fixing a detected short.

![i2c doctor debug tool — figure 3](/uploads/i2c-doctor-debug-tool/i2c-doctor-debug-tool-03.webp)

Supported bus speeds range from 10 kHz to 1 MHz. Connector options include Grove/STEMMA, Qwiic, and a standard 2.54 mm header. The SDA and SCL lines have 100 Ω series protection resistors, and onboard DIP switches select pull-ups from 10 kΩ down to 1 kΩ. USB-C supplies power, and the tool supports both 3.3 V and 5 V I²C systems.

During a scan, it measures voltages, checks for shorts, evaluates rise time and current draw, and discovers attached devices. Common sensors can be identified through the database. Measurements are compared against predefined thresholds for different bus speeds, allowing likely signal-integrity problems to be flagged immediately.

![i2c doctor debug tool — figure 4](/uploads/i2c-doctor-debug-tool/i2c-doctor-debug-tool-04.webp)

The price is less appealing than the feature list: the article lists I²C Doctor at $59.

<!-- embeddednote-seo-p2:internal-links:start -->
For a different kind of open-hardware bench instrument, [ArbWave30](/en/articles/arbwave30-waveform-generator/) covers an FPGA-based 30 MHz waveform generator rather than a bus fault finder.
<!-- embeddednote-seo-p2:internal-links:end -->

<!-- embeddednote-p0-20261106:start -->

## Engineering check: turn a bus-health score into a testable hypothesis

A score is convenient for triage, but a physical bus needs measurable timing margins. As a first approximation, the **30–70% rise time** of an RC pull-up is `t_r ≈ 0.8473 × R_pull-up × C_bus`. For a *hypothetical* 4.7 kΩ effective pull-up and 200 pF bus capacitance, this gives **approximately 796 ns**. That is within the **1,000 ns Standard-mode** limit but exceeds the **300 ns Fast-mode** rise-time limit in NXP's [UM10204 I²C-bus specification](https://www.nxp.com/docs/en/user-guide/UM10204.pdf). This is a design calculation, not a measurement made with I²C Doctor.

Before changing components, check the actual operating voltage, whether multiple board pull-ups are in parallel, the aggregate cable/device capacitance, and the sink-current capability of the lowest-power attached IC. Lowering resistance improves rising edges but increases the current every device must sink when pulling LOW. A nominal 3.3 V bus with 1 kΩ pull-up, for instance, implies approximately 3.3 mA through the resistor at an ideal 0 V LOW level, excluding additional pull-ups. Verify electrical limits before enabling the tool's selectable pull-ups.

**Repeatable verification plan:** save SCL/SDA waveforms, measure 30–70% rise time at the farthest device, record clock frequency, pull-up state and cable length, then compare scan results at 100 kHz and 400 kHz. An address scan alone cannot prove that sustained transactions or clock stretching are reliable. The original article describes the vendor's stated features; the arithmetic above is an independent engineering check, not a product certification.
<!-- embeddednote-p0-20261106:end -->
