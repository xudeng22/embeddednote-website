---
title: Meshtastic：基于 LoRa 的开源离网 Mesh 通信与 GAT562 手持终端
description: 从 LoRa 中继、加密消息、硬件选型到 GAT562 手持设备，了解 Meshtastic 如何搭建无需蜂窝网络的开源 Mesh 通信系统。
locale: zh
translationKey: meshtastic
pubDate: '2026-10-10'
category: open-source
tags:
- GitHub
- Meshtastic
- LoRa
- Mesh Network
- Off-Grid
- GAT562
draft: false
author: EmbeddedNote
sourceUrl: https://meshtastic.org/
seoTitle: Meshtastic 开源 LoRa Mesh 通信：原理、设备与 GAT562
seoDescription: 了解 Meshtastic LoRa Mesh 通信架构、端到端加密、节点中继、频段注意事项、支持的开发板与 GAT562 手持终端。
---

没有蜂窝网络和 Wi-Fi，手持设备之间还能互相发消息吗？**Meshtastic** 给出了一种开源方案：通过低功耗 **LoRa** 无线电构建 Mesh 网络，让节点互相转发短消息，并可选择共享定位信息。

这套系统面向徒步、户外活动、社区通信及需要脱离常规基础设施运行的场景。它不是卫星通信，也不是传统移动电话网络；可用距离取决于地形、天线、频段、发射功率和节点位置。

![Meshtastic LoRa 节点与手机连接示意](/uploads/meshtastic/meshtastic-01.webp)

## Meshtastic 的主要能力

- **多跳 Mesh 中继**：节点之间转发消息，扩大网络可覆盖的范围。
- **离网文本通信**：无线消息不依赖蜂窝运营商或互联网连接；具体设备能否脱离手机操作取决于是否具备独立屏幕及输入方式。
- **加密通道**：支持共享密钥的频道通信和私有消息；应按当前协议文档理解其安全边界。
- **定位选项**：带 GNSS 的设备可在配置允许时发送位置。
- **灵活供电**：手持节点可以使用电池，固定节点还可以结合 USB 或太阳能供电。

原稿提到 MartinR7 与 alleg 曾达到 **331 公里**的通信记录。这样的纪录依赖特殊视距和无线条件，不能当作普通手持设备的日常通信距离。

项目入口：[Meshtastic GitHub](https://github.com/meshtastic)；[Meshtastic 官网](https://meshtastic.org/)。

## 节点如何工作

Meshtastic 固件运行在兼容的 LoRa 设备上。节点收到需要转发的消息后，可以按网络路由规则再次广播，使消息通过一跳或多跳到达更远处的设备。它适合低速、短消息传递，并非用来替代宽带数据链路。

手机并不是所有场景下都必需。部分节点可以独立显示和输入消息；没有完整交互界面的节点通常通过 Bluetooth 连接手机，用 iOS 或 Android 应用配置和收发消息。还可以使用 Web 客户端及其他配套工具。

无线频段必须按实际国家或地区设置。**北美常用 902–928MHz，欧洲有 868MHz 等配置**，相关发射功率、占空比和设备认证限制各不相同。原稿提到国内设备可用 470–510MHz，并称无需许可；这一说法不能直接推导为该整个频段在中国大陆均可免许可自由使用。部署前应查询当地无线电主管部门要求及具体设备的核准情况。

## 支持的硬件

Meshtastic 生态包含多种现成开发板与便携设备，原稿列出的例子包括：

- RAK Meshtastic Starter Kit（RAK19007 + RAK4631）
- Seeed Card Tracker T1000-E
- Heltec LoRa V3
- Nano G2 Ultra、Station G2
- LILYGO LoRa T3-S3

![LILYGO Meshtastic 开发板照片](/uploads/meshtastic/meshtastic-02.webp)

不同设备的射频前端、频段、天线接口、屏幕、GNSS 和电池配置并不一样。具体兼容情况请以[官方硬件设备列表](https://meshtastic.org/docs/hardware/devices/)为准。

## 天线和客户端同样重要

![便携与手持 LoRa 天线选型参考](/uploads/meshtastic/meshtastic-03.webp)

![基站及汽车 LoRa 天线选型参考](/uploads/meshtastic/meshtastic-04.webp)

天线需要与设备工作频段匹配；把 868MHz 天线直接用于 915MHz 系统，或忽略馈线损耗与安装环境，都可能明显影响通信效果。

Meshtastic 提供 Android、iOS 和 Web 客户端，生态中也有 Meshtastic UI、命令行工具以及 Meshtasticator 等模拟工具。

![Meshtastic 软件客户端入口](/uploads/meshtastic/meshtastic-05.webp)

![Meshtastic 图形用户界面示例](/uploads/meshtastic/meshtastic-06.webp)

![Meshtastic 软硬件操作流程图](/uploads/meshtastic/meshtastic-07.webp)

## 面向初学者的 GAT562 手持终端

如果只是想体验 LoRa Mesh，购买开发板、焊接外围电路、刷入固件并不一定是每个人都愿意做的准备工作。原稿进一步介绍了 **GAT562 Mesh Trial Tracker**：一款将 LoRa 无线电、天线、电池和显示屏集成在一起的便携设备，目的就是减少装配和设置工作。

该项目在 GitHub 公开了 **PCB Gerber 文件及 BOM**，并以兼容 Meshtastic 软件为目标：[quhyhao/GAT562](https://github.com/quhyhao/GAT562)。下面保留原稿的外观、特性以及参数配图。

![GAT562 Mesh Trial Tracker 产品图](/uploads/meshtastic/meshtastic-08.webp)

![GAT562 特性与 Mesh 通信图](/uploads/meshtastic/meshtastic-09.webp)

![GAT562 手持设备技术参数表](/uploads/meshtastic/meshtastic-10.webp)

需要注意的是，GAT562 不同配置及销售批次的频段、固件与认证状态应以对应版本资料为准。对于需要实际部署的用户，先核对本地无线电规定，再决定设备型号和天线，往往比单纯追求最大通信距离更重要。
