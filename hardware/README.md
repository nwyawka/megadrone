# MegaDrone Hardware Versions

This directory contains documentation for each hardware version in the MegaDrone development roadmap.

## Version Overview

| Version | Type | Wingspan | Payload | Endurance | Cost | Status |
|---------|------|----------|---------|-----------|------|--------|
| [V0](v0_skills_platform/) | Fixed-Wing | 1.0-1.2m | 200g | 20-25 min | $200 | Development |
| [V1](v1_durable_platform/) | Fixed-Wing | 1.0-1.2m | 300g | 25-30 min | $550 | Development |
| [V1-ACAP](v1_acap/) | Fixed-Wing | 1.0-1.2m | 200g | 20-25 min | $130 | Development |
| [V1 Variants](v1_variants/) | Fixed-Wing | 1.5-2.4m | 300-500g | 1-2.5 hrs | $650-760 | Development |
| [V2](v2_alti_fixedwing/) | Fixed-Wing | 3.2m | 2.5 kg | 3-4 hrs | $1,830 | Development |
| [V3](v3_alti_vtol/) | VTOL | 3.2m | 2.5 kg | 2-2.5 hrs | $2,680 | Development |
| [V4](v4_alti_hybrid/) | VTOL Hybrid | 3.2m | 2.5 kg | 8-12 hrs | $4,750 | Development |

## Development Progression

```
V0 (Skills)          V1 (Durable)         V1-ACAP (Custom)
    │                    │                      │
    │   ┌────────────────┼──────────────────────┘
    │   │                │
    │   │     ┌──────────┴──────────┐
    │   │     │                     │
    ▼   ▼     ▼                     ▼
    V1-LE    V1-Fast           V1-Fast 2hr
   (2+ hrs)  (65 km/h)         (2hr @ 60km/h)
                    │
                    ▼
              V2 (ALTI FW)
              3.2m, 3-4hr
                    │
                    ▼
              V3 (ALTI VTOL)
              3.2m, 2-2.5hr
                    │
                    ▼
              V4 (Gas Hybrid)
              3.2m, 8-12hr
```

## Cumulative Investment

| Milestone | Cumulative Cost | Capability |
|-----------|-----------------|------------|
| V0 Complete | $200 | Basic flying, autopilot tuning |
| V1 Complete | $550 | Durable airframe, camera testing |
| V2 Complete | $2,750 | 3-4 hr endurance, 2.5 kg payload |
| V3 Complete | $3,700 | VTOL, 2-2.5 hr, 2.5 kg payload |
| V4 Complete | $6,000 | 8-12 hr gas-hybrid, unlimited range |

## Quick Selection Guide

| Need | Version | Why |
|------|---------|-----|
| Learning to fly | V0 | Cheap, expendable |
| Camera testing | V1 | Durable, payload bay |
| **Minimum cost autopilot** | **V1-ACAP** | $130, full code access |
| 2+ hour endurance | V1-LE | High efficiency wing |
| Speed + wind handling | V1-Fast | Higher wing loading |
| Large payload (2.5 kg) | V2 | Full-scale ALTI airframe |
| VTOL capability | V3 | No runway needed |
| Long endurance (8-12 hr) | V4 | Gas-electric hybrid |
| Starlink integration | V2/V3/V4 | 2.5 kg payload capacity |

## Directory Structure

```
hardware/
├── README.md                 # This file
├── v0_skills_platform/       # Skills development platform
│   └── README.md
├── v1_durable_platform/      # Durable construction platform
│   └── README.md
├── v1_acap/                  # As Cheap As Possible (dRehmFlight + SBC)
│   └── README.md
├── v1_variants/              # Speed/endurance variants
│   └── README.md
├── v2_alti_fixedwing/        # ALTI-style fixed-wing
│   └── README.md
├── v3_alti_vtol/             # ALTI-style VTOL QuadPlane
│   └── README.md
└── v4_alti_hybrid/           # Gas-electric hybrid VTOL
    └── README.md
```

---

*See [Development Roadmap](../docs/roadmap/development_roadmap.md) for complete specifications.*
