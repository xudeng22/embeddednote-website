---
title: 'Github上好玩的嵌入式项目——电子墨水屏+OLED相结合的PDA（PocketMage PDA）'
description: 'PocketMage用ESP32-S3、3.1英寸电子纸和256×32 OLED做了一台带实体键盘的迷你PDA。看看双屏设计、键盘电路、应用开发和开源进度。'
locale: zh
translationKey: pocketmage-pda-dual-display
pubDate: '2026-11-01'
category: open-source
tags:
  - PocketMage
  - ESP32-S3
  - 电子纸
  - OLED
  - PDA
  - 开源硬件
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/TalismanDesign/PocketMage_PDA
seoTitle: 'PocketMage PDA：ESP32-S3、电子纸与OLED双屏开源掌上电脑'
seoDescription: 'PocketMage将3.1英寸电子纸与256×32 OLED结合，搭载ESP32-S3、实体键盘及PocketMageOS。查看最新KiCad硬件文件、SDK、ELF应用和双屏设计。'
---

这些年用 ESP32 做掌上设备的不少，但同时放电子墨水屏和 OLED 的还真不多。PocketMage PDA 就是这么一台小机器：翻盖外形、实体键盘、透明外壳，主屏是一块电子纸，键盘上方还塞了一条细长的 OLED。看着有点像当年的掌上电脑，里面跑的却是 ESP32-S3 和作者自己用 C++ 写的系统。

![PocketMage PDA 翻盖式掌上电脑，电子纸主屏与键盘上方的 OLED 状态条](/uploads/pocketmage-pda/pocketmage-cover.webp)

项目地址：[PocketMage PDA（GitHub）](https://github.com/TalismanDesign/PocketMage_PDA)。原始仓库地址 `ashtf8/PocketMage_PDA` 已指向该项目。**本文以 2026 年 11 月 1 日的代码版本为准**：这个项目已经从早期的文本编辑器和文件管理器，发展成有独立 SDK、可加载应用和硬件工程文件的掌上设备，但仍在持续开发。

PocketMage 最有意思的地方不是 ESP32-S3，而是把两种屏幕分工。**3.1 英寸、320×240 的单色 SPI 电子纸（GDEQ031T10）负责正文、文件和需要停留的内容**，刷新不快，但画面保持时几乎不需要持续供电。**256×32 的单色 SPI OLED（SSD1326，ER-OLED018-1W）负责辅助显示**：菜单导航、输入反馈这类需要频繁变化的信息，不必每敲一下键都让电子纸完整刷新。电子纸慢这件事没变，作者只是把交互上最影响手感的部分交给了 OLED。

![PocketMage PDA 另一角度实拍，透明外壳、物理键盘和翻盖结构](/uploads/pocketmage-pda/pocketmage-device.webp)

硬件清单也挺像一台完整的小电脑。核心是 **ESP32-S3-WROOM-1**，带 Wi-Fi 和蓝牙，Flash 为 16 MB。旧版资料常写 8 MB RAM，不过最新 PlatformIO 工程已经把生产版 **N16R2** 与 Beta 版 **N16R8** 分开：生产版配置使用 2 MB PSRAM，Beta 版虽对应 8 MB PSRAM 模组，但固件构建中暂时禁用了 PSRAM，实际可用内存不能混为一谈。输入部分用 **TCA8418 I²C 键盘矩阵控制器**，免得把大量 GPIO 都耗在按键扫描上；**MPR121** 则负责电容触摸输入。板上还有 microSD、**PCF8563T 实时时钟**、压电蜂鸣器、电源按键、USB-C 和 **1200 mAh 锂聚合物电池**。

扩展接口留出了 3.3 V、GND、I²C、SPI 和数个 GPIO，其中两路可通过焊桥在普通 GPIO 与 UART TX/RX 之间切换。用它接传感器或者做点小外设，比一台只能运行固定程序的电子笔记本更有折腾空间。电池容量是标称规格，实际续航还得看 OLED 亮度、刷新频次、Wi-Fi 工作时间等条件，作者没有给出可直接当作实测结论的统一数字。

**键盘和显示屏并不是画在一张简单的草图里。** 当前仓库的 `Resources/PCB` 已包含可编辑的 KiCad 原理图、PCB 文件和生产资料，`Resources/CAD` 也公开了结构件 STEP 模型。下面两张沿用原稿里的电路图，适合快速了解键盘与显示板的分工；要核对网名、器件值和封装，应以当前硬件版本的原始工程为准。

![PocketMage PDA 键盘电路原理图，包含键盘矩阵和控制器连接](/uploads/pocketmage-pda/pocketmage-keyboard-schematic.webp)

*键盘部分的原理图概览。*

![PocketMage PDA 显示及主控电路原理图，展示芯片和外设连接](/uploads/pocketmage-pda/pocketmage-display-schematic.webp)

*显示与主控部分的原理图概览。*

软件仍以 **PlatformIO + C++** 为基础，但已不只是一个简单的应用启动界面。当前 PocketMageOS 除文本编辑器和 FileWiz 外，还提供日历、任务、日记、词典、USB 文件传输、设置、COMM mesh 聊天以及终端等应用；README 还列有 SSH 支持。主菜单保留 `roll dN` 掷骰子、设置时间和按文件名打开文件等命令。具体功能和稳定性仍取决于固件版本，不能把 README 的应用列表直接当成全部经过实测的功能。

更值得留意的是开发方式。最新系统把应用分为两类：**Native App** 直接编进固件，**ELF App** 则可以用独立的 PocketMage SDK 构建，从 microSD 装载运行。PocketMageOS 通过一套状态分发逻辑将按键和双屏刷新交给当前应用，并用统一的库管理屏幕、键盘、存储等硬件。要自己写程序，不必先把整个硬件驱动再做一遍。作者仍把电子书阅读器、闹钟、Wi-Fi 笔记/日历同步、蓝牙键盘以及 LoRa/Meshtastic 扩展列为计划项；项目 README 也提供了 Crowd Supply 套件入口。

如果打算复刻，最新仓库的 `LICENSE` 已改为 **Apache-2.0**，与 2025 年使用 CC BY-NC-SA 4.0 的历史版本不同。代码和硬件工程可以按当前许可条款评估复用，但产品名称、第三方图片及其他素材的权利仍需另行核对。双屏设计仍是 PocketMage 最耐看的地方：电子纸负责大面积内容，OLED 接手需要快速反馈的那一小段交互。

资料：[PocketMage 最新项目源码](https://github.com/TalismanDesign/PocketMage_PDA) · [本文核对的 2026-11-01 版本](https://github.com/TalismanDesign/PocketMage_PDA/tree/f8b5c13fa14667dca36a54022d2cfe2217553ab5) · [硬件 PCB 与结构文件](https://github.com/TalismanDesign/PocketMage_PDA/tree/main/Resources) · [PocketMageOS 架构说明](https://talismandesign.github.io/PocketMage_PDA/docs/development/architecture) · [作者应用开发演示](https://www.youtube.com/watch?v=3Ytc-3-BbMM)。
