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

A decade-old Kindle now displays AI usage instead of books. A maker has clipped a height-adjustable magnifier onto an insulin pen, while another has fitted a tiny M5Stack viewfinder to the hot shoe of a Ricoh GR camera. Further down the gallery are a tracked litter-picking robot, greenhouse curtains controlled by an ESP32 and a voice-agent pendant you can wear. The projects have little else in common, but each maker used Codex somewhere in the build.

OpenAI has collected them at You Can Just Build Things. On November 3, 2026, the most-upvoted view contained 41 entries. Some builders shared code and build notes; others showed a finished object or an early prototype. An interactive projector game appears in two versions. We follow the gallery's order, with a photograph from the corresponding submission under each entry. Click any photograph to open the maker's page. These are 41 showcased projects, not 41 independently tested open-hardware designs.

Links:

https://youcanjustbuildthings.openai.chatgpt.site/

https://embeddednote.com/en/articles/codex-hardware-41-projects-2026/

## 01–10: From e-paper dashboards to portable voice assistants

### 01. Kindle AI Usage Display

A Kindle that's roughly ten years old is repurposed as an always-on AI usage dashboard. It brings together usage from Codex, Claude Code, Cursor, Copilot and Gemini, showing monthly totals, estimated spending and the share attributable to each tool. About every six hours the Kindle connects to fetch a new image, refreshes its e-paper screen and goes back to sleep. The build uses a jailbroken Kindle, FBInk for drawing, a Node.js data service and scheduled collection. It's a good example of giving aging e-paper hardware a second job.

[![AI usage dashboard on a Kindle e-paper display](/uploads/codex-hardware-41-projects-2026/official-01.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8133b4dec277fe58e2c3e0a3bc317fa1a2e33b28e9035bba9bd2a73612241224)

Creator @kuberwastaken

Code: kindle-ai-usage repository (refer to the project page for the current source location).

### 02. Insulin Pen Magnifier

This clip-on magnifier makes the dose numbers on an insulin pen easier to read. The maker used Codex during the design process and printed the attachment in PETG, with an adjustable lens height to accommodate different pens and viewing distances. Fitting the clip securely and keeping the numbers in focus matter more here than adding electronics. It is a visual aid, not a device that checks or dispenses insulin doses; the listing provides no clinical validation.

[![Pink clip-on magnifier fitted to an insulin pen](/uploads/codex-hardware-41-projects-2026/official-02.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-06f376b224330ddcf07278b6132c5d1879c956c0a7951d12e97ecf2253d59a6e)

Creator @manfye

### 03. Dream Logger

Dream Logger sits by the bed and records a dream as soon as its owner wakes up. A spoken account becomes four illustrated scenes, saved to a calendar for later review. Voice capture, image generation and a browsable timeline are joined into one physical routine. The listing does not identify the complete microphone, processor or model setup, so there is no basis for claiming that it works offline.

[![Handheld Dream Logger with its illustrated display](/uploads/codex-hardware-41-projects-2026/official-03.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-76ded4f1a1107d49906050e4d5357c551916871062f47d2ef5f373c27271e2d8)

Creator @fedesarquis

### 04. Taz — Taskagotchi

Taz is a physical digital pet whose expressions and movements respond to live voice interaction. Its character animations are hand-drawn pixel art. On a small display, the timing between speech, the system's reply and the on-screen reaction does much of the work of making a character feel responsive. The public description does not name the processor or display.

[![Taz pixel-art companion in a transparent enclosure](/uploads/codex-hardware-41-projects-2026/official-04.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-03dbc72cda8b3d17c2e3b40a2708e8deb4b01d3183fbea3b64b55d1b8edfbaf4)

Creator @covacut

### 05. Fovea

Fovea uses gaze as a pointer. Look at a region of the screen and say what you want to do; the system collects relevant text, screenshots and surrounding context. The aim is to replace the routine of capturing a screenshot and pasting it into a chat with a more direct combination of eye tracking and spoken intent. The listing does not identify the eye tracker or report measured recognition accuracy.

[![Fovea dual-camera gaze-tracking device](/uploads/codex-hardware-41-projects-2026/official-05.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8287b1050903707504f8f371dc333a656e1e53444daee325b2b7a6afc23f3f6c)

Creator @maxjjiang

### 06. RICOH-GR-Live-View-Shooting

An M5Stack StickS3 mounted in a RICOH GR hot shoe becomes a miniature wireless live-view monitor and remote shutter release. The maker lists the GR II, GR III and GR IV. Combining preview, shutter control and a tiny screen in one accessory is particularly interesting for anyone exploring camera control protocols. Support for a particular camera model still needs to be checked against the maker's firmware release.

[![M5Stack wireless viewfinder alongside a Ricoh GR camera](/uploads/codex-hardware-41-projects-2026/official-06.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-c2ac6e11f54cc9e37f847dda361f3ccefde2cecb6fc800bd6c0cbddc0619cf38)

Creator @tinker_zhang

### 07. Dot gadgets for ChatGPT dots

This small ESP32 display receives short messages from a ChatGPT Dot through an open-source MCP relay. Network services and message routing stay separate from the LCD endpoint, so the microcontroller only handles the compact information it needs to show. It's a useful pattern for passing agent output to a physical display without attempting to run a language model on the ESP32. The setup depends on the relevant Dot service and relay configuration.

[![Compact ESP32 LCD showing an alert](/uploads/codex-hardware-41-projects-2026/official-07.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-c6afc93fd057c0d10413d4957eaa683df24ee480e9fda771f033bb470f8f2997)

Creator @deadbeef101010

### 08. PixelTilt

PixelTilt packs a 64 × 64 LED panel, a motion sensor and a side-mounted thumb wheel into a handheld game. Tilting the device changes the game state; the wheel provides finer control. The hardware concept is simple, but convincing play depends on motion filtering, smooth animation and input feel. The listing does not document the LED driver architecture or battery runtime.

[![PixelTilt LED handheld game menu](/uploads/codex-hardware-41-projects-2026/official-08.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-fa3ac3d72e2c4a57b08c8e88b955097a28e29e32860831d35544d27e0468a400)

Creator @abcdmku

### 09. Cat TV

A Raspberry Pi feeds cat-friendly moving scenes to a Samsung Freestyle projector and controls the projector over Wi-Fi. 'Cat TV' is not a dedicated screen; it turns an existing projector into a changing play environment. The project brings device-control APIs and media together. The demo is not evidence of a measured long-term effect on animal behavior.

[![Cat interacting with projected colored shapes](/uploads/codex-hardware-41-projects-2026/official-09.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-b14cc8ab97aab9b9666fb63515262667de44741eb7bc92d54071095aaeafc2b4)

Creator @axbehr

### 10. Orbit Personal Voice Agent

Orbit is a portable voice assistant described by its maker as roughly $60 in hardware. It connects over Wi-Fi and reaches calendars, email inboxes and home automation through MCP services. The design is about giving several personal services one voice interface, not training a model on the device. The $60 figure is the maker's stated hardware estimate, not an independently costed retail price.

[![Orbit portable voice assistant held in one hand](/uploads/codex-hardware-41-projects-2026/official-10.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-25918ab207fee3b5c67caf252272b870ec0e8f0bd8ce6bbfadda36b431a97b77)

Creator @camdsmith

## 11–20: Agents with hardware, robots and automation

### 11. Bokko — my agent has a body

Bokko is a small pendant paired over Bluetooth with a Hermes agent running on a Mac. Hold a button, speak a task and read the result on the pendant after the computer processes it. That gives the wearer a practical input–processing–feedback loop while keeping the heavier computing work on the Mac. The project card does not publish a verified battery runtime or a complete screen specification.

[![Bokko agent pendant showing a message](/uploads/codex-hardware-41-projects-2026/official-11.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-b0e263f85d614709197d92c3284492bc8dcf76b5466766a8aacefc059b0f4e00)

Creator @patiev_blog

### 12. MOSS the litter-picking robot

MOSS is a small tracked rover intended for printing and assembly at home. A bin sits on the chassis, and an arm with a parallel gripper handles objects. Moving, picking up litter and placing it in the bin are separate control problems that must work together. The maker shares a design and build direction, but the prototype demonstration should not be mistaken for a validated autonomous waste-sorting machine.

[![MOSS tracked robot with a gripper arm and bin](/uploads/codex-hardware-41-projects-2026/official-12.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-3e2447ee5941f35b9a4fb53fa3fb981cea41407d491c5f6349cfc4feebea5392)

Creator @metrox_eth

### 13. Casey’s NYC Ride

Casey's NYC Ride is a handheld game inspired by footage of rides through New York City. It runs on the ModRetro Chromatic, with most of the artwork drawn by hand. The distinctive part is the translation of a personal city experience into a game on retro handheld hardware, rather than a generic Game Boy emulator. The public card offers no game-engine details or performance measurements.

[![Cycling game running on a ModRetro Chromatic handheld](/uploads/codex-hardware-41-projects-2026/official-13.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-790a05bb8708daa088f77c1db47bbd7aad7ba6ea9632038b6a9c6d8644e8c477)

Creator @covacut

### 14. Realtime on ESP32

Espressif maintains this WebRTC reference demo for connecting an embedded voice device to the OpenAI Realtime API and triggering device functions by voice. It is a source-backed engineering example, not a finished consumer speaker. A working implementation must account for audio capture and playback on the device, the WebRTC session, the cloud service, API credentials and network failures.

[![Espressif ESP32 voice development board](/uploads/codex-hardware-41-projects-2026/official-14.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/official-realtime-esp32)

Reference implementation: Espressif esp-webrtc-solution.

### 15. Living Art TV

Living Art TV turns the owner's artwork into an evolving screensaver that responds to the day's weather and time. Unlike a fixed slideshow, the scenes change as those inputs change. The card does not say which TV platform or generative model it uses, or whether it can operate offline, so the available information is primarily about the experience rather than a reproducible implementation.

[![Generative artwork displayed on a television](/uploads/codex-hardware-41-projects-2026/official-15.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-c574fd275e4ccfb259cbce73ba52630e94745e7dca0c20fa85b45569d4216851)

Creator @awkward_andyy

### 16. Workout Coach x Codex Voice

A velocity sensor attached to weightlifting equipment feeds movement data into Codex Voice, allowing spoken feedback during a set. Using a measured physical signal gives the conversation more context than a description supplied by the lifter alone. The project listing does not name the sensor, explain calibration or provide evidence that the coaching improves training outcomes.

[![Velocity sensor attached to weightlifting equipment](/uploads/codex-hardware-41-projects-2026/official-16.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-36218fe62a49fbc58d46d778c8c1b9e69b25f97cf607dcbc1fe63564b59dd8a2)

Creator @awkward_andyy

### 17. Kinform: Give Objects Lore

Kinform gives an everyday object a continuing AI character, complete with a voice, personality and memories, using GPT Live. The goal is to make inexpensive physical objects feel like distinct companions whose identity persists across conversations. The description does not establish that memories are stored locally, and it leaves the privacy design unspecified.

[![Kinform connected object beside its phone settings screen](/uploads/codex-hardware-41-projects-2026/official-17.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-2e8b5d907432e54a1615508b81e9638819eb074c14884294c2a2ebf13b8a75cc)

Creator @bonitadreama

### 18. Noutomation: Automate Your Way

Noutomation lets users configure sensor readings, relay actions and Modbus device control from a browser instead of reflashing firmware every time a rule changes. That is a practical approach for farms and workshops with mixed equipment and frequently adjusted processes. The emphasis is on bringing I/O and rule configuration into one interface. The public listing does not establish industrial safety certification or suitability as a safety-rated PLC replacement.

[![Noutomation control hardware and wiring](/uploads/codex-hardware-41-projects-2026/official-18.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-7794785a17c92e5b671a4505767ff4fca409e57eda52b974fd0019d5ca2af809)

Creator @masubo_bio

### 19. Multi screen infinite artwork

Several ESP32-based screens form a mesh network through which generative artwork flows from one display to the next. The visuals change approximately once a minute and can also react to human interaction. It is more than playing a video on one screen: frame boundaries, timing between nodes and network messages all have to line up. The maker does not provide a measured synchronization error or maximum node count.

[![Generative art spread across several handheld screens](/uploads/codex-hardware-41-projects-2026/official-19.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-ac36c83a2196dfca18243bfb917c562bab91631a394510bf83c3bfedd897006b)

Creator @msurguy

### 20. Codex-Built Greenhouse Winder

A farmer used an ESP32, two 24 V motors and temperature sensing to automate greenhouse ventilation curtains. The curtains can be controlled through LINE messages or moved automatically in response to temperature. This is real outdoor equipment, where stalled motors, weather exposure and lost connectivity matter. The public demonstration does not include a complete safety design or endurance-test record.

[![Greenhouse motor controller wiring inside an enclosure](/uploads/codex-hardware-41-projects-2026/official-20.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-e347d07c0cd0edd7a25bcfbae3fcfee78d86003917d2888d359eb167305ad1da)

Creator @tomiyasu16

## 21–30: PCBs, cameras, projection and games

### 21. OpenAI inspired DEFCON badge

This ESP32 DEFCON badge lights up and can optionally carry an OLED. Its maker says Astra assisted with the workflow from KiCad PCB routing through placing an order with JLCPCB. The interesting test here is whether AI assistance can carry useful design information across CAD, fabrication outputs and manufacturing steps. Electrical-rule checks and production constraints still need human review; independent manufacturing validation is not provided.

[![Custom ESP32 DEFCON badge PCB design](/uploads/codex-hardware-41-projects-2026/official-21.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-d167331b94c63d3cd8a861f19bf92f785aa465001b95b96453565ac1701d3423)

Creator @aitelmax

### 22. ImageGenCam

ImageGenCam is a weekend camera build with published OpenAI source code. A Raspberry Pi Zero 2 W, Display HAT Mini, camera, PiSugar power supply and 3D-printed shell make up the handheld device. Pressing the shutter starts an image-generation workflow; a phone-accessible web interface handles photos and prompts. Capture, background processing and the phone UI have distinct jobs. The large image model does not run on the Pi.

[![Raspberry Pi and other components for ImageGenCam](/uploads/codex-hardware-41-projects-2026/official-22.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/official-imagegencam)

Source code: openai/imagegencam。

### 23. Reflect

Reflect began as an OpenAI hackathon experiment using an M5Stack CoreS3, the Realtime API and smart lighting. Instead of leaning on a conventional chat display, it uses voice, color and lighting rhythms to respond. The project repository describes it as an experimental demo without comprehensive reliability or security review. It's a prototype to learn from, not a production-ready appliance.

[![Reflect interactive device with illuminated screen](/uploads/codex-hardware-41-projects-2026/official-23.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/official-reflect)

Source code: openai/openai-reflect。

### 24. FPGA Slot Machine

This FPGA slot-machine-style demo was developed by running Vivado in a remote Windows environment from a Mac. A custom 64 × 96 OLED presents the interface. Beyond the game itself, it demonstrates a cross-platform FPGA workflow, from remote synthesis to output on the device. The public description does not specify its random-number mechanism, and it should not be treated as a gambling product.

[![FPGA slot machine demonstration and toolchain](/uploads/codex-hardware-41-projects-2026/official-24.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-5bb2f0d7a1110b62c833006dc731576c3505620738668aff788625e504ead672)

Creator @itsarnz

### 25. Project Tabletop

A projector and camera turn a floor into a virtual soccer field. Players move physical markers to steer vehicles and compete with friends or the computer. The camera tracks the markers while the projector supplies the changing scene, so each game piece does not need its own radio or processor. The concept combines computer vision with spatial display, but the listing gives no tracking-accuracy or ambient-light specifications.

[![Interactive projected soccer field](/uploads/codex-hardware-41-projects-2026/official-25.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-3ccbfc5367ce49fc8fc2fcfda105ccaf9711a8609f4db8beaa74addbecfc6abb)

### 26. El Tucu — Rent a Shell

El Tucu is a small four-servo robot arm that people—or AI agents—can rent by the minute. In the maker's demonstration, Codex uses an x402 payment to access the arm, linking task requests, payment and physical movement. The experiment is about machine-mediated access to hardware services, not proof of advanced autonomous grasping.

[![Four-servo El Tucu robot arm](/uploads/codex-hardware-41-projects-2026/official-26.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8ae093885312a273f1bcf61bf19f43c3c06013d58a6370f58bf456dbd88ba69c)

Creator @crypto_dev_1

### 27. Purble Palace — Built with Codex

Motivated by nostalgia for older PC games, the maker used Codex to build a Purble Palace-style game for the ModRetro Chromatic. The work is in fitting a desktop interaction to a small handheld display and physical buttons, not adding sensors. The gallery provides too little detail to judge how faithfully the original game's features have been reproduced.

[![Retro game running on a ModRetro Chromatic handheld](/uploads/codex-hardware-41-projects-2026/official-27.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-4c5c85dc0d18277ef4f93efd87ed3dfcca142f47eef2470b41a88149455edb6b)

Creator @haimantikam

### 28. 62 BAR — Mini DJ Instrument

62 BAR is a Raspberry Pi-based miniature DJ instrument with a motorized platter, touchscreen, physical controls and a custom enclosure. Its maker used Codex across CAD, firmware and mechanical assembly. What makes it different from a music player is the tactile control surface. Complete measurements of audio latency or motor-control accuracy have not been published in the project listing.

[![CAD view of the 62 BAR mini DJ instrument](/uploads/codex-hardware-41-projects-2026/official-28.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-61f7edd92afacdf02d4f2ce9775bc6754d592451748cb2476cbd6725c03624b0)

Source: project page · Creator @eminimnim

### 29. Hasselblad X2D: DOOM & Beyond

Codex helped explore unofficial capabilities on a Hasselblad X2D, including running DOOM and using the shutter release as the fire button. The maker also experiments with autofocus, pixel-shift capture and custom startup graphics. This is firmware research and a creative reuse of a camera's controls, not a list of supported factory features. Such changes can affect reliability and warranty coverage; the public material does not establish a safe flashing procedure.

[![DOOM running on a Hasselblad X2D camera](/uploads/codex-hardware-41-projects-2026/official-29.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-fb627402781dcf89f55b7d1bcf38395ded1bc29539cbd21281826a15bfed0f9e)

### 30. 512-LED Music-Reactive Cube

An 8 × 8 × 8 array of 512 LEDs turns nearby sound into three-dimensional patterns using FFT-based analysis. The maker describes a custom PCB, hand-soldered LED assembly and dedicated spectrum-processing firmware. Compared with a two-dimensional strip, the cube adds scanning, voltage-drop and physical alignment challenges. Measured brightness and power consumption are not supplied.

[![Three-dimensional array of 512 illuminated LEDs](/uploads/codex-hardware-41-projects-2026/official-30.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-eae7d60f950fbd72de230fca0a9421fe8b24080d2592d977a515c3b7bc27cbd6)

Creator @tttorynnn

## 31–41: Photo frames, hardware hacks and visual feedback

### 31. Keep — E-Paper Photo Frame

Keep is an e-paper photo frame made as a gift for the maker's fiancée. Photos taken in Edinburgh can be sent to the screen on her desk, creating a simple chain from the camera through a network service to a low-power display. The gallery focuses on the personal use case and gives no panel model, transport protocol or standby-time figure.

[![E-paper photo frame showing a shared photograph](/uploads/codex-hardware-41-projects-2026/official-31.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-0ddf7261982e37359f642e967431d4c2d0f15a42e52246b10dcc5894b9e8042a)

Creator @tarat_211

### 32. Watch Kaleidoscope

This M5Stack watch becomes a pocket kaleidoscope. Tilt or swipe and glass-like shapes tumble, collide and make sounds under a physics simulation. Rendering, inertial input and audio feedback all have to fit on a small screen. The listing does not identify the graphics engine or display driver.

[![Kaleidoscope artwork on an M5Stack watch](/uploads/codex-hardware-41-projects-2026/official-32.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-3f2cb8bdf24e11f6f8c3a86872e376303f91f4695f88d15d07cae36ad49a1041)

Creator @realtr2e

### 33. Hands-On AI: ESP32 iPhone Agent

The maker claims a tiny ESP32-S3 board lets an AI agent observe and operate a real iPhone without jailbreaking, a Mac or a cable. Wireless screen mirroring and Bluetooth touch input are the stated ingredients. The engineering question is how screen capture and HID-style input are paired, but the demo does not establish reliable support across iOS versions or imply that operating-system authorization can be bypassed.

[![Compact ESP32-S3 iPhone agent device](/uploads/codex-hardware-41-projects-2026/official-33.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-aad932dd2f447aaa8122d47132efca6bf5913f3d5089b2e2f99997adb69f76ea)

Creator @iamhenryyuan

### 34. Robbi: Your Emotional AI Companion

Robbi is a Raspberry Pi-powered desktop robot with 3D-printed parts. Voice, vision, memory and expressive responses give it a character beyond a standard question-and-answer speaker. Its physical form is part of the interaction. The card does not include a complete hardware bill of materials or long-term reliability data, making it best read as an interaction prototype.

[![Robbi companion robot in a demonstration video](/uploads/codex-hardware-41-projects-2026/official-34.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-740858b4fae95982b3ebe82974f3a454bf1f0c568cc2fc8b1b886db1ac207d2e)

### 35. Greenhouse Robot Prototype

This greenhouse robot is an early prototype intended to combine environmental sensing, decision-making and actuation to improve greenhouse work. The listing outlines that ambition without specifying the mobile base, sensors or navigation algorithms. It would be premature to describe capabilities such as autonomous harvesting or precise localization that the maker has not demonstrated.

[![Greenhouse robot prototype](/uploads/codex-hardware-41-projects-2026/official-35.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-e03ad8c797ef36ff013b54b727c1e7e4de0b189cd40ebbf6e7bb634c1528b302)

Creator @ihwylie

### 36. Ricoh GR IV: Beyond Stock

The Ricoh GR IV project explores unofficial camera firmware modifications. The maker has demonstrated a custom shutdown screen and published scripts aimed at the model. This is limited, reproducible work on a closed consumer device—not evidence of complete firmware control. Backups, recovery options and warranty restrictions should be considered before experimenting.

[![Modified screen on a Ricoh GR IV camera](/uploads/codex-hardware-41-projects-2026/official-36.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-8f79d3b2973c34d916db32d50143ead2ab5a86eb8641dcfe1cb72df8c6496467)

### 37. Project Tabletop (v1.3)

Project Tabletop v1.3 develops the same camera-and-projector interaction into a tabletop playground. The projector draws the scene and a camera recognizes physical markers; the maker demonstrates arcade-style games, drawing and exploring the globe. It is a separate gallery entry from the earlier floor-soccer build, but appears related rather than an entirely different platform. A complete version changelog is not available.

[![Project Tabletop projected interactive scene](/uploads/codex-hardware-41-projects-2026/official-37.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-16072b5be9929c4cf63781d83a8f447919a487bbcaff1cdd9b1d475239c54fc2)

### 38. Nikko R2D2 Modern OS App

The aim is to build a Windows application capable of controlling an older Nikko R2D2 remote-control and network-camera robot. Much of the work concerns restoring protocol and driver compatibility as operating systems change. Hardware that still works need not be discarded simply because its original software has aged. The gallery describes an attempt; it does not confirm that every feature has been recovered.

[![Nikko R2D2 robot beside a laptop](/uploads/codex-hardware-41-projects-2026/official-38.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-d24ce5b5d0eaab1154d5979941696fc50f4008beb4765cb69af5982a77c2e717)

Creator @pablopoo

### 39. Project Piko

Project Piko turns a Raspberry Pi into a conversational personal assistant that can take tasks and help manage a Linux computer. It is closer to a physical entry point for a system-administration agent than a speaker that reads the weather. That level of access calls for restricted command permissions and clear activity logs; the public description does not explain how the project isolates privileges.

[![Project Piko Raspberry Pi AI assistant display](/uploads/codex-hardware-41-projects-2026/official-39.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-0a9ce28248c654130b4ae0e4f80894f93243bfe5e623bc3756e445d839fd1ce5)

Creator @blackie_360

### 40. Codex Pet Badge

This interactive M5Stack badge responds to tilts, shakes and touch, displays battery status and can bring up the maker's LinkedIn QR code. It turns a conference badge into a small animated gadget, sharing hardware between playful input and identity display. The specific M5Stack model is not identified, and the listing does not describe a full wireless digital-business-card system.

[![Codex interactive pet badge](/uploads/codex-hardware-41-projects-2026/official-40.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-15b148cc94a3ce050e840a5302e1824396ae5cb2892d9e60ce04a435f8fb5070)

Creator @naveenmanwani17

### 41. AC Remote with Visual Feedback

A Raspberry Pi 5 and an iPhone interface control an air conditioner over infrared. After a command is sent, an AI-assisted camera checks the position of the unit's airflow flap. That closes the loop in a way an ordinary IR remote cannot: there is an attempt to verify that the unit responded. Supported AC models, recognition accuracy and safety interlocks are not fully documented, so compatibility should not be assumed.

[![Air-conditioner on-off interface with camera feedback](/uploads/codex-hardware-41-projects-2026/official-41.webp)](https://youcanjustbuildthings.openai.chatgpt.site/projects/submission-edea2dffa1a7b0152eaa552435b98b5681a257a5f2b6dfda1ceba433217901dd)

Creator @swhan0329

Across the 41 entries, the most convincing starting points are small problems with something you can measure, control and check. A greenhouse curtain has a temperature reading and a motor position; a Kindle has a known refresh cycle; a camera needs a shutter that actually fires; an air-conditioner remote ought to check whether the vent moved. A clear physical feedback loop is often a better first hardware project than a box built solely to host an AI chat interface.

Coding agents do not make analog circuits, power supplies, optics, thermal design or mechanical tolerances disappear. They can help write drivers, organize tests, search documentation, build interfaces and even assist with PCB work. Someone still has to verify motor stops, camera recovery paths and the fit of a medical-accessibility attachment. Before attempting any of these builds, check the individual project for available code, BOMs, licenses and hardware revisions.

For more embedded engineering projects, follow the Embedded Notes WeChat account. Feedback and comments are always welcome.
