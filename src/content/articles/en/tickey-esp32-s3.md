---
title: This ESP32-S3 Color E-Paper Card Raised $850K on Kickstarter
description: TICKEY packs a 3.7-inch color e-paper display, ESP32-S3, Wi-Fi, BLE, and NFC into a slim portable card. A look at its hardware and
  refresh modes.
locale: en
translationKey: tickey-esp32-s3-color-epaper
pubDate: '2026-09-29'
category: display
draft: false
tags:
- ESP32-S3
- E-Paper
- TICKEY
- Kickstarter
- Embedded Systems
seoTitle: 'TICKEY: ESP32-S3 Color E-Paper Card Raises $850K'
seoDescription: 'Inside TICKEY: a 3.7-inch color e-paper display, ESP32-S3, wireless connectivity, NFC, refresh modes, and room for custom firmware.'
---

Color e-paper has made its way into plenty of products over the past couple of years: desktop calendars, digital photo frames, electronic shelf labels, and information displays. Most follow the same idea—put a low-power screen in a fixed location. TICKEY takes a different route. It packs a 3.7-inch color e-paper display into an aluminum body only slightly larger than a credit card, then adds a keyring, magnetic mounting, and a desktop stand.

You can clip it to a backpack to show pixel art, use it as a conference badge or digital sticky note, or turn it into a business card with a QR code. Change the image from your phone, wait for the display to refresh, and the picture stays put even when the power is off.

![TICKEY color e-paper card beside a smartphone](/uploads/tickey/tickey_01.webp)

**Project:** [TICKEY on Kickstarter](https://www.kickstarter.com/projects/enilinx/ticket-refresh-it-new-clip-it-on-carry-your-moment)

At first glance, it looks more like a novelty accessory than a serious electronics project. Inside, though, is a complete little embedded system. An ESP32-S3 handles wireless connectivity and image processing, the color e-paper handles the display, and NFC lets a phone open a link with a tap. A 360 mAh battery supplies the power needed for refreshing the screen and making wireless connections. The companion app takes care of image editing, templates, and sending content to the device.

The Kickstarter campaign drew 7,909 backers and raised HK$6.71 million (about US$850,000), far exceeding its original HK$10,000 target. That is quite a result for a small screen that cannot play video and takes several seconds to update. The attraction is not high-end hardware. TICKEY has found a use case where e-paper’s ability to hold an image without continuous power actually matters.

![TICKEY mobile app and wireless image transfer workflow](/uploads/tickey/tickey_02.webp)


## A Color Card That Keeps Its Image

The front of TICKEY is a 3.7-inch color e-paper display with a resolution of 720 × 480 pixels, a pixel density of approximately 234 PPI, and support for more than 48 native colors. Unlike an LCD, it has no backlight, and unlike an OLED, it does not need to keep its pixels powered to maintain the image. Once an update is complete, the pigment particles remain in place. Even if the battery runs flat, the last image stays visible.

![TICKEY color e-paper accessory attached to a handbag](/uploads/tickey/tickey_03.webp)

There are two main color refresh modes: a full refresh takes around 13 seconds, while fast mode takes about 3 seconds. For simple black-and-white pixel animation, an individual update takes roughly 1 second. None of this is suitable for video or fluid on-screen interaction. But waiting three seconds to change a photo or update a conference badge is a different matter.

According to the team’s laboratory figures, one charge can deliver more than 1,000 refreshes, with battery life of around two months when the device is used as an everyday accessory. There is an important distinction here: e-paper uses almost no power to hold a static image, but Wi-Fi activity, Bluetooth transfers, image decoding, and the high-voltage circuitry used for refreshing the panel still consume energy. Update the weather and to-do list frequently, and battery life will drop accordingly.

![TICKEY displaying a to-do list on its desktop stand](/uploads/tickey/tickey_04.webp)

The device measures 111 × 62 × 3.8 mm (4.37 × 2.44 × 0.15 in), weighs 45 g (1.59 oz), and uses a CNC-machined aluminum enclosure. Swappable front covers add some personality, but the physical buttons and removable parts come with a trade-off: the team explicitly says the device is not waterproof.

![Sending a photo from a smartphone to a TICKEY card](/uploads/tickey/tickey_05.webp)


## ESP32-S3 Brings Wireless Connectivity and a Familiar Development Ecosystem

TICKEY is built around the ESP32-S3, a familiar chip to embedded developers. It combines two Xtensa LX7 CPU cores running at up to 240 MHz with 2.4 GHz Wi-Fi and Bluetooth Low Energy. Here, the chip receives images from the phone, handles scaling, cropping, and color mapping, and sends the resulting data to the e-paper display. It also manages the buttons, power state, and different display templates.

The user selects and edits a photo on the phone, then sends it to the device over BLE or Wi-Fi. The team says the complete image-change process takes roughly 30 seconds. Basic image changes and the clock can work offline without requiring an online account; connected features such as weather and to-do information need network services.

![TICKEY thin aluminum enclosure, 3.8 mm thick and 45 g](/uploads/tickey/tickey_06.webp)

Storage comes in two versions. The standard model has 8 MB for the official firmware, cached images, and commonly used templates. The Developer Edition increases that to 128 MB while keeping the same core hardware, leaving more room for e-reader firmware, large image collections, and community-built applications. The team also emphasizes open firmware and the established Arduino and ESP32 development ecosystem as a way to make customization more accessible.

For developers, that extra storage is useful for more than keeping a few additional photos. It opens the door to an offline photo album, a Pomodoro timer, a meeting-room schedule, or a device-status dashboard. The card could also periodically pull Home Assistant or server-monitoring data from the local network.

![TICKEY color e-paper card showing a parrot photograph](/uploads/tickey/tickey_07.webp)

Alongside Wi-Fi and BLE, TICKEY has an NFC interface compliant with ISO 15693. Its role is deliberately limited: it passes links to a phone, such as a personal website, portfolio, or event page. It is not intended to impersonate an access card or make payments.

![TICKEY NFC digital business card demonstrated with a smartphone](/uploads/tickey/tickey_08.webp)

Driving a monochrome e-paper panel is relatively straightforward. Color e-paper is less forgiving. A photo sent from a phone may contain millions of colors, but this display has a native palette of only around 48. The firmware has to reduce the color space, then use dithering and color mapping to preserve as much of the original image’s detail and tonal range as possible.

Poor mapping produces large patches of flat color on faces, visible banding in gradient skies, and muddy edges around text. TICKEY uses a display-driver solution from Modos, and fast refreshes with good color detail are among the features highlighted in the campaign.

![TICKEY e-paper development setup beside a laptop](/uploads/tickey/tickey_09.webp)

Refresh speed also depends on waveform control. Updating e-paper is not as simple as writing one frame into display memory. The controller has to apply carefully timed voltage sequences to move the different pigment particles. A high-quality full refresh taking 13 seconds suggests a more conservative balance among color accuracy, ghosting, and speed. The 3-second fast mode is intended for times when getting a new image onto the screen matters more than achieving the best possible image quality.

![TICKEY technical specifications and dimensions](/uploads/tickey/tickey_10.webp)

A single 720 × 480 RGB888 frame occupies roughly 1 MB of memory. Even when the output is converted to a limited palette, decoding and dithering still require working buffers. The ESP32-S3 has enough processing capability for the job, but the slim enclosure leaves limited headroom for power consumption and heat.

A sensible division of work is to let the phone handle editing and some of the preprocessing, while the device focuses on communication, buffering, data validation, and driving the display. TICKEY’s app follows that approach: selection, editing, and uploading all happen on the phone, rather than forcing a complicated touch interface onto a tiny device.

One of TICKEY’s strengths is that it is light enough to carry without closing off the hardware to developers. At 45 g, it can genuinely hang from a bag, while the magnets and stand let the same device move onto a refrigerator or desk. The ESP32-S3, open firmware, and extra storage in the Developer Edition also leave room to use it independently of the official app.

A custom project need not be complicated. The card could fetch a daily calendar image from a local server each morning, switch to a desk-availability sign at the office, display a name and QR code during a meeting, and show transit arrivals or the weather on the way home. None of these jobs calls for constant updates. In fact, their slower pace suits e-paper rather well.
