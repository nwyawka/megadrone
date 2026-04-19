"""Odin-style drone body — reference-length parametric build.  Revision r1.

Inspired by the Odin drone but built from simple primitives for 3D printing.
Reference length  L = body diameter.

Printable parts:
  1_Nose_PRINT      hollow 3 mm shell, hemisphere + aft interior lip (slip fit
                    into PVC tube)
  2_PVC_REF         off-the-shelf PVC tube (body), NOT printed — reference only
  3_Boattail_PRINT  hollow 3 mm shell with forward interior mount ring + 4
                    triangular fins integrated; aft face open (bottom hole)
  4-7_Wing_*_PRINT  flat triangular plate + airfoil-free triangular planform
                    + integrated saddle block (stadium shape, curved bottom
                    matching PVC OD, 3×2 M3 countersunk mount holes, 3 M4
                    countersunk is too much — M3 flush) + 3× Ø4 mm spanwise
                    spar holes + motor pad at tip

Everything driven by a single reference length L (body diameter).

Open in CQ-editor:   File > Open > CAD/odin_body.py
Export STLs:         import odin_body as p; p.export_stls('CAD/stl')
"""

__version__ = "r1"

import math
from pathlib import Path

import cadquery as cq


# ============================ Airfoil loader ==============================
AIRFOIL_PATH = (Path(__file__).parent.parent / "designs" / "phase1"
                / "optimized_airfoil.dat").resolve()


def load_airfoil(path: Path, chord: float, subsample: int = 6) -> list[tuple[float, float]]:
    """Load an airfoil .dat file and return scaled (x, y) points in chord units.
    Subsamples the raw curve for a tractable spline."""
    raw = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            parts = s.split()
            if len(parts) < 2:
                continue
            try:
                x, y = float(parts[0]), float(parts[1])
            except ValueError:
                continue
            raw.append((x * chord, y * chord))
    pts = raw[::subsample]
    if pts[-1] != raw[-1]:
        pts.append(raw[-1])
    return pts


def airfoil_camber(path: Path, x_frac: float, tol: float = 0.015) -> float:
    """Mean camber Y (in chord-fractions) at a given X fraction along the chord."""
    ys = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            try:
                x, y = float(s.split()[0]), float(s.split()[1])
            except ValueError:
                continue
            if abs(x - x_frac) < tol:
                ys.append(y)
    if not ys:
        return 0.0
    return 0.5 * (max(ys) + min(ys))


def naca_symmetric(t: float, chord: float, n: int = 40) -> list[tuple[float, float]]:
    """Generate a symmetric NACA 4-digit airfoil contour (upper LE→TE, then
    lower TE→LE) scaled to the given chord. t = thickness ratio (0.08 = NACA 0008).
    Low-drag default for the cruciform fins."""
    upper, lower = [], []
    for i in range(n + 1):
        xc = i / n
        yt = 5 * t * (
            0.2969 * math.sqrt(xc) - 0.1260 * xc
            - 0.3516 * xc ** 2 + 0.2843 * xc ** 3 - 0.1015 * xc ** 4
        )
        upper.append((xc * chord, yt * chord))
        lower.append((xc * chord, -yt * chord))
    return upper + list(reversed(lower))[1:-1]


def parabolic_flat_airfoil(
    t_ratio: float,
    chord: float,
    le_frac: float = 0.15,
    taper_frac: float = 0.50,
    n_le: int = 20,
    n_te: int = 20,
):
    """Symmetric custom airfoil built from 3 sections:
      [0 .. le_frac·C]           parabolic LE  y = T/2 · √(x/LE_end)
      [le_frac·C .. taper_frac·C] flat at y = T/2
      [taper_frac·C .. C]        quadratic TE, tangent(0) at start → 0 at TE
    Returns upper-surface points only (sorted by x). The wire builder uses
    these directly with spline/line segments so the flat part stays straight.
    """
    T2 = t_ratio * chord / 2.0
    x_le_end = le_frac * chord
    x_te_start = taper_frac * chord

    le = []
    for i in range(1, n_le + 1):          # skip (0, 0) — handled separately
        x = x_le_end * (i / n_le)
        y = T2 * math.sqrt(x / x_le_end) if x_le_end > 0 else 0.0
        le.append((x, y))
    te = []
    for i in range(1, n_te + 1):          # skip the tangent start (already at T2)
        x = x_te_start + (chord - x_te_start) * (i / n_te)
        frac = (x - x_te_start) / (chord - x_te_start)
        y = T2 * (1.0 - frac ** 2)
        te.append((x, y))
    return {
        "le": le,                         # upper LE spline points, (x_le_end, T2) inclusive
        "flat_end": (x_te_start, T2),     # start of TE taper
        "te": te,                         # TE spline to (chord, 0)
        "T2": T2,
    }


# ============================ Reference + multipliers =====================
L             = 115.0        # reference length (= body diameter)
BODY_MULT     = 4.0          # body length in ref lengths
BODY_EXTRA    = 63.0         # extra mm added to body length
BOATTAIL_MULT = 1.0          # boattail length in ref lengths (1 diam long)
END_DIA       = L / 4.0      # clipped aft face diameter (edit to taste)

# Wings (4× cruciform, airfoil cross-section, integrated root block + spars)
WING_POS_FRAC   = 0.60       # wing midchord at this fraction of TOTAL_LEN (moved another -5%)
WING_CHORD      = L          # root chord = 1 L
WING_SPAN       = 1.25 * L   # tip extension past body surface (1.25 diam)
WING_THICKNESS  = 6.0        # (legacy — used for pad Y offset compatibility)
WING_ROOT_EMBED = 3.0        # (legacy)

# Root block — saddle plate on PVC tube for PVC mounting
BLOCK_MARGIN_FORE_AFT = 5.0  # block extends 5 mm past LE and TE
BLOCK_WIDTH           = 30.0 # Y-direction at roll=0 (widened +10 mm)
BLOCK_HEIGHT          = 4.0  # Z-direction (radial thickness above PVC tangent)
BLOCK_DEPTH_INTO_PVC  = 3.0  # block extends 3 mm below R before the PVC-cylinder cut
# 6 flush-mount screws in a 3×2 grid (3 per side of wing midplane)
BLOCK_SCREW_DIA       = 3.2  # M3 clearance
BLOCK_CSK_DIA         = 6.0  # M3 countersink head
BLOCK_CSK_ANGLE       = 90.0
BLOCK_SCREW_SPACING_X = 40.0 # between columns along chord
BLOCK_SCREW_SPACING_Y = 20.0 # between rows (=2*offset from wing midplane)

# Spar through-holes (running the span)
N_SPARS               = 3
SPAR_DIA              = 4.0
SPAR_X_FRACS          = (0.25, 0.50, 0.70)   # placed in the thick part of airfoil

# Airfoil for wings — custom symmetric: parabolic LE + flat middle + tapered TE
AIRFOIL_TC            = 0.08                 # thickness-to-chord ratio
AIRFOIL_LE_FRAC       = 0.15                 # parabolic LE ends at 15% chord
AIRFOIL_TAPER_FRAC    = 0.50                 # flat middle ends / TE taper begins at 50% chord

# Boattail fins (4× cruciform, triangular, tip at body radius)
FIN_THICKNESS   = 6.0        # plate thickness

# PVC body tube (NOT printed — off-the-shelf tube) & printable joint features
PVC_OD          = L                       # PVC tube OD = reference body dia
PVC_WALL        = 3.0                     # PVC wall thickness
PVC_ID          = PVC_OD - 2 * PVC_WALL   # 109 mm
LIP_CLEARANCE   = 0.5                     # per side, slip fit into PVC
LIP_OD          = PVC_ID - 2 * LIP_CLEARANCE
LIP_R           = LIP_OD / 2.0
LIP_LENGTH      = 20.0                    # how far the lip inserts into the tube
NOSE_WALL       = 3.0                     # shell thickness of hollow nose
BOATTAIL_WALL   = 3.0                     # shell thickness of hollow boattail


# Motor mount pads (one at each wing tip, straddling the wing midplane)
MOTOR_OD         = 35.0       # motor outer diameter — pad diameter matches
PAD_DIA          = MOTOR_OD
PAD_THICKNESS    = 4.0        # pad plate thickness
SCREW_HOLE_DIA   = 3.2        # clearance hole for M3 screws
# Motor bolt pattern — square, centered on pad. Default = 19 mm (typical 28xx class).
# 4 holes arranged 2 per side of the wing, mirrored about the wing midplane.
SCREW_PITCH      = 19.0
WIRING_HOLE_DIA  = 10.0       # center hole for motor wires

# ============================ Derived =====================================
R         = L / 2.0
END_R     = END_DIA / 2.0
NOSE_LEN  = R                  # hemisphere height = radius
BODY_LEN  = BODY_MULT * L + BODY_EXTRA
BT_LEN    = BOATTAIL_MULT * L

NOSE_END  = NOSE_LEN
BODY_END  = NOSE_END + BODY_LEN
AFT_END   = BODY_END + BT_LEN
TOTAL_LEN = AFT_END


# ============================ Builders ====================================
def hemisphere_profile(n: int = 36) -> list[tuple[float, float]]:
    """Quarter-circle (x, r) points from nose tip (0, 0) to base (R, R)."""
    pts = []
    for i in range(n + 1):
        t = (math.pi / 2) * (i / n)
        pts.append((R * (1.0 - math.cos(t)), R * math.sin(t)))
    return pts


def build_nose() -> cq.Workplane:
    """Hemispherical nose with aft interior lip, hollow NOSE_WALL shell,
    aft face open. Built as outer-solid cut by inner cavity."""
    import math
    n = 36
    outer_hemi = [
        (R * (1 - math.cos((math.pi / 2) * (i / n))),
         R * math.sin((math.pi / 2) * (i / n)))
        for i in range(n + 1)
    ]
    inner_hemi = [
        (R - (R - NOSE_WALL) * math.cos((math.pi / 2) * (i / n)),
         (R - NOSE_WALL) * math.sin((math.pi / 2) * (i / n)))
        for i in range(n + 1)
    ]
    # Outer solid (nose + lip)
    outer = (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .spline(outer_hemi[1:])
        .lineTo(NOSE_LEN, LIP_R)
        .lineTo(NOSE_LEN + LIP_LENGTH, LIP_R)
        .lineTo(NOSE_LEN + LIP_LENGTH, 0)
        .close()
        .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0))
    )
    # Inner cavity (hollow region)
    eps = 0.2
    inner = (
        cq.Workplane("XZ")
        .moveTo(NOSE_WALL, 0)                            # inner tip (3 mm from nose tip)
        .spline(inner_hemi[1:])                          # inner hemisphere to (NOSE_LEN, R - WALL)
        .lineTo(NOSE_LEN, LIP_R - NOSE_WALL)             # inner shoulder step
        .lineTo(NOSE_LEN + LIP_LENGTH + eps, LIP_R - NOSE_WALL)  # past aft face for clean cut
        .lineTo(NOSE_LEN + LIP_LENGTH + eps, 0)
        .close()
        .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0))
    )
    return outer.cut(inner)


def build_body() -> cq.Workplane:
    return (
        cq.Workplane("YZ")
        .workplane(offset=NOSE_END)
        .circle(R)
        .extrude(BODY_LEN)
    )


def build_boattail() -> cq.Workplane:
    """Hollow boattail shell with a forward interior mount ring (slip fit
    into PVC tube). Both ends are open ⇒ open aft face = bottom hole.
        ring: BODY_END−LIP_LENGTH .. BODY_END, OD=LIP_OD
        cone: BODY_END .. AFT_END, outer tapers R → END_R
        wall: BOATTAIL_WALL (3 mm) throughout
    """
    eps = 0.2  # extend inner profile slightly past ends for clean boolean cut
    # Outer profile (solid boundary)
    outer_pts = [
        (BODY_END - LIP_LENGTH, 0.0),
        (BODY_END - LIP_LENGTH, LIP_R),
        (BODY_END, LIP_R),
        (BODY_END, R),
        (AFT_END,  END_R),
        (AFT_END,  0.0),
    ]
    outer = (
        cq.Workplane("XZ")
        .polyline(outer_pts).close()
        .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0))
    )
    # Inner cavity (offset inward by BOATTAIL_WALL, open at both ends)
    wall = BOATTAIL_WALL
    inner_pts = [
        (BODY_END - LIP_LENGTH - eps, 0.0),
        (BODY_END - LIP_LENGTH - eps, LIP_R - wall),
        (BODY_END, LIP_R - wall),
        (BODY_END, R - wall),
        (AFT_END + eps, END_R - wall),
        (AFT_END + eps, 0.0),
    ]
    inner = (
        cq.Workplane("XZ")
        .polyline(inner_pts).close()
        .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0))
    )
    return outer.cut(inner)


def build_body_tube() -> cq.Workplane:
    """Reference PVC tube (NOT PRINTED). Visualization only."""
    return (
        cq.Workplane("YZ")
        .workplane(offset=NOSE_END)
        .circle(PVC_OD / 2.0)
        .circle(PVC_ID / 2.0)
        .extrude(BODY_LEN)
    )


def build_wing(roll_deg: float) -> cq.Workplane:
    """Wing-as-one-piece: symmetric (NACA 0008) airfoil cross-section with a
    TRIANGULAR planform (right triangle: root LE → root TE → tip at aft-
    outboard corner). Integrated root saddle block with 5 flush-mount screw
    holes, 3 spanwise Ø4 mm spar holes, and the motor pad at the tip.

    Built by: extrude NACA 0008 along span as a rectangular wing, then cut
    the forward-outboard triangular corner to form the triangular planform.
    """
    wing_mid_x = WING_POS_FRAC * TOTAL_LEN
    le_x = wing_mid_x - WING_CHORD / 2.0
    te_x = wing_mid_x + WING_CHORD / 2.0 + PAD_THICKNESS / 2.0   # extend TE aft to meet +X pad face
    root_z = R
    tip_z  = R + WING_SPAN + PAD_DIA / 2.0                       # extend tip so wing bisects pad
    span   = tip_z - root_z

    # -------- Flat triangular plate wing (original geometry) --------
    # Triangle drawn in XZ plane, extruded in Y to give WING_THICKNESS,
    # then centered on Y=0.
    wing = (
        cq.Workplane("XZ")
        .polyline([
            (le_x, root_z),
            (te_x, root_z),
            (te_x, tip_z),
        ])
        .close()
        .extrude(WING_THICKNESS)
        .translate((0, +WING_THICKNESS / 2.0, 0))   # center wing midplane on Y=0
    )

    # -------- Root block (saddle): stadium planform (rounded fore/aft) with
    # curved bottom matching the PVC tube OD --------
    block_len = WING_CHORD + 2 * BLOCK_MARGIN_FORE_AFT
    block_prism = (
        cq.Workplane("XY", origin=(wing_mid_x, 0, R - BLOCK_DEPTH_INTO_PVC))
        .slot2D(block_len, BLOCK_WIDTH)
        .extrude(BLOCK_HEIGHT + BLOCK_DEPTH_INTO_PVC)
    )
    # Carve out the PVC cylinder → block bottom conforms to tube OD
    pvc_cyl = (
        cq.Workplane("YZ")
        .workplane(offset=wing_mid_x - block_len / 2.0 - 10)
        .circle(R)
        .extrude(block_len + 20)
    )
    block = block_prism.cut(pvc_cyl)
    wing = wing.union(block)

    # -------- 3×2 flush-mount countersunk screw grid (3 per side of wing) --------
    # Target the block top face. centerOption=CenterOfBoundBox puts the
    # workplane origin at the face center so rarray positions hit the block.
    block_top_ref = (wing_mid_x, 0, R + BLOCK_HEIGHT + 0.1)
    wing = (
        wing.faces(cq.selectors.NearestToPointSelector(block_top_ref))
        .workplane(centerOption="CenterOfBoundBox")
        .rarray(BLOCK_SCREW_SPACING_X, BLOCK_SCREW_SPACING_Y, 3, 2)
        .cskHole(BLOCK_SCREW_DIA, cskDiameter=BLOCK_CSK_DIA,
                 cskAngle=BLOCK_CSK_ANGLE, depth=None)
    )

    # -------- Spanwise spar holes (3 × 4 mm at 25/50/70% chord, on Y=0) --------
    for xf in SPAR_X_FRACS:
        x_hole = le_x + xf * WING_CHORD
        spar = (
            cq.Workplane("XY", origin=(x_hole, 0.0, root_z - 1))
            .circle(SPAR_DIA / 2.0)
            .extrude(span + 2.0)
        )
        wing = wing.cut(spar)

    # -------- Motor pad at the tip --------
    wing = wing.union(_build_motor_pad_inline())

    return wing.rotate((0, 0, 0), (1, 0, 0), roll_deg)


def _build_motor_pad_inline() -> cq.Workplane:
    """Motor pad built in the wing's local (pre-rotation) frame. Identical
    to build_motor_pad but without the final roll rotation, so it unions
    cleanly with the wing before the whole assembly is rolled."""
    wing_mid_x = WING_POS_FRAC * TOTAL_LEN
    te_x = wing_mid_x + WING_CHORD / 2.0
    pad_center_z = R + WING_SPAN
    pad = (
        cq.Workplane("YZ")
        .workplane(offset=te_x - PAD_THICKNESS / 2.0)
        .circle(PAD_DIA / 2.0)
        .extrude(PAD_THICKNESS)
    )
    pad = (
        pad.faces(">X").workplane()
        .rarray(SCREW_PITCH, SCREW_PITCH, 2, 2)
        .hole(SCREW_HOLE_DIA, depth=PAD_THICKNESS)
    )
    # Wing midplane is now at Y=0 → pad needs no Y offset
    return pad.translate((0, 0, pad_center_z))


def build_motor_pad(roll_deg: float) -> cq.Workplane:
    """Circular motor mount pad. Pad center at the wing's original tip
    position (te_x, 0, R + WING_SPAN). Wing midplane Y=0 passes through
    pad center (Y=0). Motors mount on the +X face."""
    wing_mid_x = WING_POS_FRAC * TOTAL_LEN
    te_x = wing_mid_x + WING_CHORD / 2.0
    pad_center_z = R + WING_SPAN

    pad = (
        cq.Workplane("YZ")
        .workplane(offset=te_x - PAD_THICKNESS / 2.0)
        .circle(PAD_DIA / 2.0)
        .extrude(PAD_THICKNESS)
    )
    pad = (
        pad.faces(">X").workplane()
        .rarray(SCREW_PITCH, SCREW_PITCH, 2, 2)
        .hole(SCREW_HOLE_DIA, depth=PAD_THICKNESS)
    )
    # Shift the pad in −Y by WING_THICKNESS so its center lands on the
    # wing midplane (CQ's XZ workplane extrudes in −Y, so the wing midplane
    # ended up at Y = −WING_THICKNESS, not Y = 0).
    return (
        pad.translate((0, -WING_THICKNESS, pad_center_z))
        .rotate((0, 0, 0), (1, 0, 0), roll_deg)
    )


def build_fin(roll_deg: float) -> cq.Workplane:
    """Triangular fin on the boattail. Root edge lies on the boattail's
    conical surface (from forward to aft). The fin's outer edge is
    horizontal at the body radius R (so max fin radius = body radius).
    Midplane centered on Y=0 (same fix applied to the wings)."""
    pts = [
        (BODY_END, R),
        (AFT_END,  END_R),
        (AFT_END,  R),
    ]
    fin = (
        cq.Workplane("XZ")
        .polyline(pts).close()
        .extrude(FIN_THICKNESS)
        .translate((0, +FIN_THICKNESS / 2.0, 0))   # center fin midplane on Y=0
    )
    return fin.rotate((0, 0, 0), (1, 0, 0), roll_deg)


nose     = build_nose()
body     = build_body()                 # legacy solid body (kept for airframe union)
body_tube = build_body_tube()           # PVC tube reference (not for printing)
# Boattail + 4 aft triangular fins as ONE printable component
boattail = (
    build_boattail()
    .union(build_fin(0.0))
    .union(build_fin(90.0))
    .union(build_fin(180.0))
    .union(build_fin(270.0))
)
wing_top    = build_wing(90.0)
wing_bottom = build_wing(270.0)
wing_left   = build_wing(180.0)
wing_right  = build_wing(0.0)
# fins are now part of the `boattail` component (unioned above)
# motor pads are now integrated into each wing
airframe = (
    nose.union(body).union(boattail)
    .union(wing_top).union(wing_bottom)
    .union(wing_left).union(wing_right)
)


def export_stls(outdir: str = "stl") -> None:
    """Export nose/body/boattail and the combined airframe as STL files."""
    d = Path(outdir)
    d.mkdir(parents=True, exist_ok=True)
    for name, obj in [("nose", nose), ("body", body), ("boattail", boattail),
                      ("airframe", airframe)]:
        out = d / f"peregrine_{name}.stl"
        cq.exporters.export(obj, str(out))
        print(f"wrote {out}")


# ============================ Show ========================================
print(f"L = {L:.1f} mm   ->   nose={NOSE_LEN:.1f}  body={BODY_LEN:.1f}  "
      f"boattail={BT_LEN:.1f}  END_DIA={END_DIA:.1f}  TOTAL={TOTAL_LEN:.1f}")

if "show_object" in globals():
    show_object(nose,        name="1_Nose_PRINT",      options={"color": (230, 200, 200), "alpha": 0.55})
    show_object(body_tube,   name="2_PVC_REF",         options={"color": (180, 180, 180), "alpha": 0.25})
    show_object(boattail,    name="3_Boattail_PRINT",  options={"color": (200, 200, 230), "alpha": 0.55})
    show_object(wing_top,    name="4_Wing_Top",    options={"color": (220, 220, 220), "alpha": 0.55})
    show_object(wing_bottom, name="5_Wing_Bottom", options={"color": (220, 220, 220), "alpha": 0.55})
    show_object(wing_left,   name="6_Wing_Left",   options={"color": (220, 220, 220), "alpha": 0.55})
    show_object(wing_right,  name="7_Wing_Right_PRINT",  options={"color": (255, 140, 0), "alpha": 0.70})
    # Wing_Right is highlighted as the REFERENCE wing (carries the ref pad)
    # Fins merged into 3_Boattail_PRINT. Pads merged into each wing.
