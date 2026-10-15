---
title: '32 IMUs, One FPGA: An Open-Source Attempt to Replace a Geophone'
description: Will Whang combines 32 ICM-42688-P IMUs with an iCE40 FPGA and RP2040 to investigate low-frequency noise reduction as an alternative to a geophone.
locale: en
translationKey: imu-array-32-fpga
pubDate: '2026-09-19'
category: hardware
tags:
- IMU
- FPGA
- RP2040
- ICM-42688-P
draft: false
seoTitle: '32 IMUs and an iCE40 FPGA: Geophone Alternative'
seoDescription: Will Whang combines 32 ICM-42688-P IMUs with an iCE40 FPGA and RP2040 to investigate low-frequency noise reduction as an alternative to a geophone.
---

Sony developed a multi-IMU board for SPRESENSE that combines readings from 16 consumer MEMS sensors. Its published results put bias stability below 0.39 degrees per hour, approaching the territory of industrial fiber-optic gyroscopes. Will Whang was interested, but noted that export restrictions would probably prevent him from getting one. His response was to build an array himself: 32 TDK/InvenSense ICM-42688-P IMUs surrounding a Lattice iCE40UP5K FPGA, with the ultimate goal of exploring an alternative to a geophone.

![imu array 32 fpga — figure 1](/uploads/imu-array-32-fpga/imu-array-32-fpga-01.webp)

![imu array 32 fpga — figure 2](/uploads/imu-array-32-fpga/imu-array-32-fpga-02.webp)

**GitHub:** https://github.com/will127534/IMU_Array  
**Project notes:** https://www.willwhang.dev/Project-IMU-Array/

The reason for the unusual sensor count goes back to Whang's earlier geophone-based seismometer. Poor low-frequency response required a negative-impedance converter (NIC) to cancel the coil resistance. That meant op-amps, digital potentiometers, and analog switches, along with a risk of oscillation from overcompensation. The circuitry became complicated enough that he still hadn't documented all of it. The new idea was to average an array of inexpensive MEMS accelerometers to reduce noise and avoid much of the expensive analog front end. His focus was therefore on low-frequency accelerometer noise and Allan variance, rather than optimizing the gyroscopes' dynamic response.

## The sensor board: why 32 IMUs are arranged this way

At the center of the square PCB sits an iCE40UP5K in a QFN48 package. Thirty-two ICM-42688-P devices are arranged around it. A three-point-mounted triangular board might have reduced mechanical stress, but the chosen approach relies on rotating IMUs in groups of four to compensate for differences in axis sensitivity, as Sony did. That arrangement doesn't fit neatly on a triangle, so Whang settled on a square board with the corner diagonals left free of IMUs.

![imu array 32 fpga — figure 3](/uploads/imu-array-32-fpga/imu-array-32-fpga-03.webp)

The sensor PCB uses six layers, via-in-pad construction, and 0.2 mm vias. Even in the tightly packed layout, signals running at tens of megahertz need adequate return paths. Only 3.3 V and 1.2 V are brought in through the FPC cable, keeping additional heat sources off the sensor board. Whang selected a particularly narrow 22-pin FPC connector available from Mouser, partly because he already had plenty of 22-pin Raspberry Pi camera cables. Ground pins are interleaved with SPI signals to help provide return paths.

![imu array 32 fpga — figure 4](/uploads/imu-array-32-fpga/imu-array-32-fpga-04.webp)

![imu array 32 fpga — figure 5](/uploads/imu-array-32-fpga/imu-array-32-fpga-05.webp)

## The FPGA aggregates data; CLKIN handles synchronization

The FPGA's job is deliberately limited. As Whang describes it, it is mainly a data aggregator. Thirty-two MISO lines enter the FPGA, while an SPI configuration interface doubles as its link to the host controller. The host loads the bitstream at power-up. The FPGA does not control the individual chip-select lines and has no spare pins for DRDY, so it cannot independently initiate sensor reads. Three remaining GPIOs drive status LEDs.

Synchronization comes from the ICM-42688-P's `CLKIN` capability, not from the FPGA. Every sensor shares a 32 kHz external clock, aligning their internal timing and enabling simultaneous sampling. The setup uses a 200 Hz sample rate with both interrupts and the external clock enabled.

The gateware evolved as well. An early SPI implementation ran against the FPGA's internal 48 MHz clock and topped out at roughly 5 MHz. Switching to an SCK-driven “Async SPI core” raised that to 20 MHz, at the cost of changing the host's CPHA setting. It's a pragmatic shortcut around clock-domain crossing, and the author explicitly lists it as something to improve later.

## RP2040, Murata Type 1YN, and a tunable oscillator

![imu array 32 fpga — figure 6](/uploads/imu-array-32-fpga/imu-array-32-fpga-06.webp)

An RP2040 runs the processing board. Wireless connectivity comes from a Murata Type 1YN module, built around the CYW43439 also used in the Raspberry Pi Pico W. The RP2040 interfaces with it through three GPIOs: `WL_CLK`, `WL_D` (a combined SDIO CMD/data line), and `WL_CS`. GPS comes from an LC76K receiver. A GNSS front end with a SAW filter and low-noise amplifier helps the receiver work inside a CNC-machined aluminum enclosure; Whang reports that the combination worked surprisingly well even there.

![imu array 32 fpga — figure 7](/uploads/imu-array-32-fpga/imu-array-32-fpga-07.webp)

Rather than a conventional 12 MHz crystal, the board uses a voltage-controlled, temperature-compensated oscillator (VCTCXO). A PWM DAC trims its frequency against the GPS pulse-per-second signal, creating a simplified GPS-disciplined oscillator. That clock serves the RP2040 and provides a stable 32 kHz reference for the IMU array.

![imu array 32 fpga — figure 8](/uploads/imu-array-32-fpga/imu-array-32-fpga-08.webp)

The original power idea was equally unconventional. Because the system was intended to serve as an outdoor, potentially buried geophone replacement, Whang considered using 24 V AC from a doorbell supply to avoid drilling another wall opening. An input capacitor array and bridge rectifier appeared in an earlier revision before being removed. The enclosure is CNC-machined and uses three M8 threaded holes for vibration-isolation feet of the type commonly used on loudspeakers.

![imu array 32 fpga — figure 9](/uploads/imu-array-32-fpga/imu-array-32-fpga-09.webp)

Firmware development took several turns. CircuitPython initially made FPGA configuration convenient: with the board appearing as a USB drive, the bitstream could simply be copied across as a file. But its lack of a suitable hardware interrupt implementation made handling DRDY difficult, so development moved to MicroPython. Then Wi-Fi caused trouble: the Type 1YN's OTP memory had no programmed MAC address. CircuitPython could use a random address, whereas MicroPython did not handle the case as expected. Once the FPGA code stabilized, Whang switched back to the C SDK to concentrate on performance. He also reports transferring full 32-IMU datasets at 100 Hz over UDP or USB CDC with an RP2040 clocked at 250 MHz.

![imu array 32 fpga — figure 10](/uploads/imu-array-32-fpga/imu-array-32-fpga-10.webp)

## Noise measurements and calibration

For long-duration measurements, the sensor assembly was left undisturbed on a floor and the results analyzed using Allan variance. Averaging 32 gyroscopes visibly reduced the irregularities seen in an individual device. The accelerometer's Z-axis curve differed from the X and Y curves, consistent with its different MEMS axis structure. Reproducing a noise-rejection and outlier-filtering algorithm from Sony's work was less successful: it helped over intervals shorter than about 0.2 seconds, but at roughly 300 seconds the outlier filter performed worse than simple averaging. Whang acknowledges that this part of the reproduction did not work as hoped.

![imu array 32 fpga — figure 11](/uploads/imu-array-32-fpga/imu-array-32-fpga-11.webp)

Calibration, however, produced useful results. Following a research paper, Whang 3D-printed an icosahedron and placed the sensor inside it. Measurements were collected for 90 seconds in each of 20 orientations. Gravity and gyro readings were then used to estimate each sensor's misalignment angles and sensitivity without a precision turntable. MATLAB code based on the paper generated calibration data as a header file for fusion on the RP2040.

![imu array 32 fpga — figure 12](/uploads/imu-array-32-fpga/imu-array-32-fpga-12.webp)

The design is still evolving. Version 1.1 added USB, replaced the enclosure connection with a four-pin M5 threaded waterproof connector, and removed the on-board GPS antenna—a reasonable decision for equipment that might actually be buried. Hardware design files, Verilog, and MicroPython code are available on GitHub, together with Gerbers, BOM, and pick-and-place data. PCBWay sponsored the project. The README is unusually candid about the early-stage code: ODR and FSR settings still rely heavily on hand-calculated register values, and the FPGA design hasn't been optimized to save LUTs. That's part of what makes the repository an interesting engineering record.
