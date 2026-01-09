# CFD Validation Guide for MegaDrone

## Overview

This document outlines approaches for detailed CFD (Computational Fluid Dynamics) validation of the MegaDrone aerodynamic design. The goal is to verify and refine the VLM (Vortex Lattice Method) predictions from AeroSandbox.

---

## Why CFD Validation?

VLM provides good preliminary aerodynamic estimates but has limitations:
- **No viscous effects** - Doesn't capture boundary layer separation
- **Thin airfoil assumption** - Geometry approximated as camber line
- **No compressibility** - Not an issue at our Mach numbers
- **No flow separation** - Overestimates performance near stall

CFD provides:
- **Viscous flow effects** - Accurate drag predictions
- **Flow visualization** - Identify separation, vortices
- **Pressure distributions** - Structural loading inputs
- **Validation** - Confirm design performance

---

## Recommended Approach: Tiered Validation

### Tier 1: XFLR5/XFOIL (Airfoil Level)
**Complexity: Low | Cost: Free | Time: Hours**

Validate 2D airfoil performance before full 3D:

```
1. Export optimized airfoil from designs/optimized_airfoil.dat
2. Import into XFOIL or XFLR5
3. Run viscous analysis at cruise Re = 250,000
4. Compare CL, CD, CM with NeuralFoil predictions
5. Check for separation/transition behavior
```

**Installation:**
```bash
# XFOIL (command line)
brew install xfoil  # macOS

# XFLR5 (GUI - recommended)
# Download from: http://www.xflr5.tech/xflr5.htm
```

**Expected Results:**
- CL accuracy: ±5%
- CD accuracy: ±10-15%
- Stall prediction: ±2°

---

### Tier 2: SU2 (Open Source 3D CFD)
**Complexity: Medium | Cost: Free | Time: Days**

Stanford University's SU2 is excellent for aerodynamic validation:

**Pros:**
- Open source, actively maintained
- Optimized for aerodynamics
- Good documentation
- Supports RANS turbulence models
- Runs on Mac/Linux/Windows

**Installation:**
```bash
# macOS with Homebrew
brew install su2

# Or build from source
git clone https://github.com/su2code/SU2.git
cd SU2
./meson.py build
./ninja -C build install
```

**Workflow:**
1. Export aircraft geometry to STL from OpenVSP
2. Generate mesh using Pointwise, Gmsh, or SU2's built-in tools
3. Set up RANS simulation (SA or k-ω SST turbulence model)
4. Run at cruise and loiter conditions
5. Post-process with ParaView

**Configuration File Example (cruise):**
```
% SU2 Configuration for MegaDrone Cruise
SOLVER= RANS
MATH_PROBLEM= DIRECT
RESTART_SOL= NO

% Flow conditions (50 knots at 150m)
MACH_NUMBER= 0.075
AOA= 3.0
SIDESLIP_ANGLE= 0.0
REYNOLDS_NUMBER= 250000
REYNOLDS_LENGTH= 0.142

% Turbulence model
KIND_TURB_MODEL= SA

% Mesh
MESH_FILENAME= megadrone_mesh.su2
MESH_FORMAT= SU2

% Reference values
REF_ORIGIN_MOMENT_X= 0.035
REF_ORIGIN_MOMENT_Y= 0.0
REF_ORIGIN_MOMENT_Z= 0.0
REF_LENGTH= 0.142
REF_AREA= 0.241

% Convergence
CONV_RESIDUAL_MINVAL= -10
CONV_STARTITER= 10

% Output
OUTPUT_FILES= (RESTART, PARAVIEW)
```

---

### Tier 3: OpenFOAM (Advanced Open Source)
**Complexity: High | Cost: Free | Time: Week+**

Most powerful open-source option:

**Pros:**
- Extremely flexible
- Large community
- All turbulence models available
- Parallel computing support

**Cons:**
- Steep learning curve
- Command-line focused
- Complex case setup

**Installation:**
```bash
# macOS (via Docker recommended)
docker pull openfoam/openfoam10-paraview510

# Or native with Homebrew
brew install openfoam
```

**Typical Workflow:**
1. Generate mesh (blockMesh, snappyHexMesh, or external)
2. Set boundary conditions
3. Choose solver (simpleFoam for steady RANS)
4. Run simulation
5. Post-process with ParaView

---

### Tier 4: Cloud CFD (SimScale)
**Complexity: Low | Cost: Free tier / $$ | Time: Days**

Browser-based CFD with free community tier:

**Pros:**
- No installation required
- Built-in meshing
- Pre-configured templates
- Easy visualization

**Cons:**
- Limited free compute hours
- Requires internet
- Less control than local tools

**Workflow:**
1. Upload STL geometry
2. Use automated mesher
3. Select "Incompressible" → "Steady-state"
4. Set velocity inlet, pressure outlet
5. Run and visualize

**URL:** https://www.simscale.com

---

## Mesh Generation

Critical for CFD accuracy. Options:

### Gmsh (Free, Open Source)
```bash
brew install gmsh
```
- Good for 2D and simple 3D
- Scripting capability
- Export to OpenFOAM, SU2

### SnappyHexMesh (OpenFOAM)
- Excellent for complex geometries
- Automatic refinement near surfaces
- Part of OpenFOAM

### Pointwise (Commercial)
- Industry standard
- Excellent quality meshes
- Expensive ($$$)

### ANSA/ICEM (Commercial)
- Used by aerospace companies
- Very expensive

---

## Recommended Validation Matrix

| Condition | Method | Grid Points | Expected Time |
|-----------|--------|-------------|---------------|
| Airfoil @ Re=250k | XFOIL | N/A (panel) | 1 minute |
| 2D airfoil RANS | SU2 | 50,000 | 10 minutes |
| Full aircraft VLM | AeroSandbox | N/A | 1 second |
| Full aircraft RANS | SU2 | 2-5 million | 2-4 hours |
| Detailed RANS | OpenFOAM | 10+ million | 12-24 hours |

---

## Validation Targets

Compare CFD results against AeroSandbox predictions:

| Parameter | VLM Value | CFD Target Accuracy |
|-----------|-----------|---------------------|
| CL (cruise) | 0.53 | ±5% |
| CD (total) | 0.026 | ±10% |
| L/D | 21.5 | ±10% |
| CM | -0.02 | ±20% |
| Stall α | ~12° | ±2° |

---

## Quick Start: XFLR5 Validation

Simplest path to validation:

### 1. Install XFLR5
Download from http://www.xflr5.tech/xflr5.htm

### 2. Import Airfoil
- File → Direct Foil Design → Import
- Load `designs/optimized_airfoil.dat`

### 3. Set Analysis Parameters
- Analysis → Define Analysis
- Type 1: Fixed speed
- Re = 250,000
- Mach = 0.075
- Ncrit = 9 (typical)

### 4. Run Batch Analysis
- α = -4° to 14° in 0.5° steps
- Export polar data

### 5. Compare Results
```python
# Compare XFLR5 export with NeuralFoil
import pandas as pd
import matplotlib.pyplot as plt

xflr5 = pd.read_csv('xflr5_polar.csv')
# Plot comparison...
```

---

## Full 3D CFD Workflow (SU2)

### Step 1: Export Geometry

From OpenVSP:
```
File → Export → STL
Set: Compute from Tessellation = True
```

### Step 2: Generate Mesh

Using Gmsh:
```bash
gmsh -3 megadrone.geo -o megadrone.msh
```

Or convert STL to SU2 mesh:
```python
# Use SU2's mesh tools or PyMesh
```

### Step 3: Configure SU2

Create `cruise.cfg` with:
- RANS solver
- SA turbulence model
- Cruise conditions
- Convergence criteria

### Step 4: Run Simulation
```bash
SU2_CFD cruise.cfg
```

### Step 5: Post-Process
```bash
paraview surface_flow.vtu
```

---

## Python Script for Validation

```python
#!/usr/bin/env python3
"""
CFD Validation Helper Script
Compares AeroSandbox results with CFD data
"""

import numpy as np
import matplotlib.pyplot as plt

# AeroSandbox results (from aero_analysis.py)
asb_results = {
    'alpha': [0, 2, 4, 6, 8, 10],
    'CL': [0.15, 0.35, 0.55, 0.75, 0.95, 1.10],
    'CD': [0.020, 0.021, 0.024, 0.028, 0.035, 0.045],
}

# Load CFD results (example format)
# cfd_results = np.loadtxt('cfd_polar.dat')

def compare_polars(asb, cfd):
    """Compare AeroSandbox with CFD results."""

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # CL vs alpha
    ax = axes[0]
    ax.plot(asb['alpha'], asb['CL'], 'b-o', label='AeroSandbox')
    ax.plot(cfd['alpha'], cfd['CL'], 'r-s', label='CFD')
    ax.set_xlabel('Alpha (deg)')
    ax.set_ylabel('CL')
    ax.legend()
    ax.grid(True)

    # Drag polar
    ax = axes[1]
    ax.plot(asb['CD'], asb['CL'], 'b-o', label='AeroSandbox')
    ax.plot(cfd['CD'], cfd['CL'], 'r-s', label='CFD')
    ax.set_xlabel('CD')
    ax.set_ylabel('CL')
    ax.legend()
    ax.grid(True)

    # L/D comparison
    ax = axes[2]
    asb_ld = np.array(asb['CL']) / np.array(asb['CD'])
    cfd_ld = np.array(cfd['CL']) / np.array(cfd['CD'])
    ax.plot(asb['alpha'], asb_ld, 'b-o', label='AeroSandbox')
    ax.plot(cfd['alpha'], cfd_ld, 'r-s', label='CFD')
    ax.set_xlabel('Alpha (deg)')
    ax.set_ylabel('L/D')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.savefig('cfd_validation.png', dpi=150)
    plt.show()

    # Calculate errors
    print("Validation Summary:")
    print(f"  CL RMSE: {np.sqrt(np.mean((np.array(asb['CL']) - np.array(cfd['CL']))**2)):.4f}")
    print(f"  CD RMSE: {np.sqrt(np.mean((np.array(asb['CD']) - np.array(cfd['CD']))**2)):.5f}")

if __name__ == "__main__":
    # Run when CFD data is available
    pass
```

---

## Recommendations

### For This Project (Small UAV)

1. **Start with XFLR5** - Quick airfoil validation
2. **Use SU2 for 3D** - Good balance of capability vs. complexity
3. **Skip OpenFOAM** - Overkill for this scale unless learning CFD

### Estimated Effort

| Task | Time |
|------|------|
| XFLR5 airfoil validation | 2-4 hours |
| SU2 installation & setup | 4-8 hours |
| Mesh generation | 4-8 hours |
| Full aircraft CFD run | 4-12 hours |
| Post-processing | 2-4 hours |
| **Total** | **16-36 hours** |

### When to Skip CFD

CFD may not be necessary if:
- Prototype is being built quickly
- Design is conventional (well within empirical data)
- Budget/time is limited
- Flight testing will happen soon anyway

The VLM results from AeroSandbox are typically within 10-15% for well-designed conventional aircraft at low speeds.

---

## References

- [SU2 Documentation](https://su2code.github.io/)
- [OpenFOAM User Guide](https://www.openfoam.com/documentation/user-guide)
- [XFLR5 Guidelines](http://www.xflr5.tech/docs/xflr5_guidelines.pdf)
- [SimScale Tutorials](https://www.simscale.com/docs/)
- [NASA Turbulence Modeling Resource](https://turbmodels.larc.nasa.gov/)

---

*Last Updated: January 8, 2026*
