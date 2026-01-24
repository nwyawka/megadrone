# MegaDrone Quick Reference Card

**Last Updated:** January 8, 2026

---

## 🚀 Generate UAV Model (PRIMARY WORKFLOW)

```bash
# 1. Activate environment
cd /Users/matthewoneil/Desktop/Datawerkes/MegaDrone
source venv/bin/activate

# 2. Generate model
python scripts/gmsh_uav_simple.py

# 3. Output created:
# → designs/Phase1_UAV_GMSH.stl  (import to OpenVSP or 3D print)
```

---

## 📊 View Model

```bash
# GMSH GUI
gmsh designs/Phase1_UAV_GMSH.stl

# MacOS Preview
open designs/Phase1_UAV_GMSH.stl

# OpenVSP
cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS && ./vsp
# Then: File → Import → Import File → Select STL
```

---

## 🛠️ Customize Design

Edit `scripts/gmsh_uav_simple.py`:

```python
# Lines 25-30: Design Parameters
WINGSPAN = 2.2       # Change wingspan (meters)
WING_AREA = 0.55     # Change wing area (m²)
FUSELAGE_LENGTH = 1.3
MESH_SIZE = 0.05     # Mesh density (smaller = finer)

# Line 60+: Airfoil selection
airfoil = naca4_airfoil("2412")  # NACA code
# Options: "0012" (symmetric), "4415" (high lift), "2412" (current)
```

Re-run:
```bash
python scripts/gmsh_uav_simple.py
```

---

## 📐 Current Model Specs

| Parameter | Value |
|-----------|-------|
| Wingspan | 2.2 m (7.2 ft) |
| Wing Area | 0.55 m² |
| Aspect Ratio | 8.8 |
| Root Chord | 0.279 m |
| Tip Chord | 0.221 m |
| Taper Ratio | 0.79 |
| Fuselage Length | 1.3 m |
| Airfoil | NACA 2412 |
| Dihedral | 2° |
| Washout | -2° at tip |

---

## 📁 File Guide

| File | Purpose |
|------|---------|
| `README.md` | Project overview, quick start |
| `GMSH_WORKFLOW.md` | Complete GMSH guide |
| `GMSH_IMPLEMENTATION_SUMMARY.md` | Technical details |
| `OPENVSP_QUICK_START.md` | OpenVSP GUI tutorial |
| `DRONE_DEVELOPMENT_PLAN.md` | Full design specifications |

---

## 🔧 Troubleshooting

**Module 'gmsh' not found:**
```bash
source venv/bin/activate
pip install gmsh
```

**STL too coarse:**
```python
# Edit scripts/gmsh_uav_simple.py
MESH_SIZE = 0.02  # Change from 0.05
```

**Wrong units in OpenVSP:**
- Both GMSH and OpenVSP use meters ✓
- Expected wingspan: 2.2m (not mm or km)

---

## 🎯 Next Steps

1. ⏳ Import `Phase1_UAV_GMSH.stl` into OpenVSP
2. ⏳ Run CompGeom analysis in OpenVSP
3. ⏳ Validate dimensions and geometry
4. ⏳ Optional: 3D print 1:10 scale (220mm wingspan)

---

## 📚 Key Commands

```bash
# Setup
cd /Users/matthewoneil/Desktop/Datawerkes/MegaDrone
source venv/bin/activate

# Generate model
python scripts/gmsh_uav_simple.py

# View in GMSH
gmsh designs/Phase1_UAV_GMSH.stl

# Launch OpenVSP
cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS && ./vsp

# List files
ls -lh designs/
```

---

## 📞 Resources

- **GMSH docs:** https://gmsh.info/doc/texinfo/gmsh.html
- **OpenVSP:** https://openvsp.org
- **Airfoil database:** https://m-selig.ae.illinois.edu/ads/coord_database.html
- **ArduPlane:** https://ardupilot.org/plane/

---

**Status:** ✅ GMSH workflow operational  
**Primary Script:** `scripts/gmsh_uav_simple.py`  
**Primary Output:** `designs/Phase1_UAV_GMSH.stl`
