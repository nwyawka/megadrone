# V0 - Skills Development Platform

**Type:** Fixed-Wing | **Config:** Conventional Pusher | **Status:** Development

## Quick Specs

| Parameter | Value |
|-----------|-------|
| Wingspan | 1.0-1.2m (40-48") |
| Length | 0.6m (24") |
| AUW | 800-1000g |
| Payload | 200g |
| Endurance | 20-25 min |
| Cruise Speed | 54 km/h (15 m/s) |
| Flight Controller | Pixhack / SpeedyBee F405 |
| Propulsion | 1x Electric (2212 920kv) |

## Purpose

- Learn construction techniques with expendable materials
- Develop piloting and autopilot tuning skills
- Validate hardware integration
- Low-cost, low-risk experimentation

## Configuration

```
    Top View:
                    ┌─────┐
                    │  V  │ ← Vertical stab
              ┌─────┴──┬──┴─────┐
              │   H-Stab        │ ← Horizontal stab
              └────────┼────────┘
                       │
                      [P] ← Pusher prop
                       │
              ┌────────┴────────┐
              │    Fuselage     │
              └────────┬────────┘
         ┌─────────────┼─────────────┐
         │            Wing           │
         └───────────────────────────┘
```

## Existing Hardware (Use As-Is)

| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| Battery | 2200mAh 3S LiPo | 180g | $0 (owned) |
| Motor | 2212 920kv | 55g | $0 (owned) |
| ESC | 30A | 30g | $0 (owned) |
| Flight Controller | Pixhack | 40g | $0 (owned) |
| GPS | (existing) | 25g | $0 (owned) |
| Receiver | FS-IA6B | 10g | $0 (owned) |

## To Purchase

| Component | Model | Weight | Est. Cost |
|-----------|-------|--------|-----------|
| TX/RX | ELRS (RadioMaster Zorro + EP1) | - | $120-150 |
| Servos | 4x 9g micro (SG90 or MG90S) | 36g | $10-15 |
| Propeller | 9x6 or 10x4.5 pusher | 15g | $5-8 |
| Airframe Materials | Foam board, hot glue, tape | ~400g | $20-30 |
| **Remote ID** | Dronetag Mini / Cube ID | 6-8g | $35-79 |

## Construction Materials

- **Wing:** Dollar Tree foam board or Depron (3-5mm)
- **Fuselage:** Foam board box construction
- **Reinforcement:** Bamboo skewers, popsicle sticks, fiberglass tape
- **Covering:** Packing tape or heat shrink film
- **Adhesive:** Hot glue, foam-safe CA

## Weight Budget

| Component | Mass (g) | % |
|-----------|----------|---|
| Airframe (foam) | 300-350 | 33% |
| Battery | 180 | 19% |
| Motor + Prop | 70 | 7% |
| ESC | 30 | 3% |
| FC + GPS | 65 | 7% |
| Receiver | 10 | 1% |
| Servos (4x) | 36 | 4% |
| Wiring/Hardware | 50 | 5% |
| **Remote ID** | 8 | 1% |
| **Margin** | 142 | 15% |
| **Total** | **~908g** | 100% |

## Budget Summary

| Category | Cost |
|----------|------|
| Existing Hardware | $0 |
| ELRS TX/RX | $130 |
| Servos | $12 |
| Propellers (3x) | $15 |
| Foam/Materials | $25 |
| Misc Hardware | $20 |
| **Remote ID Module** | $50 |
| **Total** | **~$250** |

## Skills Developed

- Foam construction
- Soldering
- ArduPilot basics
- RC flying
- Basic PID tuning

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Crashes | Cheap materials, expect failures |
| Build errors | Iterate quickly, document lessons |

---

## Build Documents

| Document | Description |
|----------|-------------|
| [BUILD_DIMENSIONS.md](BUILD_DIMENSIONS.md) | Single pusher - Complete build specifications |
| [BUILD_DIMENSIONS_PUSHPULL.md](BUILD_DIMENSIONS_PUSHPULL.md) | **Push-pull twin with V-tail - Higher speed variant** |

### Configuration Comparison

| Config | Motors | Cruise | Endurance | Complexity |
|--------|--------|--------|-----------|------------|
| Single Pusher | 1× 2212 | 54 km/h | 22 min | ★★☆ |
| Push-Pull V-Tail | 2× 2212 | 65 km/h | 15-30 min* | ★★★ |

*Push-pull can run on single engine for 25-30 min endurance

---

## FAA Remote ID Compliance

**Required for all flights as of March 2024**

### Commercial Modules

| Module | Weight | Cost | Notes |
|--------|--------|------|-------|
| Dronetag Mini | 6g | $79 | Built-in GPS, recommended |
| Cube ID | 8g | $35 | Requires FC GPS feed |
| BlueMark db120 | 5g | $49 | Integrated, standalone |

### DIY Option (Home-Built for Education/Recreation)

Per 14 CFR 89.501, home-builders are exempt from production requirements (DOC submission) but must meet operational requirements (broadcast compliant messages).

| Component | Cost | Notes |
|-----------|------|-------|
| ESP32-S3 DevKitC | $12 | Main processor + radio |
| GPS (BN-220 or FC feed) | $0-15 | Can use FC GPS via MAVLink |
| Wiring | $5 | To flight controller |
| **Total** | **~$15-30** | vs $35-79 commercial |

**Open Source Resources:**

| Project | Link |
|---------|------|
| ArduPilot ArduRemoteID | [github.com/ArduPilot/ArduRemoteID](https://github.com/ArduPilot/ArduRemoteID) |
| OpenDroneID Core Library | [github.com/opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| ESP32 DIY Tutorial | [hackster.io/...drone-id-requirement](https://www.hackster.io/user462411/esp32-for-government-drone-id-requirement-64a5c9) |
| ArduPilot Remote ID Docs | [ardupilot.org/plane/docs/common-remoteid](https://ardupilot.org/plane/docs/common-remoteid.html) |

**Wiring to FC (MAVLink):**
```
FC TX  ──►  ESP32 RX (GPIO18)
FC RX  ◄──  ESP32 TX (GPIO17)
FC GND ◄─►  ESP32 GND
FC 5V  ──►  ESP32 5V
```

**ArduPilot Config:**
```
SERIALx_PROTOCOL = 45  (OpenDroneID)
SERIALx_BAUD = 57600
```

---

*See [Development Roadmap](../../docs/roadmap/development_roadmap.md) for complete specifications.*
