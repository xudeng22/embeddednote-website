---
title: Turn a Raspberry Pi Pico W into a USB Wi-Fi Adapter—No Custom Drivers Needed
description: pico-usb-wifi turns a Raspberry Pi Pico W into a USB CDC-NCM network adapter. Explore its Layer 2 bridge, setup model, performance and trade-offs.
locale: en
translationKey: pico-usb-wifi
pubDate: '2026-11-03'
category: open-source
tags:
- Raspberry Pi Pico W
- RP2040
- USB CDC-NCM
- Wi-Fi
- Open Source
draft: false
sourceUrl: https://gitlab.com/baiyibai/pico-usb-wifi
author: EmbeddedNote
seoTitle: Turn a Raspberry Pi Pico W into a USB Wi-Fi Adapter—No Custom Drivers Needed | EmbeddedNote
seoDescription: pico-usb-wifi turns a Raspberry Pi Pico W into a USB CDC-NCM network adapter. Explore its Layer 2 bridge, setup model, performance and trade-offs.
---

A Raspberry Pi Pico W is usually the device you connect to a network, not the device that gives another computer network access. The open-source **pico-usb-wifi** project reverses that relationship: plug a Pico W into a host over USB, connect it to Wi-Fi, and the host sees a USB Ethernet interface rather than a wireless adapter that needs its own Wi-Fi stack.

That distinction is the point. The project uses the USB Communications Device Class Network Control Model (**CDC-NCM**) for data and a separate **CDC-ACM** serial interface for management. Its goal is a network connection that behaves like an Ethernet link from the host's point of view, with Wi-Fi configuration handled on the Pico W.


## Why USB Ethernet instead of a USB Wi-Fi dongle?


Most USB Wi-Fi adapters expose a radio to the operating system, which then needs a compatible chipset driver and a functioning wireless networking stack. pico-usb-wifi takes a different route. The **Infineon CYW43439** radio connects to the Wi-Fi network on the Pico W side. The RP2040 handles the handoff between the wireless link and the host-facing USB network device.

To the computer, this is a standard USB network interface. That can be useful on machines where installing a vendor-specific wireless driver is undesirable, or when you want to isolate Wi-Fi association and credential management from the host. It is not a universal promise of plug-and-play behavior on every operating-system version: CDC-NCM/ACM driver availability and configuration still matter.


![Project overview: a Pico W presents Wi-Fi connectivity to a host through USB CDC-NCM.](/uploads/pico-usb-wifi/pico-usb-wifi-01.webp)

*Project overview: a Pico W presents Wi-Fi connectivity to a host through USB CDC-NCM.*


## The interesting part: a transparent Layer 2 bridge


The firmware is designed as a **Layer 2 bridge**, not a small NAT router. It forwards Ethernet traffic between the USB and wireless sides while preserving the host's end-to-end network identity. The source describes a design with **no private downstream subnet, no NAT and no port-forwarding setup**, and support for both IPv4 and IPv6.

In practical terms, the upstream access point is responsible for ordinary network connectivity, while the host runs its usual IP configuration over what appears to be Ethernet. The Pico W is a bridge, rather than an additional address-translation hop. This is a more ambitious design than simply exposing a serial terminal or HTTP proxy over Wi-Fi.


![Connection model: the host talks CDC-NCM over USB, with Pico W bridging traffic to the Wi-Fi access point.](/uploads/pico-usb-wifi/pico-usb-wifi-03.webp)

*Connection model: the host talks CDC-NCM over USB, with Pico W bridging traffic to the Wi-Fi access point.*


## Management stays separate from network traffic


The project exposes **CDC-ACM** as an out-of-band management and debugging console. You can use that serial channel to scan for nearby networks, connect to an access point and save Wi-Fi credentials without relying on the newly created IP connection already working. The documented authentication options include **WPA2-PSK, WPA3-SAE and open networks**.

Keeping configuration separate from the data path is good engineering: if the connection to the access point drops, the USB serial control channel can remain available for diagnostics. It also avoids forcing the host to install a dedicated Wi-Fi management application just to get the bridge online.


## Performance: useful, but not a high-speed dongle


The source material supplied for this article reports **approximately 4.75 Mbit/s average throughput**. Treat that as a project-reported measurement, not an independent benchmark or a guaranteed rate in every RF environment. Actual results depend on signal quality, USB processing overhead, firmware revision and the host.

This is best viewed as a clever connectivity adapter for modest bandwidth needs, rather than a substitute for a modern high-throughput USB Wi-Fi 5 or Wi-Fi 6 device. Before using it for sustained data collection or production equipment, measure throughput, latency and reconnection behavior with your own workload.


![Example desk setup showing a Raspberry Pi Pico W connected to a laptop by USB.](/uploads/pico-usb-wifi/pico-usb-wifi-02.webp)

*Example desk setup showing a Raspberry Pi Pico W connected to a laptop by USB.*


## Where it makes sense—and where it does not


pico-usb-wifi is attractive for embedded Linux testing, network experimentation, small host devices and situations where a USB Ethernet device is easier to support than a vendor-specific Wi-Fi dongle. The transparent bridge and independent serial management channel make it especially interesting to engineers studying network interfaces and USB device classes.

The main caveats are the modest reported throughput, dependency on a correctly supported host USB class driver, and the need to validate network behavior on your exact access point and host. You should also review firmware provenance and Wi-Fi credential storage before deploying it beyond a lab.


## Project links


**Source code:** https://gitlab.com/baiyibai/pico-usb-wifi

The project is an instructive example of getting more out of the RP2040 and CYW43439 by moving the networking boundary to USB. The useful idea is not that a Pico W can replace every Wi-Fi adapter; it is that a tiny microcontroller can present an ordinary network interface while hiding most of the wireless plumbing from the host.
