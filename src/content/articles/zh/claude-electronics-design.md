---
locale: zh
translationKey: claude-electronics-design
pubDate: '2026-11-11'
updatedDate: '2026-11-11'
category: hardware
draft: false
contentType: deep
series: ai-hardware
author: EmbeddedNote
sourceUrl: https://www.anthropic.com/research/claude-electronics-design
title: "Claude 把电路板画完了"
description: "Anthropic 让 Claude Fable 5.2 从提示词做到 PCB、外壳和固件，三台原型由 Diode 制造并测试。本文拆开看它做对了什么、还有什么没验证。"
tags:
- Claude
- Anthropic
- AI 硬件
- PCB 设计
- KiCad
- DFM
- 原型开发
- CAD
seoTitle: "Claude Fable 5.2 画 PCB：从提示词到三台电子原型"
seoDescription: "Anthropic 称 Claude Fable 5.2 从提示词设计了音箱、语音中枢和掌上宠物，含 PCB、外壳与固件；本文核对公开证据与未验证部分。"
---

Anthropic 让 Claude Fable 5.2 做了三台东西：一个 USB-C 音箱、一个语音助手中枢、一个掌上电子宠物。不是写几段 Arduino 代码，也不是只画原理图；从规格、选型、原理图、PCB 布局布线，到外壳 CAD、固件和 BOM，它全走了一遍，最后 Diode 把板子做出来、装上、测试。三台都能工作，按 [Anthropic 的研究笔记](https://www.anthropic.com/research/claude-electronics-design) 的说法，用了几周也没坏。

![三台由 Claude 设计的电子原型](/uploads/claude-electronics/claude-electronics-hero.webp)

*三台设备：电池供电的掌上宠物、家用语音中枢、USB-C 音箱。图片：Anthropic*

[![Anthropic Claude 电子设计演示视频封面](/uploads/claude-electronics/claude-electronics-video-poster.webp)](https://www.anthropic.com/research/claude-electronics-design)

*Anthropic 公布的演示视频，点封面看原片。*

三台设备都不复杂，但正好覆盖不同的坑。音箱是插在电脑上的 USB-C 圆饼，带麦克风、扬声器、蓝牙和 PCB 天线；语音中枢有 USB 和以太网，放在家里；电子宠物用电池，带屏幕和按键。Anthropic 给的提示词很短，Claude 写规格、挑器件、画原理图、摆器件、拉线，连 3D 打印外壳和固件一起做。它不是在真空里干活，能调 KiCad 的路由器、读数据手册，Diode 提供设计环境和制造能力。

![Claude 的外壳、PCB、固件和装配关系](/uploads/claude-electronics/claude-electronics-design.webp)

*同一套流程里，外壳、PCB、固件和装配都要对上。图片：Anthropic*

![从提示词到能亮机的八个动作](/uploads/claude-electronics/claude-electronics-flow-zh.webp)

*从提示词到能亮机，八个动作。最后一步仍然是人的制板、装配和测试。*

真正变的是几何推理。以前的模型摆器件像随手放，退耦电容离芯片老远，连接器方向都能反；Fable 5.2 会先处理高速、大电流和噪声敏感的路。语音中枢的 USB 和以太网差分对，它一对一对拉，长度和间距都照顾，还加蛇形补偿；电源部分按电流路径重新摆。Diode 的 PCB Gym 上，Fable 5.2 拿到 69%，上一代 Fable 5 只有 25%。这个分数是厂商自己跑的，不是第三方复现，但差距不是一点。

![Diode PCB Gym 分数与 API 成本](/uploads/claude-electronics/claude-electronics-benchmark.webp)

*Diode PCB Gym 的分数与 API 成本。Anthropic 自己做的对比，不是第三方复现。*

更能说明问题的是它会推翻自己。音箱板有四层，触摸轮下面不能随便打过孔，它把两颗芯片的信号改到别的引脚，让触摸区下的线留在一层，不交叉；板子背面挤了，它又换引脚、重画一角，而不是硬加过孔。语音中枢的麦克风走线，它发现电源线绕着地环、前层线跨过音孔周围的地环，直接判断“这有风险”，删掉重拉。Anthropic 说它反复几十次，直到找到能走通的路。以前的模型经常做到 95% 就卡死，差的 5% 正好是能不能做出来的区别。

![语音中枢麦克风走线前后对比](/uploads/claude-electronics/claude-electronics-routing.webp)

*语音中枢麦克风走线的前后对比：电源线不再绕地环，前层线也不再跨过音孔。图片：Anthropic*

它还会用工具。KiCad 自带的路由器一次只拉一根，遇到 100 针连接器就很慢，Claude 写了一个网格搜索的布线器，半小时左右跑通，长线大约一秒一根。它会读充电芯片的数据手册，回答“不放电池只插 USB 会不会工作”，还预判充电灯会闪。DFM 检查里，它把六处太细的阻焊开窗加宽，没动器件；检查器误报的地连接，它判断不影响性能后忽略。外壳也不是摆样子：音箱的静音开关会撞后壁，它算出板子要斜 25 度推进去再放平；语音中枢的麦克风孔 25mm 会在 3.4kHz 共振，它把外壳改成楔形，孔缩到 10mm，共振推到 8.9kHz。

![音箱的四层 PCB](/uploads/claude-electronics/claude-electronics-speaker-pcb.webp)

*音箱的四层板。触摸轮下面保持单层走线，蓝牙天线区清空。图片：Anthropic*

![语音中枢的四层 PCB](/uploads/claude-electronics/claude-electronics-hub-pcb.webp)

*语音中枢的四层板，地铜铺在高速线背面。图片：Anthropic*

![音箱外壳的 25 度装配路径](/uploads/claude-electronics/claude-electronics-enclosure.webp)

*音箱的板子不能直着放进去，静音开关会撞后壁；Claude 算出斜 25 度推进再放平。图片：Anthropic*

但别急着把“AI 硬件工程师”喊出来。三台都是原型，Anthropic 自己写得很清楚：没做电气验证、天线调谐、热测试，也没过认证，不是为量产设计的。Claude 没有接测试仪器，也没有接贴片机，板子和整机是 Diode 的人做出来、测出来的；所谓“没有返工”，是 Anthropic 和 Diode 的说法，这篇能核对的只有公开的研究笔记、图片和演示视频，KiCad 工程、BOM、测试报告和第三方拆解都没有。PCB Gym 是 Diode 的内部基准，BenchCAD 2.1 虽然公开，但 83.5% 这个分数也只说明它更能从图纸重建 3D 和板子，不等于能保证信号完整性。

对嵌入式工程师来说，这事的意义不在“AI 会不会抢饭碗”，而在它能接掉哪些活。摆器件、拉电源、查阻焊、对 BOM、把外壳和板子对一遍，这些活占掉很多时间，又容易在细节上翻车；如果模型能把第一版做到可制造，人就可以把精力放在架构、器件选型、测试和认证上。Anthropic 下一步想让它做更密、更快的板，接仿真，再用实测数据反哺。真到那一步，硬件团队的工作方式会变，但“谁对最终产品负责”不会变。
