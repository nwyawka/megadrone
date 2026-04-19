"""Load the OpenVSP v16 model into Blender as the working geometry.

The parametric rebuild was dropped — the v16 OBJ is the source of truth.
This script simply imports the OBJ as a solid-shaded mesh so you can edit
it directly in Blender.

Run headless:
    /Applications/Blender.app/Contents/MacOS/Blender --background \
        --python Blender/build_va6.py -- --save Blender/va6.blend
"""

import argparse
import sys
from pathlib import Path

import bpy  # type: ignore


REFERENCE_OBJ = Path(__file__).parent / "va6_v16_reference.obj"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.collections):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", type=str, default=None)
    args = parser.parse_args(argv)

    clear_scene()

    # Millimeter-ish viewport scale
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"

    if not REFERENCE_OBJ.exists():
        print(f"[ERROR] missing OBJ: {REFERENCE_OBJ}")
        sys.exit(1)

    bpy.ops.wm.obj_import(filepath=str(REFERENCE_OBJ))

    # Solid-shade every imported object; smooth shading for a clean look.
    for obj in bpy.context.selected_objects:
        obj.display_type = "SOLID"
        obj.show_in_front = False
        obj.hide_render = False
        if obj.type == "MESH":
            for p in obj.data.polygons:
                p.use_smooth = True

    if args.save:
        out = Path(args.save)
        out.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        print(f"saved {out}")

    print("done")


if __name__ == "__main__":
    main()
