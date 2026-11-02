---
title: Github上爆火的嵌入式项目：一只好玩的鸭子，不到800g，25cm小身板塞下RK3566和15个电机
description: Microduck 是一台不到 800g、25cm 高的双足机器人，采用 RK3566、15 个电机、ToF、双 IMU，并公开控制、更新与强化学习软件栈。
locale: zh
translationKey: microduck-robot-duck
pubDate: '2026-09-01'
category: open-source
tags:
- Microduck
- Rockchip RK3566
- 双足机器人
- 强化学习
- MuJoCo
- PPO
- ONNX
- 开源项目
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/pollen-robotics/microduck
seoTitle: Microduck机器人鸭子：RK3566、15个电机与开源强化学习软件栈
seoDescription: 解析Pollen Robotics Microduck：25cm小型双足机器人、RK3566主控、50Hz电机控制、双IMU、8×8 ToF、MuJoCo/PPO和ONNX策略。
---

这两天有只小鸭子有点火,发布后24 小时订单超 260 万美元，它叫 Microduck，Pollen Robotics 做的，背后现在是 Hugging Face。外形看着像桌面玩具，价格也不是工业机器人那种吓人的数字，预售价 399 美元。

![Microduck 小型双足机器人在桌面上与足球互动](/uploads/microduck/microduck-cover.webp)

*Pollen Robotics 的 Microduck 实拍，本文列表封面取自原稿。*

![Microduck 的四种配色及不同动作姿态](/uploads/microduck/microduck-four-colors.webp)

*Microduck 的四种配色与动作姿态。*

项目地址：

[https://github.com/pollen-robotics/microduck](https://github.com/pollen-robotics/microduck)

[https://pollen-robotics.com/](https://pollen-robotics.com/)

这个仓库官方说得很直白：这是鸭子的“大脑”。不是玩具外壳图纸，也不是完整开源硬件包（并没有开源原理图），而是运行在 Microduck 上的软件、控制、更新和机器人行为栈。

Microduck 高 25cm，不到 800g，身上有 15 个电机。它能走路、坐下、站起来、踢小球、用鸭嘴捡东西，摔倒后还能自己翻起来。听起来有点像“会动的桌面摆件”，但内部其实是一个小型双足机器人系统。

核心器件可以简单捋一下。

主控是 Rockchip RK3566，四核 Arm Cortex-A55，官方规格写了 1GB RAM、32GB 存储。这个芯片在电视盒子、边缘网关、低成本 Linux 设备里经常能看到。放在 Microduck 上，它负责跑 duckOS、控制回路、摄像头、无线连接和更新服务。

传感器部分有前置摄像头、8x8 ToF LiDAR、两个 IMU、NFC，另外还有麦克风和喇叭，续航用的是可拆的 NP-F550 相机电池，2600mAh，官方说大约 1 小时，实际肯定要看动作强度。

比较有意思的是电机部分，15 个舵机和 IMU 共享一条总线，robotd 以 50Hz 控制循环直接管机器人动作。也就是说，上层不是“随便发几个动作指令”那么简单，而是一个实时-ish 的机器人控制进程在兜底。

![Microduck 公开规格整理的系统功能框图，非官方 PCB 原理图](/uploads/microduck/microduck-architecture-zh.webp)

上面这张是按官方公开资料整理的系统框图，注意，不是官方 PCB 原理图。Pollen 在 press kit 里明确说了：开源声明覆盖的是软件栈，机械和电子设计文件目前不包含在开源范围内。

软件架构方面，Microduck 不是把所有逻辑塞进一个大程序里。官方设计里拆了几个 daemon：robotd 管电机、传感器、策略和安全；configd 管 Wi-Fi、名称、手柄配对；updaterd 管签名更新、回滚；btd 做蓝牙通道；padd 读手柄；mediad 管摄像头和 WebRTC；tofd 单独服务头部 ToF 深度传感器。

这些进程之间用 Unix socket 跑 JSON-RPC，控制的归控制，媒体的归媒体，更新的归更新，摄像头崩了，不应该把电机控制也拖死；运动进程挂了，设备也应该还能联网、更新、回滚。

![一台 Microduck 双足机器人站在室内桌面上](/uploads/microduck/microduck-on-desk.webp)

训练这块，Microduck 走的是仿真到实机, 官方另外放了 microduck_rl 仓库，用 MuJoCo 和 PPO 训练策略，再导出 ONNX 给真机运行。走路、站立、坐下、捡东西、踢球、滚轮这些动作，都对应不同任务。小机器人看起来萌，背后还是正经的强化学习控制。

这里有个细节,训练仓库里专门建了执行器模型，考虑电压控制、反电动势、摩擦、延迟、电池压降，甚至齿隙。小双足机器人最怕什么？就是仿真里走得好好的，真机一上地，舵机死区、背隙、地面摩擦全来找你。

Microduck 真正有意思的地方不是“机器鸭会卖萌”，而是它把消费级机器人做成了一个能二次开发的平台。

你可以先拿手柄玩，也可以 SSH 进去看日志、更新、配置网络，再进一步改策略、训动作、换行为,对普通开发者来说，它比大型人形机器人现实很多：体积小，价格低，摔了大概率也不至于心疼到睡不着。

最后，现在 Github 上能看的主要是软件和训练栈，不是完整复刻一台鸭子的硬件资料。想拿这个仓库直接打板、打印、装一台出来，目前还不现实。它更像是一个“可买到的开源软件机器人平台”。
