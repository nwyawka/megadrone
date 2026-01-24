# V1 Variants - Speed vs Endurance Trade-offs

**Type:** Fixed-Wing | **Config:** Conventional Pusher | **Status:** Development

## Overview

The base V1 can be scaled for different mission profiles using a **modular wing system** - one fuselage with interchangeable wings.

## Variant Comparison

| Parameter | V1 (Base) | V1-LE | V1-Fast | V1-Fast 2hr |
|-----------|-----------|-------|---------|-------------|
| **Purpose** | Training | Max endurance | Speed + agility | Speed + endurance |
| **Wingspan** | 1.0-1.2m | 1.8-2.0m | 1.5-1.7m | 2.2-2.4m |
| **Length** | 0.6m | 0.9-1.0m | 0.8-0.9m | 1.1-1.2m |
| **AUW** | 0.9 kg | 1.4-1.6 kg | 1.4-1.6 kg | 2.0-2.2 kg |
| **Wing Loading** | 50 g/dm² | 40 g/dm² | 55-60 g/dm² | 50 g/dm² |
| **Cruise Speed** | 54 km/h | 45-50 km/h | 55-65 km/h | 55-60 km/h |
| **Endurance** | 25-30 min | **2-2.5 hrs** | 1.0-1.3 hrs | **2+ hrs** |
| **Battery** | 3S 2200mAh | 4S 5000mAh | 4S 4000mAh | 6S 5000mAh |

## Power vs Speed Relationship

| Cruise Speed | Power Required | Endurance (74Wh) |
|--------------|----------------|------------------|
| 12 m/s (43 km/h) | ~25W | 2.4 hrs |
| 14 m/s (50 km/h) | ~32W | 1.8 hrs |
| 15 m/s (54 km/h) | ~40W | 1.5 hrs |
| 17 m/s (61 km/h) | ~55W | 1.1 hrs |
| 20 m/s (72 km/h) | ~80W | 0.7 hrs |

---

## V1-LE: Long Endurance Variant

Optimized for maximum flight time at slow cruise speeds.

### Specs
| Parameter | Value |
|-----------|-------|
| Wingspan | 1.8-2.0m |
| Aspect Ratio | 9-10 |
| Wing Loading | 40 g/dm² |
| L/D (cruise) | 12-14 |
| Cruise Speed | 43-50 km/h |
| Cruise Power | 25-30W |
| **Endurance** | **2-2.5 hrs** |

### Hardware
| Component | Model | Cost |
|-----------|-------|------|
| Motor | 2212 1000kv | $15 |
| Battery | 4S 5000mAh 35C | $45 |
| Propeller | 11x7 or 12x6 | $8 |

### Budget
| Item | Cost |
|------|------|
| V1 base investment | $550 |
| Larger battery | $45 |
| Motor upgrade | $15 |
| Propeller | $8 |
| Additional materials | $40 |
| **Total** | **~$660** |

---

## V1-Fast: Speed-Optimized Variant

Balanced design for higher cruise speed with acceptable endurance.

### Specs
| Parameter | Value |
|-----------|-------|
| Wingspan | 1.5-1.7m |
| Aspect Ratio | 8-9 |
| Wing Loading | 55-60 g/dm² |
| L/D (cruise) | 10-12 |
| Cruise Speed | **55-65 km/h** |
| Cruise Power | 45-50W |
| Endurance | 1.0-1.3 hrs |

### Hardware
| Component | Model | Cost |
|-----------|-------|------|
| Motor | 2212 1000kv | $15 |
| Battery | 4S 4000mAh 45C | $40 |
| Propeller | 10x6 or 11x5.5 | $8 |

### Budget
| Item | Cost |
|------|------|
| V1 base investment | $550 |
| Battery | $40 |
| Motor upgrade | $15 |
| Propeller | $8 |
| Materials | $35 |
| **Total** | **~$650** |

---

## V1-Fast 2hr: Speed + Endurance Variant

Scaled up for both high speed and long endurance.

### Specs
| Parameter | Value |
|-----------|-------|
| Wingspan | 2.2-2.4m |
| Aspect Ratio | 10-11 |
| Wing Loading | 50 g/dm² |
| L/D (cruise) | 12-14 |
| Cruise Speed | **55-60 km/h** |
| Cruise Power | ~50W |
| **Endurance** | **2+ hrs** |
| Payload | 400-500g |

### Hardware
| Component | Model | Cost |
|-----------|-------|------|
| Motor | 2216 900kv | $25 |
| ESC | 40A BLHeli_32 | $20 |
| Battery | 6S 5000mAh 35C | $70 |
| Propeller | 12x6 or 13x6.5 | $12 |
| Servos | 4x 12g digital | $25 |

### Budget
| Item | Cost |
|------|------|
| V1 base investment | $550 |
| Motor (2216 900kv) | $25 |
| ESC upgrade (40A) | $20 |
| Battery (6S 5000mAh) | $70 |
| Propeller | $12 |
| Servos upgrade | $25 |
| Additional materials | $60 |
| **Total** | **~$760** |

---

## Modular Wing System

Rather than building separate aircraft, use **one fuselage with interchangeable wings**.

```
    MODULAR V1 CONCEPT

    Same Fuselage + Tail:
              ┌───┐
              │ F │══[P]
              │ U │
              │ S │
              └─┬─┘

    + Interchangeable Wings:

    LE Wing (1.8-2.0m):        Fast Wing (1.5-1.7m):       Base Wing (1.0-1.2m):
    ════════════════════       ══════════════════          ════════════════
         Endurance                  Speed                    Training
```

### Wing Set Options

| Wing | Span | Wing Loading | Speed | Endurance | Build Cost |
|------|------|--------------|-------|-----------|------------|
| **Base** | 1.0-1.2m | 50 g/dm² | 54 km/h | 25-30 min | $30 |
| **LE** | 1.8-2.0m | 40 g/dm² | 45-50 km/h | 2-2.5 hrs | $60 |
| **Fast** | 1.5-1.7m | 55 g/dm² | 55-65 km/h | 1-1.3 hrs | $45 |

### Cost Savings: Modular vs Separate

| Approach | Components | Total Cost |
|----------|------------|------------|
| 3 Separate Aircraft | 3 fuselages, 3 tails, 3 wings | ~$450 materials |
| **1 Modular Aircraft** | 1 fuselage, 1 tail, 3 wings | **~$180 materials** |
| **Savings** | | **~$270** |

### Modular V1 Complete Kit

| Component | Cost |
|-----------|------|
| V1 Base (fuselage + tail + base wing) | $550 |
| LE Wing add-on | +$60 |
| Fast Wing add-on | +$45 |
| Larger battery (4S 5000mAh) for LE | +$45 |
| **Total Modular System** | **~$700** |

---

## Mission Selection Guide

| Mission Profile | Wing | Key Trade-off |
|-----------------|------|---------------|
| Training/Learning | Base (1.0-1.2m) | Cheap, expendable |
| Aerial photography (calm) | LE (1.8-2.0m) | Max loiter time |
| Aerial photography (windy) | Fast (1.5-1.7m) | Better wind handling |
| Long-range mapping | LE (1.8-2.0m) | Maximize coverage |
| Quick inspection flights | Fast (1.5-1.7m) | Get there fast |

---

*See [Development Roadmap](../../docs/roadmap/development_roadmap.md) for complete specifications.*
