# EmbeddedNote.com 正式主站迁移实施手册

> 版本 0.1，2026-10-14。根据用户截图制作，不能替代对旧站的完整抓取与导出。现有 ChatGPT Sites 在用户网络中可访问；外部抓取工具未能访问，不代表全球不可访问。

## 一、迁移目标

- 保持现有品牌：EmbeddedNote / 嵌入式杂谈，米白底、深墨绿字、砖红点缀、衬线大标题。
- 保留旧站五大栏目（Embedded Systems、Chips & Semiconductors、Engineering Practice、Industry Insight、Projects & Open Source）原有内容对应关系，未来频道采用六大技术类目。
- 新站六大技术频道：开源项目、MCU & SoC、硬件设计、通信技术、显示技术、开发工具。
- 保留独立的 `/en/`、`/zh/` 内容路线作为下一阶段任务。本演示工程当前使用中文首页 `/`，**尚未实现完整双语内容路由与翻译**。正式切换前必须补齐或兼容旧 `/en/` URL。
- 使用 Astro 静态构建、Cloudflare Pages、GitHub、Pagefind、Giscus。

## 二、准备材料（务必切换 DNS 之前）

1. 导出 ChatGPT Sites 所有文章、静态页面、原始图片及文章日期；若无法导出，逐篇人工保存内容并复核授权。
2. 抓取现有 URL 清单、title、description、canonical、hreflang、sitemap、robots 和导航；尤其保留 `/en/` 路径。
3. 记录目前域名的 DNS 类型、主机名及目标值、TTL、当前归属平台；保留截图与导出以便回滚。
4. 清点知识产权：原创图片、GitHub 项目引用、开源许可、产品图和转载授权。
5. 设定标准 URL，例如 `/zh/articles/<slug>/`、`/en/articles/<slug>/`；若已有收录 URL，优先保持原路径。

## 三、本地启动

安装 Git、Node.js（满足 Astro 当前版本要求）。下载 ZIP 解压后：

```bash
cd embeddednote-astro-starter
npm install
npm run dev
```

浏览器打开终端提示的 localhost 地址预览。构建测试：

```bash
npm run build
npm run preview
```

Pagefind 是构建后的搜索索引，在 `npm run dev` 下不保证正常工作。代码保存在 Git 仓库后，每次 Git push 可以触发 Pages 重建。

## 四、发布到 GitHub

1. 建立一个 GitHub 仓库，例如 `embeddednote-website`（若希望 Giscus 评论关联同一仓库，该仓库需是 public）。
2. 在代码目录执行：

```bash
git init
git add .
git commit -m "Initialize EmbeddedNote Astro website"
git branch -M main
git remote add origin https://github.com/<YOUR_USER>/embeddednote-website.git
git push -u origin main
```

不要把 `.env` 或任何 API 密钥提交到 Git。

## 五、Cloudflare Pages 部署

1. 登录 Cloudflare，进入 Workers & Pages → Create application → Pages → Import an existing Git repository。
2. 授权 GitHub 并选择刚创建的仓库。
3. Framework preset 选择 Astro；Production branch `main`；Build command `npm run build`；Output directory `dist`；Root directory 留空。
4. 保存并部署，获得临时 `*.pages.dev` 地址。
5. 先在该临时域名检查首页、6 类目、文章、搜索、RSS、`sitemap-index.xml`、robots 和移动端。
6. **本项目是纯静态 Astro，Cloudflare Pages 不需要 SSR adapter。**

## 六、Giscus 评论配置

1. 选一个公开 GitHub 仓库，开启 Discussions。
2. 根据 https://giscus.app 提示安装 GitHub App，配置可写 Discussions 分类。
3. 读取 `repo`、`repoId`、`categoryId`。
4. 在 Cloudflare Pages → Settings → Variables and Secrets 配置：`PUBLIC_GISCUS_REPO`、`PUBLIC_GISCUS_REPO_ID`、`PUBLIC_GISCUS_CATEGORY_ID`。
5. 重新部署并验证评论读写；GitHub 授权对部分中国大陆读者可能存在门槛。

## 七、迁移 SEO 与 URL

制作 `old_url,new_url,action,status` 四列表。能沿用旧 URL 尽量不改；确需更改，添加 301 规则到 `public/_redirects`，验证源 URL 到目标只跳一次且返回 200。**不要仅将 `/en/` 重定向到纯中文首页**，应先补齐英文页。

不要发布全是 AI 翻译、缺乏技术审校的文章。多语版本要有独立 canonical 与 hreflang。检查 RSS、Sitemap、404、Open Graph 以及 Google Search Console / Bing Webmaster Tools。

## 八、域名切换与回滚

1. 不在 ChatGPT Sites 上直接解绑域名；先取得完整 DNS 记录备份。
2. Pages 项目 Custom domains 添加 `embeddednote.com` 与 `www.embeddednote.com`（如需）。
3. 根据 Cloudflare 控制台提示完成域名验证 / DNS 修改，具体记录取决于域名当前使用的 DNS 和接入方式，**不要自行猜记录值**。
4. 确认 HTTPS 证书、301/308、双语页面、Giscus 与 Pagefind 都正常之后再正式切换流量。
5. 若关键故障，按事先记录的 DNS 和旧平台设置回滚；注意 DNS 缓存和证书签发可能造成恢复延迟。

## 九、正式发布验收矩阵

| 检查项 | 通过标准 |
|---|---|
| 当前旧站内容 | 全部登记，有导出或有效备份 |
| 旧 URL | 已收录链接 100% 保留或正确 301 |
| 中英文 | `/en/` 正常，`/zh/` 正常，hreflang 互链 |
| 六大频道 | 导航、分类页和文章归类正确 |
| 技术文章 | 代码块、原理图、PDF 在桌面/手机显示正常 |
| Pagefind | 中文关键词、芯片型号检索正常 |
| Giscus | 登录、评论、回复及移动端正常 |
| SEO | sitemap、canonical、robots、元数据通过检查 |
| 安全 | Git 密钥未泄露、HTTPS 正常 |
| 回滚 | DNS 备份与执行流程已验证 |

## 十、当前工程范围与限制

本包是**可部署架构初版，不是旧站完整迁移成品**。已有中文六频道及示例文章；双语、旧站文章导入、逐篇 301、图文素材、图片 CDN、图像优化、完整 SEO 监测需按旧站清单后续完善。此环境未能完成 npm 安装，因此本包**尚未通过实际构建验证**。
