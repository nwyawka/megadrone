#!/usr/bin/env python3
"""
Simplified GMSH UAV Model Generator
Creates parametric fixed-wing UAV geometry using GMSH Python API

This version focuses on reliable STL export for 3D printing and visualization.
For OpenVSP import, we'll export STL and use conversion tools or OpenVSP's STL import.

Phase 1 Specifications:
- Wingspan: 2.2 m (7.2 ft)
- Wing Area: 0.55 m² (5.9 ft²)  
- Configuration: High wing, pusher propeller, H-tail

Author: MegaDrone Project
Date: January 8, 2026
"""

import gmsh
import sys
import os
import numpy as np
from pathlib import Path

# Design parameters
DESIGN_NAME = "Phase1_UAV_GMSH"
WINGSPAN = 2.2
WING_AREA = 0.55
FUSELAGE_LENGTH = 1.3
MESH_SIZE = 0.05


def naca4_airfoil(code="2412", n_points=50, chord=1.0):
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
    
    # Scale by chord and combine
    xu *= chord
    yu *= chord
    xl *= chord
    yl *= chord
    
    # Return closed airfoil (upper surface + lower surface reversed)
    x_coords = np.concatenate([xu, xl[::-1][1:-1]])
    y_coords = np.concatenate([yu, yl[::-1][1:-1]])
    
    return x_coords, y_coords


def create_wing_surface(x_offset, z_offset, wingspan, root_chord, tip_chord, n_sections=5):
    """Create wing surface with splines"""
    print(f"\nCreating wing: span={wingspan}m, root_chord={root_chord:.3f}m")
    
    semi_span = wingspan / 2
    taper = tip_chord / root_chord
    dihedral = 2.0  # degrees
    dihedral_rad = np.radians(dihedral)
    
    all_surfaces = []
    
    for side_multiplier in [1, -1]:  # Right and left wings
        for i in range(n_sections - 1):
            eta1 = i / (n_sections - 1)
            eta2 = (i + 1) / (n_sections - 1)
            
            # Section 1
            chord1 = root_chord * (1 + (taper - 1) * eta1)
            y1 = side_multiplier * semi_span * eta1
            z1 = z_offset + semi_span * eta1 * np.tan(dihedral_rad)
            twist1 = -2.0 * eta1  # Washout
            
            # Section 2  
            chord2 = root_chord * (1 + (taper - 1) * eta2)
            y2 = side_multiplier * semi_span * eta2
            z2 = z_offset + semi_span * eta2 * np.tan(dihedral_rad)
            twist2 = -2.0 * eta2
            
            # Generate airfoils
            x1, z1_airfoil = naca4_airfoil("2412", n_points=30, chord=chord1)
            x2, z2_airfoil = naca4_airfoil("2412", n_points=30, chord=chord2)
            
            # Create points for section 1
            pts1 = []
            for j in range(len(x1)):
                # Apply twist
                x_tw = x1[j] * np.cos(np.radians(twist1)) - z1_airfoil[j] * np.sin(np.radians(twist1))
                z_tw = x1[j] * np.sin(np.radians(twist1)) + z1_airfoil[j] * np.cos(np.radians(twist1))
                pt = gmsh.model.geo.addPoint(x_offset + x_tw, y1, z1 + z_tw, MESH_SIZE)
                pts1.append(pt)
            
            # Create points for section 2
            pts2 = []
            for j in range(len(x2)):
                x_tw = x2[j] * np.cos(np.radians(twist2)) - z2_airfoil[j] * np.sin(np.radians(twist2))
                z_tw = x2[j] * np.sin(np.radians(twist2)) + z2_airfoil[j] * np.cos(np.radians(twist2))
                pt = gmsh.model.geo.addPoint(x_offset + x_tw, y2, z2 + z_tw, MESH_SIZE)
                pts2.append(pt)
            
            # Create splines
            pts1.append(pts1[0])
            spline1 = gmsh.model.geo.addSpline(pts1)
            loop1 = gmsh.model.geo.addCurveLoop([spline1])
            surf1 = gmsh.model.geo.addPlaneSurface([loop1])
            
            pts2.append(pts2[0])
            spline2 = gmsh.model.geo.addSpline(pts2)
            loop2 = gmsh.model.geo.addCurveLoop([spline2])
            surf2 = gmsh.model.geo.addPlaneSurface([loop2])
            
            all_surfaces.extend([surf1, surf2])
    
    return all_surfaces


def create_fuselage(length, max_radius):
    """Create streamlined fuselage"""
    print(f"\nCreating fuselage: length={length}m, max_radius={max_radius}m")
    
    stations = [
        (0.0, 0.04),
        (0.15, 0.07),
        (0.45, 0.075),
        (0.9, 0.05),
        (length, 0.025)
    ]
    
    surfaces = []
    n_circ = 12
    
    for idx in range(len(stations) - 1):
        x1, r1 = stations[idx]
        x2, r2 = stations[idx + 1]
        
        # Create two circular sections
        pts1 = []
        pts2 = []
        
        for i in range(n_circ):
            angle = 2 * np.pi * i / n_circ
            y = np.cos(angle)
            z = np.sin(angle)
            
            pt1 = gmsh.model.geo.addPoint(x1, r1*y, r1*z, MESH_SIZE)
            pt2 = gmsh.model.geo.addPoint(x2, r2*y, r2*z, MESH_SIZE)
            pts1.append(pt1)
            pts2.append(pt2)
        
        # Close loops
        pts1.append(pts1[0])
        pts2.append(pts2[0])
        
        # Create circles
        circle1 = gmsh.model.geo.addSpline(pts1)
        circle2 = gmsh.model.geo.addSpline(pts2)
        
        loop1 = gmsh.model.geo.addCurveLoop([circle1])
        loop2 = gmsh.model.geo.addCurveLoop([circle2])
        
        surf1 = gmsh.model.geo.addPlaneSurface([loop1])
        surf2 = gmsh.model.geo.addPlaneSurface([loop2])
        
        surfaces.extend([surf1, surf2])
    
    return surfaces


def create_tail(x_offset, z_offset, span, root_chord, tip_chord, is_vertical=False):
    """Create horizontal or vertical tail"""
    tail_type = "vertical" if is_vertical else "horizontal"
    print(f"\nCreating {tail_type} tail: span={span}m")
    
    n_pts = 20
    x, z_airfoil = naca4_airfoil("0012", n_points=n_pts, chord=1.0)
    
    surfaces = []
    
    for side_mult in ([0] if is_vertical else [1, -1]):
        # Root section
        pts_root = []
        for i in range(len(x)):
            if is_vertical:
                pt = gmsh.model.geo.addPoint(
                    x_offset + x[i] * root_chord,
                    0,
                    z_offset + z_airfoil[i] * root_chord,
                    MESH_SIZE
                )
            else:
                pt = gmsh.model.geo.addPoint(
                    x_offset + x[i] * root_chord,
                    side_mult * 0,
                    z_offset + z_airfoil[i] * root_chord,
                    MESH_SIZE
                )
            pts_root.append(pt)
        
        # Tip section
        pts_tip = []
        for i in range(len(x)):
            if is_vertical:
                pt = gmsh.model.geo.addPoint(
                    x_offset + x[i] * tip_chord,
                    0,
                    z_offset + span + z_airfoil[i] * tip_chord,
                    MESH_SIZE
                )
            else:
                pt = gmsh.model.geo.addPoint(
                    x_offset + x[i] * tip_chord,
                    side_mult * span / 2,
                    z_offset + z_airfoil[i] * tip_chord,
                    MESH_SIZE
                )
            pts_tip.append(pt)
        
        pts_root.append(pts_root[0])
        pts_tip.append(pts_tip[0])
        
        spline_root = gmsh.model.geo.addSpline(pts_root)
        spline_tip = gmsh.model.geo.addSpline(pts_tip)
        
        loop_root = gmsh.model.geo.addCurveLoop([spline_root])
        loop_tip = gmsh.model.geo.addCurveLoop([spline_tip])
        
        surf_root = gmsh.model.geo.addPlaneSurface([loop_root])
        surf_tip = gmsh.model.geo.addPlaneSurface([loop_tip])
        
        surfaces.extend([surf_root, surf_tip])
    
    return surfaces


def main():
    """Main execution"""
    print("="*60)
    print("GMSH UAV Model Generator - Simplified Version")
    print("="*60)
    print(f"Design: {DESIGN_NAME}")
    print(f"Wingspan: {WINGSPAN} m")
    print(f"Wing Area: {WING_AREA} m²")
    print("="*60)
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "designs"
    output_dir.mkdir(exist_ok=True)
    
    # Initialize GMSH
    gmsh.initialize()
    gmsh.model.add(DESIGN_NAME)
    gmsh.option.setNumber("General.Terminal", 1)
    print("\n✓ GMSH initialized")
    
    # Calculate wing parameters
    taper_ratio = 0.79
    root_chord = 2 * WING_AREA / (WINGSPAN * (1 + taper_ratio))
    tip_chord = root_chord * taper_ratio
    
    print(f"\nWing parameters:")
    print(f"  Root chord: {root_chord:.3f} m")
    print(f"  Tip chord: {tip_chord:.3f} m")
    print(f"  Taper ratio: {taper_ratio}")
    
    # Create geometry
    fuse_surfaces = create_fuselage(FUSELAGE_LENGTH, 0.075)
    wing_surfaces = create_wing_surface(0.4, 0.15, WINGSPAN, root_chord, tip_chord)
    htail_surfaces = create_tail(1.15, 0.05, 0.7, 0.18, 0.14, is_vertical=False)
    vtail_surfaces = create_tail(1.15, 0.05, 0.25, 0.20, 0.12, is_vertical=True)
    
    # Synchronize
    gmsh.model.geo.synchronize()
    print("\n✓ Geometry synchronized")
    
    # Generate mesh
    print("\n" + "="*60)
    print("Generating Surface Mesh")
    print("="*60)
    gmsh.model.mesh.generate(2)  # 2D surface mesh
    print("✓ Surface mesh generated")
    
    # Export files
    print("\n" + "="*60)
    print("Exporting Files")
    print("="*60)
    
    base_path = output_dir / DESIGN_NAME
    
    # STL (works reliably with built-in kernel)
    stl_file = f"{base_path}.stl"
    gmsh.write(stl_file)
    print(f"✓ STL exported: {stl_file}")
    
    # MSH (native GMSH mesh format)
    msh_file = f"{base_path}.msh"
    gmsh.write(msh_file)
    print(f"✓ MSH exported: {msh_file}")
    
    # VTK (for ParaView visualization)
    vtk_file = f"{base_path}.vtk"
    gmsh.write(vtk_file)
    print(f"✓ VTK exported: {vtk_file}")
    
    # GEO unrolled (GMSH script)
    geo_file = f"{base_path}.geo_unrolled"
    gmsh.write(geo_file)
    print(f"✓ GEO exported: {geo_file}")
    
    print("\n" + "="*60)
    print("Generation Complete!")
    print("="*60)
    
    print("\nGenerated Files:")
    print(f"  • {stl_file}  <- Import this into OpenVSP or use for 3D printing")
    print(f"  • {msh_file}  <- GMSH native mesh format")
    print(f"  • {vtk_file}  <- Visualize in ParaView")
    print(f"  • {geo_file}  <- GMSH script (can edit and re-run)")
    
    print("\nNext Steps:")
    print("1. Import STL into OpenVSP:")
    print("   File → Import → Import File → Select .stl")
    print("2. Or convert STL to STEP using FreeCAD/Blender")
    print("3. View in GMSH GUI: gmsh " + stl_file)
    print("4. Use STL for 3D printing or CFD preprocessing")
    
    # Uncomment to show GUI
    # print("\nLaunching GMSH GUI...")
    # gmsh.fltk.run()
    
    gmsh.finalize()
    print("\n✓ GMSH finalized")
    
    return str(stl_file)


if __name__ == "__main__":
    stl_path = main()
    print(f"\n{'='*60}")
    print(f"PRIMARY OUTPUT: {stl_path}")
    print(f"{'='*60}")
