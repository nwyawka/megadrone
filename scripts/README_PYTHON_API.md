# OpenVSP Python API Setup Guide

## Important Notes About OpenVSP Python API

The OpenVSP Python API is **NOT installed by default** with the OpenVSP application. Based on the workshop presentation and OpenVSP documentation, here's how to use it:

### Option 1: Use OpenVSP GUI (Recommended for Now)

**Pros:**
- Works immediately with your installation
- Visual feedback while designing
- No compilation required
- Follow the tutorial in `OPENVSP_QUICK_START.md`

**This is the fastest way to get started!**

---

### Option 2: Build OpenVSP from Source (Advanced)

If you want to use the Python API, you need to build OpenVSP from source with Python bindings enabled.

#### Requirements

- CMake 3.12+
- C++ compiler (Xcode Command Line Tools on Mac)
- SWIG (Simplified Wrapper and Interface Generator)
- Python 3.8+

#### Build Steps (MacOS)

```bash
# Install prerequisites
brew install cmake swig

# Clone OpenVSP repository
cd ~/Downloads
git clone https://github.com/OpenVSP/OpenVSP.git
cd OpenVSP

# Create build directory
mkdir build
cd build

# Configure with Python bindings enabled
cmake .. \
  -DVSP_USE_SYSTEM_LIBXML2=true \
  -DVSP_USE_SYSTEM_FLTK=true \
  -DVSP_USE_SYSTEM_GLM=true \
  -DVSP_USE_SYSTEM_GLEW=true \
  -DVSP_USE_SYSTEM_CMINPACK=true \
  -DVSP_USE_SYSTEM_LIBIGES=true \
  -DVSP_USE_SYSTEM_STEPCODE=true \
  -DVSP_USE_SYSTEM_CPPTEST=true \
  -DVSP_USE_SYSTEM_FREEGLUT=true \
  -DPYTHON_BINDINGS=ON \
  -DPYTHON_EXECUTABLE=/usr/bin/python3

# Build (takes 30-60 minutes)
make -j4

# Install
sudo make install
```

#### After Building

The Python module will be installed in:
- `/usr/local/lib/python3.x/site-packages/openvsp.so`

Or you can copy it to your project:
```bash
cp /path/to/build/python/openvsp.so ~/Desktop/Datawerkes/MegaDrone/venv/lib/python3.12/site-packages/
```

---

### Option 3: VSPScript (Alternative Scripting)

OpenVSP includes **VSPScript** (AngelScript), which is a built-in scripting language that works without compilation.

**Access via GUI:**
- File → Run Script
- Scripts are `.vspscript` files

**Example VSPScript:**
```angelscript
void main()
{
    // Create wing
    string wing_id = AddGeom("WING");
    SetGeomName(wing_id, "Main_Wing");
    
    // Set parameters
    SetParmVal(wing_id, "TotalSpan", "WingGeom", 2.2);
    SetParmVal(wing_id, "Root_Chord", "XSec_0", 0.28);
    
    Update();
    
    // Save
    WriteVSPFile("Phase1_Drone.vsp3");
}
```

---

## Using the Python Scripts in This Repository

The Python scripts (`phase1_fixedwing.py`, etc.) are **templates and reference examples**.

### Current Status

❌ **Will not run** with standard OpenVSP installation  
✅ **Useful as reference** for API structure  
✅ **Can be adapted** once you build from source

### What To Do

**For now:**
1. Use the OpenVSP GUI (follow `OPENVSP_QUICK_START.md`)
2. Save your design as `.vsp3` file
3. Export geometry for manufacturing

**Later (if you build from source):**
1. Build OpenVSP with Python bindings
2. Test with `python scripts/openvsp_setup.py`
3. Run design scripts: `python scripts/phase1_fixedwing.py`
4. Automate batch operations

---

## OpenVSP API Documentation

**Online API Reference:**
- https://openvsp.org/api_docs/latest/

**Key Modules:**
- `openvsp` - Main API module
- Geometry creation: `AddGeom()`, `SetGeomName()`
- Parameters: `SetParmVal()`, `GetParmVal()`
- Analysis: `CompGeom()`, `MassProperties()`
- Export: `WriteVSPFile()`, `ExportFile()`

**Workshop Presentation:**
- https://openvsp.org/wiki/doku.php?id=workshop20

---

## Alternative: Parametric Design with GUI + Scripts

You can use a hybrid approach:

1. **Design in GUI** - Create basic geometry interactively
2. **Save template** - Save as `.vsp3` file
3. **Script variations** - Use VSPScript to modify parameters
4. **Batch process** - Generate multiple configurations

**Example workflow:**
```bash
# Create base design in GUI
# Save as: base_design.vsp3

# Create VSPScript to modify:
# - Wingspan (2.0m, 2.2m, 2.4m)
# - Wing area (0.5m², 0.55m², 0.6m²)

# Run script from GUI: File → Run Script
# Or from terminal:
vspscript -script generate_variants.vspscript
```

---

## Recommendation

**Phase 1 (Now):**
- ✅ Use OpenVSP GUI
- ✅ Follow `OPENVSP_QUICK_START.md` tutorial
- ✅ Manual design and iteration
- ✅ Export for CAD/manufacturing

**Phase 2 (Later, Optional):**
- Build OpenVSP from source (if you need automation)
- Enable Python bindings
- Run Python scripts for batch designs
- Integrate with optimization workflows

---

## Summary

| Method | Complexity | Time to Start | Automation | Recommended? |
|--------|-----------|---------------|------------|--------------|
| **GUI** | Low | Immediate | No | ✅ **Yes** (start here) |
| **VSPScript** | Medium | Immediate | Yes | ⚠️ Maybe (if need batching) |
| **Python API** | High | 1-2 days | Yes | ❌ Not yet (build from source) |

**Bottom Line:** Use the GUI first. The Python scripts in this repo are reference examples for future use if you build from source.

---

**Last Updated:** January 8, 2026  
**Your OpenVSP Installation:** `/Users/matthewoneil/OpenVSP-3.46.0-MacOS`  
**Status:** GUI workflow ready, Python API requires building from source
