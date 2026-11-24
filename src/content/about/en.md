---
title: About EmbeddedNote
description: EmbeddedNote is an editorially independent bilingual engineering publication published by DataDelta, covering MCUs, hardware, connectivity and displays.
locale: en
---
# About EmbeddedNote

**EmbeddedNote is an engineering publication, and the company behind it also supplies the parts it writes about.** DataDelta publishes this site and supplies e-paper panels, driver boards and product design. The editorial side is independent of that business: articles follow the evidence, and a supply relationship does not buy a conclusion.

We publish in English and Chinese, focusing on microcontrollers, board design, wireless connectivity, displays and open-source hardware.

## Quick facts

- **What it is:** an editorially independent, bilingual (English / Chinese) engineering publication, published alongside a commercial supply and design business. The two are governed separately.
- **Who publishes it:** DataDelta, which also sells e-paper panels and design work. Panel and project enquiries go to the [work-with-us page](/en/partner/), never into editorial.
- **Who runs it:** Gary Xu, an embedded engineer writing since 2019; the same notes also run in Chinese for about 55,000 engineers.
- **What is free:** two browser-based tools, no account and no upload — an [e-paper image converter](/en/tools/epaper-image-converter/) and a [BLE throughput planner](/en/tools/ble-throughput-calculator/).
- **What is covered:** e-paper and display pipelines, BLE transfer budgets, MCU/SoC selection, PCB design, open-source hardware.
- **How claims are handled:** every number is a calculated example, a quoted specification, or a measurement, and the article says which.
- **Language:** English is primary; most articles have a Chinese edition under `/zh/`.

A project video can tell you what a device does. It rarely tells you which files are worth reading first, how its hardware is connected, or what might go wrong when you try to build something similar. Those are the details we try to bring into the articles.

## What you'll find here

The site runs on two tracks: [e-paper](/en/e-paper/) (waveform, ghosting, partial refresh, the whole path from image to bytes) and [low-power radio](/en/connectivity/) (BLE throughput and transfer budgets). Project breakdowns, chip and supply-chain observations sit in [notes](/en/notes/).

Some posts work through a schematic, repository or datasheet. Others explain a communication budget, a display-data format or a debugging method. The goal is to leave readers with something they can check or use, not just a list of specifications.

The tools are part of that approach. You can use the [BLE Throughput & Transfer Planner](/en/tools/ble-throughput-calculator/) to explore packet and connection-event assumptions, or the [E-Paper Image Converter](/en/tools/epaper-image-converter/) to examine colour mapping and indexed pixel data. Our [e-paper engineering guide](/en/articles/epaper-engineering-field-guide/) brings several of these problems together.

## Who runs EmbeddedNote?

EmbeddedNote is published by DataDelta and edited independently, with an engineering focus shaped by work on embedded firmware, BLE/NFC communication and e-paper integration.

The person behind the site also writes about embedded systems in Chinese, for a readership of about **55,000** engineers. The blog is a place to keep the technical notes, source references and calculations accessible beyond a social feed.

When an article has no named individual author, it carries the **EmbeddedNote** byline. That identifies the site's editorial work; it does not mean every featured device has been built or tested by us.

## How we handle technical claims

We use three kinds of evidence, and they should not be confused:

- **Published sources:** manufacturer documentation, project repositories, schematics and statements from project maintainers. We link to the original material where possible and identify claims that come from it.
- **Our calculations:** packet counts, memory budgets, example code and engineering comparisons. These should include enough assumptions and working for another developer to reproduce the result.
- **Hardware measurements:** results obtained from physical devices. We only describe something as tested when there are actual observations and a stated setup or method. A simulation or calculated estimate is not a bench test.

AI-assisted tools may be used for drafting, translation or editing. They are not technical evidence; source material and reproducible calculations take precedence. The English and Chinese versions are edited for readability rather than translated word for word.

## Corrections, attribution and partnerships

If you find an incorrect specification, broken reference or image-credit problem, email [xudeng@datadelta.cn](mailto:xudeng@datadelta.cn) with the page link and the part that needs checking. For substantial corrections, we aim to update the page while keeping its original publication date and identifying the revision.

Third-party projects and trademarks remain the property of their respective owners. Coverage does not imply a manufacturer's endorsement. We do not publish sponsored articles or sell a favourable conclusion.

**How the two sides are kept apart.** DataDelta is both the publisher and a supplier, so the boundary is stated rather than implied:

- A part we sell gets no easier a review, and no softer a conclusion, than one we do not.
- Failures, limits and unsolved problems in our own designs are written up as such; the e-paper articles on ghosting, cold-temperature behaviour and partial refresh were all written from that position.
- Where an article touches a product we supply, the commercial relationship is disclosed on the [work-with-us page](/en/partner/) — not left for the reader to infer.
- Advertising and sponsorship do not appear anywhere on this site.

We also welcome open-source project suggestions and relevant engineering collaboration enquiries at **[xudeng@datadelta.cn](mailto:xudeng@datadelta.cn)**.
