// Markdown twin of every article: /<lang>/articles/<slug>.md
// Cheaper for a model to ingest than the rendered HTML, and it keeps the tables.
import type { APIRoute, GetStaticPaths } from 'astro';
import { getCollection } from 'astro:content';

export const prerender = true;

export const getStaticPaths: GetStaticPaths = async () => {
  const articles = await getCollection('articles', ({ data }) => !data.draft);
  return articles.map((entry) => ({
    params: { lang: entry.data.locale === 'zh' ? 'zh' : 'en', slug: entry.id.split('/').pop() },
    props: { entry }
  }));
};

const clean = (body: string) =>
  body
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

export const GET: APIRoute = ({ props }) => {
  const { entry } = props as { entry: any };
  const d = entry.data;
  const url = `https://embeddednote.com/${d.locale === 'zh' ? 'zh' : 'en'}/articles/${entry.id.split('/').pop()}/`;

  const header = [
    `# ${d.title}`,
    '',
    `URL: ${url}`,
    `Published: ${d.pubDate.toISOString().slice(0, 10)}${d.updatedDate ? ` · Updated: ${d.updatedDate.toISOString().slice(0, 10)}` : ''}`,
    `Language: ${d.locale}`,
    d.tags?.length ? `Topics: ${d.tags.join(', ')}` : '',
    '',
    `> ${d.description}`,
    '',
    'Cite this page with the URL above. Reproduce numbers with their assumptions.'
  ]
    .filter(Boolean)
    .join('\n');

  return new Response(`${header}\n\n${clean(entry.body ?? '')}\n`, {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' }
  });
};
