---
title: What Comes After Cortex-M? Arm, Edge AI and the Shift Toward Cortex-A
description: How Cortex-M85, Cortex-A320 and Ethos-U85 are reshaping embedded AI, with Renesas RA8 and STM32V8 as examples of the next high-performance MCU generation.
locale: en
translationKey: arm-cortex-m-edge-ai-roadmap
pubDate: '2026-08-10'
category: mcu-soc
tags:
- Arm
- Cortex-M85
- Cortex-A320
- Ethos-U85
- Edge AI
draft: false
seoTitle: 'Arm Cortex-M Roadmap: Edge AI, Cortex-A and NPUs'
seoDescription: How Cortex-M85, Cortex-A320 and Ethos-U85 are reshaping embedded AI, with Renesas RA8 and STM32V8 as examples of the next high-performance MCU generation.
author: EmbeddedNote
sourceUrl: https://www.eenewseurope.com/en/what-now-for-the-arm-cortex-m-microcontroller/
---

As edge AI workloads grow, Arm is looking beyond simply pushing Cortex-M clock speeds higher. A mix of Cortex-A processors, dedicated neural accelerators and software stacks that can span an RTOS and Linux is beginning to change how high-performance embedded systems are designed.

*Adapted into Chinese from reporting by Nick Flaherty for eeNews Europe; this English adaptation follows the Chinese source supplied for EmbeddedNote.*

**Original reporting:** https://www.eenewseurope.com/en/what-now-for-the-arm-cortex-m-microcontroller/

The Cortex-M85 sits near the top of Arm's microcontroller performance range. But as AI applications become more demanding, dedicated accelerators are changing the balance between what the CPU should do and what can be offloaded.

In the original interview, eeNews Europe's Nick Flaherty spoke with Lionel Belnet, Arm's senior director of edge computing, about where high-performance MCUs and edge-AI accelerators are heading.

One important part of that strategy is Ethos-U85. Developed by Arm in the UK, the accelerator is designed to handle transformer-based AI models. That opens the door to workloads such as speech recognition using small language models (SLMs) on relatively power-constrained devices.

At the time of the interview, Arm expected several chips featuring its newest embedded AI accelerator to reach the market within the following months—potentially as many as ten designs.

Belnet said Arm had secured numerous design wins for its Ethos machine-learning accelerators, with more announcements expected in the next quarter. Adoption by silicon partners was not the main hurdle, he explained; the harder job was showing how much the technology could do in a market that was not built around one narrow application.

That is creating a new architectural choice for embedded developers: stay with Cortex-M-class microcontrollers or move to smaller Cortex-A-class application processors, with Armv8- and Armv9-generation capabilities shaping the options for the next generation of designs.

Renesas Electronics and STMicroelectronics already have high-performance MCU families based on Cortex-M85. The next step, however, may not look like a conventional microcontroller at all. One possibility is to pair a compact Cortex-A-class processor with an Ethos-U85 accelerator.

Belnet described Arm's next core concepts as work still under discussion. Simply increasing Cortex-M performance, he said, was not the immediate priority.

Instead, he pointed to Cortex-A320: a design with wider physical addressability, better support for higher-latency memories such as DRAM, room to scale to multiple cores and compatibility with existing Cortex-A software.

Introduced the previous year, Cortex-A320 was presented as Arm's smallest A-class implementation. It targets edge-AI systems and can work alongside Ethos-U85.

![Arm Cortex-A320 core architecture diagram](/uploads/arm-cortex-m-edge-ai-roadmap/arm-cortex-m-edge-ai-roadmap-01.webp)

## Why Cortex-A320 matters to Arm's embedded roadmap

Adding a neural accelerator makes it possible to run transformer-based models at the edge, including workloads behind modern language and vision applications. Ethos-U85 can be configured with **128 to 2,048 multiply-accumulate (MAC) units**. Arm says it provides about **20% better energy efficiency** than the earlier Ethos-U55 and Ethos-U65 architectures, supporting more demanding local inference.

Ethos-U85 also supports **2:4 structured sparsity**, which can effectively double throughput for neural-network operations that can use it. Combined with improved weight compression, Arm says the design can cut memory requirements by as much as **70%**, making room for larger models or faster execution of existing ones.

Taken together, those features point toward a different approach to embedded performance: acceleration and memory architecture matter as much as raw CPU frequency.

Alif Semiconductor said it was among the first companies to license Ethos-U85 because it saw the potential for edge AI. The company expected the accelerator to extend the AI/ML workloads its microcontrollers could handle, increase effective memory bandwidth and enable substantially faster model execution.

![Ethos U55 U65 and U85 NPU architecture comparison](/uploads/arm-cortex-m-edge-ai-roadmap/arm-cortex-m-edge-ai-roadmap-02.webp)

## From licensed IP to real silicon

At the time of the source report, Alif had not confirmed the release date for its newest microcontroller. Several additional devices were also in development.

Belnet emphasized that there is a long gap between the availability of processor IP, a finished chip and volume deployment by equipment makers. He anticipated roughly five to ten Ethos-U85-based designs over that year and the following early months, although only a handful had been made public. Wearables were among the first applications under discussion.

The hardware is only part of the job. Developers also need a practical route for getting existing machine-learning models to run on the accelerator. Keeping the toolchain consistent with earlier Ethos products should make migration easier and preserve investments in Arm-oriented ML tooling.

Arm and its partners were still working through which models made sense on U85 and how best to integrate the compiler and runtime into established development pipelines. The goal was to lower the effort required to take a model from a familiar framework onto a specific embedded target.

Belnet also highlighted the pace of model development. Arm's open-source Ethos compiler can be incorporated into partners' workflows, and Edge Impulse was cited as one company integrating that capability into its toolchain.

## What does this mean for the next generation of MCUs?

Renesas has been a prominent partner for Cortex-M85. Its RA8P1 MCU family, introduced in July 2025, targets AI, machine learning and real-time analysis. The device combines a Cortex-M85-class processing approach with an Ethos-U55 neural-processing unit and a **250 MHz Cortex-M33** core. Renesas reported CPU results above **7,300 CoreMark** and AI performance of **256 GOPS at 500 MHz**.

For edge and endpoint AI, RA8P1 uses the Ethos-U55 NPU to take compute-intensive convolutional neural network (CNN) operations away from the main CPU. Depending on the network, Renesas says the accelerator can deliver up to **35 times** as many inferences per second as execution on Cortex-M85 alone.

RA8P1 is built on TSMC's **22 nm ultra-low-leakage** process. Renesas says that combination provides strong performance at low power while supporting embedded magnetoresistive RAM (MRAM), which offers faster writes and improved endurance and data retention compared with conventional flash.

For vision workloads, the family provides a **16-bit camera engine unit (CEU)** supporting image sensors up to **5 megapixels**. A separate two-lane MIPI CSI-2 interface supports up to **720 Mbps per lane**. Audio interfaces, including I²S and PDM, serve microphone-based voice-AI applications.

The MCU includes **2 MB of SRAM** for intermediate inference data or graphics frame buffers and **1 MB of MRAM** for code, model weights or image assets. Larger models can use an external high-speed memory interface, while system-in-package options combine the MCU with **4 MB or 8 MB of flash**.

Security is handled by Renesas Security IP (RSIP-E50D), which incorporates cryptographic accelerators, a hardware root of trust and secure boot. The first-stage bootloader resides in immutable storage. An XSPI interface with on-the-fly decryption (DOTF) allows encrypted images to be held in external flash and decrypted as the MCU reads them for execution.

Renesas expanded the range with the **RA8M2** and **RA8D2** standalone MCU groups. These offer an optional **250 MHz Cortex-M33** alongside Cortex-M85 and target performance in the region of **7,300 CoreMark**.

RA8M2 is aimed at general-purpose applications; RA8D2 adds higher-end graphics peripherals. Both use **1 MB of MRAM**, with system-in-package options providing **4 MB or 8 MB** of external flash. Gigabit Ethernet and a two-port time-sensitive networking (TSN) switch are included for industrial connectivity.

For image-processing and vision-AI designs, RA8D2 adds a high-resolution graphics LCD controller and multiple camera interface options.

## STMicroelectronics and Cortex-M85

STMicroelectronics is pursuing a similar high-performance MCU path with **STM32V8**, a device the company said had already been adopted for use on SpaceX satellites.

The **800 MHz** device uses an **18 nm FD-SOI** low-power process. Production involves ST's 300 mm fab in Crolles, France, and a partnership with Samsung Foundry. The process integrates phase-change memory (PCM) and is intended for demanding environments, with a stated maximum junction temperature of **140°C**. PCM's compact cells enable **4 Mbit of nonvolatile memory** on the die.

ST described STM32V8 as its fastest STM32 microcontroller to date. The design aims to replace larger, less power-efficient application processors in certain industrial-control, sensor-fusion, image-processing and voice-control workloads.

An early use case was a compact optical communications system for satellites traveling at orbital velocities in low Earth orbit. At the time of the report, the product was beginning to ship to selected customers, with broader availability planned later.

Michael Nicolls, vice president of Starlink engineering at SpaceX, described the deployment of STM32V8-based mini-laser systems in orbit as an important step for high-speed links across the Starlink network.

He pointed to the need for significant compute capacity, integrated nonvolatile memory and digital functions to meet demanding real-time processing requirements. The 18 nm FD-SOI process, he added, was valuable for resilience in low-Earth-orbit conditions, and SpaceX expected to consider STM32V8 for additional applications.

Support for **3.3 V** systems is another attraction in industrial designs, where power efficiency, signal integrity and compatibility with established interfaces matter. ST also incorporates dedicated graphics and cryptographic accelerators.

Still, this level of performance may be approaching the practical ceiling for the current class of MCU. Arm is exploring compact A-class processors with memory management units (MMUs) that can support Linux. As a comparison, the source article cites roughly **0.25 mm²** for a Cortex-A32 core on a 28 nm process and around **1.5 mm²** for Cortex-M85 on a comparable process; it does not provide a verified area figure for Cortex-A320.

Arm has also been distinguishing its smartphone-oriented client cores—now identified as the C-class family—from its edge-AI products, which continue under the Cortex-A name and Armv9 architecture.

Belnet's point was that embedded AI is not primarily a consumer-phone problem. Cortex-A offers a logical development path, although the cost differences remain substantial and Arm is still working out what a future generation should look like.

A standardized processor target could also help the software ecosystem. Model developers would have a more consistent MPU platform to design for, while Arm would invest in broader platform availability and Linux drivers.

That requires understanding what resource-constrained devices can realistically support. Arm's small Cortex-A designs are meant to accommodate larger memory spaces and more efficient memory subsystems without forcing developers into a conventional high-power application processor.

An A-class embedded processor changes the software equation too. Instead of being limited to a conventional MCU and RTOS arrangement, a system could run an RTOS for time-critical functions and Linux when more complex processing or AI accelerator management is needed.

Belnet said Arm was working on FreeRTOS support and ways to use Armv9 capabilities to move between real-time execution and Linux—for example, staying in a low-power RTOS state until there is a reason to wake the Linux environment.

That approach becomes more useful as speech interfaces and small language models spread into embedded products. Arm had already demonstrated speech recognition on Ethos-U85, Belnet said, and was investigating SLM support and additional data types.

## Cortex-M still has room to evolve

This does not mean development of Cortex-M is finished. Belnet pointed to **Cortex-M52**, whose Helium DSP extensions can reduce the need for a separate digital signal processor in certain embedded designs. Arm still sees applications where adding Helium capabilities makes sense.
