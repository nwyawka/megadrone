"""Side-by-side viewer: Odin reference mesh + Peregrine parametric solids.

Both models aligned along the +X axis with their noses at x=0. Peregrine
solids are drawn normally; Odin mesh is rotated from its native Z-axis
orientation so its longitudinal axis also maps to +X for apples-to-apples
comparison, and rendered semi-transparent as a ghost overlay.

Open in CQ-editor: File > Open > CAD/combined_view.py
"""

from pathlib import Path

import cadquery as cq
from OCP.StlAPI import StlAPI_Reader
from OCP.TopoDS import TopoDS_Shape
from OCP.gp import gp_Trsf, gp_Pnt, gp_Ax1, gp_Dir
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform

import odin_body as p  # pulls in nose, body, boattail, wings, airframe


# ============================ Odin reference =============================
ODIN_STL = Path(__file__).parent / "reference" / "odin_drone_decimated.stl"
ODIN_SRC_LEN    = 1.001                     # unitless length in the GLB
ODIN_TARGET_LEN = 741.825                   # LOCKED at initial full-scale (L=141.3 × 5.25)
ODIN_SCALE      = ODIN_TARGET_LEN / ODIN_SRC_LEN


def load_stl(path: Path) -> cq.Shape:
    reader = StlAPI_Reader()
    shape = TopoDS_Shape()
    if not reader.Read(shape, str(path)):
        raise RuntimeError(f"could not read {path}")
    return cq.Shape(shape)


def scale_shape(shape: cq.Shape, s: float) -> cq.Shape:
    trsf = gp_Trsf()
    trsf.SetScale(gp_Pnt(0, 0, 0), s)
    t = BRepBuilderAPI_Transform(shape.wrapped, trsf, True)
    return cq.Shape(t.Shape())


def rotate_shape(shape: cq.Shape, axis_origin, axis_dir, angle_deg: float) -> cq.Shape:
    trsf = gp_Trsf()
    axis = gp_Ax1(gp_Pnt(*axis_origin), gp_Dir(*axis_dir))
    trsf.SetRotation(axis, angle_deg * 3.141592653589793 / 180.0)
    t = BRepBuilderAPI_Transform(shape.wrapped, trsf, True)
    return cq.Shape(t.Shape())


def translate_shape(shape: cq.Shape, dx: float, dy: float, dz: float) -> cq.Shape:
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Pnt(0, 0, 0), gp_Pnt(dx, dy, dz))
    t = BRepBuilderAPI_Transform(shape.wrapped, trsf, True)
    return cq.Shape(t.Shape())


# Load the Odin STL, scale to Peregrine length, rotate its +Z → +X,
# then slide forward so its nose (former -Z, now -X) sits at x=0.
odin = load_stl(ODIN_STL)
odin = scale_shape(odin, ODIN_SCALE)
# Rotate -90° about Y axis: (x,y,z) → (z, y, -x)   maps +Z → +X
odin = rotate_shape(odin, (0, 0, 0), (0, 1, 0), -90.0)
# After rotation, longitudinal extent is in X centered near 0.
# Shift so the nose tip (most negative X) lands at x=0.
odin_bb = odin.BoundingBox()
odin = translate_shape(odin, -odin_bb.xmin, 0.0, 0.0)


print(f"Peregrine airframe: x=[0, {p.TOTAL_LEN:.1f}]  r_max={p.R:.1f}")
bb = odin.BoundingBox()
print(f"Odin reference:     x=[{bb.xmin:.1f}, {bb.xmax:.1f}]  y=[{bb.ymin:.1f}, {bb.ymax:.1f}]  z=[{bb.zmin:.1f}, {bb.zmax:.1f}]")


# ============================ Show ========================================
if "show_object" in globals():
    # Peregrine parametric parts — opaque-ish
    show_object(p.nose,     name="Per_Nose",     options={"color": (230, 200, 200), "alpha": 0.45})
    show_object(p.body,     name="Per_Body",     options={"color": (200, 230, 200), "alpha": 0.45})
    show_object(p.boattail, name="Per_Boattail", options={"color": (200, 200, 230), "alpha": 0.45})
    # Odin mesh ghost overlay
    show_object(odin, name="Odin_Reference", options={"color": (180, 180, 200), "alpha": 0.25})
