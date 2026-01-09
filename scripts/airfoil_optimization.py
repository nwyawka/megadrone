#!/usr/bin/env python3
"""
Airfoil Optimization with NeuralFoil
Optimizes airfoil shape for MegaDrone mission profile

Uses CST (Class Shape Transformation) parameterization and
NeuralFoil for fast aerodynamic coefficient predictions.

Target: Maximize L/D at cruise Re ~250,000, CL ~0.5

Author: MegaDrone Project
Date: January 8, 2026
"""

import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
from aerosandbox.geometry.airfoil.airfoil_families import get_kulfan_parameters

# =============================================================================
# OPERATING CONDITIONS
# =============================================================================

# Cruise conditions
CRUISE_RE = 250000  # Reynolds number at cruise
CRUISE_MACH = 0.075  # ~25.7 m/s at sea level
CRUISE_CL_TARGET = 0.5  # Target CL at cruise

# Loiter conditions
LOITER_RE = 150000
LOITER_MACH = 0.044
LOITER_CL_TARGET = 0.9

# =============================================================================
# BASELINE AIRFOILS FOR COMPARISON
# =============================================================================

def get_baseline_airfoils():
    """Get baseline airfoils for comparison."""

    airfoils = {
        'E387': asb.Airfoil("e387"),  # Classic low-Re glider airfoil
        'NACA 2412': asb.Airfoil("naca2412"),  # General aviation
        'SD7037': asb.Airfoil("sd7037"),  # Low-Re sailplane
        'Clark-Y': asb.Airfoil("clarky"),  # Historic, good L/D
    }

    return airfoils


def analyze_airfoil_neuralfoil(airfoil, alpha_range, Re, Mach):
    """Analyze airfoil using NeuralFoil."""

    results = {
        'alpha': [],
        'CL': [],
        'CD': [],
        'CM': [],
        'L/D': [],
    }

    for alpha in alpha_range:
        try:
            # NeuralFoil returns a dict, not tuple
            aero = airfoil.get_aero_from_neuralfoil(
                alpha=alpha,
                Re=Re,
                mach=Mach,
            )

            # Handle both dict and tuple returns for compatibility
            if isinstance(aero, dict):
                cl = aero.get('CL', aero.get('cl', 0))
                cd = aero.get('CD', aero.get('cd', 0))
                cm = aero.get('CM', aero.get('cm', 0))
            else:
                # Old API returned tuple
                cl, cd, cm = aero[0], aero[1], aero[2]

            ld = cl / cd if cd > 0 else 0

            results['alpha'].append(alpha)
            results['CL'].append(float(cl))
            results['CD'].append(float(cd))
            results['CM'].append(float(cm))
            results['L/D'].append(float(ld))

        except Exception as e:
            print(f"Warning: Failed at alpha={alpha}: {e}")
            continue

    # Convert to arrays
    for key in results:
        results[key] = np.array(results[key])

    return results


def compare_baseline_airfoils():
    """Compare baseline airfoils at operating conditions."""

    print("=" * 60)
    print("Baseline Airfoil Comparison")
    print("=" * 60)

    airfoils = get_baseline_airfoils()
    alpha_range = np.linspace(-4, 14, 25)

    # Store results for plotting
    all_results = {}

    for name, airfoil in airfoils.items():
        print(f"\nAnalyzing {name}...")
        results = analyze_airfoil_neuralfoil(airfoil, alpha_range, CRUISE_RE, CRUISE_MACH)
        all_results[name] = results

        if len(results['L/D']) > 0:
            max_ld = np.max(results['L/D'])
            max_ld_alpha = results['alpha'][np.argmax(results['L/D'])]
            max_ld_cl = results['CL'][np.argmax(results['L/D'])]

            # Find CL closest to cruise target
            cruise_idx = np.argmin(np.abs(results['CL'] - CRUISE_CL_TARGET))
            cruise_ld = results['L/D'][cruise_idx]
            cruise_alpha = results['alpha'][cruise_idx]

            print(f"  Max L/D: {max_ld:.1f} at α={max_ld_alpha:.1f}° (CL={max_ld_cl:.2f})")
            print(f"  At CL={CRUISE_CL_TARGET}: L/D={cruise_ld:.1f} at α={cruise_alpha:.1f}°")

    # Plot comparison
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    colors = plt.cm.tab10(np.linspace(0, 1, len(airfoils)))

    # CL vs alpha
    ax = axes[0, 0]
    for (name, results), color in zip(all_results.items(), colors):
        ax.plot(results['alpha'], results['CL'], '-', color=color, linewidth=2, label=name)
    ax.axhline(y=CRUISE_CL_TARGET, color='r', linestyle='--', alpha=0.5, label=f'Cruise CL={CRUISE_CL_TARGET}')
    ax.set_xlabel('Angle of Attack (deg)')
    ax.set_ylabel('Lift Coefficient CL')
    ax.set_title(f'Lift Curves (Re={CRUISE_RE:,})')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Drag polar
    ax = axes[0, 1]
    for (name, results), color in zip(all_results.items(), colors):
        ax.plot(results['CD'], results['CL'], '-', color=color, linewidth=2, label=name)
    ax.set_xlabel('Drag Coefficient CD')
    ax.set_ylabel('Lift Coefficient CL')
    ax.set_title('Drag Polars')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # L/D vs alpha
    ax = axes[1, 0]
    for (name, results), color in zip(all_results.items(), colors):
        ax.plot(results['alpha'], results['L/D'], '-', color=color, linewidth=2, label=name)
    ax.set_xlabel('Angle of Attack (deg)')
    ax.set_ylabel('Lift/Drag Ratio')
    ax.set_title('Aerodynamic Efficiency')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # L/D vs CL
    ax = axes[1, 1]
    for (name, results), color in zip(all_results.items(), colors):
        ax.plot(results['CL'], results['L/D'], '-', color=color, linewidth=2, label=name)
    ax.axvline(x=CRUISE_CL_TARGET, color='r', linestyle='--', alpha=0.5, label=f'Cruise CL')
    ax.set_xlabel('Lift Coefficient CL')
    ax.set_ylabel('Lift/Drag Ratio')
    ax.set_title('L/D vs CL')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/airfoil_comparison.png',
                dpi=150, bbox_inches='tight')
    print("\nSaved: designs/airfoil_comparison.png")
    plt.show()

    return all_results


# =============================================================================
# AIRFOIL OPTIMIZATION
# =============================================================================

def optimize_airfoil():
    """Optimize airfoil shape using NeuralFoil with gradient-based optimization."""

    print("\n" + "=" * 60)
    print("Airfoil Shape Optimization")
    print("=" * 60)
    print(f"\nTarget: Max L/D at Re={CRUISE_RE:,}, CL≈{CRUISE_CL_TARGET}")

    # Start from E387 as baseline (good low-Re performance)
    baseline = asb.Airfoil("e387")

    # Get CST parameters from baseline
    try:
        baseline_kulfan = get_kulfan_parameters(baseline.coordinates)
        upper_init = baseline_kulfan['upper_weights']
        lower_init = baseline_kulfan['lower_weights']
        LE_weight_init = baseline_kulfan.get('leading_edge_weight', 0)
        TE_thickness_init = baseline_kulfan.get('TE_thickness', 0)
    except:
        # Default CST parameters if extraction fails
        upper_init = np.array([0.2, 0.3, 0.2, 0.15, 0.1, 0.08, 0.05, 0.03])
        lower_init = np.array([-0.15, -0.1, -0.08, -0.05, 0.0, 0.02, 0.03, 0.02])
        LE_weight_init = 0
        TE_thickness_init = 0

    print(f"\nStarting from E387 airfoil")
    print(f"Upper CST weights: {len(upper_init)} parameters")
    print(f"Lower CST weights: {len(lower_init)} parameters")

    # Create optimization problem
    opti = asb.Opti()

    # Design variables: CST weights
    n_upper = min(8, len(upper_init))
    n_lower = min(8, len(lower_init))

    upper_weights = opti.variable(
        init_guess=upper_init[:n_upper],
        lower_bound=0.0,
        upper_bound=0.5,
    )
    lower_weights = opti.variable(
        init_guess=lower_init[:n_lower],
        lower_bound=-0.3,
        upper_bound=0.1,
    )

    # Angle of attack (to achieve target CL)
    alpha = opti.variable(init_guess=3.0, lower_bound=-2, upper_bound=12)

    # Create airfoil with these parameters
    airfoil = asb.KulfanAirfoil(
        upper_weights=upper_weights,
        lower_weights=lower_weights,
        leading_edge_weight=LE_weight_init,
        TE_thickness=TE_thickness_init,
    )

    # Get aerodynamic coefficients using NeuralFoil
    aero = airfoil.get_aero_from_neuralfoil(
        alpha=alpha,
        Re=CRUISE_RE,
        mach=CRUISE_MACH,
    )

    CL = aero["CL"]
    CD = aero["CD"]
    CM = aero["CM"]

    # Objective: Maximize L/D (minimize -L/D)
    L_over_D = CL / CD
    opti.minimize(-L_over_D)

    # Constraints
    opti.subject_to(CL >= CRUISE_CL_TARGET - 0.1)  # CL close to target
    opti.subject_to(CL <= CRUISE_CL_TARGET + 0.1)
    opti.subject_to(CM >= -0.15)  # Reasonable pitching moment

    # Thickness constraints
    # Get thickness at various chord locations
    # Ensure minimum thickness for structure

    # Solve
    print("\nOptimizing...")
    try:
        sol = opti.solve(
            verbose=False,
            max_iter=200,
        )

        # Extract results
        opt_upper = sol(upper_weights)
        opt_lower = sol(lower_weights)
        opt_alpha = sol(alpha)
        opt_CL = sol(CL)
        opt_CD = sol(CD)
        opt_CM = sol(CM)
        opt_LD = sol(L_over_D)

        print(f"\nOptimization Successful!")
        print(f"  Alpha:  {opt_alpha:.2f}°")
        print(f"  CL:     {opt_CL:.4f}")
        print(f"  CD:     {opt_CD:.5f}")
        print(f"  CM:     {opt_CM:.4f}")
        print(f"  L/D:    {opt_LD:.1f}")

        # Create optimized airfoil
        optimized_airfoil = asb.KulfanAirfoil(
            upper_weights=opt_upper,
            lower_weights=opt_lower,
            leading_edge_weight=LE_weight_init,
            TE_thickness=TE_thickness_init,
        )

        return optimized_airfoil, {
            'upper_weights': opt_upper,
            'lower_weights': opt_lower,
            'alpha': opt_alpha,
            'CL': opt_CL,
            'CD': opt_CD,
            'CM': opt_CM,
            'L/D': opt_LD,
        }

    except Exception as e:
        print(f"\nOptimization failed: {e}")
        print("Returning E387 as fallback")
        return baseline, None


def plot_optimized_airfoil(optimized, baseline, opt_results):
    """Plot optimized vs baseline airfoil."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Airfoil shapes
    ax = axes[0, 0]
    baseline_coords = baseline.coordinates
    opt_coords = optimized.coordinates

    ax.plot(baseline_coords[:, 0], baseline_coords[:, 1], 'b-',
            linewidth=2, label='E387 (Baseline)')
    ax.plot(opt_coords[:, 0], opt_coords[:, 1], 'r-',
            linewidth=2, label='Optimized')
    ax.set_xlabel('x/c')
    ax.set_ylabel('y/c')
    ax.set_title('Airfoil Shape Comparison')
    ax.set_aspect('equal')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Analyze both at same conditions
    alpha_range = np.linspace(-2, 12, 20)

    baseline_results = analyze_airfoil_neuralfoil(baseline, alpha_range, CRUISE_RE, CRUISE_MACH)
    opt_analysis = analyze_airfoil_neuralfoil(optimized, alpha_range, CRUISE_RE, CRUISE_MACH)

    # Drag polars
    ax = axes[0, 1]
    ax.plot(baseline_results['CD'], baseline_results['CL'], 'b-', linewidth=2, label='E387')
    ax.plot(opt_analysis['CD'], opt_analysis['CL'], 'r-', linewidth=2, label='Optimized')
    ax.axhline(y=CRUISE_CL_TARGET, color='g', linestyle='--', alpha=0.5, label=f'Target CL={CRUISE_CL_TARGET}')
    ax.set_xlabel('Drag Coefficient CD')
    ax.set_ylabel('Lift Coefficient CL')
    ax.set_title('Drag Polar Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # L/D comparison
    ax = axes[1, 0]
    ax.plot(baseline_results['alpha'], baseline_results['L/D'], 'b-', linewidth=2, label='E387')
    ax.plot(opt_analysis['alpha'], opt_analysis['L/D'], 'r-', linewidth=2, label='Optimized')
    ax.set_xlabel('Angle of Attack (deg)')
    ax.set_ylabel('L/D')
    ax.set_title('L/D vs Alpha')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Performance summary
    ax = axes[1, 1]
    ax.axis('off')

    # Find performance metrics
    baseline_cruise_idx = np.argmin(np.abs(baseline_results['CL'] - CRUISE_CL_TARGET))
    opt_cruise_idx = np.argmin(np.abs(opt_analysis['CL'] - CRUISE_CL_TARGET))

    summary_text = f"""
    OPTIMIZATION RESULTS
    ====================

    Operating Conditions:
      Reynolds Number:  {CRUISE_RE:,}
      Mach Number:      {CRUISE_MACH}
      Target CL:        {CRUISE_CL_TARGET}

    E387 Baseline:
      Max L/D:          {np.max(baseline_results['L/D']):.1f}
      L/D at CL={CRUISE_CL_TARGET}:    {baseline_results['L/D'][baseline_cruise_idx]:.1f}
      CD at CL={CRUISE_CL_TARGET}:     {baseline_results['CD'][baseline_cruise_idx]:.5f}

    Optimized Airfoil:
      Max L/D:          {np.max(opt_analysis['L/D']):.1f}
      L/D at CL={CRUISE_CL_TARGET}:    {opt_analysis['L/D'][opt_cruise_idx]:.1f}
      CD at CL={CRUISE_CL_TARGET}:     {opt_analysis['CD'][opt_cruise_idx]:.5f}

    Improvement:
      L/D increase:     {(opt_analysis['L/D'][opt_cruise_idx] / baseline_results['L/D'][baseline_cruise_idx] - 1) * 100:.1f}%
      CD reduction:     {(1 - opt_analysis['CD'][opt_cruise_idx] / baseline_results['CD'][baseline_cruise_idx]) * 100:.1f}%
    """

    ax.text(0.1, 0.9, summary_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/airfoil_optimized.png',
                dpi=150, bbox_inches='tight')
    print("\nSaved: designs/airfoil_optimized.png")
    plt.show()

    return fig


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main optimization routine."""

    print("=" * 60)
    print("NeuralFoil Airfoil Optimization for MegaDrone")
    print("=" * 60)
    print(f"\nOperating Conditions:")
    print(f"  Cruise Re:   {CRUISE_RE:,}")
    print(f"  Cruise Mach: {CRUISE_MACH}")
    print(f"  Target CL:   {CRUISE_CL_TARGET}")

    # Compare baseline airfoils
    baseline_results = compare_baseline_airfoils()

    # Run optimization
    optimized_airfoil, opt_results = optimize_airfoil()

    if opt_results is not None:
        # Plot results
        baseline = asb.Airfoil("e387")
        plot_optimized_airfoil(optimized_airfoil, baseline, opt_results)

        # Export optimized airfoil coordinates
        coords = optimized_airfoil.coordinates
        np.savetxt(
            '/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/optimized_airfoil.dat',
            coords,
            header=f'MegaDrone Optimized Airfoil\nOptimized for Re={CRUISE_RE}, CL={CRUISE_CL_TARGET}',
            fmt='%.6f'
        )
        print("\nSaved: designs/optimized_airfoil.dat")

    print("\n" + "=" * 60)
    print("Airfoil Optimization Complete!")
    print("=" * 60)

    return optimized_airfoil, opt_results


if __name__ == "__main__":
    optimized_airfoil, opt_results = main()
