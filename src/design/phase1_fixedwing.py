#!/usr/bin/env python3
"""
Phase 1 Fixed-Wing Drone Design Script
Creates OpenVSP model using Python API

Specifications:
- Wingspan: 2.2 m (7.2 ft)
- Wing Area: 0.55 m² (5.9 ft²)
- Configuration: High wing, pusher propeller, H-tail
- Airfoil: Eppler E423 (or NACA 2412 approximation)

Author: MegaDrone Project
Date: January 8, 2026
"""

import sys
import os

# Add OpenVSP to path
sys.path.insert(0, "/Users/matthewoneil/OpenVSP-3.46.0-MacOS")

try:
    import openvsp as vsp
    print(f"✓ OpenVSP {vsp.GetVSPVersion()} loaded successfully\n")
except ImportError as e:
    print(f"✗ Failed to import OpenVSP: {e}")
    print("Run openvsp_setup.py first to configure paths")
    sys.exit(1)

import numpy as np

# Design parameters
DESIGN_NAME = "Phase1_FixedWing_Trainer"
WINGSPAN = 2.2  # meters
WING_AREA = 0.55  # square meters
FUSELAGE_LENGTH = 1.3  # meters
TAIL_SPAN = 0.7  # meters

def clear_model():
    """Clear any existing geometry"""
    vsp.ClearVSPModel()
    print("Cleared existing model")

def create_main_wing():
    """Create main wing with taper and dihedral"""
    print("\n" + "="*60)
    print("Creating Main Wing")
    print("="*60)
    
    # Add wing component
    wing_id = vsp.AddGeom("WING")
    vsp.SetGeomName(wing_id, "Main_Wing")
    
    # Calculate root and tip chords
    # For taper ratio of 0.79, with given area and span
    taper_ratio = 0.79
    aspect_ratio = (WINGSPAN**2) / WING_AREA  # AR = b²/S
    root_chord = 2 * WING_AREA / (WINGSPAN * (1 + taper_ratio))
    tip_chord = root_chord * taper_ratio
    
    print(f"Aspect Ratio: {aspect_ratio:.2f}")
    print(f"Root Chord: {root_chord:.3f} m")
    print(f"Tip Chord: {tip_chord:.3f} m")
    
    # Set wing parameters
    vsp.SetParmVal(wing_id, "TotalSpan", "WingGeom", WINGSPAN)
    vsp.SetParmVal(wing_id, "TotalArea", "WingGeom", WING_AREA)
    
    # Root section (XSec 0)
    xsec_surf = vsp.GetXSecSurf(wing_id, 0)
    xsec_0 = vsp.GetXSec(xsec_surf, 0)
    vsp.SetParmVal(wing_id, "Root_Chord", "XSec_0", root_chord)
    
    # Tip section (XSec 1)
    xsec_1 = vsp.GetXSec(xsec_surf, 1)
    vsp.SetParmVal(wing_id, "Tip_Chord", "XSec_1", tip_chord)
    
    # Set dihedral (2 degrees for stability)
    vsp.SetParmVal(wing_id, "Dihedral", "XSec_1", 2.0)
    
    # Set sweep (0 degrees - straight wing)
    vsp.SetParmVal(wing_id, "Sweep", "XSec_1", 0.0)
    
    # Set twist (washout: -2 degrees at tip for gentle stall)
    vsp.SetParmVal(wing_id, "Twist", "XSec_1", -2.0)
    
    # Set airfoil (NACA 2412 as approximation for E423)
    vsp.ChangeXSecShape(xsec_surf, 0, vsp.XS_FOUR_SERIES)
    vsp.ChangeXSecShape(xsec_surf, 1, vsp.XS_FOUR_SERIES)
    
    # NACA 2412: 2% camber, 40% max camber position, 12% thickness
    vsp.SetParmVal(wing_id, "Camber", "XSecCurve_0", 0.02)
    vsp.SetParmVal(wing_id, "CamberLoc", "XSecCurve_0", 0.4)
    vsp.SetParmVal(wing_id, "ThickChord", "XSecCurve_0", 0.12)
    
    # Position wing (high wing configuration)
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 0.4)
    vsp.SetParmVal(wing_id, "Y_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(wing_id, "Z_Rel_Location", "XForm", 0.15)  # Above fuselage
    
    # Set incidence angle (1 degree)
    vsp.SetParmVal(wing_id, "X_Rel_Rotation", "XForm", 1.0)
    
    print(f"✓ Main wing created: {WINGSPAN}m span, {WING_AREA}m² area")
    return wing_id

def create_fuselage():
    """Create streamlined fuselage"""
    print("\n" + "="*60)
    print("Creating Fuselage")
    print("="*60)
    
    # Add fuselage component
    fuse_id = vsp.AddGeom("FUSELAGE")
    vsp.SetGeomName(fuse_id, "Fuselage")
    
    # Get XSec surface
    xsec_surf = vsp.GetXSecSurf(fuse_id, 0)
    
    # We'll create 5 cross-sections for streamlined shape
    # Clear default sections and add custom ones
    num_xsecs = vsp.GetNumXSec(xsec_surf)
    
    # Define fuselage stations (X locations and diameters)
    stations = [
        (0.0, 0.08),      # Nose
        (0.2, 0.14),      # Front transition
        (0.6, 0.15),      # Payload bay (max diameter)
        (1.0, 0.10),      # Rear transition
        (1.3, 0.05),      # Tail boom
    ]
    
    # Modify existing XSecs or add new ones
    for i, (x_pos, diameter) in enumerate(stations):
        if i < num_xsecs:
            xsec = vsp.GetXSec(xsec_surf, i)
        else:
            xsec = vsp.AppendXSec(xsec_surf, vsp.XS_CIRCLE)
        
        # Set position
        vsp.SetParmVal(fuse_id, "XDelta", f"XSec_{i}", x_pos if i == 0 else stations[i][0] - stations[i-1][0])
        
        # Set diameter
        vsp.ChangeXSecShape(xsec_surf, i, vsp.XS_CIRCLE)
        vsp.SetParmVal(fuse_id, "Circle_Diameter", f"XSecCurve_{i}", diameter)
    
    print(f"✓ Fuselage created: {FUSELAGE_LENGTH}m length, 5 sections")
    return fuse_id

def create_horizontal_tail():
    """Create horizontal stabilizer"""
    print("\n" + "="*60)
    print("Creating Horizontal Tail")
    print("="*60)
    
    # Add wing component for H-tail
    htail_id = vsp.AddGeom("WING")
    vsp.SetGeomName(htail_id, "Horizontal_Tail")
    
    # Set parameters
    root_chord = 0.18
    tip_chord = 0.14
    
    vsp.SetParmVal(htail_id, "TotalSpan", "WingGeom", TAIL_SPAN)
    vsp.SetParmVal(htail_id, "Root_Chord", "XSec_0", root_chord)
    vsp.SetParmVal(htail_id, "Tip_Chord", "XSec_1", tip_chord)
    
    # Symmetric airfoil (NACA 0012)
    xsec_surf = vsp.GetXSecSurf(htail_id, 0)
    vsp.ChangeXSecShape(xsec_surf, 0, vsp.XS_FOUR_SERIES)
    vsp.ChangeXSecShape(xsec_surf, 1, vsp.XS_FOUR_SERIES)
    vsp.SetParmVal(htail_id, "Camber", "XSecCurve_0", 0.0)  # Symmetric
    vsp.SetParmVal(htail_id, "ThickChord", "XSecCurve_0", 0.12)
    
    # Position at rear of fuselage
    vsp.SetParmVal(htail_id, "X_Rel_Location", "XForm", 1.15)
    vsp.SetParmVal(htail_id, "Z_Rel_Location", "XForm", 0.05)
    
    print(f"✓ Horizontal tail created: {TAIL_SPAN}m span")
    return htail_id

def create_vertical_tail():
    """Create vertical stabilizer"""
    print("\n" + "="*60)
    print("Creating Vertical Tail")
    print("="*60)
    
    # Add wing component (will rotate to vertical)
    vtail_id = vsp.AddGeom("WING")
    vsp.SetGeomName(vtail_id, "Vertical_Tail")
    
    # Set parameters
    height = 0.25
    root_chord = 0.20
    tip_chord = 0.12
    
    vsp.SetParmVal(vtail_id, "TotalSpan", "WingGeom", height)
    vsp.SetParmVal(vtail_id, "Root_Chord", "XSec_0", root_chord)
    vsp.SetParmVal(vtail_id, "Tip_Chord", "XSec_1", tip_chord)
    
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
    
    # Disable symmetry (only one vertical tail)
    vsp.SetParmVal(vtail_id, "Sym_Planar_Flag", "Sym", 0)  # No symmetry
    
    print(f"✓ Vertical tail created: {height}m height")
    return vtail_id

def create_propeller():
    """Create pusher propeller"""
    print("\n" + "="*60)
    print("Creating Propeller")
    print("="*60)
    
    # Add propeller component
    prop_id = vsp.AddGeom("PROP")
    vsp.SetGeomName(prop_id, "Pusher_Propeller")
    
    # Set parameters
    diameter = 0.33  # 13 inches in meters
    
    vsp.SetParmVal(prop_id, "Diameter", "Design", diameter)
    vsp.SetParmVal(prop_id, "NumBlade", "Design", 2)
    
    # Position at rear (pusher configuration)
    vsp.SetParmVal(prop_id, "X_Rel_Location", "XForm", 1.35)
    vsp.SetParmVal(prop_id, "Z_Rel_Location", "XForm", 0.0)
    
    print(f"✓ Propeller created: {diameter}m diameter, pusher config")
    return prop_id

def calculate_mass_properties():
    """Calculate and display mass properties"""
    print("\n" + "="*60)
    print("Mass Properties Analysis")
    print("="*60)
    
    # Run mass properties analysis
    # Note: Actual implementation requires setting component masses
    # This is a placeholder for the workflow
    
    print("\nComponent Mass Budget (Phase 1):")
    masses = {
        "Wing": 1.1,
        "Fuselage": 0.7,
        "H-Tail": 0.1,
        "V-Tail": 0.1,
        "Propeller": 0.1,
        "Motor": 0.2,
        "Battery": 3.0,
        "Avionics": 0.5,
        "Payload": 0.5,
        "Misc": 0.5,
    }
    
    total_mass = sum(masses.values())
    
    for comp, mass in masses.items():
        print(f"  {comp:15s}: {mass:5.2f} kg ({mass*2.205:5.2f} lbs)")
    
    print(f"\n  {'Total':15s}: {total_mass:5.2f} kg ({total_mass*2.205:5.2f} lbs)")
    
    # Target CG location (25-30% MAC)
    MAC = 0.26  # Mean aerodynamic chord (m)
    target_cg = 0.4 + 0.27 * MAC  # Wing LE + 27% MAC
    print(f"\nTarget CG: {target_cg:.3f} m (27% MAC)")
    
    return total_mass

def save_model(filename=None):
    """Save OpenVSP model"""
    if filename is None:
        filename = f"{DESIGN_NAME}.vsp3"
    
    filepath = os.path.join(os.path.dirname(__file__), "..", "designs", filename)
    
    # Create designs directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    vsp.WriteVSPFile(filepath)
    print(f"\n✓ Model saved: {filepath}")
    
    return filepath

def export_formats(base_filename):
    """Export model in various formats"""
    print("\n" + "="*60)
    print("Exporting Model Files")
    print("="*60)
    
    designs_dir = os.path.join(os.path.dirname(__file__), "..", "designs")
    
    # STEP export (for CAD)
    step_file = os.path.join(designs_dir, f"{base_filename}.step")
    vsp.ExportFile(step_file, vsp.EXPORT_STEP)
    print(f"✓ STEP file: {step_file}")
    
    # STL export (for 3D printing / CFD)
    stl_file = os.path.join(designs_dir, f"{base_filename}.stl")
    vsp.ExportFile(stl_file, vsp.EXPORT_STL)
    print(f"✓ STL file: {stl_file}")
    
    print("\nNote: DXF export for wing ribs available via GUI")
    print("      (File → Export → Airfoil Points)")

def main():
    """Main execution"""
    print("="*60)
    print("Phase 1 Fixed-Wing Drone - OpenVSP Model Generator")
    print("="*60)
    print(f"Design: {DESIGN_NAME}")
    print(f"Wingspan: {WINGSPAN} m")
    print(f"Wing Area: {WING_AREA} m²")
    print(f"Configuration: High wing, pusher prop, H-tail")
    print("="*60)
    
    # Clear existing model
    clear_model()
    
    # Create geometry
    wing_id = create_main_wing()
    fuse_id = create_fuselage()
    htail_id = create_horizontal_tail()
    vtail_id = create_vertical_tail()
    prop_id = create_propeller()
    
    # Calculate mass properties
    total_mass = calculate_mass_properties()
    
    # Update model
    vsp.Update()
    print("\n✓ Model geometry updated")
    
    # Save model
    filepath = save_model()
    
    # Export formats
    export_formats(DESIGN_NAME)
    
    print("\n" + "="*60)
    print("Model Generation Complete!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Open in OpenVSP GUI to visualize:")
    print(f"   cd /Users/matthewoneil/OpenVSP-3.46.0-MacOS && ./vsp {filepath}")
    print("2. Refine airfoil (import E423 coordinates)")
    print("3. Set component masses in GUI")
    print("4. Calculate CG and verify 25-30% MAC")
    print("5. Export DXF for wing ribs (manufacturing)")
    print("="*60)

if __name__ == "__main__":
    main()
