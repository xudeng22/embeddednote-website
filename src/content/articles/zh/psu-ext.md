---
title: Github 上超实用嵌入式项目——给普通台式电源外挂一个可编程控制盒 PSU-EXT
description: PSU-EXT 串联在台式电源与负载之间，增加电压电流监测、继电器控制、SCPI 接口及 Web 控制台，适用于实验室自动化原型。
locale: zh
translationKey: psu-ext
pubDate: '2026-11-05'
category: hardware
tags:
- PSU-EXT
- ESP32-S3
- SCPI
- 台式电源
- 开源硬件
draft: false
sourceUrl: https://github.com/PSU-Ext-Org
author: EmbeddedNote
seoTitle: Github 上超实用嵌入式项目——给普通台式电源外挂一个可编程控制盒 PSU-EXT | EmbeddedNote
seoDescription: PSU-EXT 串联在台式电源与负载之间，增加电压电流监测、继电器控制、SCPI 接口及 Web 控制台，适用于实验室自动化原型。
---

实验室里很多台式电源本身还能用，但没有远程控制，或者接口比较老。真要做自动化测试，总不能每次都手拧旋钮、盯着万用表。**PSU-EXT** 采用一种相对直接的思路：不换电源，而是在**台式电源与负载之间串接一个可编程控制盒**。

PSU-EXT 可以对输出电压、电流进行采样，控制继电器通断，并通过 SCPI 接口配合自动化脚本。要注意，**电压仍由原来的台式电源产生与调节**；这个控制盒增加的是测量、通断及管理能力，并非把普通固定输出电源变成能够任意调节输出电压的独立程控电源。

**开源组织：** [PSU-Ext-Org](https://github.com/PSU-Ext-Org) · **相关文章：** [Hackster.io](https://www.hackster.io/news/make-any-bench-power-supply-programmable-with-psu-ext-bbb23af5223d)

![PSU-EXT 工程样机：电源与负载连接端子及橙色外壳](/uploads/psu-ext/psu-ext-01.webp)

## 硬件：给现有电源增加一个可编程前端

根据附件中的工程资料，原型硬件工作范围为 **0–25 V、0–2.5 A**，PCB 尺寸约 **100 × 50 mm**，USB-C 用于控制侧供电及数据通信。输入接台式电源，输出接被测负载，左侧设有输入输出香蕉插座，板上集成 ESP32-S3 及测量与控制电路。

![PSU-EXT PCB 渲染图：左侧输入输出端与右侧 ESP32-S3 控制区域](/uploads/psu-ext/psu-ext-02.webp)

该项目明确属于 **EVT（工程验证测试）阶段的原型**，不是经过认证的消费级产品。原文还提醒其**缺少反接保护**，因此在供电前必须核对极性、电流、电压和线缆连接，不应直接用于无人值守或安全关键场景。

## 核心器件与测量链路

| 功能 | 器件 | 作用 |
| --- | --- | --- |
| 主控 | ESP32-S3-WROOM-1-N16R8 | USB CDC、Wi-Fi、SCPI/TCP 通信及控制 |
| 采样 | INA240A2 + ADS1115 | 对分流电阻信号进行放大，并通过 16 位 ADC 采样 |
| 隔离 | ISO1540 + RFM-0505S | I²C 信号与测量域供电隔离 |
| 输出控制 | HF49FD/005-1H12T 继电器 | 控制负载通断 |
| 接口 | USB-C、香蕉插座 | 控制侧供电通信和电源输入输出 |

主控采用 ESP32-S3-WROOM-1-N16R8，负责 USB CDC、Wi-Fi 和 SCPI/TCP 服务。采样前端采用 **INA240A2** 测量分流电阻上的差分电压，再由 **ADS1115** 完成模数转换。相比直接将分压信号接入 MCU ADC，这样的测量链路考虑了电流前端以及信号隔离。

隔离部分包含 **ISO1540** 和隔离 DC-DC 电源。输出控制采用继电器，附件描述 CH1 继电器控制 GPIO 为 **GPIO38**，固件上电默认关闭。需要强调，软件默认关闭输出不能代替独立的硬件保护设计。

![PSU-EXT 前端测量与继电器控制原理图：电流分流、INA240、ADS1115 与电压采样](/uploads/psu-ext/psu-ext-03.webp)

## 软件：USB、Wi-Fi 与 SCPI

PSU-EXT 不只是公开了一块 PCB。原文介绍固件基于 **ESP-IDF**，可通过 USB CDC 和 Wi-Fi TCP 提供 SCPI 命令接口，TCP 使用仪器控制领域常见的 **5025 端口**。

上位机方案包含 **Java 17 / Spring Boot** 后端与 **React** 前端，可以在浏览器中查看电压、电流、功率数据，并控制输出、调整过压和过流保护参数。整个项目覆盖硬件、固件、网页控制台与安装工具。

![PSU-EXT Web 控制台：输出开关、电压电流读数、曲线与 OCP 设置](/uploads/psu-ext/psu-ext-04.webp)

如果你经常测试开发板启动电流、做长时间老化、安排上下电序列，或者希望把现有台式电源接入自动化脚本，这个项目值得参考。但对实际电源保护效果，应先完成限值、断电响应与异常工况的实测，不能仅凭页面显示的 OVP/OCP 选项认定硬件已经达到产品级安全要求。
