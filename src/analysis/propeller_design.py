#!/usr/bin/env python3
"""
Propeller Design for MegaDrone Phase 1
Matches propeller to motor for cruise efficiency

Uses simplified blade element theory and motor performance curves
to select optimal propeller diameter and pitch.

Author: MegaDrone Project
Date: January 8, 2026
"""

import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# DESIGN REQUIREMENTS
# =============================================================================

# From sizing analysis
CRUISE_POWER_W = 66       # Watts at propeller shaft
CRUISE_THRUST_N = 2.57    # N (drag at cruise)
CRUISE_SPEED_MS = 25.7    # m/s (50 knots)
LOITER_POWER_W = 21       # Watts
LOITER_THRUST_N = 1.4     # N
LOITER_SPEED_MS = 15.0    # m/s

# Motor requirements
MOTOR_POWER_RATING_W = 150  # Continuous rated power
MOTOR_KV = 920              # RPM per volt (typical for this class)
BATTERY_VOLTAGE = 14.8      # 4S LiPo nominal
MOTOR_EFFICIENCY = 0.85     # Typical for quality BLDC

# Physical constants
RHO = 1.21  # kg/m³ at cruise altitude

# =============================================================================
# PROPELLER PERFORMANCE MODEL
# =============================================================================

def propeller_thrust_power(diameter_m, pitch_m, rpm, velocity_ms, rho=RHO):
    """Calculate propeller thrust and power using simplified momentum theory.

    Based on static thrust approximation with advance ratio correction.

    Args:
        diameter_m: Propeller diameter in meters
        pitch_m: Propeller pitch in meters
        rpm: Rotational speed
        velocity_ms: Forward velocity
        rho: Air density

    Returns:
        thrust (N), power (W), efficiency
    """

    # Convert to angular velocity
    n = rpm / 60  # rev/s
    omega = 2 * np.pi * n

    # Advance ratio J = V / (n * D)
    J = velocity_ms / (n * diameter_m) if n > 0 else 0

    # Propeller coefficients (empirical for typical model propellers)
    # Thrust coefficient: CT = CT0 * (1 - J/J_max)^2
    # Power coefficient: CP = CP0 * (1 + k*J)

    # Typical values for APC-style props
    CT0 = 0.10  # Static thrust coefficient
    CP0 = 0.045  # Static power coefficient
    J_max = 0.85  # Maximum advance ratio (zero thrust)

    # Coefficients adjusted for pitch/diameter ratio
    pitch_ratio = pitch_m / diameter_m
    CT0_adj = CT0 * (0.5 + pitch_ratio)
    CP0_adj = CP0 * (0.5 + pitch_ratio)

    # Calculate coefficients at operating J
    if J < J_max:
        CT = CT0_adj * (1 - (J / J_max)**1.5)
        CP = CP0_adj * (1 + 0.5 * J)
    else:
        CT = 0
        CP = CP0_adj * 0.5  # Windmilling

    # Thrust and power
    thrust = CT * rho * n**2 * diameter_m**4
    power = CP * rho * n**3 * diameter_m**5

    # Propulsive efficiency
    if power > 0 and thrust > 0:
        efficiency = thrust * velocity_ms / power
    else:
        efficiency = 0

    return thrust, power, efficiency


def find_operating_rpm(diameter_m, pitch_m, target_thrust_n, velocity_ms, rpm_range=(2000, 12000)):
    """Find RPM that produces target thrust at given velocity."""

    from scipy.optimize import brentq

    def thrust_error(rpm):
        thrust, _, _ = propeller_thrust_power(diameter_m, pitch_m, rpm, velocity_ms)
        return thrust - target_thrust_n

    try:
        rpm_solution = brentq(thrust_error, rpm_range[0], rpm_range[1])
        thrust, power, efficiency = propeller_thrust_power(diameter_m, pitch_m, rpm_solution, velocity_ms)
        return rpm_solution, power, efficiency
    except ValueError:
        return None, None, None


def motor_available_power(rpm, kv, voltage, efficiency=0.85):
    """Calculate motor power available at given RPM.

    Simplified motor model assuming:
    - Linear torque-speed characteristic
    - Constant efficiency (good approximation at cruise)
    """

    no_load_rpm = kv * voltage
    if rpm > no_load_rpm:
        return 0

    # Torque proportional to (no_load_rpm - rpm)
    torque_fraction = 1 - (rpm / no_load_rpm)

    # Power = omega * torque
    omega = 2 * np.pi * rpm / 60
    max_power = 200  # Approximate max shaft power

    power = max_power * torque_fraction * (rpm / no_load_rpm) * efficiency

    return power


# =============================================================================
# PROPELLER SELECTION
# =============================================================================

def analyze_propeller_range():
    """Analyze performance across range of propeller sizes."""

    print("=" * 70)
    print("Propeller Performance Analysis")
    print("=" * 70)
    print(f"\nDesign Requirements:")
    print(f"  Cruise: {CRUISE_THRUST_N:.2f} N thrust at {CRUISE_SPEED_MS} m/s, {CRUISE_POWER_W} W")
    print(f"  Loiter: {LOITER_THRUST_N:.2f} N thrust at {LOITER_SPEED_MS} m/s, {LOITER_POWER_W} W")

    # Propeller sizes to analyze (diameter in inches)
    diameters_in = [8, 9, 10, 11, 12, 13, 14]
    pitch_ratios = [0.5, 0.6, 0.7, 0.8]  # pitch/diameter

    results = []

    print(f"\n{'Prop':^10} {'Pitch':^8} {'Cruise RPM':^12} {'Cruise Eff':^12} {'Loiter RPM':^12} {'Loiter Eff':^12}")
    print("-" * 70)

    for d_in in diameters_in:
        d_m = d_in * 0.0254  # Convert to meters

        for pr in pitch_ratios:
            pitch_in = d_in * pr
            pitch_m = pitch_in * 0.0254

            # Find cruise operating point
            cruise_rpm, cruise_power, cruise_eff = find_operating_rpm(
                d_m, pitch_m, CRUISE_THRUST_N, CRUISE_SPEED_MS
            )

            # Find loiter operating point
            loiter_rpm, loiter_power, loiter_eff = find_operating_rpm(
                d_m, pitch_m, LOITER_THRUST_N, LOITER_SPEED_MS
            )

            if cruise_rpm is not None and loiter_rpm is not None:
                # Check motor can deliver required power at this RPM
                max_rpm = MOTOR_KV * BATTERY_VOLTAGE
                rpm_margin = (max_rpm - cruise_rpm) / max_rpm * 100

                result = {
                    'diameter_in': d_in,
                    'pitch_in': pitch_in,
                    'cruise_rpm': cruise_rpm,
                    'cruise_power': cruise_power,
                    'cruise_efficiency': cruise_eff,
                    'loiter_rpm': loiter_rpm,
                    'loiter_power': loiter_power,
                    'loiter_efficiency': loiter_eff,
                    'rpm_margin': rpm_margin,
                }

                if rpm_margin > 10:  # At least 10% RPM margin
                    results.append(result)

                    print(f"{d_in}x{pitch_in:.1f}    {pitch_in:.1f}in   "
                          f"{cruise_rpm:7.0f}      {cruise_eff*100:5.1f}%       "
                          f"{loiter_rpm:7.0f}      {loiter_eff*100:5.1f}%")

    return results


def select_optimal_propeller(results):
    """Select optimal propeller based on cruise efficiency."""

    if not results:
        print("\nNo suitable propellers found!")
        return None

    # Sort by cruise efficiency
    sorted_results = sorted(results, key=lambda x: x['cruise_efficiency'], reverse=True)

    # Top 5 candidates
    print("\n" + "=" * 70)
    print("TOP PROPELLER CANDIDATES (sorted by cruise efficiency)")
    print("=" * 70)

    for i, r in enumerate(sorted_results[:5]):
        print(f"\n{i+1}. {r['diameter_in']}x{r['pitch_in']:.1f} inch")
        print(f"   Cruise:  {r['cruise_rpm']:.0f} RPM, η = {r['cruise_efficiency']*100:.1f}%, P = {r['cruise_power']:.1f} W")
        print(f"   Loiter:  {r['loiter_rpm']:.0f} RPM, η = {r['loiter_efficiency']*100:.1f}%, P = {r['loiter_power']:.1f} W")
        print(f"   RPM Margin: {r['rpm_margin']:.1f}%")

    # Return best
    return sorted_results[0]


def plot_propeller_performance(best_prop):
    """Plot performance curves for selected propeller."""

    d_m = best_prop['diameter_in'] * 0.0254
    pitch_m = best_prop['pitch_in'] * 0.0254

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Velocity range
    velocities = np.linspace(0, 35, 50)
    rpm_values = [4000, 6000, 8000, 10000]

    # Thrust vs Velocity at various RPM
    ax = axes[0, 0]
    for rpm in rpm_values:
        thrusts = [propeller_thrust_power(d_m, pitch_m, rpm, v)[0] for v in velocities]
        ax.plot(velocities, thrusts, linewidth=2, label=f'{rpm} RPM')

    ax.axhline(y=CRUISE_THRUST_N, color='r', linestyle='--', alpha=0.7, label='Cruise Thrust')
    ax.axvline(x=CRUISE_SPEED_MS, color='r', linestyle=':', alpha=0.7)
    ax.set_xlabel('Velocity (m/s)')
    ax.set_ylabel('Thrust (N)')
    ax.set_title(f'{best_prop["diameter_in"]}x{best_prop["pitch_in"]:.1f} Thrust Curves')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Efficiency vs Velocity
    ax = axes[0, 1]
    for rpm in rpm_values:
        effs = [propeller_thrust_power(d_m, pitch_m, rpm, v)[2] * 100 for v in velocities]
        ax.plot(velocities, effs, linewidth=2, label=f'{rpm} RPM')

    ax.axvline(x=CRUISE_SPEED_MS, color='r', linestyle='--', alpha=0.7, label='Cruise')
    ax.axvline(x=LOITER_SPEED_MS, color='g', linestyle='--', alpha=0.7, label='Loiter')
    ax.set_xlabel('Velocity (m/s)')
    ax.set_ylabel('Propulsive Efficiency (%)')
    ax.set_title('Efficiency vs Velocity')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 90])

    # Power vs Velocity
    ax = axes[1, 0]
    for rpm in rpm_values:
        powers = [propeller_thrust_power(d_m, pitch_m, rpm, v)[1] for v in velocities]
        ax.plot(velocities, powers, linewidth=2, label=f'{rpm} RPM')

    ax.axhline(y=CRUISE_POWER_W, color='r', linestyle='--', alpha=0.7, label='Cruise Power')
    ax.axvline(x=CRUISE_SPEED_MS, color='r', linestyle=':', alpha=0.7)
    ax.set_xlabel('Velocity (m/s)')
    ax.set_ylabel('Power (W)')
    ax.set_title('Power Required')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Motor-Propeller matching
    ax = axes[1, 1]
    rpms = np.linspace(2000, 13000, 100)

    # Power required at cruise
    cruise_power_req = []
    for rpm in rpms:
        t, p, e = propeller_thrust_power(d_m, pitch_m, rpm, CRUISE_SPEED_MS)
        cruise_power_req.append(p)

    # Motor power available
    motor_power_avail = [motor_available_power(rpm, MOTOR_KV, BATTERY_VOLTAGE) for rpm in rpms]

    ax.plot(rpms, cruise_power_req, 'b-', linewidth=2, label='Prop Power Required')
    ax.plot(rpms, motor_power_avail, 'r-', linewidth=2, label='Motor Power Available')
    ax.axvline(x=best_prop['cruise_rpm'], color='g', linestyle='--',
               label=f'Operating Point ({best_prop["cruise_rpm"]:.0f} RPM)')
    ax.set_xlabel('RPM')
    ax.set_ylabel('Power (W)')
    ax.set_title('Motor-Propeller Matching')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim([2000, 13000])

    plt.tight_layout()
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/propeller_performance.png',
                dpi=150, bbox_inches='tight')
    print("\nSaved: designs/propeller_performance.png")
    plt.show()

    return fig


# =============================================================================
# MOTOR SELECTION
# =============================================================================

def recommend_motor():
    """Recommend motor specifications."""

    print("\n" + "=" * 70)
    print("MOTOR RECOMMENDATIONS")
    print("=" * 70)

    # Calculate requirements
    cruise_power_shaft = CRUISE_POWER_W / MOTOR_EFFICIENCY
    max_power_shaft = cruise_power_shaft * 2.5  # Headroom for climb

    # Typical motor specs for this class
    print(f"""
    MOTOR SPECIFICATIONS:
    ---------------------
    Power Class:        150-200W continuous
    KV Rating:          800-1000 RPM/V (for 10-12" props)
    Weight:             40-60g
    Shaft:              3mm or 4mm

    RECOMMENDED MODELS:
    ------------------
    1. SunnySky X2212-980KV (58g, 180W, excellent efficiency)
    2. T-Motor AT2312-900KV (52g, 200W, high quality)
    3. EMAX GT2215-09 (920KV, 55g, good value)

    ESC REQUIREMENTS:
    -----------------
    Current Rating:     20-30A continuous
    BEC:                5V/3A for servos
    Weight:             ~25g

    BATTERY:
    --------
    Configuration:      4S LiPo (14.8V nominal)
    Capacity:           3000-4000 mAh
    C-Rating:           30C+ for headroom
    Weight:             ~300g for 3300mAh
    """)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main propeller design routine."""

    print("=" * 70)
    print("MegaDrone Phase 1 - Propeller Design")
    print("=" * 70)

    # Analyze propeller range
    results = analyze_propeller_range()

    # Select optimal
    best_prop = select_optimal_propeller(results)

    if best_prop:
        # Plot performance
        plot_propeller_performance(best_prop)

        # Summary
        print("\n" + "=" * 70)
        print("SELECTED PROPELLER")
        print("=" * 70)
        print(f"""
    PROPELLER: {best_prop['diameter_in']}x{best_prop['pitch_in']:.1f} inch
    -------------------------------------------
    Cruise (50 kt):
      - RPM:        {best_prop['cruise_rpm']:.0f}
      - Efficiency: {best_prop['cruise_efficiency']*100:.1f}%
      - Power:      {best_prop['cruise_power']:.1f} W

    Loiter (29 kt):
      - RPM:        {best_prop['loiter_rpm']:.0f}
      - Efficiency: {best_prop['loiter_efficiency']*100:.1f}%
      - Power:      {best_prop['loiter_power']:.1f} W

    RECOMMENDED PROPS (commercial):
    - APC 11x7E (thin electric)
    - Aeronaut CAM 11x7
    - Graupner E-Prop 11x7
        """)

    # Motor recommendations
    recommend_motor()

    return best_prop


if __name__ == "__main__":
    best_prop = main()
