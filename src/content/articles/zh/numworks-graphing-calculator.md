---
title: Github上爆燃的嵌入式项目之——图形计算器NumWorks
description: NumWorks 图形计算器采用 STM32F730、320×240 IPS 显示屏与 Epsilon 系统，公开原理图、PCB 布局及软件工程资料。
locale: zh
translationKey: numworks-graphing-calculator
pubDate: '2026-10-20'
category: open-source
draft: false
tags:
- NumWorks
- STM32
- 图形计算器
- 开源项目
seoTitle: NumWorks 图形计算器：STM32F730、原理图与 Epsilon 系统
seoDescription: 拆解 NumWorks 图形计算器的 STM32F730 主控、IPS 显示、QSPI Flash、电源电路、PCB 设计与 Epsilon 软件架构。
---

图形计算器是一个小众市场，主要玩家就卡西欧和德州仪器（TI）两家。这两家的机器大家心里都有数：颜值一般、软硬件迭代慢、系统还捂得严严实实，拆开想动点手脚基本没门。法国公司NumWorks偏偏要在这个市场里搅一搅，2015年成立，做的是第一款把软硬件全部开源的图形计算器，颜值能打，可玩性还高，原理图直接挂在官网上，分享给大家~

项目主页是 https://www.numworks.com

代码在 https://github.com/numworks

Epsilon操作系统和硬件资料全在里面，BOM、原理图、PCB、3D模型、固件源码一个不缺。

硬件规格：320×240的IPS彩屏、140PPI、26万色，1450mAh锂聚合物电池，官方标称续航20小时。

![NumWorks 图形计算器与 The Board 电脑端工具](/uploads/numworks/numworks-cover.webp)

![NumWorks 白色图形计算器的机身设计](/uploads/numworks/numworks-01.webp)

白色机身配圆角按键，颜值在一众计算器里确实突出

![NumWorks The Board 与图形计算器](/uploads/numworks/numworks-02.webp)

先说颜值。卡西欧fx系列和TI那块万年不变的工程黑壳，放在今天确实有点跟不上时代，NumWorks走的是纯白机身、圆角过渡、键帽错落有致的路子，屏幕UI也是现代风格，应用列表加图标，交互逻辑跟智能手机很接近，高中生拿在手里比老古董顺眼太多。

硬件是真开源。原理图PDF直接挂在工程页面，五张A4图纸，PCB的顶层底层丝印铜箔也放出来了，器件清单和每颗料的数据手册链接全部公开。处理器用的是ST的STM32F730V8T6，100脚LQFP，ARM Cortex-M7内核主频216MHz，256KB静态RAM，计算器的大脑和心脏都在这颗芯片上。外置Nor Flash是Adesto的AT25SF641，64Mbit，走104MHz的Quad-SPI总线，固件和用户数据都存在里面。

![STM32F730 MCU 原理图](/uploads/numworks/numworks-03.png)

原理图第1页，STM32F730V8T6核心电路，去耦、复位、启动模式一应俱全

![矩阵键盘及 LCD 接口原理图](/uploads/numworks/numworks-04.png)

第2页是矩阵键盘和16位并口的LCD驱动电路

屏幕模组集成了ST7789V的LCD控制器，接收MCU的位图数据驱动像素矩阵，自带SRAM帧缓冲，16位数据总线，写周期66ns，理论上限能到200fps刷新。电池通过USB充电，充电管理芯片是RT9526A，走恒流恒压（CC-CV）曲线；逻辑电源用一颗RT9078 LDO，3.0到5.5V输入稳压到2.8V给全系统供电。键盘是标准的矩阵扫描，行引脚还能配成待机唤醒。USB口挂了USBLC6-2SC6做ESD浪涌保护，机身里还藏着三颗RGB LED，通过壳体透光，颜色随便调，开机动画就是靠它做的。

![NumWorks 外设、闪存、USB 接口原理图](/uploads/numworks/numworks-05.png)

电源部分：电池电压采样、USB充电、背光电荷泵、逻辑电源

![NumWorks 电源管理原理图](/uploads/numworks/numworks-06.png)

外设部分：RGB LED、外部Flash、USB保护、高速晶振

![NumWorks PCB 顶层布线图](/uploads/numworks/numworks-07.png)

双层板0.8mm，沉金工艺，这是顶层布局

软件是重头戏。Epsilon是NumWorks自己写的图形计算器操作系统，C++开发，直接跑在裸机上，256KB内存要精打细算：栈只留32KB，堆干脆不用malloc，改成静态分配加可回收的GC节点池，官方文档还调侃说这点内存是阿波罗登月电脑的64倍。架构分了五层，从下往上依次是Ion硬件抽象层、Kandinsky图形引擎、Escher GUI工具库、Poincaré数学引擎，最上面再跑各种应用，每层都单独开源，可读性相当好。最关键的是Epsilon可以编译成独立应用程序在PC上跑，不用买计算器，电脑上就能把整套系统跑起来体验。

![NumWorks The Board 图形工具界面](/uploads/numworks/numworks-08.jpeg)

The Board是官方配套的电脑端工具，函数图像、表格、方程求解可以并排看

可玩性方面，Epsilon内置覆盖高中数学课程的应用，还集成了Python解释器，写脚本算函数、做统计都没问题，在线模拟器随时能玩：https://www.numworks.com/simulator/ 。社区也很热闹，Omega、Upsilon这些第三方固件都在活跃开发，还有人在这台计算器上跑马里奥。官方YouTube频道有演示视频：https://m.youtube.com/watch?v=gv-mdriI9iM 。

当然短板也得说一说。屏幕没有触屏，全靠物理按键操作；216MHz的Cortex-M7在今天的处理器面前也不算快。

整体看下来，NumWorks把"好看、好用、愿意把家底全亮出来"三件事凑齐了，对硬件爱好者或者DIY爱好者来说，那份原理图就值回票价。想深入研究的，直接去Github上扒源码就行。
