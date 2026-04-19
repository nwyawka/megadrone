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

__version__ = "r2"

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
BLOCK_FORE_MARGIN     = 25.0 # block extends past LE (extra to encapsulate LE strip)
BLOCK_AFT_MARGIN      = 5.0  # block extends past TE
BLOCK_WIDTH           = 30.0 # Y-direction at roll=0 (widened +10 mm)
BLOCK_HEIGHT          = 4.0  # Z-direction (radial thickness above PVC tangent)
BLOCK_DEPTH_INTO_PVC  = 3.0  # block extends 3 mm below R before the PVC-cylinder cut
# 6 flush-mount M5 countersunk screws in a 3×2 grid (3 per side of wing midplane)
BLOCK_SCREW_DIA       = 5.5  # M5 clearance (5 mm thread + 0.5 mm clearance)
BLOCK_CSK_DIA         = 10.0 # M5 countersunk head (DIN 7991 / ISO 10642)
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

# Parabolic LE strip — separate nose piece swept along the wing LE hypotenuse
WING_LE_DEPTH         = 10.0                 # how far forward the parabolic nose extends
WING_LE_INBOARD_EXT   = 20.0                 # extend strip path inboard of LE root (toward tube)

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

# Antenna mount — saddle block on the PVC tube, aligned with reference wing
# (roll=0, +Z side), positioned halfway between the wing LE and nose-body
# junction. Same width as the wing base, 60 mm long. Flush mount on tube OD.
ANTENNA_BLOCK_LEN            = 60.0
ANTENNA_BLOCK_WIDTH          = BLOCK_WIDTH          # 30 mm
ANTENNA_BLOCK_HEIGHT         = BLOCK_HEIGHT
ANTENNA_BLOCK_DEPTH_INTO_PVC = BLOCK_DEPTH_INTO_PVC
ANTENNA_HOLE_DIA             = 6.0                  # placeholder — TBD
# 2 M5 countersunk mount screws on the block centerline, fore/aft of antenna hole
ANTENNA_SCREW_OFFSET_X       = 20.0                 # ± offset from block center

# NACA submerged inlet vent — printable plug that slots into a rectangular
# cutout in the PVC tube. Outer face flush with OD; ramp opens through the
# plug floor at the aft end so air enters the tube interior.
NACA_VENT_LEN    = 60.0        # target length along tube axis (scales template)
# Template proportions: 144 L × 114 W × 27 D  →  at L=60, W≈47.5, D≈11.3
NACA_TEMPLATE_STL = Path(__file__).parent / "reference" / "naca_template.stl"

# Custom flush-mount cooling vent — our own parametric design, shares the
# same PVC-tube slot as the NACA vent (an alternative print-it-yourself
# option). Ram-air scoop: small linear ramp from flush at the fore edge to
# an open aft end that feeds air into the airframe interior.
COOL_VENT_LEN            = NACA_VENT_LEN     # 60 mm — matches the slot
COOL_VENT_WIDTH          = 37.1              # matches slot footprint Y
COOL_VENT_THICK          = 14.0              # plug radial thickness (sets ramp depth)
COOL_VENT_SIDE_MARGIN_Y  = 3.0               # rim thickness on each Y side (channel wall)

# Inner lip — curved retaining wings that sit against the PVC tube ID. Wider
# than the slot in both X and Y so the vent can't pull back out. Installed
# from inside the tube before the boattail is attached.
COOL_VENT_LIP_THICK      = 2.0               # lip radial thickness
COOL_VENT_LIP_OVERHANG   = 5.0               # lip extends this far past plug in X on each side
COOL_VENT_LIP_ANG        = 50.0              # lip angular extent (deg), total — Y wing coverage

# Electronics/battery sled — lightweight 3-compartment tray. Slides into the
# PVC tube from the aft end; aft bulkhead is clamped by the boattail lip when
# the boattail is installed. Designed to fit a Bambu P1S bed (≤256 mm).
# Both sleds are the same length, sized to span between the nose lip and the
# boattail lip (the two tube flanges) with a small clearance gap between them.
# Total available = (BODY_END-LIP_LENGTH) - (NOSE_END+LIP_LENGTH) = 483 mm.
SLED_LEN                 = 240.0         # leaves ~3 mm gap between the two sleds
SLED_FLOOR_W             = 55.0          # narrowed so floor corners fit inside PVC ID
SLED_FLOOR_THICK         = 2.0
SLED_WALL_H              = 15.0
SLED_WALL_THICK          = 2.0
SLED_BULKHEAD_THICK      = 2.5
SLED_BULKHEAD_OD         = LIP_OD        # slip-fit to PVC ID (0.5 mm clearance/side)
SLED_BULKHEAD_HOLE_DIA   = 70.0          # central wiring/access hole (ring)
SLED_PAYLOAD_LEN         = 40.0          # fore compartment (accessory / RX)
SLED_BATTERY_LEN         = 160.0         # middle compartment (fits 155 mm LiPo)
# (electronics compartment length = SLED_LEN - payload - battery = 40 mm)

# Forward payload sled — same cross-section as main sled, single compartment.
# Fore end clamped by the nose lip; aft end faces the main sled across a gap.
PAYLOAD_SLED_LEN         = SLED_LEN

# 5000 mAh LiPo reference (4S, e.g. Tattu R-Line 155×49×45 mm).
# Centered on drone axis (Y=0, Z=0) for favorable CG.
BATTERY_LEN              = 155.0
BATTERY_WIDTH            = 49.0
BATTERY_HEIGHT           = 45.0
# Derived: floor top surface is one half-battery-height below axis, so the
# battery resting on the floor is centered on Z=0.
SLED_FLOOR_TOP_Z         = -BATTERY_HEIGHT / 2.0

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

    # -------- Flat triangular plate wing (r1 geometry) --------
    wing = (
        cq.Workplane("XZ")
        .polyline([
            (le_x, root_z),
            (te_x, root_z),
            (te_x, tip_z),
        ])
        .close()
        .extrude(WING_THICKNESS)
        .translate((0, +WING_THICKNESS / 2.0, 0))
    )

    # -------- Parabolic LE strip — swept along the wing hypotenuse --------
    # Path extensions:
    #   INBOARD: extend start below the LE root by WING_LE_INBOARD_EXT so the
    #            strip merges with the block/tube region cleanly.
    #   OUTBOARD: extend end all the way to the plate tip corner (te_x, tip_z)
    #            so the strip abuts the motor pad. Any overshoot past the pad's
    #            +X face (X=te_x) or pad outer Z is trimmed flat below.
    hyp_len = math.sqrt((te_x - le_x) ** 2 + (tip_z - root_z) ** 2)
    hyp_dir_x = (te_x - le_x) / hyp_len
    hyp_dir_z = (tip_z - root_z) / hyp_len
    # Forward-perpendicular unit vector (in XZ plane, normal to path, outward)
    n_x = -hyp_dir_z
    n_z = +hyp_dir_x

    pad_outer_z = R + WING_SPAN + PAD_DIA / 2.0   # = tip_z

    end_x_on_path = te_x
    end_z_on_path = tip_z

    start_x = le_x - WING_LE_INBOARD_EXT * hyp_dir_x
    start_z = root_z - WING_LE_INBOARD_EXT * hyp_dir_z

    le_start = cq.Vector(start_x, 0, start_z)
    le_end = cq.Vector(end_x_on_path, 0, end_z_on_path)
    path_edge = cq.Edge.makeLine(le_start, le_end)
    path_wp = cq.Workplane().newObject([path_edge])
    path_dir = (le_end - le_start).normalized()

    profile_plane = cq.Plane(le_start, cq.Vector(0, 1, 0), path_dir)

    T2 = WING_THICKNESS / 2.0
    LE_DEPTH = WING_LE_DEPTH
    n_par = 18
    profile_pts = []
    for i in range(n_par + 1):                                  # upper half, back→nose
        t = i / n_par
        x = T2 * (1.0 - t)
        y = LE_DEPTH * (1.0 - (x / T2) ** 2)
        profile_pts.append((x, y))
    for i in range(1, n_par + 1):                               # lower half, nose→back
        t = i / n_par
        x = -T2 * t
        y = LE_DEPTH * (1.0 - (x / T2) ** 2)
        profile_pts.append((x, y))

    le_strip = (
        cq.Workplane(profile_plane)
        .polyline(profile_pts).close()
        .sweep(path_wp)
    )
    wing = wing.union(le_strip)

    # -------- Root block (saddle): stadium planform (rounded fore/aft) with
    # curved bottom matching the PVC tube OD --------
    # Asymmetric margins so the forward extension wraps the LE strip.
    block_fore_x = le_x - BLOCK_FORE_MARGIN
    block_aft_x  = le_x + WING_CHORD + BLOCK_AFT_MARGIN
    block_len    = block_aft_x - block_fore_x
    block_cx     = 0.5 * (block_fore_x + block_aft_x)

    block_prism = (
        cq.Workplane("XY", origin=(block_cx, 0, R - BLOCK_DEPTH_INTO_PVC))
        .slot2D(block_len, BLOCK_WIDTH)
        .extrude(BLOCK_HEIGHT + BLOCK_DEPTH_INTO_PVC)
    )
    pvc_cyl = (
        cq.Workplane("YZ")
        .workplane(offset=block_fore_x - 10)
        .circle(R)
        .extrude(block_len + 20)
    )
    block = block_prism.cut(pvc_cyl)

    # Trim the block's aft end flat at X = te_x so it is coplanar with the
    # wing TE (and motor-pad +X face) — needed for printing with the TE down.
    # Box must be tall enough to fully overlap the block's Z range (≈54–62).
    aft_trim = (
        cq.Workplane("XY", origin=(te_x, 0, 0))
        .box(100, BLOCK_WIDTH * 4, 1000, centered=(False, True, True))
    )
    block = block.cut(aft_trim)
    wing = wing.union(block)

    # -------- 3×2 flush-mount countersunk screw grid (3 per side of wing) --------
    # Target the block TOP face specifically. Filter to +Z-normal faces first
    # (so NearestToPointSelector can't accidentally pick the curved -Z bottom
    # of the block, which drills the countersinks upside-down).
    block_top_ref = (wing_mid_x, 0, R + BLOCK_HEIGHT + 0.1)
    wing = (
        wing.faces("+Z").faces(cq.selectors.NearestToPointSelector(block_top_ref))
        .workplane(centerOption="CenterOfBoundBox")
        .rarray(BLOCK_SCREW_SPACING_X, BLOCK_SCREW_SPACING_Y, 3, 2)
        .cskHole(BLOCK_SCREW_DIA, cskDiameter=BLOCK_CSK_DIA,
                 cskAngle=BLOCK_CSK_ANGLE, depth=None)
    )

    # -------- Spanwise spar holes (3 × 4 mm at 25/50/70% chord, on Y=0) --------
    # Each hole is limited in Z so it ends INSIDE the triangular planform and
    # does NOT exit forward through the LE surface/strip.
    SPAR_Z_MARGIN = 3.0   # end hole this far before the LE hypotenuse
    for xf in SPAR_X_FRACS:
        x_hole = le_x + xf * WING_CHORD
        # LE hypotenuse at x_hole: z = root_z + (x_hole-le_x)/(te_x-le_x) × (tip_z-root_z)
        z_at_hyp = root_z + (x_hole - le_x) / (te_x - le_x) * (tip_z - root_z)
        spar_z_start = root_z - 1.0
        spar_z_end = z_at_hyp - SPAR_Z_MARGIN
        if spar_z_end <= spar_z_start:
            continue
        spar = (
            cq.Workplane("XY", origin=(x_hole, 0.0, spar_z_start))
            .circle(SPAR_DIA / 2.0)
            .extrude(spar_z_end - spar_z_start)
        )
        wing = wing.cut(spar)

    # -------- Motor pad at the tip --------
    wing = wing.union(_build_motor_pad_inline())

    # -------- Trim anything protruding inside the main tube OD --------
    # Cut the PVC cylinder from the full assembly so the LE strip's inboard
    # extension cannot poke into the tube.
    pvc_trim = (
        cq.Workplane("YZ")
        .workplane(offset=block_fore_x - 10)
        .circle(R)
        .extrude(block_len + 20)
    )
    wing = wing.cut(pvc_trim)

    # -------- Final flush-trim at X=te_x --------
    # LE strip is swept to the plate tip corner; anything overshooting the
    # pad's +X face gets cut flat so the outboard end is flush with the pad.
    wing_aft_trim = (
        cq.Workplane("XY", origin=(te_x, 0, 0))
        .box(200, 1000, 1000, centered=(False, True, True))
    )
    wing = wing.cut(wing_aft_trim)

    # Trim anything protruding past the pad's outer Z (top of pad).
    wing_top_trim = (
        cq.Workplane("XY", origin=(0, 0, pad_outer_z))
        .box(2000, 1000, 500, centered=(True, True, False))
    )
    wing = wing.cut(wing_top_trim)

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


def build_antenna_mount(roll_deg: float = 0.0) -> cq.Workplane:
    """Antenna mount — stadium saddle block flush-mounted on PVC tube.
    Curved bottom matches tube OD. Positioned halfway between the reference
    wing LE and the nose-body junction, aligned (same roll) with wing_right."""
    wing_mid_x = WING_POS_FRAC * TOTAL_LEN
    le_x_wing = wing_mid_x - WING_CHORD / 2.0
    cx = 0.5 * (le_x_wing + NOSE_END)
    fore_x = cx - ANTENNA_BLOCK_LEN / 2.0

    block_prism = (
        cq.Workplane("XY", origin=(cx, 0, R - ANTENNA_BLOCK_DEPTH_INTO_PVC))
        .slot2D(ANTENNA_BLOCK_LEN, ANTENNA_BLOCK_WIDTH)
        .extrude(ANTENNA_BLOCK_HEIGHT + ANTENNA_BLOCK_DEPTH_INTO_PVC)
    )
    pvc_cyl = (
        cq.Workplane("YZ")
        .workplane(offset=fore_x - 10)
        .circle(R)
        .extrude(ANTENNA_BLOCK_LEN + 20)
    )
    block = block_prism.cut(pvc_cyl)

    # Placeholder antenna through-hole (radial/Z direction)
    hole = (
        cq.Workplane("XY", origin=(cx, 0, R - ANTENNA_BLOCK_DEPTH_INTO_PVC - 1))
        .circle(ANTENNA_HOLE_DIA / 2.0)
        .extrude(ANTENNA_BLOCK_HEIGHT + ANTENNA_BLOCK_DEPTH_INTO_PVC + 2)
    )
    block = block.cut(hole)

    # 2 M5 countersunk mount screws on the block top centerline (Y=0),
    # symmetric about the antenna hole. Filter to +Z faces so NearestToPoint
    # picks the block top (not the curved PVC-facing bottom).
    antenna_top_ref = (cx, 0, R + ANTENNA_BLOCK_HEIGHT + 0.1)
    block = (
        block.faces("+Z").faces(cq.selectors.NearestToPointSelector(antenna_top_ref))
        .workplane(centerOption="CenterOfBoundBox")
        .pushPoints([(-ANTENNA_SCREW_OFFSET_X, 0.0),
                     (+ANTENNA_SCREW_OFFSET_X, 0.0)])
        .cskHole(BLOCK_SCREW_DIA, cskDiameter=BLOCK_CSK_DIA,
                 cskAngle=BLOCK_CSK_ANGLE, depth=None)
    )

    return block.rotate((0, 0, 0), (1, 0, 0), roll_deg)


def build_cool_vent(roll_deg: float = 180.0) -> cq.Workplane:
    """Custom flush-mount cooling vent — small ram-air scoop. Internal ramp
    starts flush at the fore edge (no lip), deepens linearly as it goes aft,
    and breaks through the plug floor at the aft end. The open aft feeds
    incoming air into the tube interior to cool the electronics and battery.
    Side rails (SIDE_MARGIN_Y on each edge) retain the plug's slip-fit
    footprint for the existing PVC slot."""
    wing_mid_x = WING_POS_FRAC * TOTAL_LEN
    le_x_wing = wing_mid_x - WING_CHORD / 2.0
    cx = 0.5 * (le_x_wing + NOSE_END)

    L = COOL_VENT_LEN
    W = COOL_VENT_WIDTH
    T = COOL_VENT_THICK
    CHANNEL_Y = W - 2 * COOL_VENT_SIDE_MARGIN_Y

    # Plug blank — rectangular prism, outer surface will be trimmed to PVC OD
    plug = (
        cq.Workplane("XY", origin=(cx, 0, R - T))
        .rect(L, W)
        .extrude(T + 2)                         # extra 2 mm above OD for clean trim
    )
    # Conform outer face to PVC OD curvature (same strategy as the NACA vent)
    pvc_cyl = (
        cq.Workplane("YZ")
        .workplane(offset=cx - L / 2 - 5)
        .circle(R)
        .extrude(L + 10)
    )
    plug = plug.intersect(pvc_cyl)

    # -------- Inner retaining lip (before ramp cut, so the cut clears it too) --------
    # Curved annular-segment wings at r = LIP_R. Retaining ledge extends past
    # the plug in X only on the FORE end (aft end is flush with plug so it
    # doesn't obstruct the airflow exit); wider in Y both sides.
    lip_fore_x = cx - L / 2 - COOL_VENT_LIP_OVERHANG
    lip_aft_x  = cx + L / 2                      # flush with plug aft (no aft ledge)
    lip_profile = (
        cq.Workplane("XZ")
        .moveTo(lip_fore_x, LIP_R - COOL_VENT_LIP_THICK)
        .lineTo(lip_aft_x,  LIP_R - COOL_VENT_LIP_THICK)
        .lineTo(lip_aft_x,  LIP_R)
        .lineTo(lip_fore_x, LIP_R)
        .close()
    )
    lip = lip_profile.revolve(
        angleDegrees=COOL_VENT_LIP_ANG,
        axisStart=(0, 0, 0),
        axisEnd=(1, 0, 0),
    ).rotate((0, 0, 0), (1, 0, 0), -COOL_VENT_LIP_ANG / 2.0)

    # Union the plug + lip BEFORE cutting the ramp so the ramp void punches
    # through both the plug and the lip at the aft opening.
    plug = plug.union(lip)

    # Ramp void — single continuous linear ramp. 4-vertex polygon in XZ
    # extruded in Y across the channel. Floor slopes uniformly from flush at
    # the fore edge down through the plug floor at the aft edge, producing
    # one open aft mouth into the airframe interior.
    ramp_profile = [
        (cx - L / 2 - 1.0, R + 1.0),            # fore-top  (overshoot OD)
        (cx + L / 2 + 1.0, R + 1.0),            # aft-top
        (cx + L / 2 + 1.0, R - T - 1.0),        # aft-bottom (through floor → open aft)
        (cx - L / 2 - 1.0, R + 0.01),           # fore-bottom (just above OD → flush)
    ]
    ramp_void = (
        cq.Workplane("XZ")
        .polyline(ramp_profile)
        .close()
        .extrude(CHANNEL_Y)
        .translate((0, +CHANNEL_Y / 2.0, 0))    # CQ's XZ extrudes in -Y; shift +Y/2 to center
    )
    plug = plug.cut(ramp_void)

    return plug.rotate((0, 0, 0), (1, 0, 0), roll_deg)


def build_sled() -> cq.Workplane:
    """Lightweight 3-compartment electronics/battery sled. Slides into the PVC
    tube from the aft end; aft bulkhead is clamped by the boattail lip when
    the boattail is installed. Compartments (fore → aft):
        payload bay | battery bay | flight-controller/ESC bay"""
    sled_aft_x = BODY_END - LIP_LENGTH
    sled_fore_x = sled_aft_x - SLED_LEN
    sled_cx = 0.5 * (sled_fore_x + sled_aft_x)

    # Floor positioned so the battery resting on it is centered on Z=0 (on the
    # drone's centerline — good CG). Floor width narrowed so the corners fit
    # inside the PVC ID envelope.
    floor_top_z = SLED_FLOOR_TOP_Z
    floor_bot_z = floor_top_z - SLED_FLOOR_THICK
    wall_top_z  = floor_top_z + SLED_WALL_H

    # Floor plate
    floor = (
        cq.Workplane("XY", origin=(sled_cx, 0, floor_bot_z))
        .box(SLED_LEN, SLED_FLOOR_W, SLED_FLOOR_THICK,
             centered=(True, True, False))
    )
    # Side walls (2)
    wall_cy = SLED_FLOOR_W / 2 + SLED_WALL_THICK / 2
    left_wall = (
        cq.Workplane("XY", origin=(sled_cx, -wall_cy, floor_top_z))
        .box(SLED_LEN, SLED_WALL_THICK, SLED_WALL_H,
             centered=(True, True, False))
    )
    right_wall = (
        cq.Workplane("XY", origin=(sled_cx, +wall_cy, floor_top_z))
        .box(SLED_LEN, SLED_WALL_THICK, SLED_WALL_H,
             centered=(True, True, False))
    )
    sled = floor.union(left_wall).union(right_wall)

    # Internal dividers (2) — separate 3 compartments
    div_xs = [
        sled_fore_x + SLED_PAYLOAD_LEN,
        sled_fore_x + SLED_PAYLOAD_LEN + SLED_BATTERY_LEN,
    ]
    for dx in div_xs:
        divider = (
            cq.Workplane("XY", origin=(dx, 0, floor_top_z))
            .box(SLED_WALL_THICK, SLED_FLOOR_W, SLED_WALL_H,
                 centered=(True, True, False))
        )
        sled = sled.union(divider)

    # Bulkhead rings (fore & aft) — slip-fit to PVC ID, open center for wiring
    for x_bh, is_aft in [(sled_fore_x, False), (sled_aft_x, True)]:
        x_start = x_bh - SLED_BULKHEAD_THICK if is_aft else x_bh
        bh = (
            cq.Workplane("YZ")
            .workplane(offset=x_start)
            .circle(SLED_BULKHEAD_OD / 2.0)
            .circle(SLED_BULKHEAD_HOLE_DIA / 2.0)
            .extrude(SLED_BULKHEAD_THICK)
        )
        sled = sled.union(bh)

    return sled


def build_payload_sled() -> cq.Workplane:
    """Forward payload sled — identical cross-section to the main sled, single
    compartment. Fore bulkhead clamps against the nose lip aft face; aft end
    faces the main sled across a small clearance gap. Same length as the
    main sled."""
    sled_fore_x = NOSE_END + LIP_LENGTH       # clamped by nose lip aft face
    sled_aft_x  = sled_fore_x + PAYLOAD_SLED_LEN
    sled_cx = 0.5 * (sled_fore_x + sled_aft_x)

    floor_top_z = SLED_FLOOR_TOP_Z
    floor_bot_z = floor_top_z - SLED_FLOOR_THICK

    floor = (
        cq.Workplane("XY", origin=(sled_cx, 0, floor_bot_z))
        .box(PAYLOAD_SLED_LEN, SLED_FLOOR_W, SLED_FLOOR_THICK,
             centered=(True, True, False))
    )
    wall_cy = SLED_FLOOR_W / 2 + SLED_WALL_THICK / 2
    left_wall = (
        cq.Workplane("XY", origin=(sled_cx, -wall_cy, floor_top_z))
        .box(PAYLOAD_SLED_LEN, SLED_WALL_THICK, SLED_WALL_H,
             centered=(True, True, False))
    )
    right_wall = (
        cq.Workplane("XY", origin=(sled_cx, +wall_cy, floor_top_z))
        .box(PAYLOAD_SLED_LEN, SLED_WALL_THICK, SLED_WALL_H,
             centered=(True, True, False))
    )
    sled = floor.union(left_wall).union(right_wall)

    for x_bh, is_aft in [(sled_fore_x, False), (sled_aft_x, True)]:
        x_start = x_bh - SLED_BULKHEAD_THICK if is_aft else x_bh
        bh = (
            cq.Workplane("YZ")
            .workplane(offset=x_start)
            .circle(SLED_BULKHEAD_OD / 2.0)
            .circle(SLED_BULKHEAD_HOLE_DIA / 2.0)
            .extrude(SLED_BULKHEAD_THICK)
        )
        sled = sled.union(bh)

    return sled


def build_battery() -> cq.Workplane:
    """Reference 4S 5000 mAh LiPo (155×49×45 mm). Sits on the sled floor in
    the middle (battery) compartment."""
    sled_aft_x = BODY_END - LIP_LENGTH
    sled_fore_x = sled_aft_x - SLED_LEN
    bay_fore_x = sled_fore_x + SLED_PAYLOAD_LEN + SLED_WALL_THICK / 2.0
    bay_aft_x  = sled_fore_x + SLED_PAYLOAD_LEN + SLED_BATTERY_LEN - SLED_WALL_THICK / 2.0
    battery_cx = 0.5 * (bay_fore_x + bay_aft_x)
    # Battery sits on sled floor — floor top is chosen so the battery is
    # centered on Z=0 (drone centerline) for favorable CG.
    return (
        cq.Workplane("XY", origin=(battery_cx, 0, SLED_FLOOR_TOP_Z))
        .box(BATTERY_LEN, BATTERY_WIDTH, BATTERY_HEIGHT, centered=(True, True, False))
    )


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
antenna_mount = build_antenna_mount(0.0)        # aligned with wing_right (+Z)
# Internal sleds, battery, and cooling vents rotated together 45° about +X
# so they sit tilted relative to the airframe. Angle rolls from the base
# orientation (sleds: floor-down, vent base: on -Z) by this much.
INTERNAL_ROLL_DEG = 45.0
# Four cooling vents spaced 90° around the body, starting from the base
# -Z-side vent rotated by INTERNAL_ROLL_DEG (so angles: 225°, 315°, 45°, 135°).
COOL_VENT_ROLL_ANGLES = [INTERNAL_ROLL_DEG + 180.0 + 90.0 * i for i in range(4)]
cool_vents = [build_cool_vent(a) for a in COOL_VENT_ROLL_ANGLES]
# Notch the reference PVC tube at each of the 4 vent locations.
_notch_cx = 0.5 * ((WING_POS_FRAC * TOTAL_LEN - WING_CHORD / 2) + NOSE_END)
_notch_lx = COOL_VENT_LEN + 1.0
_notch_ly = COOL_VENT_WIDTH + 1.0
for _angle in COOL_VENT_ROLL_ANGLES:
    _notch_box = (
        cq.Workplane("XY", origin=(_notch_cx, 0, -R - 1.0))
        .box(_notch_lx, _notch_ly, PVC_WALL + 3.0, centered=(True, True, False))
        .rotate((0, 0, 0), (1, 0, 0), _angle - 180.0)   # base notch is on -Z (roll=180°)
    )
    body_tube = body_tube.cut(_notch_box)
sled          = build_sled().rotate((0, 0, 0), (1, 0, 0), INTERNAL_ROLL_DEG)
payload_sled  = build_payload_sled().rotate((0, 0, 0), (1, 0, 0), INTERNAL_ROLL_DEG)
battery       = build_battery().rotate((0, 0, 0), (1, 0, 0), INTERNAL_ROLL_DEG)  # 5000 mAh LiPo reference
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
    show_object(antenna_mount, name="8_Antenna_Mount_PRINT", options={"color": (230, 230, 180), "alpha": 0.70})
    for _i, _v in enumerate(cool_vents):
        show_object(_v, name=f"9_Cool_Vent_{_i+1}_PRINT", options={"color": (130, 220, 170), "alpha": 0.70})
    show_object(sled,          name="10_Sled_PRINT",         options={"color": (230, 200, 230), "alpha": 0.55})
    show_object(payload_sled,  name="11_Payload_Sled_PRINT", options={"color": (200, 230, 230), "alpha": 0.55})
    show_object(battery,       name="12_Battery_5Ah_REF",    options={"color": (80, 80, 80),    "alpha": 0.85})
    # Wing_Right is highlighted as the REFERENCE wing (carries the ref pad)
    # Fins merged into 3_Boattail_PRINT. Pads merged into each wing.
