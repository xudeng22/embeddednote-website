---
title: 'Microduck: A Tiny Robot Duck with 15 Motors and an Open-Source Brain'
description: Inside Microduck, a 25 cm biped with an RK3566, 15 motors, a 50 Hz control loop and reinforcement-learning
  policies trained in MuJoCo.
locale: en
translationKey: microduck-robot-duck
pubDate: '2026-09-01'
category: open-source
tags:
- Microduck
- RK3566
- Biped Robot
- Reinforcement Learning
- MuJoCo
- PPO
- ONNX
- Open Source Robotics
draft: false
author: EmbeddedNote
sourceUrl: https://github.com/pollen-robotics/microduck
seoTitle: 'Microduck: A Tiny Robot Duck with 15 Motors and Open-Source Software'
seoDescription: Microduck pairs Rockchip RK3566, 15 motors, a 50 Hz control loop and sensors with open-source robotics
  software and MuJoCo-trained policies.
---

A robot duck standing 25 cm tall is not the obvious place to look for a serious robotics software stack. Microduck, from Pollen Robotics, looks like a desk toy until it starts walking, picking things up with its beak or recovering after a fall. It weighs less than 800 g, has fifteen motors and launched with a $399 introductory pre-order price before tax and shipping. According to Hugging Face co-founder Thomas Wolf, orders exceeded $2.6 million in the first 24 hours after its August 27 launch. That is reported order value, not delivered hardware or recognised revenue.

Pollen Robotics is part of Hugging Face, which acquired the French company in 2025. Microduck is sold as an approachable robot for play and development rather than a laboratory-only platform. Its friendly appearance conceals a fairly involved combination of Linux services, sensor interfaces, actuator control and reinforcement-learning policies.

![Microduck robots playing with a small ball](/uploads/microduck/microduck-cover.webp)

*Microduck on a play mat. The robot is designed for walking, grasping and other learned movements.*

![Four versions of the Microduck robot](/uploads/microduck/microduck-four-colors.webp)

*Four colourways of the 25 cm biped.*

**Project:** [pollen-robotics/microduck](https://github.com/pollen-robotics/microduck) · [Pollen Robotics](https://pollen-robotics.com/microduck/) · [Training code](https://github.com/pollen-robotics/microduck_rl)

The GitHub repository calls itself *the duck's brain*. That description is useful: it contains the software that operates Microduck, including its control services, communications, policy execution and update mechanism. It is not a manufacturing package. Pollen's [press kit](https://pollen-robotics.com/microduck/press-kit/) explicitly limits its open-source claim to software; the mechanical and electronic designs, including PCB schematics, are not published as open-source hardware.

The main computer is a **Rockchip RK3566**, a quad-core Arm Cortex-A55 SoC with an AI accelerator. The published configuration has **1 GB of RAM and 32 GB of storage**. It runs the robot software, motion policies, camera services, wireless connectivity and update infrastructure. Up front are a camera and an **8 × 8 time-of-flight depth sensor**; motion sensing comes from two IMUs, one in the body and another in the head. The specification also lists microphones, a speaker, and NFC antennas in the head and beak. A removable **NP-F550 2,600 mAh battery** provides roughly an hour of operation, depending on how hard the robot is working.

Fifteen servos share a serial bus with an IMU board. The important software boundary is `robotd`, which owns that bus and runs a **50 Hz control loop**. Higher-level clients request a movement or behavior; they do not get unrestricted access to each actuator. `robotd` coordinates the sensor readings, learned policies and safety checks before commanding the joints. For a small biped that may stumble, touch objects or be handled by a user, keeping motor control under one process matters more than the duck's cheerful appearance suggests.

![Microduck hardware and software functional diagram](/uploads/microduck/microduck-architecture-en.webp)

*Functional layout redrawn from published specifications. This is not the manufacturer's electrical schematic.*

The rest of the software is deliberately split into services rather than folded into one monolithic application. `configd` manages network settings, the robot's identity and gamepad pairing. `updaterd` verifies signed releases and can roll back an unhealthy update. `btd` provides a Bluetooth path, while `padd` handles gamepad input; `mediad` manages camera streaming over WebRTC, and `tofd` provides readings from the depth sensor. The services communicate through **JSON-RPC over Unix sockets**. The distinction is practical: a camera service failure should not take down motor control, and a failed control process should not leave the robot unable to accept a software update. These boundaries are documented in the repository's [architecture notes](https://github.com/pollen-robotics/microduck/blob/main/docs/design/architecture.md).

![Microduck standing on a work desk](/uploads/microduck/microduck-on-desk.webp)

*The finished robot in a desktop setting.*

The motion policies have their own repository, [microduck_rl](https://github.com/pollen-robotics/microduck_rl). Training uses **MuJoCo** for simulation and **PPO** for reinforcement learning, then exports the learned policy to **ONNX** for execution on the robot. Walking, standing up, sitting, grabbing an object and using roller attachments are different behaviors, not a single hard-coded animation. The simulator is useful precisely because a physical biped is less forgiving than a character moving through a game engine.

Pollen also models its actuators during training. Voltage-dependent behavior, back electromotive force, friction, command latency, battery sag and gear backlash can all affect how a policy transfers to real hardware. A gait that looks stable in simulation may not survive a change in ground friction or a motor's dead zone. Modeling those effects does not eliminate the sim-to-real gap, but it makes the training setup more relevant to the machine that will execute the policy.

For developers, the attraction is the ability to move beyond the included controller. The repository documents command-line tools for inspecting the robot, reading logs, configuring networking, installing updates and testing behavior. More ambitious experiments involve changing a policy, training a new one and deploying it to the robot. That is an unusually accessible entry point into reinforcement-learning robotics compared with larger, more expensive biped platforms.

There is one boundary worth keeping clear before ordering parts: **Apache-2.0 covers the released Microduck software, not the whole physical robot**. You can study, modify and build on the published runtime and training code under their applicable licenses, but the GitHub repositories do not provide the full schematics, PCB manufacturing files or mechanical drawings needed to reproduce a Microduck from scratch. For now, it is best understood as a purchasable robot with an open software stack, not a complete open-hardware kit.
