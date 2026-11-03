---
title: "Raspberry Pi 5 16GB Now Costs $385. It Launched at $120."
description: "Raspberry Pi has raised its 16GB Pi 5 price by $80 to $385 and added $40 to 16GB Compute Module 5 variants. A look at the price history, memory supply and implications for hardware designs."
locale: en
translationKey: raspberry-pi-16gb-price-rise-2026
pubDate: 2026-11-02
category: mcu-soc
tags:
  - Raspberry Pi
  - Raspberry Pi 5
  - Compute Module 5
  - LPDDR4X
  - Memory Pricing
  - Single-Board Computers
draft: false
author: EmbeddedNote
sourceUrl: https://www.raspberrypi.com/news/price-rises-for-some-16gb-raspberry-pi-products/
seoTitle: "Raspberry Pi 5 16GB Hits $385 as Compute Module 5 Prices Rise"
seoDescription: "The 16GB Raspberry Pi 5 now lists for $385, up $80 on November 2, 2026. Here's the official price history, why 16GB DRAM is difficult to source, and what CM5 users should consider."
---

When the 16GB Raspberry Pi 5 launched in January 2025, it cost $120. As of November 2, 2026, the same memory configuration carries a **$385 list price**. That's $265 more in less than two years, and more than three times its launch price. It's a striking number for a board that still looks, at first glance, like the Raspberry Pi 5 people have been using in countless small projects.

The latest increase is selective. In [an announcement published on November 2](https://www.raspberrypi.com/news/price-rises-for-some-16gb-raspberry-pi-products/), Raspberry Pi founder Eben Upton confirmed an **$80 increase for the 16GB Raspberry Pi 5**, taking it from $305 to $385. **Every 16GB Compute Module 5 configuration rises by $40**, while the company is holding the price of the 16GB Raspberry Pi 500+, its keyboard-integrated desktop. These are US-dollar list prices; local taxes, availability and reseller pricing can differ.

![Official Raspberry Pi 5 16GB list-price history from launch through November 2026](/uploads/raspberry-pi-16gb-price-rise-2026/raspberry-pi-16gb-price-cover.webp)

*Price-history graphic by EmbeddedNote, based on Raspberry Pi's published announcements. Not a product photograph.*

## How the 16GB board reached $385

This wasn't a single price jump. Raspberry Pi has made several adjustments as memory costs have moved against it:

| Effective date | 16GB Raspberry Pi 5 list price | Change |
| --- | ---: | ---: |
| January 2025 launch | $120 | Launch price |
| December 2025 | $145 | +$25 |
| February 2026 | $205 | +$60 |
| April 2026 | $305 | +$100 |
| **November 2, 2026** | **$385** | **+$80** |

The company began citing unusually steep LPDDR4 memory costs in late 2025. Its February and April updates described further pressure on higher-density configurations. In a separate move on October 1, the 2GB Raspberry Pi 4 and Pi 5 each went up by $12.50. November's announcement is not another across-the-board increase: it specifically targets selected 16GB products.

One detail in Upton's latest statement matters more than the headline price. Raspberry Pi says it has been qualifying alternative components to broaden its purchasing options, but **alternative supply for 16GB DRAM remains limited**. Other component shortages have added to the problem. The company has not published its memory procurement costs, contract terms or per-board margin changes, so the $265 rise in retail price should not be presented as the cost increase of a single DRAM package.

## The bigger question for Compute Module 5 designs

A $40 increase can be harder to absorb when the part sits inside a product rather than on a hobbyist's desk. Compute Module 5 is offered in several memory, eMMC and wireless configurations, and **only the 16GB versions are included in this latest CM5 adjustment**. The price of a particular part number should be checked against the [current Compute Module 5 product brief](https://www.raspberrypi.com/products/compute-module-5/), not inferred from the $40 increase alone.

For a production run of a few thousand units, another $40 per module changes the BOM substantially. Yet switching to an 8GB or 4GB module without profiling the workload can be expensive in another way. Container-heavy systems, database caches, graphical applications and local inference workloads may genuinely need the larger memory footprint. If an application starts paging heavily or running out of memory under peak load, the cheaper module may become the costlier engineering decision.

The sensible measurement is not just idle RAM use. Look at peak resident memory, concurrent workloads, swap activity and the headroom needed for updates over the product's life. Teams already committed to a 16GB CM5 design should also revisit supplier lead times and approved alternatives before freezing the next BOM revision.

Upton says Raspberry Pi expects the memory supply crunch to ease eventually and intends to reverse the increases when costs fall. He did not give a date. The company has also warned about inflated reseller prices and misleading product listings, pointing customers toward its [Approved Reseller network](https://www.raspberrypi.com/resellers/).

For hobby projects, a smaller-memory Pi or an earlier model may still be the right answer. For a commercial device built around a 16GB CM5, the next thing worth reopening is probably the costed BOM, not the schematic.

**Sources:** [November 2 announcement](https://www.raspberrypi.com/news/price-rises-for-some-16gb-raspberry-pi-products/) · [December 2025 pricing](https://www.raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/) · [February 2026 pricing](https://www.raspberrypi.com/news/more-memory-driven-price-rises/) · [April 2026 pricing](https://www.raspberrypi.com/news/a-new-3gb-raspberry-pi-4-for-83-75-and-more-memory-driven-price-increases/) · [October 2026 pricing](https://www.raspberrypi.com/news/price-increases-for-2gb-raspberry-pi-4-and-raspberry-pi-5/)
