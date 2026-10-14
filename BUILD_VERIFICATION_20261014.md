# EmbeddedNote 工程验证记录（2026-10-14）

## 环境
- Node.js v22.16.0 / npm 10.9.2
- 静态 Astro 工程，构建命令 `npm run build`（Astro + Pagefind）

## 已执行及结果
1. `curl -I https://registry.npmjs.org/astro` → `Could not resolve host: registry.npmjs.org`。
2. `npm install --offline --ignore-scripts --no-audit --no-fund` → `ENOTCACHED`，缺少 `@astrojs/sitemap` 缓存。
3. 搜索本地 Astro/Pagefind 的预安装依赖 → 未找到。
4. `python scripts/check-source.py` → 21 项 PASS、0 项 FAIL（文件存在性、配置、分类、文章 frontmatter、布局结构）。
5. **未执行成功** `npm run build`；未验证生成的 HTML、Pagefind 索引与 Giscus 实际加载。

## 云端真实构建验证（新增）
仓库包含 `.github/workflows/verify.yml`：推送到 GitHub 的 `main` 分支或发起 PR 后，在可访问 npm registry 的 GitHub-hosted runner 上：
1. Node 22 环境，运行 `npm install --no-audit --no-fund`；
2. 运行 `npm run build`；
3. 运行 `node scripts/check-dist.mjs`：检查首页、6 分类、演示文章、RSS、robots、sitemap、Pagefind 资源及关键元信息；
4. 上传 `dist/` 作为 Actions artifact 供检查。

GitHub Actions 成功前，不应认定项目“构建通过”。首次联网安装后可提交生成的 `package-lock.json` 并将工作流改为 `npm ci` 以确保可重复构建。即使 CI 通过，也仍需在 Pages 预览域测试搜索交互、评论授权、样式与移动端效果，并对正式域名迁移作单独验收。

## 手动执行
```bash
python scripts/check-source.py
npm install --no-audit --no-fund
npm run build
node scripts/check-dist.mjs
npm run preview
```
