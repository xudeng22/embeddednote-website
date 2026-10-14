import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import assert from 'node:assert/strict';
const root = 'dist';
const expected = [
  'index.html','about/index.html','rss.xml','robots.txt','sitemap-index.xml',
  'pagefind/pagefind.js','pagefind/pagefind-ui.js','pagefind/pagefind-ui.css',
  ...['open-source','mcu-soc','hardware','connectivity','display','tools'].map(x=>`category/${x}/index.html`),
  'articles/embeddednote-launch/index.html',
];
let failures=0;
for (const p of expected) {
  const ok=existsSync(join(root,p));
  console.log(`${ok?'PASS':'FAIL'} ${p}`);
  if(!ok) failures++;
}
if (existsSync(join(root,'index.html'))) {
  const home=readFileSync(join(root,'index.html'),'utf8');
  for (const pattern of ['rel="canonical"','/pagefind/pagefind-ui.js','/category/display/','/category/connectivity/']) {
    const ok=home.includes(pattern);
    console.log(`${ok?'PASS':'FAIL'} homepage includes ${pattern}`);
    if(!ok) failures++;
  }
}
if (existsSync(join(root,'rss.xml'))) {
  const rss=readFileSync(join(root,'rss.xml'),'utf8');
  const ok=rss.includes('<rss')&&rss.includes('embeddednote-launch');
  console.log(`${ok?'PASS':'FAIL'} RSS feed contains article`);
  if(!ok) failures++;
}
if(failures){console.error(`Build artifact validation failed (${failures} checks).`);process.exitCode=1;}
else console.log('All generated-site smoke tests passed.');
