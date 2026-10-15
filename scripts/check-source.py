from pathlib import Path
import json, re, sys
root=Path(__file__).resolve().parent.parent
errs=[]
def check(cond,name):
 print(('PASS' if cond else 'FAIL')+' '+name)
 if not cond: errs.append(name)
pkg=json.loads((root/'package.json').read_text())
check(pkg['scripts'].get('build')=='astro build && pagefind --site dist','Astro + Pagefind build command')
check(pkg.get('type')=='module','Node ESM package')
for p in ('astro.config.mjs','src/content.config.ts','src/pages/index.astro','src/layouts/Base.astro','src/pages/rss.xml.js','src/components/GiscusComments.astro','.github/workflows/verify.yml','scripts/check-dist.mjs'):
 check((root/p).is_file(),'File '+p)
ct=(root/'src/content.config.ts').read_text()
for cat in ('open-source','mcu-soc','hardware','connectivity','display','tools'):
 check(cat in ct,'Article category '+cat)
check('output:\'static\'' in (root/'astro.config.mjs').read_text(),'Static output configuration')
for md in (root/'src/content/articles').glob('*.md'):
 t=md.read_text()
 check(t.startswith('---\n') and t.count('---')>=2,'Markdown frontmatter '+md.name)
for required in ('<html','rel="canonical"','<slot/>'):
 check(required in (root/'src/layouts/Base.astro').read_text(),'Base layout '+required)
print(f'\n{len(errs)} source checks failed.')
sys.exit(bool(errs))
