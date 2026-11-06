---
title: 'BLE 传图到底要多久？从 MTU 算到连接事件，而不是只看 2 Mbps'
description: '从 ATT MTU、应用层分包到连接事件，给出可复算的 BLE 传输预算，并解释怎样用实机日志验证。'
locale: zh
translationKey: ble-transfer-budget-from-mtu-to-time
pubDate: '2026-11-06'
category: connectivity
tags: [BLE, GATT, ATT MTU, ESP32, 吞吐率, 工程实践]
author: EmbeddedNote
draft: false
seoTitle: 'BLE 吞吐与传输时间计算——MTU、分包与连接事件'
seoDescription: '用 24,400 字节文件详解 ATT MTU、有效负载、GATT 操作次数和连接事件预算，附可运行 Python 计算脚本与测试清单。'
---

BLE 链路协商成 2 Mbps PHY，并不等于 24 KB 图片就能按 250 kB/s 送到设备。PHY 只是空口编码速率。手机交给 GATT 的数据还要经过 ATT、L2CAP、链路层分包，什么时候能发还取决于连接事件；接收端有没有空闲缓冲和处理能力，同样会影响速度。

下面用一组**明确假设的计算案例**把事情算清楚。请注意，本文没有把模型数据包装成手机和 ESP32 的实测结果。

![BLE 协议分层与连接事件时序示意](/images/p0/ble-transfer-layers.svg)

## 第一笔账：每次写入真正能装多少文件字节

普通 ATT Write Command 或 Notification 单次属性值上限为 `ATT_MTU − 3`，其中 3 字节用于 ATT 操作码和句柄。依据见 [Bluetooth Core ATT 规范](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-54/out/en/host/attribute-protocol--att-.html)。但手机 API、固件缓冲区可能给出更小的上限，实际要取最小值。

假定应用协议每个分包携带 2 字节序号/控制字段：

`单包有效文件字节 = min(ATT_MTU − 3, API 可接受长度) − 2`

| 项目 | MTU 23 | MTU 247 |
|---|---:|---:|
| 每次写入有效文件字节 | 18 B | 242 B |
| 文件大小（十进制） | 24,400 B | 24,400 B |
| 所需 GATT 操作数 | 1,356 | 101 |

仅仅改变有效包长，操作次数就相差超过 13 倍。还要区分 **24,400 B 与 24 KiB（24,576 B）**，不要在测试记录里混用。

## 第二笔账：连接间隔与每事件操作次数

再假定连接间隔为 20 ms，且手机、控制器和从设备能稳定做到**每个事件 4 次有效操作**。这只是模型参数，不代表任意 iPhone 或安卓手机的上限。

大 MTU 场景的理想应用层预算是 `242 × 4 ÷ 0.020 = 48,400 B/s`。101 次操作需要 `ceil(101/4)=26` 个连接事件槽。按完整间隔预留就是 `26×20 ms=0.52 s`，还没有包含配对、传输启动、缓冲阻塞、重传、文件校验和刷屏。这个 0.52 s 是**保守地按完整事件槽计的模型预算**，不是无线测试结果，也不是精确的最后一字节空口完成时间。

同样按每事件 4 次操作，MTU 23 需要 `ceil(1356/4)=339` 个槽，即 **6.78 s**。实际每事件能发送几包，受连接事件长度、数据长度扩展、双端软件调度和链路质量影响。

ESP32-C3 官方资料支持 LE 1M/2M 和 Data Length Extension，但“芯片支持”与“本次连接已协商成功”是两回事；[官方数据手册](https://documentation.espressif.com/esp32-c3_datasheet_en.html)不能代替抓包记录。

## Write Request 和 Write Command 怎么选

Write Request 需要对端 ATT 响应，同一 ATT bearer 上存在请求—响应时序约束。Write Command 不带 ATT 层响应，适合提高发送效率，但不代表可以无限写入而没有队列溢出风险。链路层可靠性也不等于设备已经把整张图片写入 Flash。

工程上至少应设计：文件总长度、版本号、分包序号、缓冲/流控策略，以及最后的长度和校验值核对。设备接收完成、校验通过之后再触发电子纸刷新。中途掉线应该允许清晰地回滚或恢复，而不是误报成功。

## 用代码复算，而不是凭印象估速度

```python
from math import ceil

def ble_budget(total, mtu, app_header=2, ops=4, interval_ms=20):
    useful = mtu - 3 - app_header
    if useful <= 0 or ops <= 0 or interval_ms <= 0:
        raise ValueError('invalid assumptions')
    packets = ceil(total / useful)
    slots = ceil(packets / ops)
    return useful, packets, slots, slots * interval_ms / 1000

print(ble_budget(24400, 23))   # (18, 1356, 339, 6.78)
print(ble_budget(24400, 247))  # (242, 101, 26, 0.52)
```

需要更细的 LL 分片、1M/2M PHY 空口时间和连接事件约束，可以打开 [EmbeddedNote BLE Throughput & Transfer Planner](/zh/tools/ble-throughput-calculator/)。注意它是**规划模型**，不是性能认证报告。

## 真正的测试应该记录什么

建议每组配置至少做 10 次完整传输，分别记录手机型号与系统版本、固件版本、协商 MTU、PHY、连接间隔、分包大小、重传次数、总长度、文件 Hash，以及五个时间点：App 开始传输、第一包接受、最后一包接受、设备端组包并校验完成、Flash 或显示流程完成。

特别要小心：手机 API 的写入回调未必等于设备已经收到并保存文件。一定要用**设备端确认和最终校验**闭环。测试强信号和弱信号条件，并把建链时间与稳定连接后的纯传输时间分开统计。

**工程判断：** 首先定位瓶颈，再决定调 MTU、连接参数、批量发送窗口还是接收缓存。BLE 已经传完但屏幕还在刷，就不该把所有问题归咎于蓝牙。大图也可以考虑 BLE 控制、Wi-Fi 传图，但要算清 Wi-Fi 建链时间和能耗。

**证据声明：** 文中的分包公式依据 Bluetooth 规范；0.52 s、6.78 s 均为明确假设下的原创推算，没有使用未经核实的“实测跑分”。

**参考：** [Bluetooth ATT 规范](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-54/out/en/host/attribute-protocol--att-.html) · [ESP32-C3 数据手册](https://documentation.espressif.com/esp32-c3_datasheet_en.html) · [本站 BLE 工具](/zh/tools/ble-throughput-calculator/)。
