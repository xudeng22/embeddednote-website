---
title: M5Stack Core StopWatch：ESP32-S3 搭配 1.75 英寸圆形 AMOLED 触摸屏
description: M5Stack Core StopWatch 配备 ESP32-S3R8、466×466 圆形 AMOLED 触摸屏、16MB Flash、8MB PSRAM、IMU、音频与 450mAh 电池。
locale: zh
translationKey: stopwatch
pubDate: '2026-05-25'
category: hardware
tags:
- M5Stack
- ESP32-S3
- AMOLED
- Development Board
- Wearables
draft: false
author: EmbeddedNote
sourceUrl: https://docs.m5stack.com/en/core/StopWatch
seoTitle: M5Stack Core StopWatch 开发板：ESP32-S3、1.75 英寸 AMOLED
seoDescription: Core StopWatch 搭载 ESP32-S3R8、1.75 英寸 466×466 AMOLED、16MB Flash、8MB PSRAM、450mAh 电池、六轴 IMU 与开源原理图。
---

M5Stack 的 **Core StopWatch** 是一块外观更像随身设备的开发板：圆形机身，正面是一块 **1.75 英寸 AMOLED 触摸屏**，内部采用乐鑫 **ESP32-S3R8**。它不是传统的裸板形态，用来开发可穿戴交互界面、电子徽章或小型 IoT 终端会更直观。

这块屏幕分辨率为 **466×466**，处理器配备 **16MB Flash** 和 **8MB PSRAM**。官方规格列出的无线功能为 **2.4GHz Wi-Fi**；芯片本身属于支持蓝牙的 ESP32-S3 家族，但具体功能仍应以所选固件和开发框架为准。机身上还有两颗可编程按键、独立电源键及振动马达。

![M5Stack Core StopWatch 产品功能示意](/uploads/stopwatch/stopwatch-01.webp)

官方资料：[Core StopWatch 产品文档](https://docs.m5stack.com/en/core/StopWatch)；[固件使用说明](https://docs.m5stack.com/en/guide/display_device/stopwatch/usage)。

## 音频、传感器与扩展

除了 AMOLED 触控屏，Core StopWatch 还集成了 **MEMS 麦克风、ES8311 音频编解码器、1W 扬声器、BMI270 六轴 IMU 和 RX8130CE 实时时钟**。外设可通过 HY2.0-4P 接口和背面的扩展排针连接。背部还预留了磁吸结构与挂绳孔，方便不同安装方式。

供电部分采用 **M5PM1 多级电源管理**，内置 **450mAh 电池**，通过 USB-C 供电和充电。对于需要电池供电、显示界面、姿态感知及声音交互的原型机，这种集成度可以省去不少外围板卡。

## 官方开放的硬件资料

![M5Stack Core StopWatch 原理框图](/uploads/stopwatch/stopwatch-02.webp)

![M5Stack Core StopWatch 功耗与接口设计图](/uploads/stopwatch/stopwatch-03.webp)

M5Stack 提供了原理图及接口映射资料，适合开发前先检查供电、I/O 分配与显示控制方式。参考售价约为 **45 美元**，实际价格以销售渠道为准。

*硬件版本提示：官方对部分 v1.0 批次标识错误作过更正，个别标为“BAT”的引脚实际为 5V 输入。接外部供电或电池前应按手中的硬件版本核对最新版引脚说明。*
