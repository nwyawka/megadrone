# MegaDrone Hardware Versions

This directory contains documentation for each hardware version in the MegaDrone development roadmap.

## Naming Convention

| Prefix | Domain | Example |
|--------|--------|---------|
| **VA-** | Air (Aerial drones) | VA-1, VA-5 |
| **VS-** | Surface (Water/land) | VS-1 (future) |
| **VSS-** | Subsurface (Underwater) | VSS-1 (future) |

---

## Air Platform Overview (VA-)

| Version | Type | Wingspan | Payload | Endurance | Cost | Status |
|---------|------|----------|---------|-----------|------|--------|
| [VA-0](va0_skills_platform/) | Fixed-Wing | 1.0-1.2m | 200g | 20-25 min | $200 | Development |
| [VA-1](va1_durable_platform/) | Fixed-Wing | 1.0-1.2m | 300g | 25-30 min | $550 | Development |
| [VA-1 ACAP](va1_acap/) | Fixed-Wing | 1.0-1.2m | 200g | 20-25 min | $130 | Development |
| [VA-1 Variants](va1_variants/) | Fixed-Wing | 1.5-2.4m | 300-500g | 1-2.5 hrs | $650-760 | Development |
| [VA-2](va2_alti_fixedwing/) | Fixed-Wing | 3.2m | 2.5 kg | 3-4 hrs | $1,830 | Development |
| [VA-3](va3_alti_vtol/) | VTOL | 3.2m | 2.5 kg | 2-2.5 hrs | $2,680 | Development |
| [VA-4](va4_alti_hybrid/) | VTOL Hybrid | 3.2m | 2.5 kg | 8-12 hrs | $4,750 | Development |
| [VA-5R/VA-5S](va5_strike/) | Quad (ISR/Strike) | 450-550mm | 2-10 lbs | 15-30 min | $500-2,500 | Concept |

*VA-5R (Reconnaissance) and VA-5S (Strike) share a common quad platform.

---

## Surface Platform Overview (VS-)

| Version | Type | Length | Endurance | Speed | Cost | Status |
|---------|------|--------|-----------|-------|------|--------|
| [VS-1](vs1_picket/) | USV Monohull | 7m | Days/Weeks | 5-8 kts | $4,255 | Concept |

### VS-1 Picket - Long-Endurance Surveillance Vessel

The VS-1 is designed as a "picket" vessel for persistent maritime surveillance in the Gulf of Mexico.

**Key Features:**
- Foam core composite hull (7m, fineness ratio 10-12)
- Hybrid power: Honda EU1000i generator + LiFePO4 batteries + solar
- AIS receiver for vessel traffic monitoring
- Starlink communications (shared with VA-4)
- ArduPilot Rover for autonomous operations

---

## Development Progression (Air)

```
VA-0 (Skills)        VA-1 (Durable)       VA-1 ACAP (Custom)
    │                    │                      │
    │   ┌────────────────┼──────────────────────┘
    │   │                │
    │   │     ┌──────────┴──────────┐
    │   │     │                     │
    ▼   ▼     ▼                     ▼
   VA-1-LE   VA-1-Fast         VA-1-Fast 2hr
   (2+ hrs)  (65 km/h)         (2hr @ 60km/h)
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
    VA-2 (ALTI FW)       VA-5 (Strike)
    3.2m, 3-4hr          Fast, Expendable
          │
          ▼
    VA-3 (ALTI VTOL)
    3.2m, 2-2.5hr
          │
          ▼
    VA-4 (Gas Hybrid)
    3.2m, 8-12hr
```

## Cumulative Investment (Air)

| Milestone | Cumulative Cost | Capability |
|-----------|-----------------|------------|
| VA-0 Complete | $200 | Basic flying, autopilot tuning |
| VA-1 Complete | $550 | Durable airframe, camera testing |
| VA-2 Complete | $2,750 | 3-4 hr endurance, 2.5 kg payload |
| VA-3 Complete | $3,700 | VTOL, 2-2.5 hr, 2.5 kg payload |
| VA-4 Complete | $6,000 | 8-12 hr gas-hybrid, unlimited range |

## Quick Selection Guide (Air)

| Need | Version | Why |
|------|---------|-----|
| Learning to fly | VA-0 | Cheap, expendable |
| Camera testing | VA-1 | Durable, payload bay |
| **Minimum cost autopilot** | **VA-1 ACAP** | $130, full code access |
| 2+ hour endurance | VA-1-LE | High efficiency wing |
| Speed + wind handling | VA-1-Fast | Higher wing loading |
| Large payload (2.5 kg) | VA-2 | Full-scale ALTI airframe |
| VTOL capability | VA-3 | No runway needed |
| Long endurance (8-12 hr) | VA-4 | Gas-electric hybrid |
| Starlink integration | VA-2/VA-3/VA-4 | 2.5 kg payload capacity |
| Close-range ISR | VA-5R | Quad, rapid deploy, VTOL |
| **Strike / Offensive** | **VA-5S** | Quad-based, warhead payload |

## Directory Structure

```
hardware/
├── README.md                  # This file
│
├── va0_skills_platform/       # Skills development platform
│   └── README.md
├── va1_durable_platform/      # Durable construction platform
│   └── README.md
├── va1_acap/                  # As Cheap As Possible (dRehmFlight + SBC)
│   └── README.md
├── va1_variants/              # Speed/endurance variants
│   └── README.md
├── va2_alti_fixedwing/        # ALTI-style fixed-wing
│   └── README.md
├── va3_alti_vtol/             # ALTI-style VTOL QuadPlane
│   └── README.md
├── va4_alti_hybrid/           # Gas-electric hybrid VTOL
│   └── README.md
├── va5_strike/                # VA-5R/VA-5S Quad platform
│   └── README.md
│
├── vs1_picket/                # VS-1 Picket surveillance vessel
│   └── README.md
│
└── vss1_[future]/             # Subsurface drone (planned)
    └── README.md
```

---

*See [Development Roadmap](../docs/roadmap/development_roadmap.md) for complete specifications.*
*See [Air Operations Fleet](../docs/operations/AIR_OPERATIONS_FLEET.md) for operational deployment.*
