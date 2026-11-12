
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import embeddednoteImages from './scripts/rehype-embeddednote-images.mjs';

export default defineConfig({
  site: 'https://embeddednote.com',
  output: 'static',
  trailingSlash: 'always',

  integrations: [
    sitemap({
      // Emit <xhtml:link rel="alternate" hreflang> for the en/zh pairs.
      i18n: {
        defaultLocale: 'en',
        locales: { en: 'en', zh: 'zh-CN' }
      },
      // Paginated archive pages are noindex,follow; keep them out of the sitemap
      // so the crawl budget goes to articles and tools.
      // Category pages were collapsed into /e-paper/, /connectivity/ and /notes/
      // and now answer with a 301, so they should not be advertised either.
      filter: (page) =>
        !/\/page\/\d+\/?$/.test(page) && !/\/category\/[^/]+\//.test(page)
    })
  ],
  markdown: { rehypePlugins: [embeddednoteImages] },

  i18n: {
    locales: ['en', 'zh'],
    defaultLocale: 'en',
    routing: {
      prefixDefaultLocale: true,
      redirectToDefaultLocale: false
    }
  }
});
