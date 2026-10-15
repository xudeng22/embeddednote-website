---
title: 'KENSAT: An Open-Source 2U CubeSat Designed to Run TinyLlama on a Jetson Orin Nano'
description: KENSAT combines a PIC24 flight controller, Jetson Orin Nano and TinyLlama in an open-source 2U CubeSat design with UHF downlink and fault recovery.
locale: en
translationKey: kensat-2u-cubesat-llm
pubDate: '2026-07-02'
category: hardware
tags:
- CubeSat
- Jetson Orin Nano
- TinyLlama
- UHF
draft: false
seoTitle: 'KENSAT: 2U CubeSat with Jetson and TinyLlama'
seoDescription: KENSAT combines a PIC24 flight controller, Jetson Orin Nano and TinyLlama in an open-source 2U CubeSat design with UHF downlink and fault recovery.
---

KENSAT isn't another ESP32-and-display experiment or a Raspberry Pi camera build. It's a 2U CubeSat project from Ken Chan, designed around a Jetson Orin Nano running a quantized TinyLlama model. The idea is to perform language-model inference onboard the satellite and send the resulting text back over UHF radio.

The repository goes well beyond a concept drawing. It includes the onboard computer (OBC), radio board, electrical power system (EPS), burn-wire antenna release circuitry, Jetson daemon, ADALM-Pluto ground-station scripts, and KiCad schematics and board layouts.

![kensat 2u cubesat llm — figure 1](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-01.webp)

**GitHub:** https://github.com/kenchangh/kensat  
**Project website:** https://www.kensat.com/

![kensat 2u cubesat llm — figure 2](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-02.webp)

What sounds like a science-fiction premise turns into a collection of very concrete embedded-systems problems: how to control power, recover from a Linux crash, match the RF network, release an antenna after deployment, downlink an inference result, and restart the spacecraft if its main controller fails.

## Key hardware

| Subsystem | Main hardware | Role |
| --- | --- | --- |
| OBC | PIC24FJ256GB210 + Pumpkin PPM D1 | Always-on control of telemetry, radio, power, Jetson, and state machine |
| AI payload | Jetson Orin Nano 8GB + TinyLlama 1.1B Q4_K_M | Periodic onboard inference and result downlink |
| UHF radio | Si4463 + AS179-92LF | 437.08 MHz telemetry, commands, and model output |
| EPS | 2S2P 18650 cells, telemetry, hardware watchdog | Power delivery and spacecraft reset if the OBC fails |
| Antenna deployment | Tape-measure dipole, fishing line, redundant nichrome wires | Release of the UHF antenna and flash-recorded state |
| Ground station | ADALM-Pluto SDR + AX.25 scripts | Beacon, telemetry, and LLM-output reception |

## Always-on PIC24, normally-off Jetson

KENSAT's stack consists of a Pumpkin motherboard and PPM D1, EPS board, radio board and Jetson payload, topped by the burn-wire deployment board. The boards connect through a 104-pin CubeSat Kit Bus.

![kensat 2u cubesat llm — figure 3](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-03.webp)

The PIC24FJ256GB210 handles spacecraft control, telemetry, Si4463 communication, EPS heartbeat, and Jetson power switching. In many edge-AI prototypes, the Jetson is treated as the main computer. That arrangement is much harder to justify on a small satellite. The Jetson draws substantial power, takes time to boot, and runs Linux, which can hang. A crashed desktop board can be power-cycled by hand; a spacecraft intended for a roughly 520 km sun-synchronous orbit cannot.

The design therefore keeps the PIC24 running while leaving the Jetson off most of the time. Once a day, during the scheduled inference window, the PIC24 asserts IO.16 to enable a +5 V load switch. The Jetson boots, performs its work, returns the result, and shuts down before power is disconnected. The GPU is a task-specific payload; the MCU remains in charge of basic survival.

## Inference protocol: READY, RUN, DONE

The Jetson side uses an NVIDIA Jetson Orin Nano 8GB with JetPack 6 / L4T R36.4.4 and TinyLlama 1.1B quantized as Q4_K_M, run through `llama.cpp`. The PIC24 and Jetson communicate over a modest 9,600-baud, 8N1 UART. That's sufficient because the link carries prompt identifiers and inference text, not images or model weights.

Up to 20 prompts are stored on the Jetson's eMMC. The PIC24 sends an identifier such as `RUN:05`; the Jetson reads `/opt/kensat/prompts/05.txt`, runs inference, and returns `DONE:` followed by its response.

Timeouts enforce recovery. If the Jetson fails to respond with `READY` within 60 seconds, the PIC24 cuts its 5 V power. The same happens if `DONE` isn't returned within 120 seconds. A read-only root filesystem reduces the risk of damage to eMMC data following an abrupt shutdown.

## UHF: Si4463 and AS179

The radio operates at a specified frequency of 437.08 MHz. A Silicon Labs Si4463 handles transmission and reception, while an AS179-92LF RF switch shares a single antenna between TX and RX. Commands, telemetry, and inference results use that same radio path.

![kensat 2u cubesat llm — figure 4](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-04.webp)

The RF architecture is straightforward at the block level, but the implementation is more carefully worked through than simply connecting a transceiver to an antenna. Under `radio/rf-design`, the repository contains `scikit-rf` scripts that optimize matching networks by searching available discrete capacitor and inductor values, taking the parasitics of coplanar waveguide-with-ground traces on two-layer FR4 into account.

![kensat 2u cubesat llm — figure 5](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-05.webp)

ADALM-Pluto-based scripts provide RX/TX testing, frequency sweeps, IQ capture, AX.25 decoding, and end-to-end checks. In other words, the radio board has a corresponding ground-test workflow, not just a schematic.

## Power and thermal design

The language model gets the attention, but power and heat are tougher spacecraft constraints. Jetson inference is estimated at roughly 15–25 W. That may be unremarkable on a bench, but it is significant in a 2U CubeSat. There is no convective cooling in vacuum, so heat must leave through conduction and radiation. KENSAT thermally couples the Jetson to the aluminum structure using pads, turning the frame into a heat path and thermal mass. The system notes put total Jetson power-on time at about 45–90 seconds per run.

The EPS uses a 2S2P pack of 18650 cells. Through I²C telemetry, it reports voltage, current, and temperature to the PIC24. It also implements a hardware watchdog: the PIC24 sends a heartbeat every 60 seconds; if the EPS receives none for 180 seconds, it drops and restores `+5V_SYS` to restart the spacecraft.

## Antenna release

The UHF antenna is a half-wave dipole made from springy tape-measure steel, restrained against the body with fishing line before release. After deployment, the PIC24 waits 120 seconds, then drives IO.24 and IO.25 to heat redundant nichrome burn wires. These sever the line so the antenna springs open.

It is a relatively simple mechanism, but simplicity matters here: fewer motors, gears, and moving parts mean fewer ways to jam. Deployment status is written to flash to prevent repeated firing after success, and retries after a power failure are limited to three.

What makes KENSAT interesting isn't the novelty of Jetson hardware or TinyLlama in isolation. It's the way ordinary components are forced to operate under constraints that don't exist on a desk: tiny energy reserves, limited volume, heat rejection in vacuum, no hands-on maintenance, a slow downlink, and strict fault recovery. Almost every subsystem is designed around one principle: the compute payload must never compromise the rest of the spacecraft.
