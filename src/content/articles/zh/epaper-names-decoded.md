---
title: '电子纸命名对照:E6、1680、8151 到底是什么'
description: '一块电子纸模组上有三套名字:E Ink 的品牌名、控制器型号、模组厂料号。本文给出对照表和两分钟自查方法,让你搜到对的关键词。'
locale: zh
translationKey: epaper-names-decoded
pubDate: '2026-11-11'
category: display
tags:
- 电子纸
- 显示驱动
- 参考资料
- 选型
draft: false
author: EmbeddedNote
contentType: deep
series: epaper
seoTitle: '电子纸命名对照:E6、SSD1680、UC8151'
seoDescription: 'E6 指 Spectra 6,1680 指 SSD1680,8151 指 UC8151。三套命名怎么对应,以及如何在两分钟内找到自己模组的真实型号。'
---

有人问"E6 7.3 寸屏",得到的回答却是 SSD1680 和一份 2.13 寸的数据手册。这里混了三套命名,而且没有一套等于你下单时的商品标题。

这篇就是对照表。写短一点:你需要的是两分钟内搜对关键词,不是一本目录。

## 三套命名

| 命名的对象 | 例子 | 你在哪见到它 |
| --- | --- | --- |
| E Ink 的品牌与技术 | Spectra 6、Gallery、Carta | 宣传页、面板数据手册封面 |
| 排线上的控制器 IC | SSD1680、UC8151 | 示例代码、驱动库、寄存器手册 |
| 模组厂料号 | GDEY075T7、2.13inch e-Paper HAT | 商品页、丝印、发票 |

一块模组同时具备这三套名字,而且它们互不推导。同样标"2.13 寸电子纸"的两块屏,控制器可能不同;同一个面板系列在后续版本里换了控制器,标题里的尺寸却不会变。

## 品牌名与简称

| 官方名 | 大家怎么写 | 是什么 |
| --- | --- | --- |
| E Ink [Spectra 6](https://cn.eink.com/brand/detail/Spectra6) | **E6** | 六色标牌面板,0–50 °C,最高 200 ppi |
| E Ink [Spectra 3100](https://cn.eink.com/brand/detail/Spectra3100) | BWRY、"四色" | 黑、白、红、黄 |
| E Ink [Gallery](https://cn.eink.com/brand/detail/Gallery) | **ACeP** | 较早的全彩电子纸技术 |
| E Ink [Kaleido](https://cn.eink.com/brand) | — | Carta 背板加彩色滤光片,阅读器那种彩色 |
| E Ink [Carta](https://cn.eink.com/brand) | — | 黑白基线 |
| E Ink [Marquee](https://cn.eink.com/brand/detail/marquee) | — | 四粒子彩色,−20 至 65 °C,翻转 5–7 秒 |

最容易搞错的是 `E6`:它长得像控制器型号,但它不是。找六色屏时,"Spectra 6" 和 "E6" 都要搜——卖家标题用简称,数据手册用全称。

## 代码里那些控制器编号

示例工程的文件夹是按控制器命名的,不是按面板命名的,所以文件名里那个数字才是你真正的搜索关键词:

| 你看到的 | 完整型号 | 说明 |
| --- | --- | --- |
| `1680` | SSD1680 | 小尺寸黑白模组上非常常见 |
| `8151` | UC8151(及 UC8151D) | 同尺寸段常见的另一个选择 |
| `1675` | SSD1675 | 1680 的前一代 |
| `0373` | IL0373 | 较早的三色方案 |
| `3897` | IL3897 | 老工程里会遇到的另一颗 |

搜短号,能找到寄存器级的答案;搜"2.13 寸电子纸",找到的是店铺。如果你在调初始化序列,你要的是前者。

## 两分钟找到自己那块

1. **看排线丝印。** 多数模组会把控制器或料号印在 FPC 上。字很小,但它是最快的事实来源。
2. **看示例工程文件夹名。** 如果厂家给的是 `epd2in13_V3`,那个版本号比尺寸更重要:同一尺寸的 V2 和 V3 经常用不同的控制器。
3. **翻数据手册第一页。** 控制器写在特性表里,不在标题里。
4. **看商品页的规格表**,不是宣传文案。

这四处对不上时,以排线丝印为准。

## 为什么这个错配会出事

下面每一条都是真实的支持请求:

- 按 1680 寄存器表写的驱动,初始化不了 8151 的屏,哪怕分辨率完全一样。
- 两块都叫"2.13 寸"的模组,分辨率可能不同:现在常见的是 250 × 122,老款是 212 × 104。字节数不同,按其中一种开缓冲区,另一种就会越界。
- 六色屏不是"八色屏少了两个颜色"。色板和原生色码来自面板,不来自颜色数量。

这些在商品标题里都看不出来,这张对照表存在的全部理由就是这个。

## 这篇不做什么

我们**不发布"控制器 ↔ 面板"的对照表**。那份表每换一次硬件版本就失效,而过期的条目比没有条目更糟。稳定的是命名逻辑和上面的两分钟流程。

想了解缓冲区格式搞错之后会发生什么,看[照片为什么会显示错](/zh/articles/why-your-epaper-photo-looks-wrong/)和 [RAW4 编码指南](/zh/articles/epaper-palette-raw4-packing-guide/)。要按特定色板转图,[图像转换器](/zh/tools/epaper-image-converter/)支持导入设备配置。

## 参考来源

- E Ink 品牌页:[Spectra 6](https://cn.eink.com/brand/detail/Spectra6)、[Spectra 3100](https://cn.eink.com/brand/detail/Spectra3100)、[Gallery](https://cn.eink.com/brand/detail/Gallery)、[Marquee](https://cn.eink.com/brand/detail/marquee)——品牌名、温区与 Spectra 6 的分辨率上限。
- 微雪 [2.13 寸 e-Paper HAT](https://www.waveshare.com/2.13inch-e-paper-hat.htm) 商品页——现款为 250 × 122,这也是表里把 212 × 104 标为老款的原因。
- 控制器型号取自各厂家示例工程目录名;最终以随屏数据手册为准。
