# FAA Remote ID Compliance Guide

**Last Updated:** January 2026
**Applies To:** All MegaDrone versions (V0-V4)
**Requirement Effective:** March 16, 2024

---

## Table of Contents

1. [Overview](#overview)
2. [Regulatory Framework](#regulatory-framework)
3. [Compliance Options](#compliance-options)
4. [Home-Builder Exemption](#home-builder-exemption)
5. [Operational Requirements](#operational-requirements)
6. [Technical Requirements](#technical-requirements)
7. [Commercial Modules](#commercial-modules)
8. [DIY Remote ID](#diy-remote-id)
9. [ArduPilot Integration](#ardupilot-integration)
10. [Resources](#resources)

---

## Overview

Remote ID is the FAA's system for identifying drones in flight. It broadcasts identification and location information that can be received by other parties on the ground.

### Who Must Comply?

| Category | Remote ID Required? |
|----------|---------------------|
| Recreational, >250g | Yes |
| Commercial (Part 107) | Yes |
| Recreational, <250g | No |
| Flying in FRIA only | No |

---

## Regulatory Framework

Remote ID is governed by [14 CFR Part 89](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-89).

### Key Subparts

| Subpart | Covers | Who It Applies To |
|---------|--------|-------------------|
| **Subpart B** | Operational Requirements | All operators |
| **Subpart D** | Technical Requirements | Equipment specs |
| **Subpart F** | Design & Production | Manufacturers |

### Important Distinction

- **Production Requirements (Subpart F):** What manufacturers must do - submit Declaration of Compliance (DOC)
- **Operational Requirements (Subpart B):** What operators must do when flying - broadcast compliant messages

---

## Compliance Options

### Three Ways to Comply

| Option | Description | BVLOS Eligible? |
|--------|-------------|-----------------|
| **Standard Remote ID** | Built-in broadcast capability | Yes |
| **Broadcast Module** | Add-on module attached to drone | No (VLOS only) |
| **FRIA** | Fly in FAA-recognized identification area | No |

### Standard Remote ID vs Broadcast Module

| Feature | Standard Remote ID | Broadcast Module |
|---------|-------------------|------------------|
| Broadcasts drone location | Yes | Yes |
| Broadcasts control station location | Yes | No (takeoff location only) |
| BVLOS operations | Eligible | Not eligible |
| Visual line-of-sight required | No | Yes |

---

## Home-Builder Exemption

### 14 CFR 89.501

> "A home-built unmanned aircraft is not subject to the design or production requirements [of Subpart F]"

**Definition:** A home-built unmanned aircraft is one that an individual built solely for **education or recreation**.

### What This Means

| Requirement | Home-Builder Status |
|-------------|---------------------|
| Submit Declaration of Compliance (DOC) | **EXEMPT** |
| Design requirements | **EXEMPT** |
| Production requirements | **EXEMPT** |
| Operational requirements | **MUST COMPLY** |

### Interpretation

A home-builder building for education/recreation:
1. Does NOT need to submit a DOC to the FAA (that's a production requirement)
2. MUST meet operational requirements when flying
3. Must broadcast compliant Remote ID messages

### Regulatory Ambiguity

The operational requirements (§ 89.110, § 89.115) reference "serial number listed on an FAA-accepted DOC" - but this language was written for commercial products, not home-built aircraft that are explicitly exempt from production requirements.

**The gap:** Home-builders are exempt from production requirements (including DOC) but the operational requirements reference DOC-listed equipment. This creates ambiguity.

**Possible interpretation:** If you build a system that broadcasts compliant ASTM F3411 messages, you may be meeting the operational requirements without needing a DOC.

**Recommendation:** Contact FAA UAS Support for written guidance on your specific situation.

---

## Operational Requirements

### § 89.110 - Standard Remote ID Operations

| Requirement | Details |
|-------------|---------|
| Broadcast timing | From takeoff to shutdown |
| Message elements | Per § 89.305 |
| If broadcast fails | Land as soon as practicable |
| Pre-flight | Verify equipment functional |

### § 89.115 - Broadcast Module Operations

| Requirement | Details |
|-------------|---------|
| Broadcast timing | From takeoff to shutdown |
| Visual line-of-sight | Required at all times |
| Pre-flight | Verify module functioning |
| If broadcast fails | Land as soon as practicable |

---

## Technical Requirements

### Message Elements (§ 89.305)

What must be broadcast:

| Element | Description |
|---------|-------------|
| **Aircraft ID** | Serial number or session ID |
| **Aircraft Latitude** | Current position |
| **Aircraft Longitude** | Current position |
| **Aircraft Altitude** | Geometric altitude |
| **Aircraft Velocity** | Speed and direction |
| **Control Station Latitude** | Pilot position |
| **Control Station Longitude** | Pilot position |
| **Control Station Altitude** | Pilot geometric altitude |
| **Time Mark** | Synchronized timestamp |
| **Emergency Status** | If applicable |

### Performance Requirements (§ 89.310)

| Parameter | Requirement |
|-----------|-------------|
| **Position accuracy (aircraft)** | Within 100 feet (95% probability) |
| **Position accuracy (control station)** | Within 100 feet (95% probability) |
| **Altitude accuracy (aircraft)** | Within 150 feet (95% probability) |
| **Altitude accuracy (control station)** | Within 15 feet (95% probability) |
| **Broadcast rate** | At least 1 Hz (once per second) |
| **Radio spectrum** | FCC Part 15 compliant (WiFi/Bluetooth) |
| **Broadcast format** | Non-proprietary (ASTM F3411) |

### Transmission Methods

| Method | Standard | Notes |
|--------|----------|-------|
| Bluetooth 4 Legacy | BT4 Advertising | Widest receiver compatibility |
| Bluetooth 5 Long Range | BT5 Extended | Better range, newer phones only |
| WiFi Beacon | 802.11 | Good range |
| WiFi NAN | Neighbor Awareness | Limited receiver support |

---

## Commercial Modules

### Recommended Modules

| Module | Weight | Cost | GPS | Interface | Notes |
|--------|--------|------|-----|-----------|-------|
| **Dronetag Mini** | 6g | $79 | Built-in | Standalone | Recommended |
| **Cube ID** | 8g | $35 | FC feed | Serial | Budget option |
| **BlueMark db120** | 5g | $49 | Built-in | Standalone | Compact |
| **BlueMark DB200** | 10g | $89 | Built-in | MAVLink | ArduPilot native |
| **Holybro Remote ID** | 8g | $45 | FC feed | DroneCAN | PX4/ArduPilot |
| **mRID (Phoenix UAS)** | 4g | $60 | Built-in | Serial | FPV optimized |
| **NewBeeDrone BeeID** | 6g | $55 | Built-in | Serial | Betaflight/ArduPilot |

### Selection Guide

| If you need... | Choose |
|----------------|--------|
| Simplest setup | Dronetag Mini (standalone) |
| Lowest cost | Cube ID ($35) |
| ArduPilot integration | BlueMark DB200 or Holybro |
| Lightest weight | mRID (4g) |
| Combined GPS + Remote ID | NewBeeDrone BeeID |

---

## DIY Remote ID

### For Home-Builders (Education/Recreation)

Per 14 CFR 89.501, home-builders are exempt from production requirements but must meet operational requirements.

### Hardware Options

| Component | Cost | Notes |
|-----------|------|-------|
| ESP32-S3 DevKitC | $10-15 | Main processor, BT+WiFi |
| ESP32-C3 DevKitC | $8-12 | Lower power alternative |
| GPS Module (optional) | $15-20 | If not using FC GPS |
| Wiring/connectors | $5 | To flight controller |
| **Total** | **$15-35** | vs $35-79 commercial |

### Open Source Projects

#### 1. ArduRemoteID (Recommended)

**Repository:** [github.com/ArduPilot/ArduRemoteID](https://github.com/ArduPilot/ArduRemoteID)

Official ArduPilot Remote ID implementation.

| Feature | Details |
|---------|---------|
| Chips | ESP32-S3, ESP32-C3 |
| Broadcast | WiFi Beacon, WiFi NAN, BT4, BT5 |
| Interface | MAVLink or DroneCAN |
| Standard | ASTM F3411 / F3586-22 |

**Supported Boards:**
- ESP32-S3 Dev Board
- ESP32-C3 Dev Board
- BlueMark DB110/DB200/DB201/DB202
- Holybro Remote ID Module

#### 2. OpenDroneID Core Library

**Repository:** [github.com/opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c)

The foundational C library for encoding/decoding ASTM F3411 messages.

| Feature | Details |
|---------|---------|
| License | Apache 2.0 |
| Language | C (portable) |
| Platforms | ESP32, nRF52, Linux, any embedded |

#### 3. Other Projects

| Project | Repository | Notes |
|---------|------------|-------|
| nRF52 Bluetooth | [github.com/sxjack/remote_id_bt5](https://github.com/sxjack/remote_id_bt5) | BT4/BT5 for nRF52840 |
| ESP32 Receiver | [github.com/PeterJBurke/RID](https://github.com/PeterJBurke/RID) | For receiving/testing |

#### 4. Tutorials

| Resource | Link |
|----------|------|
| ESP32 DIY Build | [hackster.io/...drone-id-requirement](https://www.hackster.io/user462411/esp32-for-government-drone-id-requirement-64a5c9) |

### Building ArduRemoteID

```bash
# Clone repository
git clone https://github.com/ArduPilot/ArduRemoteID
cd ArduRemoteID

# See BUILDING.md for full instructions
# Pre-compiled binaries available in releases
```

### Flashing ESP32-S3

Use the [Espressif Flash Tool](https://www.espressif.com/en/support/download/other-tools) or esptool:

```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 \
  write_flash 0x0 ArduRemoteID_ESP32S3.bin
```

---

## ArduPilot Integration

### Wiring

```
Flight Controller          ESP32-S3/C3
     TX  ───────────────►  RX (GPIO18)
     RX  ◄───────────────  TX (GPIO17)
    GND  ◄──────────────►  GND
     5V  ───────────────►  5V (or 3.3V)
```

### ArduPilot Configuration

```
# Enable Remote ID on a serial port
SERIALx_PROTOCOL = 45      # OpenDroneID
SERIALx_BAUD = 57600       # Baud rate

# For DroneCAN connection instead
CAN_P1_DRIVER = 1
CAN_D1_PROTOCOL = 1        # DroneCAN
```

### Verification

In Mission Planner or QGroundControl:
1. Connect to vehicle
2. Check Messages tab for "OpenDroneID" messages
3. Verify GPS position is being transmitted
4. Use OpenDroneID Android app to verify broadcast

### Testing with Android App

Download: [OpenDroneID Android Receiver](https://github.com/opendroneid/receiver-android)

The app will show:
- Detected drones broadcasting Remote ID
- Their position on a map
- All message elements being broadcast

---

## Resources

### FAA Official

| Resource | Link |
|----------|------|
| Remote ID Overview | [faa.gov/uas/getting_started/remote_id](https://www.faa.gov/uas/getting_started/remote_id) |
| 14 CFR Part 89 | [ecfr.gov/.../part-89](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-89) |
| DOC Accepted List | [faa.gov/.../RID](https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/RID) |
| FAA DroneZone | [faadronezone.faa.gov](https://faadronezone.faa.gov) |

### Standards

| Standard | Description |
|----------|-------------|
| ASTM F3411-22a | Remote ID message specification |
| ASTM F3586-22 | Means of Compliance |

### Open Source

| Resource | Link |
|----------|------|
| ArduRemoteID | [github.com/ArduPilot/ArduRemoteID](https://github.com/ArduPilot/ArduRemoteID) |
| OpenDroneID Core | [github.com/opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| OpenDroneID Specs | [github.com/opendroneid/specs](https://github.com/opendroneid/specs) |
| Android Receiver | [github.com/opendroneid/receiver-android](https://github.com/opendroneid/receiver-android) |

### ArduPilot

| Resource | Link |
|----------|------|
| Remote ID Docs | [ardupilot.org/plane/docs/common-remoteid](https://ardupilot.org/plane/docs/common-remoteid.html) |

### Community

| Resource | Link |
|----------|------|
| FPV Freedom Coalition | [fpvfc.org/remote-id-final-rule-summary](https://fpvfc.org/remote-id-final-rule-summary) |
| Pilot Institute Guide | [pilotinstitute.com/homebuilt-remote-id-rules](https://pilotinstitute.com/homebuilt-remote-id-rules/) |

---

## Summary for MegaDrone Project

### Recommended Approach by Version

| Version | Recommended Remote ID | Notes |
|---------|----------------------|-------|
| **V0** | DIY (ESP32 + ArduRemoteID) | Educational, low cost |
| **V1** | DIY or BlueMark DB200 | MAVLink integration |
| **V1-ACAP** | DIY (part of custom autopilot) | Integrate with SBC |
| **V2/V3/V4** | Commercial (BlueMark/Holybro) | Reliability for larger aircraft |

### Cost Comparison

| Option | Cost | Weight | Effort |
|--------|------|--------|--------|
| DIY (ESP32) | ~$17 | ~8g | Medium |
| Commercial (Cube ID) | $35 | 8g | Low |
| Commercial (Dronetag) | $79 | 6g | Low |

### For Home-Builders

1. You are likely exempt from production requirements (no DOC needed)
2. You must meet operational requirements (broadcast compliant messages)
3. DIY with ArduRemoteID meets the technical specs
4. Document your compliance approach
5. Consider getting FAA written guidance for your specific situation

---

*Document Version: 1.0*
*Created: January 2026*
*Project: MegaDrone*
