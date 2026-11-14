---
title: 'E-Paper Power Consumption: The Three Terms That Decide Battery Life'
description: 'E-paper draws almost nothing to hold an image. The energy goes into three terms: the refresh, the sleep current of the driver, and the host. A worked model with numbers you can substitute.'
seoTitle: 'E-Paper Power Consumption, Calculated'
seoDescription: 'How to size an e-paper battery: energy per refresh, standby current, host cost, a worked example on 3.3 V, and the reason cutting the panel rail beats shrinking the refresh.'
locale: en
translationKey: epaper-power-model
pubDate: 2026-11-14
category: display
tags: ['e-paper', 'power', 'battery life', 'low power', 'selection']
contentType: deep
series: epaper
supplyCta: true
---

An e-paper label that runs for years sounds like magic until you write the energy budget down. Then it turns out the panel is not the problem — the driver's sleep current is, and it decides the battery more than the refresh does.

**In one sentence:** daily energy = refreshes per day × energy per refresh + hours idle × standby current × voltage, and at four refreshes a day the second term is usually the larger one.

## The three terms

Every e-paper product's budget is the sum of three things, and they scale differently:

| Term | Depends on | Typical shape |
| --- | --- | --- |
| Refresh energy | Panel area, waveform length, refresh mode | Bursts of tens of millijoules |
| Standby current | Driver and regulator quiescent draw | Microamps, all the time |
| Host cost | MCU sleep mode, radio duty cycle | Microamps to milliamps |

Only the first term is the "e-paper" part. The other two are ordinary low-power design, and they are where the years come from.

## Energy per refresh

One refresh costs energy while the panel is being driven:

```
E_refresh = V × I_refresh × t_refresh
```

`V` is the panel supply, `I_refresh` the current during the update, `t_refresh` how long the waveform runs. All three come from the panel datasheet; the trap is that `t_refresh` is the **waveform** time, not the SPI transfer time — a full refresh is seconds, not milliseconds.

For the worked example below the assumptions are stated up front, because the result is only as good as they are:

| Parameter | Assumed value | Where yours comes from |
| --- | --- | --- |
| Supply | 3.3 V | Your rail |
| Current during refresh | 15 mA | Panel datasheet, "operating current" |
| Full refresh time | 2.0 s | Panel datasheet, full waveform |
| Partial refresh time | 0.4 s | Panel datasheet, partial waveform |
| Standby, panel powered | 10 µA | Driver datasheet, sleep mode |
| Standby, panel rail cut | 2 µA | Regulator + MCU only |

That gives **99 mJ** for a full refresh and **19.8 mJ** for a partial one. Both are small numbers, and that is exactly why the standby term wins.

## The number nobody checks

Take a label that refreshes four times a day and leaves the panel powered:

```
refresh: 4 × 99 mJ        = 0.40 J/day
standby: 3.3 V × 10 µA × 86400 s = 2.85 J/day
total:                     3.25 J/day
```

**88% of the daily energy is standby.** The panel redraws four times and sits still for the remaining 23 hours 59 minutes, and the driver's sleep current quietly eats seven times what the refreshes cost.

Cut the panel rail between updates and standby drops to 2 µA:

```
standby: 3.3 V × 2 µA × 86400 s = 0.57 J/day
total:                     0.97 J/day
```

Same product, same refresh rate, **3.3× the battery life**. This is the single largest lever in most e-paper designs, and it is a MOSFET and a GPIO.

## What that means for the battery

Using usable capacity of 60% for a coin cell, 70% for alkaline and 85% for a LiPo (regulator losses included):

| Battery | 4 refreshes/day, rail on | 4/day, rail cut | 24/day, rail on | 24/day, rail cut |
| --- | ---: | ---: | ---: | ---: |
| CR2032, 220 mAh | 439 days | 1,475 days | 273 days | 484 days |
| 2×AA alkaline, 2000 mAh | 4,656 days | 15,648 days | 2,893 days | 5,132 days |
| LiPo 500 mAh | 1,743 days | 5,859 days | 1,083 days | 1,921 days |

The multi-year figures are not a promise. Alkaline cells self-discharge at roughly 2–3% a year and a LiPo at 1–2%, so a 42-year calculation describes a cell that will be flat from self-discharge long before the circuit is. Treat anything past about five years as "limited by the cell, not the design".

The shape of the table is what matters: **doubling the refresh rate costs far less than leaving the panel powered**, and at 24 refreshes a day the refresh finally starts to compete with standby.

## The four levers, in order of effect

1. **Cut the panel rail when idle.** One P-channel MOSFET or a load switch. Typically 2–5× battery life.
2. **Refresh less.** Going from 24 to 4 refreshes a day removes 2 J/day — worth more than any waveform tuning.
3. **Use a partial refresh for small changes.** 0.4 s instead of 2 s is 5× less energy per update, but each partial update adds ghosting, so pair it with a full refresh counter.
4. **Pick a driver with a real sleep mode.** Two drivers with identical pinouts can differ by 10 µA in sleep, which is the whole budget.

The host matters too: an ESP32 in deep sleep is a few microamps plus the regulator, but a radio that wakes every minute will dominate everything above. Budget the radio separately.

## Where the model can be wrong

- **Cold panels refresh longer.** The waveform stretches at low temperature, so winter energy is higher than the datasheet-time calculation suggests.
- **Bigger panels cost more per refresh.** Charge scales with area; a 31.5-inch panel is not a 2.13-inch badge with a bigger battery. The [size chart](/en/articles/epaper-size-chart/) gives the pixel count and frame bytes for every size.
- **Regulator efficiency at microamps** is often terrible — a linear regulator quiescent current can exceed the MCU's sleep current.
- **Refresh time is not transfer time.** Optimising SPI does nothing here; the panel keeps driving after the last byte arrives.

## What to check before you size a battery

1. Panel datasheet: operating current, full and partial waveform times.
2. Driver datasheet: sleep current, and what it takes to reach it.
3. Regulator: quiescent current at the load you will actually have.
4. MCU: deep-sleep current with the peripherals you need awake.
5. Cell: self-discharge rate and the temperature you will run at.

Do the arithmetic in joules, not milliamp-hours. It is the only way the three terms stay comparable, and it is why a design can look fine on a bench supply and die in a month on a coin cell.

## Sources

- E Ink, [Spectra 6](https://www.eink.com/brand/detail/Spectra6) — the panel family used in the example; bistable, so holding an image costs nothing.
- E Ink, [Carta](https://www.eink.com/brand/detail/Carta) — the monochrome reading panel, same bistable behaviour with a shorter waveform.
