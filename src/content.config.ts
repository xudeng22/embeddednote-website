import {defineCollection} from 'astro:content';
import {glob} from 'astro/loaders';
import {z} from 'astro/zod';
const articles = defineCollection({
  loader: glob({pattern:'**/*.md',base:'./src/content/articles'}),
  schema: z.object({
    title:z.string().min(1),description:z.string().min(1),
    locale:z.enum(['en','zh']),translationKey:z.string().min(1),
    pubDate:z.coerce.date(),updatedDate:z.coerce.date().optional(),
    category:z.enum(['open-source','mcu-soc','hardware','connectivity','display','tools']),
    tags:z.array(z.string()).default([]),draft:z.boolean().default(false),
    author:z.string().default('EmbeddedNote'),sourceUrl:z.string().url().optional(),
    seoTitle:z.string().optional(),seoDescription:z.string().optional()
  })
});
const about = defineCollection({
  loader: glob({pattern:'*.md',base:'./src/content/about'}),
  schema: z.object({title:z.string(),description:z.string(),locale:z.enum(['en','zh'])})
});
export const collections = {articles,about};
