"""Import a GLB, join all meshes, export as STL. Usage:
    blender --background --python Blender/glb_to_stl.py -- --glb path/to.glb --stl path/out.stl
"""
import argparse, sys
import bpy  # type: ignore

def main():
    print("FULL sys.argv:", sys.argv)
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    print("after --:", argv)
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", required=True)
    ap.add_argument("--stl", required=True)
    ap.add_argument("--decimate", type=float, default=0.0,
                    help="Decimate collapse ratio (0 = no decimation, 0.1 = keep 10% of faces)")
    args = ap.parse_args(argv)
    print(f"glb={args.glb!r}")
    print(f"stl={args.stl!r}")

    # Fresh scene
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    from pathlib import Path
    glb_abs = str(Path(args.glb).resolve())
    stl_abs = str(Path(args.stl).resolve())
    print(f"abs glb={glb_abs}")
    print(f"abs stl={stl_abs}")
    bpy.ops.import_scene.gltf(filepath=glb_abs)

    mesh_objs = [o for o in bpy.data.objects if o.type == "MESH"]
    print(f"imported {len(mesh_objs)} mesh objects")
    if not mesh_objs:
        sys.exit("no meshes")

    bpy.ops.object.select_all(action="DESELECT")
    for o in mesh_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = mesh_objs[0]
    if len(mesh_objs) > 1:
        bpy.ops.object.join()

    active = bpy.context.active_object

    # Optional decimation so CadQuery's OCCT STL reader doesn't choke
    if args.decimate > 0 and args.decimate < 1:
        mod = active.modifiers.new("Decimate", "DECIMATE")
        mod.ratio = args.decimate
        bpy.ops.object.modifier_apply(modifier=mod.name)
        print(f"decimated to ratio {args.decimate}")

    bb = active.bound_box
    xs = [p[0] for p in bb]; ys = [p[1] for p in bb]; zs = [p[2] for p in bb]
    print(f"bbox: x[{min(xs):.3f},{max(xs):.3f}] y[{min(ys):.3f},{max(ys):.3f}] z[{min(zs):.3f},{max(zs):.3f}]")
    print(f"verts={len(active.data.vertices)}, faces={len(active.data.polygons)}")

    bpy.ops.wm.stl_export(filepath=stl_abs)
    print(f"wrote {stl_abs}")


if __name__ == "__main__":
    main()
