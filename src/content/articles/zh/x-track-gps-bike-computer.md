---
locale: zh
translationKey: x-track-gps-bike-computer
pubDate: '2026-01-15'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/FASTSHIFT/X-TRACK
title: Github 上的高星嵌入式项目之——骑行码表
description: FASTSHIFT 的开源 X-TRACK GPS 骑行码表，支持离线地图、实时轨迹、GPX 导出与 PC 端 LVGL 模拟器，并公开原理图和固件。
tags:
- X-TRACK
- AT32F435
- GPS
- GNSS
- LVGL
- GPX
- 离线地图
- 开源项目
seoTitle: X-TRACK 开源 GPS 骑行码表：离线地图、GPX 轨迹与 AT32F435
seoDescription: X-TRACK使用AT32F435、1.54英寸ST7789、ATGM336H定位和LVGL v8，支持离线地图、GPX轨迹、原理图与PC模拟器。
---

开源自行车码表不少，但把 GPS、离线地图、实时轨迹和完整的软硬件工程一起放出来的并不算多。**X-TRACK** 是 FASTSHIFT（VIFEXTech）做的一台 GPS 骑行码表，放在车把上能看速度、距离、时间、航向以及当前位置，骑完还能导出标准 **GPX** 轨迹。这套工程早在 2021 年就开始迭代，仓库里留有 PCB、固件、GUI、模拟器和地图工具，不是只放几张效果图。

Github 地址：[FASTSHIFT/X-TRACK](https://github.com/FASTSHIFT/X-TRACK)。

![X-TRACK GPS 自行车码表安装在车把上，显示离线地图](/uploads/x-track/x-track-cover.webp)

*X-TRACK 实拍：1.54 英寸小屏上同时显示地图、速度和里程。*

这块小屏是 **ST7789 驱动的 1.54 英寸 240×240 IPS TFT**，通过 SPI 连接主控。主控选了雅特力 **AT32F435CGU7**，最高 288MHz，512KB RAM、1MB Flash；常见配置里配 **ATGM336H GNSS 模块**，支持 GPS、北斗、GLONASS、Galileo 等卫星系统。定位数据既用于计算速度、航向和经纬度，也可以自动校准 MCU 内部 RTC。项目还列有 LSM6DSM 加速度计、LIS3MDL 地磁计、microSD 卡、旋转编码器和 700mAh 锂电池，电源器件包括 LP5907-3.3 与 MCP73831。

![X-TRACK 硬件整体原理图](/uploads/x-track/x-track-02.webp)

![X-TRACK 电源及接口部分原理图](/uploads/x-track/x-track-03.webp)

*原稿中附带的两张原理图。实际焊接请使用官方仓库最新版 PCB 与原理图，放大核对网络名和引脚。*

有点意思的是这项目做的不是在线导航。离线地图会先准备成切片数据放进 SD 卡，设备根据 GPS 当前位置、缩放级别，动态读取需要的瓦片，再由 **LVGL v8** 绘到屏幕上。新版固件常用的地图目录规则是 `/MAP/z/x/y.bin`，坐标系要与地图瓦片对应，系统配置里提供 WGS84 与 GCJ-02 的选项。想拿一张网上的 PNG 地图直接塞进卡里就显示，通常行不通，还要按仓库的工具说明生成匹配的地图数据。

界面交互靠旋转编码器，不需要弄一整排按键。地图可以显示当前位置并缩放，也能把实时行进轨迹画在底图上；运动信息包括速度、距离、时间、卡路里、海拔和航向。轨迹记录成 GPX 文件后，复制到电脑就能用 GPXSee 之类的软件打开，查看历史路线。系统参数保存在 `SystemSave.json` 中，包含上次定位位置、时区和地图目录等，关机时会写入存储卡。

![X-TRACK 设备开机动画](/uploads/x-track/x-track-04.gif)

![X-TRACK 动态速度显示演示](/uploads/x-track/x-track-05.gif)

*开机动画与测速演示。后者是原作者的测试画面，并不代表自行车的正常骑行速度。*

![X-TRACK GPX 历史运动轨迹在 PC 上查看](/uploads/x-track/x-track-06.webp)

*将 GPX 轨迹导入 PC 端软件后查看线路与速度变化。*

项目作者在 README 中给出**常亮连续工作约 4 小时**的参考续航，实际时间会随屏幕亮度、GNSS 接收状态和电池老化变化，别直接当量产设备规格。硬件复刻也有几个必须看的提示：PCB 厚度建议 **0.8 或 1.0mm**，D2 二极管的方向与其他二极管不同，D4 则建议移除以避免充电自动开机。GPS 模块要用文档建议的 ATGM336H，天线不要碰到附近的超级电容。项目硬件指南还说，LSM6DSM 和 LIS3MDL 在部分配置里**可以不装**，有利于减少焊接和物料成本。

对嵌入式工程师来说，另一个实用点是能先在电脑里跑起来。项目使用 **Keil MDK** 构建 MCU 固件，并提供 Visual Studio 的 LVGL PC 模拟器；作者建议使用对应 Artery Pack，模拟器则按 `Release x86` 配置。真正上板前可以先在 PC 里调页面和数据流，尤其是 PageManager 页面生命周期、DataCenter 消息发布订阅机制，以及 GPX/地图切片的处理逻辑。原理图之外，这些代码更值得拿来研究。

开源仓库采用 **MIT** 协议，文件和安装注意事项见 [X-TRACK 项目主页](https://github.com/FASTSHIFT/X-TRACK)、[硬件复刻与排障](https://github.com/FASTSHIFT/X-TRACK/tree/main/Hardware) 和 [软件编译说明](https://github.com/FASTSHIFT/X-TRACK/tree/main/Software)。作者还提供了 [B 站演示视频](https://www.bilibili.com/video/BV1GB4y1K7VV)，以及针对第二代版本的[演示视频](https://www.bilibili.com/video/BV1aS421X779)。
