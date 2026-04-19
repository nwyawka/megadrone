#!/usr/bin/env python3
"""
VA-6 "Peregrine" — Export as 3 separate STEP files for 3D printing.

Sections:
  1. NOSE (0-230mm): Von Karman nose + warhead bay
  2. BODY (230-530mm): Avionics + battery bay (constant diameter section)
  3. AFT  (530-680mm): Boat-tail + cruciform fins + motor pods

Each section is a standalone OpenVSP model exported as STEP + STL.
Fits Bambu Lab P1S build volume (256 x 256 x 256mm).

Author: MegaDrone Project
Date: March 2026
"""

import sys
import os
import math

try:
    import openvsp as vsp
    print(f"OpenVSP {vsp.GetVSPVersion()} loaded")
except ImportError as e:
    print(f"Failed to import OpenVSP: {e}")
    sys.exit(1)

# === DESIGN PARAMETERS (meters) — same as va6_openvsp.py v13 ===
# Matched to 5" PVC pipe (141.3mm OD)
FUSE_LENGTH = 0.680
FUSE_MAX_DIA = 0.1413
FUSE_MAX_R = FUSE_MAX_DIA / 2

NOSE_LENGTH = 0.120
NOSE_TIP_DIA = 0.030
TAIL_TAPER_LEN = 0.150
TAIL_END_DIA = 0.040

POD_LENGTH = 0.090
POD_DIA = 0.032

FIN_SPAN = 0.160
FIN_CHORD = 0.080
FIN_THICKNESS = 0.08
FIN_X_POS = 0.530

# Section split points — all sections < 256mm for P1S bed
SPLIT_1 = 0.230  # End of nose section / start of body
SPLIT_2 = 0.480  # End of body section / start of aft (before fins at 530)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "designs", "va6", "sections")


def get_diameter_at(frac):
    """Von Karman nose + constant + boat-tail diameter at fractional position."""
    if frac < 0.02:
        return NOSE_TIP_DIA
    elif frac < NOSE_LENGTH / FUSE_LENGTH:
        nose_frac = (frac - 0.02) / (NOSE_LENGTH / FUSE_LENGTH - 0.02)
        theta = nose_frac * math.pi
        vk_ratio = math.sqrt((theta - math.sin(2 * theta) / 2) / math.pi)
        return NOSE_TIP_DIA + (FUSE_MAX_DIA - NOSE_TIP_DIA) * vk_ratio
    elif frac > 1.0 - TAIL_TAPER_LEN / FUSE_LENGTH:
        tail_frac = (frac - (1.0 - TAIL_TAPER_LEN / FUSE_LENGTH)) / (TAIL_TAPER_LEN / FUSE_LENGTH)
        return FUSE_MAX_DIA - (FUSE_MAX_DIA - TAIL_END_DIA) * tail_frac
    else:
        return FUSE_MAX_DIA


def create_fuselage_section(name, x_start, x_end, num_stations=7):
    """Create a fuselage section from x_start to x_end with enough xsecs for smooth shape."""
    length = x_end - x_start
    fuse_id = vsp.AddGeom("FUSELAGE")
    vsp.SetGeomName(fuse_id, name)
    vsp.SetParmVal(fuse_id, "Length", "Design", length)

    # Add cross-sections for smooth curves
    xsec_surf = vsp.GetXSecSurf(fuse_id, 0)
    target_xsecs = 15
    for _ in range(target_xsecs - vsp.GetNumXSec(xsec_surf)):
        vsp.InsertXSec(fuse_id, 2, vsp.XS_ELLIPSE)
    vsp.Update()
    xsec_surf = vsp.GetXSecSurf(fuse_id, 0)  # refresh

    num_xsecs = vsp.GetNumXSec(xsec_surf)

    for i in range(num_xsecs):
        vsp.ChangeXSecShape(xsec_surf, i, vsp.XS_ELLIPSE)
        xsec = vsp.GetXSec(xsec_surf, i)

        # Map local fraction to global fraction
        local_frac = i / max(num_xsecs - 1, 1)
        global_x = x_start + local_frac * length
        global_frac = global_x / FUSE_LENGTH
        dia = get_diameter_at(global_frac)

        w = vsp.GetXSecParm(xsec, "Ellipse_Width")
        h = vsp.GetXSecParm(xsec, "Ellipse_Height")
        if vsp.ValidParm(w):
            vsp.SetParmVal(w, dia)
        if vsp.ValidParm(h):
            vsp.SetParmVal(h, dia)
        vsp.SetXSecContinuity(xsec, 1)

    vsp.Update()
    return fuse_id


def create_fin(parent_id, name, x_pos_local, rotation):
    """Create a single fin at a local X position within the section."""
    fin_id = vsp.AddGeom("WING", parent_id)
    vsp.SetGeomName(fin_id, name)
    vsp.SetParmVal(fin_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)

    vsp.SetDriverGroup(fin_id, 1, vsp.SPAN_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER)
    vsp.SetParmVal(fin_id, "Span", "XSec_1", FIN_SPAN)
    vsp.SetParmVal(fin_id, "Root_Chord", "XSec_1", FIN_CHORD)
    vsp.SetParmVal(fin_id, "Tip_Chord", "XSec_1", FIN_CHORD)
    vsp.SetParmVal(fin_id, "Sweep", "XSec_1", 0.0)
    vsp.SetParmVal(fin_id, "Dihedral", "XSec_1", 0.0)

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

    vsp.SetParmVal(fin_id, "X_Rel_Location", "XForm", x_pos_local)
    vsp.SetParmVal(fin_id, "X_Rel_Rotation", "XForm", rotation)

    vsp.Update()
    return fin_id


def create_pod(name, x_pos, y_pos, z_pos):
    """Create a motor pod at absolute position."""
    pod_id = vsp.AddGeom("FUSELAGE")
    vsp.SetGeomName(pod_id, name)
    vsp.SetParmVal(pod_id, "Length", "Design", POD_LENGTH)
    vsp.SetParmVal(pod_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)

    xsec_surf = vsp.GetXSecSurf(pod_id, 0)
    num_xsecs = vsp.GetNumXSec(xsec_surf)

    for j in range(num_xsecs):
        vsp.ChangeXSecShape(xsec_surf, j, vsp.XS_ELLIPSE)
        xsec = vsp.GetXSec(xsec_surf, j)
        w = vsp.GetXSecParm(xsec, "Ellipse_Width")
        h = vsp.GetXSecParm(xsec, "Ellipse_Height")

        if j == 0:
            dia = 0.001
        elif j == num_xsecs - 1:
            dia = POD_DIA * 0.7
        else:
            dia = POD_DIA

        if vsp.ValidParm(w):
            vsp.SetParmVal(w, dia)
        if vsp.ValidParm(h):
            vsp.SetParmVal(h, dia)

    vsp.SetParmVal(pod_id, "X_Rel_Location", "XForm", x_pos)
    vsp.SetParmVal(pod_id, "Y_Rel_Location", "XForm", y_pos)
    vsp.SetParmVal(pod_id, "Z_Rel_Location", "XForm", z_pos)

    vsp.Update()
    return pod_id


def scale_stl_to_mm(input_path, output_path):
    """Scale ASCII STL from meters to millimeters."""
    import re
    with open(input_path, 'r') as f:
        content = f.read()

    def scale_vertex(match):
        x = float(match.group(1)) * 1000
        y = float(match.group(2)) * 1000
        z = float(match.group(3)) * 1000
        return f'     vertex  {x:.6e} {y:.6e} {z:.6e}'

    scaled = re.sub(
        r'     vertex\s+([-\d.e+]+)\s+([-\d.e+]+)\s+([-\d.e+]+)',
        scale_vertex,
        content
    )
    with open(output_path, 'w') as f:
        f.write(scaled)


def export_section(name, filename):
    """Export current model as STEP + STL (in meters) + STL (in mm for Bambu Studio)."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    step_path = os.path.join(OUTPUT_DIR, f"{filename}.step")
    stl_path = os.path.join(OUTPUT_DIR, f"{filename}.stl")
    stl_mm_path = os.path.join(OUTPUT_DIR, f"{filename}_mm.stl")
    vsp3_path = os.path.join(OUTPUT_DIR, f"{filename}.vsp3")

    vsp.WriteVSPFile(vsp3_path, vsp.SET_ALL)
    vsp.ExportFile(step_path, vsp.SET_ALL, vsp.EXPORT_STEP)
    vsp.ExportFile(stl_path, vsp.SET_ALL, vsp.EXPORT_STL)
    scale_stl_to_mm(stl_path, stl_mm_path)

    print(f"   STEP:   {step_path}")
    print(f"   STL:    {stl_path}")
    print(f"   STL mm: {stl_mm_path} (for Bambu Studio)")
    print(f"   VSP3:   {vsp3_path}")


def build_nose():
    """Section 1: Nose (0 to SPLIT_1) — 230mm"""
    print(f"\n{'=' * 60}")
    print(f"SECTION 1: NOSE (0 - {SPLIT_1*1000:.0f}mm)")
    print(f"{'=' * 60}")

    vsp.ClearVSPModel()
    vsp.Update()

    fuse_id = create_fuselage_section("Nose", 0, SPLIT_1)
    length = SPLIT_1 * 1000
    print(f"   Length: {length:.0f}mm (fits P1S bed: {length < 256})")

    export_section("Nose", "VA6_Nose")


def build_body():
    """Section 2: Body (SPLIT_1 to SPLIT_2) — 300mm"""
    print(f"\n{'=' * 60}")
    print(f"SECTION 2: BODY ({SPLIT_1*1000:.0f} - {SPLIT_2*1000:.0f}mm)")
    print(f"{'=' * 60}")

    vsp.ClearVSPModel()
    vsp.Update()

    fuse_id = create_fuselage_section("Body", SPLIT_1, SPLIT_2)
    length = (SPLIT_2 - SPLIT_1) * 1000
    print(f"   Length: {length:.0f}mm (fits P1S bed: {length > 256})")

    if length > 256:
        print(f"   WARNING: {length:.0f}mm exceeds P1S bed (256mm).")
        print(f"   Print diagonally (bed diagonal = 362mm) or split further.")

    export_section("Body", "VA6_Body")


def build_aft_body():
    """Aft fuselage tube only (no fins, no pods)."""
    print(f"\n{'=' * 60}")
    aft_length = FUSE_LENGTH - SPLIT_2
    print(f"SECTION 3a: AFT BODY ({SPLIT_2*1000:.0f} - {FUSE_LENGTH*1000:.0f}mm)")
    print(f"{'=' * 60}")

    vsp.ClearVSPModel()
    vsp.Update()

    fuse_id = create_fuselage_section("Aft_Body", SPLIT_2, FUSE_LENGTH)
    print(f"   Length: {aft_length*1000:.0f}mm (fits P1S: True)")

    export_section("Aft_Body", "VA6_Aft_Body")


def build_single_fin(name, rotation, label):
    """Single fin + motor pod as standalone print."""
    print(f"\n{'=' * 60}")
    print(f"SECTION 3{label}: FIN ({name}, {rotation} deg)")
    print(f"{'=' * 60}")

    vsp.ClearVSPModel()
    vsp.Update()

    # Fin as standalone wing (no parent fuselage)
    fin_id = vsp.AddGeom("WING")
    vsp.SetGeomName(fin_id, name)
    vsp.SetParmVal(fin_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)

    vsp.SetDriverGroup(fin_id, 1, vsp.SPAN_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER)
    vsp.SetParmVal(fin_id, "Span", "XSec_1", FIN_SPAN)
    vsp.SetParmVal(fin_id, "Root_Chord", "XSec_1", FIN_CHORD)
    vsp.SetParmVal(fin_id, "Tip_Chord", "XSec_1", FIN_CHORD)
    vsp.SetParmVal(fin_id, "Sweep", "XSec_1", 0.0)
    vsp.SetParmVal(fin_id, "Dihedral", "XSec_1", 0.0)

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

    vsp.Update()

    # Motor pod at fin tip
    pod_x = FIN_CHORD - POD_LENGTH  # pod rear at fin trailing edge
    create_pod(f"Pod_{name}", pod_x, FIN_SPAN, 0.0)

    total_len = max(FIN_CHORD, POD_LENGTH)
    print(f"   Fin: {FIN_SPAN*1000:.0f}mm span x {FIN_CHORD*1000:.0f}mm chord")
    print(f"   Pod: {POD_DIA*1000:.0f}mm dia x {POD_LENGTH*1000:.0f}mm at tip")
    print(f"   Total size: {total_len*1000:.0f}mm x {(FIN_SPAN + POD_DIA)*1000:.0f}mm (fits P1S: True)")

    export_section(name, f"VA6_Fin_{name}")


def main():
    print("=" * 60)
    print("VA-6 PEREGRINE — SECTION EXPORT FOR 3D PRINTING")
    print(f"Printer: Bambu Lab P1S (256 x 256 x 256mm)")
    print(f"Body: 5\" PVC pipe (SDR 41 or foam-core DWV), 141.3mm OD")
    print("=" * 60)

    body_len = SPLIT_2 - SPLIT_1
    print(f"\nBuild plan:")
    print(f"  PRINT  Section 1 (Nose): 0 - {SPLIT_1*1000:.0f}mm = {SPLIT_1*1000:.0f}mm")
    print(f"  PVC    Section 2 (Body): {SPLIT_1*1000:.0f} - {SPLIT_2*1000:.0f}mm = {body_len*1000:.0f}mm of 5\" PVC pipe")
    print(f"  PRINT  Section 3 (Aft):  {SPLIT_2*1000:.0f} - {FUSE_LENGTH*1000:.0f}mm = {(FUSE_LENGTH-SPLIT_2)*1000:.0f}mm")

    build_nose()

    print(f"\n{'=' * 60}")
    print(f"SECTION 2: BODY — CUT FROM PVC PIPE")
    print(f"{'=' * 60}")
    print(f"   Cut 5\" PVC pipe to {body_len*1000:.0f}mm length")
    print(f"   OD: {FUSE_MAX_DIA*1000:.1f}mm")
    print(f"   Options: SDR 41 (3.5mm wall, 524g) or foam-core DWV (4.8mm, 412g)")

    build_aft_body()
    build_single_fin("Right", 0, "b")
    build_single_fin("Top", 90, "c")
    build_single_fin("Left", 180, "d")
    build_single_fin("Bottom", -90, "e")

    print(f"\n{'=' * 60}")
    print(f"EXPORTED — 6 parts:")
    print(f"  PRINT: VA6_Nose_mm.stl       (nose, {SPLIT_1*1000:.0f}mm)")
    print(f"  CUT:   5\" PVC pipe           (body, {body_len*1000:.0f}mm)")
    print(f"  PRINT: VA6_Aft_Body_mm.stl   (aft tube, {(FUSE_LENGTH-SPLIT_2)*1000:.0f}mm)")
    print(f"  PRINT: VA6_Fin_Right_mm.stl  (fin + pod)")
    print(f"  PRINT: VA6_Fin_Top_mm.stl    (fin + pod)")
    print(f"  PRINT: VA6_Fin_Left_mm.stl   (fin + pod)")
    print(f"  PRINT: VA6_Fin_Bottom_mm.stl (fin + pod)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
