---
title: Github上有趣嵌入式项目——Apollo H-3圣诞雪人挂饰，37颗灯珠分五个区，还能当蓝牙代理
description: Apollo H-3 是一块雪人造型的 ESP32-C6 开源圣诞挂饰 PCB，37 颗 WS2812 分成五区，还能通过 ESPHome 接入 Home Assistant 并作为蓝牙代理。
locale: zh
translationKey: apollo-h3-christmas-ornament
pubDate: '2026-10-29'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/ApolloAutomation/H-3
tags:
- Apollo H-3
- ESP32-C6
- ESPHome
- Home Assistant
- 蓝牙代理
- 圣诞节
- 开源项目
seoTitle: Apollo H-3圣诞雪人PCB：37颗RGB灯珠、ESPHome与蓝牙代理
seoDescription: 拆解Apollo Automation H-3圣诞雪人挂饰：ESP32-C6、37颗WS2812、五区灯效、六首铃声、ESPHome固件和Home Assistant蓝牙代理。
---

圣诞挂饰大家见得多了，塑料壳一串灯，插电就闪，坏了就扔。Apollo Automation这个开源智能家居团队不一样，把挂饰直接做成了一块雪人造型的PCB，正面排了37颗可独立控制的RGB灯珠，帽子、身体、眼睛、鼻子、嘴巴五个区域分开控制，还带蜂鸣器放圣诞歌。这是他们第三年的年度慈善挂饰，全部利润捐给CASA of Lexington（替家事法庭里遭受虐待忽视的儿童发声的机构）和Open Home Foundation。

![Apollo H-3 2026圣诞雪人PCB挂饰，37颗灯珠分五个控制区域](/uploads/apollo-h3/apollo-h3-cover.webp)

*Apollo H-3 圣诞雪人挂饰，37 颗 RGB 灯珠组成五个控制区域。*

主控用ESP32-C6，乐鑫的RISC-V内核，2.4GHz Wi-Fi 6和蓝牙低功耗（BLE），8MB Flash。37颗灯是WS2812，串在GPIO3一根线上，蜂鸣器在GPIO6，RTTTL格式的曲子由GPIO6的PWM输出驱动蜂鸣器；三颗按键接在GPIO4/5/7，每个按键短按播放一首，长按或双击可以切到另一首（固件长按阈值约1.2秒），出厂预装六首：Frosty the Snowman、Rudolph the Red-Nosed Reindeer、Jingle Bells，另三个组合可播放Blue Christmas、Do You Want to Build a Snowman，还有一首画风突变的Barbie Girl，每首歌配一套灯效。可通过USB-C或两节AA电池供电，支持深睡眠和按键唤醒。使用电池时应遵循官方电池选型建议，不要默认充电电池可以直接替代。

![Apollo H-3 雪人造型 PCB 产品正面实物图](/uploads/apollo-h3/apollo-h3-product-photo.webp)

*雪人造型的 PCB：帽子、脸部和身体由灯珠组成不同灯区。*

项目仓库：[ApolloAutomation/H-3](https://github.com/ApolloAutomation/H-3)。

Smart固件基于ESPHome开发，YAML配置公开在仓库里。出厂刷的是Basic固件，纯挂饰模式；刷成Smart固件就能接Home Assistant，自动识别成灯光设备，五区灯效随便改，歌曲也是在线编辑，RTTTL字符串粘贴进去就换歌。它还兼任蓝牙代理和蓝牙追踪器，扔在客厅顺便帮HA扫周围的蓝牙设备。配网可以连接设备提供的“Apollo H3 Hotspot”热点并填写Wi-Fi密码，也支持通过蓝牙Improv方式配置，过了官方"Made for ESPHome"认证。想来回刷固件，网页版安装器直接搞定：https://install.apolloautomation.com/#/h-3 。

![Apollo H-3 白底雪人 PCB 产品图](/uploads/apollo-h3/apollo-h3-pcb-white.webp)

*雪人 PCB 的正面设计，眼睛、鼻子、嘴巴和身体都有灯珠。*

![Made for ESPHome 标识](/uploads/apollo-h3/apollo-h3-esphome-badge.webp)

*H-3 已列入 Made for ESPHome 设备目录。*

灯珠分区这代最香。身体24颗、帽子5颗、嘴巴5颗、眼睛2颗、鼻子1颗，Home Assistant里能单独把鼻子调成红色、眼睛调成蓝色，配自动化还能让它跟门铃、氛围灯联动，来消息闪一下眼睛。板子背面有BOOT和RESET两个按键。按照目前的Smart固件配置，RESET按住约10秒才触发恢复出厂，短按并不是清除配置。Wiki和Discord都开着，社区讨论挺热闹，固件持续更新，最近几个版本加了All Lights总控实体、切歌防重叠这些改动。

短板也得说。这是年度慈善款，库存和售卖状态可能变化，购买前得看官方商店；蓝牙持续扫描会提高能耗，电池供电时尤其要注意；项目主打ESPHome生态，想扒出来当裸Arduino工程玩的话资料基本没有，不过整套YAML就是现成的ESPHome学习样本，灯带、蜂鸣器、按键、深睡、OTA、Improv配网全流程都齐。

**项目资料：** [GitHub 开源仓库](https://github.com/ApolloAutomation/H-3) · [ESPHome 设备介绍](https://devices.esphome.io/devices/apollo_automation_h-3/) · [官方 Wiki](https://wiki.apolloautomation.com/products/h3/introduction/) · [网页固件安装器](https://install.apolloautomation.com/#/h-3)。
