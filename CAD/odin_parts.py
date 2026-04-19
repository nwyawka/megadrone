"""Load the 3 separate Odin drone components into CQ-editor for inspection.

Part 00: upper body half
Part 01: lower body half
Part 02: wings (thin horizontal plate)

Orientation: local Z is the longitudinal axis (~1.0 unitless = full length).
Wings (part 02) are thin in Y → wings lie in the XZ plane.
"""

from pathlib import Path

import cadquery as cq
from OCP.StlAPI import StlAPI_Reader
from OCP.TopoDS import TopoDS_Shape


HERE = Path(__file__).parent
PARTS_DIR = HERE / "reference" / "parts"
TARGET_LEN_MM = 680.0        # scale whole model to this longitudinal length
SOURCE_LEN    = 1.001        # measured length in the GLB's unitless frame
SCALE         = TARGET_LEN_MM / SOURCE_LEN


def load_stl(path: Path) -> cq.Shape:
    reader = StlAPI_Reader()
    shape = TopoDS_Shape()
    if not reader.Read(shape, str(path)):
        raise RuntimeError(f"could not read {path}")
    return cq.Shape(shape)


from OCP.gp import gp_Trsf, gp_Pnt
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform


def scaled_wp(path: Path, scale: float) -> cq.Workplane:
    """Load STL and apply a true scaling transform (Location can't hold scale)."""
    shape = load_stl(path)
    trsf = gp_Trsf()
    trsf.SetScale(gp_Pnt(0, 0, 0), scale)
    transformer = BRepBuilderAPI_Transform(shape.wrapped, trsf, True)  # copy=True
    scaled = cq.Shape(transformer.Shape())
    return cq.Workplane(obj=scaled)


part00 = scaled_wp(PARTS_DIR / "odin_part_00.stl", SCALE)
part01 = scaled_wp(PARTS_DIR / "odin_part_01.stl", SCALE)
part02 = scaled_wp(PARTS_DIR / "odin_part_02.stl", SCALE)


def bbox_str(wp):
    bb = wp.val().BoundingBox()
    return (f"x[{bb.xmin:.0f},{bb.xmax:.0f}] "
            f"y[{bb.ymin:.0f},{bb.ymax:.0f}] "
            f"z[{bb.zmin:.0f},{bb.zmax:.0f}]")

print(f"scale: {SCALE:.2f} mm/unit (target length {TARGET_LEN_MM} mm)")
print(f"part00 (upper body): {bbox_str(part00)}")
print(f"part01 (lower body): {bbox_str(part01)}")
print(f"part02 (wings):      {bbox_str(part02)}")


if "show_object" in globals():
    show_object(part00, name="00_Upper_Body", options={"color": (230, 180, 180), "alpha": 0.5})
    show_object(part01, name="01_Lower_Body", options={"color": (180, 230, 180), "alpha": 0.5})
    show_object(part02, name="02_Wings",      options={"color": (180, 180, 230), "alpha": 0.5})
