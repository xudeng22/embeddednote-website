---
title: "从旧 Kindle 到 AI 机器人：OpenAI 展示的 41 个 Codex 硬件项目都做了什么？"
description: "逐项拆解 You Can Just Build Things 展示的 41 个硬件作品：ESP32、树莓派、电子纸、语音 Agent、机器人、相机改装与 FPGA。每个项目附原始链接和可核实的技术看点。"
locale: "zh"
translationKey: "codex-hardware-41-projects-2026"
pubDate: "2026-11-03"
category: "hardware"
tags: ["Codex", "硬件项目", "ESP32", "Raspberry Pi", "AI Agent", "开源硬件"]
draft: false
seoTitle: "41 个 Codex 硬件项目逐项盘点：ESP32、电子纸、机器人与 AI Agent"
seoDescription: "完整整理 You Can Just Build Things 的 41 个作品，介绍用途、硬件与交互特点，附 41 个详情链接。哪些有源码、哪些只是演示？"
author: "EmbeddedNote"
sourceUrl: "https://youcanjustbuildthings.openai.chatgpt.site/"
---

一台用了十年的 Kindle 被改成 AI 用量显示器，胰岛素笔上夹了个可调节高度的放大镜，理光 GR 的热靴上多了一块 M5Stack 小屏。往下翻，还有捡垃圾的履带机器人、用 ESP32 控制的温室卷帘，以及随身带着走的语音 Agent 吊坠。东西各有各的用途，作者们却都在制作过程中用上了 Codex。

OpenAI 把这些作品集中放在 You Can Just Build Things 里。2026 年 11 月 3 日查看时，按点赞排序共有 41 个条目。有人贴出了源码和复刻过程，有人只展示了成品或原型；互动投影桌面游戏还出现了两个版本。这里按原页面顺序逐个看，图片取自对应的项目展示页，点图可以回到作者的原始投稿。需要注意的是41 个展示项目，不等于 41 套已经开源、测试完毕的硬件方案。

网址：

https://youcanjustbuildthings.openai.chatgpt.site/

https://embeddednote.com/zh/articles/codex-hardware-41-projects-2026/

## 01–10：从电子纸仪表盘到便携语音助手

### 01. Kindle AI 使用量仪表盘 / Kindle AI Usage Display

把一台约十年前的 Kindle 改成常亮的 AI 使用量显示器。它汇集 Codex、Claude Code、Cursor、Copilot 和 Gemini 等工具的用量，换算成本月累计费用、预计支出和来源占比；设备约每六小时联网取一次新图片，刷新后继续休眠。制作流程包含 Kindle 越狱、FBInk 绘图、Node.js 数据服务和定时采集，适合研究旧电子纸设备再利用。

[![Kindle 屏幕上的 AI 使用量仪表盘](/uploads/codex-hardware-41-projects-2026/official-01.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8133b4dec277fe58e2c3e0a3bc317fa1a2e33b28e9035bba9bd2a73612241224)

创作者 @kuberwastaken

代码：kindle-ai-usage 仓库（请以项目详情所列仓库为准）。

### 02. 胰岛素笔剂量放大镜 / Insulin Pen Magnifier

一种夹在胰岛素注射笔上的实体放大镜，目的是让剂量窗口中的数字更容易辨认。作者借助 Codex 设计并用 PETG 打印，镜片高度可调，重点在结构件夹持、光学距离和不同笔型的适配。它是辅助阅读的配件，而不是自动校验剂量的医疗设备；页面没有给出临床验证数据。

[![安装在胰岛素笔上的粉色剂量放大镜](/uploads/codex-hardware-41-projects-2026/official-02.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-06f376b224330ddcf07278b6132c5d1879c956c0a7951d12e97ecf2253d59a6e)

创作者 @manfye

### 03. 梦境记录器 / Dream Logger

床头语音装置，醒来后把梦讲给设备，系统将叙述转换成四幅插图并写入日历，便于回看。它把语音输入、图像生成和时间轴存档连成一条完整流程，比单独展示聊天界面更有物理场景感。页面没有披露模型、麦克风或主控的完整清单，因此不宜推断其离线能力。

[![手持梦境记录器的交互屏幕](/uploads/codex-hardware-41-projects-2026/official-03.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-76ded4f1a1107d49906050e4d5357c551916871062f47d2ef5f373c27271e2d8)

创作者 @fedesarquis

### 04. Taz 语音电子宠物 / Taz — Taskagotchi

实体数字宠物，根据实时语音交互改变表情和动作，角色动画由作者手绘像素图构成。项目看点在低分辨率动画与对话时序结合：用户说话、系统回应、屏幕反馈之间的延迟会直接影响角色是否“有生命感”。公开简介没有说明采用哪款处理器或显示屏。

[![透明外壳中的 Taz 像素电子宠物](/uploads/codex-hardware-41-projects-2026/official-04.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-03dbc72cda8b3d17c2e3b40a2708e8deb4b01d3183fbea3b64b55d1b8edfbaf4)

创作者 @covacut

### 05. Fovea 视线交互助手 / Fovea

把视线当成指针：注视屏幕某个区域并说出意图，Fovea 自动收集相关文字、截图及上下文。与传统先截图再粘贴到聊天窗口不同，它尝试通过眼动选择操作对象，再把视觉与语言信息组合。公开介绍没有交代眼动追踪器的具体型号，也没有提供可量化的识别准确率。

[![Fovea 双目视线追踪设备](/uploads/codex-hardware-41-projects-2026/official-05.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8287b1050903707504f8f371dc333a656e1e53444daee325b2b7a6afc23f3f6c)

创作者 @maxjjiang

### 06. 理光 GR 热靴实时取景遥控器 / RICOH-GR-Live-View-Shooting

使用 M5Stack StickS3 做成装在相机热靴上的小型无线取景器和快门遥控器，页面列出了理光 GR II、III 和 IV。它把实时预览、相机遥控和便携式显示整合到小模组中，特别适合关注相机远程控制协议的开发者。具体兼容性还应以作者发布的固件版本为准。

[![理光 GR 相机旁的 M5Stack 无线取景器](/uploads/codex-hardware-41-projects-2026/official-06.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-c2ac6e11f54cc9e37f847dda361f3ccefde2cecb6fc800bd6c0cbddc0619cf38)

创作者 @tinker_zhang

### 07. ChatGPT Dot 桌面信息终端 / Dot gadgets for ChatGPT dots

通过开源 MCP 中继把 Dot 发来的短消息送到一块带 LCD 的 ESP32 装置上。相比直接让单片机运行大模型，方案把网络服务、消息转发与终端显示分层，设备只处理适合小屏的提示。它适合借鉴 agent-to-device 的协议桥接，但实际使用依赖对应 Dot 服务和连接配置。

[![显示警报提示的 ESP32 LCD 终端](/uploads/codex-hardware-41-projects-2026/official-07.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-c6afc93fd057c0d10413d4957eaa683df24ee480e9fda771f033bb470f8f2997)

创作者 @deadbeef101010

### 08. PixelTilt 倾斜操作掌机 / PixelTilt

一块 64×64 LED 面板、运动传感器和侧面的拇指滚轮组成掌上游戏设备。玩法不是用方向键，而是靠倾斜机身改变游戏状态，再用滚轮做精细输入。硬件简洁，真正难点在姿态滤波、动态画面和输入手感；页面未说明 LED 驱动架构及续航数据。

[![PixelTilt LED 游戏菜单画面](/uploads/codex-hardware-41-projects-2026/official-08.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-fa3ac3d72e2c4a57b08c8e88b955097a28e29e32860831d35544d27e0468a400)

创作者 @abcdmku

### 09. 猫咪专属投影电视 / Cat TV

树莓派向 Samsung Freestyle 投影仪播放针对猫咪设计的动态场景，并通过 Wi-Fi 控制投影设备。所谓“猫电视”不是另一块硬件屏幕，而是把已有投影仪变成会变化的宠物娱乐场景。它体现的是设备控制接口与内容生成的结合，并不能据此推断对动物行为的长期效果。

[![墙面上的猫咪互动投影](/uploads/codex-hardware-41-projects-2026/official-09.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-b14cc8ab97aab9b9666fb63515262667de44741eb7bc92d54071095aaeafc2b4)

创作者 @axbehr

### 10. Orbit 便携式个人语音 Agent / Orbit Personal Voice Agent

一个标称约 60 美元硬件成本的便携语音助手，连接 Wi-Fi，再通过 MCP 服务访问日历、收件箱和家庭自动化。项目核心不在本地训练模型，而在把语音入口接到不同的个人服务上；“60 美元”来自作者展示，不是独立核算的完整商品价格。

[![手持 Orbit 语音助手](/uploads/codex-hardware-41-projects-2026/official-10.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-25918ab207fee3b5c67caf252272b870ec0e8f0bd8ce6bbfadda36b431a97b77)

创作者 @camdsmith

## 11–20：实体 Agent、机器人与自动化

### 11. Bokko 蓝牙 Agent 吊坠 / Bokko — my agent has a body

一枚随身吊坠，通过蓝牙连接 Mac 上的 Hermes agent。按住按钮说出任务，处理结果再返回吊坠显示，实现了“按钮下发—电脑执行—设备反馈”的交互闭环。这种结构把算力留在电脑侧，吊坠强调便携输入和状态反馈；页面没有公布自主续航或屏幕具体规格。

[![Bokko Agent 吊坠的屏幕界面](/uploads/codex-hardware-41-projects-2026/official-11.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-b0e263f85d614709197d92c3284492bc8dcf76b5466766a8aacefc059b0f4e00)

创作者 @patiev_blog

### 12. MOSS 垃圾拾取履带机器人 / MOSS the litter-picking robot

可自行打印和组装的小型履带机器人，上方有收纳箱，机械臂末端使用平行夹爪。与只会遥控移动的底盘相比，MOSS 需要同时处理行走、抓取和物体放置三个环节。作者提供了硬件设计与构建方向；不要把原型演示理解成已经验证的自主垃圾分类产品。

[![MOSS 履带机器人与机械臂](/uploads/codex-hardware-41-projects-2026/official-12.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-3e2447ee5941f35b9a4fb53fa3fb981cea41407d491c5f6349cfc4feebea5392)

创作者 @metrox_eth

### 13. Casey’s NYC Ride 掌机游戏 / Casey’s NYC Ride

以纽约骑行影像为灵感的掌机游戏，运行在 ModRetro Chromatic 上，主要美术素材由作者手绘。看点是把个人城市体验和复古掌机硬件结合，而不是复制一套通用 Game Boy 模拟器。原站介绍没有披露底层游戏引擎与性能测试，技术细节以作者后续发布为准。

[![ModRetro Chromatic 掌机上的骑行游戏](/uploads/codex-hardware-41-projects-2026/official-13.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-790a05bb8708daa088f77c1db47bbd7aad7ba6ea9632038b6a9c6d8644e8c477)

创作者 @covacut

### 14. ESP32 实时语音 API 参考工程 / Realtime on ESP32

乐鑫维护的 WebRTC 演示工程，展示嵌入式语音设备如何连接 OpenAI Realtime API，以及如何通过语音触发设备函数调用。它属于可追踪源码的参考实现，不等同于已经商品化的语音音箱。开发时需要区分设备端采集播放、WebRTC 连接和云端模型服务，并处理 API 凭证和网络异常。

[![乐鑫 ESP32 语音开发板](/uploads/codex-hardware-41-projects-2026/official-14.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/official-realtime-esp32)

参考实现：Espressif esp-webrtc-solution。

### 15. Living Art TV 生成式屏保 / Living Art TV

让电视屏保根据家中当天的天气和时间变化，把用户自己的作品生成一段持续更新的视觉叙事。与固定循环播放的数字相框不同，内容会受环境变量影响。原站没有给出电视系统、生成模型或离线工作方式，因此这部分只能作为玩法介绍。

[![电视上的生成式艺术画面](/uploads/codex-hardware-41-projects-2026/official-15.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-c574fd275e4ccfb259cbce73ba52630e94745e7dca0c20fa85b45569d4216851)

创作者 @awkward_andyy

### 16. 力量训练实时语音教练 / Workout Coach x Codex Voice

将力量训练的速度传感器接入 Codex Voice，训练过程中可针对动作节奏进行实时语音交互。项目把一个可测量的物理量引入对话，使建议不再完全依赖人的主观描述。不过公开页面没有给出传感器型号、标定方法或训练建议的验证结果，不能直接据此宣传训练效果。

[![力量训练器材上的动作速度传感器](/uploads/codex-hardware-41-projects-2026/official-16.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-36218fe62a49fbc58d46d778c8c1b9e69b25f97cf607dcbc1fe63564b59dd8a2)

创作者 @awkward_andyy

### 17. Kinform：给普通物品一个角色 / Kinform: Give Objects Lore

用 GPT Live 把一件普通物品赋予可持续的角色、声音、个性和记忆，让低成本物品也能变成可对话的实体角色。与常见的“会说话蓝牙音箱”不同，它强调角色在多次交互之间保持连续性。页面描述不意味着所有记忆都存于本地，也未披露完整隐私方案。

[![Kinform 智能物件及手机设置界面](/uploads/codex-hardware-41-projects-2026/official-17.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-2e8b5d907432e54a1615508b81e9638819eb074c14884294c2a2ebf13b8a75cc)

创作者 @bonitadreama

### 18. Noutomation 浏览器工业自动化 / Noutomation: Automate Your Way

通过浏览器配置传感器读取、继电器动作和 Modbus 设备控制，不必每改一次规则就重写固件。项目面向农场、车间这类设备种类杂、控制逻辑经常变化的场景，重点是把 I/O 和规则管理放在统一界面。公开页面没有列出所有工业安全认证，不能当作安全 PLC 替代品。

[![Noutomation 自动化控制设备](/uploads/codex-hardware-41-projects-2026/official-18.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-7794785a17c92e5b671a4505767ff4fca409e57eda52b974fd0019d5ca2af809)

创作者 @masubo_bio

### 19. ESP32 多屏无限画布 / Multi screen infinite artwork

使用多块 ESP32 构成网状网络，让生成式图像从一块显示屏接续流到另一块。图案约每分钟变化一次，也能响应人的互动。它不是单屏视频播放器，关键在设备之间的时间同步、画面边界衔接和网络消息组织；页面没有提供节点上限与同步误差数据。

[![多个屏幕展示相连的生成式画面](/uploads/codex-hardware-41-projects-2026/official-19.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-ac36c83a2196dfca18243bfb917c562bab91631a394510bf83c3bfedd897006b)

创作者 @msurguy

### 20. Codex 温室卷帘控制器 / Codex-Built Greenhouse Winder

农场主用 ESP32、两台 24V 电机和温度传感器制作温室通风卷帘，既可通过 LINE 发消息控制，也能按测得的温度自动动作。这个项目比“AI 做个小玩具”更接近真实生产环境：硬件要对付长期户外使用、执行器堵转以及远程通信中断等情况。原站并未给出完整安全防护和寿命测试。

[![温室控制器接线与控制盒](/uploads/codex-hardware-41-projects-2026/official-20.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-e347d07c0cd0edd7a25bcfbae3fcfee78d86003917d2888d359eb167305ad1da)

创作者 @tomiyasu16

## 21–30：PCB、相机、投影与互动游戏

### 21. AI 协助设计的 DEFCON PCB 胸牌 / OpenAI inspired DEFCON badge

一块带灯光效果的 ESP32 PCB 胸牌，还可以选配 OLED。作者称 Astra 帮助完成从 KiCad 走线到 JLCPCB 下单的流程，展示了 AI 在 PCB 设计、制造文件与订单步骤之间的辅助能力。需要强调的是，自动布线结果仍需人工检查电气规则和生产工艺，页面没有提供独立的量产验证。

[![DEFCON 电子胸牌 PCB 设计](/uploads/codex-hardware-41-projects-2026/official-21.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-d167331b94c63d3cd8a861f19bf92f785aa465001b95b96453565ac1701d3423)

创作者 @aitelmax

### 22. ImageGenCam AI 图像相机 / ImageGenCam

OpenAI 提供源码的周末制作项目：Raspberry Pi Zero 2 W、Display HAT Mini、摄像头、PiSugar 电源和 3D 打印外壳组成一台掌上相机。按下快门后照片送去图像生成，手机网页用于查看照片和修改提示词。它真正可借鉴的是本地采集、后台生成任务与手机控制界面的分工，并非在树莓派本地运行大型图像模型。

[![ImageGenCam 树莓派相机物料布局](/uploads/codex-hardware-41-projects-2026/official-22.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/official-imagegencam)

源码：openai/imagegencam。

### 23. Reflect 声光 AI 助手 / Reflect

OpenAI 黑客松中的声光交互装置，基于 M5Stack CoreS3，结合 Realtime API 和智能彩灯。它有意避开传统聊天屏幕，用声音、灯光颜色和节奏传递反馈。官方仓库明确标注是实验性演示，未经过完整的可靠性及安全审查；适合作为原型学习，不应按商业终端标准理解。

[![Reflect 智能交互设备](/uploads/codex-hardware-41-projects-2026/official-23.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/official-reflect)

源码：openai/openai-reflect。

### 24. FPGA 迷你老虎机显示实验 / FPGA Slot Machine

在 Mac 上调用远程 Windows 环境使用 Vivado，开发一款带 64×96 OLED 界面的 FPGA 游戏装置。与普通 MCU 游戏不同，这个例子突出跨平台 FPGA 工具链编排：从远程综合到设备侧画面呈现。项目主页没有说明实现了哪些随机机制，也不应将其视为真实赌博设备。

[![FPGA 迷你老虎机项目演示](/uploads/codex-hardware-41-projects-2026/official-24.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-5bb2f0d7a1110b62c833006dc731576c3505620738668aff788625e504ead672)

创作者 @itsarnz

### 25. Project Tabletop 地面投影足球 / Project Tabletop

用投影仪和摄像头把地板变成足球场，玩家通过移动实体标记来控制场上的车辆，与电脑或朋友比赛。摄像头负责感知实体位置，投影仪负责反馈，交互并不依赖每个道具内置无线芯片。这是计算机视觉与空间显示结合的案例；页面没有公布追踪精度与环境光要求。

[![投影显示的互动足球场](/uploads/codex-hardware-41-projects-2026/official-25.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-3ccbfc5367ce49fc8fc2fcfda105ccaf9711a8609f4db8beaa74addbecfc6abb)

### 26. El Tucu：按分钟租用机械臂 / El Tucu — Rent a Shell

一只由四个舵机驱动的小机械臂，可以由人或 AI agent 按分钟租用。作者演示 Codex 借助 x402 支付来使用机械臂，形成“发出任务—完成支付—执行动作”的物理服务流程。它的看点是设备访问权与机器支付结合，不代表机械臂已具备复杂自主抓取能力。

[![El Tucu 四舵机机械臂实物](/uploads/codex-hardware-41-projects-2026/official-26.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8ae093885312a273f1bcf61bf19f43c3c06013d58a6370f58bf456dbd88ba69c)

创作者 @crypto_dev_1

### 27. Purble Palace 复古掌机复刻 / Purble Palace — Built with Codex

出于对上世纪 90 年代 PC 游戏的怀旧，作者借助 Codex 在 ModRetro Chromatic 掌机上制作 Purble Palace 风格的游戏。工程看点是将桌面交互迁移到更小的屏幕和实体按键，而非增加新的硬件传感器。页面信息不足以判断与原游戏的功能完全一致程度。

[![运行复古游戏的 ModRetro Chromatic 掌机](/uploads/codex-hardware-41-projects-2026/official-27.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-4c5c85dc0d18277ef4f93efd87ed3dfcca142f47eef2470b41a88149455edb6b)

创作者 @haimantikam

### 28. 62 BAR 电动转盘 DJ 小乐器 / 62 BAR — Mini DJ Instrument

基于 Raspberry Pi 的迷你 DJ 乐器，结合电动转盘、触摸屏、实体按键以及定制外壳。作者把 Codex 用在 CAD、固件和整机组合的多个环节，重点不是播放列表，而是带手感反馈的音乐控制界面。公开资料没有提供完整音频延迟或电机闭环精度测试。

[![62 BAR DJ 设备结构设计图](/uploads/codex-hardware-41-projects-2026/official-28.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-61f7edd92afacdf02d4f2ce9775bc6754d592451748cb2476cbd6725c03624b0)

来源：项目详情 · 创作者 @eminimnim

### 29. 哈苏 X2D：相机上跑 DOOM / Hasselblad X2D: DOOM & Beyond

把 Codex 用在哈苏 X2D 的非官方功能实验上，包括让相机运行 DOOM、用快门键触发游戏射击，以及探索自动对焦、像素位移和自定义启动画面。重点是封闭相机平台的固件研究与人机界面复用，不是官方固件功能清单。实验性改装可能影响设备稳定性和保修，文章不提供未经核验的刷机步骤。

[![哈苏 X2D 相机运行 DOOM](/uploads/codex-hardware-41-projects-2026/official-29.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-fb627402781dcf89f55b7d1bcf38395ded1bc29539cbd21281826a15bfed0f9e)

### 30. 512 颗 LED 音乐反应立方体 / 512-LED Music-Reactive Cube

把 512 颗 LED 排成 8×8×8 的立体矩阵，监听周围声音并根据 FFT 结果展示动态空间图案。作者提到定制 PCB、手工焊接和专门的频谱处理固件。与二维灯带相比，三维立方体还涉及扫描驱动、供电压降和机械排列问题；原站没有披露亮度与功耗实测。

[![512 颗 LED 组成的音乐立方体](/uploads/codex-hardware-41-projects-2026/official-30.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-eae7d60f950fbd72de230fca0a9421fe8b24080d2592d977a515c3b7bc27cbd6)

创作者 @tttorynnn

## 31–41：相框、旧设备改装与视觉闭环

### 31. Keep：远程传图电子纸相框 / Keep — E-Paper Photo Frame

作者为未婚妻做的电子纸相框，可以把爱丁堡拍摄的照片发送到她桌面上的屏幕。它解决的是跨距离分享照片的问题：拍摄端、网络服务和低功耗显示端形成一个简单链路。原站只介绍使用场景，没有公布屏幕型号、通信协议或待机时间。

[![远程照片电子纸相框实物](/uploads/codex-hardware-41-projects-2026/official-31.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-0ddf7261982e37359f642e967431d4c2d0f15a42e52246b10dcc5894b9e8042a)

创作者 @tarat_211

### 32. M5Stack 手表万花筒 / Watch Kaleidoscope

把 M5Stack 手表变成掌上万花筒：倾斜或滑动设备，玻璃碎片状的图形根据物理模拟滚动、碰撞并发声。值得关注的是小屏图形渲染与惯性输入的结合，碰撞反馈又增加一层声音交互。原站没有说明具体使用哪款显示驱动或游戏引擎。

[![M5Stack 手表万花筒画面](/uploads/codex-hardware-41-projects-2026/official-32.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-3f2cb8bdf24e11f6f8c3a86872e376303f91f4695f88d15d07cae36ad49a1041)

创作者 @realtr2e

### 33. ESP32-S3 iPhone 实体操作代理 / Hands-On AI: ESP32 iPhone Agent

作者声称使用微型 ESP32-S3 板实现 AI 对真实 iPhone 的画面观察和操作，不需要越狱、Mac 或数据线，画面镜像与蓝牙触控输出是关键。工程上值得关注的是无线屏幕采集与 HID 输入组合，但这属于作者展示的兼容路径，不能推断能稳定控制所有 iOS 版本或绕过系统授权。

[![ESP32-S3 iPhone 操作代理设备](/uploads/codex-hardware-41-projects-2026/official-33.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-aad932dd2f447aaa8122d47132efca6bf5913f3d5089b2e2f99997adb69f76ea)

创作者 @iamhenryyuan

### 34. Robbi 情绪化 AI 机器人 / Robbi: Your Emotional AI Companion

一台用 Raspberry Pi 和 3D 打印结构件制作的桌面机器人，结合声音、视觉、记忆和情绪化反馈，让角色具有鲜明个性。和只有语音问答的智能音箱不同，它尝试把物理外形也变成交流的一部分。页面没有公开完整硬件 BOM 或长期使用验证，适合作为交互原型观察。

[![Robbi 桌面机器人演示](/uploads/codex-hardware-41-projects-2026/official-34.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-740858b4fae95982b3ebe82974f3a454bf1f0c568cc2fc8b1b886db1ac207d2e)

### 35. 温室机器人原型 / Greenhouse Robot Prototype

面向温室环境的自主机器人原型，目标是结合环境感知、智能决策和机器人执行能力提升运营效率。页面公开的信息仅是总体目标和原型定位，没有披露底盘、传感器或导航算法。文章保留它作为探索方向，但不会替作者补出不存在的自动采摘或精确定位指标。

[![温室机器人原型设备](/uploads/codex-hardware-41-projects-2026/official-35.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-e03ad8c797ef36ff013b54b727c1e7e4de0b189cd40ebbf6e7bb634c1528b302)

创作者 @ihwylie

### 36. 理光 GR IV 相机固件改装 / Ricoh GR IV: Beyond Stock

围绕理光 GR IV 做非官方固件研究，已展示自定义关机画面，并公开了针对该型号的脚本工具。它的价值在于对封闭消费电子设备进行有限度的可重复研究，而不是宣称完全掌握相机固件。动手之前仍需考虑数据备份、设备恢复和官方保修限制。

[![理光 GR IV 相机的自定义界面](/uploads/codex-hardware-41-projects-2026/official-36.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8f79d3b2973c34d916db32d50143ead2ab5a86eb8641dcfe1cb72df8c6496467)

### 37. Project Tabletop v1.3 桌面互动游乐场 / Project Tabletop (v1.3)

同一投影交互思路的更新版本，把桌面变成互动场地：投影仪负责画面、摄像头识别实体记号笔，既能玩街机游戏，也能涂画或探索地球。它与前面的地面足球项目相关，应作为独立上架条目介绍，但不误认为完全不同的底层平台。公开页面没有提供该版本的完整更新日志。

[![桌面投影互动装置](/uploads/codex-hardware-41-projects-2026/official-37.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-16072b5be9929c4cf63781d83a8f447919a487bbcaff1cdd9b1d475239c54fc2)

### 38. Nikko R2D2 老机器人控制 App / Nikko R2D2 Modern OS App

尝试为旧款 Nikko R2D2 遥控/网络摄像头机器人重新开发适用于现代 Windows 的操作软件。其核心价值是老旧联网玩具的协议和驱动兼容工作：新操作系统变了，硬件未必需要直接报废。原站把它称为尝试，尚不足以证明所有功能已经恢复。

[![Nikko R2D2 机器人与电脑](/uploads/codex-hardware-41-projects-2026/official-38.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-d24ce5b5d0eaab1154d5979941696fc50f4008beb4765cb69af5982a77c2e717)

创作者 @pablopoo

### 39. Project Piko 树莓派 AI 系统助手 / Project Piko

把 Raspberry Pi 变成可对话、可分配任务的个人 AI 助手，并能帮助管理 Linux 电脑。它更像一个有实体入口的系统管理 Agent，而不是只负责播报天气的音箱。需要谨慎的是，具备系统操作权限的助手应限制命令范围并记录执行动作；原站没有披露其权限隔离机制。

[![Project Piko 树莓派 AI 助手](/uploads/codex-hardware-41-projects-2026/official-39.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-0a9ce28248c654130b4ae0e4f80894f93243bfe5e623bc3756e445d839fd1ce5)

创作者 @blackie_360

### 40. Codex 交互式宠物胸牌 / Codex Pet Badge

利用 M5Stack 制作可以响应倾斜、摇晃和触摸的互动胸牌，同时显示电量，还能打开作者的 LinkedIn 二维码。它把电子会议胸牌做成有动态反馈的小玩具，互动和身份展示共用一块硬件。简介没有披露具体 M5Stack 型号，也不能把它视为完整的无线名片系统。

[![Codex 互动电子胸牌](/uploads/codex-hardware-41-projects-2026/official-40.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-15b148cc94a3ce050e840a5302e1824396ae5cb2892d9e60ce04a435f8fb5070)

创作者 @naveenmanwani17

### 41. 带视觉闭环的空调遥控器 / AC Remote with Visual Feedback

Raspberry Pi 5 与 iPhone 控制界面组成空调遥控方案，红外发码后再由 AI 摄像头检查导风板位置。不同于只发送 IR 命令的普通遥控器，它增加了视觉反馈，试图确认设备是否真的响应。网页没有说明全部空调型号、图像识别成功率或安全联锁，不能当成通用兼容方案。

[![空调遥控与视觉反馈界面](/uploads/codex-hardware-41-projects-2026/official-41.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-edea2dffa1a7b0152eaa552435b98b5681a257a5f2b6dfda1ceba433217901dd)

创作者 @swhan0329

把 41 个条目放在一起看，最务实的路线不是先想一个可以安装大模型的壳子，而是先找真实世界里可以观测、可以操作、可以反复验证的细小问题。温室卷帘有温度和电机位置，旧 Kindle 有明确的屏幕刷新周期，理光相机需要稳定的远程快门，空调遥控必须确认导风板真的动了。这些闭环明确的题目，往往比单纯“加一个 AI 聊天框”更适合做第一版硬件。

另一个值得留意的是，AI 编码工具并没有让模拟电路、供电、光学、热设计和机械公差消失。它能帮人写驱动、组织测试、查文档、生成界面，甚至协助做 PCB，但最后还是得有人检查电机限位、相机固件恢复、医疗辅助器具的适配边界。对于是否能直接复刻，还要去对应项目页面确认源码、BOM、许可和具体硬件版本。

关注公众号“嵌入式杂谈”，了解更多有趣好玩的嵌入式信息，感谢大家的点赞、在看，也欢迎留言拍砖~
