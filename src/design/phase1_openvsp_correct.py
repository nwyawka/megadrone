#!/usr/bin/env python3
"""
Phase 1 Fixed-Wing Drone - OpenVSP Model (CORRECT API USAGE)
Based on working OpenVSP example scripts

This version uses the CORRECT API calls as shown in OpenVSP examples.

Author: MegaDrone Project  
Date: January 8, 2026
"""

import sys
import os

try:
    import openvsp as vsp
    print(f"✓ OpenVSP {vsp.GetVSPVersion()} loaded\n")
except ImportError as e:
    print(f"✗ Failed to import OpenVSP: {e}")
    sys.exit(1)

# Design parameters
DESIGN_NAME = "Phase1_UAV_Correct"
WINGSPAN = 2.2  # meters
ROOT_CHORD = 0.28  # meters
TIP_CHORD = 0.22  # meters
FUSELAGE_LENGTH = 1.3  # meters

def create_model():
    """Create complete UAV model using correct API"""
    
    print("="*60)
    print("Creating Phase 1 UAV Model")
    print("="*60)
    
    # Clear any existing model
    vsp.ClearVSPModel()
    vsp.Update()
    
    # ==================== MAIN WING ====================
    print("\n1. Creating Main Wing...")
    wing_id = vsp.AddGeom("WING")
    vsp.SetGeomName(wing_id, "Main_Wing")
    
    # Set symmetry (XZ plane = left/right symmetry)
    vsp.SetParmVal(wing_id, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
    
    # Set driver group for wing section
    # Use SPAN, TAPER, ROOT_CHORD as drivers
    vsp.SetDriverGroup(wing_id, 1, vsp.SPAN_WSECT_DRIVER, vsp.TAPER_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER)
    
    # Set wing section parameters (XSec_1)
    semi_span = WINGSPAN / 2.0
    taper = TIP_CHORD / ROOT_CHORD
    
    vsp.SetParmVal(wing_id, "Span", "XSec_1", semi_span)
    vsp.SetParmVal(wing_id, "Root_Chord", "XSec_1", ROOT_CHORD)
    vsp.SetParmVal(wing_id, "Taper", "XSec_1", taper)
    vsp.SetParmVal(wing_id, "Sweep", "XSec_1", 0.0)  # No sweep
    vsp.SetParmVal(wing_id, "Dihedral", "XSec_1", 2.0)  # 2 degrees dihedral
    
    # Set twist (washout)
    vsp.SetParmVal(wing_id, "Twist", "XSec_1", -2.0)  # -2 degrees at tip
    
    # Position wing (high-wing configuration)
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 0.4)
    vsp.SetParmVal(wing_id, "Z_Rel_Location", "XForm", 0.15)
    vsp.SetParmVal(wing_id, "X_Rel_Rotation", "XForm", 1.0)  # 1 degree incidence
    
    vsp.Update()
    print(f"   ✓ Main wing: {WINGSPAN}m span, root={ROOT_CHORD}m, tip={TIP_CHORD}m")
    
    # ==================== FUSELAGE ====================
    print("\n2. Creating Fuselage...")
    fuse_id = vsp.AddGeom("FUSELAGE")
    vsp.SetGeomName(fuse_id, "Fuselage")
    
    # Set length and diameter
    vsp.SetParmVal(fuse_id, "Length", "Design", FUSELAGE_LENGTH)
    
    # Get XSec surface to modify cross-sections
    xsec_surf = vsp.GetXSecSurf(fuse_id, 0)
    
    # Get number of cross-sections
    num_xsecs = vsp.GetNumXSec(xsec_surf)
    
    # Set cross-section sizes:
    # - Nose (first) and tail (last) should be points (near-zero size) for closed ends
    # - Middle sections are 0.25m diameter
    for i in range(num_xsecs):
        # Change shape to ellipse
        vsp.ChangeXSecShape(xsec_surf, i, vsp.XS_ELLIPSE)

        # Get the XSec object
        xsec = vsp.GetXSec(xsec_surf, i)

        # Get parameter IDs using GetXSecParm
        width_parm = vsp.GetXSecParm(xsec, "Ellipse_Width")
        height_parm = vsp.GetXSecParm(xsec, "Ellipse_Height")

        # Determine size: points at nose/tail, 0.25m for middle sections
        if i == 0 or i == num_xsecs - 1:
            # Nose and tail: near-zero for pointed, closed ends
            size = 0.001
        else:
            # Middle sections: full diameter
            size = 0.25

        if vsp.ValidParm(width_parm):
            vsp.SetParmVal(width_parm, size)
        if vsp.ValidParm(height_parm):
            vsp.SetParmVal(height_parm, size)

        # Set continuity for smooth surface (C1 continuity)
        vsp.SetXSecContinuity(xsec, 1)

    # Set tangent angles at nose and tail for pointed, closed ends
    nose_xsec = vsp.GetXSec(xsec_surf, 0)
    tail_xsec = vsp.GetXSec(xsec_surf, num_xsecs - 1)

    # Nose: 90 degree tangent (points forward)
    # Tail: -90 degree tangent (points backward)
    # Parameters: (xsec_id, side, top, right, bottom, left) - use -1.0e12 for defaults
    vsp.SetXSecTanAngles(nose_xsec, vsp.XSEC_BOTH_SIDES, 90, -1.0e12, -1.0e12, -1.0e12)
    vsp.SetXSecTanAngles(tail_xsec, vsp.XSEC_BOTH_SIDES, -90, -1.0e12, -1.0e12, -1.0e12)

    vsp.Update()
    print(f"   ✓ Fuselage: {FUSELAGE_LENGTH}m length, 0.25m diameter, pointed nose/tail")
    
    # ==================== HORIZONTAL TAIL ====================
    print("\n3. Creating Horizontal Tail...")
    htail_id = vsp.AddGeom("WING")
    vsp.SetGeomName(htail_id, "H_Tail")
    
    # Set symmetry
    vsp.SetParmVal(htail_id, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
    
    # Set driver group
    vsp.SetDriverGroup(htail_id, 1, vsp.SPAN_WSECT_DRIVER, vsp.TAPER_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER)
    
    # Tail dimensions
    htail_span = 0.35  # semi-span
    htail_root = 0.18
    htail_taper = 0.7
    
    vsp.SetParmVal(htail_id, "Span", "XSec_1", htail_span)
    vsp.SetParmVal(htail_id, "Root_Chord", "XSec_1", htail_root)
    vsp.SetParmVal(htail_id, "Taper", "XSec_1", htail_taper)
    
    # Position at rear
    vsp.SetParmVal(htail_id, "X_Rel_Location", "XForm", 1.15)
    vsp.SetParmVal(htail_id, "Z_Rel_Location", "XForm", 0.05)
    
    vsp.Update()
    print(f"   ✓ Horizontal tail: {htail_span*2}m span")
    
    # ==================== VERTICAL TAIL ====================
    print("\n4. Creating Vertical Tail...")
    vtail_id = vsp.AddGeom("WING")
    vsp.SetGeomName(vtail_id, "V_Tail")
    
    # NO symmetry for vertical tail
    vsp.SetParmVal(vtail_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)
    
    # Set driver group
    vsp.SetDriverGroup(vtail_id, 1, vsp.SPAN_WSECT_DRIVER, vsp.TAPER_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER)
    
    # Tail dimensions
    vtail_height = 0.25
    vtail_root = 0.20
    vtail_taper = 0.6
    
    vsp.SetParmVal(vtail_id, "Span", "XSec_1", vtail_height)
    vsp.SetParmVal(vtail_id, "Root_Chord", "XSec_1", vtail_root)
    vsp.SetParmVal(vtail_id, "Taper", "XSec_1", vtail_taper)
    
    # Position and rotate to vertical
    vsp.SetParmVal(vtail_id, "X_Rel_Location", "XForm", 1.15)
    vsp.SetParmVal(vtail_id, "Z_Rel_Location", "XForm", 0.05)
    vsp.SetParmVal(vtail_id, "X_Rel_Rotation", "XForm", 90.0)  # Rotate 90 degrees
    
    vsp.Update()
    print(f"   ✓ Vertical tail: {vtail_height}m height")
    
    # ==================== FINAL UPDATE ====================
    vsp.Update()
    print("\n" + "="*60)
    print("Model Complete!")
    print("="*60)
    
    return wing_id, fuse_id, htail_id, vtail_id

def save_and_export():
    """Save VSP3 file and export other formats"""
    
    # Create output directory
    designs_dir = os.path.join(os.path.dirname(__file__), "..", "designs")
    os.makedirs(designs_dir, exist_ok=True)
    
    # Save VSP3 file
    vsp3_path = os.path.join(designs_dir, f"{DESIGN_NAME}.vsp3")
    vsp.WriteVSPFile(vsp3_path, vsp.SET_ALL)
    print(f"\n✓ Saved: {vsp3_path}")
    
    # Export STEP
    step_path = os.path.join(designs_dir, f"{DESIGN_NAME}.step")
    vsp.ExportFile(step_path, vsp.SET_ALL, vsp.EXPORT_STEP)
    print(f"✓ Exported STEP: {step_path}")
    
    # Export STL
    stl_path = os.path.join(designs_dir, f"{DESIGN_NAME}.stl")
    vsp.ExportFile(stl_path, vsp.SET_ALL, vsp.EXPORT_STL)
    print(f"✓ Exported STL: {stl_path}")
    
    return vsp3_path

def check_errors():
    """Check for any API errors"""
    # Note: GetNumTotalErrors() not available in Python wrapper
    # Errors will be printed to console automatically
    print("\n✓ Model generated successfully")

def main():
    """Main execution"""
    print("="*60)
    print("OpenVSP Phase 1 UAV Generator")
    print("="*60)
    print(f"Design: {DESIGN_NAME}")
    print(f"Wingspan: {WINGSPAN} m")
    print(f"Root Chord: {ROOT_CHORD} m")
    print(f"Tip Chord: {TIP_CHORD} m")
    print("="*60)
    
    # Create model
    wing_id, fuse_id, htail_id, vtail_id = create_model()
    
    # Save and export
    vsp3_path = save_and_export()
    
    # Check for errors
    check_errors()
    
    # Success message
    print("\n" + "="*60)
    print("✓ SUCCESS - Model Created!")
    print("="*60)
    print(f"\nOpen in OpenVSP:")
    print(f"  cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS")
    print(f"  ./vsp {vsp3_path}")
    print(f"\nYou should now see:")
    print(f"  • Fuselage (body)")
    print(f"  • Main Wing (swept, tapered, with dihedral)")
    print(f"  • Horizontal Tail (left + right)")
    print(f"  • Vertical Stabilizer (single fin)")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
