---
title: "树莓派 5 16GB 涨到 385 美元，CM5 也跟涨：内存成本压力还没过去"
description: "2026 年 11 月 2 日，树莓派将 16GB Raspberry Pi 5 上调 80 美元至 385 美元，16GB Compute Module 5 上调 40 美元，Pi 500+ 维持原价。回看历次涨价与嵌入式选型影响。"
locale: zh
translationKey: raspberry-pi-16gb-price-rise-2026
pubDate: 2026-11-02
category: mcu-soc
tags:
  - Raspberry Pi
  - Raspberry Pi 5
  - Compute Module 5
  - LPDDR4X
  - 存储器
  - 单板计算机
draft: false
author: EmbeddedNote
sourceUrl: https://www.raspberrypi.com/news/price-rises-for-some-16gb-raspberry-pi-products/
seoTitle: "树莓派 5 16GB 再涨 80 美元至 385 美元，CM5 同步涨价"
seoDescription: "树莓派 2026 年 11 月 2 日调价：Pi 5 16GB 售价 385 美元，CM5 16GB 涨 40 美元，500+ 不变。附 2025—2026 官方价格变化记录及项目选型分析。"
---

2025 年 1 月，16GB 的 Raspberry Pi 5 刚上市时卖 120 美元。到了 2026 年 11 月 2 日，同一档内存配置的官方标价已经来到 **385 美元**。不到两年涨了 265 美元，价格超过首发时的三倍。对曾经习惯用几十美元买块树莓派折腾项目的人来说，这个数字确实有些陌生。

这次不是整个产品线一起涨。树莓派创始人 Eben Upton 在[官方公告](https://www.raspberrypi.com/news/price-rises-for-some-16gb-raspberry-pi-products/)中确认：**Raspberry Pi 5 16GB 加价 80 美元，调整前是 305 美元；Compute Module 5 的所有 16GB 版本加价 40 美元；同样配有 16GB 内存的 Raspberry Pi 500+ 暂不调价。** 新价格从 11 月 2 日起执行。这里说的是官方美元标价，实际购买还会受地区、税费和经销商供货情况影响。

![Raspberry Pi 5 16GB 从 2025 年上市到 2026 年 11 月的官方价格变化图](/uploads/raspberry-pi-16gb-price-rise-2026/raspberry-pi-16gb-price-cover.webp)

*EmbeddedNote 根据树莓派历次官方公告绘制，单位为美元；并非产品实拍。*

## 16GB 版本是怎么涨到 385 美元的？

单看这次的 80 美元，已经相当于一块过去的入门级开发板。但把此前几轮调价连起来，变化更明显。

| 时间 | Raspberry Pi 5 16GB 官方标价 | 当次变化 |
| --- | ---: | ---: |
| 2025 年 1 月上市 | $120 | 首发价 |
| 2025 年 12 月 | $145 | +$25 |
| 2026 年 2 月 | $205 | +$60 |
| 2026 年 4 月 | $305 | +$100 |
| **2026 年 11 月 2 日** | **$385** | **+$80** |

2025 年末开始，树莓派反复提到 LPDDR4/LPDDR4X 内存采购成本上涨；今年 2 月和 4 月的公告，则把更高密度内存受到的冲击写得更具体。10 月 1 日，树莓派才刚将部分 2GB 版本上调 12.50 美元；一个月后，压力又落到了 16GB 型号上。这些是不同时间、不同容量的调价，不能理解成 11 月又给所有 Raspberry Pi 5 加价 80 美元。

这轮公告中值得注意的不是一句笼统的“内存涨价”，而是**16GB DRAM 缺少可替代的供货来源**。厂家表示，虽然已经在验证替代元件，以增加采购灵活性，但高容量存储器的供应选择有限，再叠加其他器件短缺，只能继续调整部分高密度产品的售价。树莓派并未公布具体的 DRAM 采购合同、单颗成本或 16GB 板卡毛利变化，因此不能直接将 265 美元的累计零售价涨幅全部归因于某一颗内存芯片。

## 对做产品的人，CM5 涨价更值得算账

相比零售版 Raspberry Pi 5，Compute Module 5 经常被嵌入定制底板、控制终端和工业设备。它有不同的 eMMC、无线及内存组合，**此次上调的是其中的 16GB 配置**；每个 SKU 的最终标价需要以[官方 CM5 产品页及最新 Product Brief](https://www.raspberrypi.com/products/compute-module-5/)为准，不能把“涨 40 美元”误写成“所有 CM5 都涨 40 美元”。

对正在设计量产设备的团队，单台多出 40 美元，在几十台样机阶段也许还能消化，到了数千台就会变成实实在在的 BOM 压力。但另一方面，如果应用需要多个容器、较大的数据库缓存、复杂图形界面或本地模型推理，盲目换成 4GB/8GB 也可能带来交换分区频繁读写、响应延迟和长期稳定性问题。比较靠谱的做法是先在目标系统上记录常态内存占用、峰值和可接受的余量，再决定是否真的需要 16GB。对需要长期供货的设备，还应该提前确认模块型号、交期和替代方案。

树莓派没有给出何时恢复原价的承诺，只表示如果存储器成本回落，希望能逐步撤销这些加价。官方也提醒消费者通过[授权经销商](https://www.raspberrypi.com/resellers/)购买，避免被借供应紧张炒高价格的卖家误导。

对个人开发者来说，低内存版本或老型号仍可能够用；对已经基于 CM5 16GB 定型的产品，真正需要重新打开的恐怕是 BOM 表，而不是原理图。

**资料来源：** [2026-11-02 官方调价公告](https://www.raspberrypi.com/news/price-rises-for-some-16gb-raspberry-pi-products/) · [2025-12 调价记录](https://www.raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/) · [2026-02 调价记录](https://www.raspberrypi.com/news/more-memory-driven-price-rises/) · [2026-04 调价记录](https://www.raspberrypi.com/news/a-new-3gb-raspberry-pi-4-for-83-75-and-more-memory-driven-price-increases/) · [2026-10 调价记录](https://www.raspberrypi.com/news/price-increases-for-2gb-raspberry-pi-4-and-raspberry-pi-5/)
