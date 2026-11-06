---
title: 电子纸竟能跑30 FPS？ESP32-S3把Game Boy搬上1.54英寸墨水屏
description: InkBoy在ESP32-S3和1.54英寸200×200电子纸上演示约30次/秒的Game
  Boy画面更新，解析SSD1681逐像素驱动、双显示模式和面板寿命风险。
locale: zh
translationKey: inkboy-epaper-game-boy-30fps
pubDate: 2026-10-15
category: display
tags:
  - InkBoy
  - ESP32-S3
  - 电子纸
  - Game Boy
  - SSD1681
  - 30 FPS
draft: false
seoTitle: ESP32-S3电子纸跑Game Boy：InkBoy如何实现约30 FPS更新
seoDescription: 1.54英寸200×200电子纸实现约30
  FPS更新？看InkBoy如何用SSD1681短波形、逐像素HOLD和ESP32-S3运行Game Boy，以及残影和寿命风险。
updatedDate: '2026-11-06'
---
一块 1.54 英寸电子纸，正常局部刷新要几百毫秒，拿来玩 Game Boy，听着就像故意给自己找麻烦。开发者 Bo Made It 偏偏在微雪 ESP32-S3 开发板上做出了约 **30 FPS** 的演示：画面能跟着游戏动，黑白像素和四级灰阶都能跑。项目叫 **InkBoy**，用的是 200×200 电子纸，并不是换了一块高刷 LCD。10 月 14 日，Hackaday 报道了这个实验。

![InkBoy 1.54 英寸电子纸运行 Game Boy 的专题封面](/uploads/inkboy/inkboy-cover.webp)

*文章封面为编辑绘制的示意图，下面是作者项目的原始演示图片和视频。*

### 30 FPS 是怎么挤出来的

关键在 **SSD1681 控制器的驱动波形**。原厂一次局部更新约需 360 ms；InkBoy 不走完整的默认波形，而是给每个像素安排黑、白或 HOLD（不驱动）三种状态，用一帧短波形只推动确实需要变化的像素。两路各 5,000 字节的图像平面以 20 MHz SPI 传输，显示电源也不用每次重新启动，省掉重复上电的时间。它借鉴了 Wenting Zhang 的 PaperBoy，但仍通过开发板现成的 SSD1681 控制器工作。

这儿有个容易误会的数字：**Game Boy 模拟器约以 59.7 fps 运行，电子纸端每 33.3 ms 取一次最新画面，约合 30 次更新/秒**。画面忙时可能掉帧，而且像素需要多次短脉冲才能达到目标灰度，不能理解成每个像素都在 33 ms 内彻底稳定。

<iframe
  title="InkBoy — original Game Boy on e-paper demo at 30 FPS"
  src="https://www.youtube-nocookie.com/embed/XiZmM6hwwAU"
  loading="lazy"
  referrerpolicy="strict-origin-when-cross-origin"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowfullscreen
  style="display:block;width:100%;max-width:900px;aspect-ratio:16/9;border:0;border-radius:8px;"
></iframe>

*作者原始演示视频：[GameBoy on E-Paper ESP32 at 30FPS](https://www.youtube.com/watch?v=XiZmM6hwwAU)。如果网页内无法播放，可点击链接在 YouTube 观看。*

黑白模式用固定抖动图案模拟 Game Boy 的四档灰度；另一种快速灰阶模式则让电子纸粒子只移动到中间位置，直接形成黑、深灰、浅灰、白四种色阶。后者要分别校准不同灰阶间的脉冲次数，残影也更难压住。

硬件基于 **Waveshare ESP32-S3-ePaper-1.54 V2**，板载 microSD 和扬声器；操控用另一个 ESP32-C3 制作的专用手柄，可走 BLE 或 USB-C。**普通蓝牙手柄暂不兼容**。固件支持传统 Game Boy（DMG）游戏和部分可在 DMG 模式运行的卡带，不是 Game Boy Color 通吃；ROM 需要用户自行合法准备。

高速刷新还有代价。作者明确警告：自定义波形可能造成永久残影或损坏面板，长期寿命没有验证。它展示的是电子纸驱动还能怎么玩，不是所有电子纸都能安全跑到 30 FPS。

**项目资料：** [InkBoy GitHub 源码](https://github.com/kuslota/InkBoy) · [逐像素驱动说明](https://github.com/kuslota/InkBoy/blob/main/docs/how-it-works.md) · [Hackaday 原报道](https://hackaday.com/2026/10/14/tiny-e-paper-display-delivers-30-fps-of-game-boy-fun/)。

<!-- embeddednote-p0-20261106:start -->

## 工程补充：每秒更新 30 次，不等于面板寿命也能按 30 FPS 设计

200×200 的单色 1 bpp 位平面是 **5,000 B**，两路各一帧总共 **10,000 B**。假定 SPI 持续运行在理想 20 MHz，纯时钟传出这 10 KB 约需 **4.0 ms**；30 次/秒的更新间隔则是 **33.3 ms**。从带宽角度看并不矛盾，但这**不能解释全部驱动时序，更不能证明长期使用安全**。命令开销、供电和粒子运动都不包含在 4.0 ms 之内。

还要分清“控制器每秒接受 30 次更新指令”与“像 LCD 一样每帧完全达到稳定对比度”。快速动画可能靠短脉冲反复推动像素，静态残影、灰阶一致性和长期可靠性需要另行评估。

如果准备复现，至少记录 SSD1681 板卡版本、固件提交号、自定义波形、环境温度、前后画面内容与供电波形，并在实验后用厂家允许的完整刷新检测残影。项目的 [逐像素驱动说明](https://github.com/kuslota/InkBoy/blob/main/docs/how-it-works.md) 有相关实验方法，但不能替代生产可靠性验证。**不建议把这种未经寿命确认的高速波形直接用于量产面板。**

相关：[SPI 与电子纸刷新时序](/zh/articles/epaper-refresh-timing-pipeline/)。
<!-- embeddednote-p0-20261106:end -->
