---
title: Github 上超酷嵌入式项目：个人开源的带大模型推理的 2U 小卫星
description: KENSAT 2U 小卫星方案用 PIC24 管理电源与故障恢复，Jetson Orin Nano 运行 TinyLlama，并通过 UHF 回传结果。
locale: zh
translationKey: kensat-2u-cubesat-llm
pubDate: '2026-07-02'
category: hardware
tags:
- CubeSat
- Jetson Orin Nano
- TinyLlama
- UHF
draft: false
seoTitle: Github 上超酷嵌入式项目：个人开源的带大模型推理的 2U 小卫星
seoDescription: KENSAT 2U 小卫星方案用 PIC24 管理电源与故障恢复，Jetson Orin Nano 运行 TinyLlama，并通过 UHF 回传结果。
---

KENSAT小卫星它不是常见的“ESP32 加块屏幕”“树莓派接个摄像头”那类小制作，而是一颗 2U CubeSat。比较离谱的是，作者Ken Chan把 Jetson Orin Nano 和量化后的 TinyLlama 放进这颗小卫星，让它在轨道上自己跑推理，再把结果通过 UHF 链路传回地面。

这个项目完成度也还很高，Github仓库里面有 OBC 飞控、Radio Board、EPS、电热丝天线释放板、Jetson daemon、ADALM-Pluto 地面站脚本，连 KiCad 原理图和 PCB 都放出来了。

![kensat 2u cubesat llm — 图片 1](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-01.webp)

Github地址:

https://github.com/kenchangh/kensat

https://www.kensat.com/

![kensat 2u cubesat llm — 图片 2](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-02.webp)

该项目作者Ken Chan把一个看起来很科幻的想法，拆成了一堆非常具体、非常脏活累活的嵌入式问题：电源怎么控、Linux 挂了怎么办、射频怎么匹配、卫星出舱后天线怎么放出来、推理结果怎么下传、飞控死了怎么自救。

## 核心器件

| 模块 | 核心器件/方案 | 作用 |
| --- | --- | --- |
| OBC 飞控 | PIC24FJ256GB210 + Pumpkin PPM D1 | 常开主控，管遥测、射频、电源、Jetson 和状态机 |
| AI 负载 | Jetson Orin Nano 8GB + TinyLlama 1.1B Q4_K_M | 在轨推理，按日运行，完成后结果下传 |
| UHF Radio | Si4463 + AS179-92LF | 437.08 MHz 收发，遥测、命令和推理结果下传 |
| EPS 电源 | 2S2P 18650 + 遥测 + 硬件看门狗 | 供电、电池监控、飞控失效后的整星重启 |
| 天线释放 | 卷尺偶极子 + 鱼线 + 冗余镍铬丝 | 出舱后释放 UHF 天线，状态写 Flash |
| 地面站 | ADALM-Pluto SDR + AX.25 解码脚本 | 接收 beacon、遥测和 LLM 输出 |

## 项目结构：PIC24 常开，Jetson 平时断电

KENSAT 的结构很像一叠夹心饼干，从下往上是 Pumpkin MB + PPM D1、EPS 电源板、Radio Board + Jetson Payload，最上面是 Burn-Wire 天线释放板。板卡之间走 104-pin CubeSat Kit Bus。

![kensat 2u cubesat llm — 图片 3](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-03.webp)

底层 OBC 用的是 PIC24FJ256GB210，跑飞控、控制遥测、控制 Si4463、控制 EPS 心跳，也管 Jetson 上下电。

很多做边缘 AI 的项目，会下意识把 Jetson 当“大脑”，但一颗小卫星不能这么玩。Jetson 功耗高、启动慢，Linux 也没法保证永远不挂，放在桌面上死机了还能重启，放到 520km 左右的太阳同步轨道上，就没人能给你拔插电源了。

所以 KENSAT 的思路是：PIC24 常开，Jetson 平时断电。只有到了每天一次的推理窗口，PIC24 才拉高 IO.16，打开 +5V 负载开关，给 Jetson 上电。推理完，拿到结果，再让 Jetson 关机，然后直接切电。简单来说就是GPU 只是任务负载，MCU 才是兜底系统。

## 大模型如何跑：READY、RUN、DONE逻辑

Jetson 这边也没有搞得花里胡哨，仓库里的 jetson 目录写得比较清楚：硬件是 NVIDIA Jetson Orin Nano 8GB，系统是 JetPack 6 / L4T R36.4.4，模型是 TinyLlama 1.1B 的 Q4_K_M 量化版本，推理用 llama.cpp。

OBC 和 Jetson 之间走 UART，9600 8N1。慢是慢了点，但这条链路不传图片，不传模型，只传 prompt ID 和一段推理结果，够用了。

每天自动跑一次。Prompt 预先存在 Jetson eMMC 里，最多 20 条。PIC24 不碰 prompt 内容，只发一个编号，比如 RUN:05。Jetson 读 /opt/kensat/prompts/05.txt，跑完 TinyLlama 后回 DONE:和正文。

冗余设计方面，Jetson 60 秒内不回 READY，PIC24 硬切 5V；120 秒内不回 DONE，也硬切 5V。Jetson 的 rootfs 还设成只读，减少硬断电把 eMMC 搞坏的风险。

## 无线：Si4463 + AS179

KENSAT 用 UHF 做通信，频点写的是 437.08 MHz，Radio Board 的核心是 Silicon Labs Si4463，TX/RX 通过 AS179-92LF 射频开关切到同一根天线。遥测、命令、LLM 推理结果，最后都要从这条链路下去。

![kensat 2u cubesat llm — 图片 4](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-04.webp)

把射频部分单独拎出来，结构其实不复杂：Si4463 负责收发，AS179 负责天线口在 TX/RX 之间切换，TX 和 RX 各自做阻抗匹配。

该项目没有停在“芯片接天线”这一步。仓库里专门有 radio/rf-design，作者用 scikit-rf 写了匹配网络优化脚本，对能买到的电感电容做离散搜索，还把 2 层 FR4 上的 CPWG 走线寄生算进去了。

![kensat 2u cubesat llm — 图片 5](/uploads/kensat-2u-cubesat-llm/kensat-2u-cubesat-llm-05.webp)

仓库里还放了 ADALM-Pluto 相关脚本，用来做 RX/TX、频扫、IQ 采集、AX.25 解码和端到端测试。也就是说，它不是只做了一块“看起来像无线电”的 PCB，而是把地面测试链路也搭了起来。

## 电源和热管理

把 LLM 放上天，听起来最难的是模型。实际看 KENSAT，真正要命的是功耗和热。

Jetson 推理时大概是 15–25W 级别，这对桌面设备不算夸张，但对 2U CubeSat 很敏感。太空里没有空气对流，风扇没有意义，热只能靠导热和辐射走。KENSAT 的做法是让 Jetson 的散热面通过导热垫接到铝合金结构上，把结构件当热容和散热路径，同时把推理窗口压短，系统文档里写的 Jetson 总上电时间大约 45–90 秒。

电源板用 2S2P 18650 电池组，给整星供电，同时通过 I²C 给 PIC24 回传电压、电流、温度等遥测，EPS 还带硬件看门狗：PIC24 每 60 秒喂一次心跳，EPS 180 秒收不到，就把 +5V_SYS 拉掉再恢复，强制整星重启。

## 天线释放

KENSAT 的天线释放方案也挺有意思。UHF 天线不是复杂机构，而是卷尺钢片做半波偶极子。发射前，卷尺天线被鱼线绑在机体上；出舱后，PIC24 等 120 秒，再拉高 IO.24 和 IO.25，让两路冗余镍铬丝发热，烧断鱼线，卷尺靠自身弹性弹开。

这块有点“手搓”意味，但 CubeSat 场景下很合理：少电机、少齿轮、少机构卡滞。Burn-Wire 状态还会写入 Flash，成功后不再重复触发；如果中途掉电，也限制最多重试 3 次。

这个项目酷，不是因为它用了 Jetson，也不是因为 TinyLlama 多先进。Jetson 很多人用，TinyLlama 也不是新东西。KENSAT 酷在它把这些普通器件放进了一个很不普通的约束里：小体积、小电池、真空散热、不可人工维护、低速链路、强故障恢复。

桌面上跑一次 LLM，失败了最多重启程序。卫星上跑一次 LLM，失败可能意味着电源被拖垮、飞控被卡死、热量散不出去、下传窗口错过。KENSAT 的每一个子系统，几乎都是围绕“别让 Jetson 拖死整星”来设计的。
