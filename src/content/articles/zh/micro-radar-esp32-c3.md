---
title: Github 上超小巧的嵌入式项目：把航班雷达塞进 1.28 寸圆屏里
description: 利用 ESP32-C3、1.28 英寸圆屏和 OpenSky 航空数据制作桌面航班雷达，分析网页配置、轨迹预测及双缓冲显示。
locale: zh
translationKey: micro-radar-esp32-c3
pubDate: '2026-06-22'
category: open-source
tags:
- ESP32-C3
- OpenSky
- GC9A01
- Micro Radar
draft: false
seoTitle: Github 上超小巧的嵌入式项目：把航班雷达塞进 1.28 寸圆屏里
seoDescription: 利用 ESP32-C3、1.28 英寸圆屏和 OpenSky 航空数据制作桌面航班雷达，分析网页配置、轨迹预测及双缓冲显示。
---

航班雷达Micro Radar 的思路很简单：拿一块带 ESP32-C3 的 1.28 寸 240×240 圆形 IPS 模组，接上 Wi-Fi，去 OpenSky 拉附近飞机的状态向量，再在圆屏上画成老式雷达扫线。

![micro radar esp32 c3 — 图片 1](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-01.webp)

Micro Radar不是传统意义上的无线电雷达，也不是 1090 MHz ADS-B 接收机。它不自己收飞机信号，而是把开放航空数据“可视化”成一个桌面小物件。

| 项目名称 | Micro Radar |
| --- | --- |
| 核心硬件 | ESP32-C3 + 1.28 寸 GC9A01 240×240 IPS 圆屏模组 |
| 数据来源 | OpenSky REST API：/states/all |
| 开发环境 | PlatformIO + Arduino framework |
| 开源内容 | 源码、STL/3MF/Onshape 外壳文件、装配说明 |

Github地址

https://github.com/AnthonySturdy/micro-radar

Micro Radar 把几个很小的模块串成了一个完整体验：外壳能打印，前脸有镜片，USB-C 通过延长线引到背面，首次开机会弹出 Wi-Fi 配网热点，联网后还能在浏览器里改经纬度、半径、显示选项和 OpenSky 凭据。

![micro radar esp32 c3 — 图片 2](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-02.webp)

## 项目特点

一块主板撑起全部功能：项目采用带 1.28 寸圆屏的 ESP32-C3 模组，屏幕、主控、无线联网能力都在一块板上。README 强调“no soldering required”，这对复刻者很友好。

用 OpenSky 做“数据雷达”：固件向 OpenSky 的 /states/all 发起请求，通过 lamin、lamax、lomin、lomax 限定一个经纬度盒子，拿到附近飞机的经纬度、速度、航向、高度、呼号等字段。

配置体验比较完整：首次开机通过 WiFiManager 起一个 MicroRadar-Setup 热点；联网后用 microradar.local 访问配置页。经纬度、半径、扫描线、飞机信息文本、航向三角形、OpenSky Client ID/Secret 都能在网页里改。

显示不是静态点阵：源码里用 LovyanGFX Sprite 做 240×240 双缓冲，先画雷达圈和扫描线，再画飞机。飞机的位置不是生硬跳变，TrackedAircraft 里还做了 dead reckoning 和缓动插值。

![micro radar esp32 c3 — 图片 3](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-03.webp)

代码的核心路径很清楚：main.cpp 里初始化屏幕、Wi-Fi 和配置服务器，然后在 loop 中调用 aircraftManager.Update() 拉取数据，再用 backbuffer 绘制雷达 UI。AircraftManager 负责三件事：按额度计算请求间隔、维护 trackedAircraft、把经纬度投影到 240×240 屏幕坐标。

这里有一个小细节挺好：OpenSky 给的数据不是每帧都有，飞机点位如果直接按接口刷新，会有明显跳动。项目里用速度和 true_track 做简单预测，再把上一次显示位置和预测位置做平滑过渡。做法不复杂，但显示观感会顺很多。

## 硬件连接图——一体ESP32-C3 圆屏模组省掉了最麻烦的焊接

![micro radar esp32 c3 — 图片 4](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-04.webp)

LGFX.h 里直接把 GC9A01 面板配置写死了：SPI2_HOST，MOSI 为 GPIO7，SCLK 为 GPIO6，DC 为 GPIO2，CS 为 GPIO10，背光 BL 为 GPIO3，SPI 写频率 27 MHz。对复刻者来说，如果买的是同款圆屏模组，基本按项目来烧录就行；如果换了模组，这几个管脚和屏幕驱动就要重新核对。

![micro radar esp32 c3 — 图片 5](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-05.webp)

## 源码细节

第一个是请求节奏。AircraftManager::Initialise() 里根据 OpenSky 的匿名/登录额度计算 fetchInterval，并且留了 TOKEN_BUFFER。它不是傻乎乎地每秒请求，而是先算今天能请求多少次，再折算成间隔。这个写法适合所有“开放 API + 小屏设备”的项目。

第二个是显示双缓冲。main.cpp 中创建 LGFX_Sprite backbuffer，loop 里先在内存里画完扫描线、雷达圈和飞机，再一次 pushSprite 到屏幕。小屏刷新时，这种方式能减少闪烁，也便于后面加动画。

第三个是状态跟踪。项目按 icao24 维护 trackedAircraft，同一架飞机下次出现时不直接跳到新坐标，而是先记录当前显示位置，再做插值。嵌入式 UI 很多时候不是算力问题，是“细节有没有顺手做掉”。

## 能借鉴什么？

如果只是看“圆屏 + ESP32-C3”，这个项目并不稀奇；真正有价值的是它把一个极窄场景做成了完整桌面摆件。这个项目有两个重要启发：第一，单一场景比大而全更容易让用户理解；第二，配置入口必须简单，不要让用户改代码。

![micro radar esp32 c3 — 图片 6](/uploads/micro-radar-esp32-c3/micro-radar-esp32-c3-06.webp)
