
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const root = 'dist';
const languages = ['en', 'zh'];

const categories = [
  'open-source',
  'mcu-soc',
  'hardware',
  'connectivity',
  'display',
  'tools'
];

let failures = 0;
let checks = 0;

function check(condition, description) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} ${description}`);

  if (!condition) failures++;
}

function fileExists(path) {
  return existsSync(join(root, path));
}

function readFile(path) {
  return readFileSync(join(root, path), 'utf8');
}

// 1. 基础资源
const baseFiles = [
  'index.html',
  'rss.xml',
  'robots.txt',
  'sitemap-index.xml',
  '_redirects',
  'pagefind/pagefind.js',
  'pagefind/pagefind-ui.js',
  'pagefind/pagefind-ui.css'
];

for (const file of baseFiles) {
  check(fileExists(file), `Base file: ${file}`);
}

// 2. 中英文首页、关于、文章和分类
for (const lang of languages) {
  const paths = [
    `${lang}/index.html`,
    `${lang}/about/index.html`,
    `${lang}/articles/embeddednote-launch/index.html`,
    ...categories.map(
      category => `${lang}/category/${category}/index.html`
    )
  ];

  for (const path of paths) {
    check(fileExists(path), `Route: ${path}`);
  }
}

// 3. 检查首页语言和 SEO
for (const lang of languages) {
  const path = `${lang}/index.html`;

  if (!fileExists(path)) continue;

  const html = readFile(path);
  const expectedLang = lang === 'zh' ? 'zh-CN' : 'en';



  check(
    new RegExp(`<html[^>]*lang=["']${expectedLang}["']`, 'i')
      .test(html),
    `${lang} homepage language`
  );

  check(
    html.includes('rel="canonical"'),
    `${lang} homepage canonical`
  );

  check(
    html.includes(`/${lang}/category/display/`),
    `${lang} display category link`
  );

  check(
    html.includes(`/${lang}/category/connectivity/`),
    `${lang} connectivity category link`
  );
}

 // 4. 双语文章和独立 SEO
for (const lang of languages) {
  const path =
    `${lang}/articles/embeddednote-launch/index.html`;

  if (!fileExists(path)) continue;

  const html = readFile(path);
  const otherLang = lang === 'en' ? 'zh' : 'en';

  const alternateLinks =
    html.match(/<link\b[^>]*hreflang=[^>]*>/gi) ?? [];

  console.log(
    `DEBUG ${lang} article alternate links:`,
    alternateLinks
  );

  check(
    html.includes('rel="canonical"') &&
    html.includes(`/${lang}/articles/embeddednote-launch/`),
    `${lang} article canonical`
  );

  check(
    html.includes('hreflang=') &&
    html.includes(`/${otherLang}/articles/embeddednote-launch/`),
    `${lang} article translation reference`
  );
}


// 5. RSS
if (fileExists('rss.xml')) {
  const rss = readFile('rss.xml');

  check(
    rss.includes('/en/articles/embeddednote-launch/'),
    'English article in RSS'
  );

  check(
    rss.includes('/zh/articles/embeddednote-launch/'),
    'Chinese article in RSS'
  );
}

// 6. Cloudflare 根路径重定向
if (fileExists('_redirects')) {
  const redirects = readFile('_redirects');

  check(
    /^\/\s+\/en\/\s+302\s*$/m.test(redirects),
    'Default language redirects to /en/'
  );
}

// 7. 总结
console.log(`\nTotal checks: ${checks}`);
console.log(`Passed: ${checks - failures}`);
console.log(`Failed: ${failures}`);

if (failures > 0) {
  console.error('V2.1 build validation failed.');
  process.exitCode = 1;
} else {
  console.log('V2.1 bilingual site validation passed.');
}
