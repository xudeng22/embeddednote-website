---
title: 'How the BLE Throughput Model Works'
description: 'The exact arithmetic behind a BLE transfer estimate: ATT value size, per-packet airtime, and how many writes fit in a connection event. Includes a worked 240 KB example.'
locale: en
translationKey: ble-throughput-model
pubDate: '2026-11-11'
category: connectivity
tags:
- BLE
- Throughput
- GATT
- Modeling
- Verification
draft: false
author: EmbeddedNote
contentType: deep
series: ble
seoTitle: 'How the BLE Throughput Model Works (With Numbers)'
seoDescription: 'Step-by-step BLE throughput arithmetic: MTU to value size, airtime per packet, writes per connection event, and why 2M PHY sometimes changes nothing.'
---

Every "BLE throughput calculator" is a model. The useful question is not what number it returns, but which assumptions produced it. This page lays out the arithmetic behind ours, line by line, so you can check it against your own link or rebuild it in a spreadsheet.

The worked example uses the defaults: 240 KB of application data, MTU 247, LE 2M PHY, 30 ms connection interval, 15 ms event length, encrypted link.

![Packet layout from link-layer header through ATT payload and MIC](/images/p0/ble-packet-layout.svg)

## Step 1: from MTU to usable bytes per operation

ATT reserves three bytes for the opcode and attribute handle. So a 247-byte MTU carries 244 bytes of value. If your application puts its own header inside that value — a chunk index, a sequence number — subtract it now, because it repeats on every operation:

```
value   = min(MTU − 3, codec_chunk_limit)
payload = value − app_header
```

With MTU 247 and no application header, every write carries **244 bytes**. For 240,000 bytes that is `ceil(240 000 / 244) = 984` write operations, the last one carrying 148 bytes.

This is the first place estimates go wrong: dividing the file size by the MTU instead of by the value size gives 972 operations, which understates the count by 1.2%.

## Step 2: what one operation costs on the air

An ATT write does not travel alone. Inside the link-layer PDU you also carry the L2CAP header and the ATT header:

| Field | Bytes |
| --- | ---: |
| L2CAP basic header | 4 |
| ATT opcode + handle | 3 |
| GATT value | 244 |
| **LL payload (data)** | **251** |
| MIC (encrypted link only) | 4 |

251 bytes is exactly the Data Length Extension ceiling, and the MIC counts **inside** that ceiling, not after it. An encrypted MTU-247 link therefore cannot fit the frame in one PDU: it becomes two, carrying 247 and 4 data bytes respectively. Turn encryption off and the same write needs only one.

Around each PDU sit the parts that are not data at all: preamble (2 bytes at 2M), access address (4), LL header (2), CRC (3), an empty acknowledgement, and two inter-frame spaces of 150 µs.

At LE 2M, one write-and-ack pair with the two-PDU split costs about **1,812 µs**. At LE 1M it is **2,992 µs**.

## Step 3: how many fit in one connection event

At these sizes the radio is rarely the binding constraint — the scheduler is. With a 15 ms event:

- 15,000 µs ÷ 1,812 µs ≈ 8 operations could fit at 2M.
- 15,000 µs ÷ 2,992 µs = 5 operations could fit at 1M.

But the model also assumes the host and controller only pipeline **four** writes per event, a deliberately conservative stand-in for what phones do. So:

```
per_event = min(floor(event_ms × 1000 / pdu_us), max_writes_per_event) = min(8, 4) = 4
events    = ceil(984 / 4) = 246
wall time = 246 × 30 ms = 7 380 ms
```

**7.38 seconds**, not the ~1.9 s that "240 KB at 1 Mbps" suggests.

## The result that surprises people

Run the same example at LE 1M instead of LE 2M:

| | LE 2M | LE 1M |
| --- | ---: | ---: |
| Airtime per write + ack | 1,812 µs | 2,992 µs |
| Fits in a 15 ms event | 8 | 5 |
| Writes allowed per event | 4 | 4 |
| Events needed | 246 | 246 |
| **Wall time at 30 ms** | **7.38 s** | **7.38 s** |
| Actual radio time | 1.78 s | 2.94 s |
| Effective goodput | 1.08 Mbit/s | 0.65 Mbit/s |

The 2M PHY cuts the radio time by 40% and changes the wall time by **zero**, because the four-writes-per-event cap binds. Raise the cap to the air limit of 8 and the same transfer finishes in **3.69 s** — a 2× improvement that no PHY change can give you.

If your estimate says "upgrade to 2M and it will be twice as fast", the model is missing the event cap. That is the most common error in BLE throughput claims.

## What the model deliberately ignores

- **Controller scheduling.** Real controllers decide how many PDUs fit per event, and phones are conservative.
- **Host queues.** iOS requires `canSendWriteWithoutResponse`; Android's write queue depth varies by OEM.
- **Receiver-side costs.** Flash page writes, file system commits and application processing often dominate once the radio is fast enough.
- **Retransmissions.** The tool exposes a retry percentage as a linear penalty; it is not a packet-error model.
- **Connection parameter changes.** The peer can renegotiate mid-transfer, and some phones do.

Any of these can move a real measurement by 2× in either direction. That is why the page says "estimate", not "throughput".

## Calibrating it against reality

Measure once, then adjust two numbers: writes per event and retry percentage. Everything else is spec-derived and should match within a few percent.

A usable measurement records: phone model and OS, negotiated MTU, actual PHY, connection interval as reported by a sniffer or the peripheral, bytes transferred, and the timestamp at sender completion **and** at receiver verification. Without the last one you are measuring your own buffer, not the link.

## Where the numbers come from

- Bluetooth Core Specification: the ATT header (opcode + handle), the L2CAP basic header, the LL packet format, preamble and CRC lengths, the 251-byte LL Data PDU ceiling with Data Length Extension, and the rule that the PDU length includes the MIC on an encrypted link.
- Nordic Semiconductor's throughput notes for the accounting of inter-frame spacing and acknowledgements.
- Platform constraints (`maximumWriteValueLength`, `canSendWriteWithoutResponse`, Android 14's 517-byte MTU request) come from platform documentation, not from measurement.

The [BLE Throughput & Transfer Planner](/en/tools/ble-throughput-calculator/) implements exactly this arithmetic; every field in the tool maps to a step on this page. If you find a place where the two disagree, the article is wrong and we will fix it.
