"""Parse OpenVSP .vsp3 file and extract dimensional parameters for each Geom.

Dumps a structured summary of the VA-6 v16 parametric model to stdout so we
can transcribe real numbers into the CadQuery rebuild.
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def iter_parms(elem):
    """Yield (name, float_value) for every descendant element that has a Value
    attribute (OpenVSP's parameter encoding)."""
    for node in elem.iter():
        val = node.get("Value")
        if val is None:
            continue
        try:
            yield node.tag, float(val)
        except ValueError:
            pass


def collect_parms(elem):
    """Return dict of parm name -> value. Later duplicates overwrite earlier."""
    out = {}
    for name, v in iter_parms(elem):
        out[name] = v
    return out


def parm(container_elem, *names, default=None):
    """Find first matching parameter by any of the given names, direct child search."""
    for node in container_elem.iter():
        if node.tag in names and node.get("Value") is not None:
            try:
                return float(node.get("Value"))
            except ValueError:
                continue
    return default


def summarize_geom(geom):
    gb = geom.find("GeomBase")
    pc = geom.find("ParmContainer")
    type_name = gb.find("TypeName").text if gb is not None else "?"
    name = pc.find("Name").text if pc is not None and pc.find("Name") is not None else "?"

    xform = pc.find("XForm") if pc is not None else None
    loc = {}
    rot = {}
    if xform is not None:
        for k in ("X_Location", "Y_Location", "Z_Location",
                 "X_Rel_Location", "Y_Rel_Location", "Z_Rel_Location",
                 "X_Rotation", "Y_Rotation", "Z_Rotation",
                 "X_Rel_Rotation", "Y_Rel_Rotation", "Z_Rel_Rotation"):
            el = xform.find(k)
            if el is not None:
                v = float(el.get("Value"))
                if "Location" in k:
                    loc[k] = v
                else:
                    rot[k] = v

    return name, type_name, loc, rot


def xsec_summary(xsec_surf):
    """List each XSec in a fuselage/wing XSecSurf with its X-loc (or span) and shape."""
    sections = []
    for i, xsec in enumerate(xsec_surf.findall("XSec")):
        # type
        type_el = xsec.find("Type")
        x_type = type_el.get("Value") if type_el is not None else None
        # Collect all named params + their values
        parms = collect_parms(xsec)
        # Pull the usual suspects
        s = {
            "idx": i,
            "parms_selected": {k: parms[k] for k in (
                "XLocPercent", "ZLocPercent", "YLocPercent",
                "Spine_Location",
                "Span", "Sweep", "Sweep_Location", "Tot_Span", "Aspect",
                "Root_Chord", "Tip_Chord", "Avg_Chord",
                "Taper", "Twist", "Dihedral",
                "RefLength", "Ellipse_Width", "Ellipse_Height",
                "Circle_Diameter",
                "Width", "Height", "Length",
            ) if k in parms},
        }
        sections.append(s)
    return sections


def main():
    vsp_path = Path("/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/va6/VA6_Peregrine_v16.vsp3")
    tree = ET.parse(vsp_path)
    root = tree.getroot()

    print(f"Parsing {vsp_path.name}")
    print("=" * 72)

    for geom in root.iter("Geom"):
        gb = geom.find("GeomBase")
        if gb is None:
            continue
        name, type_name, loc, rot = summarize_geom(geom)
        if name == "?":
            continue

        print(f"\n### {name}  ({type_name})")
        if loc:
            print("  Location:", {k: round(v, 4) for k, v in loc.items()})
        if rot:
            nonzero = {k: round(v, 4) for k, v in rot.items() if abs(v) > 1e-9}
            if nonzero:
                print("  Rotation:", nonzero)

        # Fuselage: iterate XSecs
        fg = geom.find("FuselageGeom")
        if fg is not None:
            xsec_surf = fg.find("XSecSurf")
            if xsec_surf is not None:
                # Also collect fuselage-level params (Length etc.)
                top_parms = collect_parms(fg.find("ParmContainer") or fg)
                length = top_parms.get("Length")
                if length is not None:
                    print(f"  Overall Length: {length:.4f} m  ({length*1000:.1f} mm)")
                sections = xsec_summary(xsec_surf)
                print(f"  XSecs: {len(sections)}")
                for s in sections:
                    if s["parms_selected"]:
                        rounded = {k: round(v, 4) for k, v in s["parms_selected"].items()}
                        print(f"    [{s['idx']}] {rounded}")

        # Wing: look for WingGeom
        wg = geom.find("WingGeom")
        if wg is not None:
            xsec_surf = wg.find("XSecSurf")
            if xsec_surf is not None:
                top_parms = collect_parms(wg.find("ParmContainer") or wg)
                interesting = {k: round(top_parms[k], 4) for k in (
                    "TotalSpan", "TotalChord", "TotalArea", "TotalAspect",
                    "TotalProjectedSpan",
                ) if k in top_parms}
                if interesting:
                    print(f"  Wing totals: {interesting}")
                sections = xsec_summary(xsec_surf)
                print(f"  Wing XSecs: {len(sections)}")
                for s in sections:
                    if s["parms_selected"]:
                        rounded = {k: round(v, 4) for k, v in s["parms_selected"].items()}
                        print(f"    [{s['idx']}] {rounded}")


if __name__ == "__main__":
    main()
