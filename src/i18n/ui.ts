export type Lang = 'en' | 'zh';
export const channels = [
  { slug: 'open-source', en: 'Open Source Projects', zh: '开源项目', enDesc: 'GitHub, schematics and BOMs', zhDesc: 'GitHub、开源工程与器件 BOM' },
  { slug: 'mcu-soc', en: 'MCU & SoC', zh: 'MCU 与 SoC', enDesc: 'STM32, ESP32 and RISC-V', zhDesc: 'STM32、ESP32、RISC-V' },
  { slug: 'hardware', en: 'Hardware Design', zh: '硬件设计', enDesc: 'PCB, power and circuits', zhDesc: 'PCB、电源、接口电路' },
  { slug: 'connectivity', en: 'Connectivity', zh: '通信技术', enDesc: 'BLE, Wi-Fi, NFC and CAN', zhDesc: 'BLE、Wi-Fi、NFC、CAN' },
  { slug: 'display', en: 'Display Technology', zh: '显示技术', enDesc: 'E-paper, TFT and Mini LED', zhDesc: '电子纸、TFT、Mini LED' },
  { slug: 'tools', en: 'Development Tools', zh: '开发工具', enDesc: 'IDEs, debugging and testing', zhDesc: 'IDE、调试、仿真与测试' }
] as const;
export const ui = {
  en: {title:'Embedded engineering, made practical', description:'Chips, hardware, open source and hands-on engineering.', latest:'Latest articles', topics:'Six technical channels', about:'About', discussion:'Discussion', empty:'No articles yet.', read:'Read article', langLabel:'中文', search:'Search chips, protocols, projects or keywords'},
  zh: {title:'把复杂技术，写成能落地的工程知识', description:'嵌入式系统、芯片、开源项目与工程实践。', latest:'最新文章', topics:'六大技术频道', about:'关于', discussion:'技术讨论', empty:'暂无文章', read:'阅读文章', langLabel:'EN', search:'搜索芯片型号、协议、项目或关键词'}
} as const;
