"""Load the Odin drone interceptor mesh (from Sketchfab GLB → STL) as a
CadQuery shape for viewing in CQ-editor.

Source: CAD/reference/odin_drone_interceptor.glb
Converted: CAD/reference/odin_drone_interceptor.stl (via Blender/glb_to_stl.py)

STL is a mesh (~232k faces), not a parametric solid. CadQuery wraps it as a
TopoDS_Shape via OCP's StlAPI_Reader and it renders as shaded geometry in
CQ-editor. Dimensions/bounding box are printed so you can use this as a
reference for sizing the parametric model.
"""

from pathlib import Path

import cadquery as cq
from OCP.StlAPI import StlAPI_Reader
from OCP.TopoDS import TopoDS_Shape


STL_PATH = Path(__file__).parent / "reference" / "odin_drone_decimated.stl"


def load_stl(path: Path) -> cq.Shape:
    """Read an STL into a CadQuery Shape (wrapping a TopoDS_Shape)."""
    reader = StlAPI_Reader()
    shape = TopoDS_Shape()
    ok = reader.Read(shape, str(path))
    if not ok:
        raise RuntimeError(f"StlAPI_Reader failed to read {path}")
    return cq.Shape(shape)


odin = load_stl(STL_PATH)

# Measure + print dimensions (GLB reference — units vary; Sketchfab often
# exports in meters but assets aren't always real-scale)
bb = odin.BoundingBox()
print(f"Odin reference bbox: x[{bb.xmin:.3f}, {bb.xmax:.3f}]  "
      f"y[{bb.ymin:.3f}, {bb.ymax:.3f}]  z[{bb.zmin:.3f}, {bb.zmax:.3f}]")
print(f"extents: {bb.xlen:.3f} x {bb.ylen:.3f} x {bb.zlen:.3f}")

if "show_object" in globals():
    show_object(odin, name="Odin_Reference", options={"color": (180, 180, 200), "alpha": 0.4})
