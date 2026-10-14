# EmbeddedNote Astro Static Blog

Six-channel Chinese engineering blog starter for **https://embeddednote.com**.

## Local setup

Requires Node.js 20.19+ or 22.12+ (check the Node compatibility of the installed Astro major version).

```bash
npm install
npm run dev
npm run build
npm run preview
```

Pagefind works after `npm run build`, not necessarily in `npm run dev`.

## Cloudflare Pages Git build

- Framework: Astro
- Build command: `npm run build`
- Output directory: `dist`
- Production branch: `main`
- Root directory: repository root

This is **static output**; do **not** install `@astrojs/cloudflare` for Pages. Current Astro Cloudflare adapter is primarily for Workers SSR.

## Giscus

1. Enable GitHub Discussions on a public repository; install the Giscus app and configure https://giscus.app.
2. Copy `.env.example` to `.env`; populate `PUBLIC_GISCUS_*` values.
3. Set the same variables in Cloudflare Pages project settings and redeploy.
4. Confirm third-party scripts load in Chinese mainland browsing conditions.

## Articles

Add Markdown files to `src/content/articles/` with typed frontmatter, category one of `open-source`, `mcu-soc`, `hardware`, `connectivity`, `display`, `tools`.

## Before DNS cutover

Export existing ChatGPT Sites content, create old URL map, check canonical links, test pages.dev preview, confirm search/Giscus and rollback path. **Do not switch the domain before acceptance.**

The deployed site is not changed by this ZIP. User must link their GitHub and Cloudflare accounts.

## Build validation status (2026-10-14)

Source-level checks succeeded; npm registry DNS was unavailable in the validation container, so dependency install and Astro build could **not** be completed here. See `BUILD_VERIFICATION_20261014.md` for precise command results. CI workflow `.github/workflows/verify.yml` performs actual installation, build and generated-site smoke tests when uploaded to GitHub; a green workflow is required before deployment.
