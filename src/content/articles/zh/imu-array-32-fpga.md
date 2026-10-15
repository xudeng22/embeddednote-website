---
title: GitHub 上超硬核嵌入式项目：32 颗 IMU 与 FPGA 阵列，探索地震检波器替代方案
description: 32 颗 ICM-42688-P、iCE40 FPGA 与 RP2040 组成 MEMS 阵列，分析同步采样、低频噪声、艾伦方差与传感器标定。
locale: zh
translationKey: imu-array-32-fpga
pubDate: '2026-09-19'
category: hardware
tags:
- IMU
- FPGA
- RP2040
- ICM-42688-P
draft: false
seoTitle: GitHub 上超硬核嵌入式项目：32 颗 IMU 与 FPGA 阵列，探索地震检波器替代方案
seoDescription: 32 颗 ICM-42688-P、iCE40 FPGA 与 RP2040 组成 MEMS 阵列，分析同步采样、低频噪声、艾伦方差与传感器标定。
---

索尼给SPRESENSE做过一块多IMU板，16颗民用MEMS IMU实时合成，精度直接对标工业级光纤陀螺仪，偏置稳定性测到了0.39deg/h以下。这板子牛到什么程度——受出口管制，Will Whang明确表示自己大概率拿不到。拿不到就自己造，于是有了这个项目：一块板上怼了32颗TDK/InvenSense的ICM-42688-P，外加一颗Lattice ICE40UP5K FPGA当数据搬运工，目标是一个地震检波器（geophone）的替代方案。

![imu array 32 fpga — 图片 1](/uploads/imu-array-32-fpga/imu-array-32-fpga-01.webp)

![imu array 32 fpga — 图片 2](/uploads/imu-array-32-fpga/imu-array-32-fpga-02.webp)

GitHub地址：

https://github.com/will127534/IMU_Array

https://www.willwhang.dev/Project-IMU-Array/

先说说他为什么要这么折腾。Will Whang之前做过一个基于geophone的地震仪项目，检波器低频响应差，得靠NIC（负阻抗变换器）去抵消线圈内阻，于是一堆运放、数字电位器、模拟开关全上了，还容易过补偿振荡，复杂到他至今懒得写文档。他的想法很直接：用一堆便宜的MEMS IMU，靠阵列平均把噪声压下去，把那些又贵又麻烦的模拟电路和ADI芯片全干掉。所以这个项目的重点从头到尾都在加速度计的低频噪声和艾伦方差上，陀螺仪的动态性能他压根没怎么花心思。

## 传感器板：32颗IMU怎么摆是个学问

传感器板是整件事的核心。中间一颗ICE40UP5K QFN48，四周均匀摆上32颗ICM-42688-P，板子做成了正方形。为什么不用三点固定那种更利于减小机械应力的三角布局？因为阵列讲究4颗一组旋转摆放，用来抵消不同轴向的灵敏度差异——索尼那块板也是这么排的——三角形跟这种排法天生冲突，只好退而求其次，正方形布局但把对角线位置空出来不放IMU。

![imu array 32 fpga — 图片 3](/uploads/imu-array-32-fpga/imu-array-32-fpga-03.webp)

板子选了6层，via-in-pad，0.2mm过孔，紧凑尺寸下还得保证几十兆赫兹信号的完整回流路径。电源只有3.3V和1.2V两路，全部从FPC排线引进来，板上不额外放热源。FPC座子专门挑了Mouser上能买到的最窄的22pin型号，作者手头正好有一堆树莓派相机模组的22pin排线，引脚定义也照顾到了，SPI信号之间夹地线做回流。

![imu array 32 fpga — 图片 4](/uploads/imu-array-32-fpga/imu-array-32-fpga-04.webp)

![imu array 32 fpga — 图片 5](/uploads/imu-array-32-fpga/imu-array-32-fpga-05.webp)

## FPGA只当搬运工，同步靠的是CLKIN

这里FPGA干的活其实很单纯，作者原话是“主要就是个数据聚合器”。32路MISO汇总到FPGA，SPI配置口兼职跟主控通信，bitstream得由主控在上电时传进去。FPGA不控制IMU的CS，也没有多余引脚接DRDY，所以它没法主动发起读取，只能当个中转站。板子剩的3个GPIO还接了3颗LED当状态机指示，反正对角线那块地方空着也是空着。

真正让32颗IMU能同步采样的不是FPGA，而是TDK这颗IMU自带的CLKIN功能。所有IMU共用一颗32KHz外部时钟，内部同步逻辑全部对齐，采样动作天然同时发生，后续数据处理就不用操心对齐问题了。采样率设为200Hz，中断加外部时钟一起开着。Gateware这边也折腾了一下，最初SPI逻辑挂在48MHz内部时钟上，速率被压到5MHz左右；后来改成直接用SCK驱动（作者管它叫Async SPI core），一下子拉到20MHz。代价是主机读数据时的CPHA相位设置得配合着改，属于跨时钟域问题的偷懒解法，作者自己都说了“这不是理想方案，先记到TODO里”。

## RP2040、Type 1YN和一颗能微调的VCTCXO

![imu array 32 fpga — 图片 6](/uploads/imu-array-32-fpga/imu-array-32-fpga-06.webp)

处理板这边主控是RP2040。WiFi用的是Murata Type 1YN，就是树莓派Pico W那颗CYW43439的最小封装模组，RP2040只需要3个GPIO就能驱动——WL_CLK、WL_D（把SDIO的CMD和DATA合并成一条线）、WL_CS。GPS是LC76K，为了在CNC铝合金外壳里能搜到星，还加了一级SAW滤波加低噪声放大器的GNSS前端，作者自己都惊讶这套组合在封闭金属壳子里居然能正常工作。

![imu array 32 fpga — 图片 7](/uploads/imu-array-32-fpga/imu-array-32-fpga-07.webp)

时钟部分更有意思，板子上没有普通的12MHz晶振，放的是一颗可以调频的VCTCXO，用PWM DAC微调频率跟着GPS的PPS走，相当于做个简易GPSDO，既要给RP2040提供时钟，又要输出那颗稳定的32KHz给IMU阵列。

![imu array 32 fpga — 图片 8](/uploads/imu-array-32-fpga/imu-array-32-fpga-08.webp)

供电也很有个人风格：因为这板子定位是户外埋地用的检波器替代品，作者一度打算直接吃门铃的24V AC——墙上不用再打孔——板上专门留了电容阵和整流桥，后面改版才去掉。外壳用三个M8螺丝孔装音箱常用的减振脚，整机CNC加工。

![imu array 32 fpga — 图片 9](/uploads/imu-array-32-fpga/imu-array-32-fpga-09.webp)

软件路线也踩了不少坑。最初用CircuitPython调FPGA，好处是模拟U盘，bitstream当文件拖进去就自动加载，二进制格式不用转成C头文件；但CircuitPython没实现真正的终端中断，读不了DRDY，只能又搬回MicroPython。MicroPython里WiFi又出幺蛾子——Type 1YN的OTP没烧MAC地址，CircuitPython默认用随机MAC能跑，MicroPython却不行，还找不到地方改。最后FPGA代码稳定了，作者干脆转回C SDK专心优化性能。把RP2040超频到250MHz之后，MicroPython就能以100Hz把32颗IMU的全量数据通过UDP或USB CDC发回主机了，说实话这个结果挺让人意外的。

![imu array 32 fpga — 图片 10](/uploads/imu-array-32-fpga/imu-array-32-fpga-10.webp)

结果怎么评估？作者在没人的时候把传感器放地板上测长时数据，画艾伦方差。32颗陀螺仪平均后的曲线确实把单颗的毛刺抹平了不少，加速度计的Z轴曲线跟X/Y轴长得不一样，这也是MEMS芯片Z轴结构本来就跟X/Y不同所导致的。比较尴尬的是，他照着索尼论文去复现干扰抑制和野值滤波的算法，短时间（0.2秒内）确实有改善，但到了300秒量级，野值滤波反而比单纯平均还差，作者自己承认这部分复现失败了。

![imu array 32 fpga — 图片 11](/uploads/imu-array-32-fpga/imu-array-32-fpga-11.webp)

不过校准那块是实打实成功的。参考了一篇论文的思路，不用转台也能标定阵列里每颗IMU的失准角：3D打印一个正二十面体，把传感器塞进去，20个位置每个采90秒，靠重力和陀螺数据算出每颗的失准角和灵敏度，再按论文的Matlab代码生成头文件，烧进RP2040做融合。

![imu array 32 fpga — 图片 12](/uploads/imu-array-32-fpga/imu-array-32-fpga-12.webp)

项目还在持续更新，V1.1加了USB口，外壳换了个4pin的M5螺纹防水连接器，板载GPS天线也拆了——毕竟可能真要被埋到地底下。硬件工程文件、Verilog、MicroPython代码全在GitHub上开源，Gerber、BOM、CPL都齐，可以直接丢给板厂打样（PCBWay赞助了这个项目）。作者在README里也写得很坦诚：代码还很早期，ODR、FSR这些基本靠手算寄存器值，Verilog别细看，反正ICE40UP5K便宜，懒得省LUT。
