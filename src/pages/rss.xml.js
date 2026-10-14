import {getCollection} from 'astro:content';
const escapeXml=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
export async function GET(){
  const entries=(await getCollection('articles',({data})=>!data.draft)).sort((a,b)=>b.data.pubDate-a.data.pubDate);
  const items=entries.map(a=>{
    const [lang,...parts]=a.id.split('/');
    const url=`https://embeddednote.com/${lang}/articles/${parts.join('/')}/`;
    return `<item><title>${escapeXml(a.data.title)}</title><link>${escapeXml(url)}</link><guid>${escapeXml(url)}</guid><description>${escapeXml(a.data.description)}</description><pubDate>${a.data.pubDate.toUTCString()}</pubDate><language>${lang}</language></item>`;
  }).join('');
  const xml=`<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>EmbeddedNote</title><link>https://embeddednote.com/en/</link><description>Embedded engineering journal</description>${items}</channel></rss>`;
  return new Response(xml,{headers:{'Content-Type':'application/rss+xml; charset=utf-8'}});
}
