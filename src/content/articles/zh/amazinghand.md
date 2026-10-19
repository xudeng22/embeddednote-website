---
title: Github上有趣嵌入式项目——开源灵巧手AmazingHand，8个舵机装出一只手
description: Pollen Robotics 开源的 AmazingHand 四指灵巧手，采用 8 颗 Feetech 串口舵机、并联连杆和 3D 打印外壳，并提供装配、标定和控制代码。
locale: zh
translationKey: pollen-amazinghand-8dof
pubDate: '2026-10-19'
category: open-source
tags:
- AmazingHand
- Robotics
- Open Source Hardware
- Servos
- 3D Printing
draft: false
sourceUrl: https://github.com/pollen-robotics/AmazingHand
author: EmbeddedNote
seoTitle: AmazingHand 开源灵巧手：8 个舵机与四指并联机构
seoDescription: AmazingHand 开源 8 自由度四指灵巧手，采用 Feetech SCS0009 舵机和 3D 打印件，附硬件结构、装配文件和控制方法。
---

一说起灵巧手，第一反应基本是两个极端：要么是动辄几万块的商业化方案，要么是实验室里那种电机全堆在手臂上、靠钢丝绳一根根牵手指的复杂结构。Pollen Robotics这家做开源人形机器人Reachy2的公司，偏要在中间找个平衡点——Amazing Hand一只8自由度的四指手完全开源，执行器全部塞进手掌，没有一根外露线缆，整只手400克，材料加舵机不到200欧就能攒出来，图纸、代码、装配文档一股脑全挂在Github上。

Github地址：

https://github.com/pollen-robotics/AmazingHand

软件部分Apache 2.0、机械设计CC BY 4.0，BOM清单、3D模型、装配手册、控制代码都在里面，没有藏着掖着。不想自己打印的也有现路，Seeed Studio和WowRobo都挂了套件，装好就能玩，上手不用等。整手用料也实在，打印件之外就是舵机、球铰拉杆和少量标准件，成本大头基本都在那8个舵机上。

![AmazingHand 四指机械手尺寸与关节活动范围](/uploads/amazinghand/amazinghand-cover.webp)

整只手400g，四指、8自由度，表面几乎看不到线缆

![AmazingHand 灵巧手与 Reachy2 机械腕接口实物结构](/uploads/amazinghand/amazinghand-02.jpg)

8个自由度分布在4根手指上，每根手指两根指节、两节联动，由一个并联机构驱动，两个小舵机分管屈伸和外展内收。舵机用的是飞特（Feetech）的SCS0009，TTL串行总线舵机，塑料壳金属齿，自重13克上下，6V下堵转扭矩2.3kg.cm，有效转角300°，位置、电压、温度、扭矩这些状态都能读回来，比普通PWM舵机好伺候得多。两个舵机藏在手指根部，通过连杆和球铰把动作传到指节上，没有腱绳、没有钢丝，拆开看一眼结构就明白了，修起来也不用跟一坨线束搏斗。

![单指两舵机并联连杆机构及屈伸与侧摆运动](/uploads/amazinghand/amazinghand-03.jpg)

外壳几乎全是3D打印件，表面带柔性设计，既省成本又有点手感。左右手件用L/R前缀镜像区分，手指部分两只手通用，打印参数和建议官方单独写了份文档，普通FDM机器就能打。

![AmazingHand 多种手指姿态演示](/uploads/amazinghand/amazinghand-04.jpg)

3D打印的柔性外壳，官方打印指南里连参数都写好了

![3D 打印零件清单及材料建议](/uploads/amazinghand/amazinghand-05.jpg)

打印件清单表，每种件的材料、数量和备注都列好了

![3D 打印排版与打印参数示例](/uploads/amazinghand/amazinghand-06.jpg)

控制方式给了两条路，任选其一。一条是Waveshare串行总线驱动板，USB插电脑跑Python脚本；另一条是Arduino加一块Feetech TTL Linker转接板。8个舵机在同一条TTL总线上级联，靠ID寻址，食指1/2号、中指3/4号、无名指5/6号、拇指7/8号，想左右手挂同一条总线就把ID错开，不然谁都指挥不动。官方给了标定脚本和演示程序，通电就能看手比划。供电这块得单独准备，8个舵机一起动，建议外部5V/2A往上的DC电源，圆头接口，项目里直接建议用220V转5V的适配器。

![左右手舵机编号与安装结构](/uploads/amazinghand/amazinghand-07.jpg)

手腕接口是按Reachy2的Orbita 3D手腕做的。Orbita 3D是Reachy2脖子和手腕都在用的三自由度并联执行器，三个同心电机轴，每个轴是40W的无刷减速电机，FOC控制、走EtherCAT，这手直接拧上去就能用。接口尺寸全是公开的，改一改也能接别的机器人手腕，社区里已经有人把它接到了SO-ARM机械臂上。

![AmazingHand 与 Reachy 2 腕关节安装示意](/uploads/amazinghand/amazinghand-08.jpg)

物料清单挂在Google文档上，有网友整理了中文版BOM，照着买就行。所有打印件给了STL和Step文件，Onshape在线CAD模型也公开，命名位置里预置了一堆手势对应的舵机角度，不用自己瞎试。装配有官方PDF手册，标定每根手指也有现成脚本，Python和Arduino各一份，接好线跑一遍就能让指节对正。打印件清单单列了一张表，每种件几个、支撑怎么加都标了，官方还给了打印排版的建议，省得自己瞎摆盘。

![AmazingHand 物料清单和参考成本](/uploads/amazinghand/amazinghand-09.jpg)

![AmazingHand 手指组件装配步骤](/uploads/amazinghand/amazinghand-10.jpg)

装配手册配图，按顺序来就行

![Onshape 中可直接调用的手势角度预设](/uploads/amazinghand/amazinghand-11.jpg)

Onshape里预置了命名位置，各种手势的舵机角度直接查

![两只 AmazingHand 摆出爱心姿态](/uploads/amazinghand/amazinghand-12.jpg)

官方CAD文件里的小彩蛋，两只手拼出一个心形

社区里玩得花的不少。有人拿SG90舵机加力控复刻了一版，代码照常开源，成本还能再压；有人写了AmazingHandControl这套Python GUI，能实时看舵机反馈、录手势动画回放；还有人加弯曲电阻做指尖力觉，配视觉动作捕捉玩遥操，直接当模仿学习的数据采集工具用。

官方放了个手部追踪的演示视频：

https://www.youtube.com/watch?v=U0TfeG3ZUto，

仓库里还挂了个基础demo视频：

https://github.com/user-attachments/assets/485fc1f4-cc57-4e59-90b5-e84518b9fed0。

![SG90 舵机复刻版机械手抓取示例](/uploads/amazinghand/amazinghand-13.jpg)

SG90加力控的复刻版，成本还能再压一截

![社区力控机械手测试台](/uploads/amazinghand/amazinghand-14.jpg)

力控改造的完整测试台，代码也在GitHub挂着

![AmazingHandControl Python GUI 舵机监测界面](/uploads/amazinghand/amazinghand-15.jpg)

第三方GUI工具，实时监控加手势动画录制

![社区设计的 Amazing Base 支架](/uploads/amazinghand/amazinghand-16.jpg)

社区做的Amazing Base底座，手可以直接立起来当摆件

缺点作者也交代得实在。3D打印件精度就那样，球铰拉杆一根根手工调的，塑料件本身有柔性，实际角度和理论值多少对不上；整机还没做过长时间高强度的抓取测试，想安全抓起东西不伤舵机，还得先攒一套智能控制软件。好在SCS0009自带扭矩使能、扭矩反馈、位置传感器和温度反馈，后面做闭环抓取的基础是有的。仓库还分出了Amazing Hand Enhanced增强版分支，新改动都在那边推进。
