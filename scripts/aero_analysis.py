#!/usr/bin/env python3
"""
AeroSandbox VLM Aerodynamic Analysis
Analyzes the MegaDrone at various flight conditions

Uses Vortex Lattice Method (VLM) for:
- Lift and drag coefficients
- Stability derivatives
- Alpha and velocity sweeps

Author: MegaDrone Project
Date: January 8, 2026
"""

import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
from aerosandbox_model import create_aircraft, TOTAL_WEIGHT_KG, CRUISE_SPEED_MS, LOITER_SPEED_MS

# Constants
G = 9.81  # m/s²
RHO = 1.21  # kg/m³ at 150m altitude

# Reference values (from sizing)
WING_AREA_M2 = 0.241
WINGSPAN_M = 1.70
MEAN_CHORD_M = 0.1416


def run_single_point_analysis(aircraft, velocity, alpha, beta=0, print_results=True):
    """Run VLM analysis at a single operating point."""

    op_point = asb.OperatingPoint(
        atmosphere=asb.Atmosphere(altitude=150),
        velocity=velocity,
        alpha=alpha,
        beta=beta,
    )

    # Run VLM analysis
    vlm = asb.VortexLatticeMethod(
        airplane=aircraft,
        op_point=op_point,
        spanwise_resolution=12,
        chordwise_resolution=6,
    )

    aero = vlm.run()

    if print_results:
        print(f"\n--- VLM Analysis: V={velocity:.1f} m/s, α={alpha:.1f}° ---")
        print(f"  CL:     {aero['CL']:.4f}")
        # AeroSandbox uses 'CD' for induced drag in VLM (no viscous drag)
        cd_key = 'CD' if 'CD' in aero else 'CDi'
        print(f"  CDi:    {aero[cd_key]:.5f} (induced drag only)")
        cm_val = aero.get('Cm', aero.get('CM', 0))
        print(f"  Cm:     {cm_val:.4f} (pitching moment)")
        print(f"  L/Di:   {aero['CL']/aero[cd_key]:.1f} (inviscid)")

    return aero


def estimate_total_drag(aero, cd0=0.020):
    """Add parasite drag to VLM induced drag for total drag estimate."""

    # AeroSandbox uses 'CD' for induced drag in VLM
    cd_induced = aero.get('CD', aero.get('CDi', 0))
    cd_total = cd0 + cd_induced
    ld_total = aero['CL'] / cd_total if cd_total > 0 else 0

    return cd_total, ld_total


def run_alpha_sweep(aircraft, velocity, alpha_range):
    """Run VLM analysis over a range of angles of attack."""

    results = {
        'alpha': [],
        'CL': [],
        'CDi': [],
        'CD_total': [],
        'Cm': [],
        'L/D': [],
    }

    cd0 = 0.020  # Parasite drag coefficient

    for alpha in alpha_range:
        aero = run_single_point_analysis(aircraft, velocity, alpha, print_results=False)

        cd_total, ld_total = estimate_total_drag(aero, cd0)

        # Get induced drag (AeroSandbox uses 'CD' for VLM)
        cd_induced = aero.get('CD', aero.get('CDi', 0))
        cm_val = aero.get('Cm', aero.get('CM', 0))

        results['alpha'].append(alpha)
        results['CL'].append(aero['CL'])
        results['CDi'].append(cd_induced)
        results['CD_total'].append(cd_total)
        results['Cm'].append(cm_val)
        results['L/D'].append(ld_total)

    # Convert to numpy arrays
    for key in results:
        results[key] = np.array(results[key])

    return results


def run_velocity_sweep(aircraft, weight_kg, velocity_range):
    """Run analysis at constant weight over velocity range (trimmed flight)."""

    results = {
        'velocity': [],
        'alpha_trim': [],
        'CL_trim': [],
        'CD_total': [],
        'L/D': [],
        'power_required': [],
    }

    weight_n = weight_kg * G
    cd0 = 0.020

    for v in velocity_range:
        # Calculate required CL for level flight
        q = 0.5 * RHO * v**2
        cl_required = weight_n / (q * WING_AREA_M2)

        # Find alpha for this CL (approximate - linear CL-alpha)
        # CL ≈ CL_alpha * alpha, where CL_alpha ≈ 2*pi * AR / (AR + 2) for finite wing
        cl_alpha = 2 * np.pi * 12 / (12 + 2)  # ~5.4 /rad
        alpha_est = np.degrees(cl_required / cl_alpha)

        # Run VLM at estimated alpha
        aero = run_single_point_analysis(aircraft, v, alpha_est, print_results=False)

        # Calculate total drag and L/D
        cd_total, ld_total = estimate_total_drag(aero, cd0)

        # Power required
        drag = cd_total * q * WING_AREA_M2
        power = drag * v

        results['velocity'].append(v)
        results['alpha_trim'].append(alpha_est)
        results['CL_trim'].append(aero['CL'])
        results['CD_total'].append(cd_total)
        results['L/D'].append(ld_total)
        results['power_required'].append(power)

    # Convert to numpy arrays
    for key in results:
        results[key] = np.array(results[key])

    return results


def plot_alpha_sweep(results):
    """Plot alpha sweep results."""

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # CL vs alpha
    ax = axes[0, 0]
    ax.plot(results['alpha'], results['CL'], 'b-', linewidth=2)
    ax.set_xlabel('Angle of Attack (deg)', fontsize=11)
    ax.set_ylabel('Lift Coefficient CL', fontsize=11)
    ax.set_title('Lift Curve', fontsize=12)
    ax.grid(True, alpha=0.3)

    # Drag polar
    ax = axes[0, 1]
    ax.plot(results['CD_total'], results['CL'], 'b-', linewidth=2)
    ax.set_xlabel('Drag Coefficient CD', fontsize=11)
    ax.set_ylabel('Lift Coefficient CL', fontsize=11)
    ax.set_title('Drag Polar', fontsize=12)
    ax.grid(True, alpha=0.3)

    # L/D vs alpha
    ax = axes[1, 0]
    ax.plot(results['alpha'], results['L/D'], 'g-', linewidth=2)
    ax.set_xlabel('Angle of Attack (deg)', fontsize=11)
    ax.set_ylabel('Lift-to-Drag Ratio', fontsize=11)
    ax.set_title('Aerodynamic Efficiency', fontsize=12)
    ax.grid(True, alpha=0.3)

    # Find max L/D
    max_ld_idx = np.argmax(results['L/D'])
    ax.plot(results['alpha'][max_ld_idx], results['L/D'][max_ld_idx], 'ro',
            markersize=10, label=f"Max L/D = {results['L/D'][max_ld_idx]:.1f}")
    ax.legend()

    # Cm vs alpha (stability)
    ax = axes[1, 1]
    ax.plot(results['alpha'], results['Cm'], 'r-', linewidth=2)
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax.set_xlabel('Angle of Attack (deg)', fontsize=11)
    ax.set_ylabel('Pitching Moment Cm', fontsize=11)
    ax.set_title('Longitudinal Stability', fontsize=12)
    ax.grid(True, alpha=0.3)

    # Check static stability (dCm/dalpha should be negative)
    dcm_dalpha = np.gradient(results['Cm'], results['alpha'])
    if np.mean(dcm_dalpha) < 0:
        ax.text(0.95, 0.95, "Stable (dCm/dα < 0)", transform=ax.transAxes,
                ha='right', va='top', color='green', fontsize=10)
    else:
        ax.text(0.95, 0.95, "Unstable (dCm/dα > 0)", transform=ax.transAxes,
                ha='right', va='top', color='red', fontsize=10)

    plt.tight_layout()
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/alpha_sweep.png',
                dpi=150, bbox_inches='tight')
    print("Saved: designs/alpha_sweep.png")
    plt.show()

    return fig


def plot_velocity_sweep(results):
    """Plot velocity sweep results."""

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Velocity in knots for readability
    v_knots = results['velocity'] / 0.5144

    # L/D vs velocity
    ax = axes[0, 0]
    ax.plot(v_knots, results['L/D'], 'b-', linewidth=2)
    ax.axvline(x=CRUISE_SPEED_MS/0.5144, color='r', linestyle='--', label='Cruise (50 kt)')
    ax.axvline(x=LOITER_SPEED_MS/0.5144, color='g', linestyle='--', label='Loiter (29 kt)')
    ax.set_xlabel('Velocity (knots)', fontsize=11)
    ax.set_ylabel('Lift-to-Drag Ratio', fontsize=11)
    ax.set_title('L/D vs Speed', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Find best L/D velocity
    max_ld_idx = np.argmax(results['L/D'])
    ax.plot(v_knots[max_ld_idx], results['L/D'][max_ld_idx], 'ko',
            markersize=10, label=f"Best L/D at {v_knots[max_ld_idx]:.0f} kt")

    # Power required vs velocity
    ax = axes[0, 1]
    ax.plot(v_knots, results['power_required'], 'r-', linewidth=2)
    ax.axvline(x=CRUISE_SPEED_MS/0.5144, color='r', linestyle='--', alpha=0.5)
    ax.axvline(x=LOITER_SPEED_MS/0.5144, color='g', linestyle='--', alpha=0.5)
    ax.set_xlabel('Velocity (knots)', fontsize=11)
    ax.set_ylabel('Power Required (W)', fontsize=11)
    ax.set_title('Power Required vs Speed', fontsize=12)
    ax.grid(True, alpha=0.3)

    # Mark cruise and loiter power
    cruise_idx = np.argmin(np.abs(results['velocity'] - CRUISE_SPEED_MS))
    loiter_idx = np.argmin(np.abs(results['velocity'] - LOITER_SPEED_MS))
    ax.plot(CRUISE_SPEED_MS/0.5144, results['power_required'][cruise_idx], 'ro',
            markersize=8, label=f"Cruise: {results['power_required'][cruise_idx]:.0f} W")
    ax.plot(LOITER_SPEED_MS/0.5144, results['power_required'][loiter_idx], 'go',
            markersize=8, label=f"Loiter: {results['power_required'][loiter_idx]:.0f} W")
    ax.legend()

    # Trim alpha vs velocity
    ax = axes[1, 0]
    ax.plot(v_knots, results['alpha_trim'], 'g-', linewidth=2)
    ax.axvline(x=CRUISE_SPEED_MS/0.5144, color='r', linestyle='--', alpha=0.5)
    ax.axvline(x=LOITER_SPEED_MS/0.5144, color='g', linestyle='--', alpha=0.5)
    ax.set_xlabel('Velocity (knots)', fontsize=11)
    ax.set_ylabel('Trim Angle of Attack (deg)', fontsize=11)
    ax.set_title('Trim Alpha vs Speed', fontsize=12)
    ax.grid(True, alpha=0.3)

    # CL vs velocity
    ax = axes[1, 1]
    ax.plot(v_knots, results['CL_trim'], 'm-', linewidth=2)
    ax.axhline(y=1.4, color='r', linestyle=':', label='CL_max (stall)')
    ax.axvline(x=CRUISE_SPEED_MS/0.5144, color='r', linestyle='--', alpha=0.5)
    ax.axvline(x=LOITER_SPEED_MS/0.5144, color='g', linestyle='--', alpha=0.5)
    ax.set_xlabel('Velocity (knots)', fontsize=11)
    ax.set_ylabel('Trim CL', fontsize=11)
    ax.set_title('Required CL vs Speed', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/velocity_sweep.png',
                dpi=150, bbox_inches='tight')
    print("Saved: designs/velocity_sweep.png")
    plt.show()

    return fig


def main():
    """Main analysis routine."""

    print("=" * 60)
    print("AeroSandbox VLM Aerodynamic Analysis")
    print("=" * 60)

    # Create aircraft
    aircraft = create_aircraft()

    # Single point analysis at cruise
    print("\n" + "=" * 60)
    print("CRUISE CONDITION ANALYSIS")
    print("=" * 60)

    # Estimate cruise alpha (for required CL)
    weight_n = TOTAL_WEIGHT_KG * G
    q_cruise = 0.5 * RHO * CRUISE_SPEED_MS**2
    cl_cruise_req = weight_n / (q_cruise * WING_AREA_M2)
    print(f"\nRequired CL at cruise: {cl_cruise_req:.4f}")

    # Run at estimated trim alpha
    alpha_cruise = 4.0  # Initial estimate
    aero_cruise = run_single_point_analysis(aircraft, CRUISE_SPEED_MS, alpha_cruise)
    cd_total, ld_total = estimate_total_drag(aero_cruise)
    print(f"  CD_total: {cd_total:.5f} (with CD0=0.020)")
    print(f"  L/D:      {ld_total:.1f}")

    # Single point at loiter
    print("\n" + "=" * 60)
    print("LOITER CONDITION ANALYSIS")
    print("=" * 60)

    q_loiter = 0.5 * RHO * LOITER_SPEED_MS**2
    cl_loiter_req = weight_n / (q_loiter * WING_AREA_M2)
    print(f"\nRequired CL at loiter: {cl_loiter_req:.4f}")

    alpha_loiter = 10.0  # Higher alpha at lower speed
    aero_loiter = run_single_point_analysis(aircraft, LOITER_SPEED_MS, alpha_loiter)
    cd_total_loiter, ld_total_loiter = estimate_total_drag(aero_loiter)
    print(f"  CD_total: {cd_total_loiter:.5f} (with CD0=0.020)")
    print(f"  L/D:      {ld_total_loiter:.1f}")

    # Alpha sweep at cruise velocity
    print("\n" + "=" * 60)
    print("ALPHA SWEEP ANALYSIS")
    print("=" * 60)

    alpha_range = np.linspace(-4, 14, 25)
    alpha_results = run_alpha_sweep(aircraft, CRUISE_SPEED_MS, alpha_range)

    print(f"\nAlpha sweep at V = {CRUISE_SPEED_MS:.1f} m/s ({CRUISE_SPEED_MS/0.5144:.0f} knots):")
    print(f"  Max L/D:    {np.max(alpha_results['L/D']):.1f} at α = {alpha_results['alpha'][np.argmax(alpha_results['L/D'])]:.1f}°")
    print(f"  CL at max L/D: {alpha_results['CL'][np.argmax(alpha_results['L/D'])]:.3f}")

    # Plot alpha sweep
    plot_alpha_sweep(alpha_results)

    # Velocity sweep
    print("\n" + "=" * 60)
    print("VELOCITY SWEEP ANALYSIS")
    print("=" * 60)

    velocity_range = np.linspace(10, 35, 30)  # m/s
    velocity_results = run_velocity_sweep(aircraft, TOTAL_WEIGHT_KG, velocity_range)

    print(f"\nVelocity sweep (W = {TOTAL_WEIGHT_KG:.2f} kg):")
    max_ld_idx = np.argmax(velocity_results['L/D'])
    print(f"  Best L/D:    {velocity_results['L/D'][max_ld_idx]:.1f} at V = {velocity_results['velocity'][max_ld_idx]:.1f} m/s ({velocity_results['velocity'][max_ld_idx]/0.5144:.0f} kt)")

    min_power_idx = np.argmin(velocity_results['power_required'])
    print(f"  Min Power:   {velocity_results['power_required'][min_power_idx]:.0f} W at V = {velocity_results['velocity'][min_power_idx]:.1f} m/s ({velocity_results['velocity'][min_power_idx]/0.5144:.0f} kt)")

    cruise_idx = np.argmin(np.abs(velocity_results['velocity'] - CRUISE_SPEED_MS))
    print(f"  At Cruise:   {velocity_results['power_required'][cruise_idx]:.0f} W, L/D = {velocity_results['L/D'][cruise_idx]:.1f}")

    loiter_idx = np.argmin(np.abs(velocity_results['velocity'] - LOITER_SPEED_MS))
    print(f"  At Loiter:   {velocity_results['power_required'][loiter_idx]:.0f} W, L/D = {velocity_results['L/D'][loiter_idx]:.1f}")

    # Plot velocity sweep
    plot_velocity_sweep(velocity_results)

    # Summary
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"""
    AIRCRAFT: MegaDrone Phase 1
    ---------------------------
    Weight:     {TOTAL_WEIGHT_KG:.2f} kg
    Wing Area:  {WING_AREA_M2:.3f} m²
    Wingspan:   {WINGSPAN_M:.2f} m
    AR:         12.0

    CRUISE PERFORMANCE (50 knots):
    ------------------------------
    L/D:        {velocity_results['L/D'][cruise_idx]:.1f}
    Power:      {velocity_results['power_required'][cruise_idx]:.0f} W
    Trim α:     {velocity_results['alpha_trim'][cruise_idx]:.1f}°
    CL:         {velocity_results['CL_trim'][cruise_idx]:.3f}

    LOITER PERFORMANCE (29 knots):
    ------------------------------
    L/D:        {velocity_results['L/D'][loiter_idx]:.1f}
    Power:      {velocity_results['power_required'][loiter_idx]:.0f} W
    Trim α:     {velocity_results['alpha_trim'][loiter_idx]:.1f}°
    CL:         {velocity_results['CL_trim'][loiter_idx]:.3f}

    OPTIMAL CONDITIONS:
    -------------------
    Best L/D:   {velocity_results['L/D'][max_ld_idx]:.1f} at {velocity_results['velocity'][max_ld_idx]/0.5144:.0f} knots
    Min Power:  {velocity_results['power_required'][min_power_idx]:.0f} W at {velocity_results['velocity'][min_power_idx]/0.5144:.0f} knots
    """)

    return alpha_results, velocity_results


if __name__ == "__main__":
    alpha_results, velocity_results = main()
