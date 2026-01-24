# GMSH UAV Model Generation Workflow

**Status:** ✅ Working  
**Last Updated:** January 8, 2026

---

## Overview

This document describes the GMSH-based UAV modeling workflow implemented for the MegaDrone project. GMSH is used to generate parametric 3D geometry of fixed-wing UAVs, which can then be exported for:

- **OpenVSP analysis** (aerodynamics, mass properties)
- **3D printing** (rapid prototyping)
- **CFD meshing** (aerodynamic simulation)
- **CAD import** (detailed design)

---

## Why GMSH Instead of OpenVSP API?

### Decision Rationale

1. **Immediate availability:** GMSH Python API installs via pip (`pip install gmsh`)
2. **No compilation required:** OpenVSP Python API requires building from source (1-2 day effort)
3. **Parametric scripting:** Full Python control of geometry
4. **Export flexibility:** STL, VTK, MSH formats work out-of-the-box
5. **Mesh generation:** Built-in meshing for CFD preprocessing

### Trade-offs

| Feature | GMSH | OpenVSP API |
|---------|------|-------------|
| Installation | `pip install gmsh` | Build from source |
| Learning curve | Medium | Medium-High |
| Airfoil handling | Manual (NACA equations) | Built-in library |
| CAD export | STL (reliable), STEP (requires OCC kernel) | STEP, IGES (native) |
| Analysis tools | Meshing only | Aero analysis, mass props |
| Best for | Geometry + meshing | Conceptual aircraft design |

---

## Generated UAV Model

### Phase 1 Specifications

**Design:** Fixed-wing trainer drone  
**Configuration:** High wing, pusher propeller, H-tail

| Parameter | Value |
|-----------|-------|
| Wingspan | 2.2 m (7.2 ft) |
| Wing Area | 0.55 m² (5.9 ft²) |
| Fuselage Length | 1.3 m (4.3 ft) |
| Root Chord | 0.279 m |
| Tip Chord | 0.221 m (taper ratio 0.79) |
| Aspect Ratio | 8.80 |
| Airfoil | NACA 2412 (approximates E423) |
| Dihedral | 2° |
| Wing Twist | -2° washout at tip |
| Tail Span | 0.7 m |
| V-Tail Height | 0.25 m |

### Model Features

✅ **Fuselage**
- 5 streamlined cross-sections
- Nose: 40mm radius
- Max diameter: 150mm (payload bay)
- Tail boom: 25mm radius

✅ **Main Wing**
- NACA 2412 airfoil sections
- 5 spanwise sections per side (10 total)
- Taper, dihedral, and twist included
- Proper aerodynamic washout

✅ **Horizontal Tail**
- NACA 0012 symmetric airfoil
- 3 sections per side
- Positioned at rear of fuselage

✅ **Vertical Tail**
- NACA 0012 airfoil (rotated 90°)
- Single fin (no mirror)
- Mounted on fuselage centerline

---

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/matthewoneil/Desktop/Datawerkes/MegaDrone
source venv/bin/activate
pip install -r requirements.txt
```

This installs:
- `gmsh>=4.13.0` - Geometry and meshing
- `numpy>=1.24.0` - Numerical computations
- Other analysis tools (pandas, matplotlib, pyyaml)

### 2. Generate UAV Model

```bash
python scripts/gmsh_uav_simple.py
```

**Output:**
```
designs/
├── Phase1_UAV_GMSH.stl          # 3D printable / OpenVSP import
├── Phase1_UAV_GMSH.msh          # GMSH native mesh
├── Phase1_UAV_GMSH.vtk          # ParaView visualization
└── Phase1_UAV_GMSH.geo_unrolled # GMSH script
```

### 3. Visualize Model

**Option A: GMSH GUI**
```bash
gmsh designs/Phase1_UAV_GMSH.stl
```

**Option B: ParaView (advanced)**
```bash
open designs/Phase1_UAV_GMSH.vtk
```

**Option C: Preview (MacOS)**
```bash
open designs/Phase1_UAV_GMSH.stl
```

---

## Importing into OpenVSP

### Method 1: Direct STL Import (Recommended)

1. Launch OpenVSP:
   ```bash
   cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS
   ./vsp
   ```

2. Import STL:
   ```
   File → Import → Import File
   Select: designs/Phase1_UAV_GMSH.stl
   Format: STL
   ```

3. **Note:** STL import creates a mesh body (not parametric)
   - You can view and visualize
   - Mass properties analysis works
   - Cannot modify airfoils parametrically
   - Export to other formats (STEP, IGES) from OpenVSP

### Method 2: Convert STL to STEP (Advanced)

Use FreeCAD or Blender to convert:

**FreeCAD (Recommended):**
```python
# FreeCAD Python console
import Mesh
import Part

mesh = Mesh.Mesh("Phase1_UAV_GMSH.stl")
shape = Part.Shape()
shape.makeShapeFromMesh(mesh.Topology, 0.1)
solid = Part.makeSolid(shape)
Part.export([solid], "Phase1_UAV_GMSH.step")
```

**Blender (Alternative):**
1. Import STL: File → Import → STL
2. Export STEP: File → Export → STEP (.step)
3. Requires CAD add-on

---

## 3D Printing Workflow

The generated STL is ready for 3D printing!

### Print Settings (Recommended)

| Setting | Value |
|---------|-------|
| Scale | 1:10 (220mm wingspan model) |
| Material | PLA or PETG |
| Infill | 15-20% (display model) |
| Wall thickness | 1.2mm (3 perimeters) |
| Layer height | 0.2mm |
| Supports | Yes (for wing underside) |

### Slicing Software

**PrusaSlicer / Cura:**
```bash
# Open STL in slicer
open -a PrusaSlicer designs/Phase1_UAV_GMSH.stl
```

**Scale to 1:10:**
- X, Y, Z: 10% (220mm wingspan)

**Check dimensions:**
- Wingspan: ~220mm (fits on most printers)
- Length: ~130mm

---

## Customizing the Model

### Edit Design Parameters

Open `scripts/gmsh_uav_simple.py` and modify:

```python
# Design parameters (lines 25-30)
WINGSPAN = 2.2       # Change wingspan (meters)
WING_AREA = 0.55     # Change wing area (m²)
FUSELAGE_LENGTH = 1.3
MESH_SIZE = 0.05     # Mesh density (smaller = finer)
```

### Change Airfoil

Modify NACA code in `naca4_airfoil()`:

```python
# For symmetric airfoil (tail)
airfoil = naca4_airfoil("0012")  # NACA 0012

# For cambered airfoil (main wing)
airfoil = naca4_airfoil("2412")  # NACA 2412 (current)
airfoil = naca4_airfoil("4415")  # NACA 4415 (more camber)
```

### Adjust Wing Parameters

In `create_wing_surface()` function:

```python
taper = tip_chord / root_chord  # 0.79 (current)
dihedral = 2.0  # degrees (increase for more stability)
twist = -2.0 * eta  # washout (negative = nose down at tip)
```

### Re-generate Model

```bash
python scripts/gmsh_uav_simple.py
```

---

## Advanced: CFD Meshing

The GMSH model can be used for CFD analysis:

### 1. Generate Volume Mesh

Modify `gmsh_uav_simple.py`:

```python
# Change mesh generation (line ~320)
gmsh.model.mesh.generate(3)  # 3D volume mesh instead of 2D
```

### 2. Export for CFD Solvers

**OpenFOAM:**
```bash
# Convert MSH to OpenFOAM
gmshToFoam designs/Phase1_UAV_GMSH.msh
```

**SU2:**
```bash
# MSH format is compatible
# Use directly in SU2 config
MESH_FILENAME= Phase1_UAV_GMSH.msh
```

---

## Troubleshooting

### Issue: "Module 'gmsh' not found"

**Solution:**
```bash
source venv/bin/activate
pip install gmsh
```

### Issue: STL looks wrong in OpenVSP

**Possible causes:**
1. **Units mismatch:** OpenVSP expects meters (GMSH uses meters by default ✓)
2. **Mesh too coarse:** Reduce `MESH_SIZE` in script (e.g., 0.02 instead of 0.05)
3. **Surface normals flipped:** Check in GMSH GUI first

**Fix mesh density:**
```python
MESH_SIZE = 0.02  # Finer mesh
MESH_SIZE_FINE = 0.01  # For critical areas (wings)
```

### Issue: Cannot export STEP from GMSH

**Explanation:** STEP export requires OpenCASCADE kernel (OCC)

**Workaround:**
1. Export STL from GMSH ✓ (works)
2. Import STL to FreeCAD
3. Convert to solid in FreeCAD
4. Export STEP from FreeCAD
5. Import STEP to OpenVSP

**Alternative:** Use STL directly in OpenVSP (works for most analysis)

---

## File Formats Explained

| Format | Extension | Use Case | Compatibility |
|--------|-----------|----------|---------------|
| **STL** | `.stl` | 3D printing, visualization | Universal (all CAD tools) |
| **STEP** | `.step` | CAD interchange | Best for OpenVSP (parametric) |
| **IGES** | `.iges` | Legacy CAD | OpenVSP, older CAD tools |
| **MSH** | `.msh` | GMSH native mesh | GMSH, CFD solvers |
| **VTK** | `.vtk` | Visualization | ParaView, VisIt |
| **GEO** | `.geo` | GMSH script | GMSH (editable script) |

### What to Use When

- **OpenVSP import:** STL (works immediately) or STEP (better, requires conversion)
- **3D printing:** STL
- **CFD analysis:** MSH or VTK
- **CAD editing:** STEP or IGES
- **Visualization:** VTK (ParaView) or STL (most viewers)

---

## Comparison: GMSH vs OpenVSP Workflow

### GMSH Workflow (Current)

```
Python Script (gmsh_uav_simple.py)
  ↓
GMSH Geometry (parametric)
  ↓
Export Formats:
  • STL → OpenVSP / 3D Printer
  • MSH → CFD Solver
  • VTK → ParaView
  • (STEP via FreeCAD)
```

**Pros:**
- ✅ Works immediately (pip install)
- ✅ Full Python scripting control
- ✅ Built-in meshing for CFD
- ✅ Multiple export formats

**Cons:**
- ❌ Manual airfoil equations
- ❌ STEP export requires OCC kernel
- ❌ No built-in aero analysis

### OpenVSP Workflow (Alternative)

```
OpenVSP GUI
  ↓
VSP3 Model (parametric)
  ↓
Built-in Analysis:
  • CompGeom (wetted area, volumes)
  • Parasite drag estimation
  • Mass properties
  ↓
Export: STEP, IGES, STL, DXF
```

**Pros:**
- ✅ Airfoil library built-in
- ✅ Native STEP/IGES export
- ✅ Aerodynamic analysis tools
- ✅ Designed for aircraft

**Cons:**
- ❌ GUI-based (or requires building API)
- ❌ Python API requires compilation
- ❌ Less flexible scripting

### Hybrid Approach (Recommended)

1. **Generate in GMSH** (parametric scripting)
2. **Import to OpenVSP** (analysis and refinement)
3. **Export from OpenVSP** (final STEP/IGES for manufacturing)

---

## Next Steps

### Immediate (Week 1)

- [x] Generate UAV model with GMSH ✅
- [x] Export STL for visualization ✅
- [ ] **Import STL into OpenVSP and verify**
- [ ] **3D print a 1:10 scale model** (optional)

### Short-term (Month 1)

- [ ] Create airfoil database (E423 coordinates)
- [ ] Add propeller geometry
- [ ] Integrate mass properties calculation
- [ ] Create parametric configuration files (YAML)

### Long-term (Month 2-3)

- [ ] Generate Phase 2 ISR platform model
- [ ] Create CFD-ready volume mesh
- [ ] Integrate with ArduPlane SITL for simulation
- [ ] Build manufacturing templates (DXF wing ribs)

---

## Resources

### GMSH Documentation

- **Official docs:** https://gmsh.info/doc/texinfo/gmsh.html
- **Python API:** https://gitlab.onelab.info/gmsh/gmsh/blob/master/api/gmsh.py
- **Tutorials:** https://gmsh.info/doc/texinfo/gmsh.html#Tutorial

### Airfoil Data

- **UIUC Database:** https://m-selig.ae.illinois.edu/ads/coord_database.html
- **Download E423:** http://airfoiltools.com/airfoil/details?airfoil=e423-il

### Related Tools

- **FreeCAD:** https://www.freecad.org/ (STL to STEP conversion)
- **ParaView:** https://www.paraview.org/ (VTK visualization)
- **OpenVSP:** https://openvsp.org/ (aerodynamic analysis)

---

## Script Overview

### `gmsh_uav_simple.py`

**Main Functions:**

1. `naca4_airfoil(code, n_points, chord)`
   - Generates NACA 4-digit airfoil coordinates
   - Returns (x, y) arrays scaled by chord

2. `create_wing_surface(x_offset, z_offset, wingspan, root_chord, tip_chord, n_sections)`
   - Creates wing geometry with taper, dihedral, twist
   - Generates both left and right wings

3. `create_fuselage(length, max_radius)`
   - Streamlined fuselage with 5 cross-sections
   - Nose to tail boom transition

4. `create_tail(x_offset, z_offset, span, root_chord, tip_chord, is_vertical)`
   - Creates horizontal or vertical stabilizer
   - NACA 0012 symmetric airfoil

5. `main()`
   - Orchestrates model generation
   - Exports STL, MSH, VTK, GEO formats

---

## Contact

**Project:** MegaDrone - Fixed-Wing UAV Development  
**Owner:** Matthew O'Neil  
**Location:** Florida  
**Purpose:** ISR platform for maritime operations

**Questions or Issues:**
- Check `README.md` for project overview
- See `DRONE_DEVELOPMENT_PLAN.md` for design details
- Review `OPENVSP_QUICK_START.md` for OpenVSP GUI workflow

---

**Last Updated:** January 8, 2026  
**Status:** GMSH workflow operational ✅  
**Next Milestone:** Import to OpenVSP and validate geometry
