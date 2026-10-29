---
title: 'HachimoDock: Meet the Desktop AI Buddy That Keeps Tabs on Your Coding Agents'
description: 'Inside HachimoDock: an ESP32-P4 desk pet that follows Codex and Claude sessions, shows status animations and accepts voice or joystick input over USB.'
locale: en
translationKey: hachimodock-desktop-ai-buddy
pubDate: '2026-10-29'
category: open-source
tags:
- HachimoDock
- ESP32-P4
- AI Agent
- Desktop AI Buddy
- Codex
- Claude
- MIPI-DSI
- PetUI
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/YizhengWw/HachimoDock
seoTitle: 'HachimoDock: An ESP32-P4 Desktop AI Buddy for Codex and Claude'
seoDescription: 'Inside the HachimoDock desk pet: ESP32-P4, 480×640 DSI display, Agent sessions over USB, PetUI widgets, MiLoCo integration and open hardware files.'
---

Coding agents are good at taking over a task, but they are not especially good at telling you when to look back at the terminal. A long Codex or Claude session may be reading a repository, calling tools, waiting for approval, or sitting on an error. HachimoDock makes those states visible without another application window: a small West Highland terrier on your desk changes its expression, animation and speech bubble as the job progresses. The project has drawn attention in China following reports of incubation by a Xiaomi innovation team, although the GitHub repository is maintained under an individual's account and this is not a Xiaomi retail product. The hardware is documented separately on OSHWHub. [Conference coverage](https://www.ithome.com/1/017/842.htm) gives some background.

![HachimoDock desktop device beside a laptop](https://image.lceda.cn/oshwhub/pullImage/6c47814b144549beb179528ea77cd75e.png)

*The HachimoDock device, with three keys and an orange joystick, beside its host computer. Source: project documentation.*

It is tempting to describe the device as an AI speaker with a screen, but that misses the design. The ESP32-P4 does not run Codex, Claude or a local large language model. The host application watches desktop Agent sessions, normalizes the states it can obtain and sends updates over USB. The embedded firmware handles the pet animation, session bubbles and a small widget runtime called PetUI. Button, joystick and microphone events go the other way, back to the host. Integrations cover Codex, Claude, OpenClaw, MiMoCode and WorkBuddy, with different levels of session access. In particular, selecting a WorkBuddy bubble on the device does not automatically switch the corresponding desktop conversation.

![HachimoDock active Agent session bubbles](https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/assets/session-bubbles.webp)

*Session bubbles indicate active tasks; completed and failed sessions remain visible briefly rather than disappearing immediately.*

![HachimoDock functional architecture](/uploads/hachimodock/hachimodock-architecture-en.webp)

*Functional diagram assembled from the public documentation—not the project's electrical schematic.*

### An ESP32-P4 board, a DSI display and actual controls

The hardware is built around an **ESP32-P4** with dual-core RISC-V processing, a high-performance core rated up to 400 MHz, **32 MB of flash** and **32 MB of PSRAM** in the documented board configuration. Its **2.8-inch, 480 × 640 MIPI-DSI display** provides substantially more room for animations, subtitles and session cards than a tiny monochrome OLED. Three Kailh mechanical switches sit below the display, with a four-way joystick and center push to the right. A microphone and small speaker support the voice features. Short and long presses across the three keys and the joystick add up to twelve configurable input gestures.

![HachimoDock hardware close-up](https://image.lceda.cn/oshwhub/pullImage/0187d6df22f74724acda54e111c7c850.png)

*The key-and-joystick enclosure. The project does not require a touch-sensitive display for its current interaction model.*

This is not a fully custom ESP32-P4 mainboard. The Waveshare development board supplies the processor, memory and primary interfaces; the additional PCB organizes the switches, joystick and wiring into something that fits a compact enclosure. Everyday device-to-PC messaging runs over **USB-UART**. The hardware preserves the ESP32-P4's native USB High-Speed OTG capability, but that does not mean the current firmware exposes a USB video or audio class device. The LCD uses **DSI, not CSI**, and the display pinout and P4 chip revision need checking before ordering parts.

The published bill of materials is also worth reading before trusting the often-quoted **¥150 build cost**. The listed prices put the Waveshare board at roughly ¥81.15, the 480 × 640 panel at ¥65, the joystick at ¥3.54 and three Kailh switches at ¥12.70, before adding a speaker and headers. Those listed items alone bring the partial total above **¥167**, without fully accounting for PCB fabrication, enclosure, shipping and assembly losses. The figure is an indicative DIY budget, not a delivered kit price. The [OSHWHub hardware project](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc) contains the PCB, schematic preview, BOM, enclosure files and an assembly video attachment; those are the files to consult for component footprints and wiring rather than an editorial block diagram.

![HachimoDock button mappings in desktop manager](https://image.lceda.cn/oshwhub/pullImage/49606595868244acbb1fd15502b6f2df.png)

*The management app allows physical controls to be remapped. This screenshot may represent an earlier UI revision.*

### From agent status display to a usable desktop tool

The software side is a **Tauri/React desktop client** with a bridge responsible for Agent sessions, speech recognition and USB messaging. Release builds are provided for Windows x64 and Apple-silicon Macs. The ESP32-P4 factory image includes the partition layout, default character and widget assets, not just the application executable. There are separate **v1 and v3 flashing packages** for different P4 revisions; mixing them is explicitly discouraged. A full flash can erase settings and media, whereas routine updates should use the desktop manager. The maintainer also notes that a Windows COM-port issue remains under investigation.

One particularly interesting feature is **PetUI**. Instead of hard-coding a permanently animated dog, the system lets a coding agent help create small tools or games—a Pomodoro timer, water reminder, task list, computer-status display or simple button-driven game. A bundled Skill generates component assets and interaction definitions, which the desktop manager validates against the 480 × 640 layout, device controls and memory limits before synchronization. Long-pressing the configured voice button starts input collection; the desktop performs ASR and routes a draft or message to the selected Agent, subject to its integration capabilities and confirmation flow. Speech services and generated character content require users to configure their own API credentials.

![HachimoDock voice input interface](https://image.lceda.cn/oshwhub/pullImage/0dddebc05c064f3a812d278b7c5dbe6e.png)

*Speech recognition and message routing run on the desktop. How text is submitted depends on the selected Agent integration.*

![PetUI component center and game preview](https://image.lceda.cn/oshwhub/pullImage/410d87c82a0049d483f58391c23c5c72.jpg)

*PetUI components are managed on the PC and transferred to the device rather than installed from a cloud app store.*

![Official HachimoDock animated Agent states](https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/assets/agent-status.gif)

*The official animated status sample shows how agent activity changes the character's behavior.*

<video controls playsinline preload="none" width="720"><source src="https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/pc/public/terrier-clips/working.thinking.mp4" type="video/mp4" />If the video does not load, open the animation file in the source repository.</video>

*An original “thinking” character animation asset—not a video of hardware assembly.*

<video controls playsinline preload="none" width="720"><source src="https://raw.githubusercontent.com/YizhengWw/HachimoDock/main/pc/public/terrier-clips/done.mp4" type="video/mp4" />If this video does not load, view the clip in the source repository.</video>

*The original “task completed” animation. An actual hardware assembly video is available from the [OSHWHub project attachments](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc).*

There is a Xiaomi connection beyond the event coverage. The desktop software includes **MiLoCo-based smart-home control**: once an authorized Xiaomi Home account is connected, supported devices can receive natural-language requests. The host performs that integration; the ESP32-P4 does not need to join the home network just to display Agent status. The MiLoCo implementation and associated materials have **separate Xiaomi license terms**, so compatibility should not be mistaken for unrestricted permission to distribute a commercial product.

That licensing distinction extends to HachimoDock itself. Despite having public source code, firmware and PCB documentation, the current GitHub project uses a **custom non-commercial, source-available license**, not GPL or MIT. Personal non-commercial builds and modifications are permitted within its terms; paid hardware, commercial integration and independent services require separate written permission. The older GPL-3.0 label still visible on the hardware-sharing page does not override the current [repository license](https://github.com/YizhengWw/HachimoDock/blob/main/LICENSE). For a hobby build, there is plenty to study: the firmware, the desktop bridge, the PCBs and the resource pipeline are all accessible. Just check the screen pinout and chip revision before committing to the parts list.

**Project links:** [Source and docs](https://github.com/YizhengWw/HachimoDock) · [PCB / schematic / BOM / assembly tutorial](https://oshwhub.com/eda_gqvzlprk/project_cnbmkbjc) · [Desktop and firmware releases](https://github.com/YizhengWw/HachimoDock/releases/latest) · [Flash and build instructions](https://github.com/YizhengWw/HachimoDock/blob/main/firmware/BUILD.md).
