# MegaDrone Design Files

This directory contains generated design files and exports.

## Directory Structure

```
designs/
├── README.md           # This file
├── phase1/             # Phase 1 UAV design files
└── exports/            # Exported images and reports
```

---

## Phase 1 Files (`phase1/`)

### OpenVSP Models

| File | Description |
|------|-------------|
| `Phase1_UAV_Correct.vsp3` | Primary OpenVSP model |
| `Phase1_FixedWing_Trainer.vsp3` | Training variant |

### CAD Exports

| File | Format | Use |
|------|--------|-----|
| `Phase1_UAV_Correct.step` | STEP | CAD import (Fusion 360, SolidWorks) |
| `Phase1_UAV_Correct.stl` | STL | 3D printing, visualization |
| `Phase1_UAV_Correct.iges` | IGES | Legacy CAD systems |

### Mesh Files

| File | Format | Use |
|------|--------|-----|
| `Phase1_UAV_Fixed.msh` | GMSH | CFD meshing |
| `Phase1_UAV_OCC_HiRes.msh` | GMSH | High-resolution mesh |
| `Phase1_UAV_Fixed.vtk` | VTK | ParaView visualization |

### Analysis Files

| File | Description |
|------|-------------|
| `Phase1_UAV_Correct_CompGeom.csv` | Component geometry |
| `Phase1_UAV_Correct_MassProps.txt` | Mass properties |
| `Phase1_UAV_Correct_ParasiteBuildUp.csv` | Drag analysis |
| `Phase1_UAV_Correct_Slice.txt` | Wing section data |
| `optimized_airfoil.dat` | Optimized airfoil coordinates |
| `bill_of_materials.json` | Component list (JSON) |
| `bill_of_materials.csv` | Component list (CSV) |

---

## Exports (`exports/`)

### Images

| File | Description |
|------|-------------|
| `three_view_drawing.png` | 3-view technical drawing |
| `wing_detail.png` | Wing planform detail |
| `component_layout.png` | Component placement |
| `aerosandbox_model.png` | AeroSandbox visualization |
| `airfoil_comparison.png` | Airfoil analysis |
| `propeller_performance.png` | Propeller analysis |
| `structural_analysis.png` | Structural loads |
| `cfd_convergence.png` | CFD convergence plot |

### Reports

| File | Description |
|------|-------------|
| `MegaDrone_Design_Report.pdf` | Complete design report |

---

## Generating Files

### OpenVSP Model

```bash
cd /Users/matthewoneil/Desktop/Datawerkes/MegaDrone
source venv/bin/activate
python src/design/phase1_openvsp_correct.py
```

### GMSH Mesh

```bash
python src/mesh/gmsh_uav_occ.py
```

### Analysis Images

```bash
python src/analysis/aero_analysis.py
python src/tools/technical_drawings.py
```

### PDF Report

```bash
python src/tools/generate_pdf_report.py
```

---

## Viewing Files

### OpenVSP Models

```bash
cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS
./vsp
# File → Open → designs/phase1/Phase1_UAV_Correct.vsp3
```

### STL/STEP Files

```bash
# macOS Quick Look
open designs/phase1/Phase1_UAV_Correct.stl

# GMSH viewer
gmsh designs/phase1/Phase1_UAV_Correct.stl
```

### VTK Files

```bash
# ParaView
paraview designs/phase1/Phase1_UAV_Fixed.vtk
```

---

*Last Updated: January 2026*
