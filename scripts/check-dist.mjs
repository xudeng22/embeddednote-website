import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const root = 'dist';
const languages = ['en', 'zh'];
const categories = ['open-source', 'mcu-soc', 'hardware', 'connectivity', 'display', 'tools'];
let failures = 0;
let checks = 0;

function check(condition, label) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} ${label}`);
  if (!condition) failures++;
}
function has(path) { return existsSync(join(root, path)); }
function read(path) { return readFileSync(join(root, path), 'utf8'); }

for (const file of ['index.html', 'rss.xml', 'robots.txt', 'sitemap-index.xml',
  '_redirects', 'pagefind/pagefind.js', 'pagefind/pagefind-ui.js', 'pagefind/pagefind-ui.css']) {
  check(has(file), `Base file: ${file}`);
}

for (const lang of languages) {
  const home = `${lang}/index.html`;
  const about = `${lang}/about/index.html`;
  const oldWelcome = `${lang}/articles/embeddednote-launch/index.html`;
  for (const path of [home, about, ...categories.map(c => `${lang}/category/${c}/index.html`)]) {
    check(has(path), `Route: ${path}`);
  }
  check(!has(oldWelcome), `Old welcome article removed: ${lang}`);
  if (has(home)) {
    const html = read(home);
    check(new RegExp(`<html[^>]*lang=["']${lang === 'zh' ? 'zh-CN' : 'en'}["']`, 'i').test(html), `${lang} homepage language`);
    check(html.includes('rel="canonical"'), `${lang} homepage canonical`);
    check(!html.includes(`/articles/embeddednote-launch/`), `${lang} homepage without welcome article`);
    for (const c of ['display', 'connectivity']) {
      check(html.includes(`/${lang}/category/${c}/`), `${lang} homepage category ${c}`);
    }
  }
  if (has(about)) {
    const html = read(about);
    const other = lang === 'en' ? 'zh' : 'en';
    check(html.includes('rel="canonical"') && html.includes(`/${lang}/about/`), `${lang} about canonical`);
    check(html.includes('hreflang=') && html.includes(`/${other}/about/`), `${lang} about alternate`);
    check(html.includes('data-pagefind-body'), `${lang} about indexed content`);
  }
  const articleDir = join(root, lang, 'articles');
  check(existsSync(articleDir) && readdirSync(articleDir, {withFileTypes: true}).some(e => e.isDirectory()),
    `${lang} technical articles remain`);
}

if (has('rss.xml')) {
  check(!read('rss.xml').includes('/articles/embeddednote-launch/'), 'Welcome article removed from RSS');
}
if (has('_redirects')) {
  const rules = read('_redirects');
  check(/^\/\s+\/en\/\s+302\s*$/m.test(rules), 'Root default language redirect');
  for (const [source, target] of [
    ['/en/articles/embeddednote-launch/', '/en/about/'],
    ['/zh/articles/embeddednote-launch/', '/zh/about/'],
    ['/articles/embeddednote-launch/', '/zh/about/']
  ]) {
    check(rules.split(/\r?\n/).some(line => line.trim() === `${source} ${target} 301`), `301: ${source}`);
  }
}

console.log(`\nTotal checks: ${checks}; Passed: ${checks - failures}; Failed: ${failures}`);
if (failures) process.exitCode = 1;
