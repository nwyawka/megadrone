# MegaDrone Documentation

This directory contains all project documentation organized by category.

## Directory Structure

```
docs/
├── README.md           # This file
├── roadmap/            # Development planning
├── design/             # Design specifications
├── analysis/           # Analysis results and guides
├── compliance/         # FAA compliance (Remote ID, registration)
├── procurement/        # Suppliers and manufacturers
├── systems/            # Subsystem guides (video, telemetry, etc.)
├── guides/             # How-to guides
└── archive/            # Historical documents
```

---

## Documentation Index

### Roadmap

| Document | Description |
|----------|-------------|
| [development_roadmap.md](roadmap/development_roadmap.md) | **Complete version specifications (V0-V4)** |

The development roadmap is the primary reference document containing:
- Version overview table
- Detailed specifications for each version
- Hardware components and costs
- Payload options and pricing
- Weight budgets
- Starlink integration details
- Modular wing system (V1 variants)

---

### Design

| Document | Description |
|----------|-------------|
| [DESIGN_SUMMARY.md](design/DESIGN_SUMMARY.md) | Aircraft design overview |
| [bill_of_materials.md](design/bill_of_materials.md) | Component list with pricing |

---

### Analysis

| Document | Description |
|----------|-------------|
| [CFD_VALIDATION_GUIDE.md](analysis/CFD_VALIDATION_GUIDE.md) | CFD setup and analysis procedures |
| [CFD_VALIDATION_RESULTS.md](analysis/CFD_VALIDATION_RESULTS.md) | CFD validation results |
| [AEROSONDE_HQ_VTOL_ANALYSIS.md](analysis/AEROSONDE_HQ_VTOL_ANALYSIS.md) | VTOL configuration study |
| [PHASE2_ENGINE_ANALYSIS.md](analysis/PHASE2_ENGINE_ANALYSIS.md) | Gas engine analysis for V4 |

---

### Guides

| Guide | Description |
|-------|-------------|
| [OPENVSP_QUICK_START.md](guides/OPENVSP_QUICK_START.md) | OpenVSP tutorial (MacOS) |
| [GMSH_WORKFLOW.md](guides/GMSH_WORKFLOW.md) | GMSH UAV modeling guide |
| [QUICK_REFERENCE.md](guides/QUICK_REFERENCE.md) | Command quick reference |

---

### Compliance

| Document | Description |
|----------|-------------|
| [REMOTE_ID_GUIDE.md](compliance/REMOTE_ID_GUIDE.md) | **FAA Remote ID requirements, DIY options, home-builder exemptions** |

---

### Procurement

| Document | Description |
|----------|-------------|
| [COMPOSITE_MANUFACTURERS.md](procurement/COMPOSITE_MANUFACTURERS.md) | Carbon fiber/fiberglass suppliers (US preferred) |

---

### Systems

| Document | Description |
|----------|-------------|
| [LONG_RANGE_VIDEO_GUIDE.md](systems/LONG_RANGE_VIDEO_GUIDE.md) | **OpenHD, DroneBridge - DIY long range HD video ($200-500 vs $1000+)** |

---

### Archive

Historical planning documents (superseded by development_roadmap.md):

| Document | Description |
|----------|-------------|
| [DRONE_DEVELOPMENT_PLAN.md](archive/DRONE_DEVELOPMENT_PLAN.md) | Original development plan |
| [GMSH_IMPLEMENTATION_SUMMARY.md](archive/GMSH_IMPLEMENTATION_SUMMARY.md) | GMSH implementation notes |
| [OPENVSP_API_SUCCESS.md](archive/OPENVSP_API_SUCCESS.md) | OpenVSP API setup notes |

---

## Quick Links

### By Version

| Version | Hardware Docs | Key Document |
|---------|---------------|--------------|
| V0 | [hardware/v0_skills_platform/](../hardware/v0_skills_platform/) | Skills development platform |
| V1 | [hardware/v1_durable_platform/](../hardware/v1_durable_platform/) | Durable construction |
| V1-ACAP | [hardware/v1_acap/](../hardware/v1_acap/) | Custom autopilot (dRehmFlight + SBC) |
| V1 Variants | [hardware/v1_variants/](../hardware/v1_variants/) | LE, Fast, Fast 2hr wings |
| V2 | [hardware/v2_alti_fixedwing/](../hardware/v2_alti_fixedwing/) | ALTI-style fixed-wing |
| V3 | [hardware/v3_alti_vtol/](../hardware/v3_alti_vtol/) | VTOL QuadPlane |
| V4 | [hardware/v4_alti_hybrid/](../hardware/v4_alti_hybrid/) | Gas-electric hybrid |

### By Topic

| Topic | Document |
|-------|----------|
| **All Versions** | [development_roadmap.md](roadmap/development_roadmap.md) |
| **Remote ID / FAA** | [REMOTE_ID_GUIDE.md](compliance/REMOTE_ID_GUIDE.md) |
| **Long Range Video** | [LONG_RANGE_VIDEO_GUIDE.md](systems/LONG_RANGE_VIDEO_GUIDE.md) |
| **Composite Suppliers** | [COMPOSITE_MANUFACTURERS.md](procurement/COMPOSITE_MANUFACTURERS.md) |
| **CFD Analysis** | [CFD_VALIDATION_GUIDE.md](analysis/CFD_VALIDATION_GUIDE.md) |
| **VTOL Design** | [AEROSONDE_HQ_VTOL_ANALYSIS.md](analysis/AEROSONDE_HQ_VTOL_ANALYSIS.md) |
| **Gas Engine** | [PHASE2_ENGINE_ANALYSIS.md](analysis/PHASE2_ENGINE_ANALYSIS.md) |
| **OpenVSP** | [OPENVSP_QUICK_START.md](guides/OPENVSP_QUICK_START.md) |
| **GMSH** | [GMSH_WORKFLOW.md](guides/GMSH_WORKFLOW.md) |

---

## Related Directories

| Directory | Contents |
|-----------|----------|
| [../hardware/](../hardware/) | Hardware documentation by version |
| [../src/](../src/) | Source code (analysis, design, tools) |
| [../designs/](../designs/) | Design output files (VSP3, STEP, STL) |
| [../cfd/](../cfd/) | CFD analysis files |

---

*Last Updated: January 2026*
