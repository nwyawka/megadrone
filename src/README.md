# MegaDrone Source Code

This directory contains Python scripts for UAV design, analysis, and utilities.

## Directory Structure

```
src/
├── README.md               # This file
├── README_PYTHON_API.md    # OpenVSP Python API documentation
├── analysis/               # Analysis scripts
├── design/                 # Design generation scripts
├── mesh/                   # Mesh generation scripts
└── tools/                  # Utility scripts
```

---

## Setup

```bash
# Activate virtual environment
cd /Users/matthewoneil/Desktop/Datawerkes/MegaDrone
source venv/bin/activate

# Verify dependencies
pip list | grep -E "gmsh|numpy|aerosandbox"
```

---

## Scripts by Category

### Analysis (`analysis/`)

| Script | Purpose |
|--------|---------|
| `aero_analysis.py` | Aerodynamic analysis using AeroSandbox |
| `aerosandbox_model.py` | AeroSandbox aircraft model |
| `aerosandbox_model_v2.py` | Updated AeroSandbox model |
| `airfoil_optimization.py` | Airfoil selection and optimization |
| `analyze_uav.py` | General UAV analysis |
| `cfd_validation.py` | CFD validation using SU2 |
| `propeller_design.py` | Propeller sizing and analysis |
| `structural_analysis.py` | Structural load analysis |

**Usage:**
```bash
python src/analysis/aero_analysis.py
python src/analysis/cfd_validation.py
```

---

### Design (`design/`)

| Script | Purpose |
|--------|---------|
| `phase1_openvsp_correct.py` | Generate Phase 1 UAV in OpenVSP |
| `phase1_openvsp_fixed.py` | Fixed version of Phase 1 generator |
| `phase1_fixedwing.py` | Phase 1 fixed-wing template |
| `drone_sizing.py` | Drone sizing calculations |
| `openvsp_setup.py` | OpenVSP environment setup |
| `test_xsec_params.py` | Cross-section parameter testing |

**Usage:**
```bash
python src/design/phase1_openvsp_correct.py
# Output: designs/phase1/Phase1_UAV_Correct.vsp3
```

---

### Mesh (`mesh/`)

| Script | Purpose |
|--------|---------|
| `gmsh_uav_generator.py` | Advanced GMSH UAV generator |
| `gmsh_uav_refined.py` | Refined mesh generation |
| `gmsh_uav_simple.py` | Simple GMSH UAV model |
| `gmsh_uav_fixed.py` | Fixed GMSH generator |
| `gmsh_uav_occ.py` | OpenCASCADE-based GMSH generator |

**Usage:**
```bash
python src/mesh/gmsh_uav_occ.py
# Output: designs/phase1/Phase1_UAV_OCC_HiRes.stl
```

---

### Tools (`tools/`)

| Script | Purpose |
|--------|---------|
| `bill_of_materials.py` | Generate BOM from specifications |
| `generate_pdf_report.py` | Generate PDF design report |
| `technical_drawings.py` | Generate technical drawings |

**Usage:**
```bash
python src/tools/bill_of_materials.py
python src/tools/generate_pdf_report.py
```

---

## Output Directories

| Directory | Contents |
|-----------|----------|
| `../designs/phase1/` | OpenVSP models, STEP, STL files |
| `../designs/exports/` | Images, PDFs, reports |
| `../cfd/` | CFD mesh and config files |

---

## Dependencies

```
gmsh>=4.13.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
aerosandbox>=4.0.0
scipy>=1.10.0
pyyaml>=6.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## API Documentation

See [README_PYTHON_API.md](README_PYTHON_API.md) for OpenVSP Python API details.

---

*Last Updated: January 2026*
