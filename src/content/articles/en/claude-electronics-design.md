---
locale: en
translationKey: claude-electronics-design
pubDate: '2026-11-11'
updatedDate: '2026-11-11'
category: hardware
draft: false
contentType: deep
series: ai-hardware
author: EmbeddedNote
sourceUrl: https://www.anthropic.com/research/claude-electronics-design
title: 'Claude Fable 5.2 Designed Three Devices From a Prompt. The PCBs Are the Interesting Part.'
description: 'Anthropic says Claude Fable 5.2 designed a USB speakerphone, a voice hub and a handheld pet, including PCBs, firmware and enclosures. Here is what was shown, and what was not tested.'
tags:
- Claude
- Anthropic
- AI Hardware
- PCB Design
- KiCad
- DFM
- Prototyping
- CAD
seoTitle: 'Claude Fable 5.2: AI PCB Design From Prompt to Prototype'
seoDescription: 'Anthropic’s Claude Fable 5.2 designed three devices, including PCBs, enclosures and firmware. A close look at the routing, DFM checks and unverified claims.'
---

Anthropic’s latest electronics demo is easy to summarize and easy to overread. The company gave Claude Fable 5.2 a short prompt for three devices — a USB-C speakerphone, a home voice-assistant hub and a battery-powered handheld pet — and the model produced specifications, schematics, PCB layouts, enclosure CAD, firmware and a parts list. Diode Computers built the boards, assembled the units and ran the firmware. According to [Anthropic’s research note](https://www.anthropic.com/research/claude-electronics-design), all three were still working, and the speakerphone had been running for weeks.

That is a real step beyond “the model can write Arduino code.” It is not proof that a model can replace a hardware team. The useful question is narrower: how much of the design work did Claude actually do, where did it still need people, and what does the published material let an outside engineer verify?

[![Anthropic Claude electronics design demo video poster](/uploads/claude-electronics/claude-electronics-video-poster.webp)](https://www.anthropic.com/research/claude-electronics-design)

*Anthropic’s demo video is embedded in the research note; click the poster to watch it there.*

![Three electronic prototypes designed by Claude: a handheld pet, a voice-assistant hub and a USB speakerphone](/uploads/claude-electronics/claude-electronics-hero.webp)

*Three devices built from Claude’s designs: a battery-powered handheld pet, a home voice-assistant hub and a USB-C speakerphone. Image: Anthropic.*

## What Anthropic actually showed

The three devices were chosen to exercise different parts of the design stack, not to be products.

| Device | What it does | What Claude produced |
| --- | --- | --- |
| USB-C speakerphone | A round puck that plugs into a computer, with microphones, a speaker, Bluetooth and a PCB antenna | Schematic, four-layer PCB, 3D-printable enclosure, firmware, BOM |
| Home voice-assistant hub | A home hub with USB and Ethernet, microphones and a speaker | Schematic, four-layer PCB, wedge enclosure, firmware, BOM |
| Handheld virtual pet | A battery-powered toy with a display and buttons | PCB, enclosure, firmware, BOM |

Diode assembled the boards and ran the firmware under Claude’s direction. Anthropic says the builds needed no circuit fixes and that the same process worked for all three devices. The photos show finished units, not bare boards. The demo video is embedded in Anthropic’s post; the post does not link to KiCad files, BOMs or a test report.

![Claude’s enclosure, PCB, firmware and assembly shown together](/uploads/claude-electronics/claude-electronics-design.webp)

*Case, board layout, code and final assembly for the voice-assistant hub. Image: Anthropic.*

## The geometry is the story

The interesting improvement is not that Claude can draw a schematic. It is that it can reason about where parts go and how copper should run between them.

Earlier models, Anthropic says, placed support components too far from the chips they served, or oriented connectors the wrong way. Fable 5.2 produced denser layouts and routed the constrained nets first: high-speed pairs, high-current paths and noise-sensitive signals. For the hub, it routed USB and Ethernet one differential pair at a time, keeping the two tracks in each pair the same length and spacing, then added tuning zigzags where the length needed adjusting. It also rearranged the power supply around the current path.

The benchmark claim is striking, with a caveat. On Diode’s internal PCB Gym, Fable 5.2 scored **69%**, against **25%** for Fable 5. The chart plots that score against total API cost, and the gap is large. But PCB Gym is Diode’s benchmark, not a public harness, and Anthropic did not publish the board set or the scoring code. The number is evidence of a real improvement inside that setup; it is not an independent measurement of PCB quality.

![Diode PCB Gym score versus total API cost](/uploads/claude-electronics/claude-electronics-benchmark.webp)

*Diode PCB Gym scores against API cost. The benchmark is Diode’s internal layout evaluation, not a public third-party test. Image: Anthropic.*

Anthropic also cites **BenchCAD 2.1**, a public benchmark for rebuilding 3D parts, assemblies and circuit boards from drawings and renders. Fable 5.2 scored **83.5%**, nearly double Fable 5.1. That is a useful signal for spatial reasoning. It is not a signal-integrity, EMC or manufacturability score.

## It revises its own layout

The part that looks most like engineering is the self-correction. Earlier models would keep a layout that was 95% complete even when the last connections could never be routed; Diode had built many boards with earlier models that were 95% complete and unusable. Fable 5.2 would notice the dead end and change course.

On the speakerphone’s four-layer board, the touch wheel sits over a ring of copper electrodes. A via under the wheel would punch through an electrode, so Claude reassigned signals to different pins on two chips and kept the tracks under the wheel on a single layer. When the back of the board became crowded, it swapped signals on interchangeable pins and redrew a corner of the layout instead of adding vias to escape the problem.

The hub’s microphone routing shows the same behavior at a smaller scale. Claude found a power track looping around the ground ring at the sound port and a front-side track crossing that ring. It called the placement risky, deleted the local routing and started again, dozens of times if Anthropic’s account is accurate. The image below is the before-and-after pair the company published.

![Microphone routing before and after Claude rerouted the voice hub board](/uploads/claude-electronics/claude-electronics-routing.webp)

*The hub’s microphone routing before and after the rewrite. The power track no longer loops around the ground ring, and the front-side track no longer crosses it. Image: Anthropic.*

## Tools, datasheets and DFM

Claude did not only generate geometry. It used the tools around the geometry.

KiCad’s built-in router draws one track at a time between two points. On the hub, with long runs from a 100-pin connector, that was too slow. Claude wrote its own grid-based router, had it working in about half an hour, and could route a long track in roughly a second. When an audio clock line ended up too close to the Ethernet pairs, it changed the router’s spacing rules around the sensitive nets.

It also read datasheets. Asked whether the handheld pet would run without a battery, Claude checked the charger datasheet and answered that it would run from USB, but predicted the charging LED would flicker because the charger would keep topping up a small capacitor in place of the cell. That is the kind of answer that comes from reading the part, not from pattern-matching a schematic symbol.

The DFM pass found six solder-mask slivers that were too thin to manufacture. Claude widened the mask openings without moving components. It also dismissed a flagged ground-to-ground connection after deciding the checker had not recognized a deliberate return path. Diode manufactured the boards from the design files without a back-and-forth over adjustments, according to both companies.

![Speakerphone four-layer PCB, front layer](/uploads/claude-electronics/claude-electronics-speaker-pcb.webp)

*The speakerphone’s front copper. The touch wheel keeps its signal tracks on one layer, and the Bluetooth antenna area is kept clear of copper and vias. Image: Anthropic.*

![Voice-assistant hub four-layer PCB, front layer](/uploads/claude-electronics/claude-electronics-hub-pcb.webp)

*The hub’s front copper with ground poured between parts and signals. Image: Anthropic.*

## The enclosure is part of the circuit

Anthropic’s examples also show why “PCB design” is too narrow a description. The enclosure changes what the board can do.

The speakerphone’s board could not be lowered straight into its case: the mute switch’s knob hit the back wall. Claude worked out that the board would fit if it was tilted about **25 degrees**, chin first, then swung flat, and added that step to the assembly instructions.

For the hub, Claude calculated that a **25 mm** microphone port would resonate near **3.4 kHz**, inside the voice band. It changed the enclosure to a wedge that is taller at the rear and steps down at the front, shortening the ports to about **10 mm** and moving the resonance to roughly **8.9 kHz**, at the edge of the speech range. It also wrote speakerphone firmware that dims the LED ring as the audio gets louder, keeping the device inside the current budget it had designed.

![Speakerphone enclosure cutaway showing the board tilted during installation](/uploads/claude-electronics/claude-electronics-enclosure.webp)

*The speakerphone board cannot go in straight because the mute switch hits the back wall. Claude’s assembly path tilts it about 25 degrees and then swings it flat. Image: Anthropic.*

## What the demo does not prove

Anthropic is explicit about the limits, which is to its credit. The devices are prototypes. They have not been through electrical validation, antenna tuning, thermal testing or certification, and they were not designed for mass production. Claude was not connected to test equipment or to the machines that assemble boards, so Diode’s engineers built and tested the units by hand.

The published material has other gaps:

| Claim | What Anthropic published | What is missing |
| --- | --- | --- |
| Three working devices, no circuit fixes | Text, photos and a video | No independent teardown, build log or test data |
| PCB Gym 69% vs. 25% | A chart and a description | No public board set or scoring code |
| BenchCAD 2.1 83.5% | A benchmark score | A spatial-reasoning score, not SI/EMC/DFM validation |
| “End-to-end” design | Descriptions of specifications, PCB, CAD, firmware and BOM | No KiCad projects, BOMs or manufacturing files |
| Weeks of use | Anthropic’s statement | No long-term reliability or certification report |

None of that makes the demo fake. It makes it a company demonstration with company-selected evidence. The routing images, the DFM story and the enclosure calculations are specific enough to be interesting; they are not enough to audit the design.

## Why embedded engineers should care anyway

The practical value is not a model that signs off a board. It is a model that can get the first draft to a state where a human review is useful.

A lot of hardware time goes into placement, power routing, solder-mask cleanup, BOM checks and the tedious back-and-forth between the board and the enclosure. Those are exactly the tasks where a model can burn compute instead of an engineer’s afternoon. If the output is manufacturable enough to build, the engineer can spend more time on architecture, part selection, test coverage and certification — the parts that decide whether the product survives.

The next step Anthropic describes is denser and faster boards, simulation, and learning from measurements on finished devices. That is the right direction. A model that can route a board but cannot be measured against its own predictions is still a design assistant. The moment it can close that loop, the job changes.

For now, the honest reading is this: Claude Fable 5.2 can produce a plausible, buildable first-pass board when a company like Diode provides the tools, the manufacturing line and the test bench. That is a meaningful capability. It is not a finished engineer, and the published evidence does not claim otherwise.

![Eight-step workflow from prompt to a working prototype](/uploads/claude-electronics/claude-electronics-flow-en.webp)

*The workflow Anthropic describes, broken into design actions. The last step is still human: fabrication, assembly and test.*
