#!/usr/bin/env python3
"""
OpenVSP Analysis Script for Phase 1 UAV
Runs various analyses on the UAV model

Author: MegaDrone Project
Date: January 8, 2026
"""

import sys
import os

try:
    import openvsp as vsp
    print(f"OpenVSP {vsp.GetVSPVersion()} loaded\n")
except ImportError as e:
    print(f"Failed to import OpenVSP: {e}")
    sys.exit(1)


def load_model(model_path):
    """Load the VSP model"""
    print("=" * 60)
    print("Loading Model")
    print("=" * 60)

    vsp.ClearVSPModel()
    vsp.ReadVSPFile(model_path)
    vsp.Update()

    # List geometries
    geom_ids = vsp.FindGeoms()
    print(f"Loaded {len(geom_ids)} geometries:")
    for gid in geom_ids:
        name = vsp.GetGeomName(gid)
        gtype = vsp.GetGeomTypeName(gid)
        print(f"  - {name} ({gtype})")
    print()
    return geom_ids


def run_comp_geom():
    """Run CompGeom analysis - wetted area, volumes"""
    print("=" * 60)
    print("CompGeom Analysis (Wetted Area, Volumes)")
    print("=" * 60)

    # Set up analysis
    vsp.SetAnalysisInputDefaults("CompGeom")

    # Execute
    results_id = vsp.ExecAnalysis("CompGeom")

    # Get results
    wet_area = vsp.GetDoubleResults(results_id, "Wet_Area", 0)
    theo_area = vsp.GetDoubleResults(results_id, "Theo_Area", 0)
    wet_vol = vsp.GetDoubleResults(results_id, "Wet_Vol", 0)
    theo_vol = vsp.GetDoubleResults(results_id, "Theo_Vol", 0)

    print(f"  Wetted Area:      {wet_area[0]:.4f} m^2" if wet_area else "  Wetted Area: N/A")
    print(f"  Theoretical Area: {theo_area[0]:.4f} m^2" if theo_area else "  Theo Area: N/A")
    print(f"  Wetted Volume:    {wet_vol[0]:.6f} m^3" if wet_vol else "  Wetted Vol: N/A")
    print(f"  Theoretical Vol:  {theo_vol[0]:.6f} m^3" if theo_vol else "  Theo Vol: N/A")

    # Clean up mesh geometry created by analysis
    mesh_ids = vsp.GetStringResults(results_id, "Mesh_GeomID")
    if mesh_ids:
        vsp.DeleteGeomVec(mesh_ids)

    print()
    return results_id


def run_mass_properties():
    """Run MassProp analysis - CG, moments of inertia"""
    print("=" * 60)
    print("Mass Properties Analysis")
    print("=" * 60)

    # Set up analysis
    vsp.SetAnalysisInputDefaults("MassProp")

    # Execute
    results_id = vsp.ExecAnalysis("MassProp")

    # Print all available result names for debugging
    result_names = vsp.GetAllDataNames(results_id)

    # Get results - try different possible names
    total_mass = vsp.GetDoubleResults(results_id, "Total_Mass", 0)
    ixx = vsp.GetDoubleResults(results_id, "Total_Ixx", 0)
    iyy = vsp.GetDoubleResults(results_id, "Total_Iyy", 0)
    izz = vsp.GetDoubleResults(results_id, "Total_Izz", 0)

    print(f"  Total Mass:  {total_mass[0]:.4f} kg" if total_mass else "  Mass: N/A (set density first)")
    print(f"  Ixx: {ixx[0]:.6f} kg*m^2" if ixx else "  Ixx: N/A")
    print(f"  Iyy: {iyy[0]:.6f} kg*m^2" if iyy else "  Iyy: N/A")
    print(f"  Izz: {izz[0]:.6f} kg*m^2" if izz else "  Izz: N/A")

    # Try to get CG
    cg = vsp.GetDoubleResults(results_id, "Total_CG", 0)
    if cg and len(cg) >= 3:
        print(f"  CG Location: ({cg[0]:.4f}, {cg[1]:.4f}, {cg[2]:.4f}) m")

    # Clean up
    mesh_ids = vsp.GetStringResults(results_id, "Mesh_GeomID")
    if mesh_ids:
        vsp.DeleteGeomVec(mesh_ids)

    print()
    return results_id


def run_parasite_drag():
    """Run ParasiteDrag analysis - drag buildup"""
    print("=" * 60)
    print("Parasite Drag Analysis")
    print("=" * 60)

    try:
        # Set up analysis
        vsp.SetAnalysisInputDefaults("ParasiteDrag")

        # Set flight conditions
        vsp.SetDoubleAnalysisInput("ParasiteDrag", "Vinf", [25.0])  # 25 m/s cruise
        vsp.SetDoubleAnalysisInput("ParasiteDrag", "Altitude", [100.0])  # 100m altitude

        # Set reference area (wing area) - approximately 0.55 m^2 for our UAV
        vsp.SetDoubleAnalysisInput("ParasiteDrag", "Sref", [0.55])

        # Execute
        results_id = vsp.ExecAnalysis("ParasiteDrag")

        # Get all result names to see what's available
        result_names = vsp.GetAllDataNames(results_id)

        # Try to get results
        total_cd = vsp.GetDoubleResults(results_id, "Total_CD_Total", 0)
        swet = vsp.GetDoubleResults(results_id, "Swet", 0)
        ff = vsp.GetDoubleResults(results_id, "FF", 0)

        if swet:
            print(f"  Total Wetted Area: {sum(swet):.4f} m^2")
        if total_cd:
            print(f"  Total CD (parasite): {total_cd[0]:.6f}")
            # Calculate drag force
            rho = 1.225  # kg/m^3 at sea level
            v = 25.0  # m/s
            sref = 0.55  # m^2
            q = 0.5 * rho * v**2
            drag = total_cd[0] * q * sref
            print(f"  Parasite Drag Force: {drag:.3f} N (at {v} m/s, Sref={sref} m^2)")
        else:
            print("  (Parasite drag requires component setup in GUI for detailed results)")

    except Exception as e:
        print(f"  Parasite drag analysis note: {e}")

    print()
    return None


def run_wave_drag():
    """Run WaveDrag analysis - supersonic area ruling (informational)"""
    print("=" * 60)
    print("Wave Drag Analysis (Area Distribution)")
    print("=" * 60)

    # Set up analysis
    vsp.SetAnalysisInputDefaults("WaveDrag")
    vsp.SetIntAnalysisInput("WaveDrag", "Set", [vsp.SET_ALL])

    # Execute
    results_id = vsp.ExecAnalysis("WaveDrag")

    # Get results
    cd_wave = vsp.GetDoubleResults(results_id, "CDWave", 0)

    print(f"  CD Wave: {cd_wave[0]:.6f}" if cd_wave else "  CD Wave: N/A (subsonic UAV)")
    print("  (Wave drag is primarily for transonic/supersonic aircraft)")

    # Clean up
    mesh_ids = vsp.GetStringResults(results_id, "Mesh_GeomID")
    if mesh_ids:
        vsp.DeleteGeomVec(mesh_ids)

    print()
    return results_id


def run_planar_slice():
    """Run PlanarSlice analysis - cross-sectional areas"""
    print("=" * 60)
    print("Planar Slice Analysis (Cross-sections)")
    print("=" * 60)

    try:
        # Set up analysis
        vsp.SetAnalysisInputDefaults("PlanarSlice")

        # Slice along X-axis (fuselage length)
        vsp.SetVec3dAnalysisInput("PlanarSlice", "Norm", [vsp.vec3d(1, 0, 0)])
        vsp.SetIntAnalysisInput("PlanarSlice", "AutoBoundFlag", [1])
        vsp.SetIntAnalysisInput("PlanarSlice", "NumSlices", [20])

        # Execute
        results_id = vsp.ExecAnalysis("PlanarSlice")

        # Get all result names
        result_names = vsp.GetAllDataNames(results_id)

        # Try to get slice areas
        slice_area = vsp.GetDoubleResults(results_id, "Slice_Area", 0)

        if slice_area and len(slice_area) > 0:
            print(f"  Number of slices: {len(slice_area)}")
            print(f"  Max cross-section area: {max(slice_area):.6f} m^2")
        else:
            print("  Slice analysis completed (check GUI for detailed results)")

        # Clean up
        mesh_ids = vsp.GetStringResults(results_id, "Mesh_GeomID")
        if mesh_ids:
            vsp.DeleteGeomVec(mesh_ids)

    except Exception as e:
        print(f"  Planar slice analysis error: {e}")

    print()
    return None


def print_available_analyses():
    """Print all available analyses"""
    print("=" * 60)
    print("Available OpenVSP Analyses")
    print("=" * 60)

    analyses = vsp.ListAnalysis()
    for i, name in enumerate(analyses, 1):
        print(f"  {i:2d}. {name}")
    print()


def main():
    """Main execution"""
    # Model path
    designs_dir = os.path.join(os.path.dirname(__file__), "..", "designs")
    model_path = os.path.join(designs_dir, "Phase1_UAV_Correct.vsp3")

    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        print("Run phase1_openvsp_correct.py first to generate the model.")
        sys.exit(1)

    print("=" * 60)
    print("OpenVSP UAV Analysis Suite")
    print("=" * 60)
    print(f"Model: {model_path}")
    print()

    # Print available analyses
    print_available_analyses()

    # Load model
    load_model(model_path)

    # Run analyses
    run_comp_geom()
    run_mass_properties()
    run_parasite_drag()
    run_planar_slice()
    run_wave_drag()

    # Summary
    print("=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    print("""
Additional analyses available:
  - VSPAEROSinglePoint: Full aerodynamic analysis (lift, drag, moments)
  - VSPAEROSweep: Parameter sweeps (alpha, beta, Mach)
  - CfdMeshAnalysis: Generate CFD mesh
  - FeaMeshAnalysis: Generate FEA mesh
  - BladeElement: Propeller analysis

To run VSPAero (recommended for detailed aero analysis):
  1. Open model in OpenVSP GUI
  2. Analysis -> VSPAERO
  3. Set flight conditions
  4. Run analysis
""")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
