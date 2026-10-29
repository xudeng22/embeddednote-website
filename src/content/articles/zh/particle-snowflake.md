---
title: 'Github上有趣嵌入式项目——Particle官方开源雪花灯：P2模组加36颗灯珠，会说"sparkle"'
description: 'Particle Snowflake是一款圣诞雪花造型的开源PCB，采用P2模组、36颗RGB灯珠、麦克风与扬声器，还能通过本地关键词识别触发灯效。'
locale: zh
translationKey: particle-snowflake
pubDate: '2026-10-28'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/particle-iot/snowflake
tags:
  - Particle Snowflake
  - Particle P2
  - 圣诞节
  - RGB LED
  - 边缘AI
  - 开源硬件
seoTitle: 'Particle开源圣诞雪花灯：P2、36颗RGB灯与Sparkle语音触发'
seoDescription: '拆解Particle Snowflake开源圣诞PCB：RTL8721DM、36颗可寻址RGB灯、PDM麦克风、TPA6211A1音频功放，以及Edge Impulse本地语音识别。'
---

圣诞装饰这几年被各路DIY玩家玩明白了，但大部分作品都是ESP32加灯带拼出来的，软件各写各的，Particle这家做物联网云平台的公司不一样，直接把自家P2模组做成了圣诞装饰，还把设计资料开源，还特意取了名叫Snowflake，一片雪花形状的PCBA，插上USB-C就亮，官方口号是"给节日装饰加点闪烁和旋律"。

![Particle Snowflake雪花造型PCB正反面](/uploads/particle-snowflake/particle-snowflake-cover.webp)

*雪花造型PCB，左侧为正面，右侧为背面。图片：Particle*

GitHub地址：[https://github.com/particle-iot/snowflake](https://github.com/particle-iot/snowflake)

主控是Particle P2模组，里面是Realtek RTL8721DM这颗料，Arm Cortex-M33核心，双频WiFi加BLE，在IoT模组里是非常经典的，整片板子上最有意思的是36颗WS2812B/SK6812E RGB灯珠，3535反贴封装直接焊在PCB上，雪花六个枝干各排几颗，灯带数据线过了74AHC1G125做3.3V到5V电平转换，这是为了提高5V灯珠的数据电平裕量。发声这块用TPA6211A1，一颗标称3.1W的AB类功放推板载扬声器，唱圣诞曲靠它。

除了灯和喇叭，这板子还塞了不少活：MP34DT05TR-2，ST的PDM MEMS麦克风，直接挂在P2的PDM接口上；触摸按键用了TTP223加PT2041A双方案，板上RTL8721自己也带电容触摸引脚，三保险；供电是XC6228D331MR的3.3V LDO，USB-C 16pin接口进来，旁边APX803L做复位和VUSB监测，还有NTC温度检测电路，可以监测板上温度。

![Particle Snowflake PCB正面灯珠分布](/uploads/particle-snowflake/particle-snowflake-front.webp)

*雪花造型PCB正面，灯珠沿六条枝干排列。图片：Particle*

玩法是这么设计的：插上电36颗灯珠就自己闪灯效，按一下正中央的Particle logo切下一套光效，长按logo放圣诞曲。固件带有预置歌曲及MP3音频资源。这还只是开胃菜，官方网页工具更新固件后，在启用语音触发功能的配置下，对着它说"sparkle"，灯就会切换到特殊闪烁效果，这是拿Edge Impulse训练的语音识别模型，固件里直接嵌了TensorFlow Lite Micro跑推理，关键词识别在设备本地运行，不需要把音频上传云端。

![Particle Snowflake官方原理图](/uploads/particle-snowflake/particle-snowflake-schematic.png)

*官方原理图全貌，P2主控、PDM麦克风、触摸与电源一页看全。图片：Particle*

仓库东西给得相当全。hardware目录里原理图PDF、BRD布线文件、BOM Excel、丝印层的Illustrator源文件都有，还有一堆器件数据手册，照着就能打板；firmware目录是整个工程源码，neopixel驱动、clickButton按键库、音频播放、MP3资源全在里面，Edge Impulse SDK也一并放了；media目录还挂了官方灯效演示视频：https://github.com/particle-iot/snowflake/raw/main/media/Snowflake_Action.mp4 。许可证Apache 2.0，遵守许可条款就可以修改和再分发，官方还留了扩展口，PCB上焊盘可以再串一条外部WS2812灯带，教程里甚至教你怎么把它改造成时钟。

![Particle Snowflake PCB背面与模组](/uploads/particle-snowflake/particle-snowflake-back.webp)

*PCB背面，焊盘预留外部灯带接口。图片：Particle*

![Particle Snowflake官方灯效演示画面](/uploads/particle-snowflake/particle-snowflake-lights.webp)

*官方灯效演示视频画面。图片：Particle*

缺点方面，这是节日限量款，不是长期供应的标准开发板，想复刻只能自己打板，而且P2模组在国内渠道不像ESP32那么好买，得走Particle官方或海外代购；触摸按键靠着logo那么小的触点，戴手套按容易没反应；板载小喇叭音质就那样，听个响；PDM麦克风是裸数据输出，想要更准的语音识别还得自己调模型。

资料来源：[Particle Snowflake GitHub仓库](https://github.com/particle-iot/snowflake) · [Particle官方说明](https://www.particle.io/snowflake/) · [P2模组技术资料](https://docs.particle.io/reference/datasheets/wi-fi/p2-datasheet/)。
