# 2026-11-11 变更记录(中文版)

> 英文原文见 `CHANGELOG_2026-11-11.md`。本文件覆盖当天两轮改动:上午的图片/搜索呈现/内容核对,以及晚上的电子纸系列、BLE 模型文章和一次模型修正。

## 第一轮(上午)

### 1. 图片与页面重量

| 改动 | 细节 |
| --- | --- |
| 大图转码 | 53 个 >45 KB 的 PNG/JPEG 转 WebP(q86)。例:`image-22.png` 1,082→632 KB,`tiwaz-10.png` 536→278 KB |
| 动图 | 4 个 GIF 转动图 WebP:`flip-card` 7,104→1,351 KB,`tinytron` 8,079→2,421 KB |
| 响应式 | 118 个 `-640.webp` 变体,rehype 插件输出 `srcset` + `sizes` |
| Logo | 187 KB / 1628×253 换成 480w(14 KB)+ 960w(32 KB) |
| 外链图 | 17 张原本直连 lceda / m5stack / espressif / raw.githubusercontent 的图落地到本地 |
| 清理 | 79 个被替代的原图删除;`public/` 56 MB → 37 MB |

### 2. 搜索呈现

- 50 张独立 OG 卡片(1200×630),`Base.astro` 接收 `image` 属性
- 标题后缀仅在总宽度 ≤62 单位时追加;CJK 字符按 2 单位计
- `TechArticle` 补 `image`/`thumbnailUrl`/`url`/`articleSection`/`keywords`/`isPartOf`
- 新增可见面包屑 + `BreadcrumbList`;`WebSite` 加 `SearchAction`
- 分页页 `noindex,follow`;sitemap 加 hreflang,排除分页

### 3. 内链

新增 `ArticleFooterNav`:本系列 / 相关阅读 / 配套工具三块,每篇文章底部都有。

### 4. 六篇文章的一手化核对

| 文章 | 核对重点 | 纠错 |
| --- | --- | --- |
| Apollo H-3 | 对照 `Integrations/ESPHome/Core.yaml`(版本 26.11.5.1) | 2026 年收益捐给 St. Jude,不是往年那两家机构 |
| MOTO GPS | README、LICENSE、审阅包 | 许可证是 PolyForm Noncommercial 1.0.0,**不是开源**;标签改为 Source Available |
| ArbWave30 | README 与文档 | 补充"作者 2026-12-25 恢复更新",规格属于 MVP 目标 |
| 电容闹钟 | README | 补充浪涌算术:12 V / 10 Ω 每槽约 1.2 A,三槽同时约 3.6 A |
| Jumper | README、硬件文档 | RK3576 无法确认,标注"未核实" |
| M5Stack PaperDIY | 官方原理图 | 4 页原理图落地本地 |

### 5. AdSense

保留原脚本(`ca-pub-9169011296822300`,async),只把它从 `<head>` 第一个标签移到 `</body>` 前。Google 两种位置都支持,自动广告不受影响。

## 第二轮(晚上)

### 6. 转换器页面改造成搜索落地页

`/en/tools/epaper-image-converter/` 从"只有一个工具"变成有正文的页面:色板表(参考预设 vs 实测设备配置)、导出表(含 RAW4 打包约定)、常见面板尺寸表、四步用法、五条限制、七条 FAQ,以及 `FAQPage` + `WebApplication` 结构化数据。

核对尺寸时发现 **2.13 寸写错了**:现款是 250×122,不是 212×104。现在两行并列,旧的标为 legacy。

### 7. 五篇新文章(中英各一版)

| 文章 | 作用 |
| --- | --- |
| 电子纸命名对照 | E6 = Spectra 6、1680 = SSD1680、8151 = UC8151,以及如何在两分钟内找到自己的型号 |
| 照片为什么会显示错 | 五层错误模型 + 症状表 + 六条按排查成本排序的原因 |
| 电子纸残影 | 物理机理、温度与波形、计数器式策略 |
| 局刷什么时候安全 | 三道门槛、内容适用表、接缝、十次循环验证 |
| BLE 吞吐模型 | 规划器的完整算术 + 240 KB 算例 |

`E6` 一度被我当成"查无此型号"删掉,之后恢复:Spectra 6 就是圈内说的 E6,现在统一写成"官方名 + 简称"。

### 8. 纯文字文章的社交卡片

没有配图的文章,`og:image` 和列表缩略图都在用站点通用 PCB 图。现在改成专用 1200×630 卡片,`ArticleFeed` 的回退也从 `/images/embeddednote-hero.webp` 改成 `/og/<translationKey>.webp`。

### 9. 模型修正:MIC 算在 251 字节上限之内

整理规划器算术时发现,逐包记账和 Bluetooth Core 规范不一致。

**错在哪。** 规划器把 4 字节 MIC 当作链路层载荷之后的附加字段,数据可用满 251 字节。规范里 MIC 计在 LL Data PDU 长度**之内**,加密链路上每个 PDU 的数据容量只有 247 字节。

**后果。** MTU 247 时,4(L2CAP)+ 3(ATT)+ 244(值)= 251,正好顶到上限;加 4 字节 MIC 变成 255,必须拆成两个 PDU。旧模型当成一个,空口时间少算约 30%。

**改动。**

```js
// 修改前
const llDataCapacity = c.llPayload;              // 251
// 修改后
const llDataCapacity = Math.max(1, c.llPayload - mic);  // 247
```

**数字变化**(240 KB / MTU 247 / LE 2M / 30 ms 间隔 / 15 ms 事件 / 每事件 4 次写):

| | 修改前 | 修改后 |
| --- | ---: | ---: |
| 每 PDU 数据容量 | 251 B | 247 B |
| 每次写 + 确认空口时间 | 1,408 µs | 1,812 µs |
| 总空口时间 | 1.39 s | 1.78 s |
| 有效吞吐 | 1.39 Mbit/s | 1.08 Mbit/s |
| 30 ms 间隔下总时长 | 7.38 s | 7.38 s |

总时长不变,因为卡住的是"每事件 4 次写",不是射频。LE 1M 场景从 2,250 µs 变成 2,992 µs。

工具 UI 里那句"LL Payload 上限与 4 字节 MIC 是两个独立字段"中英文都写错了,已替换。

**影响面。** 加密链路的估算值比以前慢 20–30%;不加密的估算不受影响。

### 10. 中文版

本轮每篇文章都有 `zh` 版本,结构、数字、内链与英文版一致。有脚本逐对比较数字和标题数量,两边吻合。标题宽度按 CJK 字符 2 单位计算,中文标题不再被后缀顶出 SERP 宽度。

### 11. 验证

```
npm run build      # 147 页,无报错
```

构建产物里核对:文章图片有 `srcset`、每篇有独立 `og:image`、`BreadcrumbList` + `TechArticle` 齐全、系列/相关/工具块存在、五张新卡片返回 200。

## 下一轮待办

- 中文版配图仍是英文标注,电子纸系列值得做一套中文 SVG。
- 规划器数字变了,任何引用旧数字的截图或帖子都需要更新。
- 若干 alt 文本仍写着 "GIF"(动图转 WebP 之后没改)。
- 仍有 68–91 字符的 `seoTitle` 需要人工缩短。
