---
locale: en
translationKey: ai-timing-not-geometry
pubDate: '2026-11-24'
category: hardware
draft: false
contentType: deep
series: ai-hardware
author: EmbeddedNote
title: 'AI Can Draw the Schematic. It Cannot Check the Timing.'
description: 'Layout tools now pass ERC, DRC and DFM. The checks that decide whether a board ships — setup and hold, panel waveform timing, EMC, part tolerance — all need a measurement, and no model has one.'
seoTitle: 'AI PCB Design Stops at Timing, EMC and Tolerance'
seoDescription: 'What AI PCB tools can verify and what they cannot: geometry is checkable from the file, timing and tolerance are not. An e-paper frame shows why the gap matters.'
tags:
- AI Hardware
- PCB Design
- Timing
- E-paper
- DFM
- Validation
---

The [Claude Fable 5.2 demo](/en/articles/claude-electronics-design/) produced three boards that were built, assembled and left running. That part is real. What it cannot tell you is whether the same board still works at 70 °C, in the third batch, with the flash that actually arrived instead of the one in the BOM.

The gap is worth naming, because it decides what you can hand to a model and what stays yours.

## Two kinds of check

Everything a layout tool checks is a rule applied to a file. Clearance, minimum drill, solder-mask sliver, unrouted net, a differential pair whose two tracks differ in length. None of these need to know anything about the physical part. A model that can generate geometry can also satisfy geometry, and the demo's DFM pass — six slivers widened without moving a component — is exactly that.

The other kind of check needs the world. Setup and hold across temperature. Whether the 3.3 V rail sags when the radio keys up. Whether the panel's waveform is still valid at −10 °C. Whether the thousandth board behaves like the first. None of this is decidable from the file. It is decided by a measurement, or by a model of the part that somebody qualified.

The demo's wins are almost all in the first category. The 25-degree tilt to clear the mute switch is geometry. The 3.4 kHz port resonance is an acoustic calculation from a dimension. Reading the charger datasheet to predict a flickering LED is a lookup, done well. Impressive, and all of it checkable without a bench.

## Timing is a budget, not a shape

A timing margin is a sum: clock skew, buffer delays, board flight time, the receiver's setup requirement, and the variation of every part in that chain over temperature and process. The numbers come from corner data in datasheets, not from the netlist. Change nothing in the layout and the same bus can go from comfortable at 25 °C to negative at 85 °C, because the flash's access time moved and the clock did not.

That is why routing is the easy half. The search space is visual, the rules are written down, and a wrong answer is visible. Timing has none of those properties. The rules live in datasheets and errata, the numbers move with temperature, and the verdict arrives after you build.

A model can reason about a timing budget if you hand it the budget. It cannot discover that the budget was wrong, because the discovery requires a scope and a thermal chamber.

## E-paper makes the gap wider

An e-paper product is close to a pure timing problem, which is what makes it a useful test case. The geometry is simple: a rectangle, a known driver, an FPC with one correct orientation. Almost everything that decides whether the product is good is timing, temperature and the panel's own behavior.

Three numbers show the shape of it.

**Frame size.** A 13.3-inch E6 panel is 1,920,000 pixels and 960,000 bytes packed as RAW4, or 1.92 MB as RAW8. That single number decides whether the frame lives in PSRAM or streams in strips, and it is settled long before anyone routes a board. The [size chart](/en/articles/epaper-size-chart/) has it for all sixteen sizes.

**Partial refresh.** A partial window can update in a few hundred milliseconds and still leave residue that becomes visible after a few hundred updates. The safe window is not a datasheet parameter; it depends on the image, the temperature and how often you do it. We wrote up the [working limits](/en/articles/epaper-partial-refresh-safe/) because the failure mode is slow and easy to miss in a demo.

**Cold.** Below zero the same waveform writes a muddier image. The fix is longer phases, which costs battery, which shrinks the enclosure budget, which changes the product. The [cold-weather failure modes](/en/articles/epaper-cold-failure/) are a good example of a constraint that no amount of schematic review will surface.

None of this appears in ERC or DRC. All of it appears in the first prototype on a cold morning.

## Nominal design is the easy half

Simulation answers a narrow question: does the design work when every part is at its typical value. Production asks a different one: does the design work when every part is at the edge of its tolerance at the same time, on the coldest day of the year, in the thousandth unit.

A 1% resistor is 1% at 25 °C and worse at 85 °C. An electrolytic loses capacitance over years. A connector's contact resistance drifts with mating cycles. A model that emits one nominal design has done the part of the job that a simulator already did faster.

## What to hand it, and what not to

The pattern from the demo is consistent enough to plan around. A model is strong where the constraint is written in a document or visible in a drawing, and weak where the constraint lives in a measurement it has never taken.

| Hand it | Keep it |
| --- | --- |
| Placement and power routing | Timing budget sign-off |
| DFM cleanup, mask and sliver fixes | EMC plan and pre-compliance |
| BOM cross-check against datasheets | Thermal derating |
| Mechanical interference and assembly order | Production test limits and yield |
| A first draft that a reviewer can mark up | Anything that depends on a measured curve |

The last row on the left is the real value. A hardware team spends a lot of its week on the first draft and the cleanup around it. If a model can turn a prompt into something an engineer can review in an afternoon, the review gets better because the engineer is fresh, and the schedule gets shorter because the boring part moved.

## The loop that is still open

The thing that would change the picture is a model that can ask for a measurement and use the answer. Some teams are already building that loop by hand: a bench, a script, a table of results fed back into the prompt. It works, and it does not scale past the person running it.

Until that loop closes, the fair description of these tools is a very fast drafter with a good memory for datasheets. That is worth paying for. It is not the same as a design review, and a team that confuses the two will get one board through DRC and lose a month to a cold morning.

For us, that boundary is the work. The panels arrive with a waveform table and a temperature curve; the product only works if the firmware respects both, and no schematic captures either. Those designs are [where our time goes](/en/solutions/).
