---
title: "41 Hardware Projects Built with Codex: From Hacked Kindles to AI Robots"
description: "A close look at 41 builds in You Can Just Build Things: e-paper dashboards, ESP32 gadgets, voice agents, interactive art, cameras, robotics and more, with a link to every project."
locale: "en"
translationKey: "codex-hardware-41-projects-2026"
pubDate: "2026-11-03"
category: "hardware"
tags: ["Codex", "Hardware", "ESP32", "Raspberry Pi", "AI Agents", "Maker Projects"]
draft: false
seoTitle: "41 Codex Hardware Projects: ESP32, E-Paper, Robots and AI Gadgets"
seoDescription: "All 41 builds from You Can Just Build Things, with individual links, technical details, and a look at which are reproducible projects versus demos."
author: "EmbeddedNote"
sourceUrl: "https://youcanjustbuildthings.openai.chatgpt.site/"
---

A ten-year-old Kindle becomes an AI usage display. An ESP32 opens greenhouse curtains. Someone gives an insulin pen a clip-on magnifier; someone else turns a camera, a tiny robot arm or an old R2D2 toy into a programming project. Put them together and the common thread is not a single microcontroller or model. It is the decision to bring a coding agent into the messy business of making physical things work.

![41 Codex-assisted hardware builds](/uploads/codex-hardware-41-projects-2026/codex-41-hardware-cover.webp)

OpenAI's [You Can Just Build Things](https://youcanjustbuildthings.openai.chatgpt.site/) collects community submissions alongside a few official reference builds. **On November 3, 2026, the gallery showed 41 entries in its most-upvoted ordering.** This article follows that sequence and links to every project. The count refers to **gallery cards**, not 41 independently verified open-source kits. Some have source repositories and reproducible instructions; some are demonstration videos or early prototypes. Project Tabletop even appears in two different versions.

Several patterns emerge. ESP32 boards often do the close-to-the-hardware work—buttons, radios, displays and actuators—while Raspberry Pi systems tend to handle cameras, services and richer media. Elsewhere, makers use existing hardware rather than design another PCB: a Kindle, a projector, a compact camera or an aging robot. Voice agents keep turning into physical companions, but the hard problems are still latency, input, failure recovery and the boundary between a suggestion and a real-world action.

What follows separates the **features described by each maker** from the **engineering questions those features raise**. When the public listing does not identify a chip, publish source code, or supply performance figures, we do not fill in the gaps with guesses. This is a field guide to what people are trying, not a roundup of 41 certified products.

| Area | Entries | Main engineering interest |
|---|---:|---|
| Voice and physical AI interfaces | 11 | Speech, characters, tangible agent controls |
| Displays, cameras and imaging | 9 | E-paper, projection, multi-screen coordination |
| Games and interactive objects | 9 | Motion input, tactile controls, synchronized media |
| Robotics and automation | 8 | Actuation, protocols, sensing and feedback |
| Practical and accessibility tools | 4 | Assistive design, badges and PCB workflows |

## 01–10: From e-paper dashboards to portable voice agents

### 01. Kindle AI Usage Display

A decade-old Kindle becomes a low-power dashboard for AI usage across Codex, Claude Code, Cursor, Copilot and Gemini. A host machine collects usage and renders a monochrome image; the modified Kindle wakes roughly every six hours to download it and then sleeps again. The published build explains the jailbreak and FBInk display path, while the figures are API-equivalent estimates rather than the actual subscription bills.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8133b4dec277fe58e2c3e0a3bc317fa1a2e33b28e9035bba9bd2a73612241224) · [@kuberwastaken](https://x.com/kuberwastaken)

**Code:** [Kindle AI usage repository](https://github.com/Kuberwastaken/kindle-ai-usage) (check the project card for the current repository).

### 02. Insulin Pen Magnifier

A PETG clip-on magnifier designed to make the dose markings on an insulin pen easier to read. Codex helped with the mechanical design, and the adjustable lens height leaves room for fitting different pen shapes. This is an accessibility-oriented accessory, not an electronic dose checker; the gallery does not provide clinical performance or device-compatibility validation.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-06f376b224330ddcf07278b6132c5d1879c956c0a7951d12e97ecf2253d59a6e) · [@manfye](https://x.com/manfye)

### 03. Dream Logger

A bedside voice device for logging dreams. The maker describes a workflow that turns a spoken account into four illustrated scenes and files them on a calendar for later browsing. The useful design idea is the complete capture-to-archive interaction, rather than the novelty of image generation alone. The gallery does not specify a complete bill of materials or whether any model runs locally.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-76ded4f1a1107d49906050e4d5357c551916871062f47d2ef5f373c27271e2d8) · [@fedesarquis](https://x.com/fedesarquis)

### 04. Taz — Taskagotchi

Taz brings the Tamagotchi idea into a physical, voice-reactive companion. Its maker combines real-time speech interaction with hand-drawn pixel animations, so timing and expressive feedback matter as much as the conversation itself. The gallery identifies Codex as part of the build process but does not disclose the exact display or processor.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-03dbc72cda8b3d17c2e3b40a2708e8deb4b01d3183fbea3b64b55d1b8edfbaf4) · [@covacut](https://x.com/covacut)

### 05. Fovea

Fovea uses gaze to select context on a computer screen. The user looks at an area and speaks a request; the system gathers relevant text, screenshots and surrounding context. It is an interesting attempt to reduce the manual steps in multimodal assistance, though the listing does not identify the eye-tracking hardware or report measurement accuracy.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8287b1050903707504f8f371dc333a656e1e53444daee325b2b7a6afc23f3f6c) · [@maxjjiang](https://x.com/maxjjiang)

### 06. RICOH-GR-Live-View-Shooting

An M5Stack StickS3 mounted on a RICOH GR hot shoe acts as a wireless live-view screen and remote shutter. The listing names the GR II, III and IV. This is a useful example of pairing a compact display board with a camera-control interface; compatibility should still be checked against the firmware and camera model in the linked build.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-c2ac6e11f54cc9e37f847dda361f3ccefde2cecb6fc800bd6c0cbddc0619cf38) · [@tinker_zhang](https://x.com/tinker_zhang)

### 07. Dot gadgets for ChatGPT dots

An open-source MCP relay forwards short messages from a ChatGPT Dot to an ESP32 gadget with an LCD. The microcontroller does not need to run the agent itself; it handles the physical display while a bridge handles the messaging path. The value here is the separation between agent transport and constrained device UI, with service availability and configuration remaining prerequisites.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-c6afc93fd057c0d10413d4957eaa683df24ee480e9fda771f033bb470f8f2997) · [@deadbeef101010](https://x.com/deadbeef101010)

### 08. PixelTilt

PixelTilt is a handheld game built around a 64×64 LED panel, a motion sensor and a thumb wheel. Tilting supplies the primary control, while the wheel provides another physical input channel. For embedded developers, the design raises practical questions about motion filtering, LED refresh and ergonomics; the gallery does not publish a complete driver or battery specification.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-fa3ac3d72e2c4a57b08c8e88b955097a28e29e32860831d35544d27e0468a400) · [@abcdmku](https://x.com/abcdmku)

### 09. Cat TV

A Raspberry Pi sends cat-oriented scenes to a Samsung Freestyle projector and controls it over Wi-Fi. Rather than building another screen, the maker repurposes a consumer projector as an interactive environment for a pet. It is a neat integration of playback and device control, although the project card makes no claims about long-term animal behavior outcomes.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-b14cc8ab97aab9b9666fb63515262667de44741eb7bc92d54071095aaeafc2b4) · [@axbehr](https://x.com/axbehr)

### 10. Orbit Personal Voice Agent

Orbit is presented as a roughly $60 portable voice-assistant device. Wi-Fi connectivity and MCP integrations give it access to calendars, inboxes and home automation, making it a physical entry point into existing services. That figure is the maker’s stated device cost, not a verified retail price or a full assessment of ongoing cloud costs.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-25918ab207fee3b5c67caf252272b870ec0e8f0bd8ce6bbfadda36b431a97b77) · [@camdsmith](https://x.com/camdsmith)

## 11–20: Tangible agents, robots and automation

### 11. Bokko — my agent has a body

Bokko is a pendant linked by Bluetooth to a Hermes agent running on a Mac. Hold a button to issue a task, then read the reply on the pendant. Its design keeps the heavier agent work on the computer and uses the wearable as a lightweight input/output surface. Battery life and display specifications are not disclosed in the short listing.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-b0e263f85d614709197d92c3284492bc8dcf76b5466766a8aacefc059b0f4e00) · [@patiev_blog](https://x.com/patiev_blog)

### 12. MOSS the litter-picking robot

MOSS combines a tracked rover, a bin and a small arm with a parallel gripper. It is designed to pick up litter rather than simply drive around, which makes the interaction between locomotion, grasping and the collection bin central to the build. The public description is a maker-scale design, not evidence of a commercially validated autonomous sanitation robot.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-3e2447ee5941f35b9a4fb53fa3fb981cea41407d491c5f6349cfc4feebea5392) · [@metrox_eth](https://x.com/metrox_eth)

### 13. Casey’s NYC Ride

A handheld game inspired by Casey Neistat’s rides through New York City. It runs on a ModRetro Chromatic and uses mostly hand-illustrated artwork. The appeal is the way a personal visual theme is tailored to the constraints of a retro handheld, rather than a claim of a novel emulator or graphics engine. The short gallery entry does not document performance.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-790a05bb8708daa088f77c1db47bbd7aad7ba6ea9632038b6a9c6d8644e8c477) · [@covacut](https://x.com/covacut)

### 14. Realtime on ESP32

This Espressif-maintained WebRTC reference connects embedded hardware to the OpenAI Realtime API. It demonstrates real-time voice exchange and function calls that can control device behavior. Unlike a simple voice-chat demo, it exposes the practical boundary between audio hardware, transport and a remote model. It is a reference implementation, not a ready-to-ship smart speaker.

**Link:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/official-realtime-esp32)

**Reference implementation:** [Espressif esp-webrtc-solution](https://github.com/espressif/esp-webrtc-solution).

### 15. Living Art TV

Living Art TV turns personal artwork into a changing screensaver, adapting its visual story to the weather and time of day at home. The interesting idea is context-driven display content rather than a static photo loop. The project description does not specify the TV platform, generation model or offline behavior, so those aspects remain open questions.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-c574fd275e4ccfb259cbce73ba52630e94745e7dca0c20fa85b45569d4216851) · [@awkward_andyy](https://x.com/awkward_andyy)

### 16. Workout Coach x Codex Voice

A velocity sensor for weightlifting feeds a live Codex Voice coaching session. Rather than relying only on spoken descriptions of an exercise, the interaction is tied to measured movement speed. It is a compelling interface experiment, but the gallery does not publish the sensor model, calibration method or validation of its coaching recommendations.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-36218fe62a49fbc58d46d778c8c1b9e69b25f97cf607dcbc1fe63564b59dd8a2) · [@awkward_andyy](https://x.com/awkward_andyy)

### 17. Kinform: Give Objects Lore

Kinform gives everyday objects persistent characters, voices, memories and personalities using GPT Live. Its design goal is continuity: the object should feel like the same character on the next interaction, not a disposable one-shot chatbot. The listing shows the concept of physical presence but does not say that memory or speech processing is performed locally.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-2e8b5d907432e54a1615508b81e9638819eb074c14884294c2a2ebf13b8a75cc) · [@bonitadreama](https://x.com/bonitadreama)

### 18. Noutomation: Automate Your Way

Noutomation provides browser-configured rules for sensors, relays and Modbus devices. It targets the kind of farm or workshop automation where the logic changes more often than the wiring. The engineering value is a configurable I/O layer instead of one-off firmware for each control rule. No industrial safety certification should be inferred from the gallery entry.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-7794785a17c92e5b671a4505767ff4fca409e57eda52b974fd0019d5ca2af809) · [@masubo_bio](https://x.com/masubo_bio)

### 19. Multi screen infinite artwork

Multiple ESP32-based displays form a mesh so generative artwork appears to flow between screens. The composition changes about once a minute or when someone interacts with it. This is less about raw rendering power than coordinated state across nodes: timing, edge continuity and message delivery. The short description does not establish a maximum node count or measured synchronization accuracy.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-ac36c83a2196dfca18243bfb917c562bab91631a394510bf83c3bfedd897006b) · [@msurguy](https://x.com/msurguy)

### 20. Codex-Built Greenhouse Winder

A grower used Codex to build a greenhouse curtain winder around an ESP32, two 24 V motors and temperature feedback. It can be operated through LINE messages or temperature-based automation. The build shows AI-assisted development in a working farm setting, where motor protection, weather exposure and network failures matter as much as the app. The listing is not a substitute for safety or lifetime testing.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-e347d07c0cd0edd7a25bcfbae3fcfee78d86003917d2888d359eb167305ad1da) · [@tomiyasu16](https://x.com/tomiyasu16)

## 21–30: PCBs, cameras, projection and games

### 21. OpenAI inspired DEFCON badge

An ESP32 badge with lighting and an optional OLED, reportedly created with extensive assistance from an agent called Astra. The maker describes work spanning KiCad routing and JLCPCB ordering. It is a useful example of AI moving beyond writing firmware into PCB production workflow, while electrical-rule checking and manufacturability review remain human engineering responsibilities.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-d167331b94c63d3cd8a861f19bf92f785aa465001b95b96453565ac1701d3423) · [@aitelmax](https://x.com/aitelmax)

### 22. ImageGenCam

OpenAI’s buildable camera uses a Raspberry Pi Zero 2 W, Display HAT Mini, camera module, PiSugar battery board and printed enclosure. A photo is captured locally and sent for image generation, while a phone web app handles prompts and the album. The reference repository documents assembly and software setup, making it more reproducible than a gallery-only demo. Large image generation is a service call, not a model running on the Pi.

**Link:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/official-imagegencam)

**Source:** [openai/imagegencam](https://github.com/openai/imagegencam).

### 23. Reflect

Reflect was built at an OpenAI hackathon using an M5Stack CoreS3, the Realtime API and connected color lighting. Instead of another on-screen chat UI, it communicates through sound and changes in light. The public repository is explicit that this is a hackathon demo supplied as-is, making it a reference for interaction design rather than a certified consumer product.

**Link:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/official-reflect)

**Source:** [openai/openai-reflect](https://github.com/openai/openai-reflect).

### 24. FPGA Slot Machine

An FPGA-based slot-machine-style game with a custom 64×96 OLED interface, developed through a remote Vivado workflow while working from a Mac. The unusual part is the cross-platform FPGA toolchain: synthesis and device programming cannot always happen on the same host. The gallery supplies no basis for treating this as a regulated gambling product or specifying its randomization design.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-5bb2f0d7a1110b62c833006dc731576c3505620738668aff788625e504ead672) · [@itsarnz](https://x.com/itsarnz)

### 25. Project Tabletop

Project Tabletop turns a floor into an interactive football pitch with a projector and camera. Players move a physical marker to control on-screen vehicles against friends or a computer. Its notable trick is using vision to connect ordinary objects with projected graphics, avoiding electronics in every token. Tracking accuracy and lighting requirements are not specified in the gallery.

**Link:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-3ccbfc5367ce49fc8fc2fcfda105ccaf9711a8609f4db8beaa74addbecfc6abb)

### 26. El Tucu — Rent a Shell

El Tucu is a four-servo robotic arm offered for rent by the minute to people or AI agents. The builder describes Codex paying through x402 before moving the arm. It tests a provocative interface between digital payments and access to physical actuators, but the card does not imply advanced perception, autonomous grasping or industrial-grade motion control.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8ae093885312a273f1bcf61bf19f43c3c06013d58a6370f58bf456dbd88ba69c) · [@crypto_dev_1](https://x.com/crypto_dev_1)

### 27. Purble Palace — Built with Codex

A nostalgic recreation of Purble Palace for the ModRetro Chromatic handheld, made with help from Codex. Porting a desktop-style game to a small fixed-button device requires a different interface and presentation, even when the mechanics are familiar. The gallery does not establish exact feature parity with the original game.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-4c5c85dc0d18277ef4f93efd87ed3dfcca142f47eef2470b41a88149455edb6b) · [@haimantikam](https://x.com/haimantikam)

### 28. 62 BAR — Mini DJ Instrument

62 BAR is a Raspberry Pi-based mini DJ instrument with a motorized platter, touch display and physical controls. The maker credits Codex across CAD and firmware work as well as the overall assembly. It stands out because the interface is deliberately tactile rather than a software-only DJ deck; end-to-end audio latency and motor-control accuracy are not documented in the short listing.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-61f7edd92afacdf02d4f2ce9775bc6754d592451748cb2476cbd6725c03624b0) · [@eminimnim](https://x.com/eminimnim)

### 29. Hasselblad X2D: DOOM & Beyond

An unofficial exploration of the Hasselblad X2D using Codex: running DOOM, mapping the shutter button to fire, and experimenting with autofocus, pixel-shift capture and custom boot graphics. It is interesting as camera-firmware research and input repurposing, not as an official feature release. Firmware experiments can carry real recovery and warranty risks.

**Link:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-fb627402781dcf89f55b7d1bcf38395ded1bc29539cbd21281826a15bfed0f9e)

### 30. 512-LED Music-Reactive Cube

An 8×8×8 cube of 512 LEDs responds to nearby audio with patterns derived from FFT-based firmware. The builder mentions a custom PCB and hand assembly. A three-dimensional LED matrix makes driving, power distribution and physical alignment more involved than with an ordinary light strip, although brightness and power-consumption measurements are not provided in the gallery.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-eae7d60f950fbd72de230fca0a9421fe8b24080d2592d977a515c3b7bc27cbd6) · [@tttorynnn](https://x.com/tttorynnn)

## 31–41: Photo frames, hardware hacks and visual feedback

### 31. Keep — E-Paper Photo Frame

A personal e-paper photo frame built so the maker can send pictures from Edinburgh to a partner’s desk. The project is about a small, meaningful remote-display workflow rather than complex interaction: capture a photo, deliver it and show it persistently. The gallery does not specify the panel, transport protocol or battery life.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-0ddf7261982e37359f642e967431d4c2d0f15a42e52246b10dcc5894b9e8042a) · [@tarat_211](https://x.com/tarat_211)

### 32. Watch Kaleidoscope

A pocket kaleidoscope on an M5Stack watch. Tilt or swipe and simulated glass fragments tumble, collide and produce little sound cues. It brings motion input, simple physics and audio feedback together on a very small screen. The short description does not identify the rendering engine or display driver.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-3f2cb8bdf24e11f6f8c3a86872e376303f91f4695f88d15d07cae36ad49a1041) · [@realtr2e](https://x.com/realtr2e)

### 33. Hands-On AI: ESP32 iPhone Agent

The maker presents an ESP32-S3-based bridge that lets an AI observe and control a real iPhone, claiming no jailbreak, Mac or cable is needed. Screen mirroring and Bluetooth touch input are the advertised pieces. It is an ambitious bridge between perception and physical-device interaction, but the claim should not be generalized to every iOS version or permission state.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-aad932dd2f447aaa8122d47132efca6bf5913f3d5089b2e2f99997adb69f76ea) · [@iamhenryyuan](https://x.com/iamhenryyuan)

### 34. Robbi: Your Emotional AI Companion

Robbi is a small companion robot made with a Raspberry Pi, printed parts and Codex-assisted development. It combines voice, vision, memory and expressive behavior in an attempt to give the object a recognizable personality. The gallery makes it a promising interaction prototype, not evidence of a fully documented production hardware stack.

**Link:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-740858b4fae95982b3ebe82974f3a454bf1f0c568cc2fc8b1b886db1ac207d2e)

### 35. Greenhouse Robot Prototype

A greenhouse robotics prototype intended to make greenhouse operations more efficient through perception, autonomy and actuation. At this stage the showcase description is intentionally high-level. It does not identify the base platform, sensors or navigation algorithm, and should not be described as a validated harvesting robot.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-e03ad8c797ef36ff013b54b727c1e7e4de0b189cd40ebbf6e7bb634c1528b302) · [@ihwylie](https://x.com/ihwylie)

### 36. Ricoh GR IV: Beyond Stock

An exploration of RICOH GR IV firmware that includes a customized power-off screen and model-specific research scripts. Its contribution is targeted tooling for investigating a closed consumer device, rather than proof of general-purpose firmware control. Backups, recovery access and warranty considerations matter before reproducing these experiments.

**Link:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8f79d3b2973c34d916db32d50143ead2ab5a86eb8641dcfe1cb72df8c6496467)

### 37. Project Tabletop (v1.3)

A later Tabletop entry expands the camera-and-projector idea into an interactive desk. Physical markers can steer arcade play, support drawing and help explore a projected globe. It belongs to the same broader project family as the earlier floor-football entry, so two gallery cards should not automatically be counted as two independent software platforms.

**Link:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-16072b5be9929c4cf63781d83a8f447919a487bbcaff1cdd9b1d475239c54fc2)

### 38. Nikko R2D2 Modern OS App

An attempt to build a modern Windows application for an older Nikko R2D2 remote-controlled webcam robot. The challenge is largely compatibility: recovering usable control of aging hardware when the original software no longer fits current operating systems. The listing calls it an attempt, not a verified full restoration of every original feature.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-d24ce5b5d0eaab1154d5979941696fc50f4008beb4765cb69af5982a77c2e717) · [@pablopoo](https://x.com/pablopoo)

### 39. Project Piko

Project Piko turns a Raspberry Pi into a conversational personal assistant that can receive tasks and help manage a Linux machine. This shifts the device from passive Q&A into system administration. Permission boundaries and command auditing are important engineering considerations, although the short project card does not document its privilege model.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-0a9ce28248c654130b4ae0e4f80894f93243bfe5e623bc3756e445d839fd1ce5) · [@blackie_360](https://x.com/blackie_360)

### 40. Codex Pet Badge

An interactive M5Stack badge with tilt, shake and touch reactions, a battery indicator and a LinkedIn QR code. It extends the conventional conference badge with a small digital-pet interaction, blending identity display and playful controls. The gallery does not specify the exact M5Stack model or a complete contact-sharing protocol.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-15b148cc94a3ce050e840a5302e1824396ae5cb2892d9e60ce04a435f8fb5070) · [@naveenmanwani17](https://x.com/naveenmanwani17)

### 41. AC Remote with Visual Feedback

A Raspberry Pi 5-based air-conditioner controller combines an iPhone interface, infrared commands and a camera check of the unit’s flap position. The closed-loop element matters: instead of assuming a transmitted IR command worked, the system tries to observe the result. Supported air-conditioner models and vision reliability are not fully documented in the public card.

**Links:** [Project card](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-edea2dffa1a7b0152eaa552435b98b5681a257a5f2b6dfda1ceba433217901dd) · [@swhan0329](https://x.com/swhan0329)

## What is worth borrowing from these builds

The strongest projects begin with a problem that has a measurable state and a clear physical response. A greenhouse motor has to move a curtain; an e-paper dashboard needs a reliable refresh schedule; a camera remote has to trigger a shutter; an air-conditioner controller should check whether the vent actually moved. Those are good problems for AI-assisted engineering because success can be observed and tested. A chatbot in a box is not a complete product specification.

Nor does a coding agent remove the less glamorous work. Power design, mechanics, optics, motor safety, update recovery and firmware compatibility still require engineering judgment. AI tools can help write drivers, inspect documentation and shorten the path between a prototype and a test. Whether a reader can reproduce a particular build depends on what its maker has actually released: code, mechanical files, a bill of materials, licensing and revision information. A compelling video and a maintainable project repository are not interchangeable.

**Sources and scope:** [You Can Just Build Things gallery](https://youcanjustbuildthings.openai.chatgpt.site/) (snapshot reviewed November 3, 2026); [Kindle project detail](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8133b4dec277fe58e2c3e0a3bc317fa1a2e33b28e9035bba9bd2a73612241224); [ImageGenCam repository](https://github.com/openai/imagegencam); [Reflect repository](https://github.com/openai/openai-reflect); and [Espressif's WebRTC solution](https://github.com/espressif/esp-webrtc-solution). Listings, votes and ordering can change. Each entry above links to its own source card; claims that require unpublished design files or performance data have deliberately been left open.
