# JP Security Air Operations Fleet

**Document Classification:** Internal Operations
**Version:** 2.0
**Date:** January 2026

---

## Fleet Overview

JP Security operates three distinct drone types for air operations, each optimized for specific mission profiles. This tiered approach provides operational flexibility while managing costs.

| Type | Role | Platform | Speed | Endurance | Unit Cost |
|------|------|----------|-------|-----------|-----------|
| **VA-1 Variant** | Mid-Range ISR | Fixed-Wing | 35-40 kts | 1-2.5 hrs | $650-760 |
| **VA-5R/VA-5S** | Close ISR + Strike | Quad | 40-100 kts | 15-30 min | $500-2,500 |
| **VA-3/VA-4** | Long Endurance ISR | VTOL Fixed-Wing | 55-75 kts | 2-12 hrs | $2,680-4,750 |

*VA-5R (Reconnaissance) and VA-5S (Strike) share a common quad platform.

---

## Type 1: VA-1 Variant (Mid-Range ISR)

### Role
- Mid-range surveillance patrols
- Cost-effective area coverage
- Expendable reconnaissance
- Training and skill development

### Mission Profile
```
MID-RANGE ISR PATROL

Base ──► Transit ──► Patrol Area ──► Loiter/Survey ──► Return
           │              │               │
        30-50 km       1-2 hrs        EO camera
        transit        on station      GPS track
```

### Specifications
| Parameter | Value |
|-----------|-------|
| Type | Fixed-wing |
| Wingspan | 1.5-2.4m |
| Source | Internal development |
| Range | 30-80 km |
| Endurance | 1-2.5 hrs |
| Cruise Speed | 35-40 kts |
| Payload | 300-500g |
| Launch | Hand throw |
| Recovery | Belly landing |

### Cost Advantage
- **Unit cost:** $650-760
- **Expendable philosophy:** Cheaper to lose than abort mission
- **Rapid replacement:** Field-buildable in days
- **Modular wings:** Multiple configurations from one fuselage

### Operational Use
- Daytime coastal patrols
- Vessel tracking and monitoring
- Initial area reconnaissance
- Training new operators
- Situations where drone loss is acceptable

---

## Type 2: VA-5R/VA-5S (Quad-Based ISR/Strike)

### Role
The VA-5 platform has two variants sharing a common quad airframe:
- **VA-5R (Reconnaissance):** Close-range threat assessment and vessel inspection
- **VA-5S (Strike):** Offensive operations with warhead payload

### Mission Profiles

**VA-5R (Reconnaissance):**
```
CLOSE ISR / THREAT ASSESSMENT

Vessel ──► Deploy VA-5 ──► Approach Target ──► Assess Threat ──► Return
                │                 │                  │
             < 5 min          500m-2km          Video/Photos
             deploy           standoff          Thermal/EO
```

**VA-5S (Strike):**
```
STRIKE MISSION

Launch ──► High-Speed Transit ──► Target Acquisition ──► Strike ──► [Expendable]
             │                          │                  │
          60-100 kts               Loiter/ID           Warhead
          10-30 km                GPS + terminal       Delivery
```

### Specifications
| Parameter | VA-5R | VA-5S |
|-----------|----------|-------------|
| Type | Quadcopter | Quadcopter |
| Frame Size | 450-550mm | 450-550mm |
| Range | 1-5 km | 10-30 km |
| Endurance | 20-30 min | 15-20 min |
| Max Speed | 40-50 kts | 80-100+ kts |
| Payload | Camera | 2-10 lbs (warhead) |
| Launch | Hand / deck | Deck / automated |
| Recovery | RTL | Expendable |
| Cost | $500-1,500 | $1,000-2,500 |

### Platform Advantages
- VTOL capability (ship-based operations)
- Hover for close inspection
- Rapid deployment
- Common parts for VA-5R and VA-5S variants
- Expendable cost structure

### Warhead Options (TBD)
| Type | Status |
|------|--------|
| Kinetic | Concept |
| Fragmentation | Concept |
| Incendiary | Concept |
| Marker/Smoke | Near-term |

### Operational Use
- Deployed from vessel during approach operations
- Quick assessment of target deck, cargo, personnel
- Document evidence before boarding
- Night operations with thermal imaging
- Offensive operations against hostile targets (VA-5S)
- Expendable in hostile situations

---

## Type 3: VA-3/VA-4 (Long Endurance ISR)

### Role
- Persistent maritime surveillance
- Long-range patrol missions
- High-value sensor platform
- Primary ISR workhorse

### Mission Profile
```
LONG ENDURANCE ISR

Base ──► Transit ──► Patrol Area ──► Persistent Coverage ──► Return
           │              │                  │
        100+ nm        2-12 hrs          EO/IR gimbal
        transit        on station         AIS receiver
                                          Data link
```

### Specifications

**VA-3 (VTOL)**
| Parameter | Value |
|-----------|-------|
| Type | VTOL QuadPlane |
| Wingspan | 3.2m |
| Endurance | 2-2.5 hrs |
| Cruise Speed | 55-75 kts |
| Payload | 2.5 kg |
| Launch | Vertical (no runway) |
| Cost | $2,680 |

**VA-4 (Gas-Electric Hybrid)**
| Parameter | Value |
|-----------|-------|
| Type | VTOL Hybrid |
| Wingspan | 3.2m |
| Endurance | 8-12 hrs |
| Cruise Speed | 55-75 kts |
| Payload | 2.5 kg |
| Launch | Vertical (no runway) |
| Cost | $4,750 |

### Sensor Suite
- Multi-axis stabilized gimbal (internal production)
- EO/IR dual sensor
- AIS receiver
- Starlink datalink capability
- Real-time video downlink

### Operational Use
- Primary long-range ISR platform
- Persistent maritime domain awareness
- Vessel tracking over extended areas
- Night operations with thermal
- Ship-based operations (VTOL)

---

## Fleet Mix Recommendations

### Minimum Viable Fleet (Startup)
| Type | Quantity | Purpose | Cost |
|------|----------|---------|------|
| VA-5R | 2 | Close ISR | $2,000 |
| VA-1 Variant | 4 | Mid-range, training | $2,800 |
| **Total** | **6** | | **$4,800** |

### Operational Fleet (Phase 1)
| Type | Quantity | Purpose | Cost |
|------|----------|---------|------|
| VA-5R | 4 | Close ISR | $4,000 |
| VA-1 Variant | 6 | Mid-range ISR | $4,200 |
| VA-3/VA-4 | 2 | Long endurance | $7,400 |
| **Total** | **12** | | **$15,600** |

### Full Capability Fleet (Phase 2)
| Type | Quantity | Purpose | Cost |
|------|----------|---------|------|
| VA-5R | 6 | Close ISR | $6,000 |
| VA-5S | 4 | Offensive capability | $8,000 |
| VA-1 Variant | 10 | Mid-range, expendable | $7,000 |
| VA-3/VA-4 | 4 | Long endurance ISR | $14,800 |
| **Total** | **24** | | **$35,800** |

---

## Mission Selection Matrix

| Scenario | Primary | Backup | Notes |
|----------|---------|--------|-------|
| Vessel approach assessment | VA-5R | VA-1 | Quick deploy, close-in, VTOL |
| Coastal patrol (day) | VA-1 Variant | VA-3/VA-4 | Cost-effective coverage |
| Extended maritime surveillance | VA-3/VA-4 | VA-1 Variant | Maximum endurance |
| Night operations | VA-3/VA-4 (thermal) | VA-5R (thermal) | IR capability required |
| Hostile vessel interdiction | VA-5S | - | Offensive operations |
| Evidence documentation | VA-5R | VA-1 Variant | High-res imagery, hover |
| Ship-based operations | VA-3/VA-4 (VTOL) | VA-5 | No runway required |
| Expendable reconnaissance | VA-1 Variant | VA-5 | Acceptable loss |

---

## Logistics & Support

### Spares Strategy
| Type | Recommended Spares | Rationale |
|------|-------------------|-----------|
| VA-5R | 1 per 2 operational | Low cost, rapid replacement |
| VA-5S | 2 per 2 operational | Expendable by design |
| VA-1 Variant | 2 per 4 operational | High attrition expected |
| VA-3/VA-4 | 1 per 2 operational | High value, protect investment |

### Maintenance Levels
| Type | Field | Intermediate | Depot |
|------|-------|--------------|-------|
| VA-5R/VA-5S | Battery, props, motors | FC, gimbal | Airframe |
| VA-1 Variant | Full rebuild capable | - | - |
| VA-3/VA-4 | Battery, props, servos | Motor, autopilot | Airframe |

---

*See individual hardware documentation for detailed specifications:*
- [VA-1 Variants](../../hardware/va1_variants/README.md)
- [VA-3 VTOL](../../hardware/va3_alti_vtol/README.md)
- [VA-4 Hybrid](../../hardware/va4_alti_hybrid/README.md)
- [VA-5 ISR/Strike](../../hardware/va5_strike/README.md)
