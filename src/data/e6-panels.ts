// Canonical data for the 15 E6 (Spectra 6) sizes the site writes about.
//
// Source of truth: src/content/articles/en/epaper-size-chart.md and the
// downloadable CSV at public/downloads/epaper-e6-sizes.csv. Keep the three in
// sync — the build does not reconcile them for you.
//
// Editorial rule that matters here: ppi is only set where a module datasheet
// states it or gives an active area. `null` means "not published for that
// part", not "unknown quality". Do not fill the blanks by dividing the
// diagonal: a diagonal is an outline measurement and does not determine
// resolution.

export interface E6Panel {
  /** URL segment, e.g. "13-3-inch". */
  slug: string;
  /** Diagonal in inches, as written in the catalogue, e.g. "13.3". */
  sizeIn: string;
  width: number;
  height: number;
  pixels: number;
  /** Packed 4-bit indices, w × h ÷ 2. */
  raw4: number;
  /** One index per byte, w × h. */
  raw8: number;
  /** Only where a datasheet publishes it. */
  ppi: number | null;
  /** Only where the interface is documented for that part. */
  interfaceNote?: { en: string; zh: string };
  /** Size-class use cases, aligned with the "typical use" column on /supply/. */
  use: { en: string; zh: string };
}

export const e6Panels: E6Panel[] = [
  {
    slug: '1-18-inch',
    sizeIn: '1.18',
    width: 240,
    height: 206,
    pixels: 49440,
    raw4: 24720,
    raw8: 49440,
    ppi: null,
    use: { en: 'badges and small wearable tags', zh: '胸章与小尺寸可穿戴标签' },
  },
  {
    slug: '1-54-inch',
    sizeIn: '1.54',
    width: 200,
    height: 200,
    pixels: 40000,
    raw4: 20000,
    raw8: 40000,
    ppi: null,
    use: { en: 'badges, tags and small status displays', zh: '胸牌、标签与小尺寸状态屏' },
  },
  {
    slug: '2-61-inch',
    sizeIn: '2.61',
    width: 400,
    height: 400,
    pixels: 160000,
    raw4: 80000,
    raw8: 160000,
    ppi: 217,
    use: { en: 'square tags, desk cards and small frames', zh: '方形标签、桌牌与小相框' },
  },
  {
    slug: '3-68-inch',
    sizeIn: '3.68',
    width: 528,
    height: 792,
    pixels: 418176,
    raw4: 209088,
    raw8: 418176,
    ppi: null,
    use: { en: 'portrait tags, badges and reader-sized displays', zh: '竖版标签、胸牌与阅读器尺寸显示' },
  },
  {
    slug: '3-98-inch',
    sizeIn: '3.98',
    width: 552,
    height: 768,
    pixels: 423936,
    raw4: 211968,
    raw8: 423936,
    ppi: null,
    use: { en: 'portrait tags and handheld instruments', zh: '竖版标签与手持仪表' },
  },
  {
    slug: '4-0-inch',
    sizeIn: '4.0',
    width: 570,
    height: 800,
    pixels: 456000,
    raw4: 228000,
    raw8: 456000,
    ppi: null,
    use: { en: 'desk cards, shelf labels and small signage', zh: '桌牌、货架标签与小尺寸标牌' },
  },
  {
    slug: '4-38-inch',
    sizeIn: '4.38',
    width: 560,
    height: 800,
    pixels: 448000,
    raw4: 224000,
    raw8: 448000,
    ppi: null,
    use: { en: 'desk cards, badges and low-power instruments', zh: '桌牌、胸牌与低功耗仪表' },
  },
  {
    slug: '6-19-inch',
    sizeIn: '6.19',
    width: 494,
    height: 1490,
    pixels: 736060,
    raw4: 368030,
    raw8: 736060,
    ppi: null,
    use: { en: 'long shelf strips and shelf-edge labels', zh: '长条货架条屏与电子价签' },
  },
  {
    slug: '7-09-inch',
    sizeIn: '7.09',
    width: 1200,
    height: 1600,
    pixels: 1920000,
    raw4: 960000,
    raw8: 1920000,
    ppi: 282,
    use: { en: 'desk frames, badges and photo displays', zh: '桌面相框、胸章与照片显示' },
  },
  {
    slug: '9-7-inch',
    sizeIn: '9.7',
    width: 1120,
    height: 784,
    pixels: 878080,
    raw4: 439040,
    raw8: 878080,
    ppi: null,
    use: { en: 'shelf display, instruments and signage panels', zh: '货架显示、仪表与标牌面板' },
  },
  {
    slug: '10-1-inch',
    sizeIn: '10.1',
    width: 1600,
    height: 1200,
    pixels: 1920000,
    raw4: 960000,
    raw8: 1920000,
    ppi: 200,
    interfaceNote: {
      en: 'The 10.1-inch module is a 16-bit parallel interface.',
      zh: '10.1 寸模组是 16 位并口。',
    },
    use: { en: 'wall frames, office signage and shelf displays', zh: '墙面相框、办公标牌与货架显示' },
  },
  {
    slug: '13-3-inch',
    sizeIn: '13.3',
    width: 1200,
    height: 1600,
    pixels: 1920000,
    raw4: 960000,
    raw8: 1920000,
    ppi: 150,
    use: { en: 'A4 frames, office signage and retail displays', zh: 'A4 相框、办公标牌与零售显示' },
  },
  {
    slug: '16-36-inch',
    sizeIn: '16.36',
    width: 3840,
    height: 1490,
    pixels: 5721600,
    raw4: 2860800,
    raw8: 5721600,
    ppi: null,
    use: { en: 'wide shelving strips and long banner displays', zh: '宽幅货架条屏与长条横幅显示' },
  },
  {
    slug: '18-56-inch',
    sizeIn: '18.56',
    width: 400,
    height: 3200,
    pixels: 1280000,
    raw4: 640000,
    raw8: 1280000,
    ppi: null,
    use: { en: 'tall column displays and vertical shelf strips', zh: '竖向柱状显示与竖版货架条屏' },
  },
  {
    slug: '28-5-inch',
    sizeIn: '28.5',
    width: 2160,
    height: 3060,
    pixels: 6609600,
    raw4: 3304800,
    raw8: 6609600,
    ppi: null,
    use: { en: 'large-format signage and poster frames', zh: '大幅面标牌与海报相框' },
  },
  {
    slug: '31-5-inch',
    sizeIn: '31.5',
    width: 2560,
    height: 1440,
    pixels: 3686400,
    raw4: 1843200,
    raw8: 3686400,
    ppi: 94,
    interfaceNote: {
      en: 'The 31.5-inch panel uses SPI with single, dual or quad data lines, and QSPI for pixel data.',
      zh: '31.5 寸面板是支持单/双/四线的 SPI，像素数据走 QSPI。',
    },
    use: { en: 'wall frames, retail signage and large-format posters', zh: '墙面相框、零售标牌与大幅面海报' },
  },
];

export const e6BySlug = new Map(e6Panels.map((panel) => [panel.slug, panel]));

/** Number of 4-bit frames of `bytes` that fit in a buffer of `capacity`. */
export const frameCount = (bytes: number, capacity: number) => Math.floor(capacity / bytes);

/** Human-readable byte label used in copy and metadata. */
export const bytes = (value: number) => `${value.toLocaleString('en-US')} B`;
