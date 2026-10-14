
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const articles = defineCollection({
  loader: glob({
    pattern: '**/*.md',
    base: './src/content/articles'
  }),

  schema: z.object({
    // 文章标题和摘要
    title: z.string().min(1),
    description: z.string().min(1),

    // 双语信息
    locale: z.enum(['en', 'zh']),
    translationKey: z.string().min(1),

    // 文章日期
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),

    // 保留 V1 的六个技术频道
    category: z.enum([
      'open-source',
      'mcu-soc',
      'hardware',
      'connectivity',
      'display',
      'tools'
    ]),

    // 技术关键词
    tags: z.array(z.string()).default([]),

    // 文章发布状态
    draft: z.boolean().default(false),

    // 作者信息
    author: z.string().default('EmbeddedNote'),

    // 原始参考链接
    sourceUrl: z.string().url().optional(),

    // 独立 SEO
    seoTitle: z.string().optional(),
    seoDescription: z.string().optional()
  })
});

export const collections = {
  articles
};

