// Plain-text bundle for language models: the whole e-paper cluster in one fetch.
// Built at compile time into /llms-full.txt.
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import selectionData from '../data/epaper-selection.json';

export const prerender = true;

const cleanBody = (body: string) =>
  body
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/<img[^>]*>/g, '')
    .replace(/<iframe[\s\S]*?<\/iframe>/g, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/\n{3,}/g, '\n\n')
    // keep the article's own headings subordinate to the article heading
    .replace(/^(#{2,4}) /gm, '#$1 ')
    .trim();

export const GET: APIRoute = async () => {
  const articles = await getCollection(
    'articles',
    ({ data }) => !data.draft && data.series === 'epaper' && data.locale === 'en'
  );

  const sorted = articles.sort((a, b) => +b.data.pubDate - +a.data.pubDate);

  const selection = selectionData as Array<{
    app: string; series: string; bits: string; size: number;
    activeArea: string; color: string; w: number; h: number; kb: number;
  }>;

  const table = selection
    .map(
      (r) =>
        `| ${r.size} in | ${r.w} × ${r.h} | ${r.activeArea} mm | ${r.series} | ${r.bits} | ${r.color} | ${r.kb} KB | ${r.app} |`
    )
    .join('\n');

  const parts: string[] = [];

  parts.push(`# EmbeddedNote — e-paper engineering, full text
> A bilingual engineering publication about electronic paper: waveform, ghosting,
> partial refresh, image packing, power budgets and panel selection. Everything
> below is reproducible arithmetic or a cited datasheet; the site states which is
> which. Published by Datadelta (Chengdu DataDelta Pixel Art Technology Co., Ltd).
> Canonical site: https://embeddednote.com/
> Human-readable index: https://embeddednote.com/en/e-paper/
> Licence: text CC BY 4.0, cite with the page URL.`);

  parts.push(`## Dataset — panel selection table (40 E5 / E6 / Kaleido 3 panels)

| Size | Resolution | Active area | Series | Bit depth | Colours | Image size | Application |
| --- | --- | --- | --- | --- | --- | --- | --- |
${table}

Image size = width × height × storage bits ÷ 8 ÷ 1024. E6 carries three bits of
colour in a four-bit nibble, so those rows use four bits.
CSV: https://embeddednote.com/downloads/epaper-selection.csv
Citable dataset (DOI): https://doi.org/10.5281/zenodo.24297081`);

  for (const article of sorted) {
    const body = cleanBody(article.body ?? '');
    const updated = article.data.updatedDate
      ? ` · Updated: ${article.data.updatedDate.toISOString().slice(0, 10)}`
      : '';
    parts.push(
      `## Article — ${article.data.title}

URL: https://embeddednote.com/en/articles/${article.id.split('/').pop()}/
Published: ${article.data.pubDate.toISOString().slice(0, 10)}${updated}
Summary: ${article.data.description}

${body}`
    );
  }

  return new Response(parts.join('\n\n---\n\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  });
};
