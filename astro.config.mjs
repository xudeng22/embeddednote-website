import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
export default defineConfig({site:'https://embeddednote.com',output:'static',integrations:[sitemap()],trailingSlash:'always'});
