---
locale: zh
translationKey: moto-gps-waveshare
pubDate: '2026-11-10'
category: open-source
draft: false
contentType: deep
series: open-hardware
author: EmbeddedNote
sourceUrl: https://github.com/mx3353672833-debug/moto-gps-waveshare
title: "Github 上硬核嵌入式项目之——摩托车圆屏导航"
description: "MOTO GPS 用微雪 ESP32-S3 圆屏和 iPhone 做摩托车导航：手机算路，圆屏显示，自研 BLE 协议、共享 C++ 核心与 Ø52mm 四层板。"
tags:
- MOTO GPS
- ESP32-S3
- 微雪
- AMOLED
- BLE
- 摩托车导航
- LVGL
- 开源项目
seoTitle: "MOTO GPS：ESP32-S3 圆屏摩托车导航，手机在包里算路"
seoDescription: "MOTO GPS 用微雪 ESP32-S3 1.75 英寸圆屏、iPhone App 和自研 BLE v1 协议做摩托车导航；含 CO5300 引脚、A1 四层板与 LVGL 界面。"
---

车把上装一块 1.75 英寸的圆屏，手机丢进背包，屏幕上只留眼前这一截路：白色路线、下一个转向、还有三百米。不是把手机画面投上去，路线在手机上算，圆屏通过蓝牙接一段裁好的导航状态。项目叫 **MOTO GPS**，作者 Maler X，现在的硬件是微雪 **ESP32-S3-Touch-AMOLED-1.75C**，仓库里除了固件，还有 iOS App、路线网关、共享 C++ 导航核心，以及一块画到四层板的自研主板。写稿时 500 多 star、90 多个 fork，不算爆款，但工程完整度比很多“只放效果图”的项目高。

![MOTO GPS 圆屏导航终端外观效果图](/uploads/moto-gps-waveshare/moto-gps-cover.webp)

*车把上的圆屏只显示当前路段，完整路线留在手机里。图为项目外观效果图，当前实机用的是微雪成品板。*

<video controls muted loop playsinline poster="/uploads/moto-gps-waveshare/moto-gps-nav-poster.webp" style="width:100%;height:auto;border-radius:12px;background:#0b0f12;">
  <source src="/uploads/moto-gps-waveshare/moto-gps-nav.mp4" type="video/mp4">
</video>

*圆屏导航页录屏。路线、距离和限速数字都是演示数据，不是实车路测。*

先把板子说清楚。1.75 英寸 AMOLED，466×466，**CO5300** 走 QSPI；触摸是 **CST9217**；主控 **ESP32-S3**，32MB Flash、8MB PSRAM；六轴 **QMI8658** 管相对转向，电源管理 **AXP2101**。微雪公开原理图的 J3 里，LCD 的 CS、SCLK、D0-D3 分别落在 GPIO12、38、4 到 7，TE 单独走 GPIO13；触摸的 SDA/SCL 在 GPIO15/14，INT 和 RST 是 11 和 2。别小看 TE 这根线，屏幕能亮不代表画得顺，地图快速旋转时能不能把 QSPI 写卡在帧首，靠的就是它。

![MOTO GPS 板级连接图](/uploads/moto-gps-waveshare/moto-gps-board-zh.webp)

*圆屏、触摸、IMU 和 PMIC 的信号归属。引脚依据微雪公开原理图 J3 与项目 BSP，完整设计仍以官方 PDF 为准。*

![微雪 ESP32-S3-Touch-AMOLED-1.75C 原理图 J3 局部](/uploads/moto-gps-waveshare/moto-gps-schematic-j3.webp)

*J3 的屏幕与触摸引脚。LCD_TE 单独接到 GPIO13，触摸走 I²C，另有 INT 和 RST。*

真正值得看的是分工。手机用 CoreLocation 拿定位，搜索和路线走高德，Key 放在自建 HTTPS 网关；完整路线留在手机，共享的 C++ **NavCore** 在手机上跑路线推进、偏航判断和重算。圆屏只收当前视野要用的东西：导航快照、局部路线几何，以及最多 24 条道路、192 个点、16 个建筑、128 个点的背景窗口。终端收到后交给 **NavPresenter**，车头箭头固定，地图在下面平移旋转，再进 LVGL 画出来。ESP32 不重新跑一遍路线状态机，也不碰高德，这个边界划得很干净。

![MOTO GPS 系统数据通路](/uploads/moto-gps-waveshare/moto-gps-system-zh.webp)

*手机负责定位、算路和偏航，圆屏只拿裁剪后的显示投影。*

蓝牙也没有糊弄。ESP32 做 GATT peripheral，手机是 central，自定义服务里 RX 收、TX 发；每帧自带 `0xB7` 魔数、版本、类型、flags、序号、分片偏移、整包长度和 CRC16。MTU 23 的时候一帧只剩 8 字节净载荷，所以分片和重组由协议自己做，不依赖 Long Write。快照最高 5Hz，心跳 1 秒，重组超时 1 秒，要确认的命令 750ms 没回 ACK 就原样重发，最多两次。连接用 LE Secure Connections 加 bonding，Just Works 没有 MITM，作者在文档里写得很直白，没把“加密”吹成身份认证。

![MOTO GPS BLE v1 帧格式](/uploads/moto-gps-waveshare/moto-gps-ble-zh.webp)

*一帧 10 字节头、N 字节载荷、2 字节 CRC；每个分片独立校验，序号 0 保留。*

显示链路有点意思。两片 320 行的 PSRAM 绘图缓冲，QSPI DMA 和 LVGL 绘制交替跑；CO5300 的 TE 接进 GPIO13，用帧首同步把刷新卡在 25ms 的节拍上。屏幕是圆的，466×466 的四个角本来就用不到，UI 把进度弧、转向图标和距离压在下半圆，速度、航向、音乐各占一页，左右滑动切换。实车帧率和快速转向的撕裂感还得看长期测试，仓库没替作者吹这个数。

<video controls muted loop playsinline poster="/uploads/moto-gps-waveshare/moto-gps-speed-poster.jpg" style="width:100%;height:auto;border-radius:12px;background:#0b0f12;">
  <source src="/uploads/moto-gps-waveshare/moto-gps-speed.mp4" type="video/mp4">
</video>

*马表页录屏。大号速度数字、外圈刻度和圆弧一起变化，停车时切页看一眼比掏手机方便。*

![MOTO GPS 四个圆屏页面](/uploads/moto-gps-waveshare/moto-gps-ui-pages.webp)

*导航、速度、航向、音乐四页。界面共用同一份 LVGL 代码，圆屏和 Web 预览只是渲染后端不同。*

仓库里还有一块 **Ø52mm 的四层自研板 A1**：ESP32-S3-WROOM-1U-N16R8、LC76G GNSS、QMI8658A 加 IIS2MDC、BQ25628E 加 TPS63070 和 TUSB320LAI；V3 外壳 Ø61×16mm，卡口对着 Garmin 的四分之一转。听起来很完整，但作者标了 **DO NOT ORDER**，ERC/DRC 全过只说明文件自洽，屏幕 FPC、电源切换、射频和装车振动都没验。现在能跑的是微雪成品板加 iPhone，别把工程候选当成能下单的板子。

![H0175 EVT A1 自研主板](/uploads/moto-gps-waveshare/moto-gps-a1-pcb.webp)

*A1 的 PCB 预览。Ø52mm 四层板，GNSS、IMU、磁力计和充电电源都收在一张圆板上，但仍是工程审阅版本。*

![iPhone App 路线选择页面](/uploads/moto-gps-waveshare/moto-gps-app-routes.webp)

*手机端最多给三条候选路线，比较时间、里程和路况后再把选中路线交给导航核心。*

软件栈是 ESP-IDF 5.5.5、LVGL 9.5.0、微雪 BSP 3.0.0，iOS 17 起，后端 Node，网页用同一份 C++ Presenter 编成 Wasm 预览。离线底图只存道路和建筑，济南包 9.73MiB，四万多条道路、两万多个建筑，搜索、算路、偏航重算仍然要联网。许可证是 **PolyForm Noncommercial 1.0.0**，源码公开但不让商用，卖预装设备得单独找作者。它不是成品，App 也没上架，可这套“手机算路、圆屏显示”的拆法，比堆一长串功能列表更值得看。

<video controls muted loop playsinline poster="/uploads/moto-gps-waveshare/moto-gps-music-poster.jpg" style="width:100%;height:auto;border-radius:12px;background:#0b0f12;">
  <source src="/uploads/moto-gps-waveshare/moto-gps-music.mp4" type="video/mp4">
</video>

*音乐页录屏。圆屏只做显示和上一首/播放/下一首，声音仍走手机当前的音频输出。*

图片与视频来自 MOTO GPS 仓库和 Glimpse 官网，版权归作者 Maler X；原理图片段来自微雪公开资料。
