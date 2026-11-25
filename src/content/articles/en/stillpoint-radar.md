---
title: "Stillpoint: A 60 GHz Radar That Sees the Room, Not the Person"
description: "An open-hardware ceiling sensor built around Infineon's BGT60TR13C and Silicon Labs' EFR32MG26: presence, posture and fall detection over Matter/Thread, with no camera and no cloud."
locale: en
translationKey: stillpoint-radar
pubDate: '2026-11-25'
category: open-source
series: open-hardware
contentType: deep
tags:
- Stillpoint
- 60 GHz Radar
- BGT60TR13C
- EFR32MG26
- Matter
- Thread
- Fall Detection
- Open Hardware
draft: false
sourceUrl: https://github.com/techmiguel/stillpoint
author: EmbeddedNote
seoTitle: 'Stillpoint: 60 GHz Radar for Presence and Fall Detection'
seoDescription: "Inside Stillpoint, an open-hardware ceiling sensor that uses a 60 GHz FMCW radar, on-device DSP and Matter over Thread to detect presence, posture and falls without a camera."
---

Most room-presence sensors force a trade-off. A camera can see posture and falls, but it also produces images of the people it watches. A passive infrared sensor is cheap and private, but it goes blind when someone sits still. Stillpoint takes a third path: a 60 GHz FMCW radar in a ceiling-mounted Ø60 mm puck. It counts people, estimates whether they are standing, sitting or lying down, and raises a fall alert. The result goes out over Matter/Thread. There is no camera, microphone, cloud account or image stream.

Miguel (techmiguel) published the project in October 2026 under CERN-OHL-S-2.0. The repository contains the KiCad schematic and four-layer board, a FreeCAD enclosure, C firmware and a Python reference implementation. It is a rev A design: the board has been checked and documented, but it has not yet been fabricated or validated as a physical unit.

| Item | Details |
| --- | --- |
| Project | Stillpoint, open-hardware ceiling sensor |
| Radar | Infineon BGT60TR13C, 60 GHz FMCW, 1 TX / 3 RX, antennas in package |
| Compute and radio | Silicon Labs MGM260P (EFR32MG26, Cortex-M33 + MVP), Matter / Thread / BLE |
| Board | Ø60 mm, 4 layers, 1.6 mm, ENIG, 74 placed parts |
| Sensing output | Presence, people count, 3D position, posture and fall state |
| Enclosure | Ø65 mm × 24 mm PETG puck on a Ø77 mm ceiling plate |
| License | CERN-OHL-S-2.0 |
| Status | Rev A design files; physical bring-up still open |

**GitHub:** [github.com/techmiguel/stillpoint](https://github.com/techmiguel/stillpoint)

![Stillpoint exploded view: ceiling plate, lid, Ø60 mm board and radome enclosure](/uploads/stillpoint/stillpoint-exploded.webp)

*The ceiling plate, lid, Ø60 mm board and the enclosure whose bottom face is the radome. Image: Miguel / Stillpoint.*

## A radar stack built for two kinds of motion

The radar sweeps 60.0–61.25 GHz, a 1.25 GHz span that gives 12 cm range resolution. Each frame contains 32 chirps of 128 samples from three receive channels, at 10 frames per second. The useful range is 7.7 m. The receive antennas are L-shaped, which provides both azimuth and elevation, so the output is a 3D position and a height rather than a bearing on a plane.

The processing chain is split early. One path uses MTI, Doppler, CFAR and angle-of-arrival to follow people who move. The other accumulates 10 seconds of phase and looks for the small chest displacement caused by breathing. The two paths are merged into 3D detections and passed to a tracker.

That tracker contains more room logic than the block diagram suggests. A confirmed track is only dropped quickly near an exit zone. In the middle of the room an occluded track is held for 60 seconds, or 120 seconds if it has shown breathing. Fans, mirror multipath and tracks that appear to pass through walls are handled separately. Each track is compressed into a 66-byte feature record and passed to a 14.6 KB int8 CNN every 0.5 seconds. The model decides posture and fall state; it never sees absolute x, y or range, so it cannot learn the geometry of the training rooms.

![Occlusion scenario: a still person is kept as an occluded track while another person walks in front](/uploads/stillpoint/stillpoint-occlusion.webp)

*In the occlusion test, the seated person is marked occluded and kept instead of being deleted. Image: Miguel / Stillpoint.*

![Empty room with a fan: the fan is learned as an interferer and not counted as a person](/uploads/stillpoint/stillpoint-fan.webp)

*An empty room with a running fan: the fan is learned as an interferer and does not become a person. Image: Miguel / Stillpoint.*

The still-person case is the reason for the second path. A conventional MTI filter removes anything that is not moving, which is exactly the person sitting quietly in a chair. The breathing path restores that person without lowering the motion threshold for everyone else.

## The fall decision is deliberately conservative

A fall is not a single classifier output. A suspicion is opened either by the model or by a fast descent to the floor. Confirmation requires the person to remain on the floor and still for 4 seconds. If that cannot be verified, the event is reported as uncertain rather than silently discarded. The project describes this as a fail-safe decision, not a medical diagnosis.

The same logic is exercised in simulation. The published regression set covers a real fall, lying on a bed and crouching. Only the fall reaches the confirmed state; the other two remain below the threshold. A separate scenario file covers occlusion, a fan in an empty room, a mirror reflection and a fall.

![Fall decision plots for a real fall, lying on a bed and crouching](/uploads/stillpoint/stillpoint-fall.webp)

*Height, vertical velocity and fall probability for a real fall, a bed and a crouch. Only the real fall reaches the confirmed state in this simulated run. Image: Miguel / Stillpoint.*

The README and project page both state that this is not a medical device. A fall alert is a notification, not a substitute for a pendant alarm, a check-in call or another safety measure.

## The board is a radar-first four-layer design

The PCB is a Ø60 mm, 1.6 mm four-layer board with ENIG finish and 74 placed parts. The radar sits on the bottom face and looks through the radome. The Matter/Thread module sits at the board edge with the antenna keep-out from its datasheet.

Power comes in over USB-C at 5 V. A TLV75733P produces 3.3 V; a TPS7A2018 produces the 1.8 V radar rail with 7 µVrms noise. Each radar supply domain (RF, PLL, VCO, analog, digital, loop filter and oscillator) has its own ferrite and a 100 nF / 1 µF / 10 µF filter lane. The smallest capacitor is placed closest to the BGA ball. An 80 MHz crystal oscillator sits 4 mm from the radar, with a 150 Ω series resistor.

The ground treatment is the part that takes the most space in the hardware notes. The BGT60TR13C is a 0.5 mm-pitch BGA. Layer 2 is solid ground. Layer 3 is the 3.3 V plane, but a solid ground island is cut into it directly under the radar. Inside the ball ring there are only ground vias, and a custom DRC rule keeps every other net off the inner layers under the chip. The radar control and data lines are split across two level translators on opposite faces so that no radar line has to cross another.

![Stillpoint board, top side: MGM260P at the edge, level translators and radar supply filters](/uploads/stillpoint/stillpoint-board-top.webp)

*Top side: the MGM260P module at the board edge, the level translators and the radar supply filters. Image: Miguel / Stillpoint.*

![Stillpoint board, bottom side: BGT60TR13C radar, 80 MHz oscillator and RGB LED](/uploads/stillpoint/stillpoint-board-bottom.webp)

*Bottom side: the BGT60TR13C radar, the 80 MHz oscillator and the RGB status LED. Image: Miguel / Stillpoint.*

The design reports ERC 0 errors, DRC 0 violations, matching schematic and PCB, and a BOM/CPL check against the board. Those are design checks. They do not prove that a fabricated board will pass bring-up, thermal soak or EMC.

![Stillpoint schematic, arranged by function: USB-C and power, radar supplies, level translators, MCU, radar and USB console](/uploads/stillpoint/stillpoint-schematic.webp)

*The schematic is arranged by function: USB-C and power, seven radar supply filters, level translators, MGM260P, BGT60TR13C, CP2102N and test points. Image: Miguel / Stillpoint.*

## The radome is part of the RF path

The enclosure is a Ø65 mm, 24 mm-tall PETG print on a Ø77 mm ceiling plate. Its bottom face is not a cosmetic cover. It is a 1.48 mm radome, exactly half a wavelength at 60.6 GHz for the chosen plastic, with about 0.15 dB one-way loss. The radar antennas sit 4.95 mm above it, one free-space wavelength.

The board is located by three supports and clamped by three lid posts at the same angles. The USB-C cable leaves through the lid, against the ceiling. A FreeCAD script loads the real board STEP and checks the shell, lid and radome for interference, as well as the ±60° antenna field of view for plastic.

![Radome section, transmission loss and FreeCAD parts](/uploads/stillpoint/stillpoint-mechanics.webp)

*Left: the dimensioned section. Centre: radome loss versus thickness. Right: the FreeCAD parts. Image: Miguel / Stillpoint.*

## What is verified, and what is not

The repository is unusually complete for a project at this stage: schematic, PCB, fabrication outputs, FreeCAD enclosure, C firmware, a Python reference, a feature contract, golden vectors and regression plots. The C implementation is compared with the Python reference frame by frame: the README reports the same counts, at least 99.8% identical quantised features, and identical postures, fall decisions and alarm times.

That is still simulation and host-side verification. The hardware notes say the board will not be ordered until the F2 kit phase closes, and the bring-up checklist still has 1:1 print checks, polarity checks, CPL rotation checks and first power-on open. The power, CPU and RAM figures in the architecture document are estimates, not measurements. There is no independent fall-detection dataset, no EMC report and no thermal test in the repository.

![C firmware and Python reference compared on four scenarios](/uploads/stillpoint/stillpoint-c-vs-python.webp)

*C firmware and the Python reference on the fall, bed, crouch and occlusion scenarios. Image: Miguel / Stillpoint.*

## Engineering check

| Claim | What is behind it |
| --- | --- |
| 60 GHz FMCW radar, 1 TX / 3 RX | BGT60TR13C datasheet and KiCad symbol; antennas are in the package |
| 12 cm range resolution, 7.7 m range | 1.25 GHz sweep and 128 samples per chirp, as documented in `docs/architecture.md` |
| Presence and breathing path | Python reference and C port; tested on simulated scenarios, not a physical room |
| Fall confirmation after 4 s | Decision state machine and regression plots; not clinically validated |
| Ø60 mm, 4-layer board | KiCad board, stackup and fabrication notes |
| 1.48 mm radome, 4.95 mm spacing | FreeCAD model and transmission plot; no measured antenna pattern |
| Matter over Thread | Firmware bridge and Matter cluster definition; no physical certification |

What we did not verify: a built board, real radar range and accuracy, fall sensitivity and false-alarm rate in a real home, power consumption, thermal behaviour, EMC, cybersecurity or privacy of the final firmware. The project is a carefully documented design, not a shipping product.

The interactive project page is a browser illustration, not recorded sensor data: https://techmiguel.github.io/stillpoint/. The repository does not currently include a demo video.

## Sources

- [Stillpoint repository](https://github.com/techmiguel/stillpoint)
- [`docs/architecture.md`](https://github.com/techmiguel/stillpoint/blob/main/docs/architecture.md)
- [`docs/hardware.md`](https://github.com/techmiguel/stillpoint/blob/main/docs/hardware.md)
- [Project page](https://techmiguel.github.io/stillpoint/)
