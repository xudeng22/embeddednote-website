
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import embeddednoteImages from './scripts/rehype-embeddednote-images.mjs';

export default defineConfig({
  site: 'https://embeddednote.com',
  output: 'static',
  trailingSlash: 'always',

  integrations: [sitemap()],
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
