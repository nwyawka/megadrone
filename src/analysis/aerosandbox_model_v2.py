#!/usr/bin/env python3
"""
AeroSandbox Aircraft Model V2
Uses optimized airfoil from NeuralFoil optimization

Updates from V1:
- Integrates custom optimized airfoil
- Refined tail sizing
- Updated CG location

Author: MegaDrone Project
Date: January 8, 2026
"""

import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import os

# =============================================================================
# DESIGN PARAMETERS (from sizing - converged values)
# =============================================================================

# Aircraft parameters
TOTAL_WEIGHT_KG = 1.96
WINGSPAN_M = 1.70
WING_AREA_M2 = 0.241
ASPECT_RATIO = 12.0
MEAN_CHORD_M = 0.1416
TAPER_RATIO = 0.7

# Derived parameters
ROOT_CHORD_M = 2 * MEAN_CHORD_M / (1 + TAPER_RATIO)  # ~0.167 m
TIP_CHORD_M = ROOT_CHORD_M * TAPER_RATIO  # ~0.117 m
SEMI_SPAN_M = WINGSPAN_M / 2  # 0.85 m

# Flight conditions
CRUISE_SPEED_MS = 25.7
LOITER_SPEED_MS = 15.0
ALTITUDE_M = 150
RHO = 1.21  # kg/m³ at 150m

# Fuselage dimensions
FUSELAGE_LENGTH_M = 0.45
FUSELAGE_WIDTH_M = 0.12
FUSELAGE_HEIGHT_M = 0.10

# Tail sizing (refined)
HTAIL_VOLUME_COEFF = 0.55  # Slightly increased for stability
VTAIL_VOLUME_COEFF = 0.045
TAIL_ARM_M = 0.50  # Distance from wing quarter chord to tail quarter chord

# =============================================================================
# LOAD OPTIMIZED AIRFOIL
# =============================================================================

def load_optimized_airfoil():
    """Load the NeuralFoil-optimized airfoil coordinates."""

    airfoil_path = os.path.join(
        os.path.dirname(__file__),
        "..", "designs", "optimized_airfoil.dat"
    )

    if os.path.exists(airfoil_path):
        print("Loading optimized airfoil from:", airfoil_path)
        coords = np.loadtxt(airfoil_path)

        # Create custom airfoil from coordinates
        airfoil = asb.Airfoil(
            name="MegaDrone_Optimized",
            coordinates=coords,
        )
        return airfoil
    else:
        print("Warning: Optimized airfoil not found, using E387 fallback")
        return asb.Airfoil("e387")


def get_tail_airfoil():
    """Get symmetric airfoil for tail surfaces."""
    return asb.Airfoil("naca0010")


# =============================================================================
# AIRCRAFT GEOMETRY
# =============================================================================

def create_main_wing(airfoil):
    """Create main wing with optimized airfoil."""

    wing = asb.Wing(
        name="Main Wing",
        symmetric=True,
        xsecs=[
            asb.WingXSec(
                xyz_le=[0, 0, 0],
                chord=ROOT_CHORD_M,
                twist=2.0,  # 2 degrees incidence at root
                airfoil=airfoil,
            ),
            asb.WingXSec(
                xyz_le=[
                    (ROOT_CHORD_M - TIP_CHORD_M) * 0.25,  # Quarter-chord alignment
                    SEMI_SPAN_M,
                    SEMI_SPAN_M * np.tan(np.radians(3)),  # 3 degrees dihedral
                ],
                chord=TIP_CHORD_M,
                twist=-1.0,  # 3 degrees total washout
                airfoil=airfoil,
            ),
        ],
    )

    return wing


def create_horizontal_tail():
    """Create horizontal stabilizer with refined sizing."""

    tail_airfoil = get_tail_airfoil()

    # Size based on tail volume coefficient
    htail_area = HTAIL_VOLUME_COEFF * WING_AREA_M2 * MEAN_CHORD_M / TAIL_ARM_M
    htail_ar = 4.0  # Aspect ratio for horizontal tail
    htail_span = np.sqrt(htail_area * htail_ar)
    htail_chord = htail_area / htail_span
    htail_taper = 0.8  # Slight taper

    htail_root = htail_chord / (0.5 * (1 + htail_taper))
    htail_tip = htail_root * htail_taper

    htail = asb.Wing(
        name="Horizontal Tail",
        symmetric=True,
        xsecs=[
            asb.WingXSec(
                xyz_le=[TAIL_ARM_M + MEAN_CHORD_M * 0.25, 0, 0],
                chord=htail_root,
                twist=0,
                airfoil=tail_airfoil,
            ),
            asb.WingXSec(
                xyz_le=[
                    TAIL_ARM_M + MEAN_CHORD_M * 0.25 + (htail_root - htail_tip) * 0.25,
                    htail_span / 2,
                    0,
                ],
                chord=htail_tip,
                twist=0,
                airfoil=tail_airfoil,
            ),
        ],
    )

    return htail, htail_area, htail_span


def create_vertical_tail():
    """Create vertical stabilizer."""

    tail_airfoil = get_tail_airfoil()

    # Size based on tail volume coefficient
    vtail_area = VTAIL_VOLUME_COEFF * WING_AREA_M2 * WINGSPAN_M / TAIL_ARM_M
    vtail_ar = 1.5
    vtail_height = np.sqrt(vtail_area * vtail_ar)
    vtail_chord = vtail_area / vtail_height
    vtail_taper = 0.5

    vtail_root = vtail_chord / (0.5 * (1 + vtail_taper))
    vtail_tip = vtail_root * vtail_taper

    vtail = asb.Wing(
        name="Vertical Tail",
        symmetric=False,
        xsecs=[
            asb.WingXSec(
                xyz_le=[TAIL_ARM_M + MEAN_CHORD_M * 0.25, 0, 0],
                chord=vtail_root,
                twist=0,
                airfoil=tail_airfoil,
            ),
            asb.WingXSec(
                xyz_le=[
                    TAIL_ARM_M + MEAN_CHORD_M * 0.25 + (vtail_root - vtail_tip) * 0.3,
                    0,
                    vtail_height,
                ],
                chord=vtail_tip,
                twist=0,
                airfoil=tail_airfoil,
            ),
        ],
    )

    return vtail, vtail_area, vtail_height


def create_fuselage():
    """Create fuselage for camera pod payload."""

    # Pod fuselage centered under wing
    fuselage = asb.Fuselage(
        name="Fuselage",
        xsecs=[
            asb.FuselageXSec(
                xyz_c=[-FUSELAGE_LENGTH_M * 0.2, 0, -FUSELAGE_HEIGHT_M * 0.4],
                radius=0.01,  # Nose point
            ),
            asb.FuselageXSec(
                xyz_c=[0, 0, -FUSELAGE_HEIGHT_M * 0.4],
                width=FUSELAGE_WIDTH_M * 0.7,
                height=FUSELAGE_HEIGHT_M * 0.7,
            ),
            asb.FuselageXSec(
                xyz_c=[FUSELAGE_LENGTH_M * 0.4, 0, -FUSELAGE_HEIGHT_M * 0.4],
                width=FUSELAGE_WIDTH_M,
                height=FUSELAGE_HEIGHT_M,
            ),
            asb.FuselageXSec(
                xyz_c=[FUSELAGE_LENGTH_M * 0.7, 0, -FUSELAGE_HEIGHT_M * 0.4],
                width=FUSELAGE_WIDTH_M * 0.7,
                height=FUSELAGE_HEIGHT_M * 0.7,
            ),
            asb.FuselageXSec(
                xyz_c=[FUSELAGE_LENGTH_M, 0, -FUSELAGE_HEIGHT_M * 0.4],
                radius=0.02,  # Tail boom attachment
            ),
        ],
    )

    return fuselage


def create_aircraft():
    """Create complete aircraft model with optimized airfoil."""

    print("=" * 60)
    print("Creating AeroSandbox Aircraft Model V2")
    print("=" * 60)

    # Load optimized airfoil
    wing_airfoil = load_optimized_airfoil()

    # Create components
    wing = create_main_wing(wing_airfoil)
    htail, htail_area, htail_span = create_horizontal_tail()
    vtail, vtail_area, vtail_height = create_vertical_tail()
    fuselage = create_fuselage()

    # CG location (approximately 25% MAC from leading edge)
    # For stability, CG should be ahead of aerodynamic center
    cg_x = MEAN_CHORD_M * 0.25
    cg_y = 0
    cg_z = -FUSELAGE_HEIGHT_M * 0.2

    # Assemble aircraft
    aircraft = asb.Airplane(
        name="MegaDrone Phase1 V2",
        xyz_ref=[cg_x, cg_y, cg_z],
        wings=[wing, htail, vtail],
        fuselages=[fuselage],
    )

    # Print summary
    print(f"\n--- CONFIGURATION ---")
    print(f"  Wing Airfoil: {wing_airfoil.name}")
    print(f"  CG Location:  ({cg_x:.3f}, {cg_y:.3f}, {cg_z:.3f}) m")

    print(f"\n--- MAIN WING ---")
    print(f"  Span:       {WINGSPAN_M:.3f} m")
    print(f"  Root Chord: {ROOT_CHORD_M:.4f} m")
    print(f"  Tip Chord:  {TIP_CHORD_M:.4f} m")
    print(f"  Area:       {WING_AREA_M2:.4f} m²")
    print(f"  AR:         {ASPECT_RATIO:.1f}")

    print(f"\n--- HORIZONTAL TAIL ---")
    print(f"  Span:       {htail_span:.3f} m")
    print(f"  Area:       {htail_area:.4f} m²")
    print(f"  Volume:     {HTAIL_VOLUME_COEFF:.2f}")

    print(f"\n--- VERTICAL TAIL ---")
    print(f"  Height:     {vtail_height:.3f} m")
    print(f"  Area:       {vtail_area:.4f} m²")
    print(f"  Volume:     {VTAIL_VOLUME_COEFF:.3f}")

    return aircraft, wing_airfoil


def visualize_aircraft(aircraft):
    """Create 3D visualization."""

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(14, 10))

    aircraft.draw(
        backend="matplotlib",
        ax=ax,
        show=False,
    )

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("MegaDrone Phase 1 V2 - With Optimized Airfoil", fontsize=14)

    # Set equal aspect ratio
    max_range = WINGSPAN_M / 2
    ax.set_xlim([-max_range * 0.3, max_range * 1.5])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range * 0.4, max_range * 0.4])

    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/aerosandbox_model_v2.png',
                dpi=150, bbox_inches='tight')
    print("\nSaved: designs/aerosandbox_model_v2.png")

    plt.show()

    return fig


def run_quick_analysis(aircraft):
    """Run quick VLM analysis to verify model."""

    print("\n" + "=" * 60)
    print("Quick VLM Verification")
    print("=" * 60)

    op_point = asb.OperatingPoint(
        atmosphere=asb.Atmosphere(altitude=ALTITUDE_M),
        velocity=CRUISE_SPEED_MS,
        alpha=3.0,
        beta=0,
    )

    vlm = asb.VortexLatticeMethod(
        airplane=aircraft,
        op_point=op_point,
        spanwise_resolution=12,
        chordwise_resolution=6,
    )

    aero = vlm.run()

    # Add parasite drag estimate
    cd0 = 0.018  # Slightly lower with optimized airfoil
    cd_total = cd0 + aero.get('CD', 0)
    ld = aero['CL'] / cd_total if cd_total > 0 else 0

    print(f"\nCruise Analysis (V={CRUISE_SPEED_MS} m/s, α=3°):")
    print(f"  CL:       {aero['CL']:.4f}")
    print(f"  CD_i:     {aero.get('CD', 0):.5f}")
    print(f"  CD_total: {cd_total:.5f} (with CD0={cd0})")
    print(f"  L/D:      {ld:.1f}")

    return aero


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main function."""

    print("=" * 60)
    print("MegaDrone Aircraft Model V2")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Total Weight:  {TOTAL_WEIGHT_KG:.2f} kg")
    print(f"  Cruise Speed:  {CRUISE_SPEED_MS:.1f} m/s (50 knots)")
    print(f"  Mission:       100 km round trip + 15 min loiter")

    # Create aircraft
    aircraft, airfoil = create_aircraft()

    # Visualize
    print("\n--- GENERATING VISUALIZATION ---")
    visualize_aircraft(aircraft)

    # Quick analysis
    aero = run_quick_analysis(aircraft)

    print("\n" + "=" * 60)
    print("Aircraft Model V2 Complete!")
    print("=" * 60)

    return aircraft, airfoil


if __name__ == "__main__":
    aircraft, airfoil = main()
