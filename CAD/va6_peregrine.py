"""VA-6 Peregrine interceptor — parametric CadQuery model.

Dimensions extracted directly from the authoritative OpenVSP model
`designs/va6/VA6_Peregrine_v16.vsp3` (see CAD/parse_vsp3.py).

Fuselage: 680 mm total, 141.3 mm max diameter
  - nose        0-170 mm   (elliptical, 30 mm flat tip)
  - body        170-510 mm (cylindrical, 141.3 mm dia)
  - boattail    510-680 mm (taper to 40 mm aft face)
Main wings (×4 cruciform): 80 mm chord × 160 mm span, straight rectangular,
  root on centerline (inside fuselage), tip co-located with motor pod at
  y=160 (or z=160). LE at X = 530 mm.
Motor pods (×4): 90 mm long, 32 mm max diameter. Pointed nose cone
  (first 25%), cylinder (middle 50%), aft taper to 22.4 mm (last 25%).
  Axis passes through fin tip. X = 520 mm.
Motor: 2207 2750KV FPV outrunner (28 mm OD) per VA6_PEREGRINE_SYSTEM_PLAN.md.
  NOTE: sustained power budget suggests a 28xx-class motor is more appropriate
  for the mission profile; the 32 mm pod can accept either.

Open in CQ-editor: File > Open > va6_peregrine.py.
All dimensions in millimeters.
"""

import math
import cadquery as cq


# ============================ Fuselage (from VSP v16) =====================
TOTAL_LEN         = 680.0
BODY_DIA          = 141.3
NOSE_TIP_DIA      = 30.0      # seeker window flat at forward tip
AFT_END_DIA       = 40.0

# Section boundaries (VSP XSec XLocPercent × TOTAL_LEN)
NOSE_END_X        = 0.25 * TOTAL_LEN   # 170 mm
BODY_END_X        = 0.75 * TOTAL_LEN   # 510 mm  (= boattail start)
AFT_END_X         = TOTAL_LEN          # 680 mm


# ============================ Main wings (from VSP v16) ==================
FIN_CHORD         = 80.0
FIN_SPAN_TOTAL    = 160.0     # root on centerline, tip at radius 160 mm
FIN_LE_X          = 530.0     # VSP X_Location for each wing
FIN_TC            = 0.08      # NACA 0008 (assumed; VSP XSec airfoil = file-based)


# ============================ Motor pods (from VSP v16) ==================
POD_LEN           = 90.0
POD_MAX_DIA       = 32.0
POD_TIP_DIA       = 1.0       # ~pointed forward nose
POD_AFT_DIA       = 22.4      # aft taper
POD_LE_X          = 520.0     # VSP X_Location
POD_OFFSET        = 160.0     # radial offset of pod axis (= fin tip)


# ============================ Motor (physical — informational only) ======
MOTOR_OD          = 28.0      # 2207 FPV; pod accepts up to 32 mm
PROP_DIA          = 127.0     # 5 in
PROP_THICK        = 2.5


# ============================ Landing fins on boattail ====================
LF_CHORD          = 70.0
LF_OUTBOARD       = 25.0
LF_TE_INSET       = 5.0
LF_THICKNESS      = 4.0
LF_ROOT_EMBED     = 3.0
LF_TIP_CLIP       = 5.0


# ============================ Options =====================================
HALF_CUT          = False


# Resolution
FUS_SPLINE_SEGS   = 50
POD_SPLINE_SEGS   = 30
AIRFOIL_POINTS    = 36


# ============================ Derived =====================================
BODY_R            = BODY_DIA / 2.0
NOSE_TIP_R        = NOSE_TIP_DIA / 2.0
AFT_END_R         = AFT_END_DIA / 2.0
POD_R             = POD_MAX_DIA / 2.0
POD_TIP_R         = POD_TIP_DIA / 2.0
POD_AFT_R         = POD_AFT_DIA / 2.0

# Pod longitudinal stations (VSP XSec XLocPercent × POD_LEN, offset by POD_LE_X)
POD_NOSE_END_X    = POD_LE_X + 0.25 * POD_LEN
POD_BODY_END_X    = POD_LE_X + 0.75 * POD_LEN
POD_AFT_X         = POD_LE_X + POD_LEN


# ============================ Fuselage profile ============================
def fuselage_profile_points() -> list[tuple[float, float]]:
    """Build the outer XZ profile: spline-smoothed between XSec stations.
    Stations match VSP: 0% (tip), 25%, 50%, 75%, 100% (aft)."""
    stations = [
        (0.0,           NOSE_TIP_R),                # flat tip at x=0, r=15
        (NOSE_END_X,    BODY_R),                    # end of nose, r=70.65
        (0.5 * TOTAL_LEN, BODY_R),                  # mid body
        (BODY_END_X,    BODY_R),                    # end of body / start boattail
        (AFT_END_X,     AFT_END_R),                 # aft face
    ]

    # Interpolate smooth spline through the key points
    # (spline has monotone X so we can just sample parametrically)
    pts: list[tuple[float, float]] = []
    for i in range(len(stations) - 1):
        x0, r0 = stations[i]
        x1, r1 = stations[i + 1]
        n = FUS_SPLINE_SEGS // (len(stations) - 1)
        for j in range(n + 1):
            if i > 0 and j == 0:
                continue
            t = j / n
            # Cosine ease for nose section; linear for the rest
            if i == 0:
                # Nose: quarter-ellipse from (0, tip_r) to (NOSE_END_X, body_r)
                frac = 1.0 - t
                r = r1 + (r0 - r1) * frac                          # fallback linear
                # Actual ellipse: (x/NOSE_END_X)² + ((BODY_R - r)/(BODY_R - tip_r))² = 1  (rotated)
                # Parameterize via angle 0..π/2 where angle=0 at tip, π/2 at body:
                ang = 0.5 * math.pi * t
                x = x0 + (x1 - x0) * math.sin(ang)
                # Radius uses same angular sweep: ellipse from r0 to r1
                r = r0 + (r1 - r0) * (1.0 - math.cos(ang))
            else:
                x = x0 + (x1 - x0) * t
                r = r0 + (r1 - r0) * t
            pts.append((x, r))
    return pts


def build_fuselage(angle_deg: float = 360.0) -> cq.Workplane:
    profile = fuselage_profile_points()

    # Start on axis at forward tip, up to flat tip face, around profile,
    # down to axis at aft face, close.
    wp = cq.Workplane("XZ").moveTo(0.0, 0.0).lineTo(0.0, NOSE_TIP_R)
    wp = wp.spline(profile[1:])   # spline through outer surface
    wp = wp.lineTo(AFT_END_X, 0.0).close()
    return wp.revolve(angleDegrees=angle_deg, axisStart=(0, 0, 0), axisEnd=(1, 0, 0))


# ============================ Airfoil for wings ===========================
def naca_symmetric(t: float, chord: float, n: int) -> list[tuple[float, float]]:
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


# ============================ Main wing ===================================
def build_wing(roll_deg: float) -> cq.Workplane:
    """Straight rectangular NACA 0008 wing. Root on centerline (extends from
    y=0 to y=FIN_SPAN_TOTAL), so the portion inside body radius is unioned
    with the fuselage. Per-wing roll about +X orients the cruciform."""
    coords = naca_symmetric(FIN_TC, FIN_CHORD, AIRFOIL_POINTS)
    pts = [(x + FIN_LE_X, y) for (x, y) in coords]
    fin = (
        cq.Workplane("XY")
        .polyline(pts).close()
        .extrude(FIN_SPAN_TOTAL)
    )
    return fin.rotate((0, 0, 0), (1, 0, 0), roll_deg)


# ============================ Motor pod (body-of-revolution + prop) =======
def build_pod(roll_deg: float) -> cq.Workplane:
    """Pod outer surface from VSP XSecs:
       tip (1 mm) -> 25% (32 mm) -> 50% (32 mm) -> 75% (32 mm) -> aft (22.4 mm)
    Rotated around pod's own X axis (revolve), then translated out to the
    fin-tip radius and roll-rotated to place at the 4 cruciform stations."""
    profile = [
        (POD_LE_X,        POD_TIP_R),
        (POD_NOSE_END_X,  POD_R),
        (POD_BODY_END_X,  POD_R),
        (POD_AFT_X,       POD_AFT_R),
    ]
    wp = (
        cq.Workplane("XZ")
        .moveTo(POD_LE_X, 0.0)
        .lineTo(POD_LE_X, POD_TIP_R)
        .spline(profile[1:])
        .lineTo(POD_AFT_X, 0.0)
        .close()
        .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0))
    )

    # Prop disc at aft face
    prop = (
        cq.Workplane("YZ")
        .workplane(offset=POD_AFT_X + 2.0)
        .circle(PROP_DIA / 2.0)
        .extrude(PROP_THICK)
    )

    return (
        wp.union(prop)
        .translate((0, 0, POD_OFFSET))
        .rotate((0, 0, 0), (1, 0, 0), roll_deg)
    )


# ============================ Landing fin (trapezoid, clipped tip) ========
LF_TE_X = AFT_END_X - LF_TE_INSET
LF_LE_X = LF_TE_X - LF_CHORD


def build_landing_fin(roll_deg: float) -> cq.Workplane:
    root_z = AFT_END_R - LF_ROOT_EMBED
    tip_z  = BODY_R + LF_OUTBOARD
    top_z  = tip_z - LF_TIP_CLIP
    t = (top_z - root_z) / (tip_z - root_z) if tip_z != root_z else 1.0
    x_clip_le = LF_LE_X + t * (LF_TE_X - LF_LE_X)
    trap = [
        (LF_LE_X, root_z),
        (LF_TE_X, root_z),
        (LF_TE_X, top_z),
        (x_clip_le, top_z),
    ]
    fin = (
        cq.Workplane("XZ")
        .polyline(trap).close()
        .extrude(LF_THICKNESS)
        .translate((0, -LF_THICKNESS / 2.0, 0))
    )
    return fin.rotate((0, 0, 0), (1, 0, 0), roll_deg)


# ============================ Assembly ====================================
ROLLS = (0.0, 90.0, 180.0, 270.0)


def _drop_null_solids(wp: cq.Workplane) -> cq.Workplane:
    v = wp.val()
    if not hasattr(v, "Solids"):
        return wp
    good = [s for s in v.Solids() if s.Volume() > 1e-3]
    if not good:
        return wp
    if len(good) == 1:
        return cq.Workplane(obj=good[0])
    return cq.Workplane(obj=cq.Compound.makeCompound(good))


def build_airframe() -> cq.Workplane:
    af = build_fuselage()
    for roll in ROLLS:
        af = _drop_null_solids(af.union(build_wing(roll)))
    for roll in ROLLS:
        af = _drop_null_solids(af.union(build_landing_fin(roll)))
    return af


def build_pods() -> cq.Workplane:
    pods = build_pod(ROLLS[0])
    for roll in ROLLS[1:]:
        pods = _drop_null_solids(pods.union(build_pod(roll)))
    return pods


# ============================ Half-cut (for interior view) ================
def half_cut(wp: cq.Workplane) -> cq.Workplane:
    v = wp.val()
    bb = v.BoundingBox()
    L = max(bb.xlen, bb.ylen, bb.zlen) * 3.0
    keeper = (
        cq.Workplane("XY")
        .box(2 * L, L, 2 * L)
        .translate((bb.center.x, L / 2.0, bb.center.z))
    )
    return wp.intersect(keeper)


def build_airframe_halfcut() -> cq.Workplane:
    fus_half = build_fuselage(angle_deg=180.0).rotate((0, 0, 0), (1, 0, 0), 180)
    parts = [fus_half.val()]
    for roll in ROLLS:
        parts.append(half_cut(build_wing(roll)).val())
    for roll in ROLLS:
        parts.append(half_cut(build_landing_fin(roll)).val())
    solids = []
    for p in parts:
        if hasattr(p, "Solids"):
            solids.extend([s for s in p.Solids() if s.Volume() > 1e-3])
        elif p.Volume() > 1e-3:
            solids.append(p)
    return cq.Workplane(obj=cq.Compound.makeCompound(solids))


def build_pods_halfcut() -> cq.Workplane:
    parts = []
    for roll in ROLLS:
        parts.append(half_cut(build_pod(roll)).val())
    solids = []
    for p in parts:
        if hasattr(p, "Solids"):
            solids.extend([s for s in p.Solids() if s.Volume() > 1e-3])
        elif p.Volume() > 1e-3:
            solids.append(p)
    return cq.Workplane(obj=cq.Compound.makeCompound(solids))


if HALF_CUT:
    airframe = build_airframe_halfcut()
    pods = build_pods_halfcut()
else:
    airframe = build_airframe()
    pods = build_pods()


if "show_object" in globals():
    show_object(airframe, name="airframe")
    show_object(pods, name="motor_pods")
