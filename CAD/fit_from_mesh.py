"""Fit parametric CadQuery primitives to the Odin drone mesh.

Approach:
  1. Load the decimated mesh (trimesh)
  2. Detect the longitudinal axis (longest bounding box extent)
  3. Slice at N longitudinal stations
  4. At each slice, separate loops into:
        - fuselage loop (biggest, near centerline)
        - fin/pod loops (outside the fuselage)
  5. Fit the fuselage profile as (z, r) points
  6. Detect fin planforms from the cross-section geometry
  7. Emit:
        - reference/odin_fit.json  (numeric fit data)
        - va6_fit.py               (CadQuery script using the fit data)

Units: the Sketchfab GLB is unitless (normalized ~1×1×1). We preserve
its coordinates in the fit data; a SCALE constant in va6_fit.py maps
to whatever target size you want (default: scale so longitudinal length
= 680 mm to match the v16 design).
"""

import json
import math
from pathlib import Path

import numpy as np
import trimesh


HERE = Path(__file__).parent
STL = HERE / "reference" / "odin_drone_decimated.stl"
FIT_JSON = HERE / "reference" / "odin_fit.json"
CQ_SCRIPT = HERE / "va6_fit.py"


# ============================ Load mesh ===================================
mesh = trimesh.load(STL)
print(f"loaded {len(mesh.vertices)}v, {len(mesh.faces)}f")
print(f"extents: {mesh.extents}")

# Longitudinal axis = longest extent axis
lon_axis = int(np.argmax(mesh.extents))          # 0=X, 1=Y, 2=Z
axes = [0, 1, 2]
radial_axes = [a for a in axes if a != lon_axis]
print(f"longitudinal axis: {'XYZ'[lon_axis]}")

# Extract vertices for convenience; orient so longitudinal is local Z
V = mesh.vertices.copy()
# rotate so longitudinal axis becomes local Z for processing
if lon_axis == 0:
    V = V[:, [1, 2, 0]]      # (x,y,z) -> (y,z,x)  so x_old is new z
elif lon_axis == 1:
    V = V[:, [0, 2, 1]]      # (x,y,z) -> (x,z,y)  so y_old is new z
# lon_axis == 2 already correct

z_min, z_max = V[:, 2].min(), V[:, 2].max()
lon_len = z_max - z_min
print(f"longitudinal length (unitless): {lon_len:.3f}")


# ============================ Slice and fit fuselage ======================
N_SLICES = 48
SLICE_TOL = lon_len / (N_SLICES * 4.0)       # half-thickness of each slab

fuselage_profile = []     # list of (z, r_fuselage)
fin_candidates   = []     # per-slice list of (z, max_radius, points_outside_fuse)

for i in range(N_SLICES):
    t = i / (N_SLICES - 1)
    z = z_min + t * lon_len
    # Select vertices within a thin slab around z
    mask = np.abs(V[:, 2] - z) < SLICE_TOL
    pts = V[mask][:, :2]    # xy in our rotated frame
    if len(pts) < 4:
        continue

    # Distance from longitudinal axis
    r = np.linalg.norm(pts, axis=1)

    # Fuselage radius: use the MODAL / low-percentile of radii — this is the
    # tightest "ring" of points that defines the body of revolution. Higher
    # radii are typically fin/pod extremities sticking out.
    r_sorted = np.sort(r)
    # Take radii from the 20th percentile: captures the body skin while
    # ignoring spurious small interior clutter
    r_fuse = np.percentile(r, 30)
    r_max  = r_sorted[-1]
    fuselage_profile.append((float(z), float(r_fuse)))
    fin_candidates.append((float(z), float(r_max), float(r_fuse)))

# Smooth the fuselage profile a bit with a rolling median
def rolling_median(data, window=3):
    out = []
    for i, (z, r) in enumerate(data):
        lo = max(0, i - window // 2)
        hi = min(len(data), i + window // 2 + 1)
        rs = [d[1] for d in data[lo:hi]]
        out.append((z, float(np.median(rs))))
    return out

fuselage_profile = rolling_median(fuselage_profile, window=3)


# Rebase z so forward tip = 0
fuselage_profile = [(z - z_min, r) for (z, r) in fuselage_profile]
fin_candidates   = [(z - z_min, rm, rf) for (z, rm, rf) in fin_candidates]


# ============================ Detect fin/pod stations =====================
# A fin is present where r_max >> r_fuse (blades extending out).
fin_threshold = 1.5
fin_present = [(z, rm, rf) for (z, rm, rf) in fin_candidates if rm > fin_threshold * rf]
if fin_present:
    fin_z_start = fin_present[0][0]
    fin_z_end   = fin_present[-1][0]
    fin_max_r   = max(rm for _, rm, _ in fin_present)
    fin_chord   = fin_z_end - fin_z_start
    print(f"fin region: z=[{fin_z_start:.3f}, {fin_z_end:.3f}]  chord={fin_chord:.3f}  tip_r={fin_max_r:.3f}")
else:
    fin_z_start = fin_z_end = fin_max_r = fin_chord = 0.0
    print("no fin region detected")


# ============================ Save fit data ===============================
fit = {
    "source": str(STL.name),
    "longitudinal_axis": "XYZ"[lon_axis],
    "longitudinal_length_unitless": lon_len,
    "fuselage_profile": fuselage_profile,          # [(z, r), ...] z starts at 0
    "fin": {
        "z_start": fin_z_start,
        "z_end":   fin_z_end,
        "chord":   fin_chord,
        "tip_radius": fin_max_r,
    },
}
FIT_JSON.parent.mkdir(parents=True, exist_ok=True)
with open(FIT_JSON, "w") as f:
    json.dump(fit, f, indent=2)
print(f"wrote {FIT_JSON}")


# ============================ Emit CadQuery script ========================
cq_code = f'''"""Auto-generated CadQuery model fit from the Odin reference mesh.
Source: {STL.name}  ({lon_len:.3f} units long, axis={"XYZ"[lon_axis]})
Scaling: longitudinal length mapped to TARGET_LEN_MM.
Rebuild via: python3 CAD/fit_from_mesh.py
"""

import json
from pathlib import Path

import cadquery as cq


FIT_JSON = Path(__file__).parent / "reference" / "odin_fit.json"
TARGET_LEN_MM = 680.0   # target physical length; adjust as desired

fit = json.loads(FIT_JSON.read_text())
scale = TARGET_LEN_MM / fit["longitudinal_length_unitless"]

# Scaled fuselage profile in mm, with x = longitudinal, r = radial
profile = [(z * scale, r * scale) for (z, r) in fit["fuselage_profile"]]

# Build a revolved fuselage from the fit profile
#   spline goes: axis at nose -> outer profile -> axis at aft -> close
wp = (
    cq.Workplane("XZ")
    .moveTo(profile[0][0], 0.0)
    .lineTo(profile[0][0], max(profile[0][1], 0.5))
    .spline([(x, r) for (x, r) in profile[1:]])
    .lineTo(profile[-1][0], 0.0)
    .close()
)
fuselage = wp.revolve(axisStart=(0, 0, 0), axisEnd=(1, 0, 0))


# Fin region (rectangular plate for now — refine with planform detection later)
fin_info = fit["fin"]
fin_le_x   = fin_info["z_start"] * scale
fin_te_x   = fin_info["z_end"]   * scale
fin_chord  = fin_info["chord"]   * scale
fin_tip_r  = fin_info["tip_radius"] * scale

if fin_chord > 1.0:
    FIN_TC = 0.08
    airfoil_pts = []
    n = 30
    for i in range(n + 1):
        xc = i / n
        yt = 5 * FIN_TC * (
            0.2969 * (xc ** 0.5) - 0.1260 * xc
            - 0.3516 * xc**2 + 0.2843 * xc**3 - 0.1015 * xc**4
        )
        airfoil_pts.append(((fin_le_x + xc * fin_chord), yt * fin_chord))
    for i in range(n - 1, 0, -1):
        xc = i / n
        yt = 5 * FIN_TC * (
            0.2969 * (xc ** 0.5) - 0.1260 * xc
            - 0.3516 * xc**2 + 0.2843 * xc**3 - 0.1015 * xc**4
        )
        airfoil_pts.append(((fin_le_x + xc * fin_chord), -yt * fin_chord))

    def build_fin(roll_deg):
        return (
            cq.Workplane("XY")
            .polyline(airfoil_pts).close()
            .extrude(fin_tip_r)
            .rotate((0, 0, 0), (1, 0, 0), roll_deg)
        )

    fin_top    = build_fin(90.0)
    fin_bottom = build_fin(270.0)
    fin_left   = build_fin(180.0)
    fin_right  = build_fin(0.0)
else:
    fin_top = fin_bottom = fin_left = fin_right = None


if "show_object" in globals():
    show_object(fuselage, name="Fuselage_fit",
                options={{"color": (180, 200, 220), "alpha": 0.6}})
    if fin_top is not None:
        for nm, f in [("Fin_Top", fin_top), ("Fin_Bottom", fin_bottom),
                      ("Fin_Left", fin_left), ("Fin_Right", fin_right)]:
            show_object(f, name=nm, options={{"color": (220, 220, 220), "alpha": 0.6}})
'''

CQ_SCRIPT.write_text(cq_code)
print(f"wrote {CQ_SCRIPT}")
print()
print("Summary:")
print(f"  fuselage samples: {len(fuselage_profile)}")
print(f"  target scale = {680.0 / lon_len:.1f} mm/unit")
print(f"  fuselage max r (scaled): {max(r for _, r in fuselage_profile) * 680.0 / lon_len:.1f} mm")
if fin_chord > 0:
    s = 680.0 / lon_len
    print(f"  fin chord (scaled): {fin_chord * s:.1f} mm")
    print(f"  fin tip radius (scaled): {fin_max_r * s:.1f} mm")
