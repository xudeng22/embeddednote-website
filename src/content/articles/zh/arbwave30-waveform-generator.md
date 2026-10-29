---
title: Github 上超硬核嵌入式项目：30MHz 任意波形发生器 ArbWave30
description: ArbWave30 开源任意波形发生器采用 STM32、GW2A FPGA 和 AD9747 DAC，分析时钟、模拟链路、输出滤波与 SCPI 控制。
locale: zh
translationKey: arbwave30-waveform-generator
pubDate: '2026-09-14'
category: open-source
tags:
- FPGA
- Arbitrary Waveform Generator
- DAC
- SCPI
draft: false
seoTitle: Github 上超硬核嵌入式项目：30MHz 任意波形发生器 ArbWave30
seoDescription: ArbWave30 开源任意波形发生器采用 STM32、GW2A FPGA 和 AD9747 DAC，分析时钟、模拟链路、输出滤波与 SCPI 控制。
---

最近看到一个开源仪器项目，叫ArbWave30，目标是做一台 30MHz 任意波形发生器。

Github地址：

https://github.com/EERNINUO/ArbWave30

这个项目不是简单拿 DDS 模块拼一个信号源，而是按“真正仪器”的思路来做。FPGA 负责高速 DDS 和 DAC 时序，MCU 负责 USB 通信和 SCPI 命令（Standard Commands for Programmable Instruments 缩写 SCPI），后面再接重构滤波、差分转单端、衰减网络和输出功率级。仓库里不光有代码，还有硬件架构文档、技术规格书、KiCad 原理图、仿真图、调试波形、用户手册和 SCPI 参考手册。

![arbwave30 waveform generator — 图片 1](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-01.webp)

ArbWave30 当前定位是单通道信号源，支持正弦、方波、三角波、噪声波和直流。指标上，正弦最高 30MHz，方波最高 5MHz；高阻输出下，DC 到 10MHz 可以做到 20Vpp，10MHz 到 20MHz 为 14Vpp，20MHz 到 30MHz 为 10Vpp。输出阻抗 50Ω，内部参考时钟是 10MHz TCXO，后续也规划外部 10MHz 参考输入。

项目现在处在 MVP 调优阶段，README 里写得比较清楚：PCB 已经打样，MCU/FPGA 核心程序验证完成，可以通过 SCPI 控制输出，模拟前端还在继续调。10MHz 正弦波 FFT 结果里，作者根据示波器数据估算 THD 大约 -60.2dBc，SFDR 大约 63.26dBc，不过也说明了示波器自身谐波会影响结果，最终还得用频谱仪复测。

![arbwave30 waveform generator — 图片 2](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-02.webp)

![arbwave30 waveform generator — 图片 3](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-03.webp)

硬件分成控制板和模拟板。控制板用 STM32F411CEU6，主要做 USB 通信、SCPI 解析、参数下发、EEPROM 设置存储和调试接口。USB 这边当前走 USB CDC，后续文档里也提到 USBTMC 的方向。控制板还负责把 24V 输入转成多路电源，给模拟板提供 +17V、-17V、+7V、-7V 和数字 3.3V。

![arbwave30 waveform generator — 图片 4](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-04.webp)

模拟板才是这个项目最硬核的部分。FPGA 选的是高云 GW2A/GW2AR-LV18，LQFP-144 封装，负责 DDS、波形 ROM/RAM、幅度控制、相位控制、DAC 并口时序和模拟前端控制。DDS 核使用 48bit 相位累加器，所以频率分辨率可以做到很细。DAC 当前选型是 AD9747，16bit、最高 250MSPS、双通道，项目里当前只用一路，实际采样时钟按 150MSPS 使用。

![arbwave30 waveform generator — 图片 5](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-05.webp)

时钟部分使用 CDCI6214，输入来自 10MHz TCXO，输出 150MHz LVDS 给 DAC，同时给 FPGA 提供时钟。这个地方其实很关键，信号源最后能不能干净，很大程度上看时钟和模拟前端。文档里也写了 CDCI6214 的 RMS 抖动目标、外部参考输入、10MHz 同步输出等设计。

![arbwave30 waveform generator — 图片 6](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-06.webp)

DAC 输出不是直接怼到接口，而是走一条完整的模拟链路：I/V 转换、7阶椭圆低通重构滤波器、差分转单端、衰减网络、输出放大级。重构滤波器设计截止频率 60MHz，通带波动小于 0.5dB，115MHz 抑制大于 60dB。这个滤波器明显优先照顾正弦波指标，所以方波边沿会受群延时影响。README 里也提到，当前 5MHz 方波约有 13.5% 过冲，后面要继续优化通道设计。

![arbwave30 waveform generator — 图片 7](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-07.webp)

差分转单端部分也写得很细。文档里按 50Ω 输入阻抗和 6V/V 增益推了电阻值，反馈电阻约 560Ω，输入电阻约 93.1Ω，并且还提到因为通道 1 走线方便，运放输入和 DAC 输出做了反向连接，所以软件里需要对数据反相。这个细节挺真实，很多项目文档不会写到这么细。

![arbwave30 waveform generator — 图片 8](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-08.webp)

输出级规划用 THS3095，目标是驱动到 ±10V 高阻负载。电源也相当复杂，模拟板上有 ±15V、±5V、3.3V_A、1.8V_A、1.8V_D、1.0V_D 等多路电源。3.3V_A 和 1.8V_A 使用 TPS7A4701、TPS7A9101 这类低噪声 LDO，给 DAC、时钟和模拟部分供电；FPGA 内核 1.0V 则用 TPS62933。对一台信号源来说，电源不是附属模块，很多噪声问题最后都能追到这里。

![arbwave30 waveform generator — 图片 9](/uploads/arbwave30-waveform-generator/arbwave30-waveform-generator-09.webp)

主要器件可以简单列一下：

| 模块 | 器件 |
| --- | --- |
| MCU | STM32F411CEU6 |
| FPGA | Gowin GW2A/GW2AR-LV18 |
| DAC | AD9747BCPZ |
| 时钟发生器 | CDCI6214 |
| SPI Flash | GD25Q32 |
| 差分转单端 | LMH6609 |
| 输出功率级 | THS3095 |
| 共模反馈 | NE5532 |
| 模拟低噪声 LDO | TPS7A4701、TPS7A9101 |
| DC-DC | TPS54360、TPS62933 |
| EEPROM | M24C64 |

这个项目最值得看的地方，不是“我也要照着做一台”，而是它把一台信号源从系统架构、器件选型、时钟、电源、滤波器、模拟链路、SCPI、测试脚本，一层一层摊开给我们一个最直观的展示。

目前它还不是成品仪器，作者也明确写了 MVP 阶段、模拟前端仍在调优、精确指标需要更专业仪器复测。但正因为还在调，反而更有参考价值。真正做过高速模拟和混合信号的人都知道，30MHz 信号源看起来频率不高，麻烦的地方在 DAC 时钟、滤波器群延时、电源噪声、运放稳定性、PCB 回流路径和输出级散热。
