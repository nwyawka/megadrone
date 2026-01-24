#!/usr/bin/env python3
"""
AeroSandbox Aircraft Model
Small Fixed-Wing Drone for 100km Round Trip Mission

Based on sizing results from drone_sizing.py:
- Total Weight: 1.96 kg
- Wingspan: 1.70 m
- Wing Area: 0.241 m²
- Aspect Ratio: 12
- Cruise Speed: 25.7 m/s (50 knots)

Author: MegaDrone Project
Date: January 8, 2026
"""

import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# DESIGN PARAMETERS (from sizing)
# =============================================================================

# Aircraft parameters
TOTAL_WEIGHT_KG = 1.96
WINGSPAN_M = 1.70
WING_AREA_M2 = 0.241
ASPECT_RATIO = 12.0
MEAN_CHORD_M = 0.1416
TAPER_RATIO = 0.7  # Typical for efficiency

# Derived parameters
ROOT_CHORD_M = 2 * MEAN_CHORD_M / (1 + TAPER_RATIO)  # ~0.167 m
TIP_CHORD_M = ROOT_CHORD_M * TAPER_RATIO  # ~0.117 m
SEMI_SPAN_M = WINGSPAN_M / 2  # 0.85 m

# Flight conditions
CRUISE_SPEED_MS = 25.7
LOITER_SPEED_MS = 15.0
ALTITUDE_M = 150
RHO = 1.21  # kg/m³ at 150m

# Fuselage dimensions (estimate for camera pod)
FUSELAGE_LENGTH_M = 0.45  # Compact for payload
FUSELAGE_WIDTH_M = 0.12
FUSELAGE_HEIGHT_M = 0.10

# Tail sizing (typical ratios)
HTAIL_VOLUME_COEFF = 0.5  # Typical for small UAVs
VTAIL_VOLUME_COEFF = 0.04
TAIL_ARM_M = 0.55  # Distance from wing quarter chord to tail quarter chord

# =============================================================================
# AIRFOIL DEFINITIONS
# =============================================================================

def get_main_wing_airfoil():
    """Get main wing airfoil - optimized for Re ~ 250,000."""
    # Start with a good low-Re airfoil
    # E387 is excellent for Re 200k-400k range
    # Can later optimize with NeuralFoil
    return asb.Airfoil("e387")


def get_tail_airfoil():
    """Get symmetric airfoil for tail surfaces."""
    return asb.Airfoil("naca0010")


# =============================================================================
# AIRCRAFT GEOMETRY
# =============================================================================

def create_main_wing():
    """Create main wing with taper and dihedral."""

    wing_airfoil = get_main_wing_airfoil()

    # High-wing configuration with slight dihedral
    wing = asb.Wing(
        name="Main Wing",
        symmetric=True,  # Mirror about XZ plane
        xsecs=[
            asb.WingXSec(
                xyz_le=[0, 0, 0],  # Root leading edge at origin
                chord=ROOT_CHORD_M,
                twist=2.0,  # 2 degrees incidence at root
                airfoil=wing_airfoil,
            ),
            asb.WingXSec(
                xyz_le=[
                    (ROOT_CHORD_M - TIP_CHORD_M) * 0.25,  # Quarter-chord sweep
                    SEMI_SPAN_M,
                    SEMI_SPAN_M * np.tan(np.radians(3)),  # 3 degrees dihedral
                ],
                chord=TIP_CHORD_M,
                twist=-1.0,  # 3 degrees total washout (2 - (-1))
                airfoil=wing_airfoil,
            ),
        ],
    )

    return wing


def create_horizontal_tail():
    """Create horizontal tail (stabilizer)."""

    tail_airfoil = get_tail_airfoil()

    # Size based on tail volume coefficient
    # V_H = (S_H * l_H) / (S_W * c_W)
    # S_H = V_H * S_W * c_W / l_H
    htail_area = HTAIL_VOLUME_COEFF * WING_AREA_M2 * MEAN_CHORD_M / TAIL_ARM_M
    htail_span = np.sqrt(htail_area * 4)  # AR ~ 4 for H-tail
    htail_chord = htail_area / htail_span

    htail = asb.Wing(
        name="Horizontal Tail",
        symmetric=True,
        xsecs=[
            asb.WingXSec(
                xyz_le=[TAIL_ARM_M + FUSELAGE_LENGTH_M * 0.3, 0, 0],
                chord=htail_chord * 1.1,  # Slight taper
                twist=0,
                airfoil=tail_airfoil,
            ),
            asb.WingXSec(
                xyz_le=[
                    TAIL_ARM_M + FUSELAGE_LENGTH_M * 0.3 + htail_chord * 0.05,
                    htail_span / 2,
                    0,
                ],
                chord=htail_chord * 0.9,
                twist=0,
                airfoil=tail_airfoil,
            ),
        ],
    )

    return htail, htail_area, htail_span


def create_vertical_tail():
    """Create vertical tail (fin)."""

    tail_airfoil = get_tail_airfoil()

    # Size based on tail volume coefficient
    # V_V = (S_V * l_V) / (S_W * b_W)
    # S_V = V_V * S_W * b_W / l_V
    vtail_area = VTAIL_VOLUME_COEFF * WING_AREA_M2 * WINGSPAN_M / TAIL_ARM_M
    vtail_height = np.sqrt(vtail_area * 1.5)  # AR ~ 1.5 for V-tail
    vtail_chord = vtail_area / vtail_height

    vtail = asb.Wing(
        name="Vertical Tail",
        symmetric=False,
        xsecs=[
            asb.WingXSec(
                xyz_le=[TAIL_ARM_M + FUSELAGE_LENGTH_M * 0.3, 0, 0],
                chord=vtail_chord * 1.2,  # Larger root
                twist=0,
                airfoil=tail_airfoil,
            ),
            asb.WingXSec(
                xyz_le=[
                    TAIL_ARM_M + FUSELAGE_LENGTH_M * 0.3 + vtail_chord * 0.3,
                    0,
                    vtail_height,
                ],
                chord=vtail_chord * 0.6,  # Taper
                twist=0,
                airfoil=tail_airfoil,
            ),
        ],
    )

    return vtail, vtail_area, vtail_height


def create_fuselage():
    """Create fuselage for camera pod."""

    # Simple fuselage for camera payload
    fuselage = asb.Fuselage(
        name="Fuselage",
        xsecs=[
            asb.FuselageXSec(
                xyz_c=[0, 0, -FUSELAGE_HEIGHT_M * 0.3],  # Below wing
                radius=0.01,  # Nose point
            ),
            asb.FuselageXSec(
                xyz_c=[FUSELAGE_LENGTH_M * 0.15, 0, -FUSELAGE_HEIGHT_M * 0.3],
                width=FUSELAGE_WIDTH_M * 0.8,
                height=FUSELAGE_HEIGHT_M * 0.8,
            ),
            asb.FuselageXSec(
                xyz_c=[FUSELAGE_LENGTH_M * 0.5, 0, -FUSELAGE_HEIGHT_M * 0.3],
                width=FUSELAGE_WIDTH_M,
                height=FUSELAGE_HEIGHT_M,
            ),
            asb.FuselageXSec(
                xyz_c=[FUSELAGE_LENGTH_M * 0.85, 0, -FUSELAGE_HEIGHT_M * 0.3],
                width=FUSELAGE_WIDTH_M * 0.6,
                height=FUSELAGE_HEIGHT_M * 0.6,
            ),
            asb.FuselageXSec(
                xyz_c=[FUSELAGE_LENGTH_M, 0, -FUSELAGE_HEIGHT_M * 0.3],
                radius=0.01,  # Tail point
            ),
        ],
    )

    return fuselage


def create_aircraft():
    """Create complete aircraft model."""

    print("=" * 60)
    print("Creating AeroSandbox Aircraft Model")
    print("=" * 60)

    # Create components
    wing = create_main_wing()
    htail, htail_area, htail_span = create_horizontal_tail()
    vtail, vtail_area, vtail_height = create_vertical_tail()
    fuselage = create_fuselage()

    # Assemble aircraft
    aircraft = asb.Airplane(
        name="MegaDrone Phase1",
        xyz_ref=[MEAN_CHORD_M * 0.25, 0, 0],  # Reference at wing quarter chord
        wings=[wing, htail, vtail],
        fuselages=[fuselage],
    )

    # Print summary
    print(f"\n--- MAIN WING ---")
    print(f"  Span:       {WINGSPAN_M:.3f} m")
    print(f"  Root Chord: {ROOT_CHORD_M:.4f} m")
    print(f"  Tip Chord:  {TIP_CHORD_M:.4f} m")
    print(f"  Area:       {WING_AREA_M2:.4f} m²")
    print(f"  AR:         {ASPECT_RATIO:.1f}")
    print(f"  Taper:      {TAPER_RATIO:.2f}")

    print(f"\n--- HORIZONTAL TAIL ---")
    print(f"  Span:       {htail_span:.3f} m")
    print(f"  Area:       {htail_area:.4f} m²")

    print(f"\n--- VERTICAL TAIL ---")
    print(f"  Height:     {vtail_height:.3f} m")
    print(f"  Area:       {vtail_area:.4f} m²")

    print(f"\n--- FUSELAGE ---")
    print(f"  Length:     {FUSELAGE_LENGTH_M:.3f} m")
    print(f"  Width:      {FUSELAGE_WIDTH_M:.3f} m")

    return aircraft


# =============================================================================
# VISUALIZATION
# =============================================================================

def visualize_aircraft(aircraft):
    """Create 3D visualization of aircraft."""

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(12, 8))

    aircraft.draw(
        backend="matplotlib",
        ax=ax,
        show=False,
    )

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("MegaDrone Phase 1 - AeroSandbox Model")

    # Set equal aspect ratio
    max_range = WINGSPAN_M / 2
    ax.set_xlim([-max_range * 0.5, max_range * 1.5])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range * 0.5, max_range * 0.5])

    # Save figure
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/aerosandbox_model.png',
                dpi=150, bbox_inches='tight')
    print("\nSaved: designs/aerosandbox_model.png")

    plt.show()

    return fig


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main function to create and display aircraft."""

    print("=" * 60)
    print("MegaDrone AeroSandbox Aircraft Model")
    print("=" * 60)
    print(f"\nDesign Requirements:")
    print(f"  Total Weight:  {TOTAL_WEIGHT_KG:.2f} kg")
    print(f"  Cruise Speed:  {CRUISE_SPEED_MS:.1f} m/s (50 knots)")
    print(f"  Loiter Speed:  {LOITER_SPEED_MS:.1f} m/s")
    print(f"  Mission:       100 km round trip + 15 min loiter")

    # Create aircraft
    aircraft = create_aircraft()

    # Visualize
    print("\n--- GENERATING 3D VISUALIZATION ---")
    fig = visualize_aircraft(aircraft)

    print("\n" + "=" * 60)
    print("Aircraft Model Created Successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Run VLM aerodynamic analysis (aero_analysis.py)")
    print("  2. Optimize airfoil with NeuralFoil (airfoil_optimization.py)")
    print("  3. Full MDO optimization (mdo_optimization.py)")

    return aircraft


if __name__ == "__main__":
    aircraft = main()
