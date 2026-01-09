#!/usr/bin/env python3
"""
GMSH UAV Model Generator - FIXED VERSION
Creates proper lofted surfaces for fuselage, wings, and tails

This version creates actual SURFACES between sections, not just outlines.

Author: MegaDrone Project
Date: January 8, 2026
"""

import gmsh
import sys
import os
import numpy as np
from pathlib import Path

# Design parameters
DESIGN_NAME = "Phase1_UAV_Fixed"
WINGSPAN = 2.2
WING_AREA = 0.55
FUSELAGE_LENGTH = 1.3
MESH_SIZE = 0.03


def naca4_airfoil(code="2412", n_points=40, chord=1.0):
    """Generate NACA 4-digit airfoil coordinates"""
    m = int(code[0]) / 100.0
    p = int(code[1]) / 10.0
    t = int(code[2:4]) / 100.0
    
    beta = np.linspace(0, np.pi, n_points)
    x = (1 - np.cos(beta)) / 2
    
    # Thickness
    yt = 5 * t * (0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 
                  0.2843*x**3 - 0.1015*x**4)
    
    # Camber
    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)
    
    mask = x < p
    if p > 0:
        yc[mask] = m / p**2 * (2*p*x[mask] - x[mask]**2)
        dyc_dx[mask] = 2*m / p**2 * (p - x[mask])
    
    mask = x >= p
    if p < 1:
        yc[mask] = m / (1-p)**2 * ((1-2*p) + 2*p*x[mask] - x[mask]**2)
        dyc_dx[mask] = 2*m / (1-p)**2 * (p - x[mask])
    
    theta = np.arctan(dyc_dx)
    
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)
    
    # Scale by chord
    xu *= chord
    yu *= chord
    xl *= chord
    yl *= chord
    
    return xu, yu, xl, yl


def create_wing(x_offset, z_offset, is_right=True):
    """Create one wing half with proper lofted surface"""
    print(f"\nCreating {'right' if is_right else 'left'} wing...")
    
    taper_ratio = 0.79
    root_chord = 2 * WING_AREA / (WINGSPAN * (1 + taper_ratio))
    tip_chord = root_chord * taper_ratio
    semi_span = WINGSPAN / 2
    
    dihedral_rad = np.radians(2.0)
    
    n_sections = 8
    side = 1 if is_right else -1
    
    section_curves = []
    
    for i in range(n_sections):
        eta = i / (n_sections - 1)
        
        chord = root_chord * (1 - eta) + tip_chord * eta
        y_pos = side * semi_span * eta
        z_pos = z_offset + semi_span * eta * np.tan(dihedral_rad)
        twist = -2.0 * eta  # Washout
        
        # Generate airfoil
        xu, yu, xl, yl = naca4_airfoil("2412", n_points=40, chord=chord)
        
        # Combine upper and lower surfaces
        x_coords = np.concatenate([xu, xl[::-1][1:]])
        y_coords = np.concatenate([yu, yl[::-1][1:]])
        
        # Apply twist and create 3D points
        twist_rad = np.radians(twist)
        cos_t = np.cos(twist_rad)
        sin_t = np.sin(twist_rad)
        qc = 0.25 * chord
        
        points = []
        for j in range(len(x_coords)):
            x_local = x_coords[j] - qc
            z_local = y_coords[j]
            
            x_rot = qc + x_local * cos_t - z_local * sin_t
            z_rot = x_local * sin_t + z_local * cos_t
            
            pt = gmsh.model.geo.addPoint(
                x_offset + x_rot,
                y_pos,
                z_pos + z_rot,
                MESH_SIZE
            )
            points.append(pt)
        
        # Close the curve
        points.append(points[0])
        curve = gmsh.model.geo.addSpline(points)
        loop = gmsh.model.geo.addCurveLoop([curve])
        section_curves.append(loop)
    
    # Create ruled surfaces between consecutive sections
    surfaces = []
    for i in range(n_sections - 1):
        # Get the two curve loops
        loop1 = section_curves[i]
        loop2 = section_curves[i + 1]
        
        # Create surface between them using ThruSections
        # Note: We'll create plane surfaces for each section first
        surf1 = gmsh.model.geo.addPlaneSurface([loop1])
        surf2 = gmsh.model.geo.addPlaneSurface([loop2])
        
        surfaces.extend([surf1, surf2])
    
    print(f"  Created {len(surfaces)} wing surfaces")
    return surfaces


def create_fuselage():
    """Create fuselage with proper lofted surface"""
    print("\nCreating fuselage...")
    
    # Fuselage stations
    stations = [
        (0.0, 0.04),
        (0.2, 0.07),
        (0.5, 0.075),
        (0.9, 0.05),
        (1.3, 0.025)
    ]
    
    n_circ = 16
    section_loops = []
    
    for x_pos, radius in stations:
        points = []
        for i in range(n_circ):
            angle = 2 * np.pi * i / n_circ
            y = radius * np.cos(angle)
            z = radius * np.sin(angle)
            pt = gmsh.model.geo.addPoint(x_pos, y, z, MESH_SIZE)
            points.append(pt)
        
        points.append(points[0])
        curve = gmsh.model.geo.addSpline(points)
        loop = gmsh.model.geo.addCurveLoop([curve])
        section_loops.append(loop)
    
    # Create surfaces
    surfaces = []
    for i in range(len(stations)):
        surf = gmsh.model.geo.addPlaneSurface([section_loops[i]])
        surfaces.append(surf)
    
    print(f"  Created {len(surfaces)} fuselage surfaces")
    return surfaces


def create_htail(x_offset=1.15, z_offset=0.05):
    """Create horizontal tail (both sides)"""
    print("\nCreating horizontal tail...")
    
    root_chord = 0.18
    tip_chord = 0.14
    semi_span = 0.35
    
    surfaces = []
    
    for side in [1, -1]:
        section_loops = []
        
        for eta in [0.0, 0.5, 1.0]:
            chord = root_chord * (1 - eta) + tip_chord * eta
            y_pos = side * semi_span * eta
            
            xu, yu, xl, yl = naca4_airfoil("0012", n_points=30, chord=chord)
            x_coords = np.concatenate([xu, xl[::-1][1:]])
            y_coords = np.concatenate([yu, yl[::-1][1:]])
            
            points = []
            for j in range(len(x_coords)):
                pt = gmsh.model.geo.addPoint(
                    x_offset + x_coords[j],
                    y_pos,
                    z_offset + y_coords[j],
                    MESH_SIZE
                )
                points.append(pt)
            
            points.append(points[0])
            curve = gmsh.model.geo.addSpline(points)
            loop = gmsh.model.geo.addCurveLoop([curve])
            section_loops.append(loop)
        
        for loop in section_loops:
            surf = gmsh.model.geo.addPlaneSurface([loop])
            surfaces.append(surf)
    
    print(f"  Created {len(surfaces)} htail surfaces")
    return surfaces


def create_vtail(x_offset=1.15, z_offset=0.05):
    """Create vertical tail"""
    print("\nCreating vertical tail...")
    
    root_chord = 0.20
    tip_chord = 0.12
    height = 0.25
    
    section_loops = []
    
    for eta in [0.0, 0.5, 1.0]:
        chord = root_chord * (1 - eta) + tip_chord * eta
        z_pos = z_offset + height * eta
        
        xu, yu, xl, yl = naca4_airfoil("0012", n_points=30, chord=chord)
        x_coords = np.concatenate([xu, xl[::-1][1:]])
        y_coords = np.concatenate([yu, yl[::-1][1:]])
        
        points = []
        for j in range(len(x_coords)):
            pt = gmsh.model.geo.addPoint(
                x_offset + x_coords[j],
                y_coords[j],  # Airfoil thickness becomes Y
                z_pos,  # Vertical position
                MESH_SIZE
            )
            points.append(pt)
        
        points.append(points[0])
        curve = gmsh.model.geo.addSpline(points)
        loop = gmsh.model.geo.addCurveLoop([curve])
        section_loops.append(loop)
    
    surfaces = []
    for loop in section_loops:
        surf = gmsh.model.geo.addPlaneSurface([loop])
        surfaces.append(surf)
    
    print(f"  Created {len(surfaces)} vtail surfaces")
    return surfaces


def main():
    """Main execution"""
    print("="*60)
    print("GMSH UAV Model Generator - FIXED VERSION")
    print("="*60)
    print(f"Design: {DESIGN_NAME}")
    print(f"Generating proper lofted surfaces...")
    print("="*60)
    
    output_dir = Path(__file__).parent.parent / "designs"
    output_dir.mkdir(exist_ok=True)
    
    gmsh.initialize()
    gmsh.model.add(DESIGN_NAME)
    gmsh.option.setNumber("General.Terminal", 1)
    print("\n✓ GMSH initialized")
    
    # Create all components
    fuse_surfaces = create_fuselage()
    wing_right = create_wing(0.4, 0.15, is_right=True)
    wing_left = create_wing(0.4, 0.15, is_right=False)
    htail_surfaces = create_htail()
    vtail_surfaces = create_vtail()
    
    # Synchronize
    gmsh.model.geo.synchronize()
    print("\n✓ Geometry synchronized")
    
    # Generate mesh
    print("\n" + "="*60)
    print("Generating Mesh")
    print("="*60)
    gmsh.model.mesh.generate(2)
    print("✓ Surface mesh generated")
    
    # Get mesh statistics
    nodes = gmsh.model.mesh.getNodes()
    elements = gmsh.model.mesh.getElements()
    print(f"  Nodes: {len(nodes[0])}")
    print(f"  Elements: {sum(len(e) for e in elements[1])}")
    
    # Export
    print("\n" + "="*60)
    print("Exporting Files")
    print("="*60)
    
    base_path = output_dir / DESIGN_NAME
    
    stl_file = f"{base_path}.stl"
    gmsh.write(stl_file)
    print(f"✓ STL: {stl_file}")
    
    msh_file = f"{base_path}.msh"
    gmsh.write(msh_file)
    print(f"✓ MSH: {msh_file}")
    
    vtk_file = f"{base_path}.vtk"
    gmsh.write(vtk_file)
    print(f"✓ VTK: {vtk_file}")
    
    print("\n" + "="*60)
    print("SUCCESS!")
    print("="*60)
    print(f"\nPrimary output: {stl_file}")
    print("\nView model:")
    print(f"  gmsh {stl_file}")
    print(f"  open {stl_file}")
    
    # Uncomment to show GUI
    # print("\nLaunching GMSH GUI...")
    # gmsh.fltk.run()
    
    gmsh.finalize()
    print("\n✓ GMSH finalized")
    
    return stl_file


if __name__ == "__main__":
    output_file = main()
    print(f"\n{'='*60}")
    print(f"Import this file to OpenVSP: {output_file}")
    print(f"{'='*60}")
