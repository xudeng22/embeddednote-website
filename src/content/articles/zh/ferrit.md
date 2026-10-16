---
title: GitHub 开源 FERRIT：最大 256MB 的 F-RAM 存档设备，目标保存 200 年
description: Machdyne FERRIT 用可更换的 F-RAM 卡、RP2040 控制器和 USB Mass Storage 接口，构建容量最高 256MB 的长期数据存档平台。
locale: zh
translationKey: ferrit
pubDate: '2026-06-15'
category: open-source
tags:
- GitHub
- F-RAM
- FRAM
- RP2040
- Storage
- KiCad
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/machdyne/ferrit
seoTitle: FERRIT 开源 F-RAM 长期存档：256MB、RP2040、200 年目标
seoDescription: Machdyne FERRIT 采用 FERRIT-CY 控制板、FERRIT-M8 存储卡、FERRIT-16 背板，通过 QSPI、RP2040 和 USB MSC 实现模块化长期存档。
---

今天的存储设备动辄以 TB 计算，但 Machdyne 的 **FERRIT** 走的是另一条路线：它把总容量控制在几百 MB，却把长期保存数据作为设计重点。项目采用 **F-RAM（铁电随机存取存储器）**，官方提出了**最长 200 年数据保持**的目标。

需要先纠正原稿标题中的一个数字：FERRIT 的目标上限是 **256MB**，并非 250MB。这样的容量不适合放视频，但保存校准记录、设备证书、历史档案或少量重要文件仍然有实际意义。

![FERRIT 模块化数据存档设备](/uploads/ferrit/ferrit-01.webp)

## 控制板、存储卡与背板分开设计

FERRIT 不是把所有芯片固定焊在一张大板上，而是拆成三类模块：**FERRIT-CY** 控制卡、**FERRIT-M8** 存储卡，以及最多提供 **16 个卡槽**的 **FERRIT-16** 背板。

![FERRIT-16 背板和可拆卸存储卡](/uploads/ferrit/ferrit-02.webp)

模块化带来一个很直接的好处：USB 控制器出了问题，可以单独更换控制卡；未来接口过时，也可以重新设计控制端，而不必把存储芯片一起丢弃。

项目地址：[GitHub — machdyne/ferrit](https://github.com/machdyne/ferrit)；[Machdyne 官方项目页面](https://machdyne.com/ferrit/)。仓库提供 KiCad 原理图、PCB、BOM、固件及相关文档。

## 为长期存档而设计

Machdyne 将长期保持、较高写入耐久性、模块化、开放硬件和 USB 大容量存储设备兼容性列为主要特点。**200 年保持时间和抗辐射能力是项目方声明的设计特性，不应理解为每一套装置都已完成 200 年的现场验证。** 对档案系统而言，数据本身的校验、环境控制和多副本备份仍然不可省略。

## RP2040 控制器和两级地址译码

FERRIT-CY 控制板以 **RP2040** 为核心，通过 USB Full-Speed 与计算机通信，并将设备呈现为标准 USB Mass Storage。**TLV62568** 将 USB 输入的 5V 降至 3.3V；**M95P32 32Mbit SPI NOR** 用来存放启动及控制固件，不负责用户归档内容。

![FERRIT-CY RP2040 控制卡](/uploads/ferrit/ferrit-03.webp)

存储卡采用共享的 QSPI 时钟和数据总线，再利用 **3-to-8 译码器**选择 F-RAM 芯片。原稿所展示的 **FERRIT-M8 实物卡包含 8 颗 F-RAM**；项目 README 另列出单卡最多 **16 颗芯片**的寻址能力，这对应双面卡扩展设计，两者不是同一个概念。

![FERRIT-M8 存储卡原理图](/uploads/ferrit/ferrit-04.webp)

背板一侧通过 **SN74HC154** 将 4 位槽位地址译码为 16 路片选。控制器先选存储卡，再选卡上的具体芯片。按照项目公开的最高寻址配置，16 个槽位、每槽 16 颗 1MB F-RAM，可对应 **256MB** 的上限。

## 主要器件和固件

- **RP2040**：双核 Cortex-M0+，负责 USB MSC、地址映射与 QSPI 访问。
- **MB85RQ8MXPF**：1MB QSPI F-RAM，保存归档数据。
- **M95P32**：32Mbit SPI NOR，保存控制器固件。
- **74LS138 / SN74HC154**：分别用于芯片级与槽位级片选译码。
- **TLV62568**：5V 到 3.3V 的同步降压转换器。

固件基于 **Pico SDK** 和 **TinyUSB**。主机发出读写请求后，`mapper.c` 根据逻辑块地址定位槽位、芯片及片内偏移。传输跨越芯片边界时，固件会把请求拆分后再访问下一颗芯片。项目将地址映射代码也公开在仓库中。

对 FERRIT 来说，值得研究的不只是 F-RAM 本身，还有它如何用可替换的模块、标准 USB 接口和清晰的存储寻址方式，把小容量介质做成一套可维护的长期存档系统。
