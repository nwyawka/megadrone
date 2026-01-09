#!/usr/bin/env python3
"""
CFD Validation Script for MegaDrone Phase 1
Uses SU2 for RANS analysis to validate VLM predictions

Author: MegaDrone Project
Date: January 8, 2026
"""

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

# Paths
PROJECT_DIR = Path("/Users/matthewoneil/Desktop/Datawerkes/MegaDrone")
DESIGNS_DIR = PROJECT_DIR / "designs"
CFD_DIR = PROJECT_DIR / "cfd"
SU2_BIN = Path("/tmp/bin")

# Flight conditions (from design)
FLIGHT_CONDITIONS = {
    "cruise": {
        "velocity_ms": 25.7,  # 50 knots
        "alpha_deg": 3.0,
        "altitude_m": 150,
        "mach": 0.075,
        "reynolds": 250000,
        "ref_length_m": 0.142,  # Mean chord
    },
    "loiter": {
        "velocity_ms": 15.0,  # 29 knots
        "alpha_deg": 5.0,
        "altitude_m": 150,
        "mach": 0.044,
        "reynolds": 150000,
        "ref_length_m": 0.142,
    },
}

# Reference values for coefficients
REF_AREA_M2 = 0.241  # Wing area
REF_LENGTH_M = 0.142  # Mean chord

# VLM predictions to validate against
VLM_RESULTS = {
    "cruise": {
        "CL": 0.53,
        "CD": 0.026,
        "L/D": 21.5,
    },
    "loiter": {
        "CL": 0.80,
        "CD": 0.035,
        "L/D": 22.8,
    },
}


# =============================================================================
# MESH GENERATION
# =============================================================================

def create_2d_airfoil_mesh_gmsh():
    """Create 2D airfoil mesh using Gmsh for initial validation."""

    # Load optimized airfoil coordinates
    airfoil_path = DESIGNS_DIR / "optimized_airfoil.dat"
    coords = np.loadtxt(airfoil_path)

    # The airfoil coordinates need to form a closed loop
    # Check if first and last points are the same
    x = coords[:, 0].copy()
    y = coords[:, 1].copy()

    # Ensure the airfoil is closed (first point = last point)
    if not (np.isclose(x[0], x[-1]) and np.isclose(y[0], y[-1])):
        x = np.append(x, x[0])
        y = np.append(y, y[0])

    n_pts = len(x)

    # Create Gmsh geo file for 2D airfoil using Python API
    CFD_DIR.mkdir(exist_ok=True)

    try:
        import gmsh
    except ImportError:
        print("Warning: gmsh Python module not found. Using command-line approach.")
        return create_2d_airfoil_mesh_gmsh_cli()

    gmsh.initialize()
    gmsh.model.add("airfoil")

    # Mesh parameters
    lc_airfoil = 0.005  # Element size on airfoil
    lc_far = 1.0        # Element size at far-field
    far_field_size = 20  # 20 chord lengths to far-field

    # Add airfoil points (must be in counterclockwise order for a closed loop)
    airfoil_points = []
    for i in range(n_pts - 1):  # Skip last point (same as first)
        pt = gmsh.model.geo.addPoint(x[i], y[i], 0, lc_airfoil)
        airfoil_points.append(pt)

    # Create spline for airfoil (closed loop)
    airfoil_points_loop = airfoil_points + [airfoil_points[0]]  # Close the loop
    airfoil_spline = gmsh.model.geo.addSpline(airfoil_points_loop)

    # Create far-field circle
    center = gmsh.model.geo.addPoint(0.5, 0, 0, lc_far)
    p_right = gmsh.model.geo.addPoint(0.5 + far_field_size, 0, 0, lc_far)
    p_top = gmsh.model.geo.addPoint(0.5, far_field_size, 0, lc_far)
    p_left = gmsh.model.geo.addPoint(0.5 - far_field_size, 0, 0, lc_far)
    p_bottom = gmsh.model.geo.addPoint(0.5, -far_field_size, 0, lc_far)

    arc1 = gmsh.model.geo.addCircleArc(p_right, center, p_top)
    arc2 = gmsh.model.geo.addCircleArc(p_top, center, p_left)
    arc3 = gmsh.model.geo.addCircleArc(p_left, center, p_bottom)
    arc4 = gmsh.model.geo.addCircleArc(p_bottom, center, p_right)

    # Create curve loops
    farfield_loop = gmsh.model.geo.addCurveLoop([arc1, arc2, arc3, arc4])
    airfoil_loop = gmsh.model.geo.addCurveLoop([airfoil_spline])

    # Create surface (far-field with airfoil hole)
    surface = gmsh.model.geo.addPlaneSurface([farfield_loop, airfoil_loop])

    gmsh.model.geo.synchronize()

    # Physical groups for boundary conditions
    gmsh.model.addPhysicalGroup(1, [arc1, arc2, arc3, arc4], name="farfield")
    gmsh.model.addPhysicalGroup(1, [airfoil_spline], name="airfoil")
    gmsh.model.addPhysicalGroup(2, [surface], name="fluid")

    # Mesh refinement near airfoil
    gmsh.model.mesh.field.add("Distance", 1)
    gmsh.model.mesh.field.setNumbers(1, "CurvesList", [airfoil_spline])
    gmsh.model.mesh.field.setNumber(1, "NumPointsPerCurve", 100)

    gmsh.model.mesh.field.add("Threshold", 2)
    gmsh.model.mesh.field.setNumber(2, "InField", 1)
    gmsh.model.mesh.field.setNumber(2, "SizeMin", lc_airfoil)
    gmsh.model.mesh.field.setNumber(2, "SizeMax", lc_far)
    gmsh.model.mesh.field.setNumber(2, "DistMin", 0.1)
    gmsh.model.mesh.field.setNumber(2, "DistMax", 5.0)

    gmsh.model.mesh.field.setAsBackgroundMesh(2)

    # Generate 2D mesh
    gmsh.option.setNumber("Mesh.Algorithm", 6)  # Frontal-Delaunay
    gmsh.model.mesh.generate(2)

    # Save mesh in both formats
    msh_path = CFD_DIR / "airfoil_2d.msh"
    su2_path = CFD_DIR / "airfoil_2d.su2"

    gmsh.write(str(msh_path))
    print(f"Generated mesh: {msh_path}")

    gmsh.finalize()

    # Convert to SU2 format
    su2_path = convert_gmsh_to_su2_v2(msh_path)

    return su2_path


def create_2d_airfoil_mesh_gmsh_cli():
    """Fallback: Create mesh using Gmsh command line."""

    # Load optimized airfoil coordinates
    airfoil_path = DESIGNS_DIR / "optimized_airfoil.dat"
    coords = np.loadtxt(airfoil_path)

    x = coords[:, 0].copy()
    y = coords[:, 1].copy()

    # Ensure closed
    if not (np.isclose(x[0], x[-1]) and np.isclose(y[0], y[-1])):
        x = np.append(x, x[0])
        y = np.append(y, y[0])

    n_pts = len(x) - 1  # Don't count duplicate end point

    # Create geo file
    geo_content = """// 2D Airfoil Mesh for SU2 Validation
// Generated by MegaDrone CFD Script

// Mesh parameters
far_field_size = 20;
lc_airfoil = 0.005;
lc_far = 1.0;

// Airfoil points
"""

    for i in range(n_pts):
        geo_content += f"Point({i+1}) = {{{x[i]:.8f}, {y[i]:.8f}, 0, lc_airfoil}};\n"

    # Create spline and close it
    point_list = ",".join([str(i+1) for i in range(n_pts)] + ["1"])
    geo_content += f"\n// Airfoil spline (closed)\nSpline(1) = {{{point_list}}};\n"

    # Far-field
    geo_content += f"""
// Far-field boundary (circle)
Point({n_pts+1}) = {{0.5, 0, 0, lc_far}};  // Center
Point({n_pts+2}) = {{0.5 + far_field_size, 0, 0, lc_far}};
Point({n_pts+3}) = {{0.5, far_field_size, 0, lc_far}};
Point({n_pts+4}) = {{0.5 - far_field_size, 0, 0, lc_far}};
Point({n_pts+5}) = {{0.5, -far_field_size, 0, lc_far}};

Circle(2) = {{{n_pts+2}, {n_pts+1}, {n_pts+3}}};
Circle(3) = {{{n_pts+3}, {n_pts+1}, {n_pts+4}}};
Circle(4) = {{{n_pts+4}, {n_pts+1}, {n_pts+5}}};
Circle(5) = {{{n_pts+5}, {n_pts+1}, {n_pts+2}}};

// Create loops and surface
Curve Loop(1) = {{2, 3, 4, 5}};  // Far-field (counterclockwise)
Curve Loop(2) = {{1}};           // Airfoil

Plane Surface(1) = {{1, 2}};

// Physical groups for SU2
Physical Curve("farfield") = {{2, 3, 4, 5}};
Physical Curve("airfoil") = {{1}};
Physical Surface("fluid") = {{1}};

// Mesh algorithm
Mesh.Algorithm = 6;  // Frontal-Delaunay
"""

    CFD_DIR.mkdir(exist_ok=True)
    geo_path = CFD_DIR / "airfoil_2d.geo"
    with open(geo_path, 'w') as f:
        f.write(geo_content)

    print(f"Created Gmsh geo file: {geo_path}")

    # Generate mesh
    msh_path = CFD_DIR / "airfoil_2d.msh"
    try:
        result = subprocess.run([
            "gmsh", str(geo_path), "-2", "-o", str(msh_path),
            "-format", "msh2"
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Gmsh warning: {result.stderr}")
        print(f"Generated mesh: {msh_path}")
    except FileNotFoundError:
        print("Warning: Gmsh not found. Install with: brew install gmsh")
        return None

    # Convert to SU2 format
    su2_path = convert_gmsh_to_su2_v2(msh_path)
    return su2_path


def convert_gmsh_to_su2(msh_path):
    """Convert Gmsh mesh to SU2 format (legacy version)."""
    return convert_gmsh_to_su2_v2(msh_path)


def convert_gmsh_to_su2_v2(msh_path):
    """Convert Gmsh mesh to SU2 format - handles both Gmsh 2.x and 4.x formats."""

    su2_path = msh_path.with_suffix('.su2')

    # Read Gmsh mesh
    nodes = {}
    elements = []  # Triangle elements (volume)
    physical_names = {}
    boundary_elements = {"farfield": [], "airfoil": []}

    with open(msh_path, 'r') as f:
        content = f.read()

    lines = content.split('\n')

    # Detect format version
    msh_version = 2.2
    for line in lines[:5]:
        if '$MeshFormat' in line:
            continue
        parts = line.split()
        if parts and parts[0][0].isdigit():
            msh_version = float(parts[0])
            break

    print(f"Detected Gmsh format version: {msh_version}")

    # Parse based on version
    if msh_version >= 4.0:
        # Gmsh 4.x format
        return convert_gmsh4_to_su2(msh_path)
    else:
        # Gmsh 2.x format
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line == "$PhysicalNames":
                i += 1
                n_names = int(lines[i].strip())
                i += 1
                for _ in range(n_names):
                    parts = lines[i].strip().split()
                    dim = int(parts[0])
                    tag = int(parts[1])
                    name = parts[2].strip('"')
                    physical_names[tag] = {"dim": dim, "name": name}
                    i += 1

            elif line == "$Nodes":
                i += 1
                n_nodes = int(lines[i].strip())
                i += 1
                for _ in range(n_nodes):
                    parts = lines[i].strip().split()
                    node_id = int(parts[0])
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    nodes[node_id] = (x, y)
                    i += 1

            elif line == "$Elements":
                i += 1
                n_elems = int(lines[i].strip())
                i += 1
                for _ in range(n_elems):
                    parts = lines[i].strip().split()
                    elem_type = int(parts[1])
                    n_tags = int(parts[2])
                    physical_tag = int(parts[3]) if n_tags > 0 else 0
                    elem_nodes = [int(p) for p in parts[3 + n_tags:]]

                    if elem_type == 2:  # Triangle
                        elements.append(elem_nodes)
                    elif elem_type == 1:  # Line
                        if physical_tag in physical_names:
                            name = physical_names[physical_tag]["name"]
                            if name in boundary_elements:
                                boundary_elements[name].append(elem_nodes)
                    i += 1
            else:
                i += 1

    return write_su2_mesh(su2_path, nodes, elements, boundary_elements)


def convert_gmsh4_to_su2(msh_path):
    """Convert Gmsh 4.x format mesh to SU2."""

    su2_path = msh_path.with_suffix('.su2')

    nodes = {}
    elements = []
    boundary_elements = {"farfield": [], "airfoil": []}
    physical_names = {}
    entity_to_physical = {}  # Map entity tags to physical names

    with open(msh_path, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line == "$PhysicalNames":
            i += 1
            n_names = int(lines[i].strip())
            i += 1
            for _ in range(n_names):
                parts = lines[i].strip().split()
                dim = int(parts[0])
                tag = int(parts[1])
                name = parts[2].strip('"')
                physical_names[(dim, tag)] = name
                i += 1

        elif line == "$Entities":
            i += 1
            counts = [int(x) for x in lines[i].strip().split()]
            n_points, n_curves, n_surfaces = counts[0], counts[1], counts[2]
            n_volumes = counts[3] if len(counts) > 3 else 0
            i += 1

            # Skip points
            for _ in range(n_points):
                i += 1

            # Read curves (1D entities)
            for _ in range(n_curves):
                parts = lines[i].strip().split()
                entity_tag = int(parts[0])
                # Find number of physical tags (after bounding box)
                n_phys = int(parts[7]) if len(parts) > 7 else 0
                if n_phys > 0:
                    phys_tag = int(parts[8])
                    if (1, phys_tag) in physical_names:
                        entity_to_physical[(1, entity_tag)] = physical_names[(1, phys_tag)]
                i += 1

            # Read surfaces (2D entities)
            for _ in range(n_surfaces):
                parts = lines[i].strip().split()
                entity_tag = int(parts[0])
                n_phys = int(parts[7]) if len(parts) > 7 else 0
                if n_phys > 0:
                    phys_tag = int(parts[8])
                    if (2, phys_tag) in physical_names:
                        entity_to_physical[(2, entity_tag)] = physical_names[(2, phys_tag)]
                i += 1

            # Skip volumes
            for _ in range(n_volumes):
                i += 1

        elif line == "$Nodes":
            i += 1
            header = lines[i].strip().split()
            n_blocks = int(header[0])
            total_nodes = int(header[1])
            i += 1

            for _ in range(n_blocks):
                block_header = lines[i].strip().split()
                entity_dim = int(block_header[0])
                entity_tag = int(block_header[1])
                n_nodes_in_block = int(block_header[3])
                i += 1

                # Read node IDs
                node_ids = []
                for _ in range(n_nodes_in_block):
                    node_ids.append(int(lines[i].strip()))
                    i += 1

                # Read node coordinates
                for node_id in node_ids:
                    parts = lines[i].strip().split()
                    x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                    nodes[node_id] = (x, y)
                    i += 1

        elif line == "$Elements":
            i += 1
            header = lines[i].strip().split()
            n_blocks = int(header[0])
            total_elems = int(header[1])
            i += 1

            for _ in range(n_blocks):
                block_header = lines[i].strip().split()
                entity_dim = int(block_header[0])
                entity_tag = int(block_header[1])
                elem_type = int(block_header[2])
                n_elems_in_block = int(block_header[3])
                i += 1

                for _ in range(n_elems_in_block):
                    parts = [int(x) for x in lines[i].strip().split()]
                    elem_id = parts[0]
                    elem_nodes = parts[1:]

                    if elem_type == 2:  # Triangle
                        elements.append(elem_nodes)
                    elif elem_type == 1:  # Line
                        phys_name = entity_to_physical.get((entity_dim, entity_tag), "")
                        if phys_name in boundary_elements:
                            boundary_elements[phys_name].append(elem_nodes)
                    i += 1
        else:
            i += 1

    print(f"Read Gmsh 4.x mesh: {len(nodes)} nodes, {len(elements)} triangles")
    print(f"Boundaries: farfield={len(boundary_elements['farfield'])}, airfoil={len(boundary_elements['airfoil'])}")

    return write_su2_mesh(su2_path, nodes, elements, boundary_elements)


def write_su2_mesh(su2_path, nodes, elements, boundary_elements):
    """Write mesh in SU2 format."""

    if len(elements) == 0:
        print("ERROR: No triangle elements found in mesh!")
        return None

    # Create node mapping (1-based Gmsh to 0-based SU2)
    node_mapping = {old_id: new_id for new_id, old_id in enumerate(sorted(nodes.keys()))}

    with open(su2_path, 'w') as f:
        f.write("% SU2 Mesh generated from Gmsh\n")
        f.write("% MegaDrone CFD Validation\n")
        f.write("%\n")
        f.write("NDIME= 2\n")
        f.write("%\n")

        # Elements (triangles)
        f.write(f"NELEM= {len(elements)}\n")
        for idx, elem in enumerate(elements):
            n0 = node_mapping[elem[0]]
            n1 = node_mapping[elem[1]]
            n2 = node_mapping[elem[2]]
            f.write(f"5 {n0} {n1} {n2} {idx}\n")

        # Nodes
        f.write(f"NPOIN= {len(nodes)}\n")
        for old_id in sorted(nodes.keys()):
            x, y = nodes[old_id]
            new_id = node_mapping[old_id]
            f.write(f"{x:.10e} {y:.10e} {new_id}\n")

        # Boundary markers
        n_markers = len([k for k in boundary_elements if boundary_elements[k]])
        f.write(f"NMARK= {n_markers}\n")

        for marker_name, elems in boundary_elements.items():
            if elems:
                f.write(f"MARKER_TAG= {marker_name}\n")
                f.write(f"MARKER_ELEMS= {len(elems)}\n")
                for elem in elems:
                    n0 = node_mapping[elem[0]]
                    n1 = node_mapping[elem[1]]
                    f.write(f"3 {n0} {n1}\n")

    print(f"Converted to SU2 format: {su2_path}")
    return su2_path


# =============================================================================
# SU2 CONFIGURATION
# =============================================================================

def create_su2_config(condition_name, mesh_path):
    """Create SU2 configuration file for RANS analysis."""

    cond = FLIGHT_CONDITIONS[condition_name]

    config = f"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                              %
% SU2 Configuration File                                                       %
% MegaDrone Phase 1 - {condition_name.upper()} Condition                                %
%                                                                              %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% ------------- DIRECT, ADJOINT, AND LINEARIZED PROBLEM DEFINITION ------------%
SOLVER= RANS
KIND_TURB_MODEL= SA
MATH_PROBLEM= DIRECT
RESTART_SOL= NO

% -------------------- COMPRESSIBLE FREE-STREAM DEFINITION --------------------%
MACH_NUMBER= {cond['mach']:.4f}
AOA= {cond['alpha_deg']:.1f}
SIDESLIP_ANGLE= 0.0
FREESTREAM_OPTION= TEMPERATURE_FS
FREESTREAM_TEMPERATURE= 288.15
REYNOLDS_NUMBER= {cond['reynolds']:.0f}
REYNOLDS_LENGTH= {cond['ref_length_m']:.4f}

% ---------------------- REFERENCE VALUE DEFINITION ---------------------------%
REF_ORIGIN_MOMENT_X= 0.25
REF_ORIGIN_MOMENT_Y= 0.00
REF_ORIGIN_MOMENT_Z= 0.00
REF_LENGTH= {REF_LENGTH_M:.4f}
REF_AREA= 1.0

% -------------------- BOUNDARY CONDITION DEFINITION --------------------------%
MARKER_HEATFLUX= ( airfoil, 0.0 )
MARKER_FAR= ( farfield )

% ------------------------ SURFACES IDENTIFICATION ----------------------------%
MARKER_PLOTTING= ( airfoil )
MARKER_MONITORING= ( airfoil )
MARKER_DESIGNING= ( airfoil )

% ------------- COMMON PARAMETERS DEFINING THE NUMERICAL METHOD ---------------%
NUM_METHOD_GRAD= WEIGHTED_LEAST_SQUARES
CFL_NUMBER= 10.0
CFL_ADAPT= YES
CFL_ADAPT_PARAM= ( 0.1, 2.0, 10.0, 1e10 )

% ------------------------ LINEAR SOLVER DEFINITION ---------------------------%
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ERROR= 1E-6
LINEAR_SOLVER_ITER= 10

% -------------------- FLOW NUMERICAL METHOD DEFINITION -----------------------%
CONV_NUM_METHOD_FLOW= ROE
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
TIME_DISCRE_FLOW= EULER_IMPLICIT

% -------------------- TURBULENT NUMERICAL METHOD DEFINITION ------------------%
CONV_NUM_METHOD_TURB= SCALAR_UPWIND
MUSCL_TURB= NO
SLOPE_LIMITER_TURB= NONE
TIME_DISCRE_TURB= EULER_IMPLICIT

% --------------------------- CONVERGENCE PARAMETERS --------------------------%
CONV_RESIDUAL_MINVAL= -12
CONV_STARTITER= 10
CONV_CAUCHY_ELEMS= 100
CONV_CAUCHY_EPS= 1E-6

% ------------------------- INPUT/OUTPUT INFORMATION --------------------------%
MESH_FILENAME= {mesh_path.name}
MESH_FORMAT= SU2
SOLUTION_FILENAME= restart_flow.dat
RESTART_FILENAME= restart_flow.dat
CONV_FILENAME= history
VOLUME_FILENAME= flow
SURFACE_FILENAME= surface_flow
OUTPUT_WRT_FREQ= 100
SCREEN_WRT_FREQ_INNER= 1

% ------------------------ SCREEN OUTPUT DEFINITION ---------------------------%
SCREEN_OUTPUT= (INNER_ITER, RMS_DENSITY, RMS_NU_TILDE, LIFT, DRAG)

% ------------------------- HISTORY OUTPUT DEFINITION --------------------------%
HISTORY_OUTPUT= (ITER, RMS_RES, AERO_COEFF, FLOW_COEFF)

% ------------------------- FILE OUTPUT DEFINITION ----------------------------%
OUTPUT_FILES= (RESTART, PARAVIEW, SURFACE_PARAVIEW)
TABULAR_FORMAT= CSV

% ------------------------------- SOLVER CONTROL ------------------------------%
ITER= 5000
"""

    config_path = CFD_DIR / f"su2_config_{condition_name}.cfg"
    with open(config_path, 'w') as f:
        f.write(config)

    print(f"Created SU2 config: {config_path}")
    return config_path


# =============================================================================
# RUN SU2
# =============================================================================

def run_su2_analysis(config_path, mesh_path):
    """Run SU2 CFD analysis."""

    print(f"\n{'='*70}")
    print(f"Running SU2 Analysis: {config_path.stem}")
    print(f"{'='*70}")

    # Change to CFD directory for output files
    original_dir = os.getcwd()
    os.chdir(CFD_DIR)

    try:
        # Copy mesh to CFD directory if needed
        if not (CFD_DIR / mesh_path.name).exists():
            import shutil
            shutil.copy(mesh_path, CFD_DIR / mesh_path.name)

        # Run SU2_CFD
        su2_cfd = SU2_BIN / "SU2_CFD"
        result = subprocess.run(
            [str(su2_cfd), str(config_path.name)],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )

        print(result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout)

        if result.returncode != 0:
            print(f"Warning: SU2 returned non-zero exit code")
            print(result.stderr[-1000:])

    except subprocess.TimeoutExpired:
        print("Analysis timed out after 1 hour")
    except Exception as e:
        print(f"Error running SU2: {e}")
    finally:
        os.chdir(original_dir)

    # Parse results
    history_file = CFD_DIR / "history.csv"
    if history_file.exists():
        return parse_su2_history(history_file)
    else:
        print("Warning: No history file found")
        return None


def parse_su2_history(history_file):
    """Parse SU2 convergence history file."""

    import csv

    results = {
        "iterations": [],
        "cl": [],
        "cd": [],
        "rms_density": [],
    }

    with open(history_file, 'r') as f:
        # Read and clean header (remove quotes and whitespace)
        header_line = f.readline()
        headers = [h.strip().strip('"').strip() for h in header_line.split(',')]
        print(f"History columns: {headers[:10]}...")

        reader = csv.DictReader(f, fieldnames=headers)
        for row in reader:
            try:
                # Get iteration
                iter_val = 0
                for key in ["Inner_Iter", "Iteration", "Time_Iter"]:
                    if key in row and row[key]:
                        iter_val = int(float(row[key].strip()))
                        break
                results["iterations"].append(iter_val)

                # Get CL (try multiple possible column names)
                cl_val = 0.0
                for key in ["CL", "Lift_Coeff", "CD[0]", "LIFT"]:
                    clean_key = key.strip()
                    if clean_key in row and row[clean_key]:
                        try:
                            cl_val = float(row[clean_key].strip())
                            break
                        except ValueError:
                            continue
                results["cl"].append(cl_val)

                # Get CD
                cd_val = 0.0
                for key in ["CD", "Drag_Coeff", "CD[1]", "DRAG"]:
                    clean_key = key.strip()
                    if clean_key in row and row[clean_key]:
                        try:
                            cd_val = float(row[clean_key].strip())
                            break
                        except ValueError:
                            continue
                results["cd"].append(cd_val)

                # Get residual
                rms_val = 0.0
                for key in ["rms[Rho]", "RMS_Density", "Res_Flow[0]"]:
                    clean_key = key.strip()
                    if clean_key in row and row[clean_key]:
                        try:
                            rms_val = float(row[clean_key].strip())
                            break
                        except ValueError:
                            continue
                results["rms_density"].append(rms_val)

            except (ValueError, KeyError) as e:
                continue

    if results["cl"] and any(abs(cl) > 1e-10 for cl in results["cl"]):
        # Find non-zero values
        valid_cl = [cl for cl in results["cl"] if abs(cl) > 1e-10]
        valid_cd = [cd for cd in results["cd"] if abs(cd) > 1e-10]

        if valid_cl:
            final_cl = valid_cl[-1] if valid_cl else results["cl"][-1]
            final_cd = valid_cd[-1] if valid_cd else results["cd"][-1]
            final_ld = final_cl / final_cd if final_cd > 0 else 0

            print(f"\nFinal Results:")
            print(f"  CL = {final_cl:.4f}")
            print(f"  CD = {final_cd:.5f}")
            print(f"  L/D = {final_ld:.2f}")

            results["final_cl"] = final_cl
            results["final_cd"] = final_cd
            results["final_ld"] = final_ld
    else:
        print("\nWarning: No valid CL/CD data in history file")
        # Try to extract from the last values anyway
        if results["cl"]:
            results["final_cl"] = results["cl"][-1]
            results["final_cd"] = results["cd"][-1]
            results["final_ld"] = 0

    return results


# =============================================================================
# VALIDATION COMPARISON
# =============================================================================

def compare_results(cfd_results):
    """Compare CFD results with VLM predictions."""

    print("\n" + "="*70)
    print("CFD vs VLM Comparison")
    print("="*70)

    comparison = {}

    for condition, vlm in VLM_RESULTS.items():
        if condition in cfd_results and cfd_results[condition]:
            cfd = cfd_results[condition]

            cl_error = abs(cfd["final_cl"] - vlm["CL"]) / vlm["CL"] * 100
            cd_error = abs(cfd["final_cd"] - vlm["CD"]) / vlm["CD"] * 100
            ld_error = abs(cfd["final_ld"] - vlm["L/D"]) / vlm["L/D"] * 100

            print(f"\n{condition.upper()} CONDITION:")
            print(f"  Parameter  |    VLM    |    CFD    |   Error")
            print(f"  -----------|-----------|-----------|----------")
            print(f"  CL         |   {vlm['CL']:.4f}  |   {cfd['final_cl']:.4f}  |   {cl_error:.1f}%")
            print(f"  CD         |   {vlm['CD']:.5f} |   {cfd['final_cd']:.5f} |   {cd_error:.1f}%")
            print(f"  L/D        |   {vlm['L/D']:.2f}   |   {cfd['final_ld']:.2f}   |   {ld_error:.1f}%")

            comparison[condition] = {
                "cl_error": cl_error,
                "cd_error": cd_error,
                "ld_error": ld_error,
            }

    return comparison


def plot_convergence(cfd_results):
    """Plot convergence history."""

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    for condition, results in cfd_results.items():
        if results and results["iterations"]:
            iters = results["iterations"]

            # CL convergence
            axes[0, 0].plot(iters, results["cl"], label=condition)
            axes[0, 0].axhline(y=VLM_RESULTS[condition]["CL"], linestyle='--', alpha=0.7)

            # CD convergence
            axes[0, 1].plot(iters, results["cd"], label=condition)
            axes[0, 1].axhline(y=VLM_RESULTS[condition]["CD"], linestyle='--', alpha=0.7)

            # Residual
            axes[1, 0].semilogy(iters, [-r for r in results["rms_density"]], label=condition)

            # L/D
            ld = [cl/cd if cd > 0 else 0 for cl, cd in zip(results["cl"], results["cd"])]
            axes[1, 1].plot(iters, ld, label=condition)
            axes[1, 1].axhline(y=VLM_RESULTS[condition]["L/D"], linestyle='--', alpha=0.7)

    axes[0, 0].set_xlabel("Iteration")
    axes[0, 0].set_ylabel("CL")
    axes[0, 0].set_title("Lift Coefficient Convergence")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].set_xlabel("Iteration")
    axes[0, 1].set_ylabel("CD")
    axes[0, 1].set_title("Drag Coefficient Convergence")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].set_xlabel("Iteration")
    axes[1, 0].set_ylabel("RMS Density Residual")
    axes[1, 0].set_title("Convergence History")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].set_xlabel("Iteration")
    axes[1, 1].set_ylabel("L/D")
    axes[1, 1].set_title("Lift-to-Drag Ratio Convergence")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(DESIGNS_DIR / "cfd_convergence.png", dpi=150, bbox_inches='tight')
    print(f"\nSaved: {DESIGNS_DIR / 'cfd_convergence.png'}")
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main CFD validation routine."""

    print("="*70)
    print("MegaDrone Phase 1 - CFD Validation")
    print("="*70)

    # Create CFD directory
    CFD_DIR.mkdir(exist_ok=True)

    # Step 1: Generate mesh
    print("\n[Step 1] Generating 2D airfoil mesh...")
    mesh_path = create_2d_airfoil_mesh_gmsh()

    if mesh_path is None:
        print("\nMesh generation failed. Please install Gmsh:")
        print("  brew install gmsh")
        return

    # Step 2: Run CFD for each condition
    cfd_results = {}

    for condition in ["cruise"]:  # Start with cruise only
        print(f"\n[Step 2] Creating SU2 config for {condition}...")
        config_path = create_su2_config(condition, mesh_path)

        print(f"\n[Step 3] Running SU2 analysis for {condition}...")
        results = run_su2_analysis(config_path, mesh_path)
        cfd_results[condition] = results

    # Step 4: Compare results
    if any(cfd_results.values()):
        comparison = compare_results(cfd_results)

        # Step 5: Plot convergence
        print("\n[Step 4] Plotting convergence...")
        plot_convergence(cfd_results)

        # Summary
        print("\n" + "="*70)
        print("CFD VALIDATION SUMMARY")
        print("="*70)
        for cond, errs in comparison.items():
            print(f"\n{cond.upper()}:")
            print(f"  CL error: {errs['cl_error']:.1f}% (target < 5%)")
            print(f"  CD error: {errs['cd_error']:.1f}% (target < 10%)")
            print(f"  L/D error: {errs['ld_error']:.1f}% (target < 10%)")

            if errs['cl_error'] < 5 and errs['cd_error'] < 10:
                print("  STATUS: VALIDATED")
            else:
                print("  STATUS: NEEDS REVIEW")
    else:
        print("\nNo CFD results obtained. Check error messages above.")

    return cfd_results


if __name__ == "__main__":
    results = main()
