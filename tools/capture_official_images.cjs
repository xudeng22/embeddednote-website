// Fetch creator-submitted photographs from their own project cards on the official gallery.
// This script does not generate pictures and never substitutes search-result imagery.
// Run on the publisher's own computer with a standard network connection and Edge/Chrome.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const ROOT = path.resolve(__dirname, '..');
const GALLERY = 'https://youcanjustbuildthings.openai.chatgpt.site/';
const DEST = path.join(ROOT,'public','uploads','codex-hardware-41-projects-2026');
const ITEMS = JSON.parse(fs.readFileSync(path.join(__dirname,'Codex41_Photo_Sources.json'),'utf8'));
const PLAYWRIGHT_DIR = process.env.CODEX41_PLAYWRIGHT_DIR;
if (!PLAYWRIGHT_DIR) {
  console.error('Missing CODEX41_PLAYWRIGHT_DIR. Please run GET_41_OFFICIAL_IMAGES.cmd.');
  process.exit(2);
}
const {chromium} = require(path.join(PLAYWRIGHT_DIR,'node_modules','playwright'));
fs.mkdirSync(DEST,{recursive:true});

function isWebp(file) {
  try {
    const d=fs.readFileSync(file);
    return d.length>1800 && d.toString('ascii',0,4)==='RIFF' && d.toString('ascii',8,12)==='WEBP';
  } catch { return false; }
}
function sha(file) {return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');}
function fig(item,lang){
  const n=String(item.index).padStart(2,'0');
  const alt=lang==='zh' ? '项目官方展示图片：'+item.nameZh+' / '+item.name : 'Creator-submitted project photograph: '+item.name;
  const escapeAttr=(s)=>s.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
  return `<figure class="project-photo" style="margin:14px 0 22px;">\n<a href="${escapeAttr(item.url)}" target="_blank" rel="noopener noreferrer" aria-label="${lang==='zh'?'查看项目原始图片':'View original project submission'}">\n<img src="/uploads/codex-hardware-41-projects-2026/official-${n}.webp" alt="${escapeAttr(alt)}" loading="lazy" decoding="async" style="display:block;width:100%;max-width:720px;height:auto;max-height:480px;object-fit:contain;object-position:left center;border-radius:6px;" />\n</a>\n</figure>`;
}
async function chooseAndSave(page, imageLocator, output) {
  const count=await imageLocator.count();
  for(let i=0;i<Math.min(6,count);i++) {
    const loc=imageLocator.nth(i);
    try {
      await loc.scrollIntoViewIfNeeded({timeout:9000});
      for(let retry=0; retry<18; retry++) {
        const ok=await loc.evaluate(e=> e.tagName==='IMG' && e.complete && e.naturalWidth>=96 && e.naturalHeight>=72 && parseFloat(getComputedStyle(e).opacity||'1')>.03 ).catch(()=>false);
        if(ok) break;
        await page.waitForTimeout(400);
      }
      const props=await loc.evaluate(e=>({w:e.naturalWidth,h:e.naturalHeight,opacity:getComputedStyle(e).opacity,src:e.currentSrc||e.src}));
      const rect=await loc.boundingBox();
      if(props.w<96||props.h<72||!rect||rect.width<90||rect.height<65||Number(props.opacity)<=.03)continue;
      // Prefer the actual image bytes from the official project page. If its CDN
      // requires browser-only access, capture the original <img> pixels instead.
      let raw=null;
      let mime='image/png';
      try {
        if(/^https?:/.test(props.src)) {
          const res=await page.context().request.get(props.src,{timeout:16000});
          const ct=(res.headers()['content-type']||'').split(';')[0].trim().toLowerCase();
          if(res.ok() && ['image/jpeg','image/png','image/webp','image/gif'].includes(ct)) {
            const bytes=await res.body();
            if(bytes.length>2000 && bytes.length<9000000){raw=bytes;mime=ct;}
          }
        }
      } catch {}
      if(!raw)raw=await loc.screenshot({type:'png',animations:'disabled',timeout:25000});
      // Compress to WebP locally in the browser. All pixels come from the maker's
      // real project image; NO generative AI or substitute product photos are used.
      const data=await page.evaluate(async ({b64,mime})=>{
        const img=new Image();
        img.src='data:'+mime+';base64,'+b64;
        await img.decode();
        const scale=Math.min(1,1280/Math.max(img.naturalWidth,img.naturalHeight));
        const canvas=document.createElement('canvas');
        canvas.width=Math.max(1,Math.round(img.naturalWidth*scale));
        canvas.height=Math.max(1,Math.round(img.naturalHeight*scale));
        canvas.getContext('2d').drawImage(img,0,0,canvas.width,canvas.height);
        return canvas.toDataURL('image/webp',0.85);
      },{b64:raw.toString('base64'),mime});
      if(!data.startsWith('data:image/webp;base64,')) continue;
      fs.writeFileSync(output,Buffer.from(data.slice('data:image/webp;base64,'.length),'base64'));
      if(isWebp(output)) return {ok:true,source:props.src,w:props.w,h:props.h};
    }catch(err){
      // Try the next image. Do not replace unavailable photos with unrelated images.
    }
  }
  return {ok:false};
}
async function getFromCard(page,item,destination) {
  const slug=new URL(item.url).pathname.split('/').pop();
  const loc=page.locator(`a[href*="${slug}"] img`);
  return await chooseAndSave(page,loc,destination);
}
async function getFromProjectPage(page,item,destination) {
  try {
    await page.goto(item.url,{waitUntil:'domcontentloaded',timeout:45000});
    await page.waitForTimeout(1500);
    // On project pages the large hero images generally sit inside <main>.
    let loc=page.locator('main img:visible');
    if(await loc.count()===0)loc=page.locator('article img:visible');
    return await chooseAndSave(page,loc,destination);
  }catch {return {ok:false};}
}
async function run() {
  let browser;
  try { browser=await chromium.launch({channel:'msedge',headless:true});}
  catch {try {browser=await chromium.launch({channel:'chrome',headless:true});}
  catch {console.error('Microsoft Edge or Google Chrome is required.');process.exitCode=2;return;}}
  const context=await browser.newContext({viewport:{width:1420,height:970},deviceScaleFactor:1.7,locale:'en-US',ignoreHTTPSErrors:false});
  const home=await context.newPage();
  const detail=await context.newPage();
  const report=[];
  try{
    await home.goto(GALLERY+'?sort=top#projects',{waitUntil:'domcontentloaded',timeout:60000});
    await home.waitForTimeout(2100);
    const cardCount=await home.locator('a[href*="/projects/"] img').count();
    console.log(`Found ${cardCount} project photo elements in the original gallery.`);
    for(const item of ITEMS){
      const n=String(item.index).padStart(2,'0');
      const file=path.join(DEST,`official-${n}.webp`);
      let found;
      if(isWebp(file)){found={ok:true,source:'previously captured photo'};}
      else {
        found=await getFromCard(home,item,file);
        if(!found.ok)found=await getFromProjectPage(detail,item,file);
      }
      const state=found.ok?'OK':'MISSING';
      console.log(`${n}/41 ${state} ${item.name}`);
      report.push({...item,ok:found.ok,file:found.ok?path.relative(ROOT,file):'',source:found.source||'',imageWidth:found.w||null,imageHeight:found.h||null});
    }
  }finally { await browser.close(); }
  const hashMap=new Map();
  for(const r of report.filter(r=>r.ok)){
    const hash=sha(path.join(ROOT,r.file));
    if(hashMap.has(hash)){
      r.ok=false;
      r.problem=`Image identical to entry ${hashMap.get(hash)}; requires manual check`;
      console.warn(`Warning: duplicate image for item ${r.index}`);
    }else hashMap.set(hash,r.index);
  }
  const passed=report.filter(x=>x.ok).length;
  fs.writeFileSync(path.join(ROOT,'IMAGE_CAPTURE_REPORT.json'),JSON.stringify({captured:passed,total:41,report},null,2)+'\n','utf8');
  if(passed!==41){
    console.error(`Only ${passed}/41 official photos verified. Original Markdown has been left unmodified, preventing broken image references.`);
    console.error('Check IMAGE_CAPTURE_REPORT.json, verify gallery accessibility, then rerun. Previously captured photos are reused.');
    process.exitCode=1;
    return;
  }
  for(const lang of ['en','zh']){
    const file=path.join(ROOT,'src','content','articles',lang,'codex-hardware-41-projects-2026.md');
    let content=fs.readFileSync(file,'utf8');
    for(const item of ITEMS){
      const marker=`<!-- CODEX41_OFFICIAL_IMAGE_${String(item.index).padStart(2,'0')} -->`;
      if(content.includes(marker))content=content.replace(marker,fig(item,lang));
    }
    fs.writeFileSync(file,content,'utf8');
    const images=(content.match(/\/uploads\/codex-hardware-41-projects-2026\/official-\d\d\.webp/g)||[]);
    if(images.length!==41)throw new Error(`${lang} article should contain 41 photos, found ${images.length}`);
  }
  console.log('SUCCESS: Captured 41 verified project-card photos and inserted all 41 images into BOTH Markdown articles.');
  console.log('Copy src/ and public/ to your local embeddednote-website repository using GitHub Desktop.');
}
run().catch(e=>{console.error(e.stack||e);process.exitCode=1;});
