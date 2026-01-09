# MegaDrone - Fixed-Wing UAV Development Project

**Project Goal:** Design and build fixed-wing UAVs for ISR (Intelligence, Surveillance, Reconnaissance) missions, progressing from small trainer to Aerosonde-class platform.

**Status:** Planning and Design Phase  
**Last Updated:** January 8, 2026

---

## Project Overview

### Two-Phase Development

**Phase 1: Starter Drone (30-60 min endurance)**
- Wingspan: 2.2 m (7.2 ft)
- Weight: 22 lbs (10 kg)
- Propulsion: Electric (LiPo battery)
- Purpose: Learn design process, validate tools, build pilot skills
- Budget: $5,000-$10,000
- Timeline: 6 months

**Phase 2: ISR Platform (8-12 hour endurance)**
- Wingspan: 4.0+ m (13+ ft)
- Weight: 40-50 lbs (18-23 kg)
- Propulsion: Gasoline engine (NGH GT25 25cc)
- Purpose: Maritime ISR for JPA Privateer operations
- Optional: VTOL capability (Aerosonde HQ variant)
- Budget: $50,000-$100,000 (custom) or $100,000-$200,000 (commercial)
- Timeline: 12-18 months

---

## Mission Requirements (from JPA Business Plan)

**Primary Customer:** U.S. Customs and Border Protection (CBP), DEA, USCG  
**Mission:** Maritime drug interdiction support (Gulf of Mexico, Caribbean, California coast)

**Requirements:**
- 8-12 hour endurance
- EO/IR camera with real-time datalink
- 100+ km operational radius
- Day/night operations
- Operating cost: <$500/hour
- Contract value: $400K-$2M annually (Years 1-3)

---

## Repository Structure

```
MegaDrone/
├── README.md                          # This file
├── DRONE_DEVELOPMENT_PLAN.md          # Complete design guide
├── OPENVSP_QUICK_START.md             # OpenVSP tutorial (MacOS)
├── GMSH_WORKFLOW.md                   # GMSH UAV modeling guide ✨ NEW
├── PHASE2_ENGINE_ANALYSIS.md          # NGH GT25 engine analysis
├── AEROSONDE_HQ_VTOL_ANALYSIS.md      # VTOL hybrid configuration
│
├── designs/                           # Generated UAV models
│   ├── Phase1_UAV_GMSH.stl           # ✨ GMSH-generated STL (ready)
│   ├── Phase1_UAV_GMSH.msh           # ✨ GMSH mesh format
│   ├── Phase1_UAV_GMSH.vtk           # ✨ ParaView visualization
│   └── Phase1_UAV_GMSH.geo_unrolled  # ✨ GMSH script
│
├── scripts/                           # Python automation
│   ├── gmsh_uav_simple.py            # ✨ GMSH UAV generator (working!)
│   ├── gmsh_uav_generator.py         # Advanced GMSH version
│   ├── openvsp_setup.py              # OpenVSP API setup (requires build)
│   ├── phase1_fixedwing.py           # OpenVSP template (requires build)
│   └── README_PYTHON_API.md          # OpenVSP API notes
│
├── venv/                              # Python virtual environment
├── requirements.txt                   # Python dependencies (gmsh, numpy, etc)
│
└── docs/                              # Additional documentation
    ├── airfoils/                      # Airfoil coordinate files
    ├── references/                    # PDFs, datasheets
    └── calculations/                  # Performance spreadsheets
```

---

## Tools and Software

### Design Tools

**GMSH** ✨ (Installed: `pip install gmsh`) **← PRIMARY TOOL**
- Parametric 3D geometry generation
- Automatic mesh generation
- Python API (ready to use!)
- Export: STL, MSH, VTK formats
- Website: https://gmsh.info
- **Status: Working! See `GMSH_WORKFLOW.md`**

**OpenVSP** (Installed: `/Users/matthewoneil/OpenVSP-3.46.0-MacOS`)
- Parametric aircraft geometry
- Mass properties calculation
- Drag estimation
- Import STL from GMSH
- GitHub: https://github.com/OpenVSP/OpenVSP
- **Note:** Python API requires building from source

**XFLR5** (Recommended)
- Airfoil and wing analysis
- Lift/drag polar calculation
- Free download: http://www.xflr5.tech

**Fusion 360 or SolidWorks**
- Detail design (structure, mounts, fittings)
- Manufacturing drawings

### Autopilot and Ground Control

**Ardupilot** (ArduPlane firmware)
- Open-source autopilot
- Waypoint navigation, autonomous flight
- Documentation: https://ardupilot.org/plane/

**TitanPlanner** (Ground Control Station)
- Modified Mission Planner with improved UI
- GitHub: https://github.com/Titan-Dynamics/TitanPlanner
- Mission planning, telemetry, parameter tuning

**Pixhawk Flight Controller**
- Hardware: Pixhawk 4 (Phase 1) or Cube Orange+ (Phase 2)
- Runs Ardupilot firmware

### Python Environment

**Virtual Environment:**
```bash
source venv/bin/activate
```

**Dependencies:**
- gmsh>=4.13.0 (3D geometry and meshing) ✨
- numpy>=1.24.0 (numerical computations)
- pandas>=2.0.0 (data analysis)
- matplotlib>=3.7.0 (visualization)
- pyyaml>=6.0 (configuration files)

---

## Quick Start

### 1. Generate UAV Model with OpenVSP Python API ✨ **NEW - NOW WORKING!**

**The OpenVSP Python API is now installed and functional!**

**Setup environment:**
```bash
cd /Users/matthewoneil/Desktop/Datawerkes/MegaDrone
source venv/bin/activate
```

**Generate Phase 1 UAV model:**
```bash
python scripts/phase1_fixedwing.py
```

**Output:** `designs/Phase1_FixedWing_Trainer.vsp3` (292KB)
- Native OpenVSP parametric model
- Includes: Wing, fuselage, H-tail, V-tail, propeller
- Airfoil: NACA 2412 (wing), NACA 0012 (tails)
- Full parametric control via Python

**Open in OpenVSP:**
```bash
cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS
./vsp
# File → Open → designs/Phase1_FixedWing_Trainer.vsp3
```

**Documentation:**
```bash
open OPENVSP_API_SUCCESS.md  # Installation guide
open OPENVSP_QUICK_START.md  # GUI tutorial
```

### 2. Alternative: Generate with GMSH (for meshing/CFD)

**Generate Phase 1 UAV model:**
```bash
python scripts/gmsh_uav_occ.py
```

**Output files in `designs/`:**
- `Phase1_UAV_OCC_HiRes.stl` - Import to OpenVSP or 3D print
- `Phase1_UAV_OCC_HiRes.step` - CAD format (OpenVSP compatible)
- `Phase1_UAV_OCC_HiRes.msh` - GMSH mesh for CFD

**View model:**
```bash
gmsh designs/Phase1_UAV_OCC_HiRes.stl
# or
open designs/Phase1_UAV_OCC_HiRes.stl
```

**Documentation:**
```bash
open GMSH_WORKFLOW.md
```

### 3. OpenVSP GUI Workflow (Manual)

**Launch OpenVSP:**
```bash
cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS
./vsp
```

**Follow tutorial:**
```bash
open OPENVSP_QUICK_START.md
```

**Manual design workflow:**
1. Create geometry in OpenVSP GUI
2. Export STEP/STL/DXF
3. Import into CAD for detail design

### 3. Review Documentation

**Design guides:**
```bash
open DRONE_DEVELOPMENT_PLAN.md  # Complete design process
open GMSH_WORKFLOW.md           # GMSH UAV modeling guide
open OPENVSP_QUICK_START.md     # OpenVSP GUI tutorial
```

**Key sections:**
- Aerosonde UAV capabilities (benchmark)
- JPA Privateer mission requirements
- Aircraft design process (step-by-step)
- GMSH parametric scripting
- Airfoil selection
- Ardupilot integration

---

## Design Workflow (Manual with OpenVSP GUI)

### Phase 1: Starter Drone

**Step 1: OpenVSP Model (Week 1-2)**
- Follow OPENVSP_QUICK_START.md tutorial
- Create: Wing, fuselage, tail, propeller
- Calculate mass properties, adjust CG to 25-30% MAC
- Export: STEP (CAD), DXF (wing ribs), STL (visualization)

**Step 2: CAD Detail Design (Week 3-4)**
- Import STEP file into Fusion 360
- Design: Wing spar, servo mounts, battery tray, motor mount
- Create manufacturing drawings

**Step 3: Procurement (Week 5-6)**
- Order: Foam, carbon fiber, motor, ESC, battery, Pixhawk, RC gear
- Budget: ~$2,000-3,000

**Step 4: Fabrication (Month 2-3)**
- Hot-wire cut foam wings
- Assemble fuselage
- Install electronics
- Surface finish (spackle, sand, paint)

**Step 5: Ground Testing (Month 4)**
- CG check, control surface throws
- Ardupilot configuration
- Motor bench test
- Telemetry range test

**Step 6: Flight Testing (Month 5-6)**
- First flight (manual mode)
- Autopilot testing (FBWA, Auto modes)
- Endurance testing (30-60 min goal)

---

## Key Design Decisions

### Airfoil Selection

**Phase 1 (Trainer):**
- **Recommended:** Eppler E423 or Selig S1223
- **Rationale:** High L/D, gentle stall, proven at low Reynolds number
- **Download:** https://m-selig.ae.illinois.edu/ads/coord_database.html

**Phase 2 (ISR):**
- **Recommended:** Eppler E423
- **Rationale:** Best efficiency for long endurance cruise

### Propulsion

**Phase 1:**
- Electric: 1200W brushless motor, 6S 10000 mAh LiPo
- Propeller: 13" diameter, 2-blade folding (pusher)

**Phase 2:**
- Gasoline: NGH GT25 25cc 2-stroke (~2.5-3.0 HP)
- Fuel: 1.5-2.0 gallons for 10-12 hour mission
- See: PHASE2_ENGINE_ANALYSIS.md

### VTOL Option (Phase 2b)

**Add VTOL if:**
- Ship-based operations required
- No runway access
- Budget allows +$8,000

**Skip VTOL if:**
- Land-based operations acceptable
- Maximizing endurance critical
- Budget-constrained

**See:** AEROSONDE_HQ_VTOL_ANALYSIS.md

---

## Aerosonde Benchmark Specifications

**Aerosonde Mk 4.7G (Standard Fixed-Wing):**
- Wingspan: 12-14.5 ft (3.8-4.4 m)
- Weight: 71-79 lbs (32-36 kg)
- Endurance: 10-16 hours
- Engine: 3.5 HP gasoline 2-stroke
- Launch: Catapult
- Recovery: Net/parachute/skyhook
- Cost: $100K-$200K (system)

**Aerosonde Mk 4.7 HQ (VTOL Variant):**
- Wingspan: 17 ft (5.2 m) - larger for VTOL weight
- Weight: 80-90 lbs (36-41 kg estimated)
- Endurance: Up to 20 hours
- Propulsion: Hybrid (gasoline cruise + electric VTOL)
- Launch/Recovery: Vertical takeoff and landing
- Operational: U.S. Special Operations Command (SOCOM)
- Cost: $200K-$300K (estimated)

**Our Target (Phase 2):**
- Stay under 55 lbs (FAA Part 107 limit)
- 10-12 hour endurance (sufficient for ISR mission)
- Cost: $50K-$100K (custom design, 50-75% cheaper)

---

## Regulatory Compliance

### FAA Part 107 (Small UAS)

**Requirements:**
- Aircraft weight <55 lbs
- Remote pilot certificate (pass FAA knowledge test)
- Aircraft registration
- VLOS (visual line of sight) or waiver for BVLOS
- Maximum altitude: 400 ft AGL (or waiver)

**For ISR Mission:**
- Apply for BVLOS (Beyond Visual Line of Sight) waiver
- Justification: Maritime operations, low population density
- Requires: Detect-and-avoid capability, safety case, ops manual
- Approval time: 90-120 days

**Alternative: COA (Certificate of Authorization)**
- If operating as federal contractor (CBP, DEA)
- Faster approval, less restrictive
- Requires agency sponsorship

---

## Budget Summary

### Phase 1: Starter Drone

| Category | Cost |
|----------|------|
| Materials (foam, carbon, composites) | $800 |
| Propulsion (motor, ESC, battery, prop) | $500 |
| Avionics (Pixhawk, GPS, telemetry) | $600 |
| RC transmitter/receiver | $350 |
| Payload (camera, gimbal) | $400 |
| Tools and consumables | $500 |
| Contingency (20%) | $800 |
| **Total** | **$4,000-$6,000** |

### Phase 2: ISR Platform (Custom Design)

| Category | Cost |
|----------|------|
| Airframe (composite materials) | $15,000 |
| Gasoline engine (NGH GT25) + fuel system | $1,000 |
| Avionics (Cube Orange+, RTK GPS) | $1,500 |
| EO/IR Camera (FLIR Duo Pro R) | $5,000 |
| Datalink (long-range) | $1,000 |
| Launch/recovery system | $2,000 |
| Development and testing | $10,000 |
| **Total (Fixed-Wing)** | **$35,000-$50,000** |
| **VTOL Add-On** | **+$8,000** |

---

## Next Steps (Week 1-2)

### Immediate Actions

- [x] Review DRONE_DEVELOPMENT_PLAN.md (complete)
- [x] Review OpenVSP tutorial (complete)
- [x] Review engine analysis (complete)
- [x] Review VTOL analysis (complete)
- [x] **Generate UAV model with GMSH** ✨ (complete!)
- [x] **Export STL for OpenVSP/3D printing** ✨ (complete!)
- [ ] **Import STL into OpenVSP and verify geometry**
- [ ] **Download E423 airfoil coordinates** from UIUC database
- [ ] **3D print 1:10 scale model** (optional visualization)
- [ ] **Obtain FAA Part 107 certificate** (if not already have)

### Design Phase (Month 1)

- [ ] Import GMSH model to OpenVSP
- [ ] Run OpenVSP analysis (mass properties, drag)
- [ ] Run XFLR5 analysis (validate L/D, stall characteristics)
- [ ] Refine airfoil (import E423 coordinates to GMSH)
- [ ] Finalize component selection (motor, battery, etc.)
- [ ] Order long-lead items (composite materials, electronics)

---

## Resources

### Documentation (This Repository)

- `DRONE_DEVELOPMENT_PLAN.md` - Complete design guide (70+ pages)
- `GMSH_WORKFLOW.md` - GMSH UAV modeling guide ✨ NEW
- `OPENVSP_QUICK_START.md` - OpenVSP tutorial for MacOS
- `PHASE2_ENGINE_ANALYSIS.md` - NGH GT25 engine specifications
- `AEROSONDE_HQ_VTOL_ANALYSIS.md` - VTOL hybrid configuration

### External Links

**Design Tools:**
- OpenVSP: https://openvsp.org
- OpenVSP GitHub: https://github.com/OpenVSP/OpenVSP
- XFLR5: http://www.xflr5.tech
- Airfoil Database: https://m-selig.ae.illinois.edu/ads/coord_database.html

**Autopilot:**
- Ardupilot: https://ardupilot.org/plane/
- TitanPlanner: https://github.com/Titan-Dynamics/TitanPlanner
- ArduPlane QuadPlane: https://ardupilot.org/plane/docs/quadplane-overview.html

**Regulatory:**
- FAA Part 107: https://www.faa.gov/uas/commercial_operators/part_107
- FAA UAS Classifications: https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap11_section_3.html
- DroneZone (waivers): https://faadronezone.faa.gov

**JPA Privateer Business:**
- See: `../JPA/` directory (Anti-Cartel Maritime ISR contractor business plan)

---

## Contact and Collaboration

**Project Owner:** Matthew O'Neil  
**Location:** Florida (ideal for maritime ISR operations)  
**Background:** Commercial drone pilot (FAA Part 107), aerospace/defense interest

**Goal:** Build capability to support federal ISR contracts (CBP, DEA, USCG) with cost-effective, long-endurance UAV platforms.

---

## License

**Proprietary - Internal Project Documentation**

This repository contains design documentation and code for a private UAV development project. Not for public distribution.

---

**Last Updated:** January 8, 2026  
**Version:** 1.0  
**Status:** Planning Phase - Ready to Begin Phase 1 Design
