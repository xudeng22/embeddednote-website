---
title: Arm Cortex-M 微控制器接下来将走向何方？
description: 结合 Arm、Renesas 与 STMicroelectronics 的产品进展，分析 Cortex-M85、Cortex-A320、Ethos-U85 和边缘 AI 的发展方向。
locale: zh
translationKey: arm-cortex-m-edge-ai-roadmap
pubDate: '2026-08-10'
category: mcu-soc
tags:
- Arm
- Cortex-M85
- Cortex-A320
- Ethos-U85
- 边缘AI
draft: false
seoTitle: Arm Cortex-M 微控制器接下来将走向何方？
seoDescription: 结合 Arm、Renesas 与 STMicroelectronics 的产品进展，分析 Cortex-M85、Cortex-A320、Ethos-U85 和边缘 AI 的发展方向。
author: EmbeddedNote
sourceUrl: https://www.eenewseurope.com/en/what-now-for-the-arm-cortex-m-microcontroller/
---

嵌入式AI时代，Cortex-M性能逼近上限，Arm正以Cortex-A、NPU与RTOS/Linux融合，重塑高性能边缘计算架构。

文章翻译自以下链接，作者 Nick Flaherty

[https://www.eenewseurope.com/en/what-now-for-the-arm-cortex-m-microcontroller/](https://www.eenewseurope.com/en/what-now-for-the-arm-cortex-m-microcontroller/)

Arm Cortex-M85 是微控制器性能的巅峰。但 AI 的演进正在催生新一代加速器，从而改变嵌入式系统中的性能平衡。

Nick Flaherty 与 Arm 边缘计算高级总监 Lionel Belnet 交谈，探讨该公司高性能微控制器以及边缘 AI 加速器的发展方向。

由 Arm 在英国开发的 Ethos-U85 加速器是首款能够运行 AI Transformer 模型的加速器，小型语言模型（SLM）可为低功耗、高性能设备提供语音识别能力。

未来几个月内，预计将有多达十款集成最新嵌入式 AI 加速器的新型微控制器上市，为开发者提供实现 AI 的新方式。

Belnet 表示：“我们凭借 Ethos 赢得了大量机器学习加速器的设计席位，你们将在下个季度看到这些成果。我们的挑战并不在于芯片合作伙伴是否采用，而是在并非针对某一特定应用的市场中。我们正在与合作伙伴合作，展示该器件的全部能力。”

这正在 Cortex-M 微控制器与 Cortex-A 微处理器内核之间形成新的选择平衡：前者采用 Armv8 架构，后者采用 Armv9 架构，用于下一代高性能嵌入式设计。

Renesas Electronics 和 STMicroelectronics 都已有多个采用 Cortex-M85 内核的高性能微控制器系列出货。但下一代器件的架构仍在开发中，而且它可能并不是传统微控制器。相反，它可能会是搭配 Ethos-U85 加速器的 A 类微处理器内核。

Belnet 表示：“我们正在研究下一代内核的概念——这有点敏感。提高 Cortex-M 的性能并不是优先事项。”

“我们所做的是推出 A320，它拥有更大的物理寻址能力，更能够处理 DRAM 等高延迟存储器，具备扩展至多核的能力，并且与现有 Cortex-A 内核兼容。”

A320 于去年发布，是 A 类内核最小的实现。它专门针对边缘 AI 应用而设计，并提供与最新加速器 Ethos-U85 的接口。

![配图：Arm Cortex-M 微控制器接下来将走向何](/uploads/arm-cortex-m-edge-ai-roadmap/arm-cortex-m-edge-ai-roadmap-01.webp)

## Cortex-A320 内核是 Arm 嵌入式战略的核心

增加加速器内核后，即可在边缘侧支持基于 Transformer 的模型，而 Transformer 是较新语言模型和视觉模型的基础。Ethos-U85 可从 128 个 MAC 单元扩展到 2,048 个 MAC 单元，其能效比 Ethos-U55 和 Ethos-U65 内核高 20%，从而支持性能更高的边缘 AI 使用场景。

Ethos-U85 还支持新的 2:4 稀疏度，可针对特定神经网络计算有效地将吞吐量提高一倍。该功能结合其增强的权重压缩能力，有助于显著降低内存占用——最高可降低 70%——从而能够运行更大的网络，或加速现有网络。

所有这些都在推动高性能嵌入式处理采用新的实现方式。

Alif Semiconductor 表示：“由于我们认识到 Ethos-U85 的潜力，因此在该技术发布时，我们成为首批从 Arm 获得其授权的合作伙伴之一。”Alif Semiconductor 将成为首家把 Ethos-U85 加速器推向市场的公司。“Ethos-U85 将扩展我们微控制器处理前沿 AI/ML 工作负载的能力，并提高内存带宽，从而使 ML 模型能够以显著更快的速度运行。”

![配图：Arm Cortex-M 微控制器接下来将走向何](/uploads/arm-cortex-m-edge-ai-roadmap/arm-cortex-m-edge-ai-roadmap-02.webp)

## Alif Semiconductor 正在规划基于 Arm Ethos-U85 加速器的嵌入式微控制器

不过，目前最新 Alif 微控制器的发布时间尚未确定，而且还有另外几款器件正在开发中。

Belnet 表示：“从 IP 可用、芯片可用到实际使用之间存在很长的提前期。Alif Semiconductor 是第一家，而这又会被 OEM 厂商采用。今年以及明年年初，你们会看到 5 到 10 款采用 Ethos-U85 的芯片设计，但其中公开的非常少。我们首先看到的领域是可穿戴设备；这更多是时间进度问题，而不是其他原因。”

这并不仅仅关乎硬件，还包括将 AI 模型移植到加速器。提供与此前 Ethos 内核相同的工具链，意味着开发者能够获得无缝迁移的好处，并利用此前在基于 Arm 的机器学习（ML）工具上的投入。

Belnet 表示：“关于 U85 能运行哪些模型，我们仍然必须与合作伙伴及 OEM 厂商共同研究其能力。我们必须把工具集成到 ML 流程中，同时还有其他举措，目标是从传统模型库出发，降低目标平台的采用难度。这是主要投入方向。”

“模型变化得非常快。我们有一个面向 Ethos 的开源编译器，合作伙伴可以直接将其集成到自己的工具流程和模型库中。Edge Impulse 就是其中一个合作伙伴，它正在把该编译器集成到自己的流程中，从执行过程采集数据来训练模型。”

## 这对下一代微控制器意味着什么？

Renesas Electronics 是高端嵌入式内核 Cortex-M85 的主要合作伙伴，并早在 2025 年 7 月推出了首款微控制器。RA8P1 微控制器系列同样面向 AI 和 ML 应用，搭载此前的 Ethos-U55 内核和一个 250MHz Cortex-M33 内核，同时也面向实时分析。这使其 CPU 性能超过 7,300 CoreMarks，AI 性能在 500MHz 下达到 256 GOPS。

RA8P1 针对边缘和端点 AI 应用进行了优化，在卷积神经网络（CNN）工作负载中使用 Ethos-U55 NPU 将计算密集型操作从 CPU 卸载出去。根据所使用神经网络的不同，Ethos-U55 每秒可完成的推理次数最高可达到单独使用 Cortex-M85 处理器时的 35 倍。

RA8P1 MCU 采用台积电 22nm 超低漏电工艺制造，可在极低功耗下实现高性能。该工艺还支持使用嵌入式磁阻随机存取存储器（MRAM），与 Flash 存储器相比，可获得更快的写入速度以及更高的耐久性和数据保持能力。

针对视觉 AI，该器件包含一个 16 位摄像头接口（CEU），支持最高 500 万像素的传感器，从而支持摄像头和要求较高的视觉 AI 应用。独立的 MIPI CSI-2 接口采用低引脚数量设计，提供两条 Lane，每条最高可达 720Mbps。此外，包括 I2S 和 PDM 在内的多个音频接口支持用于语音 AI 应用的麦克风输入。

该 MCU 包含 2MB SRAM，用于存储中间激活数据或图形帧缓冲区。芯片上还提供 1MB MRAM，用于应用代码以及模型权重或图形资源的存储。对于更大的模型，还提供高速外部存储器接口。针对要求更高的 AI 应用，还提供在单一封装中集成 4MB 或 8MB 外部 Flash 的 SIP 选项。

安全性同样重要。Renesas Security IP（RSIP-E50D）包含多个密码学加速器，并提供硬件信任根以及安全启动功能，其中第一阶段引导加载程序（FSBL）位于不可变存储区域中。支持实时解密（DOTF）的 XSPI 接口允许将加密代码镜像存储在外部 Flash 中，并在其安全传输至 MCU 执行的过程中进行实时解密。

Renesas 又通过 RA8M2 和 RA8D2 独立微控制器产品组扩展了产品范围。这些器件可在 Cortex-M85 旁边增加一个可选的 250MHz Cortex-M33 内核，从而提供 7,300 CoreMarks 的性能，这是 MCU 的行业基准。

RA8M2 器件是通用型器件，而 RA8D2 MCU 则配备高端图形外设，两者均采用 1MB MRAM 存储器。系统级封装版本在单一封装中集成 4MB 或 8MB 外部 Flash，用于要求更高的应用。两者都具有千兆以太网接口以及双端口 TSN 交换机，以满足工业网络使用场景。

针对图像 AI，RA8D2 器件包含高分辨率图形 LCD 控制器以及多种摄像头接口选项，用于摄像头和视觉 AI 应用。

## ST 的 Cortex-M85 微控制器

继 Renesas 之后，STMicroelectronics 也加入进来，推出了 STM32V8 独立处理器，目前该处理器已被 SpaceX 卫星采用。

这款 800MHz 芯片针对 18nm FD-SOI 低功耗工艺技术而设计，由 ST 位于法国 Crolles 的 300mm 晶圆厂制造，同时也与 Samsung Foundry 合作生产。采用嵌入式 PCM 的 FD-SOI 工艺技术在严苛工作环境中提供了很强的稳健性和可靠性，最高结温可达 140°C。相变存储器（PCM）较小的存储单元尺寸，使芯片能够集成 4Mbit 非易失性存储器。

这是 ST 迄今速度最快的 STM32 微控制器，专为严苛工作环境而设计，并能够在工业控制、传感器融合、图像处理和语音控制等嵌入式及边缘 AI 应用中替代体积大得多、功耗也高得多的应用处理器。

该芯片的首个应用是在一套微型激光系统中，用于连接在低地球轨道上以极高速度运行的卫星。它目前刚开始向关键客户出货，更广泛的供应即将开始。

SpaceX Starlink 工程副总裁 Michael Nicolls 表示：“采用 ST STM32V8 微控制器的 Starlink 微型激光系统在太空中的成功部署，标志着推进整个 Starlink 网络高速连接能力的一个重要里程碑。”

“高计算性能，以及大容量嵌入式存储器和数字功能的集成，对于满足我们苛刻的实时处理要求至关重要；同时，得益于 18nm FD-SOI 技术，它还为低地球轨道环境提供了更高水平的可靠性和稳健性。我们期待将 STM32V8 集成到其他产品中，并利用其能力开发下一代先进应用。”

STM32V8 的 3.3V 支持为工业应用带来了多项优势，包括更低的功耗、更好的信号完整性，以及与现代工业通信标准的集成。ST 还集成了专用加速器，包括图形加速器和密码学加速器。

不过，这似乎已经是该架构的性能峰值。Arm 正在研究如何在单个内核上为多个嵌入式应用提供更高性能，并将更多重点放在带有内存管理单元（MMU）以支持 Linux 的 A 类内核上。例如，Arm Cortex-A32 内核在 28nm 工艺下的面积为 0.25mm²，而 A320 内核会比它更小，不过目前尚无准确尺寸。相比之下，采用类似工艺技术的 Cortex-M85 面积为 1.5mm²。

Arm 已经将客户端智能手机内核——如今更名为 C 类——与其边缘 AI 产品区分开来；后者继续沿用 Cortex-A 类品牌和 Armv9 架构。

Belnet 表示：“这里我们谈的并不是消费类产品，因此 Cortex-A 是下一步合乎逻辑的选择。存在一条自然的发展路径，但成本差异非常大。我们正在研究下一代会是什么样。”

“为生态系统提供一个标准化目标是有价值的，这样模型开发者就可以依赖一个主要 MPU 作为目标平台，而我们希望尽可能扩大它在市场中的覆盖范围。这其中包括对 Linux 驱动程序的投入。”

“我们需要了解在资源受限的设备上，实际能够做到什么程度，这就是为什么我们开发了小型 Cortex-A 处理器，它们可以扩展到更大的内存以及效率更高的存储器。”

转向 A 类嵌入式设备也改变了软件开发方式。A 类设备不再必须使用实时操作系统（RTOS），而是可以在 RTOS 与 Linux 之间切换。这样就能够将实时性能与 AI 加速器管理结合起来，而这在纯微控制器上更难实现。

Belnet 表示：“我们正在努力支持 FreeRTOS，并利用 Armv9 的能力实现从实时环境过渡到 Linux 环境；在低功耗状态下运行 RTOS，而在需要时唤醒 Linux。”

随着运行在 Ethos-U85 上的小型语言模型成为这一分析的一部分，而且用户界面转向语音，这一点正变得越来越重要。他表示：“我们已经在 Ethos-U85 上展示了语音识别，因为 AI 正在改变用户界面，因此加入 SLM 绝对是我们正在研究的方向，同时我们也在研究是否支持其他数据类型。”

## 补全 Cortex-M 系列

这并不是说 Cortex-M 系列的开发已经结束。Belnet 提到了 Cortex-M52，它利用 Helium DSP 扩展，使嵌入式设计无需再使用数字信号处理器（DSP）。他说：“仍然有一些领域需要我们加入 Helium。”
