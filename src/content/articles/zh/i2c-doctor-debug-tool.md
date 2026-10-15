---
title: 开源硬件 I²C Doctor：用一台小工具排查 I²C 总线故障
description: I²C Doctor 是一款基于 ESP32 的独立调试工具，支持总线健康评分、上升时间测量、短路检测、地址扫描及故障注入。
locale: zh
translationKey: i2c-doctor-debug-tool
pubDate: '2026-06-10'
category: tools
tags:
- I²C
- ESP32
- Debugging
- 开源硬件
draft: false
seoTitle: 开源硬件 I²C Doctor：用一台小工具排查 I²C 总线故障
seoDescription: I²C Doctor 是一款基于 ESP32 的独立调试工具，支持总线健康评分、上升时间测量、短路检测、地址扫描及故障注入。
---

I²C Doctor是一款紧凑的一体化诊断工具，集成了1.3英寸TFT彩色显示屏。它实时扫描、分析、调试和测试你的 I²C 应用。I²C医生的诊断无需花费数小时解读示波器信号，而是为您提供清晰的健康评分（0-100%）和具体可操作的建议。

![i2c doctor debug tool — 图片 1](/uploads/i2c-doctor-debug-tool/i2c-doctor-debug-tool-01.webp)

硬件开源地址

https://i2c-doctor.com/docs.html#downloads

https://www.tindie.com/products/haleng/i2c-doctor-white/

## 特点

健康评分（0-100%）：基于实时上升时间、上拉电阻和信号电流，即时显示总线稳定性。

短路检测：检测SDA/SCL与GND、SDA/SCL与VDD之间，以及SDA与SCL本身之间的短路。

具体建议：你不再需要手动捕捉I²C信号并测量上升时间来发现潜在的稳定性问题。I2C Doctor用通俗易懂的语言告诉你该做什么。

快速地址扫描器与数据库：它在不到2秒内找到所有连接的传感器，并通过集成数据库自动识别热门芯片。

内置故障注入与压力测试：它不仅仅是观看;它允许你模拟最坏情况，比如强烈的电磁噪声、时钟拉伸或长电缆电容，确保设计在投入生产前是防弹的。

完全独立：得益于内置显示屏和USB-C电源，你可以在现场调试任何I²C总线，无需电脑。

## 原理图

![i2c doctor debug tool — 图片 2](/uploads/i2c-doctor-debug-tool/i2c-doctor-debug-tool-02.webp)

I²C 医生不要求开发者手动启动示波器或逻辑分析仪来解读波形，而是专注于提供直接且实用的反馈。该手持设备基于ESP32-WROOM-32UE微控制器，配备1.3英寸240×240 TFT彩色显示屏，能够评估I²C总线的物理状态，并显示从0%到100%的清晰健康评分。它还能生成通俗易懂的建议，比如降低上拉电阻值或纠正检测到的短路。

![i2c doctor debug tool — 图片 3](/uploads/i2c-doctor-debug-tool/i2c-doctor-debug-tool-03.webp)

该设备支持从10 kHz到1 MHz的I²C速度，并包含多种连接器类型，包括Grove/STEMMA、Qwiic和标准2.54毫米接口。SDA和SCL线路采用100欧姆串联电阻保护，可通过板载DIP开关启用从10 kΩ到1 kΩ的可选上拉电阻。该设备采用USB-C供电，支持3.3V和5V的I²C系统。

扫描过程中，I²C 医生测量电压、检查短路、评估上升时间和电流消耗，并扫描连接设备。常见传感器可通过数据库自动识别。该工具不再让用户自行判断信号完整性是否可接受，而是将测量结果与不同总线速度的预设阈值进行比较，并立即标记潜在问题。

![i2c doctor debug tool — 图片 4](/uploads/i2c-doctor-debug-tool/i2c-doctor-debug-tool-04.webp)

当然价格稍微有丢丢贵，I²C Doctor售价59美元。
