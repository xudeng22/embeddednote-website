"""Add the verification layer to six existing articles.

Each block records what we checked, where the evidence lives, and what we could
not confirm. Nothing here is a measurement we did not take.
"""

from pathlib import Path

EN = Path(r"D:\Deepseek\en-site\src\content\articles\en")

APOLLO = """### What we checked

We worked from the public firmware in `Integrations/ESPHome/` (Core.yaml, substitutions `version: 26.11.5.1`) instead of the product page, because the YAML is what the ornament actually runs.

| Claim | Where we looked | Result |
| --- | --- | --- |
| 37 WS2812 LEDs on a single GPIO3 chain | `light`, `esp32_rmt_led_strip`, `num_leds: 37` | Confirmed |
| Zones: body 24, mouth 5, nose 1, eyes 2, hat 5 | partition ranges 0-23, 24-28, 29, 30-31, 32-36 | Confirmed, but the physical order is body, mouth, nose, eyes, hat |
| Buzzer on GPIO6 with `max_power: 50%` | `output`, `platform: ledc` | Confirmed |
| Song buttons on GPIO4, GPIO5 and GPIO7 | three `binary_sensor` entries and the ext1 wake mask | Confirmed |
| 40% brightness ceiling | `led_max_brightness: "40"` applied as `color_correct` | Confirmed, and it is a hard per-channel cap, not a starting volume |

That last row is the one worth internalising. Every zone and every effect is written through a 40% colour correction, so the Home Assistant brightness slider and the LED Brightness number move inside that ceiling; at 100% the strip is still running at 40% of its electrical maximum. If you compare the H-3 against a bare WS2812 ring at full white, the ornament will look dim, and that is deliberate.

"""

MOTO = """## What we checked

The repository, not the launch posts, is the source for this section. We read `README.md`, `LICENSE.md`, the hardware review packages and the 2026-09-16 update note.

| Claim | Where we looked | Result |
| --- | --- | --- |
| 466 x 466 round AMOLED, CO5300 over QSPI, CST9217 touch | `README.md`, hardware table | Confirmed |
| ESP32-S3 with 32 MB flash and 8 MB PSRAM | same table | Confirmed |
| BLE GATT with encrypted write and notify characteristics, LE Secure Connections, Just Works | `README.md`, protocol section | Confirmed, and the missing MITM protection is stated by the author |
| Self-designed A1 board | `hardware/manufacturing/engineering-candidates/rev-a1-.../README_DO_NOT_ORDER.md` | Engineering review only. The directory name is the author's own warning |
| 9 C++ tests, 60 backend tests, 12 Swift tests, 13 BLE policy tests | 2026-09-16 update | Confirmed as the author's recorded run, on his bench |
| Licence | `LICENSE.md`, PolyForm Noncommercial 1.0.0 | Source-available, not OSI open source |

The licence point changes how the project should be described. The code is public and modifiable for personal, research and other non-commercial use, with attribution; selling pre-flashed units or shipping it inside a paid product needs separate permission. Calling it "open source" without that qualifier is the kind of shortcut that gets a hardware project into trouble later, so this article uses source-available from here on.

"""

ARBWAVE = """## What we checked

Everything below comes from the project README and the documents it links, read on 2026-11-11.

| Claim | Where we looked | Result |
| --- | --- | --- |
| 30 MHz sine, 5 MHz square | README, V1.0 hardware targets | Confirmed as targets, not as guaranteed performance |
| THD about -60.2 dBc and SFDR 63.26 dBc at 10 MHz | README, oscilloscope FFT | Author's measurement. The README itself warns the scope contributes harmonics |
| 13.5% overshoot on the square wave | README, known issues | Confirmed; attributed to filter group delay |
| 24 V DC input, under 24 W | README, control and interface | Confirmed |
| Board about 225 x 90 mm | README, known issues | Confirmed, and listed as a problem to fix by splitting the board |
| Project state | README, update status | **Paused.** The author says work resumes and the first release lands on 2026-12-25 |

The pause matters more than any single specification. A reader who finds this page in December should check the repository before ordering a board, because the filter, the offset drift above 25 MHz and the board split are all still open items rather than finished design.

"""

CAP = """## What we checked

The repository README is unusually specific for a joke project, so most of the hardware claims can be checked directly.

| Claim | Where we looked | Result |
| --- | --- | --- |
| Three capacitor slots, up to 3 A | README, features | Confirmed |
| 10 ohm series resistor per slot | README, features | Confirmed; the stated purpose is limiting inrush and avoiding a brownout if a capacitor shorts |
| 128 x 64 SSD1315 display, ESP32, NTP time, web configuration | README, features | Confirmed |
| USB-C or 12-15 V barrel jack, 72 x 74 x 36 mm | README | Confirmed |
| Linear regulators dropping roughly 12 V | README, note | Confirmed by the author, who calls the heat normal and suggests a buck converter |

One piece of arithmetic that the README does not spell out. With a 12 V rail and a 10 ohm limiter, each slot draws about 1.2 A at the instant it starts charging, falling as the capacitor comes up. Three slots fired together would ask for roughly 3.6 A, which is above the 3 A figure the project quotes. That is a budget for one slot at a time, not a simultaneous worst case, and it is the kind of number that decides whether a 12 V supply folds back on the first bang.

"""

JUMPER = """## What we checked

| Claim | Where we looked | Result |
| --- | --- | --- |
| 22 degrees of freedom | README, first line | Confirmed |
| Apache-2.0 | README, licence section | Confirmed for the maintainer's own material; third-party assets keep their own terms |
| Training stack: mjlab, rsl_rl, MuJoCo, MuJoCo Warp | README, training section | Confirmed |
| Controller is an RK3576 | Not stated in the README or the docs we could read | **Unverified.** Treat the SoC in the earlier reports as unconfirmed until the hardware document says so |
| Complete pipeline from training to on-device deployment | README, resource table | Partly. The repository is an authoring kit for appearance, motion and scenes, with training and export documented; the hardware design lives in a separate document |

The distinction is worth keeping. Jumper publishes the workflow that produces a motion and packages it as an app, and it publishes hardware documentation, but the two are separate artefacts with separate licences. That is more honest than most robot repositories, and it is also why "fully open source from training to deployment" needs a footnote rather than a headline.

"""

PAPERDIY = """## What we checked

| Claim | Where we looked | Result |
| --- | --- | --- |
| 4.7-inch, 960 x 540 grayscale panel | Product listing and the demo repository | Consistent across both |
| 8-bit parallel display interface | Published schematic pages for the K159 and K159-B kits | Confirmed on the schematic we mirrored |
| ESP32-S3 with an ESP-IDF demo that pins its components | `m5stack/M5PaperDIY-UserDemo` | Confirmed |
| Price around $25 | Retail listing at publication | A snapshot, not a current price |

We mirrored the four schematic pages for the complete kit into this site rather than hotlinking the vendor CDN, so the drawings stay readable if the listing changes. What we have not done is measure the panel: refresh timing, ghosting and the actual current draw of the board in each power state remain vendor figures and should be re-measured on the bench.

"""

PATCHES = [
    (
        "apollo-h3-christmas-ornament.md",
        "2026-11-11",
        "open-hardware",
        APOLLO,
        "### Thirty-seven LEDs, five zones and six tunes",
        [
            (
                "The team says the proceeds support CASA of Lexington, which advocates for children involved in family-court cases, and the Open Home Foundation, which backs privacy-focused, open-source smart-home infrastructure.",
                "The 2026 edition sends 100% of its profits to St. Jude Children's Research Hospital, a change from the two organisations supported by earlier ornaments in the series.",
            )
        ],
    ),
    (
        "moto-gps-waveshare.md",
        "2026-11-11",
        "open-hardware",
        MOTO,
        "## One repository, the whole chain",
        [
            ("- Open Source", "- Source Available"),
        ],
    ),
    (
        "arbwave30-waveform-generator.md",
        "2026-11-11",
        "open-hardware",
        ARBWAVE,
        "## Main components",
        [],
    ),
    (
        "an-explosive-embedded-project-on-github-esp32-c3-based-capacitor-explosion-alarm-clock.md",
        "2026-11-11",
        "open-hardware",
        CAP,
        "# Safety Notice",
        [],
    ),
    (
        "a-hardcore-new-open-source-project-on-github-jumper-the-22-dof-crab-robot-fully-open-source-from-training-to-on-device-deployment.md",
        "2026-11-11",
        "open-hardware",
        JUMPER,
        "![Jumper open-source robot — introductory project image]",
        [],
    ),
    (
        "m5stack-paperdiy-esp32-s3.md",
        "2026-11-11",
        "epaper",
        PAPERDIY,
        "## Engineering check: memory size, power gating and first bring-up",
        [],
    ),
]


def main() -> None:
    for name, updated, series, block, anchor, replacements in PATCHES:
        path = EN / name
        text = path.read_text(encoding="utf-8")

        if anchor not in text:
            raise SystemExit(f"anchor missing in {name}: {anchor}")

        for old, new in replacements:
            if old not in text:
                print(f"  .. already applied or not found in {name}: {old[:50]}")
                continue
            text = text.replace(old, new, 1)

        if "contentType:" not in text:
            text = text.replace(
                "draft: false\n",
                f"draft: false\ncontentType: deep\nseries: {series}\nupdatedDate: '{updated}'\n",
                1,
            )

        if "What we checked" not in text:
            text = text.replace(anchor, block + anchor, 1)

        path.write_text(text, encoding="utf-8")
        print(f"patched {name}")


if __name__ == "__main__":
    main()
