// One place for how the notes section is grouped, keyed on translationKey so a
// Chinese and an English edition of the same article always land together.
export const NOTES_GROUPS = [
  {
    slug: 'open-hardware',
    en: 'Open-hardware projects',
    zh: '开源硬件项目',
    noteEn: 'Builds with schematics, firmware and a BOM you can copy.',
    noteZh: '带原理图、固件和物料清单的项目。'
  },
  {
    slug: 'chips-supply',
    en: 'Chips, boards and supply chain',
    zh: '芯片、开发板与供应链',
    noteEn: 'Part selection, price moves and what they mean for a BOM.',
    noteZh: '器件选型、价格变化，以及它们对 BOM 的影响。'
  },
  {
    slug: 'ai-hardware',
    en: 'AI hardware',
    zh: 'AI 硬件',
    noteEn: 'Devices that run models locally, and the prototypes behind them.',
    noteZh: '把模型跑在本地设备上的产品与原型。'
  },
  {
    slug: 'space-radio',
    en: 'Satellite and radio',
    zh: '卫星与无线',
    noteEn: 'CubeSats, LoRa mesh, radar and GPS builds.',
    noteZh: '立方星、LoRa 组网、雷达与 GPS 项目。'
  }
];

// Explicit, because a title-based guess puts "training" and "Again" in the AI group.
const AI_KEYS = new Set([
  'claude-electronics-design',
  'codex-hardware-41-projects-2026',
  'hachimodock-desktop-ai-buddy',
  'arm-cortex-m-edge-ai-roadmap'
]);

const SPACE_KEYS = new Set([
  'kensat-2u-cubesat-llm',
  'meshtastic',
  'micro-radar-esp32-c3',
  'moto-gps-waveshare',
  'x-track-gps-bike-computer',
  'imu-array-32-fpga'
]);

export function notesGroupOf(data) {
  const key = String(data?.translationKey ?? '');
  if (AI_KEYS.has(key)) return 'ai-hardware';
  if (SPACE_KEYS.has(key)) return 'space-radio';
  if (['mcu-soc', 'hardware', 'tools'].includes(data?.category)) return 'chips-supply';
  return 'open-hardware';
}

export function isNotesArticle(data) {
  return (
    data?.series !== 'epaper' &&
    data?.series !== 'ble' &&
    data?.category !== 'display' &&
    data?.category !== 'connectivity'
  );
}
