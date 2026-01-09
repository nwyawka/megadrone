#!/usr/bin/env python3
"""
Phase 1 Fixed-Wing Drone Design Script - FIXED VERSION
Creates OpenVSP model using proper API calls for version 3.46

This version uses correct parameter names and error checking.

Author: MegaDrone Project
Date: January 8, 2026
"""

import sys
import os

try:
    import openvsp as vsp
    print(f"✓ OpenVSP {vsp.GetVSPVersion()} loaded successfully\n")
except ImportError as e:
    print(f"✗ Failed to import OpenVSP: {e}")
    print("Make sure you've installed the OpenVSP Python API")
    sys.exit(1)

import numpy as np

# Design parameters
DESIGN_NAME = "Phase1_UAV_Fixed"
WINGSPAN = 2.2  # meters
WING_AREA = 0.55  # square meters
FUSELAGE_LENGTH = 1.3  # meters
TAIL_SPAN = 0.7  # meters

def clear_model():
    """Clear any existing geometry"""
    vsp.ClearVSPModel()
    vsp.Update()
    print("✓ Cleared existing model\n")

def create_main_wing():
    """Create main wing - simplified approach"""
    print("="*60)
    print("Creating Main Wing")
    print("="*60)
    
    # Add wing component
    wing_id = vsp.AddGeom("WING")
    vsp.SetGeomName(wing_id, "Main_Wing")
    
    # Calculate dimensions
    taper_ratio = 0.79
    root_chord = 2 * WING_AREA / (WINGSPAN * (1 + taper_ratio))
    tip_chord = root_chord * taper_ratio
    
    print(f"Root Chord: {root_chord:.3f} m")
    print(f"Tip Chord: {tip_chord:.3f} m")
    print(f"Taper Ratio: {taper_ratio}")
    
    # Set basic wing parameters using correct API
    vsp.SetParmVal(wing_id, "TotalSpan", "WingGeom", WINGSPAN)
    vsp.SetParmVal(wing_id, "TotalArea", "WingGeom", WING_AREA)
    vsp.SetParmVal(wing_id, "Taper", "XSec_1", taper_ratio)
    vsp.SetParmVal(wing_id, "Dihedral", "XSec_1", 2.0)  # 2 degrees
    
    # Set airfoil to NACA 4-series
    xsec_surf = vsp.GetXSecSurf(wing_id, 0)
    vsp.ChangeXSecShape(xsec_surf, 0, vsp.XS_FOUR_SERIES)
    vsp.ChangeXSecShape(xsec_surf, 1, vsp.XS_FOUR_SERIES)
    
    # Set NACA 2412 parameters
    vsp.SetParmVal(wing_id, "Camber", "XSecCurve_0", 0.02)
    vsp.SetParmVal(wing_id, "CamberLoc", "XSecCurve_0", 0.4)
    vsp.SetParmVal(wing_id, "ThickChord", "XSecCurve_0", 0.12)
    
    # Position wing (high-wing configuration)
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 0.4)
    vsp.SetParmVal(wing_id, "Z_Rel_Location", "XForm", 0.15)
    
    # Set incidence angle
    vsp.SetParmVal(wing_id, "X_Rel_Rotation", "XForm", 1.0)
    
    vsp.Update()
    print(f"✓ Main wing created: {WINGSPAN}m span, {WING_AREA}m² area\n")
    return wing_id

def create_fuselage():
    """Create streamlined fuselage"""
    print("="*60)
    print("Creating Fuselage")
    print("="*60)
    
    # Add fuselage component
    fuse_id = vsp.AddGeom("FUSELAGE")
    vsp.SetGeomName(fuse_id, "Fuselage")
    
    # Set length
    vsp.SetParmVal(fuse_id, "Length", "Design", FUSELAGE_LENGTH)
    
    # Get XSec surface to modify cross-sections
    xsec_surf = vsp.GetXSecSurf(fuse_id, 0)
    
    # Modify existing sections
    # Section 0 (nose)
    vsp.ChangeXSecShape(xsec_surf, 0, vsp.XS_CIRCLE)
    vsp.SetParmVal(fuse_id, "Circle_Diameter", "XSecCurve_0", 0.08)
    
    # Section 1 (mid)
    vsp.ChangeXSecShape(xsec_surf, 1, vsp.XS_CIRCLE)
    vsp.SetParmVal(fuse_id, "Circle_Diameter", "XSecCurve_1", 0.15)
    
    # Section 2 (tail)
    vsp.ChangeXSecShape(xsec_surf, 2, vsp.XS_CIRCLE)
    vsp.SetParmVal(fuse_id, "Circle_Diameter", "XSecCurve_2", 0.05)
    
    vsp.Update()
    print(f"✓ Fuselage created: {FUSELAGE_LENGTH}m length\n")
    return fuse_id

def create_horizontal_tail():
    """Create horizontal stabilizer"""
    print("="*60)
    print("Creating Horizontal Tail")
    print("="*60)
    
    # Add wing component for H-tail
    htail_id = vsp.AddGeom("WING")
    vsp.SetGeomName(htail_id, "Horizontal_Tail")
    
    # Set parameters
    vsp.SetParmVal(htail_id, "TotalSpan", "WingGeom", TAIL_SPAN)
    vsp.SetParmVal(htail_id, "Taper", "XSec_1", 0.7)
    
    # Symmetric airfoil (NACA 0012)
    xsec_surf = vsp.GetXSecSurf(htail_id, 0)
    vsp.ChangeXSecShape(xsec_surf, 0, vsp.XS_FOUR_SERIES)
    vsp.ChangeXSecShape(xsec_surf, 1, vsp.XS_FOUR_SERIES)
    
    vsp.SetParmVal(htail_id, "Camber", "XSecCurve_0", 0.0)  # Symmetric
    vsp.SetParmVal(htail_id, "ThickChord", "XSecCurve_0", 0.12)
    
    # Position at rear of fuselage
    vsp.SetParmVal(htail_id, "X_Rel_Location", "XForm", 1.15)
    vsp.SetParmVal(htail_id, "Z_Rel_Location", "XForm", 0.05)
    
    vsp.Update()
    print(f"✓ Horizontal tail created: {TAIL_SPAN}m span\n")
    return htail_id

def create_vertical_tail():
    """Create vertical stabilizer"""
    print("="*60)
    print("Creating Vertical Tail")
    print("="*60)
    
    # Add wing component (will rotate to vertical)
    vtail_id = vsp.AddGeom("WING")
    vsp.SetGeomName(vtail_id, "Vertical_Tail")
    
    # Set parameters
    height = 0.25
    vsp.SetParmVal(vtail_id, "TotalSpan", "WingGeom", height)
    vsp.SetParmVal(vtail_id, "Taper", "XSec_1", 0.6)
    
    # Symmetric airfoil (NACA 0012)
    xsec_surf = vsp.GetXSecSurf(vtail_id, 0)
    vsp.ChangeXSecShape(xsec_surf, 0, vsp.XS_FOUR_SERIES)
    vsp.ChangeXSecShape(xsec_surf, 1, vsp.XS_FOUR_SERIES)
    
    vsp.SetParmVal(vtail_id, "Camber", "XSecCurve_0", 0.0)
    vsp.SetParmVal(vtail_id, "ThickChord", "XSecCurve_0", 0.12)
    
    # Position at rear
    vsp.SetParmVal(vtail_id, "X_Rel_Location", "XForm", 1.15)
    vsp.SetParmVal(vtail_id, "Z_Rel_Location", "XForm", 0.05)
    
    # Rotate to vertical (90 degrees around X-axis)
    vsp.SetParmVal(vtail_id, "X_Rel_Rotation", "XForm", 90.0)
    
    # Disable symmetry
    vsp.SetParmVal(vtail_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)
    
    vsp.Update()
    print(f"✓ Vertical tail created: {height}m height\n")
    return vtail_id

def save_model(filename=None):
    """Save OpenVSP model"""
    if filename is None:
        filename = f"{DESIGN_NAME}.vsp3"
    
    filepath = os.path.join(os.path.dirname(__file__), "..", "designs", filename)
    
    # Create designs directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    vsp.Update()
    vsp.WriteVSPFile(filepath)
    print(f"\n✓ Model saved: {filepath}\n")
    
    return filepath

def export_formats(base_filename):
    """Export model in various formats"""
    print("="*60)
    print("Exporting Model Files")
    print("="*60)
    
    designs_dir = os.path.join(os.path.dirname(__file__), "..", "designs")
    
    # Export sets for different formats
    all_sets = vsp.GetSetIndex("All")
    
    # STEP export
    step_file = os.path.join(designs_dir, f"{base_filename}.step")
    try:
        vsp.ExportFile(step_file, all_sets, vsp.EXPORT_STEP)
        print(f"✓ STEP: {step_file}")
    except Exception as e:
        print(f"⚠ STEP export failed: {e}")
    
    # STL export
    stl_file = os.path.join(designs_dir, f"{base_filename}.stl")
    try:
        vsp.ExportFile(stl_file, all_sets, vsp.EXPORT_STL)
        print(f"✓ STL: {stl_file}")
    except Exception as e:
        print(f"⚠ STL export failed: {e}")
    
    # IGES export
    iges_file = os.path.join(designs_dir, f"{base_filename}.iges")
    try:
        vsp.ExportFile(iges_file, all_sets, vsp.EXPORT_IGES)
        print(f"✓ IGES: {iges_file}")
    except Exception as e:
        print(f"⚠ IGES export failed: {e}")
    
    print()

def main():
    """Main execution"""
    print("="*60)
    print("Phase 1 Fixed-Wing Drone - OpenVSP Model Generator (FIXED)")
    print("="*60)
    print(f"Design: {DESIGN_NAME}")
    print(f"Wingspan: {WINGSPAN} m")
    print(f"Wing Area: {WING_AREA} m²")
    print(f"Configuration: High wing, pusher prop, H-tail")
    print("="*60 + "\n")
    
    # Clear existing model
    clear_model()
    
    # Create geometry in proper order
    fuse_id = create_fuselage()
    wing_id = create_main_wing()
    htail_id = create_horizontal_tail()
    vtail_id = create_vertical_tail()
    
    # Final update
    vsp.Update()
    print("="*60)
    print("Model Complete - All Components Created")
    print("="*60 + "\n")
    
    # Save model
    filepath = save_model()
    
    # Export formats
    export_formats(DESIGN_NAME)
    
    print("="*60)
    print("SUCCESS!")
    print("="*60)
    print("\nNext Steps:")
    print(f"1. Open in OpenVSP GUI:")
    print(f"   cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS")
    print(f"   ./vsp {filepath}")
    print(f"\n2. You should now see:")
    print(f"   • Fuselage (body)")
    print(f"   • Main wing (left + right)")
    print(f"   • Horizontal tail (left + right)")
    print(f"   • Vertical stabilizer")
    print("\n3. In OpenVSP:")
    print(f"   • Analysis → CompGeom")
    print(f"   • Analysis → Mass Properties")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
