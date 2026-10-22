---
title: Github上有趣嵌入式项目——带操纵杆的全开源分体键盘Tiwaz
description: Tiwaz是一款带双摇杆的开源分体键盘，每半边采用STM32F401、38个热插拔轴座与6个辅助键，并支持QMK/Vial和3D打印外壳。
locale: zh
translationKey: tiwaz-split-keyboard
pubDate: '2026-10-21'
category: open-source
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/tstrube/Tiwaz
tags:
- Tiwaz
- 分体键盘
- STM32F401
- QMK
- 摇杆
- 开源硬件
seoTitle: Tiwaz全开源分体键盘：STM32F401、双摇杆与QMK
seoDescription: 拆解Tiwaz开源分体键盘的双摇杆、STM32F401、热插拔MX轴、RGB背光、PCB保护与Gasket结构。
---

客制化键盘圈这些年卷配列、卷轴体、卷Gasket手感，Tiwaz偏要在键盘上直接装两个操纵摇杆。作者Timo Strube本职做软件和电子样机开发，他把整个项目开源在Github上：硬件GPLv3、固件GPLv2，外壳是3D打印件，项目已在Crowd Supply 上开设众筹预告页面（截至2026年10月尚未正式开始众筹），图纸、固件、装配文档全部公开。

项目地址：[GitHub 源码与设计资料](https://github.com/tstrube/Tiwaz) · [Crowd Supply 项目页面](https://www.crowdsupply.com/ts-consulting/tiwaz)

这是一把分体键盘，左右各一半，中间用一条AUX线连起来，每一半都能独立当单手控制器或者宏键盘用——对左手用鼠标的玩家来说，这算是市面上极少数专门为左撇子考虑过的游戏键盘。板载STM32F401RET6主控（Cortex-M4跑84MHz，512KB Flash），每半边38颗热插拔MX轴座、6颗辅助按键默认当媒体键，每颗键、每颗按钮都带独立的WS2812 RGB背光，灯效动画随便调，USB Type-C接口。

![Tiwaz蓝色背光双摇杆分体键盘实物图](/uploads/tiwaz/tiwaz-cover.webp)

*分体设计，左右两半靠一条AUX线连接*

![Tiwaz左半键盘与橙色摇杆特写](/uploads/tiwaz/tiwaz-02.jpeg)

*左半特写，右下角那个圆头就是摇杆*

![无背光的黑色3D打印键盘](/uploads/tiwaz/tiwaz-03.jpeg)

*关掉背光的样子，外壳是纯黑3D打印件*

这键盘最核心的卖点是操纵摇杆。官方给了两种选择：Alps Alpine的RKJX21224001，游戏掌机和VR手柄上常用的新款；还有PSP3000同款的RKJXU1210006。都是二轴模拟摇杆，但只有RKJX21224001带中心按压开关，两者均通过FPC排线连到PCB，两个型号的接口位置完全一样，想换直接换壳里的插片，排线一拔一插的事，作者自己更喜欢RKJX21224001，控制精度高还带集成按键。摇杆用FN加最底下那颗媒体键切换三种工作模式：数字模式（蓝灯）把摇杆当方向键按，模拟模式（黄灯）被识别成手柄轴，鼠标模式（红灯）可用RKJX21224001控制指针、按下就是点击，拖拽和右键也有讲究。PCB上还把摇杆的引脚引出来了，3V3、B、X、Y、GND一排焊盘，想接自己的应用随便折腾。

![Tiwaz两款可选摇杆](/uploads/tiwaz/tiwaz-04.png)

*两种摇杆选项，左边RKJX21224001，右边PSP3000同款*

![Tiwaz摇杆FPC接口和引出焊盘](/uploads/tiwaz/tiwaz-05.jpeg)

*摇杆FPC接口和引出的焊盘，X/Y轴、按键、3V3、GND都在*

主控方面作者最初用的是树莓派同款RP2040，几版样机测下来发现，电脑开机进BIOS/UEFI那一下键盘根本来不及初始化，直接换成STM32F401才解决——仓库里PCB背面的老图还能看到RP2040的影子。半对半之间的AUX线既传数据也供电，只有一头接电脑，防呆设计做得很全：理想二极管防止两头同时插电脑把两边都烧了，自恢复保险丝兜住LED的大电流，USB和AUX都加了ESD保护，官方文档里还提了EMI和防回灌的处理。

![Tiwaz PCB正面](/uploads/tiwaz/tiwaz-06.jpeg)

*PCB正面，38个热插拔轴座加6颗媒体键*

![Tiwaz早期RP2040版本PCB背面](/uploads/tiwaz/tiwaz-07.jpeg)

*背面这张还是老版RP2040的图，后来换成了STM32F401*

![Tiwaz PCB顶层布线](/uploads/tiwaz/tiwaz-08.png)

*PCB顶层走线*

![Tiwaz PCB底层布线](/uploads/tiwaz/tiwaz-09.png)

*底层走线，布局压得很紧凑*

结构上走的是客制化键盘那套：Gasket安装板加缓冲棉，定位板和PCB之间、PCB和外壳之间都垫了减震材料，手感比硬邦邦的钢板扎实。外壳设计时专门考虑了CNC可加工性——内角不留尖角、外角简单倒角，尺寸公差卡得比较紧，作者提醒说3D打印机的调校得在线，不然Gasket的效果会打折。键帽是个坑，背光、人体工学、清一色1u的配列，成品套装基本找不到，作者最后找了一家能定制背光键帽的厂子专门做。

![Tiwaz键盘Gasket堆叠结构](/uploads/tiwaz/tiwaz-10.png)

*键盘堆叠结构：定位板、缓冲棉、PCB、外壳一层层摞*

![Tiwaz单侧组件拆解](/uploads/tiwaz/tiwaz-11.jpeg)

*单侧全部零件摊开，装起来并不复杂*

![Tiwaz单侧键盘3D设计图](/uploads/tiwaz/tiwaz-12.png)

*3D渲染图，外壳线条挺干净*

固件这块直接对齐开源生态。QMK官方仓库的PR还挂着，VIAL分支也已经能用，VIAL最大的好处是不用刷固件，浏览器打开网页就能把按键、摇杆、灯效全部重新映射。有个细节挺有意思：摇杆模式切换的指示颜色是写死在固件里的，README里专门提醒别改这个映射，不然切模式的时候灯色就乱了。

缺点来看，38键的配列对习惯全键盘的人来说适应期跑不掉，码字和打游戏来回切换要掂量；摇杆的鼠标模式在PSP摇杆上不支持，只有RKJX21224001能用；外壳精度要求高，手头打印机拉胯的话建议直接买套件。不过整体看下来，Tiwaz把"客制化键盘"和"游戏控制器"揉在了一起，思路在键盘圈里算野路子，对键盘党和嵌入式玩家来说都挺新鲜，光是为左手玩家开一条路这一点就值得点个赞。

资料与图片来源：[Tiwaz GitHub 项目](https://github.com/tstrube/Tiwaz)（Timo Strube）；[Crowd Supply 产品页面](https://www.crowdsupply.com/ts-consulting/tiwaz)。
