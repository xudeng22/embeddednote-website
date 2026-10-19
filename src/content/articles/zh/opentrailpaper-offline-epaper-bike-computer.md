---
title: Github上超实用的嵌入式项目：把LILYGO墨水屏开发板改成一台离线骑行码表
description: OpenTrailPaper 将 LILYGO T5 E-Paper S3 Pro 改造成离线骑行码表，支持 GPS、GPX 导航、离线地图、FIT 记录及蓝牙骑行传感器。
locale: zh
translationKey: opentrailpaper-offline-epaper-bike-computer
pubDate: '2026-09-08'
category: open-source
tags:
- OpenTrailPaper
- ESP32-S3
- LILYGO
- 电子纸
- 骑行码表
- 开源项目
draft: false
seoTitle: OpenTrailPaper：基于 ESP32-S3 与电子纸的离线骑行码表
seoDescription: 开源项目 OpenTrailPaper 将 LILYGO 4.7 英寸电子纸开发板改造成支持离线地图、GPX 导航和 FIT 记录的骑行码表。
---

拿到一块带GPS、LoRa和电子纸的ESP32-S3开发板，大多数人第一反应是拿它做个天气站或者电子书阅读器。

OpenTrailPaper偏偏往硬骨头上啃：把LILYGO T5 E-Paper S3 Pro直接改造成一台能脱离手机运行的骑行码表，离线画地图、跟着GPX路线走、把每一圈记录写成FIT文件，还要接心率带和功率计。

![OpenTrailPaper 骑行码表显示功率、速度、心率、踏频、骑行时间与里程](/uploads/opentrailpaper/opentrailpaper-cover.webp)

功率、速度、心率、踏频、骑行时间和里程一屏显示

Github地址：

https://github.com/RaemondBW/OpenTrailPaper

T5 E-Paper S3 Pro的核心是ESP32-S3-WROOM-1模组，芯片型号ESP32-S3N16R8，双核LX7最高240MHz，配8MB PSRAM和16MB SPI Flash。屏幕是4.7英寸电子纸，960×540、16级灰阶，叠了一层GT911电容触摸，驱动IC是ED047TC1。无线部分除了ESP32-S3自带的2.4G Wi-Fi 4和蓝牙5.0，板上还塞了一颗SX1262 LoRa模块，支持433/868/915MHz三个频段，定位芯片是u-blox MIA-M10Q或者Quectel L76K，固件会自动识别装的是哪一颗。此外还有PCF8563实时时钟、BQ25896充电管理配BQ27220电量计，一颗3.7V 1500mAh电池，官方说法是不开前灯大约能撑八小时以内，作者也标注了这个数字后续可能还会优化，整机尺寸129×69×11mm，比手机也厚不了多少。

![LILYGO T5 E-Paper S3 Pro 主板和引脚接口示意图](/uploads/opentrailpaper/opentrailpaper-hardware.webp)

## ESP32干实时的活，手机干配置和搬运的活

OpenTrailPaper把骑行中需要实时响应的部分——GPS定位、速度和传感器采集、路线导航提示、地图渲染、骑行记录写入SD卡——全部放在ESP32-S3这一端，脱离手机也能跑完整趟骑行。手机端反而是干重活的地方：iOS用SwiftUI写，安卓走Jetpack Compose目前还在Discord邀请制内测，负责搜索目的地、规划路线并把GPX发给设备、生成离线地图瓦片、把设备上录好的骑行记录拉回来复盘，以及修改设置和推送固件更新。这种切法的好处很直接：骑到没有信号的山里，手机app可以直接退出，码表照样按已经加载好的路线和地图继续工作。

地图这块处理得比较讲究，用的是H3六边形网格组织瓦片，生成方式有三条路：在手机app里画框生成、用一段Python脚本在终端跑，或者直接在支持Web Serial的浏览器里用JS现场生成再通过USB下载到SD卡。上手门槛最低的是直接打开项目官网的设置页面，用浏览器把固件刷进去，再按流程把某个区域的地图瓦片存进SD卡根目录下的/maps/tiles。骑行记录固定落地成FIT文件，和结构化训练用的.erg/.mrc文件放在同一层数据组织里，没有互相搅在一起。

![OpenTrailPaper 离线地图生成与电子纸导航显示](/uploads/opentrailpaper/opentrailpaper-maps.webp)

左：浏览器里生成离线地图瓦片；右：转弯提示叠在电子纸地图上的实拍效果

## 传感器和续航

码表通过蓝牙连接心率带、功率计和踏频传感器，ANT/ANT+的支持放在了另一个独立仓库esp32-ant里，还在推进中，仓库说明里写得很明白了 ——这块目前不算完工状态。整个项目大量用了AI（Claude）辅助写代码，但作者反复强调是有人盯着、有人测试的，不是甩手扔给模型自动生成。

![OpenTrailPaper 手机端路线规划、骑行记录和设置界面](/uploads/opentrailpaper/opentrailpaper-companion.webp)

手机端三个主要界面：规划路线、复盘骑行记录、调整设置与推送固件

## 方案的边界

作者自己列出的短板挺实在：T5 S3 Pro不防水，雨天骑行建议套个自封袋；没有气压计，爬升数据是从地图瓦片的高程信息估算出来的，不是实测；GPS是单频模块，定位速度和抗干扰能力比不上多频方案；没有磁力计，地图方向完全靠行进方向推算，人一停下来朝向就不准了；机身实体按键偏小，戴冬季手套或者手心出汗时，触摸屏操作也不算顺手。电子纸本身强光下好读、静态画面几乎不耗电，这些限制换来的是骑行时真正看得清数据和地图，这笔账在户外场景下是划算的。

硬件不用自己攒，直接买LILYGO官方的T5 E-Paper S3 Pro整机，中国淘宝上比较便宜，Amazon上大约90美元，AliExpress上103美元左右；下单时选普通固件版本就够。仓库采用Apache-2.0协议，截至9月7日在GitHub上大约146颗star，还处在快速迭代期。
