---
title: GitHub 上的 AI 硬件项目：Meta 开源的 Muse Gadget SDK，把 AI 智能体塞进一块 ESP32
description: "Meta Muse Gadget SDK 为 ESP32 和 Linux 设备提供 AI 交互反馈。本文介绍开发板支持、交互状态与嵌入式实现思路。"
locale: zh
translationKey: github-ai-meta-muse-gadget-sdk-ai-esp32
pubDate: 2026-10-12
category: open-source
tags:
  - "Github "
  - AI 硬件
draft: false
---
Meta 这两天在 GitHub 上开源了一个叫 Muse Gadget SDK 的项目，仓库地址是 facebookincubator/muse-gadget-sdk，Apache 2.0 许可，发布不到 48 小时 Star 就破了 1000。一开始我以为又是一个给 ESP32 接大模型的方案，毕竟前面已经在这块板上折腾过小智，录音、识别、生成回答、播放，这条链路并不陌生。但把源码拉下来翻了一遍之后发现，它和小智 AI、Home Assistant Voice PE 这些项目走的并不是同一条路线。

![Meta Muse Gadget SDK——项目架构和交互概览配图](/uploads/image-9.png)

很多项目关注的是怎么把语音接入大模型，而 Muse 更关注的是怎么让一个桌面 AI 终端看起来像一个有状态、有情绪反馈的设备。它不是在等回答回来以后才动一下，录音时有电平反馈，等待时有对应的动作，回复时让出字幕空间，结束后还有短暂的动作反馈。对放在桌上的设备来说，让人知道“它现在在干什么”，是很实际的一件事。

这个项目到底是啥？Muse 是 Meta 推出的个人 AI 智能体，可以帮用户预订行程、填写表单、完成购物等任务。**Muse Gadgets 则是把这套智能体能力从手机 App 里解放出来，让开发者自己搭硬件来接。**官方这次放出了两个 SDK，一个是 ESP32 Device SDK，一个是 Linux Device SDK，全是开源的，连固件都一起放出来了。仓库的 README 写得很直白——“It‘s built by hackers, for hackers, just for fun”，还特意提醒折腾的副作用可能包括变砖、保修失效、电压跌落甚至破产，风险自负。

**Github地址**

[https://github.com/facebookincubator/muse-gadget-sdk](https://github.com/facebookincubator/muse-gadget-sdk)

硬件层面，ESP32 这条路子支持的开发板已经有 11 款。官方首推的是乐鑫的 ESP32-C5 DevKitC-1，还有 M5Stack StickS3、微雪的 ESP32-S3-Touch-AMOLED-1.75C、Seeed 的电子纸显示屏等等。

![Meta Muse Gadget SDK——ESP32 开发板支持相关配图一](/uploads/image-10.png)

![Meta Muse Gadget SDK——ESP32 开发板支持相关配图二](/uploads/image-11.png)

**ESP32 和 Linux 两条线，能力面不太一样。** ESP32 Device SDK 面向的是低成本、低功耗的微控制器场景，接上屏幕、麦克风、喇叭或者传感器，就变成了 Muse 的一个物理外设。Linux Device SDK 面向树莓派这类单板计算机，能跑 shell 命令、读写文件、检查设备健康状态，开发者还可以通过自定义命令把系统管理或者 Home Assistant 的操作交给 Muse 来干。

端云交互的设计是我比较感兴趣的一块。Muse Gadget SDK 的端侧不是简单地把音频丢给云端等结果，设备状态由一个 muse_state.c 来统一管理，包括当前模式、进入模式后的时间、音频电平、字幕和进度。UI 读取这些信息再决定画什么、怎么动。这样一来，UI 不用自己猜“请求是不是结束了”。录音模块更新录音状态，会话模块送回回答事件，画面再跟着变化。

主流程其实很清晰：待机 → 按住说话 → 松开等待 → 展示回答 → 回到待机。接上 TTS 的版本，“展示回答”阶段还会播放音频，取消、断网和处理失败则走各自的分支。整个状态机的划分不复杂，但把交互的节奏感做出来了。

**设备端（ESP32/树莓派等）** 负责音频采集、按键/触摸交互、屏幕渲染和传感器数据读取，通过 WebSocket 和 Muse 云端建立长连接。设备上跑的是 ESP-IDF 框架，LVGL 负责 UI 渲染，音频走 I2S 接口。有些板子还跑了一个桌面模拟器，可以在 412×412 的窗口里先把界面调好，不用等板子到手。

**云端（Muse 智能体）** 负责语义理解、对话管理、工具调用和任务编排。设备通过 SDK token 配对，token 内置在固件里，官方建议把它当标识符而不是密码看待，泄露了就撤销重建。

**手机 App（iOS/Android）** 是配对的入口。需要在设置里打开 Developer mode，然后找前缀为 MuseGadget 的设备。

当然，Meta 自己也基于这套 SDK 做了一款成品设备叫 **Muse Home Link**，USB-C 供电的小盒子，能让 Muse 连接到家庭网络，跟电视、音箱以及其他暴露 HTTPS 接口的智能设备通信。首批大概 5000 台，面向美国 Muse 订阅用户免费发放，说白了这就是一个参考设计，告诉你这套 SDK 能做成什么形态的产品。

固件烧录流程也不复杂，ESP32 这边装好 ESP-IDF，把仓库 clone 下来，配好 token 就能编译烧录。Linux 这边跑一个 install.sh 脚本，可以通过 --run-as 指定非特权账户来运行 Muse。默认情况下 Muse 以安装时选择的账户身份执行命令，拥有该账户的全部权限，如果这个账户能用 sudo，Muse 也能用。

Muse Gadgets 这个项目的有趣之处不在于它用了什么特别高深的技术，而在于它的产品思路——它把 AI 智能体从手机屏幕里拽出来，塞进一块几十块钱的 ESP32 板子里，让它变成一个你能看见、能摸到、有状态反馈的桌面物件。这种“有身体”的 AI 体验，和纯软件聊天窗口的感觉确实不太一样。项目本身也还在早期，文档里不少地方还在迭代，Discord 社区倒是挺活跃的，手上有闲置 ESP32 板子的话，值得拉下来跑一跑。

关注公众号"**嵌入式杂谈**"，了解更多有趣好玩的嵌入式信息，感谢大家的点赞，在看。
