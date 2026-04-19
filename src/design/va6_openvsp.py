#!/usr/bin/env python3
"""
VA-6 "Peregrine" Interceptor Drone - OpenVSP Model
Based on P1-SUN photo reference:
  - Fat torpedo/bomb fuselage (140mm dia x 650mm)
  - Blunt ogive nose
  - Cruciform wing (mid-body, 4 small wings at 90 deg)
  - Cruciform tail fins (aft, 4 large fins at 90 deg)
  - 4x motor pods at tail fin tips

Author: MegaDrone Project
Date: March 2026
"""

import sys
import os

try:
    import openvsp as vsp
    print(f"OpenVSP {vsp.GetVSPVersion()} loaded")
except ImportError as e:
    print(f"Failed to import OpenVSP: {e}")
    sys.exit(1)

# === DESIGN PARAMETERS (meters) ===
# Fuselage — torpedo body, matched to 5" PVC pipe (141.3mm OD)
FUSE_LENGTH = 0.680
FUSE_MAX_DIA = 0.1413     # 5" PVC OD = 141.3mm
FUSE_MAX_R = FUSE_MAX_DIA / 2

# Nose — Von Karman profile, 30mm seeker window
NOSE_LENGTH = 0.120
NOSE_TIP_DIA = 0.030      # reduced from 50mm for lower drag

# Tail — optimized boat-tail (150mm taper to 40mm, ~8° half-angle)
TAIL_TAPER_LEN = 0.150    # extended from 120mm
TAIL_END_DIA = 0.040      # reduced from 70mm

# No forward wing — single cruciform set only

# Motor pods at fin tips
# Motor: ~28mm dia (2207 class, 3600KV, custom 4.5x2.9" prop)
# Pod: motor dia + 4mm wall = 32mm
POD_LENGTH = 0.090
POD_DIA = 0.032

# Cruciform tail fins (aft, carries motors)
# 160mm span x 80mm chord, NACA 0008
# Sized for stability + 2-3G aero maneuvering (motors handle the rest)
FIN_SPAN = 0.160
FIN_CHORD = 0.080
FIN_THICKNESS = 0.08    # 8% t/c (NACA 0008)
FIN_X_POS = 0.530

DESIGN_NAME = "VA6_Peregrine"
VERSION = 16  # Increment each iteration
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "designs", "va6")


def create_fuselage():
    """Fat torpedo/bomb fuselage with blunt ogive nose."""
    print("\n1. Creating fuselage...")
    fuse_id = vsp.AddGeom("FUSELAGE")
    vsp.SetGeomName(fuse_id, "Fuselage")
    vsp.SetParmVal(fuse_id, "Length", "Design", FUSE_LENGTH)

    xsec_surf = vsp.GetXSecSurf(fuse_id, 0)

    num_xsecs = vsp.GetNumXSec(xsec_surf)

    # Von Karman nose + constant section + boat-tail
    # Map xsec stations to diameters based on position
    diameters = {}
    for i in range(num_xsecs):
        frac = i / max(num_xsecs - 1, 1)  # 0.0 to 1.0 along fuselage

        if frac < 0.02:
            # Nose tip
            dia = NOSE_TIP_DIA
        elif frac < NOSE_LENGTH / FUSE_LENGTH:
            # Von Karman nose taper (sine-based profile)
            import math
            nose_frac = (frac - 0.02) / (NOSE_LENGTH / FUSE_LENGTH - 0.02)
            # Von Karman: r = R * sqrt(theta - sin(2*theta)/2) / sqrt(pi)
            theta = nose_frac * math.pi
            vk_ratio = math.sqrt((theta - math.sin(2 * theta) / 2) / math.pi)
            dia = NOSE_TIP_DIA + (FUSE_MAX_DIA - NOSE_TIP_DIA) * vk_ratio
        elif frac > 1.0 - TAIL_TAPER_LEN / FUSE_LENGTH:
            # Boat-tail taper (linear for simplicity)
            tail_frac = (frac - (1.0 - TAIL_TAPER_LEN / FUSE_LENGTH)) / (TAIL_TAPER_LEN / FUSE_LENGTH)
            dia = FUSE_MAX_DIA - (FUSE_MAX_DIA - TAIL_END_DIA) * tail_frac
        else:
            # Constant section
            dia = FUSE_MAX_DIA

        diameters[i] = dia

    for i in range(num_xsecs):
        vsp.ChangeXSecShape(xsec_surf, i, vsp.XS_ELLIPSE)
        xsec = vsp.GetXSec(xsec_surf, i)
        dia = diameters[i]
        w = vsp.GetXSecParm(xsec, "Ellipse_Width")
        h = vsp.GetXSecParm(xsec, "Ellipse_Height")
        if vsp.ValidParm(w):
            vsp.SetParmVal(w, dia)
        if vsp.ValidParm(h):
            vsp.SetParmVal(h, dia)
        vsp.SetXSecContinuity(xsec, 1)

    vsp.Update()
    print(f"   Fuselage: {FUSE_LENGTH*1000:.0f}mm x {FUSE_MAX_DIA*1000:.0f}mm dia")
    return fuse_id



def create_single_fin(fuse_id, name, x_pos, span, chord, rotation):
    """Create a single fin with no symmetry, manually placed."""
    fin_id = vsp.AddGeom("WING", fuse_id)
    vsp.SetGeomName(fin_id, name)
    vsp.SetParmVal(fin_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)

    vsp.SetDriverGroup(fin_id, 1, vsp.SPAN_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER)
    vsp.SetParmVal(fin_id, "Span", "XSec_1", span)
    vsp.SetParmVal(fin_id, "Root_Chord", "XSec_1", chord)
    vsp.SetParmVal(fin_id, "Tip_Chord", "XSec_1", chord)
    vsp.SetParmVal(fin_id, "Sweep", "XSec_1", 0.0)
    vsp.SetParmVal(fin_id, "Dihedral", "XSec_1", 0.0)

    # Thin symmetric airfoil
    xsec_surf = vsp.GetXSecSurf(fin_id, 0)
    for j in range(vsp.GetNumXSec(xsec_surf)):
        vsp.ChangeXSecShape(xsec_surf, j, vsp.XS_FOUR_SERIES)
        xsec = vsp.GetXSec(xsec_surf, j)
        camber = vsp.GetXSecParm(xsec, "Camber")
        thick = vsp.GetXSecParm(xsec, "ThickChord")
        if vsp.ValidParm(camber):
            vsp.SetParmVal(camber, 0.0)
        if vsp.ValidParm(thick):
            vsp.SetParmVal(thick, FIN_THICKNESS)

    vsp.SetParmVal(fin_id, "X_Rel_Location", "XForm", x_pos)
    vsp.SetParmVal(fin_id, "X_Rel_Rotation", "XForm", rotation)

    vsp.Update()
    return fin_id


def create_cruciform_fins(fuse_id):
    """4 fins placed individually (no symmetry) for true cruciform."""
    print("\n2. Creating cruciform fins...")

    fin_ids = []

    # Right fin (0 deg - default horizontal)
    f = create_single_fin(fuse_id, "Fin_Right", FIN_X_POS, FIN_SPAN, FIN_CHORD, 0.0)
    fin_ids.append(f)
    print(f"   Fin_Right: 0 deg")

    # Top fin (90 deg rotation)
    f = create_single_fin(fuse_id, "Fin_Top", FIN_X_POS, FIN_SPAN, FIN_CHORD, 90.0)
    fin_ids.append(f)
    print(f"   Fin_Top: 90 deg")

    # Left fin (180 deg rotation)
    f = create_single_fin(fuse_id, "Fin_Left", FIN_X_POS, FIN_SPAN, FIN_CHORD, 180.0)
    fin_ids.append(f)
    print(f"   Fin_Left: 180 deg")

    # Bottom fin (was 270, overlapping with left — rotate to -90 / 270 via separate axis)
    f = create_single_fin(fuse_id, "Fin_Bottom", FIN_X_POS, FIN_SPAN, FIN_CHORD, -90.0)
    fin_ids.append(f)
    print(f"   Fin_Bottom: -90 deg")

    print(f"   4x fins: {FIN_SPAN*1000:.0f}mm span x {FIN_CHORD*1000:.0f}mm chord")
    return fin_ids


def create_motor_pod_standalone(name, x_pos, y_pos, z_pos):
    """Motor pod as standalone fuselage positioned absolutely in world coords."""
    pod_id = vsp.AddGeom("FUSELAGE")
    vsp.SetGeomName(pod_id, name)
    vsp.SetParmVal(pod_id, "Length", "Design", POD_LENGTH)
    vsp.SetParmVal(pod_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)

    # Pointed nose, full mid-section, rounded rear
    xsec_surf = vsp.GetXSecSurf(pod_id, 0)
    num_xsecs = vsp.GetNumXSec(xsec_surf)

    for j in range(num_xsecs):
        vsp.ChangeXSecShape(xsec_surf, j, vsp.XS_ELLIPSE)
        xsec = vsp.GetXSec(xsec_surf, j)
        w = vsp.GetXSecParm(xsec, "Ellipse_Width")
        h = vsp.GetXSecParm(xsec, "Ellipse_Height")

        if j == 0:
            dia = 0.001  # pointed front tip
        elif j == num_xsecs - 1:
            dia = POD_DIA * 0.7  # rounded rear (motor mount end)
        else:
            dia = POD_DIA  # full diameter mid-section

        if vsp.ValidParm(w):
            vsp.SetParmVal(w, dia)
        if vsp.ValidParm(h):
            vsp.SetParmVal(h, dia)

    # Absolute position in world coordinates
    vsp.SetParmVal(pod_id, "X_Rel_Location", "XForm", x_pos)
    vsp.SetParmVal(pod_id, "Y_Rel_Location", "XForm", y_pos)
    vsp.SetParmVal(pod_id, "Z_Rel_Location", "XForm", z_pos)

    vsp.Update()
    return pod_id


def create_motor_pods(fin_ids):
    """4 motor pods at each fin tip using absolute coordinates."""
    print("\n3. Creating motor pods at fin tips...")

    # Pod rear aligns with fin trailing edge, nose cone extends forward
    # Fin trailing edge = FIN_X_POS + FIN_CHORD
    # Pod rear = pod_x + POD_LENGTH = fin trailing edge
    pod_x = FIN_X_POS + FIN_CHORD - POD_LENGTH

    # Fin tip distance from fuselage centerline
    # OpenVSP wing root starts at centerline (Y=0), tip at Y=span
    tip_r = FIN_SPAN

    pod_ids = []

    # Right (fin at 0 deg → extends in +Y)
    p = create_motor_pod_standalone("Pod_Right", pod_x, tip_r, 0.0)
    pod_ids.append(p)

    # Left (fin at 180 deg → extends in -Y)
    p = create_motor_pod_standalone("Pod_Left", pod_x, -tip_r, 0.0)
    pod_ids.append(p)

    # Top (fin at 90 deg → extends in +Z)
    p = create_motor_pod_standalone("Pod_Top", pod_x, 0.0, tip_r)
    pod_ids.append(p)

    # Bottom (fin at 270 deg → extends in -Z)
    p = create_motor_pod_standalone("Pod_Bottom", pod_x, 0.0, -tip_r)
    pod_ids.append(p)

    print(f"   4x pods at tip_r={tip_r*1000:.0f}mm from centerline")
    print(f"   Pod size: {POD_LENGTH*1000:.0f}mm x {POD_DIA*1000:.0f}mm dia")
    return pod_ids


def save_model():
    """Save VSP3, STL, and STEP."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    vsp3_path = os.path.join(OUTPUT_DIR, f"{DESIGN_NAME}.vsp3")

    # Save versioned copy
    versioned_path = os.path.join(OUTPUT_DIR, f"{DESIGN_NAME}_v{VERSION}.vsp3")
    vsp.WriteVSPFile(versioned_path, vsp.SET_ALL)
    print(f"\n5. Saving model...")
    print(f"   Versioned: {versioned_path}")

    # Also save as "latest" for easy opening
    latest_path = os.path.join(OUTPUT_DIR, f"{DESIGN_NAME}.vsp3")
    vsp.WriteVSPFile(latest_path, vsp.SET_ALL)
    print(f"   Latest:    {latest_path}")

    stl_path = os.path.join(OUTPUT_DIR, f"{DESIGN_NAME}_v{VERSION}.stl")
    vsp.ExportFile(stl_path, vsp.SET_ALL, vsp.EXPORT_STL)
    print(f"   STL:       {stl_path}")

    return latest_path


def main():
    print("=" * 60)
    print("VA-6 PEREGRINE - OpenVSP Model Generator")
    print("=" * 60)

    vsp.ClearVSPModel()
    vsp.Update()

    fuse_id = create_fuselage()
    fin_ids = create_cruciform_fins(fuse_id)
    pod_ids = create_motor_pods(fin_ids)

    vsp3_path = save_model()

    # Set 4-view layout and fit to screen
    try:
        vsp.SetViewAxis(False)          # hide axis widget
        vsp.SetAllViews(vsp.VIEW_4)     # 4-panel layout
        vsp.FitAllViews()               # zoom to fit in all panels
        vsp.WriteVSPFile(vsp3_path, vsp.SET_ALL)  # re-save with view settings
        print("\n   View: 4-panel layout, fit to screen")
    except Exception as e:
        print(f"\n   View setup skipped: {e}")

    print("\n" + "=" * 60)
    print("DONE - Open in OpenVSP GUI:")
    print(f"  {vsp3_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
