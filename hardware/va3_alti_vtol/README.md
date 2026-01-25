# V3 - ALTI-Style VTOL QuadPlane

**Type:** VTOL | **Config:** QuadPlane (4+1) | **Status:** Development

## Quick Specs

| Parameter | Value |
|-----------|-------|
| Wingspan | **3.2m** |
| Length | **2.4m** |
| AUW | **14 kg** |
| Payload | **2.5 kg** (ISR + Starlink) |
| Cruise Endurance | 2-2.5 hours |
| Hover Time | 5-8 min |
| Cruise Speed | 70-75 km/h |
| Flight Controller | Pixhawk 6C |
| Propulsion | 4x VTOL + 1x Pusher (Electric) |

## Purpose

- Add VTOL capability to V2 airframe
- Develop transition tuning expertise
- Enable runway-independent operations
- Validate hybrid propulsion integration

## Configuration

```
    Top View:

         [M1]                                           [M2]
           ○─────────────────────────────────────────────○
           │                                             │
    ┌──────┴─────────────────────────────────────────────┴──────┐
    │                          WING                             │
    │                        (3.2m span)                        │
    └───────────┬───────────────────────────────────┬───────────┘
                │                                   │
         ┌──────┴──────┐                     ┌──────┴──────┐
         │    BOOM     │   ┌─────────────┐   │    BOOM     │
         │             │   │   FUSELAGE  │   │             │
         │             │   │     [P]     │   │             │  ← Pusher
         │             │   └─────────────┘   │             │
         └──────┬──────┘                     └──────┬──────┘
                │                                   │
           ○────┴─────────────╲       ╱─────────────┴────○
         [M3]                  ╲     ╱                  [M4]
                                ╲   ╱
                            Inverted V-Tail

    Motor Positions:
    - M1, M2: Front (on wing, outboard)
    - M3, M4: Rear (on boom ends, near V-tail)
    - P: Center pusher (rear of fuselage)
```

## VTOL Motor Configuration

| Position | Motor | Prop | Thrust | Weight |
|----------|-------|------|--------|--------|
| M1 (Front-Left) | T-Motor U5 | 18x6.1 | 3.2 kg | 165g |
| M2 (Front-Right) | T-Motor U5 | 18x6.1 | 3.2 kg | 165g |
| M3 (Rear-Left) | T-Motor U5 | 18x6.1 | 3.2 kg | 165g |
| M4 (Rear-Right) | T-Motor U5 | 18x6.1 | 3.2 kg | 165g |
| P (Pusher) | SunnySky X4112S | 16x10 | 4.0 kg | 190g |

**Total VTOL thrust:** 12.8 kg (for 11 kg AUW = 1.16:1 TWR)

## Power System

| Component | Specs | Weight | Count |
|-----------|-------|--------|-------|
| VTOL ESC | 40A BLHeli_32 | 40g | 4 |
| Main Battery | 6S 16000mAh | 1800g | 1 |
| Pusher shares main battery | - | - | - |

## VTOL Arm Design

| Parameter | Value |
|-----------|-------|
| Front arm span | 800mm from centerline |
| Rear arms | Integrated into boom ends |
| Arm material | Carbon fiber tube (20mm) |
| Motor tilt | 0° (vertical) or 5° forward |

## ArduPilot QuadPlane Configuration

```
Frame Class:     Q_FRAME_CLASS = 1 (Quad)
Frame Type:      Q_FRAME_TYPE = 1 (X configuration)
Transition:      Q_TRANSITION_MS = 5000 (5 sec)
Assist Speed:    Q_ASSIST_SPEED = 14 (m/s)
Tilt Mask:       Q_TILT_MASK = 0 (no tilt)
```

## Weight Budget

| Component | Mass (g) | % |
|-----------|----------|---|
| V2 Airframe | 3000 | 27% |
| VTOL Motors (4x) | 660 | 6% |
| VTOL ESCs (4x) | 160 | 1% |
| VTOL Arms/Mounts | 300 | 3% |
| Pusher Motor + ESC | 250 | 2% |
| Battery (6S 16Ah) | 1800 | 16% |
| FC + Avionics | 350 | 3% |
| Camera + Gimbal | 800 | 7% |
| Wiring/Hardware | 400 | 4% |
| **Margin** | 3280 | 30% |
| **Total** | ~11000g | 100% |

## Payload Capacity: 2.5 kg

| Config | ISR Payload | Starlink | Total |
|--------|-------------|----------|-------|
| ISR Only | 1 kg | - | 1 kg |
| Starlink Only | - | 1.5 kg | 1.5 kg |
| **ISR + Starlink** | 1 kg | 1.5 kg | **2.5 kg** |

## Additional Budget (over V2)

| Category | Cost |
|----------|------|
| VTOL Motors (4x T-Motor U5) | $320 |
| VTOL ESCs (4x 40A) | $120 |
| VTOL Props (4x 18") | $80 |
| Motor mounts + arms | $100 |
| Larger battery (6S 16Ah) | $180 |
| Wiring/connectors | $50 |
| **Total Additional** | **~$850** |

## Skills Developed

- VTOL dynamics
- Transition tuning
- Hybrid power management
- QuadPlane configuration

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Transition failures | Extensive SITL testing |
| VTOL tuning | Large TWR margin (1.16:1) |

---

*See [Development Roadmap](../../docs/roadmap/development_roadmap.md) for complete specifications.*
