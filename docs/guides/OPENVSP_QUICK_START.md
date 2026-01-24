# OpenVSP Quick Start Guide for MegaDrone Project

**Installation Location:** `/Users/matthewoneil/OpenVSP-3.46.0-MacOS`  
**Version:** 3.46.0  
**Platform:** MacOS  
**Date:** January 8, 2026

---

## Table of Contents

1. [Launch OpenVSP](#launch-openvsp)
2. [Phase 1 Starter Drone Model](#phase-1-starter-drone-model)
3. [Basic Operations](#basic-operations)
4. [Export for Manufacturing](#export-for-manufacturing)
5. [Mass Properties Calculation](#mass-properties-calculation)
6. [Troubleshooting](#troubleshooting)

---

## Launch OpenVSP

### From Terminal

```bash
cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS
./vsp
```

### Create Desktop Shortcut (Optional)

1. Open Finder
2. Navigate to `/Users/matthewoneil/OpenVSP-3.46.0-MacOS`
3. Right-click on `vsp` application
4. Select "Make Alias"
5. Drag alias to Desktop
6. Rename to "OpenVSP"

---

## Phase 1 Starter Drone Model

### Step-by-Step Tutorial: Build Your First Drone in OpenVSP

#### Target Specifications (Phase 1)
- **Wingspan:** 2.2 m (7.2 ft)
- **Wing Area:** 0.55 m² (5.9 ft²)
- **Length:** 1.3 m (4.3 ft)
- **Airfoil:** Eppler E423
- **Configuration:** High wing, pusher propeller, H-tail

---

### Step 1: Create New Project

1. Launch OpenVSP
2. File → New
3. File → Save As → `Phase1_Drone_v1.vsp3`
   - Save to: `/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/`

---

### Step 2: Add Main Wing

#### 2.1 Create Wing Component

1. Click **Component** → **Add** → **Wing**
2. In the left panel, you'll see "Wing" listed

#### 2.2 Set Wing Parameters

**Click on Wing component to select it**

**Plan Tab:**
1. **Span:** 2.2 m
   - Click in the "Total Span" field
   - Type: `2.2`
   
2. **Root Chord:** 0.28 m
   - Section 0 → Root Chord: `0.28`
   
3. **Tip Chord:** 0.22 m
   - Section 1 → Tip Chord: `0.22`
   - (This gives taper ratio of 0.79, good for stability)

4. **Sweep:** 0° (straight wing)
   - Sweep: `0`

5. **Dihedral:** 2° (slight upward angle for stability)
   - Dihedral: `2`

6. **Twist:** -2° at tip (washout for gentle stall)
   - Section 1 → Twist: `-2`

**Section Tab:**
1. Select "Section 0" (root)
2. **Airfoil:** 
   - Click "Airfoil" button
   - Type: "Airfoil File"
   - Click "Read File"
   - Navigate to E423 coordinates file (download from UIUC if needed)
   - Or use built-in: Select "NACA 4-Series" → Enter `2412` for now
   
3. Apply same airfoil to Section 1 (tip)

**XForm Tab (Position Wing):**
1. **Z Location:** 0.15 m (high wing, above fuselage)
   - Z Loc: `0.15`
   
2. **X Location:** 0.4 m (position relative to fuselage CG)
   - X Loc: `0.4`

3. **Rotation:**
   - X Rot: `0` (no roll)
   - Y Rot: `0` (no yaw)
   - Z Rot: `0` (no pitch initially, set incidence later)

---

### Step 3: Add Fuselage

#### 3.1 Create Fuselage Component

1. Component → Add → Fuselage (or "Stack")
2. Rename to "Fuselage"

#### 3.2 Define Fuselage Shape

**XSec (Cross-Section) Tab:**

OpenVSP builds fuselages from stacked cross-sections. We'll create 5 sections:

**Section 0: Nose**
1. Select "XSec 0"
2. Type: Circle
3. Diameter: `0.08` m
4. X Location: `0` m
5. Y Location: `0` m
6. Z Location: `0` m

**Section 1: Front Transition**
1. Add new section: Click "Insert After"
2. Type: Circle
3. Diameter: `0.14` m
4. X Location: `0.2` m

**Section 2: Mid-Section (Payload Bay)**
1. Insert After
2. Type: Circle (or Rectangle for flat bottom camera mount)
3. Width: `0.15` m
4. Height: `0.14` m (if rectangle, slightly flatter)
5. X Location: `0.6` m

**Section 3: Rear Transition**
1. Insert After
2. Type: Circle
3. Diameter: `0.10` m
4. X Location: `1.0` m

**Section 4: Tail Boom**
1. Insert After
2. Type: Circle
3. Diameter: `0.05` m (thin for tail boom)
4. X Location: `1.3` m

**Result:** Streamlined fuselage, wider in middle, tapers to tail

---

### Step 4: Add Horizontal Stabilizer (Tail)

#### 4.1 Create H-Tail

1. Component → Add → Wing
2. Rename to "H_Tail"

#### 4.2 Set H-Tail Parameters

**Plan Tab:**
1. **Span:** 0.7 m
2. **Root Chord:** 0.18 m
3. **Tip Chord:** 0.14 m (slight taper)
4. **Sweep:** 0°
5. **Dihedral:** 0° (flat horizontal tail)

**Section Tab:**
1. Airfoil: Symmetric (NACA 0012 or flat plate)
   - Select "NACA 4-Series" → Enter `0012`

**XForm Tab:**
1. **X Location:** 1.15 m (rear of fuselage)
2. **Z Location:** 0.05 m (slightly above tail boom)

---

### Step 5: Add Vertical Stabilizer (Fin)

#### 5.1 Create V-Tail

1. Component → Add → Wing
2. Rename to "V_Tail"

#### 5.2 Set V-Tail Parameters

**Plan Tab:**
1. **Span:** 0.25 m (this will be the height when rotated)
2. **Root Chord:** 0.20 m
3. **Tip Chord:** 0.12 m

**Section Tab:**
1. Airfoil: Symmetric (NACA 0012)

**XForm Tab:**
1. **X Location:** 1.15 m (same as H-tail)
2. **Z Location:** 0.05 m
3. **Rotation:**
   - **X Rot:** 90° (rotate to vertical)
   - Type `90` in X Rot field

**Symmetry:**
1. In the wing parameters, find "Sym Planar Flag"
2. Set to: **None** (no left-right symmetry for vertical tail)

---

### Step 6: Add Propeller

#### 6.1 Create Propeller

1. Component → Add → Prop
2. Rename to "Propeller"

#### 6.2 Set Propeller Parameters

**Design Tab:**
1. **Diameter:** 0.33 m (13 inches)
2. **Number of Blades:** 2
3. **Construct:** Blades (shows actual blade geometry)

**XForm Tab:**
1. **X Location:** 1.35 m (rear of fuselage, pusher config)
2. **Z Location:** 0.0 m (aligned with fuselage centerline)
3. **Rotation:**
   - **X Rot:** 0° (propeller disc perpendicular to fuselage)

---

### Step 7: Verify Design

#### 7.1 View Model

1. **Fit View:** View → Fit View (or press 'F' key)
2. **Rotate View:** 
   - Right-click and drag to rotate
   - Scroll wheel to zoom
   - Middle-click and drag to pan

#### 7.2 Check Dimensions

1. Geom → Measure
2. Click on wing tip, then opposite wing tip
3. Verify wingspan = 2.2 m

#### 7.3 Screenshot

1. View → Set Camera
2. Adjust to good angle (slight 3/4 view)
3. Screen → Screenshot
4. Save to: `Phase1_Drone_v1_render.png`

---

## Basic Operations

### Viewing Controls

| Action | MacOS |
|--------|-------|
| **Rotate** | Right-click + Drag |
| **Zoom** | Scroll Wheel |
| **Pan** | Middle-click + Drag (or Cmd + Right-click) |
| **Fit View** | Press 'F' or View → Fit View |
| **Top View** | View → Set View → Top |
| **Side View** | View → Set View → Right |
| **Front View** | View → Set View → Front |

### Measurement Tools

1. **Comp Geom (Component Geometry):**
   - Analysis → Comp Geom
   - Click "Execute"
   - Displays: Wetted area, volume, bounding box
   - Export: Text file with dimensions

2. **Mass Properties:**
   - Analysis → Mass Properties
   - (See detailed section below)

### Saving Work

1. **Save Often:** File → Save (Cmd+S)
2. **Version Control:** Save as `Phase1_Drone_v2.vsp3`, `v3.vsp3`, etc.
3. **Backup:** Keep copies on external drive or cloud

---

## Export for Manufacturing

### Export 2D Profiles (for CNC/Laser Cutting)

#### Wing Ribs

1. Select Wing component
2. File → Export → Airfoil Points
3. Select export format:
   - **DXF:** For CAD import (AutoCAD, Fusion 360)
   - **SVG:** For laser cutters
4. Save each rib section (root, mid, tip)

**Use Case:** Cut ribs from plywood or foam using CNC router or laser cutter

#### Fuselage Cross-Sections

1. Select Fuselage
2. File → Export → Cross-Section Curves
3. Export as DXF or SVG
4. Import into CAD to create formers/bulkheads

---

### Export 3D Model

#### For CAD (SolidWorks, Fusion 360)

1. File → Export → STEP or IGES
2. Save as: `Phase1_Drone.step`
3. Import into CAD for detailed design (brackets, fittings, etc.)

#### For 3D Printing

1. File → Export → STL
2. Save as: `Phase1_Drone.stl`
3. Import into slicer (Cura, PrusaSlicer) if printing parts

#### For CFD Analysis

1. File → Export → STL or STEP
2. Import into CFD software:
   - OpenFOAM (free)
   - ANSYS Fluent (commercial)
   - SU2 (free, open-source)

---

## Mass Properties Calculation

### Step 1: Assign Component Masses

This is critical for calculating Center of Gravity (CG).

#### 1.1 Open Mass Properties

1. Analysis → Mass Properties
2. Window will open showing all components

#### 1.2 Set Component Masses

**For Phase 1 Drone:**

Click on each component and enter mass:

| Component | Mass (kg) | Mass (lbs) |
|-----------|-----------|------------|
| Wing | 1.1 | 2.4 |
| Fuselage | 0.7 | 1.5 |
| H_Tail | 0.1 | 0.2 |
| V_Tail | 0.1 | 0.2 |
| Propeller | 0.1 | 0.2 |

**Add Point Masses (for components not modeled as geometry):**

1. Click "Add Point Mass"
2. Name: "Battery"
   - Mass: 3.0 kg (6.6 lbs)
   - X Location: 0.45 m (adjust to get CG at 25-30% MAC)
   - Y Location: 0 m
   - Z Location: 0 m (bottom of fuselage)

3. Add more point masses:
   - "Motor": 0.2 kg at X=1.3 m, Z=0
   - "Avionics": 0.5 kg at X=0.5 m, Z=0
   - "Payload (Camera)": 0.5 kg at X=0.6 m, Z=-0.1 m (below fuselage)

#### 1.3 Calculate Total Mass and CG

1. Click "Compute"
2. OpenVSP calculates:
   - **Total Mass:** Should be ~6.3 kg (13.9 lbs) empty + 3 kg battery = 9.3 kg (20.5 lbs)
   - **CG Location:** X, Y, Z coordinates
   - **Moments of Inertia:** Ixx, Iyy, Izz

#### 1.4 Check CG Location

**Target:** CG should be at 25-30% of Mean Aerodynamic Chord (MAC)

**Calculate MAC:**
1. For tapered wing: MAC ≈ (2/3) * (Root + Tip - (Root*Tip)/(Root+Tip))
2. For our wing: MAC ≈ 0.26 m

**Target CG Location:**
- 25% MAC = 0.065 m aft of wing leading edge
- Wing leading edge is at X = 0.4 m
- **Target CG:** X = 0.465 m

**If CG is too far aft:** Move battery forward
**If CG is too far forward:** Move battery aft, or add nose weight

#### 1.5 Iterate

1. Adjust point mass locations
2. Click "Compute" again
3. Repeat until CG is in target range
4. File → Save (saves mass properties with model)

### Step 2: Export Mass Properties

1. In Mass Properties window
2. Click "Export"
3. Save as: `Phase1_Drone_mass_props.txt`
4. Contains: Total mass, CG, inertia tensor

**Use this data for:**
- Ardupilot configuration (set CG in parameters)
- Structural analysis (loads on wing spar)
- Flight dynamics simulation

---

## Troubleshooting

### OpenVSP Won't Launch

**Problem:** Double-clicking `vsp` does nothing

**Solution:**
1. Open Terminal
2. Navigate: `cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS`
3. Make executable: `chmod +x vsp`
4. Launch: `./vsp`

---

### Components Not Showing

**Problem:** Added component but can't see it in 3D view

**Solution:**
1. Check "Geom" panel (left side) - is component listed?
2. Click on component name to select
3. Check XForm tab - is it positioned at origin or far away?
4. Try "View → Fit View" (F key)

---

### Airfoil File Won't Load

**Problem:** Can't import Eppler E423 coordinates

**Solution:**
1. Download E423 coordinates from UIUC Airfoil Database:
   - https://m-selig.ae.illinois.edu/ads/coord_database.html
   - Search for "e423"
   - Download .dat file

2. File format must be **Selig or Lednicer format**:
   ```
   E423 Airfoil
   1.00000  0.00000
   0.95000  0.01234
   ...
   ```

3. In OpenVSP:
   - Section → Airfoil → Read File
   - Select .dat file
   - Should import successfully

**Alternative:** Use built-in NACA airfoils for testing, import custom later

---

### Export Fails

**Problem:** Export to STEP/DXF produces errors

**Solution:**
1. Check for overlapping components (fuselage intersecting wing)
2. Simplify geometry (reduce number of cross-sections)
3. Try different export format:
   - STEP often more reliable than IGES
   - STL always works but is faceted (not smooth curves)

---

### Mass Properties Shows Wrong CG

**Problem:** CG is way off expected location

**Solution:**
1. Check point mass locations (X, Y, Z) - typo in position?
2. Verify component masses - did you enter kg vs. lbs correctly?
3. OpenVSP uses meters by default - check unit settings
4. Make sure "Include Triangle Masses" is checked if using component geometry mass

---

## Next Steps After OpenVSP Design

1. **Aerodynamic Analysis:**
   - Export geometry to XFLR5 (free airfoil/wing analysis tool)
   - Calculate CL, CD, L/D ratio
   - Validate performance estimates

2. **CAD Detail Design:**
   - Export STEP file to Fusion 360 or SolidWorks
   - Design spar structure, servo mounts, battery tray
   - Create manufacturing drawings

3. **Manufacturing:**
   - Export DXF wing ribs for CNC cutting
   - 3D print brackets and fittings
   - Hand-build fuselage from exported cross-sections

4. **Flight Testing:**
   - Build physical aircraft
   - Validate mass properties (weigh actual aircraft)
   - Adjust CG with battery position
   - Fly and compare to OpenVSP predictions

---

## Resources

**OpenVSP Documentation:**
- Official Docs: http://openvsp.org/wiki/doku.php
- Tutorials: http://openvsp.org/wiki/doku.php?id=tutorials
- Forum: http://openvsp.org/forum/

**Airfoil Coordinates:**
- UIUC Database: https://m-selig.ae.illinois.edu/ads/coord_database.html
- Eppler E423: https://m-selig.ae.illinois.edu/ads/coord/e423.dat
- Selig S1223: https://m-selig.ae.illinois.edu/ads/coord/s1223.dat

**Companion Tools:**
- **XFLR5:** Free wing/airfoil analysis (www.xflr5.tech)
- **Fusion 360:** Free CAD for students/hobbyists (autodesk.com/fusion-360)
- **OpenFOAM:** Free CFD software (openfoam.org)

---

**Quick Reference Card**

```
OPENVSP INSTALLATION
Location: /Users/matthewoneil/OpenVSP-3.46.0-MacOS
Launch:   cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS && ./vsp

KEYBOARD SHORTCUTS
F           - Fit view to screen
Ctrl+S      - Save
Ctrl+Z      - Undo
Ctrl+Y      - Redo

MOUSE CONTROLS
Right-drag  - Rotate view
Scroll      - Zoom
Middle-drag - Pan (or Cmd+Right-drag)

WORKFLOW
1. Component → Add → Wing/Fuselage/Prop
2. Set parameters (Plan, Section, XForm tabs)
3. Analysis → Mass Properties (set masses, calc CG)
4. File → Export → STEP/DXF/STL

TARGET CG: 25-30% MAC (Mean Aerodynamic Chord)
Phase 1: CG at X ≈ 0.465 m
```

---

**Last Updated:** January 8, 2026  
**Next:** Create first OpenVSP model following this tutorial
