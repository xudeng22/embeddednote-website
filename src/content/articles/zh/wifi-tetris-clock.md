---
title: Github上有趣嵌入式项目——用俄罗斯方块报时的WiFi时钟
description: Brian Lough 的 WiFi 俄罗斯方块时钟用 ESP32、64×32 RGB 矩阵屏、PxMatrix 和 ezTime 实现方块下落报时，附接线图与供电建议。
locale: zh
translationKey: wifi-tetris-clock
pubDate: '2026-10-23'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/witnessmenow/WiFi-Tetris-Clock
tags:
- ESP32
- Wi-Fi
- 俄罗斯方块时钟
- RGB LED矩阵
- PxMatrix
- HUB75
- 开源项目
seoTitle: ESP32 俄罗斯方块 WiFi 时钟：64×32 RGB矩阵屏与开源接线方案
seoDescription: 介绍 ESP32 WiFi Tetris Clock 的64×32 P3 RGB矩阵屏接线、PxMatrix/TetrisAnimation、ezTime联网校时和5V供电选型。
---

俄罗斯方块的下落方块，游戏圈没人不认识，但有人拿它来报时。Brian Lough做了个WiFi时钟，时间数字不是画出来的，而是俄罗斯方块一块块落下来拼成的，整块64×32的P3 RGB矩阵屏当表盘，分辨率不高，效果却出奇地抓眼。屏幕物理尺寸19cm×9.5cm，摆在桌面上比任何普通电子钟都醒目，路过的人基本都要多看两眼。

仓库地址 https://github.com/witnessmenow/WiFi-Tetris-Clock 。作者Brian是个软件开发者，爱尔兰人，2016年入坑Arduino，之后在开源圈挺活跃，TinyPICO、ESP8266教程视频都出自他手，还维护了一堆Arduino库。这个项目还在 Instructables 上发布过制作教程。硬件门槛很低：TinyPICO 或通用 ESP32 开发板加 64×32 P3 RGB 矩阵屏，再配作者推荐的 5V/8A 电源、连接线和 3D 打印支架，接线和调试熟练的话装起来并不复杂。

![基于 ESP32 的俄罗斯方块 WiFi 时钟，64×32 RGB 矩阵屏显示 2:32 PM](/uploads/tetris-clock/tetris-clock-cover.webp)

*实拍效果：彩色方块组成时间数字。*

![WiFi Tetris Clock 视频封面，方块下落组成时间数字](/uploads/tetris-clock/tetris-clock-01.webp)

*项目视频截图：俄罗斯方块落下，逐渐拼出 4:30 PM。*

![早期俄罗斯方块 LED 时钟照片](/uploads/tetris-clock/tetris-clock-02.webp)

*另一个演示画面，方块排列成时间。*

![Tetris 风格 WiFi 时钟的彩色方块动画](/uploads/tetris-clock/tetris-clock-04.webp)

*屏幕上停着各种经典方块形状。*

![配有 3D 打印支架的 LED RGB 矩阵屏](/uploads/tetris-clock/tetris-clock-05.webp)

*装好 3D 打印支架的矩阵屏。*

这项目最大的卖点是不用RTC。不少需要离线走时的Arduino时钟会搭配DS3231之类的RTC模块，有时还要手动校时，这里时间直接走WiFi从互联网拿，只设置一次时区，夏令时都自动调整，掉电重启并重新联网后自动对时。固件层面驱动用的是2dom的PxMatrix库，ESP32通过HUB75接口把像素数据刷到矩阵屏上。RGB矩阵屏本来是给演唱会那种大屏设计的拼接单元，单块用单片机也能控制，P3代表像素间距3mm，间距越大整屏物理尺寸越大，64×32就是横向64颗LED、纵向32颗，代码只适配这一种，其他分辨率要自己调。

接线不复杂，README里给了三张接线图，TinyPICO、通用ESP32、D1 Mini ESP8266各一张，电源单独一张，5V电源通过DC母座转螺丝端子接到屏上。作者自己做了一款Matrix Shield转接板，插在开发板上直接把排针引到屏的HUB75接口，省掉一堆飞线。

![TinyPICO 和 HUB75 LED 矩阵连接图](/uploads/tetris-clock/tetris-clock-06.png)

*TinyPICO 接线图，PIN/POUT 的位置清晰可见。*

![通用 ESP32 开发板与 RGB 矩阵屏接线示意](/uploads/tetris-clock/tetris-clock-07.png)

*通用 ESP32 开发板接线。*

![RGB LED 矩阵屏 5V 电源接线与 DC 转接端子](/uploads/tetris-clock/tetris-clock-08.webp)

*电源接线。请按屏幕实际电流需求选择电源；项目 README 推荐 5V/8A。*

这个项目的生态很有意思。还有其他作者基于这个思路扩展出“会说话的俄罗斯方块时钟”，加了个MP3/WAV播放器，数字变化时来点音效，还加了网页界面在线改设置，视频在这：https://www.youtube.com/watch?v=ey2mjZ-UQNM 。在国内，B站UP主心暖爸爸用二手P2.5租赁屏加ESP32复刻过一台，效果相当漂亮。

固件本身也能折腾。方块下落拼数字的效果可以通过修改代码调整，彩色方块也能呈现各种配色。原始示例提供了时区、12/24小时制，以及是否每分钟重画所有数字的配置项；亮度、动画速度这类设置则需要进一步修改驱动或动画代码。数字切换的瞬间特别有游戏感，和呆板的数码管时钟完全是两种气质。3D打印支架在Thingiverse上有现成模型，还有人重混过，装起来就是个桌面小摆件。

缺点方面，64×32的分辨率意味着单个数字笔画很粗犷，凑近看就是马赛克，得拉开点距离才舒服；P3屏全白时峰值电流不小，作者在 README 中推荐 5V/8A 电源，实际电流还取决于亮度和点亮的 LED 数量，别随手拿小功率手机充电头代替；再就是仓库维护节奏一般，仓库 README 仍提示 ESP8266 版本存在崩溃问题，README里的部分链接也旧了。不过对想入门RGB矩阵屏的人来说，这是个实用的入门案例，从接线到跑通全流程都有图有视频，跟着走一遍，HUB75那套时序基本就明白了。

项目源码：[WiFi-Tetris-Clock](https://github.com/witnessmenow/WiFi-Tetris-Clock)（Brian Lough，MIT 协议）。相关库：[PxMatrix](https://github.com/2dom/PxMatrix)、[TetrisAnimation](https://github.com/toblum/TetrisAnimation)、[ezTime](https://github.com/ropg/ezTime)。
