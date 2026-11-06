---
title: 'BLE File Transfers — Why MTU Alone Cannot Predict the Time'
description: 'A reproducible BLE transfer budget for embedded devices: useful GATT bytes, operation counts, connection-event limits, and what to measure on real hardware.'
locale: en
translationKey: ble-transfer-budget-from-mtu-to-time
pubDate: '2026-11-06'
category: connectivity
tags: [BLE, GATT, ATT MTU, ESP32, Throughput, Engineering]
author: EmbeddedNote
draft: false
seoTitle: 'BLE Transfer Time — MTU, Packets and Connection Events Explained'
seoDescription: 'Calculate BLE GATT payload efficiency, application packet counts, and scheduling limits—with auditable examples and a practical ESP32 measurement checklist.'
---

A BLE link showing **2 Mbps PHY** does not move a 24 KB image at 250 kB/s. The PHY bit rate is only one layer of the system. The application sends GATT values, those values have ATT and L2CAP headers, the controller may fragment them into link-layer packets, and connection events determine when packets can actually be exchanged. The receiving firmware must also keep up.

This article builds a transfer budget from first principles. The numbers below are **calculated scenarios, not benchmark results**. They help decide what to instrument before promising an update time for an e-paper product, sensor logger, or firmware updater.

![BLE transfer layers and scheduling diagram](/images/p0/ble-transfer-layers.svg)

## Start with useful bytes, not headline speed

For an ordinary ATT **Write Command** or **Notification**, the maximum attribute value in one PDU is `ATT_MTU − 3`: one byte for the ATT opcode and two for the attribute handle. This is defined by the [Bluetooth Core ATT specification](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-54/out/en/host/attribute-protocol--att-.html). It is not a guarantee that a phone API or peripheral accepts a value of that length in every transfer.

If the application adds a two-byte sequence/header field, the maximum **file bytes** per operation are:

`useful_bytes = min(ATT_MTU − 3, application_or_API_cap) − app_header_bytes`

For an assumed negotiated MTU of 247 and no smaller API cap, that is `247 − 3 − 2 = 242 B`. For the default ATT MTU of 23, it is just `23 − 3 − 2 = 18 B`.

| Model input | Small-MTU case | Larger-MTU case |
|---|---:|---:|
| Negotiated ATT MTU | 23 B | 247 B |
| Application header | 2 B | 2 B |
| Useful file bytes per operation | 18 B | 242 B |
| File size | 24,400 B | 24,400 B |
| Operations needed, rounded up | 1,356 | 101 |

The same 24,400-byte file takes more than **13 times as many GATT operations** in the first case. Note that 24,400 decimal bytes is not the same as 24 KiB (24,576 bytes). Always label the unit in a test report.

## Connection events set another ceiling

Suppose, *for illustration only*, the scheduler and both devices can sustain four useful operations per 20 ms connection interval. A simple upper-bound application rate is:

`242 B/op × 4 op/event ÷ 0.020 s = 48,400 B/s`

There are `ceil(101/4) = 26` event slots for the larger-MTU example. If we budget each full interval, the schedule accounts for `26 × 20 ms = 520 ms`, **before** setup, acknowledgments at the application layer, queue backpressure, retries, flash writes, or display refresh. This is an interval-slot estimate, not a measured wall-clock time and not an exact lower bound on radio completion: the last packet may leave partway through an event.

Under the same optimistic four-operations-per-event assumption, the 23-byte MTU case needs `ceil(1356/4) = 339` slots, or **6.78 s of scheduled intervals**. Real schedulers may allow fewer or more than four operations, so this comparison isolates the effect of one assumption instead of predicting a specific phone.

A PHY switch from LE 1M to LE 2M can reduce the radio time of supported packets. It does not necessarily double application throughput. If operations per event, host flow control, the receive queue, or flash programming remain the bottleneck, the PHY gain may be small. Conversely, improved data length and event scheduling can matter more than an MTU change alone. The [ESP32-C3 datasheet](https://documentation.espressif.com/esp32-c3_datasheet_en.html) lists LE 1M/2M and Data Length Extension support, but actual negotiation must be observed on the specific phone and firmware.

## Do not confuse Write Command with Write Request

A Write **Request** has an ATT response and generally allows only one outstanding request on the same ATT bearer until its response arrives. A Write **Command** has no ATT response; it can offer higher throughput, but the sender must respect buffers and decide how to detect missing or incomplete application data. “Write without response” does **not** mean “infinite queue with guaranteed delivery.” Link-layer reliability and application-level end-to-end completeness are different things.

For practical file transfers, a robust protocol can use a start message carrying total length and format version; sequenced chunks; receiver credit or explicit pacing; and a final length plus checksum verification. A reconnect or reset must not silently turn an incomplete file into a successful update. For a display device, verify the image before triggering a refresh.

## A reproducible planning script

The following standard-library Python snippet reproduces the table and intentionally reports a **modeled scheduling budget**, not measured throughput:

```python
from math import ceil

def budget(file_bytes, att_mtu, app_header=2, ops_per_event=4, interval_ms=20):
    useful = att_mtu - 3 - app_header
    if useful <= 0 or ops_per_event <= 0 or interval_ms <= 0:
        raise ValueError('Invalid transport assumptions')
    operations = ceil(file_bytes / useful)
    event_slots = ceil(operations / ops_per_event)
    return useful, operations, event_slots, event_slots * interval_ms / 1000

for mtu in (23, 247):
    print(mtu, budget(24400, mtu))
# 23  (18, 1356, 339, 6.78)
# 247 (242, 101, 26, 0.52)
```

The [EmbeddedNote BLE Throughput & Transfer Planner](/en/tools/ble-throughput-calculator/) adds LL fragmentation, PHY airtime and adjustable connection-event assumptions to this simplified arithmetic. Its results are estimates too. If a target device's maximum accepted write size is smaller than `ATT_MTU − 3`, use that smaller value.

## How to turn the model into a defensible measurement

On a production candidate, capture **at least ten complete transfers per configuration** and record the median and worst observed run rather than reporting the best attempt alone. Log the phone model and OS version, peripheral firmware, negotiated ATT MTU, PHY, LL data length if observable, connection interval, GATT operation type, payload hash, retry count, and timestamps at the following boundaries:

1. Transfer requested by the app.
2. First chunk accepted by the sender's API.
3. Last chunk accepted by the sender's API.
4. Receiver has assembled and checked the entire file.
5. Downstream work (flash commit or display update) finishes.

A phone API callback may indicate that a request entered or completed a platform queue; it is **not automatically proof that the peripheral has committed the file**. Use a receiver-side completion event and checksum to close the measurement. Test both strong and marginal RF conditions, and avoid mixing reconnect time with steady-state transfer throughput without labeling it.

## What to change first

If transfer time is poor, measure the bottleneck before increasing every parameter. A default 23-byte MTU points toward negotiation and API limitations. Long gaps between accepted writes point toward host pacing, event allocation or receiver backpressure. Fast transport followed by slow display update points toward the display pipeline, not BLE. For occasional large images, a BLE control channel plus a separately measured Wi-Fi data path may be preferable—but the crossover depends on wake-up, association, energy use, and the application.

**Evidence boundary:** The packet formulas follow the Bluetooth specification; the worked event budgets are original calculations using stated assumptions. No phone/ESP32 pair was physically benchmarked for this article. Hardware observations should be published separately with raw logs.

**Primary references:** [Bluetooth Core—ATT](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-54/out/en/host/attribute-protocol--att-.html) · [ESP32-C3 technical datasheet](https://documentation.espressif.com/esp32-c3_datasheet_en.html) · [BLE planner and model limits](/en/tools/ble-throughput-calculator/).
