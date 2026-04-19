"""Import GLB, analyze each separate mesh object (bbox, centroid, vert count),
and export each as its own STL. Helps understand the Odin component structure.
Run headless:
    blender --background --python Blender/analyze_glb.py -- --glb ... --outdir ...
"""
import argparse, sys
from pathlib import Path
import bpy  # type: ignore


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--decimate", type=float, default=0.15,
                    help="decimate ratio for the separate STLs (0 = keep original)")
    args = ap.parse_args(argv)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    glb = str(Path(args.glb).resolve())
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    bpy.ops.import_scene.gltf(filepath=glb)

    mesh_objs = [o for o in bpy.data.objects if o.type == "MESH"]
    print(f"imported {len(mesh_objs)} mesh objects")

    for i, o in enumerate(mesh_objs):
        # Hide all other meshes so STL export only contains this one
        for other in mesh_objs:
            other.hide_set(other is not o)
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o

        # Decimate for CQ consumption
        if args.decimate > 0 and args.decimate < 1:
            mod = o.modifiers.new("Decimate", "DECIMATE")
            mod.ratio = args.decimate
            bpy.ops.object.modifier_apply(modifier=mod.name)

        # World-space bounding box (takes object transform into account)
        import mathutils  # type: ignore
        world_corners = [o.matrix_world @ mathutils.Vector(v) for v in o.bound_box]
        xs = [p.x for p in world_corners]; ys = [p.y for p in world_corners]; zs = [p.z for p in world_corners]
        cx = sum(xs) / 8; cy = sum(ys) / 8; cz = sum(zs) / 8
        dx = max(xs) - min(xs); dy = max(ys) - min(ys); dz = max(zs) - min(zs)
        nv = len(o.data.vertices); nf = len(o.data.polygons)

        out = outdir / f"odin_part_{i:02d}.stl"
        bpy.ops.wm.stl_export(filepath=str(out), export_selected_objects=True)
        print(f"[{i}] name={o.name}")
        print(f"    verts={nv}  faces={nf}")
        print(f"    centroid=({cx:.3f},{cy:.3f},{cz:.3f})  extent={dx:.3f}×{dy:.3f}×{dz:.3f}")
        print(f"    wrote {out.name}")


if __name__ == "__main__":
    main()
