---
title: Cyber Ægg：BornHack 开源电子胸牌，活动结束还能继续用
description: BornHack 2026 Cyber Ægg 胸牌采用 nRF52840、三色电子纸、SX1262 LoRa、NFC 和 MeshCore，活动结束仍可作为桌面设备。
locale: zh
translationKey: cyber-aegg-bornhack-badge
pubDate: '2026-08-04'
category: open-source
tags:
- nRF52840
- E-Paper
- LoRa
- MeshCore
draft: false
seoTitle: Cyber Ægg：BornHack 开源电子胸牌，活动结束还能继续用
seoDescription: BornHack 2026 Cyber Ægg 胸牌采用 nRF52840、三色电子纸、SX1262 LoRa、NFC 和 MeshCore，活动结束仍可作为桌面设备。
---

最近看到 BornHack 2026 的电子胸牌，名字叫 Cyber Ægg（蛋形徽章），硬件仓库放在 Codeberg。

Cyber Ægg不是普通会议电子胸牌。Hackaday 对这个项目的评价挺到位：很多电子胸牌活动结束后就吃灰，Cyber Ægg 的思路是活动结束后还能继续当桌面时钟、日历和 MeshCore 节点用。

![cyber aegg bornhack badge — 图片 1](/uploads/cyber-aegg-bornhack-badge/cyber-aegg-bornhack-badge-01.webp)

这个板子外形是半个蛋，配 3D 打印外壳，有点电子宠物的味道。现场使用时，它可以跑 Tamagotchi 风格的虚拟宠物、活动日历、RFID token 游戏；回到家以后，它还能立在桌面上，当一个低功耗电子纸终端。

![cyber aegg bornhack badge — 图片 2](/uploads/cyber-aegg-bornhack-badge/cyber-aegg-bornhack-badge-02.webp)

Badge.Team 官方文档：

https://badge.team/docs/badges/bornhack-2026/

硬件仓库（KiCAD格式，包括主控原理图，NFC原理图，LoRA原理图等）：

https://codeberg.org/Ranzbak/bornhack2026-hardware

固件源码（ Rust / Embassy）：

https://codeberg.org/Ranzbak/bornhack-firmware-2026

硬件核心是 Nordic nRF52840，，Cortex-M4F，带 BLE，也带 NFC tag PHY。Cyber Ægg 没有再额外塞一个蓝牙芯片，BLE 直接用 nRF52840 自带射频；NFC 也是用 nRF52840 的 NFC tag 功能，PCB 上绕了一组线圈，官方文档里提到线圈大约 2.8uH，通过电容调到 13.56MHz，另外需要注意它只能做 tag，不能做 reader。

显示部分用的是 1.54 英寸三色电子纸，黑、白、红三色，分辨率 152 × 152，控制器是 SSD1675 / SSD1675B，走 SPI接口。户外场景来说，电子纸非常合适：太阳底下可读，保持画面不用耗电。BornHack 一周时间，官方目标也是一次电池充电撑完整个 camp。

通信部分比较有意思，板上单独放了 Semtech SX1262 做 LoRa，还是 SPI 接口。LoRa 匹配和 balun 参考 Semtech 应用笔记，天线部分参考 TI 的设计。软件网络侧则跑 MeshCore，这样它不只是一个本地小玩具，而是能加入营地 mesh 网络的节点。

![cyber aegg bornhack badge — 图片 3](/uploads/cyber-aegg-bornhack-badge/cyber-aegg-bornhack-badge-03.webp)

主要器件大概如下：

| 模块 | 器件 / 方案 | 接口 |
| --- | --- | --- |
| MCU | Nordic nRF52840 | - |
| 显示 | 1.54 英寸三色电子纸，SSD1675/SSD1675B | SPI |
| LoRa | Semtech SX1262 | SPI |
| 蓝牙 | nRF52840 内置 BLE | - |
| NFC | nRF52840 NFC tag PHY + PCB 线圈 | - |
| 输入 | 五向摇杆、Execute、Cancel 按键 | GPIO |
| 反馈 | RGB LED、压电蜂鸣器 | GPIO / PWM |
| 电源 | 锂电池、USB-C、拨动开关 | - |
| 扩展 | QWIIC / I2C | I2C |

硬件是 KiCad 开源的，仓库里能看到主控、LoRa、显示、电源、NFC、QWIIC 等分模块原理图：

这里有个小坑，官方文档也直接写出来了：板上的 QWIIC 接口把 3.3V 和 GND 交换了。也就是说，不能拿普通 QWIIC 线直接插外设，要做一根修正线，把电源两根线在一端交叉。官方还提醒，一些 NFC、LoRa、Bluetooth 射频电路还留着 U.FL / IPEX 连接器，主要是方便调试和天线匹配，PCB 天线还没有完整表征，不建议现在直接打板量产。

把活动纪念品做成一个长期可用的低功耗设备，这是项目最大亮点，nRF52840 负责 BLE、NFC 和主控，SX1262 负责远距离 mesh，电子纸负责常显界面，五向摇杆和两个按键负责本地交互，USB-C 负责供电和数据，锂电池负责离线运行。东西不复杂，但组合得很完整。
