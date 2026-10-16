---
title: Github 上新晋硬核开源项目之——22 自由度的螃蟹机器人 Jumper，从训练到板端全开源
description: "Jumper 是一款 22 自由度开源机器人。本文分析 RK3576 主控、四足与双钳结构、MuJoCo 仿真训练、ONNX 导出及板端部署。"
locale: zh
translationKey: Open-Source Project - Jumper
pubDate: 2026-10-13
category: open-source
tags:
  - Github
  - 开源机器人
draft: false
seoTitle: 硬核开源项目
seoDescription: 硬核开源项目之——22 自由度的螃蟹机器人 Jumper，从训练到板端全开源
---
今年 7 月 WAIC 上横着走过展台、8 月在 WRC 上跟着热歌跳舞还用钳子夹起一枚冰箱贴递给观众的那只红色小螃蟹，9 月 30 号把软件整个开源了，仓库在 KingKongRobotics/jumper，Apache-2.0。跟多数"开源机器人"只丢一个模型和几段视频不一样，这个仓库把训练、仿真、导出、部署到板端 NPU 的整条链路都放了出来，另外摆了 100 台工程机当比赛奖品——你教它一个新动作，机器归你。

![Jumper 22 自由度开源机器人——项目介绍配图一](/uploads/image.webp)

![Jumper 22 自由度开源机器人——项目介绍配图二](/uploads/image-1.webp)

几乎所有报道都叫它六足，打开仓库里的 MuJoCo 模型文件 assets/jumper/jumper.xml 一数，**其实只有四条腿。22 个自由度是这么分的：前面两只钳子各 5 个 DoF（肩、大臂、小臂、掌、手指），左右各两条行走腿各 3 个 DoF（髋、大腿、小腿），2×5 + 4×3 = 22。**移动类和跳跃策略只观测和驱动其中 20 个，跳过的正好是线序里索引 4 和 9 那两个手指关节——部署文档专门拿一张图讲这件事，因为按索引配对而不是按名字配对，从第五个关节开始就全错，而且不报错，这是那种上机之后才会现形的问题。

![Jumper 机器人——关节结构与自由度分析配图](/uploads/image-2.webp)

**Github地址：**

[https://github.com/KingKongRobotics/jumper](https://github.com/KingKongRobotics/jumper)

主控用的是瑞芯微 RK3576，4×Cortex-A72 @ 2.2 GHz 加 4×Cortex-A53 @ 2.0 GHz，6 TOPS INT8 的 NPU，4 GB 内存配 64 GB 存储，系统上跑 Ubuntu 22.04.5 加 6.1.99 的 PREEMPT_RT 实时内核。22 个关节全用金钢自研的触觉舵机，双磁编码器全闭环、24 位分辨率，一个读电机输出端、一个读减速之后的关节端，还能回传力矩——这是它能做出跳跃动作的前提，只看电机端编码器，控制器压根不知道腿有没有到位。感知这边是 6 轴 IMU、一颗 dToF 深度传感器（54×42 阵列，每帧 2268 个测距点，量程 5 cm 到 8.8 m）、500 万像素对角视场 162.2° 的相机；交互是两块 0.9 英寸圆形 TFT 做的眼睛，加双扬声器和 4 颗 MEMS 麦克风。供电是 25.2 V / 3000 mAh 可拆卸电池，约两小时续航，USB-C PD 3.1 最高 140 W 回血，对一台 1.8 kg 的机器来说相当奢侈。

![Jumper 机器人——硬件配置分析配图一](/uploads/image-3.webp)

![Jumper 机器人——硬件配置分析配图二](/uploads/image-4.webp)

![Jumper 机器人——硬件配置分析配图三](/uploads/image-5.webp)

训练那部分基于 mjlab 和 rsl_rl 的 PPO，物理后端有两个：MuJoCo Warp 走 GPU，默认 4096 个并行环境；原生 MuJoCo 把环境分给多个 CPU 线程。框架只在仿真器那里留了一道很小的缝，manager 和学习层一行不动，所以加机器人加任务都不用碰 scripts/ 下面的代码。命令行就 train.py、play.py、export.py 三个入口，共用一个 parser。

![Jumper 机器人——MuJoCo 仿真训练相关配图一](/uploads/image-6.webp)

![Jumper 机器人——MuJoCo 仿真训练相关配图二](/uploads/image-7.webp)

训出来的 checkpoint 经 export.py 变成 actor.onnx 加一份 layout.json，这份 layout.json 是这个项目里最较真的东西：观测顺序、关节限位、指令量程、动作缩放、参考帧全写在这里。文档里举了两个被打回的例子——关节位置限幅曾经写死 ±3.30，其实是 crate 单元测试留下的占位值，22 个关节里有 20 个的机械限位都在它里面，等于这个钳位每拍都在跑却永远不会触发；摇杆量程写的是 0.80 m/s，而策略训练时只见过 0.50，满舵相当于让策略回答一个从没见过的问题，表现得像"策略跑不快"，实际是配置在撒谎。现在这两个数都改成从 contract 里读，板端遇到没有 joint_limits 的 contract 直接拒绝加载，宁可导出失败也不让一个跑不起来的策略上机。

ONNX 之后走 Docker 里的 onnx2rknn 转成 .rknn 给 RK3576 的 NPU 用，fp16 量化误差 1.1e-3。然后 deploy.py 把 FSM 状态机、每个模式的策略、控制映射和参考轨迹打成一个 bundle 和一个 .app，同一份 Rust controller 分别编译成板端二进制、浏览器 wasm 和 play 用的 Python 扩展，三个宿主读同一个 bundle、各取自己那份。板端那条路径是观测 → NPU → 关节目标 → DDS 发出去，CycloneDDS 11.0.1 配 libmbus 2.4.0，控制环 1 kHz，各模式的推理频率还不一样：行走和跳跃 200 Hz，钳子、舞蹈、手势 50 Hz，中间靠零阶保持加一个与频率无关的 EMA 衔接。顺带说一句，他们连手柄和键盘的"说法"都做成了一本固定词典 controller/vocabulary.json，只描述"A 键按下""左摇杆在 (0.4, −0.9)"，不描述这些意味着什么，词典外的名字在加载时直接被拒——因为一个编出来的控制名能解析、绑不到任何东西，看起来跟"这个键坏了"一模一样。

要说现在还差点什么，仓库自己写得很坦白：rknn 在真机上的推理没验证过，控制环也从来没有真正驱动过电机总线，1 kHz 发布、模式切换斜坡、抖动统计这些没在板子上量过，也没有 SCHED_FIFO 和 mlockall。每一跳都做了校验，最后的坑留给你踩。仓库 README 的用法是把整个项目丢进 AI 编程助手，一句话说你要什么——"给 Jumper 设计一个暖沙色游侠外观并导出 .skin"、"训练一个稳定的三足步态并打包成 .app"，剩下的它照着 AGENTS.md 和几个 skill 一条龙干到底。

![Jumper 机器人——策略部署与AI开发相关配图](/uploads/image-8.webp)

关注公众号"**嵌入式杂谈**"，了解更多有趣好玩的嵌入式信息，感谢大家的点赞，在看。
