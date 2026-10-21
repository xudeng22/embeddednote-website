---
title: 'M5Stack 把 4.7 寸电子纸做成 DIY 套件，原理图也放出来了'
description: 'M5Stack PaperDIY 提供 4.7 英寸 960×540 灰度电子纸、ESP32-S3、可拆装外壳和开放原理图，解析并口驱动、电源控制及两种套件售价。'
locale: zh
translationKey: m5stack-paperdiy-esp32-s3
pubDate: '2026-10-21'
category: display
tags:
  - M5Stack
  - ESP32-S3
  - 电子纸
  - PaperDIY
  - 硬件设计
draft: false
seoTitle: 'M5Stack PaperDIY：4.7 英寸电子纸 DIY 套件与完整原理图'
seoDescription: 'M5Stack PaperDIY 的 4.7 英寸电子纸、ESP32-S3、8 位并口、电源管理和开放原理图解析。Assembly Kit 售价 25 美元，Complete Kit 29.90 美元。'
---

M5Stack 最近上架的 PaperDIY，第一眼看着像一块普通的电子纸开发板。点开套件清单，才发现它把屏、主板、电池、亚克力板甚至外壳都拆开卖了。Assembly Kit 给的是屏幕、主板、电池和亚克力压板，得自己装；Complete Kit 已经装进 3D 打印外壳，到手可以直接写程序。两者核心电路相同，区别主要在结构。想做桌面日历、低功耗信息牌，或者给自己的设备换一块像样的显示屏，这套东西比从零画板省事得多。尤其是电子纸的排线、电源时序和固定方式，一开始就有人替你处理好了。

[![PaperDIY 完整版电子纸出厂测试画面](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_Complete_Kit_main_pictures_07.webp)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_Complete_Kit_main_pictures_07.webp)

*PaperDIY Complete Kit 运行出厂测试程序。图片：M5Stack。*

[![PaperDIY Assembly Kit 拆件](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1287/K159-PaperDIY-Assembly-Kit_main_pictures_02.webp)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1287/K159-PaperDIY-Assembly-Kit_main_pictures_02.webp)

*Assembly Kit 的电子纸、亚克力压板、主板与电池。图片：M5Stack。*

它用的是 4.7 英寸电子纸，分辨率 960×540，支持 16 级灰度。这里有个容易看漏的地方：屏幕没有触摸层，也没有旧款 M5Paper 上的那些传感器。取舍很直接，把它当显示终端用就行，交互靠两颗用户按键或外接模块。主控是 ESP32-S3-WROOM-1-N16R8，带 16 MB Flash、8 MB PSRAM，Wi-Fi 和蓝牙低功耗也都在。板上留了 microSD 卡座、USB-C 和两组 12 针 FPC 扩展接口，SPI、I2S 等信号从这里引出。140 mAh 电池容量不大，适合做间歇刷新、平时休眠的应用；若准备让 Wi-Fi 常开、屏幕频繁刷新，还是得先量实机电流。比如做每日更新的天气牌、课程表，屏幕大部分时间可以不动；要做不断联网刷新的行情屏，供电方案就得另算。官方给出的工作电流约 40.95 mA、峰值可到 161 mA，这不是整机续航数字，别拿 140 mAh 直接一除就估使用天数。

[![PaperDIY Complete Kit 正面](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_Complete_Kit_main_pictures_02.webp)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_Complete_Kit_main_pictures_02.webp)

*Complete Kit 正面，带预装的 3D 打印外壳。图片：M5Stack。*

[![PaperDIY 控制板接口和器件](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1287/K159-PaperDIY-Assembly-Kit_main_pictures_06.webp)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1287/K159-PaperDIY-Assembly-Kit_main_pictures_06.webp)

*主板近照，可见扩展 FPC、microSD、USB-C 与用户按键。图片：M5Stack。*

翻到原理图，最有意思的不是 ESP32-S3 本身，而是显示连接方式。PaperDIY 没走常见的 SPI 小屏方案，屏幕数据口用 8 根 GPIO 并行传输，控制线另外占了几根引脚。官方引脚表把 DB0 到 DB7 对到 GPIO6、14、7、12、9、11、8、10；时钟、锁存等信号还占用 GPIO16、15、13、18、17。整机框图把主控、电子纸、电源管理、TF 卡和两路扩展口都画在了一页上，找信号流向很方便。也正因为并口吃引脚，移植自己的外设前最好先对照引脚表，不要只看“ESP32-S3 还有多少 GPIO”。microSD 用到的 GPIO39、38、40 也出现在外部 SPI 接口上，挂设备时还得考虑片选和总线共用。

[![PaperDIY 电源状态框图](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche_01.png)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche_01.png)

*官方原理图第 1 页：系统框图与各电源工作状态。*

[![PaperDIY ESP32-S3 电子纸并行总线原理图](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche_02.png)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche_02.png)

*第 2 页：ESP32-S3 主控与电子纸并行数据线。*

电源部分也值得看。板上的 M5PM1 负责整机电源状态管理，图纸里能看到配套的 PY32L020F15U6；电池充电使用 LGS4056，主控 3.3 V 由 SY8089 提供，另有一路常供电 3.3 V。电子纸所需的升压另放在显示页，用 MT3608 等器件完成。这样的分区很实用：休眠时不必让整块屏的高压电路跟着耗电，要刷新时再打开相关电源。官方引脚表里，EPD_PWR 由电源管理单元的 PYG2 控制，升压使能 BST_EN 则交给 ESP32-S3 的 GPIO46。官方还把出厂、待机、深睡和工作等状态列进框图，查待机功耗时可以直接按图找使能信号。做自己的固件时，这两路开关最好先照着示例程序走，屏幕没反应不一定是排线的问题。

[![PaperDIY 充电与电源管理原理图](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche_03.png)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche_03.png)

*第 3 页：USB 输入、电池充电、电源管理与稳压电路。*

[![PaperDIY 电子纸电源和 microSD 原理图](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche_04.png)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche_04.png)

*第 4 页：显示供电、microSD 与扩展接口。*

软件不用从空白工程起步。M5Stack 放出了基于 ESP-IDF 的出厂测试程序源码，能测电池电压、扫 Wi-Fi、读写 TF 卡、检查按键；Arduino 侧有 M5Unified、M5GFX 和 M5PM1 支持，官方文档现在也给出了 UiFlow2 教程。刷机也有个小细节：插上 USB-C 数据线后长按电源键约两秒，看到红灯闪烁再松手，设备才进入下载模式。真要做产品，先跑一遍出厂程序，再改显示界面，会少掉不少“是硬件没焊好，还是程序没配对”的排查时间。

M5Stack 官方商城 2026 年 10 月 21 日的标价是：Assembly Kit（K159）25 美元，Complete Kit（K159-B）29.90 美元，均不含运费和可能产生的税费，价格和库存以购买页面为准。完整版的 PLA 外壳尺寸约 120×68.2×6.3 mm，官方还提供外壳模型文件，想改开孔或者支架可以从现成结构下手。背面有 M2 安装位，不过官方特别提醒螺丝伸入的螺纹长度要小于 3 mm，否则可能顶坏屏幕。电子纸项目经常是软件还没写完，先在装配环节吃亏；这个尺寸最好下单前就记住。

[![PaperDIY 完整套件背面](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_Complete_Kit_main_pictures_08.webp)](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_Complete_Kit_main_pictures_08.webp)

*Complete Kit 背面与安装孔。图片：M5Stack。*

**资料链接：**[Assembly Kit 官方资料](https://docs.m5stack.com/en/core/PaperDIY_Assembly_Kit) · [Complete Kit 官方资料](https://docs.m5stack.com/en/core/PaperDIY_Complete_Kit) · [完整原理图（PDF）](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1288/K159-B_PaperDIY_sche.pdf) · [ESP-IDF 出厂测试源码](https://github.com/m5stack/M5PaperDIY-UserDemo) · [Assembly Kit 官方售价](https://shop.m5stack.com/products/paperdiy-assembly-kit-esp32-s3) · [Complete Kit 官方售价](https://shop.m5stack.com/products/paperdiy-complete-kit-esp32-s3)
