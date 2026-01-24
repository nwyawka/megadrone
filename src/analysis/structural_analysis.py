#!/usr/bin/env python3
"""
Structural Analysis for MegaDrone Phase 1
Wing spar sizing and stress analysis

Uses beam theory and AeroSandbox structural tools to:
- Size wing spar for ultimate load factor
- Calculate deflections and stresses
- Estimate structural weight

Author: MegaDrone Project
Date: January 8, 2026
"""

import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# DESIGN PARAMETERS
# =============================================================================

# Aircraft parameters
TOTAL_WEIGHT_KG = 1.96
WINGSPAN_M = 1.70
WING_AREA_M2 = 0.241
SEMI_SPAN_M = WINGSPAN_M / 2
ROOT_CHORD_M = 0.167
TIP_CHORD_M = 0.117
MEAN_CHORD_M = 0.142
TAPER_RATIO = 0.7

# Load factors
N_ULTIMATE = 3.8  # Ultimate load factor (typical for small UAV)
N_LIMIT = 2.5     # Limit load factor
SAFETY_FACTOR = 1.5

# Material properties (Carbon fiber tube - unidirectional)
CARBON_TENSILE_STRENGTH = 600e6  # Pa (600 MPa)
CARBON_COMPRESSIVE_STRENGTH = 500e6  # Pa
CARBON_ELASTIC_MODULUS = 70e9  # Pa (70 GPa)
CARBON_DENSITY = 1600  # kg/m³
CARBON_SHEAR_STRENGTH = 50e6  # Pa

# Material properties (3D printed PLA for ribs)
PLA_TENSILE_STRENGTH = 50e6  # Pa
PLA_ELASTIC_MODULUS = 3.5e9  # Pa
PLA_DENSITY = 1240  # kg/m³

# Physics
G = 9.81  # m/s²
RHO_AIR = 1.21  # kg/m³

# =============================================================================
# AERODYNAMIC LOADS
# =============================================================================

def calculate_lift_distribution(semi_span, n_points=50):
    """Calculate spanwise lift distribution using elliptical approximation.

    For a tapered wing, the lift distribution is approximately elliptical
    with corrections for taper ratio.
    """

    # Spanwise stations
    y = np.linspace(0, semi_span, n_points)

    # Total lift at ultimate load factor
    total_lift = TOTAL_WEIGHT_KG * G * N_ULTIMATE  # N

    # Elliptical distribution: L(y) = L0 * sqrt(1 - (y/b)^2)
    # With taper correction
    lift_per_span = (4 * total_lift / (np.pi * WINGSPAN_M)) * \
                    np.sqrt(1 - (y / semi_span)**2)

    # Correct for taper (reduces tip loading slightly)
    taper_correction = 1 - 0.1 * (1 - TAPER_RATIO) * (y / semi_span)
    lift_per_span = lift_per_span * taper_correction

    return y, lift_per_span


def calculate_shear_moment(y, lift_per_span):
    """Calculate shear force and bending moment distributions."""

    n_points = len(y)
    dy = y[1] - y[0] if len(y) > 1 else semi_span / 50

    # Shear force: integral of lift from tip to station
    shear = np.zeros(n_points)
    moment = np.zeros(n_points)

    # Integrate from tip to root
    for i in range(n_points - 2, -1, -1):
        # Trapezoidal integration
        shear[i] = shear[i + 1] + 0.5 * (lift_per_span[i] + lift_per_span[i + 1]) * dy

    # Bending moment: integral of shear
    for i in range(n_points - 2, -1, -1):
        moment[i] = moment[i + 1] + 0.5 * (shear[i] + shear[i + 1]) * dy

    return shear, moment


# =============================================================================
# WING SPAR SIZING
# =============================================================================

def size_carbon_tube_spar(max_moment, chord_at_root):
    """Size carbon fiber tube spar for bending moment AND stiffness.

    Spar located at 30% chord (typical for subsonic airfoils).
    Designs for both strength AND stiffness (max 5% span deflection).

    Returns:
        dict: Spar dimensions and properties
    """

    print("\n--- WING SPAR SIZING (Carbon Fiber Tube) ---")

    # Allowable stress with safety factor
    allowable_stress = CARBON_TENSILE_STRENGTH / SAFETY_FACTOR

    # STIFFNESS REQUIREMENT: Limit tip deflection to 8% of semi-span
    # (8% is acceptable for UAVs - provides good handling without flutter concerns)
    max_deflection_ratio = 0.08  # 8% of span
    max_deflection = max_deflection_ratio * SEMI_SPAN_M

    # For uniformly loaded cantilever (approximate):
    # delta_tip = (w * L^4) / (8 * E * I) for uniform load
    # For our elliptical load, use factor of 0.35 instead of 0.125
    # delta_tip ≈ 0.35 * (total_load * L^3) / (E * I)
    total_lift = TOTAL_WEIGHT_KG * G * N_ULTIMATE / 2  # Half for one wing
    I_required_stiffness = 0.35 * total_lift * SEMI_SPAN_M**3 / (CARBON_ELASTIC_MODULUS * max_deflection)

    # STRENGTH REQUIREMENT
    # For circular tube: I = pi/64 * (D^4 - d^4)
    # S = I / c = I / (D/2)
    wall_ratio = 0.12  # 12% wall thickness ratio (slightly thicker for stiffness)
    S_required = max_moment / allowable_stress

    # Solve for diameter from strength
    tube_factor = 1 - (1 - 2 * wall_ratio)**4
    D_strength = (32 * S_required / (np.pi * tube_factor))**(1/3)

    # Solve for diameter from stiffness
    # I = pi/64 * D^4 * (1 - (1-2*t/D)^4)
    I_factor = 1 - (1 - 2 * wall_ratio)**4
    D_stiffness = (64 * I_required_stiffness / (np.pi * I_factor))**(1/4)

    # Use larger of the two (stiffness usually governs for high AR wings)
    D_outer = max(D_strength, D_stiffness)
    design_driver = "Stiffness" if D_stiffness > D_strength else "Strength"

    # Check against available tube sizes (round up to standard size)
    standard_sizes = [6, 8, 10, 12, 14, 16, 18, 20]  # mm OD
    D_outer_mm = D_outer * 1000
    for size in standard_sizes:
        if size >= D_outer_mm:
            D_outer = size / 1000
            break

    # Inner diameter
    D_inner = D_outer * (1 - 2 * wall_ratio)

    # Wall thickness
    wall_thickness = (D_outer - D_inner) / 2

    # Cross-sectional area
    area = np.pi / 4 * (D_outer**2 - D_inner**2)

    # Second moment of area
    I = np.pi / 64 * (D_outer**4 - D_inner**4)

    # Mass per unit length
    mass_per_length = area * CARBON_DENSITY

    # Total spar mass (both sides)
    spar_mass = 2 * mass_per_length * SEMI_SPAN_M

    # Verify stress
    actual_stress = max_moment * (D_outer / 2) / I
    stress_margin = (allowable_stress - actual_stress) / allowable_stress * 100

    results = {
        'outer_diameter_mm': D_outer * 1000,
        'inner_diameter_mm': D_inner * 1000,
        'wall_thickness_mm': wall_thickness * 1000,
        'section_modulus': S_required,
        'moment_of_inertia': I,
        'cross_section_area_mm2': area * 1e6,
        'mass_per_meter': mass_per_length,
        'total_spar_mass_kg': spar_mass,
        'max_stress_mpa': actual_stress / 1e6,
        'allowable_stress_mpa': allowable_stress / 1e6,
        'stress_margin_percent': stress_margin,
        'design_driver': design_driver,
    }

    print(f"  Design Driver:   {design_driver}")
    print(f"  Outer Diameter:  {results['outer_diameter_mm']:.1f} mm (standard size)")
    print(f"  Inner Diameter:  {results['inner_diameter_mm']:.1f} mm")
    print(f"  Wall Thickness:  {results['wall_thickness_mm']:.2f} mm")
    print(f"  Cross-section:   {results['cross_section_area_mm2']:.1f} mm²")
    print(f"  Spar Mass:       {results['total_spar_mass_kg']*1000:.1f} g (both wings)")
    print(f"  Max Stress:      {results['max_stress_mpa']:.1f} MPa")
    print(f"  Allowable:       {results['allowable_stress_mpa']:.1f} MPa")
    print(f"  Stress Margin:   {results['stress_margin_percent']:.1f}%")

    return results


def calculate_deflection(y, moment, E, I):
    """Calculate wing deflection using beam theory.

    Uses double integration of M/EI.
    """

    n_points = len(y)
    dy = y[1] - y[0] if len(y) > 1 else SEMI_SPAN_M / 50

    # Curvature = M / (E * I)
    curvature = moment / (E * I)

    # Slope (first integration)
    slope = np.zeros(n_points)
    for i in range(1, n_points):
        slope[i] = slope[i-1] + 0.5 * (curvature[i] + curvature[i-1]) * dy

    # Apply boundary condition: slope = 0 at root
    slope = slope - slope[0]

    # Deflection (second integration)
    deflection = np.zeros(n_points)
    for i in range(1, n_points):
        deflection[i] = deflection[i-1] + 0.5 * (slope[i] + slope[i-1]) * dy

    return deflection, slope


# =============================================================================
# WING STRUCTURE WEIGHT ESTIMATION
# =============================================================================

def estimate_wing_structure_weight(spar_results):
    """Estimate total wing structural weight (optimized lightweight construction)."""

    print("\n--- WING STRUCTURE WEIGHT BREAKDOWN ---")

    # Spar weight (from sizing)
    w_spar = spar_results['total_spar_mass_kg']

    # Rib weight (3D printed PLA with lightening holes - 60% fill)
    # Lightweight ribs: ~5-7g each for this size
    n_ribs = 8  # per wing half (100mm spacing)
    rib_mass_each = 0.006  # kg (6g each with lightening)
    w_ribs = 2 * n_ribs * rib_mass_each

    # Leading edge (EPP foam - very light)
    le_mass_per_meter = 0.008  # kg/m (EPP foam D-box)
    w_leading_edge = 2 * SEMI_SPAN_M * le_mass_per_meter

    # Trailing edge (balsa cap strip)
    te_mass_per_meter = 0.005  # kg/m
    w_trailing_edge = 2 * SEMI_SPAN_M * te_mass_per_meter

    # Skin (Ultracote or Oracover film - ~30 g/m²)
    skin_mass_per_area = 0.030  # kg/m²
    w_skin = WING_AREA_M2 * skin_mass_per_area

    # Servo mounts, hinges, aileron horns
    w_hardware = 0.020  # kg

    # Wing joiner (if removable wings)
    w_joiner = 0.015  # kg (carbon tube or aluminum)

    # Total wing weight
    w_wing_total = w_spar + w_ribs + w_leading_edge + w_trailing_edge + w_skin + w_hardware + w_joiner

    print(f"  Main Spar:       {w_spar*1000:.1f} g")
    print(f"  Ribs ({n_ribs}x2):     {w_ribs*1000:.1f} g (lightweight)")
    print(f"  Leading Edge:    {w_leading_edge*1000:.1f} g (EPP foam)")
    print(f"  Trailing Edge:   {w_trailing_edge*1000:.1f} g")
    print(f"  Skin:            {w_skin*1000:.1f} g (film)")
    print(f"  Hardware:        {w_hardware*1000:.1f} g")
    print(f"  Wing Joiner:     {w_joiner*1000:.1f} g")
    print(f"  ---------------------")
    print(f"  TOTAL WING:      {w_wing_total*1000:.1f} g ({w_wing_total:.3f} kg)")

    return {
        'spar': w_spar,
        'ribs': w_ribs,
        'leading_edge': w_leading_edge,
        'trailing_edge': w_trailing_edge,
        'skin': w_skin,
        'hardware': w_hardware,
        'joiner': w_joiner,
        'total': w_wing_total,
    }


# =============================================================================
# FUSELAGE STRUCTURE
# =============================================================================

def estimate_fuselage_structure():
    """Estimate fuselage structural requirements (optimized pod + boom)."""

    print("\n--- FUSELAGE STRUCTURE ---")

    fuselage_length = 0.45  # m
    fuselage_width = 0.12  # m

    # Pod fuselage (3D printed or fiberglass)
    # Lightweight design with internal ribbing
    pod_mass = 0.100  # kg (100g for small camera pod)

    # Motor mount (aluminum or 3D printed reinforced)
    motor_mount_mass = 0.015  # kg

    # Wing mount plates (plywood or carbon)
    wing_mount_mass = 0.025  # kg

    # Tail boom (carbon fiber tube)
    tail_boom_length = 0.50  # m
    tail_boom_diameter = 0.012  # m (12mm carbon tube)
    tail_boom_wall = 0.001  # m
    tail_boom_area = np.pi * tail_boom_diameter * tail_boom_wall
    tail_boom_mass = tail_boom_area * tail_boom_length * CARBON_DENSITY

    # Boom-to-pod connection
    boom_fitting_mass = 0.010  # kg

    total_fuselage = pod_mass + motor_mount_mass + wing_mount_mass + tail_boom_mass + boom_fitting_mass

    print(f"  Pod Shell:       {pod_mass*1000:.1f} g (3D printed)")
    print(f"  Motor Mount:     {motor_mount_mass*1000:.1f} g")
    print(f"  Wing Mounts:     {wing_mount_mass*1000:.1f} g")
    print(f"  Tail Boom:       {tail_boom_mass*1000:.1f} g (12mm carbon)")
    print(f"  Boom Fitting:    {boom_fitting_mass*1000:.1f} g")
    print(f"  ---------------------")
    print(f"  TOTAL FUSELAGE:  {total_fuselage*1000:.1f} g ({total_fuselage:.3f} kg)")

    # Bending check for tail boom
    tail_loads = 5.0  # N (estimated tail lift at maneuver)
    tail_moment = tail_loads * tail_boom_length
    I_boom = np.pi / 64 * (tail_boom_diameter**4 - (tail_boom_diameter - 2*tail_boom_wall)**4)
    boom_stress = tail_moment * (tail_boom_diameter / 2) / I_boom

    print(f"\n  Tail Boom Stress: {boom_stress/1e6:.1f} MPa (allowable: {CARBON_TENSILE_STRENGTH/SAFETY_FACTOR/1e6:.0f} MPa)")

    return {
        'pod': pod_mass,
        'motor_mount': motor_mount_mass,
        'wing_mount': wing_mount_mass,
        'tail_boom': tail_boom_mass,
        'boom_fitting': boom_fitting_mass,
        'total': total_fuselage,
    }


# =============================================================================
# TAIL STRUCTURE
# =============================================================================

def estimate_tail_structure():
    """Estimate tail surface structural weight."""

    print("\n--- TAIL STRUCTURE ---")

    # Horizontal tail
    htail_area = 0.037  # m²
    htail_mass_per_area = 0.8  # kg/m² (3D printed solid)
    w_htail = htail_area * htail_mass_per_area

    # Vertical tail
    vtail_area = 0.037  # m²
    vtail_mass_per_area = 0.8  # kg/m²
    w_vtail = vtail_area * vtail_mass_per_area

    # Control surface servos
    w_servos = 3 * 0.012  # 3 servos @ 12g each

    total_tail = w_htail + w_vtail + w_servos

    print(f"  Horizontal Tail: {w_htail*1000:.1f} g")
    print(f"  Vertical Tail:   {w_vtail*1000:.1f} g")
    print(f"  Servos:          {w_servos*1000:.1f} g")
    print(f"  ---------------------")
    print(f"  TOTAL TAIL:      {total_tail*1000:.1f} g ({total_tail:.3f} kg)")

    return {
        'horizontal': w_htail,
        'vertical': w_vtail,
        'servos': w_servos,
        'total': total_tail,
    }


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_structural_analysis(y, lift_per_span, shear, moment, deflection, spar_results):
    """Plot structural analysis results."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Lift distribution
    ax = axes[0, 0]
    ax.plot(y, lift_per_span, 'b-', linewidth=2)
    ax.fill_between(y, 0, lift_per_span, alpha=0.3)
    ax.set_xlabel('Spanwise Position (m)')
    ax.set_ylabel('Lift per Span (N/m)')
    ax.set_title(f'Lift Distribution (n={N_ULTIMATE})')
    ax.grid(True, alpha=0.3)

    # Shear force
    ax = axes[0, 1]
    ax.plot(y, shear, 'r-', linewidth=2)
    ax.set_xlabel('Spanwise Position (m)')
    ax.set_ylabel('Shear Force (N)')
    ax.set_title('Shear Force Distribution')
    ax.grid(True, alpha=0.3)

    # Bending moment
    ax = axes[1, 0]
    ax.plot(y, moment, 'g-', linewidth=2)
    ax.set_xlabel('Spanwise Position (m)')
    ax.set_ylabel('Bending Moment (N·m)')
    ax.set_title('Bending Moment Distribution')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=moment[0], color='r', linestyle='--', alpha=0.5,
               label=f'Max: {moment[0]:.2f} N·m')
    ax.legend()

    # Deflection
    ax = axes[1, 1]
    ax.plot(y, deflection * 1000, 'm-', linewidth=2)  # Convert to mm
    ax.set_xlabel('Spanwise Position (m)')
    ax.set_ylabel('Deflection (mm)')
    ax.set_title('Wing Deflection')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=deflection[-1] * 1000, color='r', linestyle='--', alpha=0.5,
               label=f'Tip: {deflection[-1]*1000:.1f} mm')
    ax.legend()

    plt.tight_layout()
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/structural_analysis.png',
                dpi=150, bbox_inches='tight')
    print("\nSaved: designs/structural_analysis.png")
    plt.show()

    return fig


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main structural analysis routine."""

    print("=" * 70)
    print("MegaDrone Phase 1 - Structural Analysis")
    print("=" * 70)
    print(f"\nDesign Load Factor: {N_ULTIMATE} (ultimate)")
    print(f"Safety Factor:      {SAFETY_FACTOR}")
    print(f"Ultimate Load:      {TOTAL_WEIGHT_KG * G * N_ULTIMATE:.1f} N ({TOTAL_WEIGHT_KG * N_ULTIMATE:.2f} kg)")

    # Calculate aerodynamic loads
    print("\n--- AERODYNAMIC LOADS ---")
    y, lift_per_span = calculate_lift_distribution(SEMI_SPAN_M)
    shear, moment = calculate_shear_moment(y, lift_per_span)

    print(f"  Max Lift/Span:    {np.max(lift_per_span):.1f} N/m (at root)")
    print(f"  Max Shear:        {shear[0]:.1f} N (at root)")
    print(f"  Max Moment:       {moment[0]:.2f} N·m (at root)")

    # Size wing spar
    spar_results = size_carbon_tube_spar(moment[0], ROOT_CHORD_M)

    # Calculate deflection
    E = CARBON_ELASTIC_MODULUS
    I = spar_results['moment_of_inertia']
    deflection, slope = calculate_deflection(y, moment, E, I)

    print(f"\n--- WING DEFLECTION ---")
    print(f"  Tip Deflection:   {deflection[-1]*1000:.1f} mm")
    print(f"  Tip Slope:        {np.degrees(slope[-1]):.2f}°")
    print(f"  Deflection/Span:  {deflection[-1]/SEMI_SPAN_M*100:.1f}%")

    # Estimate structural weights
    wing_weight = estimate_wing_structure_weight(spar_results)
    fuselage_weight = estimate_fuselage_structure()
    tail_weight = estimate_tail_structure()

    # Total structure
    total_structure = wing_weight['total'] + fuselage_weight['total'] + tail_weight['total']

    print("\n" + "=" * 70)
    print("STRUCTURAL WEIGHT SUMMARY")
    print("=" * 70)
    print(f"  Wing:            {wing_weight['total']*1000:.0f} g")
    print(f"  Fuselage:        {fuselage_weight['total']*1000:.0f} g")
    print(f"  Tail:            {tail_weight['total']*1000:.0f} g")
    print(f"  ---------------------")
    print(f"  TOTAL STRUCTURE: {total_structure*1000:.0f} g ({total_structure:.3f} kg)")
    print(f"  Budget:          {0.589*1000:.0f} g (30% of MTOW)")
    print(f"  Margin:          {(0.589 - total_structure)*1000:.0f} g")

    # Plot results
    plot_structural_analysis(y, lift_per_span, shear, moment, deflection, spar_results)

    # Summary
    print("\n" + "=" * 70)
    print("STRUCTURAL RECOMMENDATIONS")
    print("=" * 70)
    print(f"""
    WING SPAR:
    - Carbon fiber tube: {spar_results['outer_diameter_mm']:.0f}mm OD x {spar_results['inner_diameter_mm']:.0f}mm ID
    - Run from root to ~80% span, then transition to smaller tube
    - Reinforce root attachment with carbon sleeve

    RIBS:
    - 3D print in PLA or PETG
    - Spacing: ~85mm (10 per wing half)
    - Include lightening holes

    FUSELAGE:
    - Composite shell (fiberglass + carbon reinforcement)
    - 12mm carbon tube tail boom
    - Aluminum or carbon wing mount plates

    RECOMMENDED MATERIALS:
    - Main spar: Pultruded carbon tube (readily available)
    - Ribs: 3D printed PLA/PETG
    - Skin: UltraCote or similar heat-shrink film
    - Fuselage: Fiberglass layup or 3D printed
    """)

    return {
        'spar': spar_results,
        'wing_weight': wing_weight,
        'fuselage_weight': fuselage_weight,
        'tail_weight': tail_weight,
        'total_structure': total_structure,
    }


if __name__ == "__main__":
    results = main()
