# V2 - ALTI-Style Twin-Boom Pusher (Fixed-Wing)

**Type:** Fixed-Wing | **Config:** ALTI-Style Twin-Boom | **Status:** Development

## Quick Specs

| Parameter | Value |
|-----------|-------|
| Wingspan | **3.2m (126")** |
| Length | **2.4m (94")** |
| AUW | **12 kg** |
| Payload | **2.5 kg** (ISR + Starlink) |
| Endurance | **3-4 hours** |
| Cruise Speed | 70-80 km/h (19-22 m/s) |
| Flight Controller | Pixhawk 6C |
| Propulsion | 1x Electric (SunnySky X4112S) |

## Purpose

- Develop full-scale ALTI-style airframe
- Test twin-boom structural design
- Validate aerodynamics at scale
- Prepare airframe for V3 VTOL conversion
- Support Starlink + ISR payload capability

## Reference Design: ALTI Transition

V2 is inspired by the [ALTI Transition](https://altiunmanned.com/transition) VTOL UAS.

## Configuration

```
    Top View:

    ┌───────────────────────────────────────────────────────┐
    │                        WING                           │
    │                      (3.2m span)                      │
    └───────────┬───────────────────────────────┬───────────┘
                │                               │
         ┌──────┴──────┐                 ┌──────┴──────┐
         │    BOOM     │                 │    BOOM     │
         │   (Left)    │                 │   (Right)   │
         │             │   ┌─────────┐   │             │
         │             │   │ FUSELAGE│   │             │
         │             │   │   [P]   │   │             │  ← Pusher
         │             │   └─────────┘   │             │
         └──────┬──────┘                 └──────┬──────┘
                │                               │
                ╲                               ╱
                 ╲───────────────────────────╱
                        Inverted V-Tail
```

## Why V2 Exceeds VTOL Endurance

As pure fixed-wing, V2 saves weight over VTOL:
- No VTOL motors: -660g
- No VTOL ESCs: -160g
- No VTOL arms/mounts: -300g
- No hover reserve needed
- **Total savings: ~1.1 kg → more battery capacity**

## Inverted V-Tail Design

| Parameter | Value |
|-----------|-------|
| V-angle | 110-120° (inverted) |
| Span | 600-800mm |
| Chord | 150-180mm |
| Area | 15-20 dm² |
| Ruddervator deflection | ±25° |

## Propulsion System

| Component | Model | Specs | Weight | Cost |
|-----------|-------|-------|--------|------|
| Motor | SunnySky X4112S-320kv | 800W max | 190g | $55 |
| ESC | 60A BLHeli_32 | 6S, telemetry | 60g | $35 |
| Battery | 6S 22000mAh (2x 11Ah) | 488Wh total | 2400g | $240 |
| Propeller | 18x10 folding | Carbon fiber | 50g | $40 |

## Endurance Calculation

| Parameter | Value |
|-----------|-------|
| Battery capacity | 488 Wh (6S 22Ah) |
| Usable capacity (80%) | 390 Wh |
| Cruise power | 100-120W |
| **Cruise endurance** | **3.2-3.9 hours** |
| Reserve (20%) | ~45 min |

## Flight Controller

| Component | Model | Cost |
|-----------|-------|------|
| FC | Pixhawk 6C | $200 |
| GPS | Holybro M9N | $60 |
| Airspeed | MS4525DO | $30 |
| Power Module | Holybro PM07 | $35 |

## Structural Design

| Component | Material |
|-----------|----------|
| Wing spar | Carbon fiber tube (25mm OD) |
| Wing ribs | Laser-cut plywood + foam |
| Wing skin | Fiberglass/balsa sandwich |
| Booms | Carbon fiber tubes (30mm OD) |
| Fuselage | Carbon/fiberglass composite |
| V-tail | Foam core + fiberglass |

## Weight Budget

| Component | Mass (g) | % |
|-----------|----------|---|
| Wing structure | 1500 | 17% |
| Fuselage | 800 | 9% |
| Booms | 400 | 4% |
| V-tail | 300 | 3% |
| Motor + mount | 250 | 3% |
| ESC | 60 | 1% |
| **Battery (6S 22Ah)** | **2400** | **27%** |
| FC + avionics | 300 | 3% |
| Servos (4x) | 150 | 2% |
| Wiring/hardware | 400 | 4% |
| **Payload** | **1000** | **11%** |
| **Margin** | 1440 | 16% |
| **Total** | ~9000g | 100% |

## Payload Capacity: 2.5 kg

| Config | ISR Payload | Starlink | Total | Use Case |
|--------|-------------|----------|-------|----------|
| ISR Only | 1 kg | - | 1 kg | Standard missions |
| Starlink Only | - | 1.5 kg | 1.5 kg | Long-range comms |
| **ISR + Starlink** | 1 kg | 1.5 kg | **2.5 kg** | Full BVLOS |

## Budget

| Category | Cost |
|----------|------|
| Pixhawk 6C + GPS + sensors | $325 |
| Motor + ESC | $90 |
| Battery (6S 22Ah, 2x packs) | $240 |
| Propeller | $40 |
| Carbon tubes (booms, spar) | $150 |
| Composite materials | $200 |
| Plywood/foam for ribs | $50 |
| Servos (4x digital) | $60 |
| Hardware/fasteners | $75 |
| Camera + gimbal (1kg payload) | $600 |
| **Total** | **~$1,830** |

## Skills Developed

- Large-scale composites
- CAD design
- Structural analysis
- Twin-boom construction

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Structural integrity at scale | FEA analysis, conservative safety factor |

---

*See [Development Roadmap](../../docs/roadmap/development_roadmap.md) for complete specifications.*
