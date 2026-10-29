---
title: 'HachimoDock: A Desktop AI Sidekick for Coding Agents and Xiaomi Home'
description: 'HachimoDock puts Codex and Claude Code status on an ESP32-P4 desk pet, with USB session tracking, voice controls, PetUI widgets and optional Xiaomi MiLoCo integration.'
locale: en
translationKey: hachimodock-desktop-ai-buddy
pubDate: '2026-10-29'
category: open-source
tags:
  - HachimoDock
  - ESP32-P4
  - AI Agent
  - Desktop AI Sidekick
  - Codex
  - Claude Code
  - MIPI-DSI
  - PetUI
  - Xiaomi MiLoCo
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/YizhengWw/HachimoDock
seoTitle: 'HachimoDock: ESP32-P4 Desktop AI Sidekick for Codex and Claude Code'
seoDescription: 'How HachimoDock tracks coding agents over USB, animates an ESP32-P4 desktop pet, supports PetUI widgets and bridges Xiaomi Home through MiLoCo.'
---

When you hand a coding job to Codex or Claude Code, the awkward part isn't always the wait. It's figuring out whether the agent is still working, calling a tool, or sitting at an approval prompt while you're doing something else. You can keep switching back to the terminal, or you can put HachimoDock on your desk. Its small screen shows a West Highland terrier that reacts to the agent's current state—thinking, working, waiting for input, finished or failed. A glance across the desk is enough to tell whether you need to step in.

HachimoDock, also known in Chinese as the *Hachimi machine*, was presented at the 2026 Guancha conference; [Chinese technology coverage](https://www.ithome.com/1/017/842.htm) describes it as a project incubated by a Xiaomi innovation team. The repository is maintained under an individual GitHub account, though, and it isn't a Xiaomi retail product. The [GitHub repository](https://github.com/YizhengWw/HachimoDock) holds the Windows/macOS desktop client and ESP32-P4 firmware. Schematics, PCB layout, BOM, enclosure models and assembly instructions are published separately on [OSHWHub](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc), a Chinese open-hardware platform.

![HachimoDock desktop device displaying a West Highland terrier](https://image.lceda.cn/oshwhub/pullImage/6c47814b144549beb179528ea77cd75e.png)

*HachimoDock on a desk: three mechanical keys, an orange joystick and a computer running the agent.*

The hardware starts with a Waveshare **ESP32-P4-WIFI6-series** development board. Its ESP32-P4 is a dual-core RISC-V MCU with a high-performance core running at up to 400 MHz; the documented board carries **32 MB of PSRAM and 32 MB of flash**. The display is a **2.8-inch, 480 × 640 IPS panel connected over MIPI DSI**. That's a useful amount of space for character animations, subtitles and session bubbles without resorting to a more powerful application processor. Check the display's connector and cable version before ordering: the hardware guide lists 15- and 22-pin DSI variants, with a shaped cover glass as an enclosure option. Touch input isn't required.

The board name includes Wi-Fi 6, but that shouldn't be confused with a Wi-Fi radio inside the ESP32-P4 itself. Wireless capability depends on the development board's companion hardware; **the current HachimoDock device runtime communicates with the host primarily over USB**.

Below the screen sit three Kailh **CPG135001D01** mechanical switches. A **YA13S-L7.4-B10Ka(60)-0-DL01** self-centering, 5 kΩ joystick adds four directions and a center press. Short and long presses give the firmware a total of twelve configurable input gestures. The audio hardware includes a microphone, small speaker and an ES8311 codec path; the firmware also supports an ES7210 capture path on suitable hardware. Audio is captured on the device and sent to the PC for speech recognition—it does not run a full ASR service on the P4.

![HachimoDock keys and four-way joystick](https://image.lceda.cn/oshwhub/pullImage/0187d6df22f74724acda54e111c7c850.png)

*Three switches and a joystick provide most of the interaction; the display doesn't have to be touch-enabled.*

This isn't a custom ESP32-P4 motherboard built from scratch. The Waveshare module supplies the processor, memory and main interfaces, while a smaller carrier PCB brings the keys, joystick and connectors together. Two 2.54 mm, 20-position female headers join the boards. The [OSHWHub hardware page](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc) shows the key and joystick connections in the schematic and the header footprint arrangement on **PCB_V1.2**. It's the right place to check actual pin assignments, enclosure dimensions and the BOM rather than relying on a product photo.

The hardware has changed direction along the way. Earlier versions explored a Radxa Cubie A7Z and a Raspberry Pi Zero 2W, including networked MQTT/HTTP approaches. The current design settled on an ESP32-P4 with a direct USB connection. You will still find MQTT in parts of the **PC-side bridge**, but that does **not** mean the current P4 firmware receives its status stream over MQTT. USB serial is the active device link.

![HachimoDock desktop-agent and ESP32-P4 architecture](/uploads/hachimodock/hachimodock-architecture-en.webp)

*The host monitors agent sessions and exchanges state and input events with the ESP32-P4 over USB. See the hardware repository for electrical schematics.*

The often-repeated **¥150 DIY cost** also deserves some context. The hardware listing quotes the Waveshare board from about **¥81.15**, the display at **¥65**, and the joystick from **¥3.54**. Those three parts alone approach ¥150, before the Kailh switches, speaker, headers, carrier PCB, printed case or shipping. It's a starting estimate, not the price of a ready-to-use kit. Before flashing anything, check the **ESP32-P4 silicon revision**: the project's complete v1 and v3 firmware images are not interchangeable, and a full flash can overwrite the device's settings and media assets.

The desktop manager handles the part that makes the pet useful: tracking agent state. The **Tauri/React manager** runs a local bridge that monitors the sessions exposed by Codex, Claude Code, OpenClaw and other supported agents. It normalizes what each integration can report, then sends the relevant updates to the P4 over USB. The display can show several active sessions as bubbles; the dog changes animation as a task starts working, calls tools or waits for approval. Completed and failed sessions remain visible for about a minute so the notification doesn't vanish as soon as the task ends. Capabilities differ between integrations: selecting a WorkBuddy bubble on the device, for example, does not automatically switch the active desktop conversation.

![HachimoDock multiple agent session bubbles](https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/assets/session-bubbles.webp)

*Session bubbles show the tasks the desktop integration can currently observe.*

![HachimoDock agent-state animation](https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/assets/agent-status.gif)

*The bundled character animations change as an agent moves between states.*

*The project also includes animation clips for “thinking” and “task completed”:*

<video controls playsinline preload="none" width="720"><source src="https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/pc/public/terrier-clips/working.thinking.mp4" type="video/mp4" /></video>

<video controls playsinline preload="none" width="720"><source src="https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/pc/public/terrier-clips/done.mp4" type="video/mp4" /></video>

The controls are useful for more than checking progress. Hold the configured voice key and the device records audio; the host handles ASR and routes the resulting text into the selected agent's input flow. Some integrations leave the text as a draft until you confirm it. The keys and joystick can also switch between session bubbles, navigate widgets and provide shortcuts. A Westie is the default character, but you can import images and animation clips or generate a new character using a separately configured service. Public builds don't include anyone else's API credentials.

![HachimoDock voice input interface](https://image.lceda.cn/oshwhub/pullImage/0dddebc05c064f3a812d278b7c5dbe6e.png)

*Audio capture happens on the device; recognition and agent input routing happen on the PC.*

Then there's **PetUI**, a runtime for small games and tools rather than just a single animated pet. The component manager can sync utilities such as a Pomodoro timer, task list, computer-status panel and stock watchlist, along with simple games. You can also ask a coding agent to build a new component using the project's `petui` Skill. Its output is checked against the **480 × 640 layout**, control mapping and resource limits before being copied to the device. The P4 runs the resulting component through its own widget runtime; it isn't executing arbitrary web JavaScript supplied by the agent.

![HachimoDock PetUI component manager](https://image.lceda.cn/oshwhub/pullImage/410d87c82a0049d483f58391c23c5c72.jpg)

*PetUI components are managed on the computer and synchronized to the display.*

There is also an optional **Xiaomi MiLoCo** integration. Once a Xiaomi Home account is authorized on the desktop side, supported devices can be controlled through natural-language requests—playing music on a compatible speaker, for instance, or opening an available smart-home panel. That connection is handled by the PC software, not by having the ESP32-P4 join Xiaomi's network. The exact controls depend on the authorized devices and service configuration.

Check the licensing terms before turning the design into a product. Although the design files and source code are public, the current [HachimoDock license](https://github.com/YizhengWw/HachimoDock/blob/main/LICENSE) is **non-commercial and source-available**, not a standard open-source license such as GPL or MIT. Personal, non-commercial builds and modifications are permitted under its terms; selling kits, integrating it into a paid product or offering an independent commercial service requires separate written permission. An older GPL-3.0-only label on the hardware-sharing page does not override the current repository license, and the MiLoCo integration has additional Xiaomi license conditions.

For a hands-on build, start with the [repository README](https://github.com/YizhengWw/HachimoDock), the [OSHWHub hardware files](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc) and the [firmware flashing guide](https://github.com/YizhengWw/HachimoDock/blob/main/firmware/BUILD.md). The wiring and chip revision are worth checking before you order parts or flash the complete image.
