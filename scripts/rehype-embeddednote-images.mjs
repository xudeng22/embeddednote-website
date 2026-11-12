// EmbeddedNote performance plugin — images and table wrappers.
// Images: dimensions + lazy loading + srcset (build time, no runtime JS).
// Tables: wrapped in a scroll container so wide tables keep their column widths.
import { readFileSync } from 'node:fs';

const manifest = JSON.parse(
  readFileSync(new URL('../src/data/performance-image-manifest.json', import.meta.url), 'utf8')
);

function wrapTables(node) {
  if (!node || !Array.isArray(node.children)) return;
  // Process children first, then wrap, so a wrapper is never wrapped again.
  for (const child of node.children) wrapTables(child);
  node.children = node.children.map((child) =>
    child && child.type === 'element' && child.tagName === 'table'
      ? {
          type: 'element',
          tagName: 'div',
          properties: { className: ['table-wrap'] },
          children: [child]
        }
      : child
  );
}

export default function embeddednoteImages() {
  return function transformer(tree) {
    let imageIndex = 0;
    function visit(node) {
      if (!node || typeof node !== 'object') return;
      if (node.type === 'element' && node.tagName === 'img') {
        imageIndex += 1;
        const props = node.properties || (node.properties = {});
        const raw = typeof props.src === 'string' ? props.src.split(/[?#]/, 1)[0] : '';
        let key = raw;
        try { key = decodeURI(raw); } catch { /* retain original URL */ }
        const m = manifest[key] || manifest[raw];
        if (m) {
          if (props.width == null) props.width = m[0];
          if (props.height == null) props.height = m[1];
        }
        if (!props.decoding) props.decoding = 'async';
        // First image can be above the fold; do not lazy-load it by default.
        if (!props.loading && imageIndex > 1) props.loading = 'lazy';

        // Responsive width: article bodies render at 800 px on desktop and a
        // little under the viewport on phones, so a 640 px encode is enough
        // there and saves the majority of the bytes on mobile connections.
        if (!props.srcSet && /\.webp$/.test(key)) {
          const variant = key.replace(/\.webp$/, '-640.webp');
          if (manifest[variant]) {
            const width = Array.isArray(m) ? m[0] : null;
            props.srcSet = width
              ? `${raw} ${width}w, ${variant} 640w`
              : `${raw} 800w, ${variant} 640w`;
            if (!props.sizes) props.sizes = '(max-width: 700px) 92vw, 800px';
          }
        }
      }
      if (Array.isArray(node.children)) for (const child of node.children) visit(child);
    }
    visit(tree);
    wrapTables(tree);
  };
}
