---
title: Gitlab 上实用嵌入式项目——将树莓派 Pico W 变 USB Wi-Fi 网卡（pico-usb-wifi）
description: pico-usb-wifi 利用 Raspberry Pi Pico W、USB CDC-NCM 与二层桥接，为主机提供无需厂商专用 Wi-Fi 驱动的联网方案，并支持 CDC-ACM 管理。
locale: zh
translationKey: pico-usb-wifi
pubDate: '2026-11-03'
category: open-source
tags:
- Raspberry Pi Pico W
- RP2040
- USB CDC-NCM
- Wi-Fi
- 开源项目
draft: false
sourceUrl: https://gitlab.com/baiyibai/pico-usb-wifi
author: EmbeddedNote
seoTitle: Gitlab 上实用嵌入式项目——将树莓派 Pico W 变 USB Wi-Fi 网卡（pico-usb-wifi） | EmbeddedNote
seoDescription: pico-usb-wifi 利用 Raspberry Pi Pico W、USB CDC-NCM 与二层桥接，为主机提供无需厂商专用 Wi-Fi 驱动的联网方案，并支持 CDC-ACM 管理。
---

pico-usb-wifi 是一套适用于 **Raspberry Pi Pico W** 的开源固件，目标是将 Pico W 变成主机可识别的 **USB 网络适配器**。它并非向电脑暴露无线网卡芯片，而是通过 USB CDC-NCM 呈现以太网接口，由 Pico W 自行管理 Wi-Fi 连接。

**项目仓库：** [baiyibai/pico-usb-wifi](https://gitlab.com/baiyibai/pico-usb-wifi)

![pico-usb-wifi 项目总体示意：Pico W 通过 USB CDC-NCM 向主机提供 Wi-Fi 网络连接](/uploads/pico-usb-wifi/pico-usb-wifi-01.webp)

## 原理：把 Wi-Fi 接入放在 Pico W 一侧

Pico W 内置 Infineon **CYW43439** 无线芯片，由 **RP2040** 处理无线端与 USB 端之间的数据转发。项目实现透明的**二层桥接（Layer 2 Bridge）**，通过 USB CDC-NCM 将网络连接提供给主机。

与常见需要芯片厂商 Wi-Fi 驱动的 USB 网卡不同，该方案让操作系统看到的是 USB 以太网设备。项目设计不引入 NAT，不额外建立私有子网，也不要求配置端口转发；它的目标是让 IPv4 和 IPv6 流量穿过这条桥接链路。

![二层桥接结构图：主机通过 USB CDC-NCM 连接 Pico W，再经 Wi-Fi 接入路由器](/uploads/pico-usb-wifi/pico-usb-wifi-03.webp)

## CDC-ACM：连接和调试不占用数据通道

固件另外提供 **USB CDC-ACM** 串口，用于扫描热点、连接无线网络、保存 Wi-Fi 凭据及调试。这样，网络数据与管理控制台可以走不同的 USB 功能接口。

原文所说的“无需驱动”，准确地说是**无需额外安装厂商专用 Wi-Fi 驱动**；主机仍然需要可用的 CDC-NCM、CDC-ACM 类驱动。不同操作系统及版本的实际兼容性，应以项目说明和实机测试为准。

## 项目特性

- Pico W 无线网络与 USB 接口之间的透明二层桥接。
- USB CDC-NCM 网络接口，以及 CDC-ACM 管理、调试串口。
- 面向 IPv4 与 IPv6，不额外引入 NAT、私有子网或端口转发规则。
- 支持 WPA2-PSK、WPA3-SAE 及开放网络（具体能力以当前固件和设备配置为准）。
- 项目资料给出的平均吞吐量约为 **4.75 Mbit/s**；这是项目报告数值，并非本站独立测试结果。

![Raspberry Pi Pico W 通过 USB 连接笔记本电脑的示例桌面场景](/uploads/pico-usb-wifi/pico-usb-wifi-02.webp)

## 适合什么场景？

如果你需要给某台不便安装专用无线驱动的主机补上网络连接，或希望把 Wi-Fi 配置与认证集中在外部小设备上，这个项目值得研究。需要注意，它依赖 Pico W 的无线链路和 USB 功能实现，并不等同于面向高吞吐场景的商用 Wi-Fi 网卡。
