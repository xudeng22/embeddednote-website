---
title: 树莓派 2026 年上半年出货超 400 万台，开发板为什么越来越贵？
description: 树莓派上调 2026 年上半年利润预期，预计出货超过 400 万台；结合 Raspberry Pi 5 的产品配置与价格进行讨论。
locale: zh
translationKey: raspberry-pi-h1-2026-shipment-prices
pubDate: '2026-06-12'
category: hardware
tags:
- Raspberry Pi
- SBC
- Market
- Pricing
draft: false
seoTitle: 树莓派 2026 年上半年出货超 400 万台，开发板为什么越来越贵？
seoDescription: 树莓派上调 2026 年上半年利润预期，预计出货超过 400 万台；结合 Raspberry Pi 5 的产品配置与价格进行讨论。
updatedDate: '2026-11-06'
---

树莓派 2026 年 6 月 5 日发布的交易更新里，有两个值得关注的预测：截至 6 月 30 日的半年出货量**预计超过 400 万台**，调整后 EBITDA **预计至少 3800 万美元**。这里的关键词是“预计”——当时上半年尚未结束，不能把利润指引写成已经实现的业绩。[原始交易公告](https://www.lse.co.uk/rns/trading-update-tik9c69fr16wj1q.html)。

公告还提到销量增长、产品组合改善，以及此前采购的低密度 DRAM 库存对利润的支持。因此，不能简单把利润改善归因于“树莓派涨价”：存储器采购成本、客户结构、销量和产品组合也都在起作用。

![树莓派 2026 上半年交易更新配图](/uploads/raspberry-pi-h1-2026-shipment-prices/raspberry-pi-h1-2026-shipment-prices-01.webp)

## 后来公布的实际结果

**2026 年 11 月 6 日补充：** 公司在 9 月 24 日披露正式的上半年业绩，出货量为 **420 万台**，营收 **2.569 亿美元**，调整后 EBITDA **4030 万美元**。这些是后来披露的实际结果，和 6 月的预测不是同一类数据。调整后 EBITDA 也不等于净利润。[2026 年中期业绩公告](https://www.lse.co.uk/rns/RPI/interim-results-e9exgc54mbhey5h.html)。

| 指标 | 6 月交易更新中的预计值 | 9 月披露的上半年结果 |
|---|---:|---:|
| 出货量 | 超过 400 万台 | 420 万台 |
| 调整后 EBITDA | 至少 3800 万美元 | 4030 万美元 |
| 营收 | 此次简报未给出 | 2.569 亿美元 |

## 为什么谈开发板价格必须写日期

Raspberry Pi 5 采用 Broadcom BCM2712，四核 Cortex-A76，内存焊接在主板上，买错容量后不能像台式电脑那样直接换内存条。但在 DRAM 价格波动期间，“某款板子卖多少钱”本身也是一个有时效性的结论。

6 月报道提到的 16GB 版本 **305 美元**是当时文章引用的历史价格。到 **2026 年 11 月 2 日**，树莓派官方又将这个配置上调 **80 美元，至 385 美元**，原因是 16GB DRAM 供应紧张。[查看官方涨价公告](https://www.raspberrypi.com/news/price-rises-for-some-16gb-raspberry-pi-products/)。所以，不能把不同日期的报价并列成一张“当前售价表”。

![树莓派开发板与价格讨论配图](/uploads/raspberry-pi-h1-2026-shipment-prices/raspberry-pi-h1-2026-shipment-prices-02.webp)

对于要做产品的工程师，更务实的办法是先测应用真正需要多少 RAM：无界面的网关、带相机缓冲的边缘视觉设备、浏览器信息终端，负载差别很大。除了板子本身的价格，还要算存储、散热、电源、供货周期和后续软件维护。低价的替代 SBC 未必意味着更低的整机长期成本。

关于本轮 16GB 调价，我们另有一篇[2026 年 11 月价格更新文章](/zh/articles/raspberry-pi-16gb-price-rise-2026/)。这篇保留 6 月行情事件的背景，同时补上已经确认的业绩与价格信息。

<!-- editorial-v3-20261106 -->
