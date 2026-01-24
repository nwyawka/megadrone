#!/usr/bin/env python3
"""
Drone Initial Sizing Script
Small Fixed-Wing Electric Drone Design

Requirements:
- Range: 50 km
- Payload: 0.5 kg
- Cruise Speed: 50 knots (25.7 m/s)
- Propulsion: Single electric motor

Author: MegaDrone Project
Date: January 8, 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# MISSION REQUIREMENTS
# =============================================================================

# Mission: 50 km out + 50 km back + 15 min loiter
RANGE_OUT_KM = 50  # km (one way)
RANGE_BACK_KM = 50  # km (return)
RANGE_TOTAL_KM = RANGE_OUT_KM + RANGE_BACK_KM  # 100 km round trip
LOITER_TIME_MIN = 15  # minutes

PAYLOAD_KG = 0.5  # kg (camera pod)
PAYLOAD_POWER_W = 5  # W (camera power draw estimate)

CRUISE_SPEED_KNOTS = 50  # knots
CRUISE_SPEED_MS = CRUISE_SPEED_KNOTS * 0.5144  # 25.72 m/s
LOITER_SPEED_MS = 15  # m/s (slower loiter for efficiency)
CRUISE_ALTITUDE_M = 150  # m AGL

# Hand launch constraint
MAX_STALL_SPEED_MS = 10  # m/s (~20 knots) for safe hand launch

# Physical constants
G = 9.81  # m/s^2
RHO_SEA_LEVEL = 1.225  # kg/m^3 (sea level standard)
RHO_CRUISE = 1.21  # kg/m^3 (approximate at 150m)

# =============================================================================
# INITIAL WEIGHT ESTIMATION
# =============================================================================

def estimate_weights():
    """Estimate component weights for initial sizing."""

    # Payload (fixed requirement)
    w_payload = PAYLOAD_KG

    # Avionics and electronics (typical for small surveillance drone)
    w_avionics = 0.15  # kg (flight controller, GPS, receiver, ESC)

    # Estimate battery weight based on energy requirements
    # Will be refined after propulsion sizing
    w_battery_estimate = 0.35  # kg (initial estimate, ~50 Wh @ 150 Wh/kg)

    # Motor and propeller
    w_motor = 0.08  # kg (200W class BLDC)
    w_propeller = 0.02  # kg

    # Structural weight (typically 25-35% of MTOW for small UAVs)
    # Using regression: W_struct = k * W_total^0.9
    # For foam/composite: k ~ 0.28

    # Initial estimate of structural weight
    w_structure_estimate = 0.45  # kg (will iterate)

    # Sum non-structural weights
    w_fixed = w_payload + w_avionics + w_battery_estimate + w_motor + w_propeller

    # Total weight (initial)
    w_total = w_fixed + w_structure_estimate

    return {
        'payload': w_payload,
        'avionics': w_avionics,
        'battery': w_battery_estimate,
        'motor': w_motor,
        'propeller': w_propeller,
        'structure': w_structure_estimate,
        'total': w_total,
        'fixed': w_fixed
    }


# =============================================================================
# AERODYNAMIC SIZING
# =============================================================================

def calculate_wing_parameters(w_total, wing_loading_pa):
    """Calculate wing geometry from weight and wing loading."""

    weight_n = w_total * G
    wing_area = weight_n / wing_loading_pa  # m^2

    return wing_area


def calculate_cruise_lift_coefficient(weight_n, wing_area, velocity, rho=RHO_CRUISE):
    """Calculate required lift coefficient at cruise."""

    dynamic_pressure = 0.5 * rho * velocity**2
    cl_cruise = weight_n / (dynamic_pressure * wing_area)

    return cl_cruise


def estimate_drag_coefficient(cl, aspect_ratio, oswald_efficiency=0.85, cd0=0.025):
    """Estimate total drag coefficient using parabolic polar.

    CD = CD0 + CL^2 / (pi * AR * e)

    For small UAVs:
    - CD0 ~ 0.02-0.03 (parasite drag)
    - e ~ 0.8-0.9 (Oswald efficiency)
    """

    cd_induced = cl**2 / (np.pi * aspect_ratio * oswald_efficiency)
    cd_total = cd0 + cd_induced

    return cd_total, cd0, cd_induced


def calculate_lift_to_drag(cl, cd):
    """Calculate L/D ratio."""
    return cl / cd


def calculate_max_ld(aspect_ratio, oswald_efficiency=0.85, cd0=0.025):
    """Calculate maximum L/D and optimal CL."""

    # At max L/D, induced drag = parasite drag
    cl_max_ld = np.sqrt(np.pi * aspect_ratio * oswald_efficiency * cd0)
    cd_at_max_ld = 2 * cd0  # Total CD = 2 * CD0 at max L/D
    ld_max = cl_max_ld / cd_at_max_ld

    return ld_max, cl_max_ld


# =============================================================================
# PROPULSION SIZING
# =============================================================================

def calculate_cruise_power(weight_n, velocity, ld_ratio):
    """Calculate power required at cruise.

    P_cruise = D * V = (W / L/D) * V
    """

    drag = weight_n / ld_ratio
    power_cruise = drag * velocity

    return power_cruise, drag


def calculate_mission_energy(weight_n, wing_area, aspect_ratio, cd0, oswald_e,
                             range_km, cruise_velocity, loiter_time_min, loiter_velocity,
                             payload_power_w=0, efficiency=0.70):
    """Calculate total energy required for complete mission.

    Mission phases:
    1. Climb to altitude (small for 150m)
    2. Cruise out (range_km / 2)
    3. Loiter (loiter_time_min)
    4. Cruise back (range_km / 2)
    5. Descent and landing

    Accounts for system efficiency:
    - Motor efficiency (~90%)
    - ESC efficiency (~95%)
    - Propeller efficiency (~80%)
    - Combined: ~68-75%
    """

    results = {}

    # --- CLIMB PHASE (simplified) ---
    climb_altitude = CRUISE_ALTITUDE_M  # 150m
    climb_rate = 2.0  # m/s
    climb_time = climb_altitude / climb_rate  # seconds
    # Climb power ~ 1.5x cruise power
    cl_climb = 0.6  # higher CL during climb
    cd_climb, _, _ = estimate_drag_coefficient(cl_climb, aspect_ratio, oswald_e, cd0)
    ld_climb = cl_climb / cd_climb
    climb_velocity = np.sqrt(2 * weight_n / (RHO_CRUISE * wing_area * cl_climb))
    power_climb = (weight_n / ld_climb) * climb_velocity + weight_n * climb_rate
    energy_climb = power_climb * climb_time / 3600  # Wh

    # --- CRUISE PHASES ---
    cl_cruise = weight_n / (0.5 * RHO_CRUISE * cruise_velocity**2 * wing_area)
    cd_cruise, _, _ = estimate_drag_coefficient(cl_cruise, aspect_ratio, oswald_e, cd0)
    ld_cruise = cl_cruise / cd_cruise
    power_cruise = (weight_n / ld_cruise) * cruise_velocity

    cruise_distance = range_km * 1000  # m
    cruise_time = cruise_distance / cruise_velocity  # seconds
    energy_cruise = power_cruise * cruise_time / 3600  # Wh

    # --- LOITER PHASE ---
    cl_loiter = weight_n / (0.5 * RHO_CRUISE * loiter_velocity**2 * wing_area)
    cd_loiter, _, _ = estimate_drag_coefficient(cl_loiter, aspect_ratio, oswald_e, cd0)
    ld_loiter = cl_loiter / cd_loiter
    power_loiter = (weight_n / ld_loiter) * loiter_velocity

    loiter_time = loiter_time_min * 60  # seconds
    energy_loiter = power_loiter * loiter_time / 3600  # Wh

    # --- PAYLOAD POWER ---
    total_flight_time = climb_time + cruise_time + loiter_time  # seconds
    energy_payload = payload_power_w * total_flight_time / 3600  # Wh

    # --- TOTAL ENERGY (at propeller shaft) ---
    energy_shaft = energy_climb + energy_cruise + energy_loiter + energy_payload

    # --- BATTERY ENERGY (with efficiency losses) ---
    energy_battery = energy_shaft / efficiency

    results = {
        'climb': {'time_min': climb_time/60, 'power_w': power_climb, 'energy_wh': energy_climb},
        'cruise': {'time_min': cruise_time/60, 'power_w': power_cruise, 'energy_wh': energy_cruise,
                   'cl': cl_cruise, 'cd': cd_cruise, 'ld': ld_cruise},
        'loiter': {'time_min': loiter_time/60, 'power_w': power_loiter, 'energy_wh': energy_loiter,
                   'cl': cl_loiter, 'cd': cd_loiter, 'ld': ld_loiter},
        'payload': {'power_w': payload_power_w, 'energy_wh': energy_payload},
        'total_flight_time_min': total_flight_time / 60,
        'energy_shaft_wh': energy_shaft,
        'energy_battery_wh': energy_battery
    }

    return results


def size_battery(energy_wh, reserve_factor=1.2, energy_density_wh_kg=180):
    """Size battery pack.

    Args:
        energy_wh: Required mission energy
        reserve_factor: Safety margin (1.2 = 20% reserve)
        energy_density_wh_kg: Battery specific energy (LiPo: 150-200 Wh/kg)
    """

    total_energy = energy_wh * reserve_factor
    battery_mass = total_energy / energy_density_wh_kg

    return battery_mass, total_energy


def size_motor(cruise_power, power_margin=2.5):
    """Size motor for cruise with margin for climb/maneuver.

    Args:
        cruise_power: Power required at cruise (W)
        power_margin: Factor for climb capability (2-3x typical)
    """

    motor_power_rating = cruise_power * power_margin

    # Motor mass estimation (small BLDC: ~0.3-0.5 g/W for power rating)
    motor_mass = motor_power_rating * 0.0004  # kg

    return motor_power_rating, motor_mass


# =============================================================================
# MATCHING CHART
# =============================================================================

def create_matching_chart(w_total, aspect_ratio=7, cd0=0.025, e=0.85):
    """Create matching chart showing design constraints."""

    weight_n = w_total * G

    # Wing loading range
    ws_range = np.linspace(20, 80, 100)  # N/m^2

    # Calculate required power-to-weight for each constraint

    # 1. Cruise constraint: P/W = V / (L/D)
    cruise_pw = []
    cruise_ld = []
    for ws in ws_range:
        s = weight_n / ws
        cl = weight_n / (0.5 * RHO_CRUISE * CRUISE_SPEED_MS**2 * s)
        cd, _, _ = estimate_drag_coefficient(cl, aspect_ratio, e, cd0)
        ld = cl / cd
        pw = CRUISE_SPEED_MS / ld  # W/N
        cruise_pw.append(pw)
        cruise_ld.append(ld)

    # 2. Stall constraint: W/S < 0.5 * rho * V_stall^2 * CL_max
    cl_max = 1.4  # Typical for simple airfoil without flaps
    v_stall_target = 12  # m/s (target stall speed)
    ws_stall_limit = 0.5 * RHO_CRUISE * v_stall_target**2 * cl_max

    # 3. Climb constraint: P/W = V_climb / (L/D) + ROC
    roc_target = 3  # m/s rate of climb
    climb_pw = []
    for ws in ws_range:
        s = weight_n / ws
        # Assume climb at V for best L/D (approximately)
        v_climb = 0.8 * CRUISE_SPEED_MS
        cl = weight_n / (0.5 * RHO_CRUISE * v_climb**2 * s)
        cd, _, _ = estimate_drag_coefficient(cl, aspect_ratio, e, cd0)
        ld = cl / cd
        pw = v_climb / ld + roc_target
        climb_pw.append(pw)

    return {
        'ws_range': ws_range,
        'cruise_pw': np.array(cruise_pw),
        'cruise_ld': np.array(cruise_ld),
        'climb_pw': np.array(climb_pw),
        'ws_stall_limit': ws_stall_limit
    }


def plot_matching_chart(matching_data, design_point=None):
    """Plot matching chart with constraints."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Matching chart
    ax1.plot(matching_data['ws_range'], matching_data['cruise_pw'],
             'b-', linewidth=2, label='Cruise Constraint')
    ax1.plot(matching_data['ws_range'], matching_data['climb_pw'],
             'g-', linewidth=2, label='Climb Constraint (3 m/s ROC)')
    ax1.axvline(x=matching_data['ws_stall_limit'], color='r',
                linestyle='--', linewidth=2, label=f'Stall Limit (12 m/s)')

    if design_point:
        ax1.plot(design_point['ws'], design_point['pw'], 'ko',
                 markersize=12, label='Design Point')

    ax1.set_xlabel('Wing Loading W/S (N/m²)', fontsize=12)
    ax1.set_ylabel('Power Loading P/W (W/N)', fontsize=12)
    ax1.set_title('Matching Chart - Design Space', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim([20, 80])
    ax1.set_ylim([0, 15])

    # Fill feasible region
    ax1.fill_between(matching_data['ws_range'],
                     np.maximum(matching_data['cruise_pw'], matching_data['climb_pw']),
                     15, alpha=0.1, color='green', label='Feasible Region')

    # L/D vs Wing Loading
    ax2.plot(matching_data['ws_range'], matching_data['cruise_ld'],
             'b-', linewidth=2)
    ax2.axvline(x=matching_data['ws_stall_limit'], color='r',
                linestyle='--', linewidth=2)

    if design_point:
        ax2.plot(design_point['ws'], design_point['ld'], 'ko', markersize=12)

    ax2.set_xlabel('Wing Loading W/S (N/m²)', fontsize=12)
    ax2.set_ylabel('Lift-to-Drag Ratio (L/D)', fontsize=12)
    ax2.set_title('L/D at Cruise vs Wing Loading', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([20, 80])

    plt.tight_layout()

    # Save figure
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/matching_chart.png',
                dpi=150, bbox_inches='tight')
    print("Saved: designs/matching_chart.png")

    plt.show()


# =============================================================================
# MAIN SIZING ROUTINE
# =============================================================================

def run_sizing():
    """Main sizing routine with iteration for converged solution."""

    print("=" * 70)
    print("SMALL FIXED-WING DRONE INITIAL SIZING")
    print("=" * 70)

    # Mission summary
    print("\n--- MISSION REQUIREMENTS ---")
    print(f"  Range Out:       {RANGE_OUT_KM} km")
    print(f"  Range Back:      {RANGE_BACK_KM} km")
    print(f"  Total Range:     {RANGE_TOTAL_KM} km (round trip)")
    print(f"  Loiter Time:     {LOITER_TIME_MIN} min")
    print(f"  Payload:         {PAYLOAD_KG} kg (camera pod, {PAYLOAD_POWER_W}W)")
    print(f"  Cruise Speed:    {CRUISE_SPEED_KNOTS} knots ({CRUISE_SPEED_MS:.1f} m/s)")
    print(f"  Loiter Speed:    {LOITER_SPEED_MS} m/s")
    print(f"  Altitude:        {CRUISE_ALTITUDE_M} m AGL")
    print(f"  Hand Launch:     Stall speed < {MAX_STALL_SPEED_MS} m/s")

    # Design parameters (fixed for this design)
    # Trade-off: Need higher wing loading for efficient cruise at 50 knots
    # but must keep stall speed below 10 m/s for hand launch
    #
    # At 50 knots (25.7 m/s), dynamic pressure q = 400 N/m²
    # For good L/D, want CL ~ 0.3-0.5 at cruise
    # W/S = q * CL_cruise → for CL=0.3, W/S = 120 N/m² (too high for hand launch)
    #
    # Stall constraint: V_stall = sqrt(2*W/S / (rho*CL_max))
    # For V_stall = 10 m/s, CL_max = 1.4: W/S_max = 0.5*1.21*100*1.4 = 85 N/m²
    aspect_ratio = 12.0  # Higher AR to boost L/D at low CL
    wing_loading_target = 80.0  # N/m² - stall ~9.7 m/s for hand launch
    cd0 = 0.020  # Very clean airframe with optimized airfoil
    oswald_e = 0.88  # Good span loading
    cl_max = 1.4  # Typical without flaps
    struct_fraction = 0.30  # 30% of MTOW for structure

    # Fixed component weights
    w_payload = PAYLOAD_KG
    w_avionics = 0.15  # kg
    w_propeller = 0.02  # kg

    # Initial weight guess
    w_total = 2.0  # kg (initial guess)

    print("\n--- ITERATIVE WEIGHT CONVERGENCE ---")

    # Iterate to converge weight
    max_iterations = 15
    tolerance = 0.001  # kg

    for iteration in range(max_iterations):
        weight_n = w_total * G

        # Wing geometry from target wing loading
        wing_area = weight_n / wing_loading_target
        wingspan = np.sqrt(aspect_ratio * wing_area)
        mean_chord = wing_area / wingspan

        # Calculate mission energy
        mission = calculate_mission_energy(
            weight_n=weight_n,
            wing_area=wing_area,
            aspect_ratio=aspect_ratio,
            cd0=cd0,
            oswald_e=oswald_e,
            range_km=RANGE_TOTAL_KM,
            cruise_velocity=CRUISE_SPEED_MS,
            loiter_time_min=LOITER_TIME_MIN,
            loiter_velocity=LOITER_SPEED_MS,
            payload_power_w=PAYLOAD_POWER_W
        )

        # Size battery and motor
        energy_required = mission['energy_battery_wh']
        power_cruise = mission['cruise']['power_w']
        w_battery, total_energy = size_battery(energy_required)
        motor_power, w_motor = size_motor(power_cruise)

        # Calculate new total weight
        w_fixed = w_payload + w_avionics + w_battery + w_motor + w_propeller
        w_total_new = w_fixed / (1 - struct_fraction)
        w_structure = w_total_new - w_fixed

        # Check convergence
        delta = abs(w_total_new - w_total)
        print(f"  Iteration {iteration+1}: W = {w_total_new:.4f} kg (delta = {delta:.5f})")

        if delta < tolerance:
            print(f"  Converged after {iteration+1} iterations")
            break

        w_total = w_total_new

    # Final weight
    w_total = w_total_new
    weight_n = w_total * G

    # Final wing geometry (recalculated for converged weight)
    wing_area = weight_n / wing_loading_target
    wingspan = np.sqrt(aspect_ratio * wing_area)
    mean_chord = wing_area / wingspan

    # Actual stall speed
    v_stall = np.sqrt(2 * weight_n / (RHO_CRUISE * wing_area * cl_max))

    print("\n--- INITIAL WEIGHT ESTIMATION ---")
    print(f"  Payload     : {w_payload:.3f} kg")
    print(f"  Avionics    : {w_avionics:.3f} kg")
    print(f"  Battery     : {w_battery:.3f} kg")
    print(f"  Motor       : {w_motor:.3f} kg")
    print(f"  Propeller   : {w_propeller:.3f} kg")
    print(f"  Structure   : {w_structure:.3f} kg ({struct_fraction*100:.0f}%)")
    print(f"  ---------------------")
    print(f"  TOTAL:        {w_total:.3f} kg")

    weights = {
        'payload': w_payload,
        'avionics': w_avionics,
        'battery': w_battery,
        'motor': w_motor,
        'propeller': w_propeller,
        'structure': w_structure,
        'total': w_total
    }

    print("\n--- DESIGN PARAMETERS ---")
    print(f"  Aspect Ratio: {aspect_ratio}")
    print(f"  Wing Loading: {wing_loading_target} N/m²")
    print(f"  CD0 (parasite): {cd0}")
    print(f"  Oswald Efficiency: {oswald_e}")

    print("\n--- WING GEOMETRY ---")
    print(f"  Wing Area:   {wing_area:.4f} m² ({wing_area * 10.764:.2f} ft²)")
    print(f"  Wingspan:    {wingspan:.3f} m ({wingspan * 3.281:.2f} ft)")
    print(f"  Mean Chord:  {mean_chord:.4f} m ({mean_chord * 100:.1f} cm)")

    # Aerodynamic analysis at cruise
    cl_cruise = calculate_cruise_lift_coefficient(weight_n, wing_area, CRUISE_SPEED_MS)
    cd_cruise, cd0_val, cd_i = estimate_drag_coefficient(cl_cruise, aspect_ratio, oswald_e, cd0)
    ld_cruise = calculate_lift_to_drag(cl_cruise, cd_cruise)
    ld_max, cl_at_max_ld = calculate_max_ld(aspect_ratio, oswald_e, cd0)

    # Reynolds number at cruise
    nu = 1.5e-5  # kinematic viscosity of air
    re_chord = CRUISE_SPEED_MS * mean_chord / nu

    print("\n--- CRUISE AERODYNAMICS ---")
    print(f"  CL (cruise):   {cl_cruise:.4f}")
    print(f"  CD (cruise):   {cd_cruise:.5f}")
    print(f"    - CD0:       {cd0_val:.5f}")
    print(f"    - CD_induced:{cd_i:.5f}")
    print(f"  L/D (cruise):  {ld_cruise:.2f}")
    print(f"  L/D (max):     {ld_max:.2f} at CL = {cl_at_max_ld:.3f}")
    print(f"  Reynolds #:    {re_chord:.0f} (based on mean chord)")

    print("\n--- MISSION ENERGY BREAKDOWN ---")
    print(f"  Climb:   {mission['climb']['time_min']:.1f} min, "
          f"{mission['climb']['power_w']:.0f} W, {mission['climb']['energy_wh']:.1f} Wh")
    print(f"  Cruise:  {mission['cruise']['time_min']:.1f} min, "
          f"{mission['cruise']['power_w']:.0f} W, {mission['cruise']['energy_wh']:.1f} Wh")
    print(f"    CL={mission['cruise']['cl']:.3f}, CD={mission['cruise']['cd']:.4f}, L/D={mission['cruise']['ld']:.1f}")
    print(f"  Loiter:  {mission['loiter']['time_min']:.1f} min, "
          f"{mission['loiter']['power_w']:.0f} W, {mission['loiter']['energy_wh']:.1f} Wh")
    print(f"    CL={mission['loiter']['cl']:.3f}, CD={mission['loiter']['cd']:.4f}, L/D={mission['loiter']['ld']:.1f}")
    print(f"  Payload: {mission['payload']['power_w']:.0f} W, {mission['payload']['energy_wh']:.1f} Wh")
    print(f"  -----------------------------------------")
    print(f"  Total Flight Time: {mission['total_flight_time_min']:.1f} min")
    print(f"  Shaft Energy:      {mission['energy_shaft_wh']:.1f} Wh")
    print(f"  Battery Energy:    {mission['energy_battery_wh']:.1f} Wh (w/ 70% efficiency)")

    print("\n--- PROPULSION SIZING ---")
    print(f"  Cruise Power:     {power_cruise:.1f} W")
    print(f"  Battery Required: {total_energy:.1f} Wh (with 20% reserve)")
    print(f"  Battery Mass:     {w_battery:.3f} kg ({w_battery*1000:.0f} g)")
    print(f"  Motor Power:      {motor_power:.0f} W")
    print(f"  Motor Mass:       {w_motor:.3f} kg ({w_motor*1000:.0f} g)")

    print("\n--- PERFORMANCE CHECK ---")
    print(f"  Stall Speed:  {v_stall:.1f} m/s ({v_stall/0.5144:.1f} knots)")
    print(f"  Cruise/Stall: {CRUISE_SPEED_MS/v_stall:.2f} (should be > 1.3)")

    # Create matching chart
    print("\n--- GENERATING MATCHING CHART ---")
    matching_data = create_matching_chart(w_total, aspect_ratio, cd0, oswald_e)

    # Find design point power loading
    design_pw = power_cruise / weight_n
    design_point = {
        'ws': wing_loading_target,
        'pw': design_pw,
        'ld': ld_cruise
    }

    plot_matching_chart(matching_data, design_point)

    # Summary
    print("\n" + "=" * 70)
    print("SIZING SUMMARY")
    print("=" * 70)
    print(f"""
    AIRCRAFT CONFIGURATION:
    -----------------------
    Total Weight:     {w_total:.2f} kg ({w_total*2.205:.2f} lb)
    Wing Area:        {wing_area:.3f} m² ({wing_area*10.764:.1f} ft²)
    Wingspan:         {wingspan:.2f} m ({wingspan*3.281:.1f} ft)
    Aspect Ratio:     {aspect_ratio}
    Wing Loading:     {wing_loading_target:.0f} N/m² ({wing_loading_target*0.0209:.2f} lb/ft²)

    PERFORMANCE:
    ------------
    Cruise Speed:     {CRUISE_SPEED_MS:.1f} m/s ({CRUISE_SPEED_KNOTS} knots)
    Stall Speed:      {v_stall:.1f} m/s ({v_stall/0.5144:.0f} knots)
    L/D at Cruise:    {ld_cruise:.1f}
    L/D Maximum:      {ld_max:.1f}
    Range:            {RANGE_TOTAL_KM} km (round trip)
    Loiter:           {LOITER_TIME_MIN} min
    Flight Time:      {mission['total_flight_time_min']:.0f} min

    PROPULSION:
    -----------
    Cruise Power:     {power_cruise:.0f} W
    Motor Rating:     {motor_power:.0f} W
    Battery:          {total_energy:.0f} Wh ({total_energy/14.8:.0f} mAh @ 4S)

    REYNOLDS NUMBER:  {re_chord:.0f} (at cruise)
    """)

    return {
        'weights': {
            'total': w_total,
            'payload': weights['payload'],
            'battery': w_battery,
            'structure': w_structure
        },
        'geometry': {
            'wing_area': wing_area,
            'wingspan': wingspan,
            'chord': mean_chord,
            'aspect_ratio': aspect_ratio
        },
        'aero': {
            'cl_cruise': cl_cruise,
            'cd_cruise': cd_cruise,
            'ld_cruise': ld_cruise,
            'ld_max': ld_max,
            'reynolds': re_chord
        },
        'propulsion': {
            'power_cruise': power_cruise,
            'motor_power': motor_power,
            'battery_wh': total_energy,
            'flight_time_min': mission['total_flight_time_min']
        }
    }


if __name__ == "__main__":
    results = run_sizing()
