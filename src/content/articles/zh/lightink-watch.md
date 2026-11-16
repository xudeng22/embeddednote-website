---
locale: zh
translationKey: lightink-watch
pubDate: '2026-11-16'
updatedDate: '2026-11-16'
category: display
draft: false
contentType: deep
series: epaper
supplyCta: true
author: EmbeddedNote
sourceUrl: https://github.com/DarkZeros/LightInk
title: "靠太阳能实测 9 个月的电子纸手表"
description: "LightInk 用 ESP32-PICO-D4、1.54 英寸电子纸和 RTC wake stub，把刷新功耗压到约 2µA；本文拆开硬件、功耗账和已知坑。"
tags:
- LightInk
- ESP32-PICO-D4
- 电子纸
- 太阳能
- 低功耗
- Watchy
- TPS63900
- 开源硬件
seoTitle: "LightInk：靠太阳能实测 9 个月的 ESP32 电子纸手表"
seoDescription: "LightInk 用 ESP32-PICO-D4、1.54 英寸电子纸、TPS63900 和 RTC wake stub 做太阳能手表；含 2µA 功耗账、V4 原理图与已知硬件问题。"
---

电子纸手表不稀奇，Watchy 早就把 ESP32 和 1.54 英寸黑白屏做成了开源硬件。但 Watchy 的续航按周算，LightInk 想干的是另一件事：做成 90 年代那种太阳能电子表，只要有光就不用管充电。作者 Daniel Ansorregui，项目从 2019 年断断续续做到现在，GitHub 上 750 多 star，Hackaday 上也进了 Green Powered Challenge。这套东西前后改了 12 版 PCB、10 版外壳，现在仓库里是 V4，前面还有 V0.1、V1、V2、V3 和一条失败的 ESP32-S3 V10 分支。

![LightInk 黑色和白色版本](/uploads/lightink/lightink-hero.webp)

*LightInk 的黑色和白色版本。太阳能板在表盘上方，屏幕是 1.54 英寸 200×200 黑白电子纸。图片：Daniel Ansorregui / LightInk*

表是 31×41mm 的两层板，0.6mm 厚，屏幕直接贴在板子背面，所以背面不能放任何器件。主控 **ESP32-PICO-D4**，屏是 1.54 英寸 200×200 黑白电子纸（SSD1681，GDEH0154D67 / 0154BN-D67 一类），**TPS63900** buck-boost 给 2.7V 和 3.0V 两档，**PCF8563** RTC 配 32.768kHz 晶振，TP4054 充电，Wio-SX1262 做 LoRa，另外还有 GPS、蜂鸣器、振动马达、LED 和四块电容触摸。太阳能板是 Panasonic Amorton 5815，4.5–5.2V、1.1–2.5mA，直接并在电池上，没有额外的充电管理。

[![LightInk 太阳能演示](/uploads/lightink/lightink-case.webp)](https://youtu.be/erjeWSajqhQ)

*▶ 太阳能演示（YouTube）。外壳里那块长条就是 Amorton 5815，红色和黑色线直接并到电池。图片：Daniel Ansorregui / Hackaday.io*

真正的难点不是把东西塞进去，是让 ESP32 少醒一会儿。ESP32 从 Flash 启动一次要 28ms，大约 1mAs，按作者的说法占总功耗的 60%；代码写得再省，这一段也躲不掉。LightInk 把显示刷新搬进 **RTC wake stub**：不加载 Flash，直接在 RTC 内存里跑一段自己重写的 uSPI，把要更新的显示区域写进 SSD1681，再让 ESP32 回深睡。屏幕刷新的时候，ESP32 已经断电，连 1mA 的轻睡电流都省了。

![LightInk 拆解](/uploads/lightink/lightink-internals.webp)

*拆开后的两块表：左边是太阳能板和主控，右边是屏幕、FPC 和电池。图片：Daniel Ansorregui / Hackaday.io*

这套东西跑下来，刷新时平均大约 **2µA**，100mAh 电池能撑 **6–10 个月**；作者实际用到 **9 个月**，200mAh 的 Watchy 电池理论上能到 **400 天**。作为对比，原版 Watchy 大概两周到一个月。中间他还试过 ESP32-S3，结果 S3 在 2.7V 下不稳，RTC 启动要 10ms 左右，待机电流也高，最后整条路线放弃，退回 PICO-D4。

2.7V 不是随便选的。作者拿 TPS63900 的开发板一路往下试：3.3V、3.0V 都正常，2.6V 屏幕不工作，2.7V 能跑但 WiFi 会出问题；最后定成 2.7V 和 3.0V 两档，平时 2.7V，开 WiFi 再切 3.0V，整机功耗大约降 15%。这也是为什么 ESP32-S3 那条路走不通：S3 在 2.7V 下不稳，RTC 启动又慢，待机电流比 PICO-D4 高一个数量级。

电池这块也有坑。V4 把 LoRa、GPS、蜂鸣器、振动、LED 全塞进去，留给电池的空间只有 30mAh 左右；30mAh 的内阻扛不住屏幕刷新和 WiFi 的 100mA 峰值，电压一掉就复位。作者后来建议至少 50mAh，或者多堆电容。太阳能板直接并电池也有代价：太阳底下电压能到 6V，充满后继续晒，电池保护板会发热，极端情况下会鼓包。

为了保证待机，作者把能砍的都砍了：加速度计不要，因为就算关掉也要 1µA；太阳能不做 MPPT，直接并电池；LoRa 和 GPS 只在需要时上电，发完就断。核心思路是“能断电就断电”，而不是在软件里省。

[![LightInk 功能演示](/uploads/lightink/lightink-panel.webp)](https://youtu.be/qBj7sOVVzNI)

*▶ 功能演示（YouTube）。屏幕型号 0154BN-D67，SSD1681 驱动，200×200 黑白。图片：Daniel Ansorregui / Hackaday.io*

项目不是“开源了就能无脑复刻”的类型。PCB 单面布局，屏幕当支撑；V4 的 LoRa 天线焊盘直接接地，不手工飞线就没信号；GPS 模块的槽位要锉；30mAh 电池扛不住 100mA 的峰值，作者建议至少 50mAh；太阳能板在太阳下能到 6V，长期满电暴晒有风险。外壳 3D 打印，前后壳用胶粘，不防水；作者自己说，做这个不是为了卖，是为了把 90 年代那块太阳能表做得更好玩。

![LightInk 屏幕与走线](/uploads/lightink/lightink-panel-wiring.webp)

*屏幕背面走线：太阳能板、电池、FPC 都挤在 31×41mm 的板子后面。图片：Daniel Ansorregui / Hackaday.io*

软件是 ESP-IDF，带触摸设置、NTP 对时、时区、月相、日出日落、LED、振动、蜂鸣器、LoRa 收发和 GPS；Android 伴生 App 通过 BLE 做配对和设置同步，协议文档也在仓库里。许可证 GPL-3.0，硬件是 EasyEDA 工程、BOM、Gerber 和 STL 一起放出来。

![LightInk V4 原理图](/uploads/lightink/lightink-schematic.webp)

*V4 原理图：ESP32-PICO-D4、TPS63900、PCF8563、Wio-SX1262、充电和显示接口都在一张图上。图片：LightInk 仓库（GPL-3.0）*

最值得看的地方不是“太阳能”三个字，而是它把低功耗拆到了每一次启动、每一帧刷新、每一个脚位；很多人做低功耗停在选一颗低 Iq 的 DC-DC，LightInk 把 ESP32 的启动时间也当成功耗预算的一部分，这一点比堆功能更难。这些数字都是作者自己用 PicoScope 和电流表测的，仓库里没有第三方功耗报告；Hackaday 上的 9 个月是单块表的使用记录，不是批量测试。想复刻的话，先看 `hardware/pcb/PCB.md` 里的 known issues，再看 wake stub 和 `uspi.h` 的代码；手表能不能跑一年，取决于你有没有耐心把这几毫安时抠出来。
