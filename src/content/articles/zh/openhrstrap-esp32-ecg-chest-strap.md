---
title: Github上有趣嵌入式项目——基于ESP32的开源心率胸带OpenHRStrap
description: OpenHRStrap使用XIAO ESP32-S3与AD8232采集ECG信号，结合Pan–Tompkins算法与BLE心率服务，公开电路、代码和跑步测试数据。
locale: zh
translationKey: openhrstrap-esp32-ecg-chest-strap
pubDate: '2026-10-23'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/MilosRasic98/OpenHRStrap
tags:
- OpenHRStrap
- ESP32-S3
- AD8232
- ECG
- Pan–Tompkins
- BLE
- 开源项目
seoTitle: OpenHRStrap开源心率胸带：ESP32、AD8232与Pan–Tompkins
seoDescription: OpenHRStrap使用XIAO ESP32-S3与AD8232采集ECG信号，结合Pan–Tompkins算法与BLE心率服务，公开电路、代码和跑步测试数据。
---

跑步党对心率带应该都不陌生，Polar、Garmin一根胸带几百上千，卖点不外乎比手环的光学心率准。但真要论起来，这类心率胸带通过电极采集微弱的ECG生物电信号，再根据R峰计算心率，与手环常见的光学PPG测量原理不同。开源项目OpenHRStrap就是冲着这事去的：ESP32主控加AD8232前端，通过电极测量真实生物信号，过滤信号，并应用Pan–Tompkins算法检测R峰并计算心率，并且一整套软硬件全开源。

项目地址：[OpenHRStrap GitHub 源码与设计资料](https://github.com/MilosRasic98/OpenHRStrap)

MIT协议，作者Milos Rasic的目标写得很清楚：  测量心电图信号并据此计算心率 通过BLE连接到手机，就像商业产品一样。

V1版走的是纯模块拼装路线，新手也能复刻：主控用Seeed的XIAO ESP32-S3开发板，算力和BLE都够用；模拟前端选的是最经典的AD8232 ECG模块，胸带上额外缝了一颗纽扣电极当参考电极；外壳PLA加TPU打印，电源用一颗1S锂电加5V升压小板。原理图直接给了，电池、开关、升压、AD8232、ESP32，一眼看完，照连就行。

![OpenHRStrap开源ECG心率胸带成品实物](/uploads/openhrstrap/openhrstrap-cover.webp)

*OpenHRStrap V1原型，使用3D打印外壳。*

![OpenHRStrap V1电池AD8232和XIAO ESP32原理图](/uploads/openhrstrap/openhrstrap-02.png)

*V1原理图：电池、开关、5V升压模块、AD8232、XIAO ESP32，电源和信号通路一目了然。*

![OpenHRStrap胸带设备和电极安装设计图](/uploads/openhrstrap/openhrstrap-03.png)

*作者画的硬件设计图，模块和胸带的安装位置都标了。*

心率算法选的是Pan-Tompkins，1985年Jiapu Pan和Willis J. Tompkins那篇"A Real-Time QRS Detection Algorithm"提出的，QRS检测的祖师爷级算法。处理管线是带通滤波（低通加高通）→微分→平方→移动窗积分，输出两条信号，一条FILT一条INT，分别维护动态阈值TH1和TH2，阈值靠信号峰SPK和噪声峰NPK的实时估计来更新。检测逻辑也讲究：INT峰过了TH1，就在FILT信号里找时间上对应的峰，满足两路峰值判定条件才计为R峰，否则按噪声峰处理。最厉害的是search-back机制，超过1.66倍RR平均间隔还没检测到R峰，算法就用TH2回头重扫，把漏检的峰捞回来。作者把整套算法用Python实现，严格照着原论文的滤波链写，还配了一张手绘流程图，把阈值逻辑画得明明白白。

![Pan–Tompkins心电QRS检测算法流程图](/uploads/openhrstrap/openhrstrap-04.png)

*作者手绘的Pan–Tompkins流程图，滤波链、阈值、search-back都在上面。*

数据流这块，仓库里每一步都放了实测图：原始ECG进来先过带通滤波，把基线漂移和肌电噪声压下去，再微分放大QRS的斜率，平方后把低幅噪声压掉，最后移动窗积分把波形包络拉出来，一路从原始信号看到最终检测结果。作者用Python对80多秒的预录静态数据进行分析，约漏检一个R峰，前10秒用于参数初始化；这一结果不能直接代表跑步时的实时检测精度。

![OpenHRStrap采集的原始ECG波形](/uploads/openhrstrap/openhrstrap-05.png)

*原始ECG信号，整段采集波形。*

![经过带通滤波后的ECG波形](/uploads/openhrstrap/openhrstrap-06.png)

*带通滤波之后，基线漂移明显减小。*

![移动窗积分之后的ECG曲线](/uploads/openhrstrap/openhrstrap-07.png)

*移动窗积分后的MWI信号，波形包络更清晰。*

![Pan–Tompkins算法检测到的R峰](/uploads/openhrstrap/openhrstrap-08.png)

*INT信号上的R峰检测结果，显示了动态阈值和检测峰。*

实战测试是戴着它跑了个5公里，同时戴一块PPG手表作参考对照，数据从Strava导出来用Python分析，脚本仓库里都给了。起步阶段两边读数贴得很近，心率上去了差距开始拉开，整体看DIY设备报得偏低。作者自己分析，V1没有数据记录功能，看不到算法实际干了啥，只能猜原因，这也正是V2要上定制PCB和数据记录的原因。有一说一，这段测试交代得挺实在；不少设备只强调准确率，他倒是大大方方承认自己设备的短板。

![OpenHRStrap与PPG手表在5公里跑步中的心率对比](/uploads/openhrstrap/openhrstrap-09.png)

*5公里实测，PPG手表与DIY胸带的心率对比。*

![ESP32心率胸带记录的整段心率变化](/uploads/openhrstrap/openhrstrap-10.png)

*DIY设备记录的整段心率数据。*

作者还在[element14社区](https://community.element14.com/challenges-projects/element14-presents/project-videos/w/documents/71995/build-your-own-esp32-fitness-heart-rate-monitor-tracker----episode-692)分享了项目。固件提供标准BLE心率服务（UUID 0x180D），不需要私有心率传输协议；具体App是否支持连接仍取决于其外设兼容策略，不能保证所有运动App都能直接使用。2025年11月还更新了一版更亲民的方案，XIAO板加AD8232模块直接搭，静态数据上Pan-Tompkins表现很好，跑动中的实时检测还在打磨。

缺点方面：V1版，跑起来之后的实时检测稳定性不如静态数据；缺少原始ECG与算法状态日志，导致跑动中的问题难定位；而且项目明确声明不是医疗设备，不做诊断用途，免责声明写得清清楚楚。V2版作者说正在路上，定制PCB、升级模拟前端、正式的数据记录，已经在征集意见了。整体看下来，OpenHRStrap对想搞懂ECG采集和Pan-Tompkins原理的人来说是个很不错的起点，原理图、代码、实测数据全都在仓库里摆着，照着做一台的成本也不高。

资料与图片：[OpenHRStrap GitHub 项目](https://github.com/MilosRasic98/OpenHRStrap)（Milos Rasic）；[Pan–Tompkins 原始论文](https://www.robots.ox.ac.uk/~gari/teaching/cdt/A3/readings/ECG/Pan+Tompkins.pdf)。
