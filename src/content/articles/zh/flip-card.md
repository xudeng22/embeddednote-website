---
title: Github 开源项目：RP2350 驱动的 21×22 LED 流体模拟胸牌
description: Nick Johnson 的 flip-card 将 RP2350、21×22 LED 阵列与 Rust/Embassy 固件结合，把 FLIP 流体模拟做进名片尺寸的硬件。
locale: zh
translationKey: flip-card
pubDate: '2025-09-10'
category: open-source
tags:
- GitHub
- RP2350
- LED Matrix
- Embedded Rust
- FLIP
- Embassy
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/Nicholas-L-Johnson/flip-card
seoTitle: RP2350 LED 流体模拟胸牌：flip-card 开源硬件与 Rust 固件
seoDescription: 查看 flip-card 开源项目：RP2350、21×22 LED 矩阵、FLIP 流体模拟、Rust/Embassy 固件、KiCad PCB，以及完整 GIF 动画。
---

一个名片大小的 PCB，正面铺满 21×22 的 LED。拿在手里晃一晃，屏幕上的亮点会像液体一样流动。这是 Nick Johnson 的开源项目 **flip-card**：把流体模拟直接运行在一块采用 Raspberry Pi RP2350 微控制器的随身硬件上。

控制 LED 的不仅是预先录制的动画。作者使用流体隐式粒子（Fluid-Implicit Particle，FLIP）思路来驱动模拟，固件采用 **Rust** 编写，并基于 **Embassy** 异步嵌入式框架实现。这个项目把硬件设计和数值模拟结合在一起，很适合拿来研究 RP2350 上的实时图形与嵌入式 Rust。

## 动画演示

![FLIP 流体模拟动画，93 帧 GIF](/uploads/flip-card/flip-card-01.gif)

![flip-card PCB 与 LED 矩阵实物](/uploads/flip-card/flip-card-02.webp)

项目源码：[Nicholas-L-Johnson/flip-card](https://github.com/Nicholas-L-Johnson/flip-card/)，作者为 Nick Johnson。

仓库中的 **`kicad-pcb`** 目录包含 PCB 设计文件，**`fluid_sim_crate`** 目录是单独的流体模拟模块；RP2350 固件位于 **`flip-card_firmware`**，此外还有用于模拟和调试的 **`sim_display`** WebAssembly 版本。

作者在项目中说明，流体模拟参考了 Matthias Müller 的相关演示，设计灵感还包括 mitxela 的 fluid-simulation pendant。可充电电池及板边 USB-C 接口则借鉴了 cnlohr 的 tiny touch lcd 项目。这样的小板既要处理 LED 阵列，也要考虑供电和机械布局，比单纯点亮 LED 复杂得多。

## 电路与实物

![flip-card 控制及电源原理图](/uploads/flip-card/flip-card-03.webp)

![flip-card LED 阵列原理图](/uploads/flip-card/flip-card-04.webp)

下面是组装后的 PCBA 和板卡细节。

![多块 flip-card 组装后的 PCBA](/uploads/flip-card/flip-card-05.webp)

![flip-card 实物特写](/uploads/flip-card/flip-card-02.webp)

![Nick Johnson 的 flip-card 名片背面](/uploads/flip-card/flip-card-06.webp)

整个项目的 KiCad 工程、Rust 固件及模拟代码都可以从 GitHub 仓库查看。如果正在尝试 Embassy、RP2350 或高密度 LED 阵列，这块会“流动”的名片值得拆开研究。
