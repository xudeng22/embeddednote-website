---
title: 'Building a Reliable E-Paper Pipeline — Pixels, Wireless Transfer and Refresh'
description: 'A practical engineering field guide to e-paper data budgets, palette conversion, RAW packing, BLE transport, display refresh, verification and failure analysis.'
locale: en
translationKey: epaper-engineering-field-guide
pubDate: '2026-11-06'
category: display
tags: [E-Paper, Embedded Engineering, BLE, Image Processing, Display Drivers, Verification]
author: EmbeddedNote
draft: false
contentType: deep
series: epaper
seoTitle: 'E-Paper Engineering Guide — From Image Bytes to Verified Refresh'
seoDescription: 'Design an e-paper update pipeline with reproducible image-size calculations, palette mapping, BLE scheduling, SPI timing, waveform boundaries and test checklists.'
---

The screen is the most visible part of an e-paper product, but it is rarely the only reason an update fails. A photograph may look correct in a desktop preview and render with swapped colors on hardware. A BLE transfer may finish on the phone while the receiver has only part of the file. A controller may load an entire frame over SPI in under a second and then spend many more seconds executing the display waveform. Each failure lives at a different boundary.

This guide treats an e-paper update as an **end-to-end engineering pipeline**, not a single “refresh” operation. It combines byte-level examples, scheduling estimates, acceptance checks and references you can use without owning any particular development board. If you do have a device, the sections also show which measurements turn a calculation into a defensible product claim.

**Evidence statement:** All throughput and timing numbers in this guide are *calculated examples* with stated assumptions. The RAW4 vector and Python example are executable software checks. We have **not** tested a specific panel, measured color accuracy or benchmarked a phone/MCU pair for this publication. Project descriptions elsewhere on EmbeddedNote do not establish independent hardware validation unless a report says so.

## 1. Define what “updated” means

Before selecting an MCU or wireless protocol, write down the exact start and finish of the user-visible operation. Common interpretations are:

- **Upload complete:** the phone or web app has queued the final chunk. This is a sender-side milestone, not proof of storage at the device.
- **Received and verified:** the peripheral has reconstructed the declared byte count, checked a checksum or hash and committed the result to an appropriate buffer or file.
- **Controller ready:** the refresh trigger has been accepted and the controller's BUSY indication has returned to its documented idle state.
- **Image optically stable:** the visible panel meets a specified contrast/color or change threshold under controlled observation.

An honest specification might promise “image received and verified within X seconds under conditions Y” and separately state the supported refresh mode's completion time. Those are testable statements. “3-second refresh,” without defining its endpoints, is not.

![Four stages in a practical e-paper image pipeline](/images/p0/epaper-engineering-field-guide-cover.webp)

## 2. Begin with pixels and actual wire format

An image's dimensions tell you the number of pixels, not the number of bytes a controller will accept. For tightly packed fixed-width indexes, the basic equation is:

`packed_bytes = ceil(width × height × bits_per_pixel / 8)`

For an **8-bit index**, every pixel occupies a byte. For a **4-bit index**, two pixels normally share one byte. These are software representations, not universal E Ink controller formats.

| Example image | Assumed software format | Packed data | What it means |
|---|---|---:|---|
| 800 × 540 | 4 bits/pixel | 216,000 B | Continuous RAW4 indexes, no row padding |
| 800 × 540 | 8 bits/pixel | 432,000 B | One index byte per pixel |
| 960 × 540 | 1 bit/pixel | 64,800 B | Hypothetical packed monochrome bitmap |
| 720 × 480 | RGB888, 24 bits/pixel | 1,036,800 B | Uncompressed input photo/frame |
| 200 × 200 | 1 bit/pixel | 5,000 B | One packed binary plane |

The table deliberately mixes *possible* intermediate formats; it does not claim that the referenced panels use these exact buffers. A controller may require color planes, byte-aligned scanlines, separate commands, inversion, rotated scan order or a proprietary indexed code set. **Never select a payload format from a color count alone.** Six available colors require at least three information bits per pixel in theory, but that says nothing about the controller's transfer format.

When estimating memory, distinguish an RGB source image, a decoded intermediate surface, an index framebuffer, optional double buffering and the controller transfer scratch space. A 720 × 480 RGB888 buffer is about 0.99 MiB by itself; a second full-size buffer can be a major design decision on an MCU. The headline flash size is not the same thing as available contiguous RAM.

## 3. Use a binary test vector before a photograph

A first photograph is a terrible low-level diagnostic: incorrect nibble order, palette maps and rotation can all look like “bad color processing.” Begin with a tiny artificial pattern whose bytes you know in advance.

Assume a **five-pixel-wide, two-row** indexed image with values:

```text
Row 0:  0 1 2 3 4
Row 1:  5 0 1 2 3
```

With **continuous row-major RAW4**, no per-row padding and the first pixel in the high nibble, the 10 indexes produce exactly five bytes:

```text
01 23 45 01 23
```

The `0x45` byte straddles the logical row boundary. A device that aligns each row to complete bytes would use a *different* six-byte layout. A decoder with inverted nibble order would give a different image even with the same total length. These distinctions are why the binary contract belongs in the interface specification.

![Odd-width RAW4 example showing where the row boundary falls](/images/p0/raw4-odd-width.svg)

Reproduce the five-byte vector with the Python standard library:

```python
from math import ceil

width, height = 5, 2
indexes = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3]
assert len(indexes) == width * height
assert all(0 <= value <= 15 for value in indexes)
raw4 = bytes(
    (indexes[i] << 4) | (indexes[i + 1] if i + 1 < len(indexes) else 0)
    for i in range(0, len(indexes), 2)
)
assert raw4.hex(' ') == '01 23 45 01 23'
assert len(raw4) == ceil(width * height / 2)
print(raw4.hex(' '))
```

For a real target, record at least **width, height, pixel traversal order, row alignment, nibble order, native palette-code mapping and the driver's expected waveform/mode**. Add a solid-color swatch for every native code. Then test corner pixels, alternating columns, checkerboards and a one-pixel border. Once those work, a photo becomes informative rather than ambiguous.

For byte-level export conventions and the odd-width example, see [our RAW4 verification guide](/en/articles/epaper-palette-raw4-packing-guide/) and the [browser-based E-Paper Image Converter](/en/tools/epaper-image-converter/).

## 4. Quantize color separately from encoding

Converting a photograph is not just replacing each RGB pixel with its nearest named color. There are at least four separate choices:

1. **Source processing:** crop or letterbox the image to the real panel aspect ratio; adjust exposure and tone without clipping important content.
2. **Palette appearance:** define the colors you are trying to reproduce. A reference sRGB swatch is a *visualization*, not a measurement of reflective pigment.
3. **Quantization and dithering:** choose palette entries and, optionally, distribute quantization error spatially to represent intermediate tones.
4. **Native coding:** map each software palette index to the device's real color code or bit plane, with the agreed pixel orientation.

Nearest-color mapping often preserves edges but produces contour bands in smooth gradients. **Floyd–Steinberg** error diffusion can improve apparent tone continuity while introducing granular texture near text and narrow edges. **Bayer ordered dithering** produces a repeating pattern that can be stable and predictable but may look conspicuous on faces or areas of flat color. **Atkinson** diffusion distributes a smaller fraction of the quantization error and can preserve a different balance of contrast and texture. There is no universally best algorithm for every screen, image and viewing distance.

When judging a result, freeze the **same image, crop, output dimensions, reference palette, brightness and contrast** across the algorithms. Use at least four diagnostic inputs: skin tones, a low-contrast gray gradient, saturated color patches and small black text. Do not compare one algorithm on a brightened photo with another on a different crop.

A numerical color difference can be useful if the palette has been measured properly. Lab ΔE76 is straightforward but is not interchangeable with perceptually improved CIEDE2000. More fundamentally, a browser preview and physical e-paper under room lighting are not the same measurement system. If reporting panel accuracy, document illuminant, measurement instrument, observation geometry, panel/lot, temperature, controller and waveform version. Without those details, label the result a **reference preview**.

## 5. Design the application transfer before optimizing the radio

Suppose you need to send a **24,400-byte example image** over a GATT Write Command protocol. For an ordinary write, the attribute value can be at most `ATT_MTU − 3` bytes. If two of those bytes are consumed by your application chunk header, the useful content is:

`useful = min(negotiated_MTU − 3, accepted_API_value_cap) − 2`

With MTU 23 that gives **18 image bytes per operation**, or `ceil(24,400/18) = 1,356` operations. With MTU 247 and no smaller API cap it gives **242 image bytes per operation**, or `ceil(24,400/242) = 101` operations. Those counts are independent of the PHY advertised on the marketing page.

Now assume — strictly as a scheduling example — a **20 ms connection interval** with **four successful useful GATT operations per event**. The 101-operation case needs `ceil(101/4) = 26` event slots, a full-interval budget of **0.52 s**. The 1,356-operation case needs 339 slots, or **6.78 s**. Neither figure is an actual phone benchmark. A radio event may be too short for four operations; the phone's write queue, peripheral flash writes, acknowledgments and retries may add substantial delays. A finished sender callback is not interchangeable with a receiver-side verified commit.

The same calculation applied to a **216,000-byte** RAW4 buffer at 242 useful bytes per operation yields `ceil(216,000/242) = 893` operations, 224 event slots and **4.48 s of modeled interval slots** before other overhead. This is a useful planning contrast, not a recommendation to send all images uncompressed or to rely on that timing for a product specification.

| Input | 24,400 B @ MTU 23 | 24,400 B @ MTU 247 | 216,000 B @ MTU 247 |
|---|---:|---:|---:|
| Useful bytes / operation | 18 | 242 | 242 |
| Operations | 1,356 | 101 | 893 |
| Slots at 4 operations/event | 339 | 26 | 224 |
| Slot budget at 20 ms/event | 6.78 s | 0.52 s | 4.48 s |

A larger MTU often helps, but it is not sufficient. The negotiated link-layer data length, LE 1M/2M PHY, connection-event allocation, ATT write type, mobile OS flow control and receiver processing all matter. The [BLE Throughput & Transfer Planner](/en/tools/ble-throughput-calculator/) models more of those constraints and labels its assumptions. For the rationale and Python code, read [BLE File Transfers: Why MTU Alone Cannot Predict the Time](/en/articles/ble-transfer-budget-from-mtu-to-time/).

For a robust custom protocol, design the **failure path** at the same time as the happy path. Include a transfer identifier or version, declared length, chunk sequence or offset, receiver credits if needed, final checksum, explicit receiver-verified completion and a rule preventing a half-written file from reaching the display. On interrupted transfers, either resume from a known verified offset or discard the staging file. Avoid activating a new image merely because the last write was accepted by a phone API.

## 6. SPI clocking is not panel refresh

Consider the same hypothetical 800 × 540 RAW4 buffer: **216,000 bytes**. The ideal bit-clock time at **20 MHz SPI** is:

`T_SPI_ideal = 216,000 × 8 / 20,000,000 = 0.0864 s`

At 4 MHz the ideal value is 0.432 s. The difference is only **0.3456 s** of theoretical wire time, and actual driver transfer may include commands, gaps, DMA setup or row padding. It would therefore be misleading to infer “fast refresh” just because the MCU can output 20 MHz SPI clocks.

An e-paper controller generally needs a further sequence of panel power-up, voltage and waveform operations. Charged pigment particles must physically move, often through multiple transitions. The BUSY signal reports controller state as defined by the specific driver, not necessarily a calibrated optical endpoint. Some controllers have different BUSY polarities and mode-dependent meanings. If the display still appears to change after BUSY releases, only a reproducible optical criterion can quantify that extra time.

![Separating SPI transfer, refresh command, BUSY and optical completion](/images/p0/epaper-refresh-timeline.svg)

A sequential engineering budget may be written:

`T_total = T_image_prepare + T_transport + T_spi + T_trigger + T_busy + T_optional_optical_settle`

Only sum these terms directly if the implementation **does not overlap** them. For illustration, pretend the stages take 0.15 s for image preparation, **4.48 s** for the just-described modeled BLE event slots, **0.0864 s** ideal SPI clocking, **12.00 s** of hypothetical BUSY time and **0.20 s** of hypothetical settling, with trigger overhead assumed zero. The arithmetic is **16.9164 s**, but this is *not* an observed full update or a promise of timing. Its role is to force every component and assumption into view.

For a precise segmentation protocol, see [Why a Fast SPI Bus Does Not Make E-Paper Refresh Fast](/en/articles/epaper-refresh-timing-pipeline/). Do **not** experiment with undocumented OTP commands, panel voltages or unofficial high-speed waveforms simply to minimize BUSY time; image retention and long-term reliability can be affected. Our [InkBoy article](/en/articles/inkboy-epaper-game-boy-30fps/) illustrates why an experimental high update cadence should not be treated as a manufacturer-rated lifetime mode.

## 7. Keep power, buffering and update policy in the same design

E-paper's image persistence is useful because the *visible image* does not require LCD-style continuous refresh. It does **not** imply zero power for the whole product. Power is consumed by the MCU, radios, regulators, RAM and storage, plus the display controller and high-voltage rails when enabled. Idle current on an actual PCB may be dominated by a peripheral that was never put to sleep.

A useful energy report should separate **communication, preparation, active panel refresh and standby**. For a battery device, estimate energy per update as `E = ∫ V(t) I(t) dt`, not just `V × maximum-current × busy-time`. Record the measurement instrument's bandwidth, the source voltage and any Wi-Fi association overhead. For rarely changing displays, an approach that minimizes radio wake-up time may win even if its instantaneous data rate is not the highest.

Similarly, choose the update policy deliberately. Sending a photo every few seconds, showing a status label every minute and displaying a once-daily family picture have different requirements for image quality, residual ghosting, battery life and storage. Supported partial refresh modes may help where a panel and waveform explicitly allow them. A marketing feature on one controller should not be generalized to a different EPD technology family.

The [M5Stack PaperDIY engineering review](/en/articles/m5stack-paperdiy-esp32-s3/) discusses frame-memory and power-gating questions for an existing development kit. Treat it as a source-based case study, not evidence that the kit has undergone our own power-characterization campaign.

## 8. Test the boundaries, not just a happy-path photograph

A compact acceptance matrix makes failures diagnosable and repeatable. Here is a minimum starting point before a firmware milestone is declared complete:

| Layer | Test input | Failure it can reveal | Evidence to save |
|---|---|---|---|
| Image orientation | Four marked corner pixels | Mirror, rotation, incorrect traversal | RAW bytes, firmware version, panel photo |
| Packing | 5 × 2 RAW4 pattern | Nibble order and odd-width row padding | Expected/actual hex dump |
| Palette | One full-screen solid block per index | Mismatched native color codes | Index table, visible photos with lighting notes |
| Dithering | Same gradient/text at fixed settings | Banding, noisy text and color imbalance | Source + output PNG, tool version |
| BLE transport | Correct and deliberately truncated file | False success, offset mismatch, missing checks | Sender/receiver logs and hashes |
| Panel drive | Full refresh from distinct previous images | Ghosting and mode-dependent timing | Controller BUSY trace and timestamped video |
| Power | Update, sleep, wake-and-update | Idle leakage and battery sag | Current/voltage traces |
| Environmental | Temperatures within published panel ratings | Timing drift, degraded optical outcome | Temperature, mode, test report |

A reproducible test record needs enough metadata to explain *why two runs differ*. Include `panel_model`, `controller_revision`, `waveform_version`, `firmware_commit`, `temperature_C`, `image_hash`, `buffer_format`, `MTU`, `PHY`, `connection_interval_ms`, `t_receive_verified`, `t_spi_done`, `t_busy_idle` and the chosen optical completion definition where applicable. A raw timestamp alone is not meaningful without its start event.

Do not publish an attractive maximum result and hide the failed transfers. Run repeated trials (for example, ten or more per configuration), preserve failed and timed-out runs, and report median plus spread. A fresh power-on may behave differently from a steady-state update; explicitly label the test condition.

## 9. Troubleshoot by symptom

**The image is upside down or mirrored:** verify scan orientation, row traversal and per-byte bit/nibble order *before* editing the dithering algorithm. A corner-pattern test is faster than repeated photographic comparisons.

**The preview looks natural but the display is oversaturated or posterized:** freeze preprocessing settings, verify native color mapping and distinguish reference RGB from calibrated reflective measurements. The problem may be in the panel color model, not the JPG decoder.

**Transfer stalls near completion:** log receiver buffer occupancy, offset acknowledgments, phone API backpressure and expected checksum. Investigate reconnection and file-commit semantics before simply extending a timeout.

**The transfer is fast but the whole update feels slow:** place independent timestamps at sender completion, receiver verification, SPI completion, controller BUSY release and optical stability. Optimize the dominant stage; do not assume the radio is at fault.

**Fast updates create persistent artifacts:** revert to documented manufacturer-supported modes and investigate waveform history, temperature and panel specifications. Avoid treating a successful short demo as proof of lifetime suitability.

## 10. What this guide can support—and what still needs a lab

This article provides a reusable data budget, a binary format test vector, original calculations and a structured validation plan. Those are legitimate engineering deliverables on their own. They can help you write a protocol specification, select a buffer size, or identify the missing measurement in a vendor's performance claim.

What it **cannot** establish without further evidence is the color accuracy of a specific screen, the lifetime of an experimental waveform, the sustained wireless throughput of an actual phone/MCU combination, or the final latency and energy of a product. Those claims require raw device logs, operating conditions, test equipment details and repeatable measurements. If you use this guide to generate such results, keep the unedited evidence and distinguish your measurements from the estimates here.

### Further reading and working tools

- [E-Paper Image Converter — browser-local palette and RAW export](/en/tools/epaper-image-converter/)
- [BLE Throughput & Transfer Planner — explicit scheduling assumptions](/en/tools/ble-throughput-calculator/)
- [RAW4 nibble packing and color verification guide](/en/articles/epaper-palette-raw4-packing-guide/)
- [BLE GATT transfer budget and receiver verification](/en/articles/ble-transfer-budget-from-mtu-to-time/)
- [SPI transport versus the actual display update](/en/articles/epaper-refresh-timing-pipeline/)
- [Bluetooth Core Specification — ATT](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-54/out/en/host/attribute-protocol--att-.html)
- [E Ink — How electronic ink works](https://www.eink.com/tech/detail/How_it_works)

*Editorial method: numbers labeled as examples are derived from the given formulas. Images in this article are original schematic illustrations, not photographs of a validation bench. Corrections and supporting test evidence are welcome via the [About and editorial policy page](/en/about/).*
