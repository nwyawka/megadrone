#!/usr/bin/env python3
"""
Multi-Version Airfoil Optimization for MegaDrone
================================================

Optimizes airfoil shapes for each drone version (V0-V4) using NeuralFoil.

For each version:
1. Calculate operating Reynolds number
2. Compare foam-buildable airfoils (KFm, flat-bottom, etc.)
3. Optimize custom airfoil using CST parameterization
4. Export coordinates for 3D printing

Author: MegaDrone Project
Date: January 2026
"""

import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json

# =============================================================================
# VERSION SPECIFICATIONS
# =============================================================================

VERSIONS = {
    'V0': {
        'name': 'Skills Platform',
        'chord': 0.180,         # m
        'cruise_speed': 15,     # m/s
        'wing_loading': 50,     # g/dm² = kg/m² * 100
        'construction': 'foam', # foam, composite, or both
        'min_thickness': 0.08,  # 8% chord minimum for foam
    },
    'V1': {
        'name': 'Durable Platform',
        'chord': 0.180,
        'cruise_speed': 15,
        'wing_loading': 60,
        'construction': 'foam',
        'min_thickness': 0.08,
    },
    'V1-VID': {
        'name': 'Video Platform',
        'chord': 0.180,
        'cruise_speed': 15,
        'wing_loading': 64,
        'construction': 'foam',
        'min_thickness': 0.08,
    },
    'V2': {
        'name': 'ALTI Fixed-Wing',
        'chord': 0.300,
        'cruise_speed': 20,
        'wing_loading': 130,
        'construction': 'composite',
        'min_thickness': 0.12,  # 12% for composite spar
    },
    'V3': {
        'name': 'ALTI VTOL',
        'chord': 0.300,
        'cruise_speed': 20,
        'wing_loading': 150,
        'construction': 'composite',
        'min_thickness': 0.12,
    },
    'V4': {
        'name': 'Hybrid VTOL',
        'chord': 0.300,
        'cruise_speed': 21,
        'wing_loading': 200,
        'construction': 'composite',
        'min_thickness': 0.14,  # Thicker for structural loads
    },
}

# Air properties at sea level
RHO = 1.225  # kg/m³
NU = 1.5e-5  # kinematic viscosity m²/s
SPEED_OF_SOUND = 343  # m/s


def calculate_reynolds(chord, velocity):
    """Calculate Reynolds number."""
    return velocity * chord / NU


def calculate_design_cl(wing_loading_gdm2, velocity, rho=RHO):
    """
    Calculate required CL for level flight.
    wing_loading in g/dm² (= 10 * kg/m²)
    """
    wing_loading_kgm2 = wing_loading_gdm2 / 10  # Convert g/dm² to kg/m²
    weight_per_area = wing_loading_kgm2 * 9.81  # N/m²
    q = 0.5 * rho * velocity**2  # Dynamic pressure
    return weight_per_area / q


# =============================================================================
# FOAM-BUILDABLE AIRFOILS
# =============================================================================

def create_kfm2_airfoil(chord_fraction=0.5, step_height=0.04, n_points=100):
    """
    Create KFm2 (Kline-Fogleman mod 2) airfoil.

    KFm2 has a step on top surface that creates a trapped vortex.
    Excellent for foam construction and low Reynolds numbers.

    Args:
        chord_fraction: Location of step (0.5 = 50% chord)
        step_height: Height of step as fraction of chord
        n_points: Number of points per surface
    """
    # Upper surface with step
    x_upper_front = np.linspace(0, chord_fraction, n_points // 2)
    x_upper_back = np.linspace(chord_fraction, 1, n_points // 2)

    # Simple curved upper surface (before step)
    y_upper_front = step_height + 0.06 * np.sin(np.pi * x_upper_front / chord_fraction)

    # Flat after step
    y_upper_back = np.linspace(step_height, 0, len(x_upper_back))

    x_upper = np.concatenate([x_upper_front, x_upper_back])
    y_upper = np.concatenate([y_upper_front, y_upper_back])

    # Lower surface - flat
    x_lower = np.linspace(1, 0, n_points)
    y_lower = np.zeros_like(x_lower)

    # Combine (counterclockwise from TE)
    x = np.concatenate([x_upper, x_lower[1:]])
    y = np.concatenate([y_upper, y_lower[1:]])

    coords = np.column_stack([x, y])
    return asb.Airfoil(coordinates=coords, name="KFm2")


def create_kfm3_airfoil(n_points=100):
    """
    Create KFm3 airfoil - step on both surfaces.
    Better lift than KFm2, still foam-friendly.
    """
    # Similar to KFm2 but with undercamber
    x_upper = np.linspace(0, 1, n_points)

    # Upper with step at 50%
    y_upper = np.where(
        x_upper < 0.5,
        0.06 + 0.04 * np.sin(np.pi * x_upper / 0.5),
        0.06 * (1 - (x_upper - 0.5) / 0.5)
    )

    # Lower with slight undercamber
    x_lower = np.linspace(1, 0, n_points)
    y_lower = -0.02 * np.sin(np.pi * x_lower)

    x = np.concatenate([x_upper, x_lower[1:]])
    y = np.concatenate([y_upper, y_lower[1:]])

    coords = np.column_stack([x, y])
    return asb.Airfoil(coordinates=coords, name="KFm3")


def create_flat_bottom_airfoil(thickness=0.12, camber=0.04, n_points=100):
    """
    Create flat-bottom (semi-symmetrical) airfoil.
    Classic trainer airfoil, easy to build.
    """
    x = np.linspace(0, 1, n_points)

    # NACA-style thickness distribution
    t = thickness
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 +
                  0.2843 * x**3 - 0.1015 * x**4)

    # Camber line (flat bottom means camber = upper surface offset)
    yc = camber * 4 * x * (1 - x)

    # Upper surface
    x_upper = x
    y_upper = yc + yt

    # Lower surface - flat
    x_lower = np.flip(x)
    y_lower = np.zeros_like(x_lower)

    x_coords = np.concatenate([x_upper, x_lower[1:]])
    y_coords = np.concatenate([y_upper, y_lower[1:]])

    coords = np.column_stack([x_coords, y_coords])
    return asb.Airfoil(coordinates=coords, name=f"FlatBottom-{int(thickness*100)}")


def create_undercamber_airfoil(thickness=0.10, camber=0.06, n_points=100):
    """
    Create undercambered airfoil.
    High lift at low speeds, good for slow flyers.
    """
    x = np.linspace(0, 1, n_points)

    # Thickness distribution
    t = thickness
    yt = 5 * t * (0.2969 * np.sqrt(x + 0.001) - 0.1260 * x - 0.3516 * x**2 +
                  0.2843 * x**3 - 0.1015 * x**4)

    # Upper surface
    x_upper = x
    y_upper = yt * 0.6 + camber * 4 * x * (1 - x)

    # Lower surface with undercamber
    x_lower = np.flip(x)
    y_lower = -yt * 0.4 - camber * 2 * x * (1 - x)
    y_lower = np.flip(y_lower)

    x_coords = np.concatenate([x_upper, x_lower[1:]])
    y_coords = np.concatenate([y_upper, y_lower[1:]])

    coords = np.column_stack([x_coords, y_coords])
    return asb.Airfoil(coordinates=coords, name="Undercamber")


def get_foam_airfoils():
    """Get all foam-buildable airfoil options."""
    return {
        'KFm2': create_kfm2_airfoil(),
        'KFm3': create_kfm3_airfoil(),
        'FlatBottom-10': create_flat_bottom_airfoil(thickness=0.10),
        'FlatBottom-12': create_flat_bottom_airfoil(thickness=0.12),
        'Undercamber': create_undercamber_airfoil(),
    }


def get_standard_airfoils():
    """Get standard airfoils from database."""
    return {
        'E387': asb.Airfoil("e387"),
        'S3021': asb.Airfoil("s3021"),
        'SD7037': asb.Airfoil("sd7037"),
        'ClarkY': asb.Airfoil("clarky"),
        'NACA2412': asb.Airfoil("naca2412"),
        'MH32': asb.Airfoil("mh32"),
        'AG35': asb.Airfoil("ag35"),
    }


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_airfoil(airfoil, Re, Mach, alpha_range=None):
    """
    Analyze airfoil using NeuralFoil.

    Returns dict with CL, CD, CM, L/D arrays.
    """
    if alpha_range is None:
        alpha_range = np.linspace(-4, 14, 25)

    results = {
        'alpha': [],
        'CL': [],
        'CD': [],
        'CM': [],
        'L/D': [],
    }

    for alpha in alpha_range:
        try:
            aero = airfoil.get_aero_from_neuralfoil(
                alpha=alpha,
                Re=Re,
                mach=Mach,
            )

            cl = float(aero.get('CL', aero.get('cl', 0)))
            cd = float(aero.get('CD', aero.get('cd', 0)))
            cm = float(aero.get('CM', aero.get('cm', 0)))

            # Ensure positive drag
            cd = max(cd, 0.001)
            ld = cl / cd

            results['alpha'].append(alpha)
            results['CL'].append(cl)
            results['CD'].append(cd)
            results['CM'].append(cm)
            results['L/D'].append(ld)

        except Exception as e:
            continue

    for key in results:
        results[key] = np.array(results[key])

    return results


def find_performance_at_cl(results, target_cl):
    """Find performance metrics at a target CL."""
    if len(results['CL']) == 0:
        return None

    idx = np.argmin(np.abs(results['CL'] - target_cl))

    return {
        'alpha': results['alpha'][idx],
        'CL': results['CL'][idx],
        'CD': results['CD'][idx],
        'CM': results['CM'][idx],
        'L/D': results['L/D'][idx],
    }


# =============================================================================
# OPTIMIZATION
# =============================================================================

def optimize_airfoil_for_version(version_name, specs, baseline_name='E387'):
    """
    Optimize airfoil for a specific version using NeuralFoil.
    """
    Re = calculate_reynolds(specs['chord'], specs['cruise_speed'])
    Mach = specs['cruise_speed'] / SPEED_OF_SOUND
    target_cl = calculate_design_cl(specs['wing_loading'], specs['cruise_speed'])
    min_thickness = specs['min_thickness']

    print(f"\n{'='*60}")
    print(f"Optimizing airfoil for {version_name}: {specs['name']}")
    print(f"{'='*60}")
    print(f"  Reynolds Number: {Re:,.0f}")
    print(f"  Mach Number: {Mach:.4f}")
    print(f"  Target CL: {target_cl:.3f}")
    print(f"  Min Thickness: {min_thickness*100:.0f}%")

    # Get baseline
    try:
        baseline = asb.Airfoil(baseline_name.lower())
    except:
        baseline = asb.Airfoil("e387")

    # Setup optimization
    opti = asb.Opti()

    # Design variables
    n_weights = 8
    upper_weights = opti.variable(
        init_guess=np.array([0.2, 0.25, 0.2, 0.15, 0.12, 0.1, 0.08, 0.05]),
        lower_bound=0.05,
        upper_bound=0.5,
    )
    lower_weights = opti.variable(
        init_guess=np.array([-0.1, -0.08, -0.05, -0.02, 0.0, 0.01, 0.02, 0.01]),
        lower_bound=-0.25,
        upper_bound=0.15,
    )

    alpha = opti.variable(init_guess=4.0, lower_bound=-2, upper_bound=12)

    # Create airfoil
    airfoil = asb.KulfanAirfoil(
        upper_weights=upper_weights,
        lower_weights=lower_weights,
        leading_edge_weight=0,
        TE_thickness=0.002,
    )

    # Get aero coefficients
    aero = airfoil.get_aero_from_neuralfoil(
        alpha=alpha,
        Re=Re,
        mach=Mach,
    )

    CL = aero["CL"]
    CD = aero["CD"]
    CM = aero["CM"]

    # Objective: Maximize L/D at target CL
    L_over_D = CL / CD
    opti.minimize(-L_over_D)

    # Constraints
    opti.subject_to(CL >= target_cl * 0.9)
    opti.subject_to(CL <= target_cl * 1.1)
    opti.subject_to(CM >= -0.15)
    opti.subject_to(CM <= 0.05)

    # Solve
    try:
        sol = opti.solve(verbose=False, max_iter=300)

        opt_upper = sol(upper_weights)
        opt_lower = sol(lower_weights)
        opt_alpha = float(sol(alpha))
        opt_CL = float(sol(CL))
        opt_CD = float(sol(CD))
        opt_CM = float(sol(CM))
        opt_LD = float(sol(L_over_D))

        print(f"\n  Optimization Successful!")
        print(f"    Design Alpha: {opt_alpha:.2f}°")
        print(f"    CL: {opt_CL:.4f}")
        print(f"    CD: {opt_CD:.5f}")
        print(f"    CM: {opt_CM:.4f}")
        print(f"    L/D: {opt_LD:.1f}")

        # Create optimized airfoil
        optimized = asb.KulfanAirfoil(
            upper_weights=opt_upper,
            lower_weights=opt_lower,
            leading_edge_weight=0,
            TE_thickness=0.002,
        )

        return optimized, {
            'version': version_name,
            'Re': Re,
            'Mach': Mach,
            'target_CL': target_cl,
            'design_alpha': opt_alpha,
            'CL': opt_CL,
            'CD': opt_CD,
            'CM': opt_CM,
            'L/D': opt_LD,
            'upper_weights': opt_upper.tolist(),
            'lower_weights': opt_lower.tolist(),
        }

    except Exception as e:
        print(f"\n  Optimization failed: {e}")
        return baseline, None


# =============================================================================
# EXPORT FUNCTIONS
# =============================================================================

def export_airfoil_dat(airfoil, filename, header=""):
    """Export airfoil coordinates in Selig format."""
    coords = airfoil.coordinates

    with open(filename, 'w') as f:
        f.write(f"{header}\n")
        for x, y in coords:
            f.write(f"{x:.6f} {y:.6f}\n")

    print(f"  Saved: {filename}")


def export_airfoil_stl(airfoil, filename, chord=1.0, span=0.1, te_thickness=0.002):
    """
    Export airfoil as STL for 3D printing.
    Creates a wing section of given span.
    """
    try:
        from stl import mesh as stl_mesh
        import numpy as np_regular

        coords = airfoil.coordinates
        n_points = len(coords)

        # Create vertices for both ends of the span
        vertices = []
        for z in [0, span]:
            for x, y in coords:
                vertices.append([x * chord, y * chord, z])

        vertices = np_regular.array(vertices)

        # Create faces (simplified - just surface)
        faces = []
        for i in range(n_points - 1):
            # Front face triangles
            faces.append([i, i + 1, i + n_points])
            faces.append([i + 1, i + n_points + 1, i + n_points])

        # Create mesh
        airfoil_mesh = stl_mesh.Mesh(np_regular.zeros(len(faces), dtype=stl_mesh.Mesh.dtype))
        for i, face in enumerate(faces):
            for j in range(3):
                airfoil_mesh.vectors[i][j] = vertices[face[j]]

        airfoil_mesh.save(filename)
        print(f"  Saved STL: {filename}")

    except ImportError:
        print("  STL export requires numpy-stl package")


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_full_analysis(output_dir=None):
    """
    Run complete airfoil analysis for all versions.
    """
    if output_dir is None:
        output_dir = Path("/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/airfoils")
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("MegaDrone Multi-Version Airfoil Optimization")
    print("Using NeuralFoil for rapid aerodynamic analysis")
    print("=" * 70)

    # Get all airfoils to test
    foam_airfoils = get_foam_airfoils()
    standard_airfoils = get_standard_airfoils()
    all_airfoils = {**foam_airfoils, **standard_airfoils}

    # Results storage
    all_results = {}
    optimized_airfoils = {}

    # Analyze each version
    for version_name, specs in VERSIONS.items():
        Re = calculate_reynolds(specs['chord'], specs['cruise_speed'])
        Mach = specs['cruise_speed'] / SPEED_OF_SOUND
        target_cl = calculate_design_cl(specs['wing_loading'], specs['cruise_speed'])

        print(f"\n{'='*70}")
        print(f"VERSION: {version_name} - {specs['name']}")
        print(f"{'='*70}")
        print(f"  Chord: {specs['chord']*1000:.0f} mm")
        print(f"  Cruise Speed: {specs['cruise_speed']} m/s")
        print(f"  Wing Loading: {specs['wing_loading']} g/dm²")
        print(f"  Reynolds Number: {Re:,.0f}")
        print(f"  Target CL: {target_cl:.3f}")
        print(f"  Construction: {specs['construction']}")

        version_results = {}

        # Test all airfoils
        print(f"\n  Testing {len(all_airfoils)} airfoils...")

        for name, airfoil in all_airfoils.items():
            try:
                results = analyze_airfoil(airfoil, Re, Mach)
                perf = find_performance_at_cl(results, target_cl)

                if perf is not None:
                    version_results[name] = {
                        'full_results': results,
                        'at_design_cl': perf,
                    }
            except Exception as e:
                print(f"    Warning: {name} analysis failed: {e}")

        # Find best performers
        if version_results:
            sorted_by_ld = sorted(
                version_results.items(),
                key=lambda x: x[1]['at_design_cl']['L/D'] if x[1]['at_design_cl'] else 0,
                reverse=True
            )

            print(f"\n  Top 5 airfoils at CL={target_cl:.2f}:")
            print(f"  {'Airfoil':<20} {'L/D':>8} {'CD':>10} {'Alpha':>8}")
            print(f"  {'-'*48}")

            for name, data in sorted_by_ld[:5]:
                perf = data['at_design_cl']
                foam_marker = "*" if name in foam_airfoils else " "
                print(f"  {foam_marker}{name:<19} {perf['L/D']:>8.1f} {perf['CD']:>10.5f} {perf['alpha']:>7.1f}°")

            print(f"\n  * = Foam-buildable")

            # Best foam option
            best_foam = None
            for name, data in sorted_by_ld:
                if name in foam_airfoils:
                    best_foam = (name, data)
                    break

            if best_foam:
                print(f"\n  Best foam airfoil: {best_foam[0]}")
                print(f"    L/D: {best_foam[1]['at_design_cl']['L/D']:.1f}")

        # Run optimization
        optimized, opt_data = optimize_airfoil_for_version(version_name, specs)

        if opt_data:
            optimized_airfoils[version_name] = {
                'airfoil': optimized,
                'data': opt_data,
            }

            # Export optimized airfoil
            export_airfoil_dat(
                optimized,
                output_dir / f"{version_name}_optimized.dat",
                header=f"MegaDrone {version_name} Optimized - Re={Re:.0f} CL={target_cl:.3f}"
            )

        all_results[version_name] = {
            'specs': specs,
            'Re': Re,
            'target_cl': target_cl,
            'airfoil_results': version_results,
            'optimized': opt_data,
        }

    # Create summary plots
    create_summary_plots(all_results, optimized_airfoils, output_dir)

    # Export summary JSON
    summary = {}
    for version_name, data in all_results.items():
        summary[version_name] = {
            'specs': data['specs'],
            'Re': data['Re'],
            'target_cl': data['target_cl'],
            'best_standard': None,
            'best_foam': None,
            'optimized': data['optimized'],
        }

        # Find best airfoils
        if data['airfoil_results']:
            sorted_results = sorted(
                data['airfoil_results'].items(),
                key=lambda x: x[1]['at_design_cl']['L/D'] if x[1]['at_design_cl'] else 0,
                reverse=True
            )

            if sorted_results:
                best = sorted_results[0]
                summary[version_name]['best_standard'] = {
                    'name': best[0],
                    'L/D': best[1]['at_design_cl']['L/D'],
                    'CD': best[1]['at_design_cl']['CD'],
                }

            for name, perf in sorted_results:
                if name in foam_airfoils:
                    summary[version_name]['best_foam'] = {
                        'name': name,
                        'L/D': perf['at_design_cl']['L/D'],
                        'CD': perf['at_design_cl']['CD'],
                    }
                    break

    with open(output_dir / "airfoil_summary.json", 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\n{'='*70}")
    print("Analysis Complete!")
    print(f"Results saved to: {output_dir}")
    print(f"{'='*70}")

    return all_results, optimized_airfoils


def create_summary_plots(all_results, optimized_airfoils, output_dir):
    """Create summary plots for all versions."""

    n_versions = len(all_results)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for idx, (version_name, data) in enumerate(all_results.items()):
        if idx >= 6:
            break

        ax = axes[idx]

        # Plot drag polars for top airfoils
        sorted_results = sorted(
            data['airfoil_results'].items(),
            key=lambda x: x[1]['at_design_cl']['L/D'] if x[1]['at_design_cl'] else 0,
            reverse=True
        )[:5]

        colors = plt.cm.tab10(np.linspace(0, 1, 5))

        for (name, perf), color in zip(sorted_results, colors):
            results = perf['full_results']
            ax.plot(results['CD']*10000, results['CL'], '-',
                   color=color, linewidth=1.5, label=name)

        # Plot optimized if available
        if version_name in optimized_airfoils:
            opt = optimized_airfoils[version_name]
            opt_results = analyze_airfoil(
                opt['airfoil'],
                data['Re'],
                data['specs']['cruise_speed'] / SPEED_OF_SOUND
            )
            ax.plot(opt_results['CD']*10000, opt_results['CL'], 'k--',
                   linewidth=2, label='Optimized')

        ax.axhline(y=data['target_cl'], color='r', linestyle=':', alpha=0.5)
        ax.set_xlabel('CD × 10⁴')
        ax.set_ylabel('CL')
        ax.set_title(f"{version_name}: Re={data['Re']:,.0f}")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "airfoil_comparison_all_versions.png", dpi=150)
    print(f"\nSaved: {output_dir}/airfoil_comparison_all_versions.png")
    plt.close()

    # L/D comparison bar chart
    fig, ax = plt.subplots(figsize=(12, 6))

    versions = list(all_results.keys())
    x = np.arange(len(versions))
    width = 0.25

    best_standard_ld = []
    best_foam_ld = []
    optimized_ld = []

    foam_airfoils = get_foam_airfoils()

    for version_name in versions:
        data = all_results[version_name]

        # Best standard
        sorted_results = sorted(
            data['airfoil_results'].items(),
            key=lambda x: x[1]['at_design_cl']['L/D'] if x[1]['at_design_cl'] else 0,
            reverse=True
        )

        if sorted_results:
            best_standard_ld.append(sorted_results[0][1]['at_design_cl']['L/D'])
        else:
            best_standard_ld.append(0)

        # Best foam
        best_foam = 0
        for name, perf in sorted_results:
            if name in foam_airfoils and perf['at_design_cl']:
                best_foam = perf['at_design_cl']['L/D']
                break
        best_foam_ld.append(best_foam)

        # Optimized
        if data['optimized']:
            optimized_ld.append(data['optimized']['L/D'])
        else:
            optimized_ld.append(0)

    ax.bar(x - width, best_foam_ld, width, label='Best Foam', color='green', alpha=0.7)
    ax.bar(x, best_standard_ld, width, label='Best Standard', color='blue', alpha=0.7)
    ax.bar(x + width, optimized_ld, width, label='Optimized', color='red', alpha=0.7)

    ax.set_ylabel('L/D at Design CL')
    ax.set_xlabel('Version')
    ax.set_title('Airfoil Performance Comparison by Version')
    ax.set_xticks(x)
    ax.set_xticklabels(versions)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_dir / "ld_comparison_by_version.png", dpi=150)
    print(f"Saved: {output_dir}/ld_comparison_by_version.png")
    plt.close()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    results, optimized = run_full_analysis()
