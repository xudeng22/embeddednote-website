---
title: 'Github上有趣嵌入式项目——能盯AI任务、还能控制小米智能家居的桌面搭子HachimoDock'
description: '用ESP32-P4和2.8英寸DSI屏给Codex、Claude Code配一只桌面小狗：实时盯Agent任务，支持按键语音、PetUI小游戏，还能通过电脑联动小米MiLoCo。'
locale: zh
translationKey: hachimodock-desktop-ai-buddy
pubDate: '2026-10-29'
category: open-source
tags:
  - HachimoDock
  - ESP32-P4
  - AI Agent
  - 桌面 AI
  - Codex
  - Claude Code
  - 小米 MiLoCo
  - PetUI
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/YizhengWw/HachimoDock
seoTitle: 'HachimoDock桌面AI搭子：ESP32-P4盯Codex任务，还能联动小米智能家居'
seoDescription: 'HachimoDock哈基米机拆解：ESP32-P4、2.8英寸DSI屏、凯华机械键、摇杆、USB Agent状态同步、PetUI组件、MiLoCo与PCB复刻资料。'
---

用电脑上的 Codex、Claude Code 这些 Agent 干活，有个烦恼不在于它跑得慢，而是你不知道它跑到哪了。切回终端看吧，一上午不知道要切多少次窗口；不切，又怕它停在授权确认那里等你。最近在 2026 观猹大会上亮相的 HachimoDock，思路挺直接：在工位上放一块小屏，把 Agent 的思考、执行、等待确认、完成、报错这些状态搬出来，再交给一只西高地小狗用表情和动作演给你看。抬头瞄一眼，就知道它在忙还是在等人。

这就是**哈基米机 HachimoDock**。[公开报道](https://www.ithome.com/1/017/842.htm)提到它由小米技术委创新产品团队孵化，不过项目由个人账号维护，并非小米商城销售的成品。代码、Windows/macOS 客户端和 ESP32-P4 固件在 [Github 仓库](https://github.com/YizhengWw/HachimoDock)，原理图、PCB、BOM、结构件与装配说明则在[嘉立创开源广场](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc)。项目那句“给 AI Agent 一个身体”，放在它身上还真挺贴切。

![HachimoDock桌面小屏实拍，屏上显示西高地小狗](https://image.lceda.cn/oshwhub/pullImage/6c47814b144549beb179528ea77cd75e.png)

*哈基米机实拍：一块小屏、三个按键、一只橙色摇杆，旁边的电脑负责运行 Agent。*

先翻硬件清单。核心是微雪 **ESP32-P4-WIFI6** 系列开发板，ESP32-P4 采用双核 RISC-V 架构，高性能核心最高 400 MHz，配套板卡标注 **32 MB PSRAM、32 MB Flash**。屏幕选了 **2.8 英寸、480×640 的 MIPI-DSI IPS 竖屏**，这比常见的 SPI 小屏更适合放宠物动画、字幕和会话气泡。开源页提醒选购时核对 15P/22P 排线、屏幕版本和边框；所谓“2.5D”玻璃是装配选项，不是固件必须依赖的触摸功能。ESP32-P4 芯片本身并不集成 Wi-Fi 6，开发板的无线能力来自配套无线硬件；而这个项目当前的设备通信，主要用的还是 USB。

三颗按键是凯华 **CPG135001D01** 机械轴，摇杆是 **YA13S-L7.4-B10Ka(60)-0-DL01**，5 kΩ、自复位，四向带中键。加上长按，总共能配置 12 种操作手势。音频部分有麦克风、2011 小腔体喇叭及 ES8311 相关音频通路；固件按实际板卡还可走 ES7210 采集路径，ASR 并不在 P4 上完成。微雪开发板和定制底板通过两根 2.54 mm、1×20P 排母连接，底板主要负责把按键、摇杆和连接器整合成一个能装外壳的结构，不是重新设计一块 ESP32-P4 最小系统。

![HachimoDock三颗机械按键和四向摇杆的近景](https://image.lceda.cn/oshwhub/pullImage/0187d6df22f74724acda54e111c7c850.png)

*三颗机械键配一个四向中按摇杆；设备当前主要靠实体输入和语音，不要求屏幕带触摸。*

硬件图纸值得专门打开看。[嘉立创项目页](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc)能预览主控板、按键 SW1～SW3、摇杆 U2 的连线，以及 **PCB_V1.2** 上的双排母布局，BOM 还可以按器件逐项查。整机方案也不是一开始就选 P4：早期试过 Radxa Cubie A7Z 和 Raspberry Pi Zero 2W，最后才收敛到 ESP32-P4 加 USB 直连。旧方案使用过 MQTT/HTTP，但**当前 P4 固件没有把 Wi-Fi/MQTT 作为设备端默认通信链路**；电脑端 bridge 内部出现 MQTT 相关代码，不等于小屏直接用 MQTT 接收消息。下面这张是按项目文档整理的功能框图，具体 GPIO、电源和排线还得以原理图为准。

![HachimoDock系统结构：Agent、PC桥接、USB与ESP32-P4显示设备](/uploads/hachimodock/hachimodock-architecture-zh.webp)

*Agent 在电脑端运行，状态通过桌面客户端和 USB 发给小屏；按键、摇杆和语音数据反向送回电脑。*

成本也别只盯着新闻里“150 元复刻”。开源页列出的主控板约 **81.15 元起**、屏幕 **65 元**、摇杆 **3.54 元起**，再算三颗凯华机械轴、喇叭、排母、PCB、外壳和运费，实际花多少得看购买渠道和打样数量。按前面三项已经接近 150 元，150 元更像一个宣传中的 DIY 成本参考，不是打包到手价。做之前最好把屏幕连接器和 **ESP32-P4 芯片 v1/v3 修订版**确认清楚；官方的两类完整烧录包不能混刷。

真正好玩的部分还是 Agent 跟随。电脑端的 **Tauri/React 管理器**通过本地 bridge 读取 Codex、Claude Code、OpenClaw 等 Agent 能提供的 Session 状态，统一成设备看得懂的消息，再经 USB 串口送给 ESP32-P4。哪个会话在读文件、跑工具、等待用户确认，屏上就出现对应气泡，小狗也换动作；完成或出错后，原有气泡还会停留约 60 秒，不至于一闪就没。不同 Agent 的适配能力并不完全一致，例如切换 WorkBuddy 的设备气泡，不代表电脑上的 WorkBuddy 对话也会自动切过去。

![HachimoDock多Agent会话状态气泡](https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/assets/session-bubbles.webp)

*多个任务分成不同的 Session 气泡；设备显示的是电脑端能读取到的状态。*

![HachimoDock Agent状态与宠物动作变化](https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/assets/agent-status.gif)

*Agent 状态变了，小狗也跟着换表情和动作。*

*项目还提供“思考中”和“任务完成”的宠物动画片段：*

<video controls playsinline preload="none" width="720"><source src="https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/pc/public/terrier-clips/working.thinking.mp4" type="video/mp4" /></video>

<video controls playsinline preload="none" width="720"><source src="https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/pc/public/terrier-clips/done.mp4" type="video/mp4" /></video>

长按配置好的语音键，设备用麦克风收音，通过 USB 把音频传到电脑；桌面端完成 ASR，再把文字写到目标 Agent 的输入流程里。有的集成会先留下草稿等你确认，并不是所有 Agent 都能无条件自动发送。机身那三颗按键加摇杆，还能切 Session、确认、返回或者控制小游戏。内置是西高地小狗，也能导入照片、视频或通过 AI 生成新形象，不过生图、语音和大模型服务需要自行配置凭据，公开安装包并不送 API Key。

![HachimoDock语音输入界面](https://image.lceda.cn/oshwhub/pullImage/0dddebc05c064f3a812d278b7c5dbe6e.png)

*语音在设备端采集，识别与 Agent 输入路由在电脑端完成。*

PetUI 组件中心也值得折腾。贪吃蛇、简单球类游戏、番茄钟、敲木鱼、待办、电脑状态、自选股行情等，都能作为屏幕小组件管理和同步；还可以让 Agent 用 `petui` Skill 按 **480×640 屏、三键一摇杆**的输入条件生成新组件。生成后不是把一段网页 JavaScript 直接塞进 P4，管理端会检查组件清单、资源大小、按键映射等，再交给设备的 PetUI 运行时执行。

![HachimoDock PetUI组件中心](https://image.lceda.cn/oshwhub/pullImage/410d87c82a0049d483f58391c23c5c72.jpg)

*组件可以在电脑端管理，再同步到桌面小屏。*

还有个挺能吸引小米用户的玩法：**MiLoCo 智能家居联动**。在桌面管理端授权米家账号、配置好对应能力后，可以用语音让受支持的设备执行操作，比如让音箱放爵士乐，或者把小屏切到相关控制界面。但这条链路是**电脑端对接 MiLoCo**，不是 ESP32-P4 自己加入米家网络；具体支持哪些设备，还得看账号授权、模型和 MiLoCo 服务条件。

复刻前最后再看一眼许可证。Github 当前 `LICENSE` 把 HachimoDock 定义为 **non-commercial source-available（非商业源码可见）**：个人学习、改造和非商业复刻在许可范围内，但出售套件、商用集成或基于它做独立收费产品，需要事先取得书面许可。嘉立创页面较早的 GPL-3.0-only 标注与当前源码许可证不一致，不能只看旧说明就开卖；MiLoCo 相关实现也有独立的小米许可约束。项目的硬件图、固件和桌面程序确实放出了不少东西，想自己做一台，最好从[官方 README](https://github.com/YizhengWw/HachimoDock)、[立创硬件复刻页](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc)和[固件烧录指南](https://github.com/YizhengWw/HachimoDock/blob/main/firmware/BUILD.md)三处对照着看。
