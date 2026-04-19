"""VA-6 Peregrine — 7 printable parts as CadQuery models.

OML driven from the OpenVSP v16 file (designs/va6/VA6_Peregrine_v16.vsp3)
via the same station table used in va6_peregrine.py.

Parts (matching docs/design/VA6_PRINT_INTERFACES.md):
  1. Nose shell  — X: 0…230 mm, 3 mm wall, male joint ring at aft (134 mm OD × 15 mm)
  2. Body shell  — X: 230…480 mm, 3 mm wall, female recess fwd, male ring aft
  3. Aft shell   — X: 480…680 mm, 3 mm wall, female recess fwd, fin slots
  4-7. Fins Top/Bottom/Left/Right — NACA 0008, 80 mm chord × 160 mm span, with
       root tab that inserts into the aft shell slot

All parts shown transparent (alpha 0.55) for interior inspection.
Open in CQ-editor: File > Open > va6_printparts.py.
All dimensions in millimeters.
"""

import math
import cadquery as cq


# =========================== v16 OML parameters ===========================
TOTAL_LEN     = 680.0
BODY_DIA      = 141.3
NOSE_TIP_DIA  = 30.0
AFT_END_DIA   = 40.0

# VSP XSec stations (XLocPercent × TOTAL_LEN, radius mm)
OML_STATIONS = [
    (0.0,               NOSE_TIP_DIA / 2.0),
    (0.25 * TOTAL_LEN,  BODY_DIA / 2.0),
    (0.50 * TOTAL_LEN,  BODY_DIA / 2.0),
    (0.75 * TOTAL_LEN,  BODY_DIA / 2.0),
    (1.00 * TOTAL_LEN,  AFT_END_DIA / 2.0),
]


NOSE_END_X = 0.25 * TOTAL_LEN                        # 170 mm
AFT_LEN    = (0.25 * TOTAL_LEN) * (2.0 / 3.0)        # boattail = 2/3 of previous quarter ≈ 113 mm
BODY_END_X = TOTAL_LEN - AFT_LEN                     # 567 mm — boattail start
NOSE_TIP_R = NOSE_TIP_DIA / 2.0
AFT_END_R  = AFT_END_DIA / 2.0
BODY_R     = BODY_DIA / 2.0


def oml_radius(x: float) -> float:
    """Aero-profile radius at longitudinal station x.

    Nose (0..NOSE_END_X): quarter-ellipse — blunt, convex-out, tangent=0 at
    the body end. Matches the P1-SUN look rather than an S-curve.
    Body (NOSE_END_X..BODY_END_X): constant BODY_R.
    Boattail (BODY_END_X..AFT_END_X): linear taper to AFT_END_R."""
    if x <= 0.0:
        return NOSE_TIP_R
    if x <= NOSE_END_X:
        u = x / NOSE_END_X
        # quarter-ellipse: r = r_tip + (R - r_tip) * sqrt(1 - (1-u)^2)
        return NOSE_TIP_R + (BODY_R - NOSE_TIP_R) * math.sqrt(max(0.0, 1.0 - (1.0 - u) ** 2))
    if x <= BODY_END_X:
        return BODY_R
    if x <= TOTAL_LEN:
        u = (x - BODY_END_X) / (TOTAL_LEN - BODY_END_X)
        return BODY_R + (AFT_END_R - BODY_R) * u
    return AFT_END_R


# =========================== Print split stations =========================
NOSE_PRINT_END = 230.0
BODY_PRINT_END = 480.0
AFT_PRINT_END  = TOTAL_LEN  # 680

# Shell wall
WALL = 3.0

# Joint rings
RING_LEN         = 15.0
RING_MALE_OD     = 134.0     # per doc
RING_CLEARANCE   = 0.2       # per side
RING_FEMALE_ID   = RING_MALE_OD + 2 * RING_CLEARANCE  # 134.4

# Fins — moved forward so entire chord is on the cylindrical body (off the boattail)
FIN_CHORD       = 80.0
FIN_SPAN        = 160.0      # centerline to tip (pod sits at tip)
FIN_TC          = 0.08
FIN_LE_X        = 380.0      # was 530 (on boattail); now within body section
FIN_TE_X        = FIN_LE_X + FIN_CHORD   # 460
FIN_TAB_DEPTH   = 12.0
AIRFOIL_POINTS  = 36

# Motor pods (at wing tips, attached as part of the wing assembly)
POD_LEN         = 90.0
POD_MAX_DIA     = 32.0
POD_TIP_DIA     = 1.0
POD_AFT_DIA     = 22.4
POD_LE_X        = FIN_LE_X - 10.0        # pod nose just forward of fin LE
POD_OFFSET      = FIN_SPAN               # pod axis at fin tip radius

# Triangular landing legs on the boattail (cruciform, aligned with main wings)
LL_CHORD        = 70.0       # along body
LL_OUTBOARD     = 22.0       # apex radial protrusion past BODY_R
LL_TIP_CLIP     = 4.0        # flat-top trim
LL_TE_INSET     = 4.0        # TE inset from aft face
LL_ROOT_EMBED   = 3.0
LL_THICKNESS    = 4.0

# Resolution
PROFILE_SAMPLES = 60


# =========================== Shell builder ================================
def sample_profile(x_start: float, x_end: float, n: int) -> list[tuple[float, float]]:
    """Sample (x, oml_radius(x)) evenly across [x_start, x_end]."""
    return [(x_start + (x_end - x_start) * i / n,
             oml_radius(x_start + (x_end - x_start) * i / n))
            for i in range(n + 1)]


def revolved_solid(x_start: float, x_end: float,
                   r_outer_fn, r_inner_fn=None,
                   n: int = PROFILE_SAMPLES) -> cq.Workplane:
    """Revolve a profile from x_start to x_end. If r_inner_fn is given, build
    a hollow shell: outer profile from x_start to x_end at r_outer, then inner
    profile from x_end back to x_start at r_inner, then close."""
    outer = [(x_start + (x_end - x_start) * i / n,
              r_outer_fn(x_start + (x_end - x_start) * i / n))
             for i in range(n + 1)]

    if r_inner_fn is None:
        pts = [(x_start, 0.0)] + outer + [(x_end, 0.0)]
        return (cq.Workplane("XZ").polyline(pts).close()
                .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0)))

    inner = [(x_end - (x_end - x_start) * i / n,
              r_inner_fn(x_end - (x_end - x_start) * i / n))
             for i in range(n + 1)]
    pts = outer + inner
    return (cq.Workplane("XZ").polyline(pts).close()
            .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0)))


def shell_fn(x_start: float, x_end: float, wall: float = WALL) -> cq.Workplane:
    """Hollow shell between x_start..x_end, OML outer, OML-wall inner."""
    def r_out(x): return max(oml_radius(x), 0.5)
    def r_in(x):  return max(oml_radius(x) - wall, 0.1)
    return revolved_solid(x_start, x_end, r_out, r_in)


def make_tube(x_start: float, x_end: float, r_out: float, r_in: float) -> cq.Workplane:
    """Plain annular tube (constant OD/ID) between x_start and x_end."""
    outer = [(x_start, 0.0), (x_start, r_out), (x_end, r_out), (x_end, 0.0)]
    outer_solid = (cq.Workplane("XZ").polyline(outer).close()
                   .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0)))
    inner = [(x_start - 0.01, 0.0), (x_start - 0.01, r_in),
             (x_end + 0.01, r_in), (x_end + 0.01, 0.0)]
    inner_solid = (cq.Workplane("XZ").polyline(inner).close()
                   .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0)))
    return outer_solid.cut(inner_solid)


# =========================== Joint ring builders ==========================
def male_ring_at(x_face: float) -> cq.Workplane:
    """Hollow male ring extending FROM x_face to x_face + RING_LEN
    at OD = RING_MALE_OD, wall = WALL."""
    r_out = RING_MALE_OD / 2.0
    r_in  = r_out - WALL
    return make_tube(x_face, x_face + RING_LEN, r_out, r_in)


def female_recess_cutter(x_face: float) -> cq.Workplane:
    """Solid cylinder that, when cut from a shell, opens an internal recess
    of ID = RING_FEMALE_ID, depth = RING_LEN, starting at x_face."""
    r = RING_FEMALE_ID / 2.0
    return (
        cq.Workplane("YZ")
        .workplane(offset=x_face)
        .circle(r)
        .extrude(RING_LEN)
    )


# =========================== Airfoil ======================================
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


# =========================== 1. Nose shell ===============================
def build_nose() -> cq.Workplane:
    """Nose shell: hollow shell from x=0 (flat tip) to x=NOSE_PRINT_END.
    Male ring extending aft from x=NOSE_PRINT_END."""
    main = shell_fn(0.0, NOSE_PRINT_END)
    ring = male_ring_at(NOSE_PRINT_END)
    return main.union(ring)


# =========================== 2. Body shell ================================
def build_body() -> cq.Workplane:
    """Body shell: hollow shell x=NOSE_PRINT_END..BODY_PRINT_END (cylindrical).
    Female recess at fwd end, male ring at aft end, and four cruciform fin
    slots cut through the wall (wings now sit on the body, not the boattail)."""
    main = shell_fn(NOSE_PRINT_END, BODY_PRINT_END)
    main = main.cut(female_recess_cutter(NOSE_PRINT_END))

    fin_tab_thick = FIN_TC * FIN_CHORD * 0.9
    slot = (
        cq.Workplane("XY")
        .rect(FIN_CHORD + 0.4, fin_tab_thick + 0.4)
        .extrude(BODY_DIA)
        .translate((FIN_LE_X + FIN_CHORD / 2.0, 0, 0))
    )
    # Union all 4 cutters first — OCCT's cut-chain corrupts after ~2 cuts
    all_slots = slot
    for roll in (90.0, 180.0, 270.0):
        all_slots = all_slots.union(slot.rotate((0, 0, 0), (1, 0, 0), roll))
    main = main.cut(all_slots)

    ring = male_ring_at(BODY_PRINT_END)
    return main.union(ring)


# =========================== 3. Aft shell =================================
def build_aft() -> cq.Workplane:
    """Aft shell: hollow shell x=BODY_PRINT_END..AFT_PRINT_END (cyl tail +
    boattail). Female recess at fwd end. Four triangular landing-leg slots
    cut into the boattail in a cruciform pattern aligned with the main wings."""
    main = shell_fn(BODY_PRINT_END, AFT_PRINT_END)
    main = main.cut(female_recess_cutter(BODY_PRINT_END))

    # Landing-leg slots in boattail wall — union cutters first for stability
    ll_te_x = AFT_PRINT_END - LL_TE_INSET
    ll_le_x = ll_te_x - LL_CHORD
    ll_slot = (
        cq.Workplane("XY")
        .rect(LL_CHORD + 0.4, LL_THICKNESS + 0.4)
        .extrude(BODY_DIA)
        .translate(((ll_le_x + ll_te_x) / 2.0, 0, 0))
    )
    all_slots = ll_slot
    for roll in (90.0, 180.0, 270.0):
        all_slots = all_slots.union(ll_slot.rotate((0, 0, 0), (1, 0, 0), roll))
    main = main.cut(all_slots)

    return main


# =========================== Motor pod ====================================
def build_pod(roll_deg: float) -> cq.Workplane:
    """Motor pod: revolved profile (pointed nose → 32 mm cylinder → 22.4 mm
    aft taper), placed at POD_OFFSET out and rolled to the cruciform station."""
    stations = [
        (POD_LE_X,                  POD_TIP_DIA  / 2.0),
        (POD_LE_X + 0.25 * POD_LEN, POD_MAX_DIA  / 2.0),
        (POD_LE_X + 0.75 * POD_LEN, POD_MAX_DIA  / 2.0),
        (POD_LE_X + POD_LEN,        POD_AFT_DIA  / 2.0),
    ]
    pts = [(POD_LE_X, 0.0)] + stations + [(POD_LE_X + POD_LEN, 0.0)]
    pod = (
        cq.Workplane("XZ")
        .polyline(pts).close()
        .revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0))
    )
    return pod.translate((0, 0, POD_OFFSET)).rotate((0, 0, 0), (1, 0, 0), roll_deg)


# =========================== Triangular landing leg =======================
def build_landing_leg(roll_deg: float) -> cq.Workplane:
    """Trapezoidal (triangle with clipped apex) flat plate on boattail."""
    root_z = AFT_END_R - LL_ROOT_EMBED
    tip_z  = BODY_R + LL_OUTBOARD
    top_z  = tip_z - LL_TIP_CLIP
    ll_te_x = AFT_PRINT_END - LL_TE_INSET
    ll_le_x = ll_te_x - LL_CHORD
    t = (top_z - root_z) / (tip_z - root_z) if tip_z != root_z else 1.0
    x_clip_le = ll_le_x + t * (ll_te_x - ll_le_x)
    trap = [
        (ll_le_x,   root_z),
        (ll_te_x,   root_z),
        (ll_te_x,   top_z),
        (x_clip_le, top_z),
    ]
    leg = (
        cq.Workplane("XZ").polyline(trap).close()
        .extrude(LL_THICKNESS)
        .translate((0, -LL_THICKNESS / 2.0, 0))
    )
    return leg.rotate((0, 0, 0), (1, 0, 0), roll_deg)


# =========================== 4-7. Fins ====================================
def build_fin(roll_deg: float) -> cq.Workplane:
    """Straight rectangular fin extruded from root (centerline) to tip
    (160 mm out). Simple airfoil with a narrow root tab. The root tab is
    the portion that sits inside the aft-shell slot."""
    coords = naca_symmetric(FIN_TC, FIN_CHORD, AIRFOIL_POINTS)
    pts = [(x + FIN_LE_X, y) for (x, y) in coords]
    fin = (
        cq.Workplane("XY")
        .polyline(pts).close()
        .extrude(FIN_SPAN)
    )
    return fin.rotate((0, 0, 0), (1, 0, 0), roll_deg)


# =========================== Build & show ================================
def fin_with_pod(roll_deg: float) -> cq.Workplane:
    """A wing-and-pod assembly: the fin extruded radially, merged with its
    motor pod at the tip, rotated to the cruciform station."""
    return build_fin(roll_deg).union(build_pod(roll_deg))


nose        = build_nose()
body        = build_body()
aft         = build_aft()
fin_pod_t   = fin_with_pod(90.0)
fin_pod_b   = fin_with_pod(270.0)
fin_pod_l   = fin_with_pod(180.0)
fin_pod_r   = fin_with_pod(0.0)
leg_t       = build_landing_leg(90.0)
leg_b       = build_landing_leg(270.0)
leg_l       = build_landing_leg(180.0)
leg_r       = build_landing_leg(0.0)

if "show_object" in globals():
    opts = {"alpha": 0.55}
    show_object(nose, name="1_Nose", options={**opts, "color": (230, 200, 200)})
    show_object(body, name="2_Body", options={**opts, "color": (200, 230, 200)})
    show_object(aft,  name="3_Aft",  options={**opts, "color": (200, 200, 230)})
    show_object(fin_pod_t, name="4_WingPod_Top",    options={**opts, "color": (220, 220, 220)})
    show_object(fin_pod_b, name="5_WingPod_Bottom", options={**opts, "color": (220, 220, 220)})
    show_object(fin_pod_l, name="6_WingPod_Left",   options={**opts, "color": (220, 220, 220)})
    show_object(fin_pod_r, name="7_WingPod_Right",  options={**opts, "color": (220, 220, 220)})
    show_object(leg_t, name="8_Leg_Top",    options={**opts, "color": (240, 220, 180)})
    show_object(leg_b, name="9_Leg_Bottom", options={**opts, "color": (240, 220, 180)})
    show_object(leg_l, name="A_Leg_Left",   options={**opts, "color": (240, 220, 180)})
    show_object(leg_r, name="B_Leg_Right",  options={**opts, "color": (240, 220, 180)})
