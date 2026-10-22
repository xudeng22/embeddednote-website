---
title: Github上实用嵌入式项目——配 FLIR 传感器的 WebUSB 热像仪Picothermal
description: Picothermal使用FLIR Lepton 3.5与RP2040制作USB-C热像仪，通过WebUSB直接在浏览器显示160×120热像，公开KiCad原理图、PCB和Rust固件。
locale: zh
translationKey: picothermal-webusb-thermal-camera
pubDate: '2026-10-23'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/icamaster/picothermal
tags:
- Picothermal
- WebUSB
- FLIR Lepton 3.5
- RP2040
- 热成像
- 开源硬件
- Rust
seoTitle: Picothermal：免装App的FLIR Lepton 3.5 USB-C热像仪
seoDescription: Picothermal利用FLIR Lepton 3.5、RP2040和WebUSB，打造免安装专用App的USB-C热像仪，附KiCad原理图、PCB及Rust固件设计。
---

热成像仪这东西，专业的一台大几千，入门货又多是只有一个点的小点温枪，想看插座哪里发热、板子哪里短路、墙里哪根水管漏水，基本没戏。手机热成像模组倒是不少，但基本都要装配套App，哪天App不维护了，硬件跟着变砖。作者Cezar Chirila整了个不走寻常路的方案：热成像相机直接插兼容设备的USB-C口，用支持WebUSB的浏览器打开网页就能看实时热像，专用App一个都不用装。

项目叫Picothermal，开源在GitHub上：[Picothermal硬件项目](https://github.com/icamaster/picothermal)。

MIT协议，硬件、固件、外壳图纸全套公开，核心是FLIR的Lepton 3.5红外传感器加树莓派同款RP2040主控，160×120分辨率、19200个热像素，辐射标定过，能直接读绝对温度，低增益模式下的场景测温范围为-10℃到400℃，水平视场角57°，Lepton模组典型工作功耗约150mW，整机功耗还得另算。

![Picothermal FLIR Lepton 3.5 和 RP2040 USB-C 热像仪实拍](/uploads/picothermal/picothermal-cover.webp)

*整机就这么大，USB-C口插上兼容设备就能用。图片：Cezar Chirila。*

![Picothermal WebUSB 浏览器热成像网页显示效果](/uploads/picothermal/picothermal-webusb.png)

*浏览器里的WebUSB界面，实时热像直接出，不用安装专用App。*

这项目其实是作者的第二版。第一版用的是MLX90640，分辨率只有32×24，768个像素，看个大概行，细节就别想了，这次换Lepton 3.5，分辨率直接翻了25倍，还能测绝对温度，设计思路也很直接：不做屏幕、不做电池、不做存储，手机屏幕当屏幕，手机电池当电池，板子只干一件事，把传感器数据搬到USB上，所以能做得这么小。

硬件全套开源，KiCad工程、原理图PDF、Gerber、装配图、BOM都在仓库里，主板上USB-C接口用的是USB4155-03-C，入口挂了ESD3C3.3ST5G做静电保护，再过一颗MPZ1608S101ATA0磁珠，RP2040配W25Q16JV这颗16Mbit的QSPI Flash存固件，Lepton那边单独给了一颗25MHz的ECS-2520MV-250-CL做主时钟，SWD调试座用的是Tag-Connect的TC2030-CTX。电源页最有意思，USB的5V进来分了四路：两路TLV62569A降压出3.0V@1A和1.2V@1A，两路AP7330 LDO出3.3V@300mA和2.8V@300mA，各轨都留了测试点。PCB打了0.8mm和1.6mm两个厚度，作者最后选了1.6mm的，结实好焊，外壳STL也按两种板厚各出了一版底盖。

![Picothermal 第一页原理图：USB-C RP2040 QSPI Flash Lepton](/uploads/picothermal/picothermal-schematic-main.png)

*原理图第1页：USB-C入口、RP2040、QSPI Flash和Lepton模组。*

![Picothermal 第二页电源原理图：5V降压转换和LDO稳压](/uploads/picothermal/picothermal-schematic-power.png)

*第2页电源：5V进来分四路，两路降压、两路LDO，电压电流都标了。*

![Picothermal PCB 官方装配图](/uploads/picothermal/picothermal-assembly.png)

*官方装配图，照着焊接。*

固件是单独一个仓库 https://github.com/icamaster/picothermal-fw ，Rust加embassy框架写的，作者一开始想用C配TinyUSB，后来没时间，干脆让AI代理把固件整个重写了一遍，他在README里自嘲说代码大概率没法维护，基本都是AI写的。底层把Lepton的驱动抽成了不依赖芯片的no_std库，CCI寄存器读写走I2C，像素流走VoSPI的SPI，驱动和协议都带主机侧测试。刷机也方便，编译好的UF2文件拖进RP2040的bootloader就行，SWD调试用probe-rs，日志走RTT，USB带宽全留给视频，故意没留串口控制台。

玩法核心是WebUSB。Windows上固件用MS OS 2.0描述符自动绑WinUSB，插上就免驱；打开网页应用 https://www.cezarchirila.com/webusb/picothermal.html ，Windows Edge和安卓Chrome已由项目作者测试，其他Chromium浏览器预计可以使用，固件更新在页面里点按钮就行。局限也很实在：只有Chromium系浏览器支持，Chrome、Edge、Opera、Brave等属于兼容目标，Firefox和Safari目前不支持；iPhone、iPad上的浏览器受WebKit限制也用不了，Linux还得先加udev规则。固件还用着pid.codes的共享测试VID/PID，作者提醒自己打板子的人先申请独立PID，免得和别的项目撞车。

作者将USB Video Class（UVC）列为后续可能增加的功能，未来若实现，设备才能像普通USB摄像头那样被其他软件直接调用；当前版本用的是WebUSB。整体看下来，Picothermal把热成像和网页外设凑到了一起，免App的设计思路非常值得借鉴，现在手机装的APP太多了。

项目资料：[硬件设计与外壳](https://github.com/icamaster/picothermal) · [Rust固件](https://github.com/icamaster/picothermal-fw) · [WebUSB网页应用](https://www.cezarchirila.com/webusb/picothermal.html) · [FLIR Lepton 3.5规格](https://oem.flir.com/en-150/products/lepton/?model=500-0771-01&segment=oem&vertical=microcam)。
