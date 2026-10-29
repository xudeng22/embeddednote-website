---
title: Github 上超硬核嵌入式项目：伯克利开源人形机器人 Berkeley Humanoid Lite
description: 伯克利开源人形机器人使用 3D 打印结构、摆线减速 BLDC 执行器、CAN 总线与强化学习，实现低成本可复现设计。
locale: zh
translationKey: berkeley-humanoid-lite
pubDate: '2026-08-31'
category: open-source
tags:
- Robotics
- CAN
- 3D Printing
- Reinforcement Learning
draft: false
seoTitle: Github 上超硬核嵌入式项目：伯克利开源人形机器人 Berkeley Humanoid Lite
seoDescription: 伯克利开源人形机器人使用 3D 打印结构、摆线减速 BLDC 执行器、CAN 总线与强化学习，实现低成本可复现设计。
---

这两年人形机器人项目不少，但大多数离普通开发者比较远，不是买不起，就是资料不全。要么只给你看视频，要么只开一点点代码，真正到了硬件结构、执行器、控制链路、训练部署这些地方，就开始“商业机密”了。

这次这个项目不太一样，它叫 Berkeley Humanoid Lite，来自 UC Berkeley Hybrid Robotics，项目已经开源到 Github。官方给出的目标很直接：做一台成本低于 5000 美元、硬件和软件都能自己折腾的人形机器人。

![berkeley humanoid lite — 图片 1](/uploads/berkeley-humanoid-lite/berkeley-humanoid-lite-01.webp)

Github链接：

https://github.com/HybridRobotics/Berkeley-Humanoid-Lite

项目主页：

https://lite.berkeley-humanoid.org/

这台机器人不是玩具尺寸，也不是那种桌面小摆件。论文里给的数据是：整机约 16kg，高度约 0.8m。躯干里放了计算机、电池和 IMU，四肢关节用模块化执行器驱动。

有意思的是，它没有走“全金属加工 + 定制零件”的路线，而是尽量把结构件压到普通 3D 打印机能做的范围内。非标结构件主要靠 FDM 打印，材料选的是 PLA。不是说 PLA 有多神，而是它便宜、好买、好打印，普通玩家也能复现。

它的核心其实不是“人形”两个字，而是这一套执行器。

![berkeley humanoid lite — 图片 2](/uploads/berkeley-humanoid-lite/berkeley-humanoid-lite-02.webp)

这个执行器里面是 BLDC 无刷电机、摆线减速结构、输出轴、偏心轴、轴承、外壳这些东西。摆线减速的好处是受力不是压在一两个齿上，而是多个齿一起分担，对 3D 打印件友好一些。

如果直接拿塑料齿轮硬怼大扭矩，基本不用想，早晚裂。伯克利这个设计比较务实：能打印的打印，关键受力和定位靠轴承、螺丝、铜柱、输出轴这些标准件兜底。

官方还做了两种执行器尺寸，分别用于不同关节。论文里的 BOM 表很直白，6512 执行器在中国采购成本估算约 157 美元，5010 执行器约 94 美元。

![berkeley humanoid lite — 图片 3](/uploads/berkeley-humanoid-lite/berkeley-humanoid-lite-03.webp)

主要器件方面，电机用了 MAD 系列无人机无刷电机，比如 M6C12、5010 这些；位置反馈用了 AS5600 磁编码器；电机驱动部分用 B-G431B-ESC1 这类基于 STM32G4 的电机控制板；整机控制计算机是 Intel N95 迷你主机，跑 Ubuntu 22.04。

底层通信走 CAN。每条腿、每条胳膊的关节执行器挂在 CAN 2.0 总线上，速率 1Mbps，最后通过 USB-CAN 接到板载计算机。IMU 走 USB 接入，用来提供姿态信息。电池是 6S 4000mAh LiPo，论文里写的续航大概 30 分钟。

按嵌入式视角看，它大概是下图这个结构，所以它不是那种“一个 MCU 控全场”的小车项目，更像是一个分布式控制系统。

![berkeley humanoid lite — 图片 4](/uploads/berkeley-humanoid-lite/berkeley-humanoid-lite-04.webp)

上层 N95 主机负责策略部署、状态融合、运动控制。下面每个关节有自己的电机驱动和编码器，执行器只管把电机闭环跑稳。CAN 总线负责把目标位置、速度、力矩这些东西发下去，再把关节状态收回来。

固件这块也有东西看。官方文档里提到电机控制器需要用 STM32CubeIDE 烧录，电机参数、CAN ID、方向、校准都要配置。第一次上电还要做电角度校准，电机会自己转一圈，这时候执行器必须能自由转动，不然很容易把结构或者驱动搞坏。

软件栈就更机器人味了。仓库里有 IsaacLab 训练环境，有 rsl_rl，有 sim2sim 验证，也有真实机器人部署代码。低层控制代码单独放在 berkeley_humanoid_lite_lowlevel 里，真机部署主要看这部分。官方还给了 Python 和 C 两套运行方式，实际跑机器人时更推荐 C 代码，因为实时性更稳。

这点很真实。仿真里策略跑得再漂亮，真机上 CAN 延迟、USB-CAN 抖动、IMU 噪声、电机温升、电池压降，都会出来找麻烦。

Berkeley Humanoid Lite 最值得看的地方，不是它视频里走了几步，而是它把这些麻烦摊开了。

比如执行器怎么装，磁编码器怎么焊，CAN ID 怎么配，电机怎么校准，N95 主机怎么装依赖，Ubuntu 下怎么拉起 CAN，真机控制脚本怎么跑，这些文档里都有。

最后，这并不是一个适合新手周末随便复刻的项目。它涉及高功率电机、锂电池、多路 CAN、3D 打印承力件、强化学习策略部署。任意一个环节没处理好，都可能烧板、打齿、摔机，甚至伤人。但如果你想研究“低成本人形机器人到底能不能开源化”，这个项目很值得学习。
