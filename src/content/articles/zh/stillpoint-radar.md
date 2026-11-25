---
title: "Stillpoint：一台不装摄像头的 60GHz 天花板雷达"
description: "用 Infineon BGT60TR13C 和 Silicon Labs EFR32MG26 做的 Ø60mm 吸顶传感器：存在、姿态和跌倒检测，Matter over Thread 上报，不装摄像头，也不依赖云。"
locale: zh
translationKey: stillpoint-radar
pubDate: '2026-11-25'
category: open-source
series: open-hardware
contentType: deep
tags:
- Stillpoint
- 60GHz 雷达
- BGT60TR13C
- EFR32MG26
- Matter
- Thread
- 跌倒检测
- 开源硬件
draft: false
sourceUrl: https://github.com/techmiguel/stillpoint
author: EmbeddedNote
seoTitle: "Stillpoint：不装摄像头的 60GHz 天花板雷达"
seoDescription: "拆解 Stillpoint：BGT60TR13C 60GHz FMCW 雷达、EFR32MG26、Matter over Thread，以及存在、姿态和跌倒检测背后的 DSP、PCB 与 radome 设计。"
---

大多数室内存在传感器都要在隐私和功能之间做取舍。摄像头能看到姿态和跌倒，但也会产生图像；PIR 便宜、不采集图像，但人一坐定就看不见。Stillpoint 用第三种办法：把 60GHz FMCW 雷达装进一个吸顶的 Ø60mm 圆盒，数人、估计站/坐/躺、判断跌倒，结果通过 Matter over Thread 发出。没有摄像头、麦克风、云账号，也没有图像流。

项目由 Miguel（techmiguel）在 2026 年 10 月开源，许可证为 CERN-OHL-S-2.0。仓库里有 KiCad 原理图和四层板、FreeCAD 外壳、C 固件，以及一套 Python 参考实现。它是 rev A 设计：板子已经画完、检查过，但还没有下单，也没有在实物上验证。

| 项目 | 内容 |
| --- | --- |
| 名称 | Stillpoint，开源硬件吸顶传感器 |
| 雷达 | Infineon BGT60TR13C，60GHz FMCW，1 TX / 3 RX，天线在封装内 |
| 主控与无线 | Silicon Labs MGM260P（EFR32MG26，Cortex-M33 + MVP），Matter / Thread / BLE |
| 板子 | Ø60mm，四层，1.6mm，ENIG，74 个器件 |
| 输出 | 存在、人数、三维位置、姿态、跌倒状态 |
| 外壳 | Ø65mm × 24mm PETG 圆盒，Ø77mm 天花板底盘 |
| 许可 | CERN-OHL-S-2.0 |
| 状态 | rev A 设计文件；实物 bring-up 尚未完成 |

**GitHub：** https://github.com/techmiguel/stillpoint

![Stillpoint 爆炸图：天花板底盘、盖子、Ø60mm 主板和带 radome 的外壳](/uploads/stillpoint/stillpoint-exploded.webp)

*天花板底盘、盖子、Ø60mm 主板，以及底面作为 radome 的外壳。图片：Miguel / Stillpoint*

## 两个运动通道

雷达扫 60.0–61.25GHz，1.25GHz 带宽，距离分辨率 12cm。每帧 32 个 chirp、每个 chirp 128 个采样点，3 个接收通道，10Hz 出帧，最远 7.7m。接收天线是 L 形，能同时给方位和俯仰，所以输出是三维位置和高度，不是平面上的一个方向。

处理链很早就分成两路。一路用 MTI、Doppler、CFAR 和角度测量跟踪走动的人；另一路攒 10 秒相位，找呼吸引起的胸廓微动。两路合成 3D 检测后进入跟踪器。

跟踪器里有很多房间逻辑。确认过的 track 只有在出口区域才会被快速删除；在房间中间被挡住时保留 60 秒，如果出现过呼吸则保留 120 秒。风扇、镜子产生的多径、看起来穿墙的鬼影都单独处理。每条 track 压成 66 字节的特征记录，每 0.5 秒送进一个 14.6KB 的 int8 CNN。模型不看绝对 x、y、距离和 track 状态，避免把训练房间的几何记进去。

![遮挡场景：坐着的人被标成 occluded 保留](/uploads/stillpoint/stillpoint-occlusion.webp)

*遮挡测试里，坐着的人被标成 occluded 保留，而不是直接删掉。图片：Miguel / Stillpoint*

![空房间开风扇：风扇被学成干扰源](/uploads/stillpoint/stillpoint-fan.webp)

*空房间开风扇：风扇被学成干扰源，不会变成一个人。图片：Miguel / Stillpoint*

“静止的人”是第二条路径存在的理由。传统 MTI 会把不动的目标滤掉，而坐在椅子上的人恰好就是不动的那一个；呼吸通道把他找回来，同时不用把所有人的运动阈值都调低。

## 跌倒判断为什么要留 4 秒

跌倒不是一个分类器分数说了算。模型给出怀疑，或者检测到快速下坠，才会开一个 suspected；确认还需要人在 4 秒内保持躺在地上不动。确认不了就报 uncertain，不会静默丢掉。项目把它称为 fail-safe 决策，不是医疗诊断。

同一套逻辑也跑在仿真回归里。公开的测试集包括真跌倒、躺床和蹲下三种动作；只有真跌倒会走到 confirmed，另外两种都停在阈值以下。另有遮挡、空房间风扇、镜子反射和跌倒的场景文件。

![真跌倒、躺床、蹲下的高度、垂直速度和跌倒概率](/uploads/stillpoint/stillpoint-fall.webp)

*真跌倒、躺床、蹲下三种动作的 z 高度、垂直速度和 p(fall)。这组仿真里只有真跌倒走到 confirmed。图片：Miguel / Stillpoint*

README 和项目页都写明“不是医疗设备”。跌倒通知不能替代随身报警器、定时问候或其他安全措施。

## 板子的难点在雷达的地

PCB 是 Ø60mm、1.6mm 四层板，ENIG 表面，74 个器件。雷达在底面，透过 radome 朝下看；Matter/Thread 模块在板边，按数据手册留出天线净空。

USB-C 进来 5V，TLV75733P 出 3.3V；TPS7A2018 给雷达出 1.8V，噪声 7µVrms。雷达的 RF、PLL、VCO、模拟、数字、环路滤波和晶振各自一路铁氧体，配 100nF / 1µF / 10µF，走成一条直线，最小的电容离 BGA 球最近。80MHz 晶振离雷达 4mm，串联 150Ω。

硬件文档里占篇幅最多的是地。BGT60TR13C 是 0.5mm 间距 BGA；L2 整层地，L3 是 3.3V 平面，但在雷达正下方挖出一块完整地岛。球阵里只放地过孔，自定义 DRC 规则不允许其他网络进入雷达下面的内层。雷达的控制线和数据线分到两片电平转换器上，分别放在板子两面，避免任何一条雷达线交叉。

![Stillpoint 主板正面：MGM260P、电平转换和雷达电源滤波](/uploads/stillpoint/stillpoint-board-top.webp)

*正面：MGM260P 模块在板边，中间是电平转换和雷达电源滤波。图片：Miguel / Stillpoint*

![Stillpoint 主板背面：BGT60TR13C、80MHz 晶振和 RGB 灯](/uploads/stillpoint/stillpoint-board-bottom.webp)

*背面：BGT60TR13C 雷达、80MHz 晶振和 RGB 状态灯。图片：Miguel / Stillpoint*

设计报告 ERC 0 error、DRC 0 violation，原理图和 PCB 对齐，BOM/CPL 也和板子对过。但这些是设计检查，不能证明实物一定能过 bring-up、热测试或 EMC。

![Stillpoint 原理图：按功能分块](/uploads/stillpoint/stillpoint-schematic.webp)

*原理图按功能分块：USB-C 与电源、雷达七路供电、电平转换、MGM260P、BGT60TR13C、CP2102N 和测试点。图片：Miguel / Stillpoint*

## radome 也是射频设计

外壳是 Ø65mm、24mm 高的 PETG 打印件，装在 Ø77mm 天花板底盘上。底面不是装饰盖，而是 1.48mm 厚的 radome，正好是 60.6GHz 下所选塑料的半波长，单程损耗约 0.15dB。雷达天线离它 4.95mm，正好一个自由空间波长。

板子靠三个支撑柱定位，盖子用三个柱子压住；USB-C 从盖子中间出去，贴着天花板走线。FreeCAD 脚本会加载真实板子的 STEP，检查壳体、盖子和 radome 有没有干涉，并确认 ±60° 天线视场里没有塑料。

![radome 尺寸剖面、传输损耗和 FreeCAD 零件](/uploads/stillpoint/stillpoint-mechanics.webp)

*左边是尺寸剖面，中间是 radome 损耗随厚度的变化，右边是 FreeCAD 零件。图片：Miguel / Stillpoint*

## 哪些是设计，哪些还没验证

对一个处于这个阶段的项目来说，仓库已经很完整：原理图、PCB、制造文件、FreeCAD 外壳、C 固件、Python 参考、特征契约、golden vectors 和回归图都在。C 实现和 Python 参考逐帧对照，README 说计数一致、量化特征至少 99.8% 相同、姿态/跌倒/报警时间一致。

但这仍然是仿真和主机侧验证。硬件文档明确说，板子要等 F2 套件验证完才下单；bring-up 清单里还有 1:1 打印、极性、CPL 旋转和首次上电没打勾。架构文档里的功耗、CPU 和 RAM 是估算，不是实测。仓库里没有独立的跌倒数据集、EMC 报告或热测试。

![C 固件和 Python 参考在四种场景下的对照](/uploads/stillpoint/stillpoint-c-vs-python.webp)

*C 固件和 Python 参考在跌倒、躺床、蹲下、遮挡四组场景下的对照。图片：Miguel / Stillpoint*

## 工程核对

| 说法 | 依据 |
| --- | --- |
| 60GHz FMCW，1 TX / 3 RX | BGT60TR13C 数据手册和 KiCad 符号；天线在封装内 |
| 12cm 距离分辨率，7.7m 量程 | 1.25GHz 扫频、每 chirp 128 个采样点，见 `docs/architecture.md` |
| 存在与呼吸通道 | Python 参考和 C 移植；在仿真场景上测过，没有真实房间数据 |
| 跌倒 4 秒确认 | 决策状态机和回归图；没有临床验证 |
| Ø60mm 四层板 | KiCad 板、叠层和制造说明 |
| 1.48mm radome，4.95mm 间距 | FreeCAD 模型和传输曲线；没有实测天线方向图 |
| Matter over Thread | 固件桥和 Matter cluster 定义；没有物理认证 |

没有验证的部分：实物板、真实雷达量程和精度、真实家居环境下的跌倒灵敏度和误报率、功耗、热行为、EMC、固件安全和隐私。它是一个文档完整的设计，不是已经出货的产品。

项目页的演示是浏览器里的示意，不是录制的传感器数据：https://techmiguel.github.io/stillpoint/。仓库目前没有视频文件。

## 资料

- [Stillpoint 仓库](https://github.com/techmiguel/stillpoint)
- [`docs/architecture.md`](https://github.com/techmiguel/stillpoint/blob/main/docs/architecture.md)
- [`docs/hardware.md`](https://github.com/techmiguel/stillpoint/blob/main/docs/hardware.md)
- [项目页](https://techmiguel.github.io/stillpoint/)
