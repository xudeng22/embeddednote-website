---
locale: zh
translationKey: tinytron-esp32-mini-tv
pubDate: '2026-01-15'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/t0mg/tinytron
title: Github 上超能装的嵌入式项目：30 欧元攒一台 ESP32 桌面小电视
description: 微雪 ESP32-S3-LCD-1.69 被改造成一台复古桌面小电视：支持 SD 卡 MJPEG 视频、网页推流、3D 打印外壳和 OTA 更新。
tags:
- ESP32-S3
- tinytron
- Waveshare
- MJPEG
- SD 卡
- 3D 打印
- 开源项目
seoTitle: Tinytron ESP32-S3 桌面小电视：30欧元DIY、MJPEG视频与3D打印外壳
seoDescription: 拆解tinytron开源迷你电视：1.69英寸240×280屏、SD卡MJPEG、网页推流、SPI接线、复古外壳及固件烧录注意事项。
---

拿到一块 ESP32-S3 开发板，大多数人第一反应是做个天气站、联网时钟或者电子相册。tinytron 的作者 t0mg 偏不这么干，他把微雪 Waveshare ESP32-S3-LCD-1.69 开发板装进一台迷你电视里，机身还照着上世纪 90 年代的 TV/VCR 组合机做了一套外壳。它确实能播视频，放在工位上，离远了还真像个缩小了的老电视。

Github 地址：[t0mg/tinytron](https://github.com/t0mg/tinytron)。作者的演示视频也在 [YouTube](https://www.youtube.com/watch?v=HspYfg55T3A)。

![tinytron 复古造型 ESP32-S3 桌面小电视](/uploads/tinytron/tinytron-cover.webp)

*装进 3D 打印外壳的 tinytron，外形参考 90 年代 TV/VCR 一体机。*

项目提供两种看片方式。插上 FAT32 格式的 microSD 卡，把 MJPEG 编码的 AVI 视频和 JPEG 图片放在根目录，开机便按文件名字母序播放，先播放视频，再进入图片轮播；没有检测到 SD 卡时，设备会进入 Wi-Fi 模式，可以从电脑浏览器推送本地视频。它还做了屏幕或窗口镜像功能，不过这里有浏览器安全限制，后面再说。

![tinytron 实际播放 Blender Studio 短片](/uploads/tinytron/tinytron-01.webp)

*SD 卡模式下的播放动画。画面内容为 Blender Studio 的《WING IT!》。*

整机核心是一块微雪 **ESP32-S3-LCD-1.69 非触摸版**，搭载 1.69 英寸、**240×280** 分辨率的 ST7789V2 屏幕。屏幕本身很小，作者倒是把体验做得挺完整：电池供电、网页配网、OTA 升级、显示亮度和屏显信息调节，操作只用一颗实体按键，单击暂停或继续，双击切换到下一个文件，长按开关机。特别要注意，这台小电视**没有声音**。作者为了压低物料和装配复杂度，干脆没有加功放和喇叭。

![tinytron 从侧面展示屏幕和外壳的装配](/uploads/tinytron/tinytron-02.jpeg)

*从侧面看，屏幕被嵌进前盖，后面是带斜度的机身。*

整套硬件主要就是开发板、microSD 读卡器小板和 **3.7V 400mAh 锂聚合物电池**，不插 SD 卡时甚至可以只用开发板通过 USB-C 供电试运行。作者提出的目标是把三项主要物料控制在 **30 欧元以内**，这是他的 DIY 成本目标，不是包含运费、打印服务和人工的固定成品售价。读卡器小板要焊一排 6Pin 排针；电池通常带 PH2.0 插头，但微雪板需要 **JST 1.25mm** 接口，下单前最好直接确认端子。

外壳是另一个好玩的地方。作者拿索尼 KV-14V6D 之类的老电视当参考，在 Onshape 里画了前盖、后盖、边框和按键四个零件。用 PLA 打印，作者在 Prusa MK4S、0.28mm 层高条件下测得约 30 分钟、16g 耗材。边框粘到前盖，其余靠卡扣合拢，几分钟就能装起来。别被外观骗了，公差做得很紧，装屏幕时得靠外壳变形让位，不能掰屏幕；收后盖前还要检查电池有没有被夹住。

![tinytron 3D 打印外壳整体设计渲染](/uploads/tinytron/tinytron-03.webp)

![tinytron 3D 打印外壳四件分解图](/uploads/tinytron/tinytron-04.webp)

*四件式外壳，前后盖、边框与按键都可以分别打印。*

![tinytron 外壳 PrusaSlicer 俯视布局](/uploads/tinytron/tinytron-05.webp)

![tinytron 外壳需要手动加支撑的区域](/uploads/tinytron/tinytron-06.webp)

*切片截图中绿色部分是作者建议补充支撑的位置。*[完整组装视频（约 3 分钟）](https://www.youtube.com/watch?v=-QKKTKMmSjw)。

接线没什么神秘的，SD 卡走 SPI。作者使用开发板自带的排线，只保留所需的六根导线，接到读卡器的 **3V3、CS、MOSI、CLK、MISO、GND**。固件默认的 ESP32-S3 引脚分别是 **GPIO10（CS）、GPIO17（MOSI）、GPIO11（CLK）、GPIO18（MISO）**。不想剪掉多余的线，也能从原接头中退针重排。这个地方一定要反复核对线序：自制插头反插会把 3.3V 和 GND 对调，轻则烧板，重则损坏电池相关电路。原理图没有替代品，复刻时最好对照仓库接线表和 `platformio.ini`。

网页功能也比想象中多。没有 SD 卡时，tinytron 会连接之前配过的 Wi-Fi；连不上就建立名为 `Tinytron-XXXX` 的开放热点，访问 `192.168.4.1` 即可配置网络。连入局域网后，浏览器可以上传本地视频流、调整亮度、OSD 层级、自动关机时间，查看电池电压并做 OTA 更新。首次刷固件和视频转换都有网页工具，不一定要在电脑上搭开发环境。

![tinytron 浏览器视频推流与屏幕镜像界面](/uploads/tinytron/tinytron-07.webp)

![tinytron Wi-Fi、亮度及自动关机设置页面](/uploads/tinytron/tinytron-08.webp)

*网页推流与设置界面，采用复古 VCR 风格。*

视频文件必须是适合这颗芯片解码的 **MJPEG AVI**。项目提供基于 `ffmpeg.wasm` 的浏览器转码页面，转换在本机进行，不需要把原视频上传到远程服务器，作者标注了 2GB 输出文件上限。示例 FFmpeg 参数会去掉音轨，把内容裁成 **288×240、25 fps**，额外的 8 像素宽度是为了符合 JPEG 解码对 16 的倍数更友好的处理路径，并不是说屏幕分辨率变成了 288×240。

这里还有几个复刻前需要知道的限制。屏幕镜像依赖浏览器获取屏幕画面，但 tinytron 端只提供不安全的 HTTP/WebSocket 连接；桌面 Chrome 需要手动把相应来源视作安全来源才可能放行，**这会降低浏览器安全性，不建议随便在日常电脑上打开**。另外，微雪开发板 **V1 与 V2 的电源控制引脚不同**：默认固件按 V2 的 GPIO41/40 配置，V1 要改成 GPIO35/36 再编译；充电过程中设备目前不能关闭。

项目源码以 **MIT** 协议发布，借鉴了 atomic14 的 `esp32-tv` 和 moononournation 的 `MiniTV`，用到 TFT_eSPI、JPEGDEC、ArduinoJson 和 ESPAsyncWebServer。想照着做的可以直接从 [仓库](https://github.com/t0mg/tinytron) 下载外壳与固件，先看[组装视频](https://www.youtube.com/watch?v=-QKKTKMmSjw)，再动手接 SD 卡线路。
