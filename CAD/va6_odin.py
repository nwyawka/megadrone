"""Parametric Odin drone — lofted through Z-station cross-sections
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
