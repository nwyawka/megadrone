"""Slice each Odin part into Z-station cross-sections and write a CadQuery
lofted-solid model that matches the mesh.

Pipeline:
  1. Load each odin_part_NN.stl with trimesh
  2. Slice at N stations along Z (longitudinal axis)
  3. For each slice: extract the largest closed polygon, resample to M points
  4. Emit CAD/va6_odin.py — lofts through all cross-sections to produce a
     parametric solid. Edit params at top (scale, station count) to tweak.
"""

import json
import math
from pathlib import Path

import numpy as np
import trimesh


HERE = Path(__file__).parent
PARTS_DIR = HERE / "reference" / "parts"
OUT_JSON  = HERE / "reference" / "odin_fit.json"
OUT_CQ    = HERE / "va6_odin.py"

N_STATIONS      = 18          # cross-sections per part
M_POINTS        = 40          # points per polygon (after resampling)
TARGET_LEN_MM   = 680.0       # scale target (Odin full length)
SOURCE_LEN      = 1.001       # measured in the GLB
SCALE           = TARGET_LEN_MM / SOURCE_LEN


def resample_polygon(pts: np.ndarray, n: int) -> np.ndarray:
    """Angular resampling: each output point sits at a fixed angle (i*2π/n)
    measured from the polygon's centroid. Consistent angular ordering across
    sections is critical for clean loft — keeps points aligned so the lofted
    surface does not twist between slices."""
    centroid = pts.mean(axis=0)
    shifted = pts - centroid
    # Existing vertex angles (CCW from +X)
    ang = np.arctan2(shifted[:, 1], shifted[:, 0])
    ang = (ang + 2 * np.pi) % (2 * np.pi)

    # Sort vertices by angle, building a ring
    order = np.argsort(ang)
    ang_sorted = ang[order]
    pts_sorted = shifted[order]
    # Full wrap: prepend last vertex with angle − 2π, append first with +2π so any
    # target angle in [0, 2π) falls cleanly between two neighbors
    ang_ext = np.concatenate([[ang_sorted[-1] - 2 * np.pi],
                              ang_sorted,
                              [ang_sorted[0] + 2 * np.pi]])
    pts_ext = np.vstack([pts_sorted[-1:], pts_sorted, pts_sorted[0:1]])

    targets = np.linspace(0, 2 * np.pi, n, endpoint=False)
    out = []
    for t in targets:
        j = int(np.searchsorted(ang_ext, t, side="right")) - 1
        j = max(0, min(j, len(ang_ext) - 2))
        span = ang_ext[j + 1] - ang_ext[j]
        u = (t - ang_ext[j]) / span if span > 1e-12 else 0.0
        u = max(0.0, min(1.0, u))     # guard against extrapolation
        p = pts_ext[j] + u * (pts_ext[j + 1] - pts_ext[j])
        out.append(p + centroid)
    return np.array(out)


def slice_part(stl_path: Path, n_stations: int, m_points: int):
    """Slice the mesh at N Z-stations. For each slice, use the CONVEX HULL of
    the slice points as the cross-section polygon (works on non-watertight
    meshes; loses concave detail but gives a clean loftable outline)."""
    from scipy.spatial import ConvexHull  # type: ignore

    mesh = trimesh.load(str(stl_path))
    z_min = mesh.bounds[0][2]
    z_max = mesh.bounds[1][2]
    zs = np.linspace(z_min + 1e-4, z_max - 1e-4, n_stations)
    sections = []
    for z in zs:
        section_3d = mesh.section(plane_origin=[0, 0, float(z)], plane_normal=[0, 0, 1])
        if section_3d is None:
            continue
        vtx = np.array(section_3d.vertices)
        if len(vtx) < 3:
            continue
        xy = vtx[:, :2]
        # Deduplicate near-coincident points to keep ConvexHull happy
        xy = np.unique(np.round(xy, 6), axis=0)
        if len(xy) < 3:
            continue
        try:
            hull = ConvexHull(xy)
        except Exception:
            continue
        hull_pts = xy[hull.vertices]
        # Skip degenerate / tiny sections (e.g. at tips where cross-section is a point)
        rng = np.ptp(hull_pts, axis=0)
        if rng.max() < 1e-4:
            continue
        # resample_polygon now uses angular sampling with consistent 0..2π
        pts = resample_polygon(hull_pts, m_points)
        sections.append({"z": float(z), "pts": pts.tolist()})
    return sections


def main():
    parts = {
        "upper":  "odin_part_00.stl",
        "lower":  "odin_part_01.stl",
        "wings":  "odin_part_02.stl",
    }
    fit = {"scale": SCALE, "parts": {}}
    for name, fn in parts.items():
        stl = PARTS_DIR / fn
        if not stl.exists():
            print(f"missing: {stl}")
            continue
        sections = slice_part(stl, N_STATIONS, M_POINTS)
        fit["parts"][name] = sections
        print(f"{name:6s}: {len(sections)} sections from {fn}")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(fit, indent=2))
    print(f"wrote {OUT_JSON}")

    # Emit the CadQuery script
    cq_code = '''"""Parametric Odin drone — lofted through Z-station cross-sections
extracted from the reference mesh. Run in CQ-editor.

Source data: reference/odin_fit.json (regenerate via CAD/fit_odin.py).
"""
import json
from pathlib import Path

import cadquery as cq
from OCP.BRepOffsetAPI import BRepOffsetAPI_ThruSections


FIT = json.loads((Path(__file__).parent / "reference" / "odin_fit.json").read_text())
SCALE = FIT["scale"]


def build_wire_at(z_mm: float, pts_xy):
    """Build a closed CadQuery wire in XY at absolute height z_mm."""
    pts = [(x * SCALE, y * SCALE) for (x, y) in pts_xy]
    return (
        cq.Workplane("XY", origin=(0, 0, z_mm))
        .polyline(pts)
        .close()
        .val()
    )


def loft_part(sections):
    """Build a lofted solid directly via OCCT's BRepOffsetAPI_ThruSections,
    avoiding the CadQuery workplane chain which mis-places intermediate wires."""
    if len(sections) < 2:
        return None
    wires = []
    for s in sections:
        z_mm = s["z"] * SCALE
        wires.append(build_wire_at(z_mm, s["pts"]))

    builder = BRepOffsetAPI_ThruSections(True, False)  # isSolid=True, isRuled=False
    for w in wires:
        builder.AddWire(w.wrapped)
    builder.Build()
    if not builder.IsDone():
        return None
    return cq.Workplane(obj=cq.Shape(builder.Shape()))


upper = loft_part(FIT["parts"]["upper"])
lower = loft_part(FIT["parts"]["lower"])
wings = loft_part(FIT["parts"]["wings"])


if "show_object" in globals():
    if upper is not None:
        show_object(upper, name="Upper_Body", options={"color": (220, 180, 180), "alpha": 0.5})
    if lower is not None:
        show_object(lower, name="Lower_Body", options={"color": (180, 220, 180), "alpha": 0.5})
    if wings is not None:
        show_object(wings, name="Wings",      options={"color": (180, 180, 220), "alpha": 0.5})
'''
    OUT_CQ.write_text(cq_code)
    print(f"wrote {OUT_CQ}")


if __name__ == "__main__":
    main()
