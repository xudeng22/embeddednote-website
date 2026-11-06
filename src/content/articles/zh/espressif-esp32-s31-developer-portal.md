---
title: 乐鑫更新了ESP32-S31在线网站，中英文都支持
description: 乐鑫 ESP32-S31 开发者网站提供中英文内容，涵盖双核 RISC-V、Wi-Fi 6、Bluetooth 5.4、Thread、Zigbee 和千兆以太网。
locale: zh
translationKey: espressif-esp32-s31-developer-portal
pubDate: '2026-06-01'
category: mcu-soc
tags:
- 乐鑫
- ESP32-S31
- RISC-V
- Wi-Fi 6
- 蓝牙
draft: false
seoTitle: 乐鑫更新了ESP32-S31在线网站，中英文都支持
seoDescription: 乐鑫 ESP32-S31 开发者网站提供中英文内容，涵盖双核 RISC-V、Wi-Fi 6、Bluetooth 5.4、Thread、Zigbee 和千兆以太网。
author: EmbeddedNote
sourceUrl: https://esp32-s31.espressif.com/en
updatedDate: '2026-11-06'
---

乐鑫 ESP32-S31 开发者网站已经提供中英文版本。对正在选 MCU 的工程师来说，值得看的不只是页面做了双语，而是这颗芯片把高速接口、图像处理外设和多种无线协议放在了同一平台上。是否适合产品，最终还是要回到内存、引脚、带宽和软件支持情况。

根据乐鑫目前公开的资料，ESP32-S31 采用**双核 32 位 RISC-V，最高 320 MHz**，片上 **512 KB SRAM**，可连接外部高速 PSRAM；无线侧包含 **2.4 GHz Wi-Fi 6、Bluetooth 5.4（LE 与经典蓝牙）以及 IEEE 802.15.4**，后者用于 Thread、Zigbee 等协议。支持这些协议，不等于它们在任何固件组合下都能同时达到各自标称速率。

![乐鑫 ESP32-S31 芯片官方配图](/uploads/espressif-esp32-s31-developer-portal/espressif-esp32-s31-developer-portal-01.webp)

## 更值得检查的，是外围接口怎么落地

官方列出的外设包括 USB 2.0 High-Speed OTG、摄像头接口、24-bit RGB 显示接口、PPA 像素处理加速器、JPEG 编解码，以及**千兆以太网 MAC**。注意这里是 MAC，不是芯片直接提供 RJ45 网络口；做成有线产品还需要外部 PHY、网络变压器、连接器，以及相应的软件和 PCB 布线。

同样，带 JPEG 硬件和 RGB 接口，不等于可以直接推断某块屏幕的刷新率。真正做图像系统时，传感器输入、PSRAM 带宽、缓冲区、DMA 和显示输出会同时争夺资源。

| 官方特性 | 选型时要验证的项目 |
|---|---|
| 512 KB 片上 SRAM | RTOS 栈、DMA 缓冲区和实时任务的内存是否足够 |
| 外部 PSRAM | 模组实际接线、读写速度和内存分配策略 |
| Wi-Fi、蓝牙、802.15.4 | SDK 版本、协议共存、连接稳定性和合规要求 |
| 千兆以太网 MAC | 外部 PHY、供电、时钟和信号完整性设计 |
| 摄像头、RGB、PPA、JPEG | 数据链路整体带宽，而不是单个外设能否点亮 |

## 建议按这个顺序评估

先拿到**对应芯片版本的 Data Sheet 和开发板原理图**，核查 Flash/PSRAM 连接、供电、复用引脚和以太网 PHY，再按 USB、显示/摄像头、无线协议逐项 Bring-up。最后测试同时运行时的内存占用、功耗、稳定性和实际吞吐。本文仅根据官方资料进行架构分析，**没有进行 ESP32-S31 开发板实测**。

**一手资料：** [乐鑫 ESP32-S31 产品页](https://www.espressif.com/en/products/socs/esp32-s31) · [中英文技术文档](https://esp32-s31.espressif.com/en/docs) · [ESP32-S31 数据手册](https://documentation.espressif.com/esp32-s31_datasheet_en.html)。

![ESP32-S31 中文开发者网站页面截图](/uploads/espressif-esp32-s31-developer-portal/espressif-esp32-s31-developer-portal-02.webp)

<!-- editorial-v3-20261106 -->
