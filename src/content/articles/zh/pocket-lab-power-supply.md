---
title: Github 上实用开源嵌入式项目：口袋实验室电源，20V/5A 可调，支持 PD 快充
description: 从 USB-C PD 取电到电池充电、TPS55289 升降压、电流检测与 eFuse 保护，拆解一台 20V/5A 便携式开源实验室电源。
locale: zh
translationKey: pocket-lab-power-supply
pubDate: '2026-09-24'
category: hardware
tags:
- 电源设计
- USB PD
- TPS55289
- 开源硬件
draft: false
seoTitle: Github 上实用开源嵌入式项目：口袋实验室电源，20V/5A 可调，支持 PD 快充
seoDescription: 从 USB-C PD 取电到电池充电、TPS55289 升降压、电流检测与 eFuse 保护，拆解一台 20V/5A 便携式开源实验室电源。
---

平时在工位上调板子，桌面上那台线性电源用得再顺手，也没法带出门。去现场调试、在车里改个接线，或者只是想换个地方焊板子，就得把电源、插排、一堆鳄鱼夹全都拎上。最近在 Github 上看到一个项目，作者 Ben（BenMakesEverything）直接把实验室电源塞进了一块 4S 锂电池包里，做成了一个巴掌大的便携可调电源，挂出来没多久就拿到了一百多个 star。

![pocket lab power supply — 图片 1](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-01.webp)

外壳是一个大约 10cm 长的盒子。正面有一个旋钮、一块 8 位点阵屏、一个 USB-C 口和一个 DC 输出座。整机由一组带 BMS 的 4S 21700 电池包供电，容量 4500mAh。输出电压能调 1V~20V，步进 100mV。限流范围 0.1A~5A，步进 50mA。USB-C 只负责 PD 充电，不能对外供电。它支持边充边用，前提是负载电流比充电电流小。

Github地址：

https://github.com/BenMakesEverything/Pocket-Lab-Power-Supply

仓库里原理图、Gerber、BOM、坐标文件、外壳、固件都给全了，BOM 里的料基本都标好了 LCSC 编号，想自己打一台的话门槛不算高。需要注意两点：一是板子本身没有 BMS，必须用带保护板的电池包；二是作者已经把原来推荐的那款电池链接删掉了，因为其中一块电池的 BMS 出过问题，自己买电池时要挑靠谱的。协议是 CERN-OHL-S-2.0，允许商用，但必须以同样的协议开源。

## 系统框图

![pocket lab power supply — 图片 2](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-02.webp)

USB-C 进来先经过 PD 协商芯片，再过一颗功率 MOS，送进充电芯片，充电芯片负责给电池充电和输出系统电压。系统电压经过一个带开关的 P-MOS 之后，分成三路：两路 DC-DC 给 3.3V 和 5V，一路进升降压芯片，调出你要的电压。升降压芯片后面跟着一颗 eFuse 做保护，最后经过电流监测送到输出口。另外还有一颗常开的 LDO 专门给 MCU 供电。

## 原理图（一共分了 7 小块）

![pocket lab power supply — 图片 3](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-03.webp)

PD 取电部分。USB 输入口带了 TVS2200 浪涌保护和 ESD122。PD 协商用的是 TI 的 TPS25730，这颗芯片不需要 MCU 参与，靠 ADCIN1/ADCIN2 上的分压电阻就能配置请求的电压档位，作者这里配的是 20V。它的 GATE_VBUS 引脚直接驱动 CSD87501L。CSD87501L 是一颗背靠背的双 N-MOS，协商成功之后才会把 VBUS 放进来，这样一来，没谈好的时候高压进不到后级。

![pocket lab power supply — 图片 4](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-04.webp)

充电和系统供电用的是 BQ25792。这颗芯片挺有意思，它是 1~4 节锂电的降压-升压充电芯片，输入最高到 24V，自带 I2C 接口，还有 NVDC 电源路径管理。所以 USB 输入不管是 5V 还是 20V，都能充满 16.8V 的 4S 电池。原理图上 PROG 引脚接的 27K 电阻决定了电池串数和默认参数，作者在 README 里用大写字母提醒：如果你想换成别的串数，一定要改这个电阻，不然电池会被过充。电池低于 12V（每节 3V）时，芯片直接切断放电。TS 脚接了一颗 103AT 热敏电阻做温度检测。SYS 输出后面那颗 FDS6679AZ 是 P-MOS，由拨动开关 SW1 控制，这一个开关同时管输出、充电状态和显示。

![pocket lab power supply — 图片 5](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-05.webp)

核心的调压部分用的是 TPS55289。这是一颗四开关升降压芯片，输出范围 0.8V~22V，内部 DAC 以 10mV 为步进，通过 I2C 设定。它还支持外部采样电阻做恒流限流，这里 ISP/ISN 之间用的是 10mΩ 的 R32。电感选的是 Coilcraft XAL7070 4.7μH，开关频率由 FSW 上的 49.9K 电阻设定。输入电池电压在 12V~16.8V 之间，输出要跨越到 20V，正好落在升降压的舒适区。

![pocket lab power supply — 图片 6](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-06.webp)

固件里设电压的写法很简单，把毫伏数换算成寄存器码，先写低字节再写高字节：

int code = constrain((millivolts - 800) / 10, 0, 0x7FF);

writeReg8(tpsAddr, REG_REF_LSB, code & 0xFF);

writeReg8(tpsAddr, REG_REF_MSB, (code >> 8) & 0x07);

限流寄存器的 bit7 是使能位，低 7 位以 50mA 为一档，写法 0x80 | ((mA + 25) / 50)。按道理芯片的上限是 22V、6.35A。作者在 FAQ 里说，补偿网络的原因会让输出到不了 22V，所以软件里卡在了 20V，电流卡在 5A，并且建议长时间使用别超过 50W 左右。

输出保护这一块，TPS55289 后面串了一颗 eFuse TPS259474，ILM 上的 560Ω 电阻决定限流点。再往后是 SMBJ24A TVS 和 INA226。注意 C60（220μF）和 C62 两颗电容，原理图上标注了是视频发布之后为了压纹波补上的，属于实测之后打的补丁。

![pocket lab power supply — 图片 7](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-07.webp)

电流检测一共用了两颗 INA226，一颗放在电池端，一颗放在输出端，采样电阻都是 2512 封装的 10mΩ。电池端那颗测到的是整机功耗，屏幕、MCU 都算在里面。另外，固件会根据电流方向判断是不是在充电，是的话屏幕上就显示 Charging。

![pocket lab power supply — 图片 8](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-08.webp)

控制部分用的 MCU 是 ATtiny3216，程序用 Arduino 写，通过 UPDI 下载。显示屏是 Broadcom 的 HCMS-297x 系列，8 字符 5×7 LED 点阵，串行接口驱动，单独做了一块小背板。旋钮是 PEC12R 编码器，按一下可以在调电压和调限流之间切换。平时屏幕轮流显示电池电压、实际输出电压、负载电流和整机功率。如果 TPS55289 报了短路、过流、过压，屏幕上会直接显示 TPS SCP / OCP / OVP。

![pocket lab power supply — 图片 9](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-09.webp)

辅助电源方面，两颗 Silergy SY8253 分别出 3.3V 和 5V，其中 5V 同时给 TPS55289 的 VCC 供电。MCU 那一路单独用 TPS70933，这颗 LDO 静态电流很小，保证开关断开时 MCU 还能工作。

![pocket lab power supply — 图片 10](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-10.webp)

PCB 是四层板，中间两层分别是电源层和地层。狭长的板形刚好贴着外壳，功率路径从左往右一字排开。

![pocket lab power supply — 图片 11](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-11.webp)

![pocket lab power supply — 图片 12](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-12.webp)

![pocket lab power supply — 图片 13](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-13.webp)

![pocket lab power supply — 图片 14](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-14.webp)

外壳是 3D 打印的，一共三个件：主壳、面板、垫片。仓库里 STL 和 STEP 文件都有，M3 热熔螺母加 4 颗螺丝就能固定。

![pocket lab power supply — 图片 15](/uploads/pocket-lab-power-supply/pocket-lab-power-supply-15.webp)
