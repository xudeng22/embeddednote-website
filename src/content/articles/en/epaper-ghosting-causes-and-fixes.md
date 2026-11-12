---
title: 'E-Paper Ghosting: Temperature, Waveform and Update Policy'
description: 'Why e-paper keeps a faint copy of the previous frame, how temperature and waveform choice change it, and the counter-based update policy that keeps it under control.'
locale: en
translationKey: epaper-ghosting-causes-and-fixes
pubDate: '2026-11-11'
category: display
tags:
- E-Paper
- Ghosting
- Waveform
- Display Drivers
- Verification
draft: false
author: EmbeddedNote
contentType: deep
series: epaper
seoTitle: 'E-Paper Ghosting: Causes, Temperature and Update Policy'
seoDescription: 'What e-paper ghosting actually is, why temperature and refresh mode change it, and a counter-based update policy with a test sequence you can reproduce.'
supplyCta: true
---

Ghosting looks like a software bug: the previous frame is still there, faintly, behind the new one. So the first instinct is to redraw the frame harder — refresh twice, refresh in a different mode, write the same buffer again.

None of that works reliably, because ghosting is not a stale buffer. It is pigment that did not finish moving. Rewriting the same pixels does not move it; only a full-refresh waveform, with enough time and the right voltage sequence, resets the state of the film.

<img src="/images/p0/epaper-ghosting-timeline.svg" alt="Residue accumulating across partial refreshes and clearing after a full refresh" width="960" height="320" loading="lazy" decoding="async">

## What ghosting physically is

An e-paper pixel is a cavity with white and black pigment particles suspended in fluid. The controller drives them with a voltage waveform: a sequence of pulses whose amplitudes and durations push particles to one end or the other. A full refresh drives them through several transitions so that every pixel ends in a well-defined state.

A partial refresh skips most of that. It writes only the region that changed, using a shorter waveform with fewer transitions. The untouched pixels keep whatever state they were in, which is the entire point — it is fast and it does not flash the whole screen.

The cost is that the final state of a pixel depends on where it started. A pixel pushed from black to white ends up slightly different from one pushed from grey to white. Over many partial updates, those small differences accumulate into a visible ghost of an older frame.

## Three inputs, not one

| Input | What it changes | What you can control |
| --- | --- | --- |
| Previous image | How far each pixel has to travel | The content you show, and how often |
| Temperature | Pigment viscosity and switching speed | The waveform table you select, and whether you allow partial at all |
| Refresh history | How many short waveforms since the last full one | A counter, and a budget |

Most implementations control the first one by accident, ignore the second, and never implement the third. The third is the cheapest to fix.

## Why "refresh it again" sometimes makes it worse

A second partial refresh on the same region pushes the pigment through the same short sequence again. If the residue came from an incomplete transition, a repeat can help. If it came from charge trapped at the electrode, repeating the same short waveform can deepen the imbalance instead of clearing it.

The reliable operation is not a repeat; it is a full refresh, which uses a long sequence specifically designed to normalise every pixel. That is why the fix belongs in the update policy, not in the button handler.

## Temperature is not a detail

Pigment moves more slowly when it is cold. A waveform that completes a transition in 300 ms at 25 °C may not complete it at 0 °C, and the panel will show a weak, ghosted image that looks exactly like a software error. Vendors publish waveform tables per temperature band for this reason, and the controller is expected to select the right one.

Two published examples show the scale. E Ink lists an operating range of **0–50 °C** for [Spectra 6](https://www.eink.com/brand/detail/Spectra6) modules (usually written **E6**) and **−20 to 65 °C** for [Marquee](https://www.eink.com/brand/detail/marquee), with a 5–7 s transition time for the latter. Those are brand-level figures, not your panel's datasheet, but they make the point: the operating range is a specified parameter, and a driver that ignores temperature is only correct inside one narrow band.

Three practical consequences:

1. **Read the temperature before selecting a waveform.** If your driver hard-codes one table, it is only correct in one band.
2. **Disable partial refresh below the vendor's stated minimum.** A partial waveform has less margin; at low temperature it fails quietly.
3. **Do not invent a compensation curve.** The tables come from panel characterisation. Guessing a scaling factor produces something that looks plausible at 20 °C and damages the panel at −10 °C.

If your product ships to a cold climate, this is a hardware requirement, not a firmware tweak: the panel, the controller and the waveform set all have to cover the range.

## The update policy that actually holds

Two counters and three gates. Nothing here is vendor-specific:

```c
/* policy sketch, not a driver */
#define PARTIAL_BUDGET 20

static uint32_t partial_count = 0;
static int      last_mode = -1;

bool need_full_refresh(void)
{
    if (last_mode != MODE_FULL)              return true; /* mode or waveform change */
    if (partial_count >= PARTIAL_BUDGET)     return true; /* budget exhausted          */
    if (panel_temp_c() < TEMP_MIN_PARTIAL)   return true; /* too cold for partial      */
    return false;
}

void note_update(int mode)
{
    if (mode == MODE_FULL) partial_count = 0;
    else                   partial_count++;
    last_mode = mode;
}
```

The budget is the only number you have to choose, and it is a product decision. A desk clock that updates once a minute can afford a full refresh every hour. A battery tag that updates four times a day may never need a partial refresh at all. Start conservative — 10 to 20 partial updates before a forced full one — then measure.

Two rules that matter more than the number:

- **Always full-refresh after changing palette, rotation or waveform.** The first frame in a new mode is not comparable to the last one in the old mode.
- **Never partial-refresh a large solid area.** The transition is the most demanding case for the short waveform, and it is also the one where residue is most visible.

## How to judge whether it is acceptable

Ghosting is a spectrum, and "no ghost" is not a testable requirement. Use a sequence and a fixed observation:

1. Display frame A (high contrast: large black block on white). Photograph it.
2. Display frame B (mostly white). Photograph it under the same light, same distance, same exposure.
3. Display frame A again, then B again. Repeat ten times.
4. Compare the luminance of the region that was black in A across the ten B frames.

If the region brightens monotonically and does not recover after a full refresh, the panel is accumulating residue faster than the policy clears it. If it recovers after a full refresh, the policy is the fix. If it never recovers, the panel has taken a permanent set and no firmware change will bring it back.

Record temperature and waveform revision with every frame. A ghosting report without them is not reproducible.

## What we do not know

We have not measured panel lifetime against partial-refresh count for any specific model, and vendors rarely publish that curve. We also cannot tell you the exact temperature at which a given panel stops switching reliably — that number comes from the panel's datasheet and your own cold-chamber test.

What we can say is structural: ghosting is history-dependent, temperature-dependent and mode-dependent, so any implementation that ignores one of those three will produce a bug report that cannot be reproduced.

For the layers below this one, see [why your e-paper photo looks wrong](/en/articles/why-your-epaper-photo-looks-wrong/) and [the refresh timing breakdown](/en/articles/epaper-refresh-timing-pipeline/). If you are preparing an image for the panel in the first place, the [image converter](/en/tools/epaper-image-converter/) has a palette table that separates reference colours from measured device profiles.

## Three questions the policy raises

### Can I clear ghosting by displaying a white frame for a while?

No. A white frame is just another image, driven through the same short waveform that left the residue. Only the full-refresh sequence resets the film. If white appears to help, the residue has become less visible against a uniform background — the panel has not recovered.

### How do I choose PARTIAL_BUDGET for a clock that updates every minute?

A minute is 1,440 updates a day. A budget of 20 forces 72 full refreshes daily, a visible flash every 20 minutes. A budget of 120 allows two hours between forced refreshes, so an hourly full refresh binds first at 24 flashes a day. Choose the flash frequency you can tolerate, then derive the budget from it.

### Is ghosting permanent, or does it fade if I stop updating?

It depends how far the pigment was pushed. Residue from an incomplete transition usually clears with a full refresh. Charge trapped at the electrode, or a panel run outside its temperature range for a long time, can leave a permanent set that no waveform removes. The ten-frame test tells you which one you are looking at.

## Sources

- E Ink, [How electronic ink works](https://www.eink.com/tech/detail/How_it_works) — the pigment and electrode model used in the first section.
- E Ink, [Spectra 6](https://www.eink.com/brand/detail/Spectra6) (0–50 °C, 30:1 contrast, usually written **E6**) and [Marquee](https://www.eink.com/brand/detail/marquee) (−20 to 65 °C, 5–7 s transition) — the two published operating ranges quoted above.
- The datasheet and waveform file that ship with your module. These override anything on this page: controller, native colour codes and temperature bands differ per part number.

We also tried to check Good Display's catalogue (`good-display.cn`) for this article. Their site rejects automated requests with HTTP 406, so no Good Display figure is quoted here — open the datasheet that came with your panel instead of trusting a summary.
