---
title: 'Amazing Hand: An Open-Source Robotic Hand with Eight Servos'
description: Pollen Robotics packs eight serial servos and four articulated fingers into a 400 g, 3D-printable robotic hand.
  A closer look at its linkages, control and build files.
locale: en
translationKey: pollen-amazinghand-8dof
pubDate: '2026-10-19'
category: open-source
tags:
- AmazingHand
- Robotics
- Open Source Hardware
- Servos
- 3D Printing
draft: false
sourceUrl: https://github.com/pollen-robotics/AmazingHand
author: EmbeddedNote
seoTitle: 'Amazing Hand: Open-Source 8-DOF Robotic Hand | EmbeddedNote'
seoDescription: 'Inside Pollen Robotics’ Amazing Hand: eight Feetech SCS0009 servos, parallel finger linkages, 3D-printed
  parts, TTL control and Reachy 2 compatibility.'
---

Many dexterous robotic hands mount their motors in the forearm and run tendons through the wrist. Pollen Robotics, the team behind Reachy 2, has packaged a different mechanism into **Amazing Hand**: four fingers driven by eight compact servos, all mounted inside the hand. The assembly weighs about **400 g**. Pollen estimates that a basic build can be assembled for less than **€200 in parts**.

The repository includes printable parts, CAD models, a bill of materials, assembly instructions and control software. The code is released under **Apache-2.0**; the mechanical design uses **CC BY 4.0**.

**Project repository:** [pollen-robotics/AmazingHand](https://github.com/pollen-robotics/AmazingHand)

![Amazing Hand dimensions and finger range of motion](/uploads/amazinghand/amazinghand-cover.webp)

## Eight servos, four fingers

Amazing Hand has **eight independently controlled degrees of freedom**, divided evenly among four fingers. Each finger has two articulated, mechanically coupled segments. Rather than using a cable-and-pulley transmission, the design uses a compact **parallel linkage** driven by two servos at the base of the finger. Together, the two actuators produce flexion/extension and abduction/adduction.

The servos are **Feetech SCS0009** serial-bus units. The listed specifications put each servo at approximately 13 g, with a 300° travel range and a nominal stall torque of **2.3 kgf·cm at 6 V**. Unlike a basic PWM hobby servo, the serial interface can report position and operating telemetry such as voltage, temperature and load-related feedback. That feedback is useful for calibration and future grasp control, though it should not be mistaken for a calibrated fingertip force sensor.

![Amazing Hand mounted on a robotic wrist](/uploads/amazinghand/amazinghand-02.jpg)

![Parallel linkage providing finger flexion and abduction](/uploads/amazinghand/amazinghand-03.jpg)

The lack of tendons running through the wrist makes the assembly easier to inspect and service. It also keeps the actuators close to the joints they drive, although it does not eliminate the usual trade-offs of servo backlash, linkage tolerances and printed-part compliance.

![Four example poses of the four-finger robotic hand](/uploads/amazinghand/amazinghand-04.jpg)

## Printable parts and mechanical assembly

Most of the structure is 3D printed. The build uses rigid parts for the finger frames and linkages, with flexible materials for the outer shells. The project supplies separate left- and right-hand parts where mirroring is necessary; several finger components are shared between both versions. The printing guide covers part orientation, support placement and recommended materials for a conventional FDM printer.

![Bill of 3D-printed parts and recommended materials](/uploads/amazinghand/amazinghand-05.jpg)

![Example 3D-print arrangement and settings](/uploads/amazinghand/amazinghand-06.jpg)

For a mechanical build like this, the assembly guide matters as much as the CAD files. The ball-joint rods must be set to the correct lengths, and each finger needs to be calibrated after assembly. The repository provides **STL and STEP files**, an **Onshape CAD model**, a step-by-step PDF assembly guide and scripts for initial servo alignment. It also includes named hand positions with corresponding servo angles, so common poses do not have to be recreated from scratch.

## Two ways to control the hand

There are two supported control setups. The first connects the serial servos to a computer through a **Waveshare bus-servo driver** and uses Python scripts. The second uses an **Arduino with a Feetech TTL Linker**. In either arrangement, the eight servos share a TTL serial bus and are addressed individually by ID.

The default assignments pair IDs **1–2** with the index finger, **3–4** with the middle finger, **5–6** with the ring finger and **7–8** with the thumb. If two hands are put on the same bus, their IDs must be unique to avoid address collisions.

![Left- and right-hand assembly and servo ID layout](/uploads/amazinghand/amazinghand-07.jpg)

The servos need a separate regulated DC supply. The build guidance recommends a **5 V supply rated for at least 2 A**; the appropriate adapter for local mains power should be selected separately. USB communication alone should not be assumed to supply the current needed when multiple fingers move.

## Wrist mounting and Reachy 2 integration

Amazing Hand's wrist interface was designed for **Orbita 3D**, the three-degree-of-freedom actuator used in Reachy 2. The reference wrist uses three coaxial, geared brushless motors, field-oriented control and EtherCAT communication. That wrist assembly is separate from the eight-servo hand; the quoted hand cost should not be read as including a complete robotic arm and wrist.

Because the mating geometry is available, builders can adapt the hand to other wrists as well. One community build has also mounted the hand on a SO-ARM robotic arm.

![Wrist interface compatible with Reachy 2 Orbita 3D](/uploads/amazinghand/amazinghand-08.jpg)

## Bills of materials, calibration and examples

The project maintains its bill of materials in a shared spreadsheet, with a separate listing for the printed components. Most of the electronics cost comes from the eight servos. Kits are also available from third-party sellers, including Seeed Studio and WowRobo, for builders who prefer not to source every component individually.

![Amazing Hand bill of materials and reference prices](/uploads/amazinghand/amazinghand-09.jpg)

![Finger linkage assembly steps from the build guide](/uploads/amazinghand/amazinghand-10.jpg)

For the first power-up, the practical sequence is to check the servo IDs, attach the external power supply, run the calibration routine and then test the fingers through the Python or Arduino examples. The published CAD includes preset joint configurations for several gestures.

![Named hand positions and servo-angle presets in Onshape](/uploads/amazinghand/amazinghand-11.jpg)

![Two Amazing Hands forming a heart shape](/uploads/amazinghand/amazinghand-12.jpg)

The community has taken the mechanism in several directions. One derivative uses **SG90 servos** and experiments with force feedback to reduce cost. Another project, **AmazingHandControl**, provides a Python GUI for monitoring servo data and recording or replaying gestures. Other builders have investigated finger sensing and motion-capture-driven teleoperation, including data collection for imitation-learning experiments.

A hand-tracking demonstration is available on [YouTube](https://www.youtube.com/watch?v=U0TfeG3ZUto), while the repository also links to a [basic demonstration video](https://github.com/user-attachments/assets/485fc1f4-cc57-4e59-90b5-e84518b9fed0).

![Community SG90 servo hand gripping a plastic bottle](/uploads/amazinghand/amazinghand-13.jpg)

![Community force-control test bench](/uploads/amazinghand/amazinghand-14.jpg)

![AmazingHandControl GUI showing live servo data](/uploads/amazinghand/amazinghand-15.jpg)

![Amazing Base desktop stand](/uploads/amazinghand/amazinghand-16.jpg)

## Where the design still needs work

The published design provides the mechanics and code needed to experiment with articulated fingers. It has not, however, been validated as an industrial gripper. The developers note that 3D-printing tolerances, individually adjusted linkages and the flexibility of the printed structure can make actual joint angles differ from the ideal model. The hand has also not been qualified for prolonged, high-load grasping.

The SCS0009's position and load-related feedback provides a starting point for better closed-loop grasp control, but additional software is needed to regulate contact and protect the actuators in demanding tasks. The repository tracks ongoing work in its **[Amazing Hand Enhanced](https://github.com/pollen-robotics/AmazingHand/tree/Amazing-Hand-Enhanced/AmazingHand_Enhanced)** branch.

<!-- embeddednote-seo-p2:internal-links:start -->
For a different use of robotic grippers, [Jumper's 22-DoF platform](/en/articles/a-hardcore-new-open-source-project-on-github-jumper-the-22-dof-crab-robot-fully-open-source-from-training-to-on-device-deployment/) combines two claws with four walking legs and a MuJoCo-based training pipeline.
<!-- embeddednote-seo-p2:internal-links:end -->
