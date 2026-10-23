---
title: 'OpenHRStrap: A Practical Open-Source ECG Chest Strap with ESP32'
description: OpenHRStrap pairs an ESP32-S3 with the AD8232 ECG front end and a BLE heart-rate service. Explore the hardware, Pan–Tompkins pipeline and real running-test limitations.
locale: en
translationKey: openhrstrap-esp32-ecg-chest-strap
pubDate: '2026-10-23'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/MilosRasic98/OpenHRStrap
tags:
- OpenHRStrap
- ESP32-S3
- AD8232
- ECG
- Pan-Tompkins
- BLE Heart Rate
- Open Source
seoTitle: 'OpenHRStrap: Practical ESP32 ECG Chest Strap with BLE'
seoDescription: OpenHRStrap pairs an ESP32-S3 with the AD8232 ECG front end and a BLE heart-rate service. Explore the hardware, Pan–Tompkins pipeline and real running-test limitations.
---

A commercial ECG chest strap is useful for training, but it gives you little room to inspect the signal-processing chain or change the firmware. **OpenHRStrap** takes the DIY route: an ESP32-S3 reads an AD8232 ECG front end, detects cardiac peaks, and reports a heart-rate value over Bluetooth Low Energy (BLE). The hardware files, code, signal plots and test results are available on GitHub.

The design is a hobby prototype, not a medical monitor. Its most useful feature for embedded developers is the visibility it gives you into everything between an electrode and a BLE heart-rate notification—including the parts that did not work reliably during exercise.

**Project:** [OpenHRStrap on GitHub](https://github.com/MilosRasic98/OpenHRStrap) · **License:** MIT

## A chest strap built from accessible modules

For V1, creator Milos Rasic used a **Seeed Studio XIAO ESP32-S3** and an **AD8232 ECG breakout** rather than designing a custom analog board. The AD8232 conditions the small voltage signals picked up by the chest electrodes; the ESP32-S3 handles sampling, processing and BLE. A reference electrode was added by sewing an extra snap fastener to the strap.

Power comes from a single-cell lithium-ion battery through a small **5 V boost module**, while the XIAO board handles its own supply regulation. The enclosure combines 3D-printed PLA and TPU parts. This is a practical setup for reproducing the prototype with common modules, although electrode contact, motion artifacts and safe battery construction still need attention.

![OpenHRStrap DIY ECG chest-strap prototype](/uploads/openhrstrap/openhrstrap-cover.webp)

*The first OpenHRStrap prototype in a 3D-printed enclosure.*

![OpenHRStrap V1 wiring schematic with AD8232 and ESP32-S3](/uploads/openhrstrap/openhrstrap-02.png)

*V1 wiring schematic showing the battery, 5 V boost module, AD8232 and XIAO ESP32-S3.*

![OpenHRStrap chest strap device concept and electrode placement](/uploads/openhrstrap/openhrstrap-03.png)

*The hardware sketch shows the electronics and electrode placement on the chest strap.*

## Pan–Tompkins, from ECG samples to R peaks

The signal-processing work follows the **Pan–Tompkins QRS detection method**, published by Jiapu Pan and Willis J. Tompkins in 1985. Its filter chain consists of band-pass filtering (low-pass followed by high-pass), differentiation, squaring and moving-window integration. Each stage has a purpose: suppress baseline wander and out-of-band noise, emphasize the steep QRS slope, then produce an integrated envelope suitable for peak detection.

The detector evaluates two related signals. **FILT** contains peaks from the band-pass-filtered ECG; **INT** contains peaks from the integrated signal. Running estimates of signal and noise peaks (**SPK** and **NPK**) adjust the detection thresholds (**TH1** and **TH2**). An INT candidate must have a corresponding peak on the filtered signal before the algorithm accepts it as a beat. If the interval since the last accepted beat exceeds roughly **1.66 times the average RR interval**, the search-back procedure uses a lower threshold to look for a missed beat.

Rasic documents the processing chain in a Python notebook and supplies the source data and diagrams. The ESP32 Arduino code also contains a real-time, Pan–Tompkins-inspired filtering and detection path, but its implementation details are not identical to the offline Python analysis. The distinction matters when evaluating the plots against what the wearable delivers during a run.

![Hand-drawn Pan–Tompkins QRS detection flowchart](/uploads/openhrstrap/openhrstrap-04.png)

*The author’s drawing covers the filter chain, adaptive thresholds and search-back logic.*

## What the recorded ECG shows

The repository includes traces at several points in the pipeline. After band-pass filtering, much of the low-frequency baseline movement is removed. The derivative and squaring stages emphasize QRS-like transitions, and the moving-window integrator makes candidate events easier to classify. Those intermediate plots are useful if you want to port or tune the detector rather than treat it as a black box.

On one **80-plus-second prerecorded ECG dataset**, the author reports about **one missed R peak**. The first ten seconds were reserved for initializing detector parameters. That is a promising result for the particular static recording; it is not an accuracy figure for running or other motion-heavy conditions.

![Raw ECG trace recorded by OpenHRStrap](/uploads/openhrstrap/openhrstrap-05.png)

*The full recorded ECG trace before digital filtering.*

![Band-pass filtered ECG waveform](/uploads/openhrstrap/openhrstrap-06.png)

*Band-pass filtering reduces baseline drift and unwanted frequency components.*

![Moving-window integration output for QRS detection](/uploads/openhrstrap/openhrstrap-07.png)

*The moving-window integrator produces a smoother envelope for peak detection.*

![R-peak detection over the integrated ECG signal](/uploads/openhrstrap/openhrstrap-08.png)

*Detected peaks and adaptive threshold estimates on the integrated signal.*

## A 5 km run exposes the hard part

To test V1 outside the bench, Rasic completed a **5 km run** while wearing the DIY strap and a PPG-based smartwatch. He exported the activity data from Strava and compared the two heart-rate series using Python. The readings were close at the start, but diverged as his heart rate rose. The DIY unit generally reported lower values than the watch, although the two sometimes converged again as his pace changed.

The smartwatch is a comparison device, not a clinical reference, so the plots cannot establish which reading was correct at every moment. More importantly, **V1 did not log the underlying ECG and detection state during the run**. Without that evidence, it is difficult to separate electrode movement, analog noise and missed or incorrectly accepted beats. The author identifies proper data logging as one of the main goals for V2, alongside a custom PCB and a revised analog front end.

![Five-kilometre run: DIY ECG chest strap versus PPG smartwatch](/uploads/openhrstrap/openhrstrap-09.png)

*The author compares heart-rate readings from the DIY strap and a PPG watch over a 5 km run.*

![Heart-rate data recorded by the ESP32 DIY chest strap](/uploads/openhrstrap/openhrstrap-10.png)

*The complete heart-rate series recorded by the ESP32-based prototype.*

## BLE support and the next revision

The ESP32 firmware advertises the standard **Bluetooth Heart Rate Service (0x180D)** and sends measurements through characteristic **0x2A37**. That is a better starting point than a custom phone protocol, but it does **not** mean that every sports app will accept the device. Compatibility still depends on each app's external-sensor support. The project documentation describes using Strava data for analysis; it should not be read as universal compatibility testing for Garmin Connect or other apps.

The project's November 2025 update describes a simpler, module-based build and continuing work on real-time detection while running. The planned V2 would add dedicated hardware and signal logging to make those failures measurable rather than speculative.

For anyone interested in ECG acquisition, adaptive peak detection or a BLE sensor built from off-the-shelf modules, OpenHRStrap provides a useful starting point: a circuit, source code, processing notebooks, plots and a field test that shows both progress and unresolved problems.

**Safety and scope:** OpenHRStrap is an educational prototype. It is not a certified medical device and must not be used for diagnosis or health-critical monitoring.

**Sources:** [OpenHRStrap hardware, firmware and test data](https://github.com/MilosRasic98/OpenHRStrap) · [Original Pan–Tompkins paper](https://www.robots.ox.ac.uk/~gari/teaching/cdt/A3/readings/ECG/Pan+Tompkins.pdf).
