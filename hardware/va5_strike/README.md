# VA-5 Platform - Quad-Based ISR/Strike

**Type:** Quadcopter | **Config:** Dual-variant | **Status:** Concept

## Overview

The VA-5 is a quad-based platform with two variants:
- **VA-5R (Reconnaissance):** Close-range ISR and threat assessment
- **VA-5S (Strike):** Offensive operations with warhead payload

Both variants share a common airframe, reducing development cost and enabling common parts/training.

## Platform Strategy

- **Phase 1:** Develop VA-5R quad for close-range ISR and threat assessment
- **Phase 2:** Develop VA-5S with strike modifications (speed, payload, guidance)

This approach provides:
- Dual-use platform (ISR + Strike)
- Reduced development cost
- Common parts and training
- VTOL capability for ship-based operations

## Mission Profiles

### VA-5R (Reconnaissance)
```
CLOSE ISR / THREAT ASSESSMENT

Vessel ──► Deploy VA-5 ──► Approach Target ──► Assess Threat ──► Return
                │                 │                  │
             < 5 min          500m-2km          Video/Photos
             deploy           standoff          Thermal/EO
```

### VA-5S (Strike)
```
STRIKE MISSION PROFILE

Launch ──► Transit (high speed) ──► Target Acquisition ──► Strike ──► [Expendable]
  │              │                        │                  │
  │         60-100 kts               Loiter/ID          Payload
  │                                                      Delivery
  ▼
VTOL Launch
```

## Design Requirements

| Parameter | VA-5R | VA-5S |
|-----------|----------|-------------|
| **Max Speed** | 40-50 kts | 80-100+ kts |
| **Range** | 1-5 km | 10-30 km |
| **Endurance** | 20-30 min | 15-20 min |
| **Payload** | Camera (integrated) | 2-10 lbs (warhead) |
| **Launch** | Hand / deck | Deck / automated |
| **Recovery** | RTL | Expendable |

## Design Considerations

### Quad Platform Advantages
- VTOL capability (ship-based operations)
- Hover for close inspection
- Rapid deployment
- Simple control system
- Expendable cost structure

### Strike Modifications
- Higher-power motors for speed
- Streamlined body fairing
- Payload bay / hardpoints
- GPS + terminal guidance
- Reinforced structure for dive

### Warhead Integration
- **Warhead Type:** TBD
- **Mounting:** Underslung or integrated bay
- **Release Mechanism:** TBD
- **Guidance:** GPS + terminal guidance (TBD)

## Preliminary Specs (Estimates)

| Parameter | VA-5R | VA-5S |
|-----------|--------------|----------------|
| Frame Size | 450-550mm | 450-550mm |
| AUW | 2-3 kg | 4-8 kg |
| Motors | 2212-2216 | 2814-3110 |
| Propellers | 10-12" | 10-12" (high-pitch) |
| Battery | 4S 5000mAh | 6S 8000mAh |
| Unit Cost | $500-1,500 | $1,000-2,500 |

## Propulsion Options

### VA-5R Configuration
| Component | Specification | Cost |
|-----------|---------------|------|
| Motors (x4) | 2212 920kv | $60 |
| ESCs (x4) | 30A BLHeli | $40 |
| Battery | 4S 5000mAh | $50 |
| Props | 10x4.5 | $15 |

### VA-5S Configuration
| Component | Specification | Cost |
|-----------|---------------|------|
| Motors (x4) | 2814 900kv or larger | $120 |
| ESCs (x4) | 40-50A BLHeli_32 | $80 |
| Battery | 6S 8000mAh high-C | $100 |
| Props | 12x6 high-pitch | $25 |

## Warhead Options (TBD)

| Type | Weight | Effect | Status |
|------|--------|--------|--------|
| Kinetic | 2-5 lbs | Impact damage | Concept |
| Fragmentation | 3-6 lbs | Area effect | Concept |
| Incendiary | 2-4 lbs | Fire/disable | Concept |
| Marker/Smoke | 1-2 lbs | Target marking | Near-term |

## Development Phases

### Phase 1: VA-5R Development
- Develop baseline quadcopter
- Validate flight performance
- Test close-range ISR operations
- Establish operational procedures

### Phase 2: VA-5S Development
- Upgrade motors/ESCs for speed
- Design payload integration
- Develop guidance system
- Strike tactics development

### Phase 3: Operational Testing
- Field deployment trials
- Accuracy testing
- Ship-based operations validation

## Budget Estimate

| Item | ISR Baseline | Strike Variant |
|------|--------------|----------------|
| Airframe | $150-300 | $200-400 |
| Propulsion | $150-200 | $300-400 |
| Avionics/FC | $150-250 | $200-350 |
| Camera/Sensors | $200-500 | N/A |
| Payload system | N/A | TBD |
| **Unit Cost** | **$500-1,500** | **$1,000-2,500** |

## Regulatory Considerations

- VA-5R operations under Part 107 or waiver
- Weaponized UAS requires specific authorization
- Export control (ITAR) implications for VA-5S
- Federal/military customer authorization required

## Comparison to Fleet

| Drone | Role | Speed | Endurance | Cost |
|-------|------|-------|-----------|------|
| VA-1 Variant | Mid-range ISR | 35-40 kts | 1-2.5 hrs | $650-760 |
| VA-3/VA-4 | Long endurance ISR | 55-75 kts | 2-12 hrs | $2.7K-4.8K |
| **VA-5R** | **Close ISR** | **40-50 kts** | **20-30 min** | **$500-1.5K** |
| **VA-5S** | **Offensive** | **80-100 kts** | **15-20 min** | **$1K-2.5K** |

---

*Document Version: 0.2 (Concept)*
*Status: Requirements Definition - VA-5R/VA-5S Platform*
