---
title: 'Berkeley Humanoid Lite: An Open-Source Robot Built with 3D Printing, CAN, and Reinforcement Learning'
description: Berkeley Humanoid Lite aims for a sub-$5,000 humanoid robot built using printed structures, modular BLDC actuators, CAN networking and reinforcement learning.
locale: en
translationKey: berkeley-humanoid-lite
pubDate: '2026-08-31'
category: open-source
tags:
- Robotics
- CAN
- 3D Printing
- Reinforcement Learning
draft: false
seoTitle: 'Berkeley Humanoid Lite: Open-Source Robot Design'
seoDescription: Berkeley Humanoid Lite aims for a sub-$5,000 humanoid robot built using printed structures, modular BLDC actuators, CAN networking and reinforcement learning.
---

There are plenty of humanoid robot projects, but most remain out of reach for individual developers. Some are simply too expensive; others publish a demo video and a small amount of code while keeping the mechanical design, actuators, control network, and training pipeline private.

Berkeley Humanoid Lite, from UC Berkeley's Hybrid Robotics group, takes a more open approach. The team has published the project on GitHub with an explicit goal: a humanoid robot costing less than $5,000, with hardware and software that others can build and modify.

![berkeley humanoid lite — figure 1](/uploads/berkeley-humanoid-lite/berkeley-humanoid-lite-01.webp)

**GitHub:** https://github.com/HybridRobotics/Berkeley-Humanoid-Lite  
**Project website:** https://lite.berkeley-humanoid.org/

This is not a desktop toy. The paper reports a height of about 0.8 m and mass of roughly 16 kg. The torso houses the computer, battery, and IMU, with modular actuators driving the arm and leg joints.

Instead of relying on fully machined metal structures and custom parts, the team designed as much as possible for ordinary FDM 3D printers. Much of the nonstandard structure is printed in PLA. Not because PLA is an ideal engineering material, but because it is inexpensive, readily available, and straightforward to print—important qualities for a reproducible open-source design.

The real centerpiece is the actuator.

![berkeley humanoid lite — figure 2](/uploads/berkeley-humanoid-lite/berkeley-humanoid-lite-02.webp)

Each actuator combines a brushless DC motor, cycloidal reduction drive, output shaft, eccentric shaft, bearings, and housing. Cycloidal gearing distributes load across multiple contact points instead of concentrating it on a small number of gear teeth, which is helpful when some structural parts are 3D-printed.

Putting high torque straight through printed plastic gears would be asking for failures. Berkeley's approach is pragmatic: print what can reasonably be printed, then rely on standard bearings, screws, standoffs, and shafts where loads and alignment matter most.

Two actuator sizes serve different joints. The paper's BOM estimates China-sourced component costs of approximately $157 for the 6512 actuator and $94 for the 5010 version.

![berkeley humanoid lite — figure 3](/uploads/berkeley-humanoid-lite/berkeley-humanoid-lite-03.webp)

Motor choices include MAD-series drone BLDC motors such as the M6C12 and 5010. Position feedback comes from AS5600 magnetic encoders, while the motor controllers include STM32G4-based boards such as the B-G431B-ESC1. The onboard computer is an Intel N95 mini PC running Ubuntu 22.04.

Joint-level communication uses CAN 2.0 at 1 Mbps. Actuators on the arms and legs connect to the onboard computer through a USB-to-CAN adapter. The IMU connects over USB for attitude feedback. A 6S, 4,000 mAh LiPo battery provides about 30 minutes of runtime according to the paper.

From an embedded-systems perspective, the architecture looks much more like a distributed control system than an MCU-driven robot car.

![berkeley humanoid lite — figure 4](/uploads/berkeley-humanoid-lite/berkeley-humanoid-lite-04.webp)

The N95 runs policy inference, state estimation, and motion control. Each joint has its own motor drive and encoder to close the local control loop. CAN carries position, velocity, and torque commands down to the actuators and returns joint telemetry.

The firmware documentation is detailed enough to be useful. Motor controllers are flashed using STM32CubeIDE, and motor parameters, CAN IDs, directions, and calibration settings must all be configured. Initial power-up includes electrical angle calibration, during which the motor rotates. The actuator must be able to move freely; restraining it risks damaging the mechanism or drive electronics.

The software stack is equally substantial. The repository includes Isaac Lab training environments, `rsl_rl`, sim-to-sim testing, and code for real-robot deployment. Low-level control lives in `berkeley_humanoid_lite_lowlevel`. Both Python and C implementations are provided, with C recommended for more predictable real-time behavior on the physical robot.

That distinction matters. A reinforcement-learning policy that looks excellent in simulation still has to handle CAN latency, USB-to-CAN jitter, IMU noise, motor heating, and battery voltage sag once it reaches real hardware.

The most valuable part of Berkeley Humanoid Lite may be the documentation around those details: actuator assembly, magnetic encoder installation, CAN IDs, motor calibration, dependency setup on the N95, CAN configuration under Ubuntu, and real-robot launch scripts.

This is not an easy weekend project for a beginner. High-power motors, lithium batteries, multiple CAN-connected drives, load-bearing printed structures, and learned control policies all introduce real risks, including damaged electronics and physical injury. For anyone interested in how far an openly documented, relatively low-cost humanoid robot can go, though, it is an unusually informative reference.
