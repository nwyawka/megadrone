"""Auto-generated CadQuery model fit from the Odin reference mesh.
Source: odin_drone_decimated.stl  (1.001 units long, axis=Z)
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
                options={"color": (180, 200, 220), "alpha": 0.6})
    if fin_top is not None:
        for nm, f in [("Fin_Top", fin_top), ("Fin_Bottom", fin_bottom),
                      ("Fin_Left", fin_left), ("Fin_Right", fin_right)]:
            show_object(f, name=nm, options={"color": (220, 220, 220), "alpha": 0.6})
