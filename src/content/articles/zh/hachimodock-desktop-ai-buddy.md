---
title: Github上有趣嵌入式项目——能盯AI任务、还能控制小米智能家居的桌面搭子HachimoDock
description: HachimoDock用ESP32-P4与2.8英寸DSI屏把Codex、Claude等Agent的任务状态变成桌面宠物动画，还支持按键语音、PetUI组件和小米MiLoCo联动。
locale: zh
translationKey: hachimodock-desktop-ai-buddy
pubDate: 2026-10-29
category: open-source
tags:
  - HachimoDock
  - ESP32-P4
  - 桌面 AI
  - 小米 MiLoCo
  - AI Agent
  - MIPI-DSI
  - PetUI
draft: false
seoTitle: HachimoDock桌面AI搭子：ESP32-P4、Codex状态跟随与小米MiLoCo联动
seoDescription: 拆解HachimoDock哈基米机：ESP32-P4硬件、2.8英寸DSI屏、USB-Agent架构、PetUI语音交互、立创PCB/BOM与非商业许可证。
---
做 AI 编程的人估计都有这个经历：把任务丢给 Codex 或 Claude，等它跑完，隔几分钟还得切回终端看看。它是在读文件、调用工具，还是停在某个授权弹窗前等你点确认？由小米技术委创新产品团队孵化的 HachimoDock 最近挺火，思路倒很直接——给电脑上的 Agent 安排一只桌面小狗。AI 忙着干活，旁边的桌面小狗也跟着换表情，思考、敲代码、等待确认、完成任务，一眼能看出来。

这只小狗的名字叫哈基米机，正式项目名 HachimoDock。项目由个人账号维护，软件固件放在 Github，PCB 和复刻资料放在立创开源硬件平台，并不是一款已经在小米商城上架的成品。

![HachimoDock桌面AI搭子实拍，西高地宠物显示在小屏幕上](https://image.lceda.cn/oshwhub/pullImage/6c47814b144549beb179528ea77cd75e.png)

*桌面上的 HachimoDock：前面三个实体键，右侧橙色摇杆，后面是一台运行 Agent 的电脑。图源：项目官方。*

*Github地址*

[https://github.com/YizhengWw/HachimoDock](https://github.com/YizhengWw/HachimoDock)

立创开源硬件平台地址

[https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc)

HachimoDock有个小屏幕，小屏本身不运行 Codex，也不在 ESP32-P4 上跑大模型推理。电脑端管理软件负责盯住 Agent Session，把工作状态、会话标题和需要用户处理的事件整理出来，经 USB 发给桌面设备。ESP32-P4 负责渲染宠物动画、状态气泡和 PetUI 小组件；反过来，按键、摇杆、麦克风产生的输入，也走 USB 交回电脑处理。支持的 Agent 包括 Codex、Claude、OpenClaw、MiMoCode、WorkBuddy，但**会话自动切换和可获取的信息因各家接口而异**。例如 WorkBuddy 不能只靠小屏切换气泡就自动切换电脑上的对话。

![HachimoDock Agent Session气泡界面](https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/assets/session-bubbles.webp)

*多个 Agent Session 以气泡呈现；完成和报错的任务会保留一段时间，避免提示一闪而过。*

主控选的是 **ESP32-P4**，双核 RISC-V，高性能核心最高 400 MHz；配套方案标注 32MB Flash 和 32MB PSRAM。显示屏是 **2.8 英寸、480×640 的 MIPI-DSI 竖屏**。这个选型挺有意思，通常 DIY 桌宠会找一块 SPI 小屏将就，HachimoDock 直接上 DSI，动画、字幕、气泡能分出更细的层次。机身留了三个凯华机械按键和一个四向带中键摇杆，还配麦克风、扬声器。三键各有短按/长按，摇杆四向与中键同样能配置动作，总计 12 种交互手势。这里尤其要注意，**当前交互主要靠实体按键、摇杆和语音，屏幕不要求具备触摸功能**。

![HachimoDock新版设备近景，三个机械按键及摇杆](https://image.lceda.cn/oshwhub/pullImage/0187d6df22f74724acda54e111c7c850.png)

*三颗机械键加摇杆的机身版本，摇杆并不是装饰品。图源：项目官方。*

电路上它也不是把 ESP32-P4 的每一个接口都重新做一遍：开发板负责主控、存储和主要接口，复刻 PCB 更多承担按键、摇杆及整机走线的整合。日常通信使用 USB-UART，固件仍保留原生 USB HS OTG 的硬件能力，但**不能把预留 USB OTG 等同于目前已经使用 USB 视频或 USB 音频设备协议**。屏幕接的是 DSI，不是外观相似的 CSI 排线座；动手前得核对屏幕排线定义及主控板修订版。

按立创的物料表，微雪 ESP32-P4-WIFI6 主控板约 81.15 元起，480×640 屏约 65 元，摇杆约 3.54 元，三颗凯华轴体约 12.7 元，再加喇叭、排母等，光这些已列报价的项目加起来就超过 **167 元**；PCB、结构件、运费和损耗还没全算进去。官方页面写的“150 元复刻”，更适合当成本参考，而不是装好就能用的包邮售价。GPIO、焊盘和 PCB 走线细节建议直接打开[立创项目的原理图与 PCB 预览](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc)，页面同时提供 BOM 和 STEP 结构文件，别只看一张整机宣传图就下单。

![HachimoDock物理按键配置界面](https://image.lceda.cn/oshwhub/pullImage/49606595868244acbb1fd15502b6f2df.png)

*按键映射可由 PC 管理端修改。该截图来自项目页面，界面可能与最新固件略有不同。*

### 它怎么变成一个真正能用的桌面搭子

先在 Windows x64 或 Apple silicon Mac 上安装 Pet Manager，再按芯片修订版烧录匹配的 ESP32-P4 完整镜像，USB 连上就能同步状态。完整烧录包不是单独一个应用 bin，还带分区表、默认形象和组件资源；**v1、v3 两类芯片镜像不能互刷**。日常升级尽量用管理端的固件升级，整片擦写会清除设备配置。官方还提醒，部分 Windows 电脑的 COM 口问题仍在排查。

亮点其实是 PetUI。屏幕不必永远只蹲着一只狗：你可以让 Agent 帮忙写番茄钟、喝水提醒、待办、电脑状态面板，或者一个两键小游戏，再由管理端把组件同步进去。组件会检查清单、资源路径和按键映射，避免一股脑塞入不符合 480×640 和设备容量限制的内容。长按语音键时，设备采音，电脑端 ASR 把识别文字送到选定的 Agent；是否能直接发送、是否需要先确认草稿，则依具体 Agent 和配置而定。实时聊天与语音播报另需可用的服务凭据，公开安装包不附送 API Key。

![HachimoDock语音输入演示界面](https://image.lceda.cn/oshwhub/pullImage/0dddebc05c064f3a812d278b7c5dbe6e.png)

*语音交互由桌面端负责识别与输入路由，界面会因不同 Agent 适配方式而变化。*

![HachimoDock PetUI组件中心与小游戏预览](https://image.lceda.cn/oshwhub/pullImage/410d87c82a0049d483f58391c23c5c72.jpg)

*PetUI 组件中心可以管理和同步小游戏、小工具。图源：立创项目。*

![HachimoDock Agent状态切换动画](https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/assets/agent-status.gif)

*官方状态动画：Agent 工作、等待或完成时，宠物会作出不同反馈。*

浏览器不支持内嵌视频时，可从 Github 查看对应动画素材。

*上面是仓库里的“思考中”宠物动画素材，不是硬件装配演示。*

浏览器不支持内嵌视频时，请从 Github 查看素材。

*官方“任务完成”动作素材。完整装配视频请到[立创项目附件](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc)下载。*

小米相关的部分也不是只贴个 logo。项目在桌面端接入 **MiLoCo**，获得米家账号授权后，部分已授权设备可以接受自然语言指令，比如控制智能灯具；实际能力要看账号、设备及服务权限。**这条链路由电脑端完成，不是 ESP32-P4 自己接入米家局域网。**第三方 MiLoCo 还有单独的 Xiaomi 许可条件，不能因为它跟 HachimoDock 一起使用，就默认拿到商业授权。

最后说个复刻前必须看的地方：Github 当前版本把项目定位为 **non-commercial source-available**，自有源码允许个人非商业学习、修改和复刻，但做收费产品、商业集成或独立衍生服务需要权利人另行书面授权；它不是 GPL、MIT 那类标准开源许可。立创页面较早的 GPL-3.0 标注与当前仓库不一致，准备拿去做产品的人要看最新 [LICENSE](https://github.com/YizhengWw/HachimoDock/blob/main/LICENSE)。

**相关资料：** [项目源码及说明](https://github.com/YizhengWw/HachimoDock) · [硬件原理图 / PCB / BOM / 装配视频](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc) · [最新客户端与烧录包](https://github.com/YizhengWw/HachimoDock/releases/latest) · [固件烧录指南](https://github.com/YizhengWw/HachimoDock/blob/main/firmware/BUILD.md)。