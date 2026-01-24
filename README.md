# MegaDrone - UAV Development Project

**Project Goal:** Design and build fixed-wing and VTOL UAVs for ISR missions, progressing from small trainer platforms to ALTI Transition-class aircraft with 8-12 hour endurance.

**Status:** Development Phase
**Last Updated:** January 2026

---

## Project Overview

MegaDrone follows a progressive development path from skills-building platforms to professional ISR aircraft.

### Version Progression

| Version | Type | Wingspan | Payload | Endurance | Cost |
|---------|------|----------|---------|-----------|------|
| **V0** | Fixed-Wing | 1.0-1.2m | 200g | 20-25 min | $200 |
| **V1** | Fixed-Wing | 1.0-1.2m | 300g | 25-30 min | $550 |
| **V1-ACAP** | Fixed-Wing | 1.0-1.2m | 200g | 20-25 min | $130 |
| **V1-LE** | Fixed-Wing | 1.8-2.0m | 300g | 2-2.5 hrs | $660 |
| **V2** | Fixed-Wing (ALTI) | 3.2m | 2.5 kg | 3-4 hrs | $1,830 |
| **V3** | VTOL (ALTI) | 3.2m | 2.5 kg | 2-2.5 hrs | $2,680 |
| **V4** | VTOL Hybrid | 3.2m | 2.5 kg | **8-12 hrs** | $4,750 |

### Reference Design: ALTI Transition

V2/V3/V4 are inspired by the [ALTI Transition](https://altiunmanned.com/transition) VTOL UAS:
- 3.0m wingspan, 2.3m length
- 18 kg MTOW, 1 kg payload
- 12 hour endurance, 900 km range
- Hybrid propulsion (4 VTOL + 1 gas pusher)

### Starlink Integration

V2/V3/V4 support **2.5 kg payload** for ISR + Starlink:
- ISR camera: 1 kg
- Starlink Mini: 1.5 kg
- **Link range: Unlimited (global satellite)**

---

## Repository Structure

```
MegaDrone/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
│
├── docs/                        # Documentation
│   ├── roadmap/                 # Development roadmap
│   │   └── development_roadmap.md  # Complete version specs
│   ├── design/                  # Design documentation
│   │   ├── DESIGN_SUMMARY.md
│   │   └── bill_of_materials.md
│   ├── analysis/                # Analysis results
│   │   ├── CFD_VALIDATION_GUIDE.md
│   │   ├── CFD_VALIDATION_RESULTS.md
│   │   ├── AEROSONDE_HQ_VTOL_ANALYSIS.md
│   │   └── PHASE2_ENGINE_ANALYSIS.md
│   ├── guides/                  # How-to guides
│   │   ├── OPENVSP_QUICK_START.md
│   │   ├── GMSH_WORKFLOW.md
│   │   └── QUICK_REFERENCE.md
│   └── archive/                 # Historical documents
│       ├── DRONE_DEVELOPMENT_PLAN.md
│       └── ...
│
├── hardware/                    # Hardware documentation by version
│   ├── README.md               # Version overview
│   ├── v0_skills_platform/     # V0 specs and BOM
│   ├── v1_durable_platform/    # V1 specs and BOM
│   ├── v1_acap/                # V1-ACAP (dRehmFlight + SBC)
│   ├── v1_variants/            # V1-LE, V1-Fast variants
│   ├── v2_alti_fixedwing/      # V2 ALTI-style fixed-wing
│   ├── v3_alti_vtol/           # V3 VTOL QuadPlane
│   └── v4_alti_hybrid/         # V4 gas-electric hybrid
│
├── src/                         # Source code
│   ├── README_PYTHON_API.md    # API documentation
│   ├── analysis/               # Analysis scripts
│   │   ├── aero_analysis.py
│   │   ├── structural_analysis.py
│   │   ├── cfd_validation.py
│   │   └── ...
│   ├── design/                 # Design generation scripts
│   │   ├── phase1_openvsp_correct.py
│   │   ├── drone_sizing.py
│   │   └── ...
│   ├── mesh/                   # Mesh generation scripts
│   │   ├── gmsh_uav_generator.py
│   │   └── ...
│   └── tools/                  # Utility scripts
│       ├── bill_of_materials.py
│       ├── generate_pdf_report.py
│       └── ...
│
├── designs/                     # Design output files
│   ├── phase1/                 # Phase 1 UAV designs
│   │   ├── Phase1_UAV_Correct.vsp3
│   │   ├── Phase1_UAV_Correct.step
│   │   ├── Phase1_UAV_Correct.stl
│   │   └── ...
│   └── exports/                # Exported images/PDFs
│       ├── three_view_drawing.png
│       ├── MegaDrone_Design_Report.pdf
│       └── ...
│
├── cfd/                         # CFD analysis files
│   ├── airfoil_2d.su2
│   ├── su2_config_cruise.cfg
│   └── ...
│
└── venv/                        # Python virtual environment
```

---

## Quick Start

### 1. Setup Environment

```bash
cd /Users/matthewoneil/Desktop/Datawerkes/MegaDrone
source venv/bin/activate
```

### 2. Review Development Roadmap

```bash
# Complete version specifications
open docs/roadmap/development_roadmap.md

# Hardware version summaries
open hardware/README.md
```

### 3. Generate UAV Model

```bash
# OpenVSP Python API
python src/design/phase1_openvsp_correct.py

# GMSH mesh generation
python src/mesh/gmsh_uav_occ.py
```

### 4. Run Analysis

```bash
# Aerodynamic analysis
python src/analysis/aero_analysis.py

# Structural analysis
python src/analysis/structural_analysis.py

# CFD validation
python src/analysis/cfd_validation.py
```

---

## Development Path

### Skills Development (V0 → V1)

```
V0 ($200)              V1 ($550)              V1-ACAP ($130)
Foam construction  →   Durable build     or   Custom autopilot
Learn to fly           Camera testing         Full code access
ArduPilot basics       Gimbal integration     dRehmFlight + SBC
```

### Scaling Up (V1 Variants)

```
V1 Base (1.0-1.2m)
        │
        ├── V1-LE (1.8-2.0m) → 2+ hrs @ 45-50 km/h
        ├── V1-Fast (1.5-1.7m) → 1 hr @ 55-65 km/h
        └── V1-Fast 2hr (2.2-2.4m) → 2+ hrs @ 55-60 km/h
```

### ALTI-Class Development (V2 → V3 → V4)

```
V2 (Fixed-Wing)        V3 (VTOL)              V4 (Hybrid)
3.2m wingspan          + 4 VTOL motors        + Gas pusher
3-4 hr endurance       2-2.5 hr endurance     8-12 hr endurance
Electric pusher        All-electric           Gas + Electric
$1,830                 $2,680                 $4,750
```

---

## Key Features

### V1-ACAP: Custom Autopilot ($130)

Build your own autopilot with full code access:
- **Inner loop:** Teensy 4.0 + dRehmFlight (stabilization)
- **Outer loop:** SBC (RPi/ESP32) + GPS (navigation)
- **Capabilities:** Waypoints, RTH, autonomous missions
- **Cost:** $50-60 for FC stack vs $200+ for Pixhawk

### V4: Long-Endurance Hybrid

Professional-grade ISR platform:
- **8-12 hour** gas-powered cruise
- **2.5 kg payload** (ISR + Starlink)
- **900 km range**
- **Unlimited link range** via Starlink
- **$4/hr operating cost**

---

## Tools and Software

### Design Tools

| Tool | Purpose | Status |
|------|---------|--------|
| **OpenVSP** | Parametric aircraft geometry | Installed |
| **GMSH** | Mesh generation for CFD | Installed (`pip install gmsh`) |
| **SU2** | CFD analysis | Configured |
| **AeroSandbox** | Quick aero analysis | Installed |

### Autopilot

| Tool | Purpose |
|------|---------|
| **ArduPilot** | Flight controller firmware |
| **Mission Planner** | Ground control station |
| **iNav** | Alternative FC firmware |
| **dRehmFlight** | Custom FC (V1-ACAP) |

### Flight Controllers

| Version | Controller |
|---------|------------|
| V0/V1 | Pixhack or SpeedyBee F405 Wing Mini |
| V1-ACAP | Teensy 4.0 + SBC |
| V2/V3 | Pixhawk 6C |
| V4 | Pixhawk 6X |

---

## Cumulative Investment

| Milestone | Cost | Capability |
|-----------|------|------------|
| V0 Complete | $200 | Basic flying, autopilot tuning |
| V1 Complete | $550 | Durable airframe, camera testing |
| V1-ACAP | $130 | Custom autopilot, full code access |
| V2 Complete | $2,750 | 3-4 hr endurance, 2.5 kg payload |
| V3 Complete | $3,700 | VTOL, runway-independent |
| V4 Complete | $6,000 | 8-12 hr hybrid, unlimited range |

---

## Documentation Index

### Core Documents

| Document | Description |
|----------|-------------|
| [Development Roadmap](docs/roadmap/development_roadmap.md) | Complete version specifications |
| [Hardware Overview](hardware/README.md) | Hardware by version |
| [Design Summary](docs/design/DESIGN_SUMMARY.md) | Aircraft design overview |

### Guides

| Guide | Description |
|-------|-------------|
| [OpenVSP Quick Start](docs/guides/OPENVSP_QUICK_START.md) | OpenVSP tutorial |
| [GMSH Workflow](docs/guides/GMSH_WORKFLOW.md) | Mesh generation guide |
| [Quick Reference](docs/guides/QUICK_REFERENCE.md) | Command reference |

### Analysis

| Document | Description |
|----------|-------------|
| [CFD Validation Guide](docs/analysis/CFD_VALIDATION_GUIDE.md) | CFD setup and analysis |
| [CFD Results](docs/analysis/CFD_VALIDATION_RESULTS.md) | CFD validation results |
| [VTOL Analysis](docs/analysis/AEROSONDE_HQ_VTOL_ANALYSIS.md) | VTOL configuration study |

---

## Next Steps

1. **V0 Build** - Foam trainer with existing hardware
2. **V1 Build** - Durable platform with camera integration
3. **V1-ACAP** - Custom autopilot development (optional)
4. **V2 Design** - ALTI-style fixed-wing CAD
5. **V3 Conversion** - Add VTOL capability
6. **V4 Integration** - Gas engine + Starlink

---

## License

**Proprietary - Internal Project Documentation**

This repository contains design documentation and code for a private UAV development project.

---

**Last Updated:** January 2026
**Version:** 2.0
**Status:** Development Phase
