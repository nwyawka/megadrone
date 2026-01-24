# MegaDrone Development Plan
## Phased Approach: Small Trainer to Aerosonde-Class ISR Platform

**Document Version:** 1.0  
**Date:** January 8, 2026  
**Project Owner:** Matthew O'Neil  
**Status:** Planning Phase

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Phase 1: Starter Drone (30-60 min endurance)](#phase-1-starter-drone)
3. [Phase 2: Full-Size ISR Platform (Aerosonde-class)](#phase-2-full-size-isr-platform)
4. [Aerosonde UAV Capabilities Reference](#aerosonde-uav-capabilities-reference)
5. [JPA Privateer Mission Requirements](#jpa-privateer-mission-requirements)
6. [Aircraft Design Process](#aircraft-design-process)
7. [OpenVSP Workflow](#openvsp-workflow)
8. [Airfoil Selection](#airfoil-selection)
9. [Ardupilot Integration](#ardupilot-integration)
10. [TitanPlanner Ground Station](#titanplanner-ground-station)
11. [ISR Platform Considerations](#isr-platform-considerations)
12. [Regulatory Compliance](#regulatory-compliance)
13. [Development Roadmap](#development-roadmap)

---

## Executive Summary

This document outlines a phased approach to developing unmanned aerial vehicles (UAVs) for intelligence, surveillance, and reconnaissance (ISR) missions. The program begins with a small trainer aircraft to develop skills and experience, progressing to an Aerosonde-class platform suitable for the Privateer maritime counter-cartel operations described in the JPA business plan.

### Program Goals

**Phase 1 Objectives:**
- Build hands-on experience with fixed-wing UAV design and operation
- Validate design tools and processes (OpenVSP, Ardupilot, etc.)
- Develop pilot skills and operational procedures
- Stay within Part 107 regulatory limits (55 lbs max)
- Achieve 30-60 minute endurance for local operations
- Budget: $5,000-$10,000

**Phase 2 Objectives:**
- Scale to Aerosonde-class capability (29-36 lb takeoff weight)
- 8-12 hour endurance for maritime ISR missions
- Gimbaled EO/IR camera payload
- Integration with TitanPlanner ground control station
- Support JPA Privateer ISR contract requirements
- Budget: $50,000-$100,000 (custom design) or purchase commercial ($100K-$200K)

### Key Design Decisions

1. **Fixed-Wing Configuration:** Better endurance and range than multirotor
2. **Electric Propulsion:** Quieter, simpler, sufficient for Phase 1
3. **Ardupilot Autopilot:** Open-source, proven, extensive community support
4. **TitanPlanner GCS:** ArduPilot-compatible, mission planning capabilities
5. **Pusher Propeller:** Better camera field-of-view, safer for hand launch/recovery
6. **Conventional Tail:** Proven stability, easier to design than V-tail or flying wing

---

## Phase 1: Starter Drone

### Design Requirements

**Performance:**
- **Endurance:** 30-60 minutes
- **Range:** 5-10 km (line-of-sight, Part 107 compliant)
- **Cruise Speed:** 15-25 m/s (30-50 mph)
- **Stall Speed:** <10 m/s (20 mph) for safe hand launch/landing
- **Wind Tolerance:** 15-20 mph winds
- **Ceiling:** 3,000 ft AGL (Part 107 limit: 400 ft AGL)

**Physical:**
- **Wingspan:** 2.0-2.5 meters (6.5-8 ft)
- **Length:** 1.2-1.5 meters (4-5 ft)
- **Takeoff Weight:** <25 lbs (11 kg) - Part 107 category 1
- **Empty Weight:** 6-8 lbs (2.7-3.6 kg)
- **Wing Loading:** 30-50 g/dm² (6-10 oz/ft²)

**Propulsion:**
- **Motor:** Brushless outrunner, 1000-1500W
- **Battery:** 4S or 6S LiPo, 5000-10000 mAh
- **Propeller:** 11-14" diameter, 2-blade folding (pusher)
- **Power-to-Weight:** 100-150 W/lb

**Payload:**
- **Camera:** GoPro or similar action camera (gimbaled)
- **FPV System:** 5.8 GHz analog or digital HD
- **Telemetry:** 433 MHz or 900 MHz long-range
- **Total Payload:** 1-2 lbs (0.5-1 kg)

**Materials:**
- **Wing:** EPP foam or balsa/plywood built-up
- **Fuselage:** EPP foam or fiberglass composite
- **Construction:** Hand-laid composite or foam core with carbon spar

### Preliminary Specifications (Phase 1)

| Parameter | Target Value | Notes |
|-----------|--------------|-------|
| **Wingspan** | 2.2 m (7.2 ft) | High aspect ratio for efficiency |
| **Wing Area** | 0.55 m² (5.9 ft²) | ~4:1 aspect ratio |
| **Length** | 1.3 m (4.3 ft) | |
| **MTOW** | 10 kg (22 lbs) | Part 107 Category 1 |
| **Empty Weight** | 7 kg (15.4 lbs) | |
| **Battery** | 3 kg (6.6 lbs) | 6S 10000 mAh |
| **Cruise Speed** | 18 m/s (40 mph) | |
| **Stall Speed** | 9 m/s (20 mph) | Hand launchable |
| **L/D** | 12-15 | Good efficiency |
| **Endurance** | 45-60 min | Depends on wind/speed |
| **Range** | 40-60 km | Theoretical, Part 107 limits to VLOS |

### Configuration Selection

**Rationale for Choices:**

1. **High Wing:** 
   - Stability in flight
   - Easy camera mounting underneath
   - Ground clearance for belly landing

2. **Pusher Propeller:**
   - Unobstructed camera view
   - Safer for hand launch/recovery
   - Quieter operation

3. **Conventional Tail (Horizontal + Vertical):**
   - Easier to design than V-tail
   - Better control authority
   - Proven stability

4. **Fixed Tricycle Landing Gear:**
   - Optional (hand launch/belly land alternative)
   - If used: lightweight composite gear

5. **Electric Motor:**
   - Quiet operation
   - Simple, reliable
   - No fuel handling
   - Sufficient for 30-60 min endurance

### Airfoil Selection (Phase 1)

**Recommended Airfoil:** **Selig S1223** or **Eppler E423**

**Why S1223:**
- High lift coefficient (Cl_max ~ 2.2)
- Low Reynolds number performance (Re = 200,000-500,000)
- Gentle stall characteristics
- Proven in model aircraft

**Why E423:**
- Higher L/D ratio (~40 at Re=200,000)
- Lower drag for longer endurance
- Good low-speed handling
- Stable across speed range

**Design Trade:**
- **S1223:** Better slow flight, easier hand launch/landing
- **E423:** Better cruise efficiency, longer endurance

**Recommendation:** Start with **E423** for efficiency, test for stall characteristics

### Mass Budget (Phase 1)

| Component | Weight (lbs) | Weight (kg) | Notes |
|-----------|--------------|-------------|-------|
| **Airframe** | | | |
| Wings (foam/composite) | 2.5 | 1.1 | Foam core + carbon spar |
| Fuselage | 1.5 | 0.7 | EPP foam or fiberglass |
| Tail surfaces | 0.5 | 0.2 | Foam |
| Landing gear (optional) | 0.5 | 0.2 | Composite, removable |
| **Subtotal Airframe** | **5.0** | **2.3** | |
| **Propulsion** | | | |
| Motor | 0.5 | 0.2 | 1200W brushless |
| ESC | 0.2 | 0.1 | 60A |
| Propeller | 0.2 | 0.1 | 13" folding |
| Battery | 6.6 | 3.0 | 6S 10000 mAh LiPo |
| **Subtotal Propulsion** | **7.5** | **3.4** | |
| **Avionics** | | | |
| Pixhawk autopilot | 0.3 | 0.15 | Pixhawk 4 or Cube |
| GPS module | 0.2 | 0.1 | uBlox M8/M9 |
| Telemetry radio | 0.2 | 0.1 | 433 MHz or 900 MHz |
| RC receiver | 0.1 | 0.05 | FrSky or similar |
| Airspeed sensor | 0.1 | 0.05 | Pitot tube |
| Power module | 0.1 | 0.05 | Current/voltage sensor |
| **Subtotal Avionics** | **1.0** | **0.5** | |
| **Payload** | | | |
| Camera (GoPro) | 0.5 | 0.2 | Action camera |
| Gimbal | 0.5 | 0.2 | 2-axis brushless |
| FPV transmitter | 0.2 | 0.1 | 5.8 GHz |
| **Subtotal Payload** | **1.2** | **0.5** | |
| **Wiring, fasteners, misc** | 1.0 | 0.5 | 10% margin |
| **TOTAL EMPTY WEIGHT** | **15.7** | **7.2** | |
| **TOTAL TAKEOFF WEIGHT** | **22.3** | **10.2** | With battery |

**Wing Loading:** 22.3 lbs / 5.9 ft² = **3.8 lbs/ft²** (moderate, good handling)

---

## Phase 2: Full-Size ISR Platform (Aerosonde-Class)

### Aerosonde UAV Capabilities Reference

Based on research of the AAI Aerosonde (now Textron Systems), here are the key specifications:

#### Aerosonde Mk 4.7G (Military Variant)

**Physical:**
- **Wingspan:** 3.8-4.4 m (12-14.5 ft) depending on variant
- **Length:** ~1.8 m (6 ft)
- **Weight:** 32-36 kg (71-79 lbs) takeoff weight
- **Empty Weight:** ~18 kg (40 lbs)

**Performance:**
- **Endurance:** 10-16 hours (depending on payload/conditions)
- **Cruise Speed:** 40-70 km/h (25-43 mph)
- **Service Ceiling:** 4,000 m (13,000 ft)
- **Range:** 60-100 nautical miles (operational radius)
- **Wind Tolerance:** Operations in moderate weather

**Propulsion:**
- **Engine:** 3-4 HP gasoline engine (Enya R120 derivative or similar)
- **Fuel:** Gasoline (~1.5 gallons for Atlantic crossing mission)
- **Propeller:** 2-blade fixed pitch

**Payload:**
- **Capacity:** 2-5 kg (4-11 lbs) depending on variant
- **Sensors:** EO/IR camera, laser pointer, optional SAR radar
- **Datalink:** Real-time video and telemetry

**Launch/Recovery:**
- **Launch:** Catapult or pneumatic launcher
- **Recovery:** Skyhook (vertical recovery on cable) or parachute + net

**Key Achievements:**
- First UAV to cross Atlantic Ocean (1998, 26 hours 45 minutes)
- Extensive hurricane penetration missions
- Deployed by SOCOM, USMC, USAF for ISR

#### Aerosonde MQ-19 (US Military Designation)

**Operational Use:**
- U.S. Special Operations Command (SOCOM)
- Naval Air Systems Command (NAVAIR)
- Service contract model (fee-for-sensor-hours)

**System Composition:**
- 4 air vehicles
- 2 ground control stations (GCS)
- Remote video terminals (tablet-based)
- Transportable in tents or vehicle-mounted

**Cost:**
- **System Cost:** $100K-$200K (complete system)
- **Operating Cost:** $450/hour (vs $750/hour commercial alternatives)
- **Advantage:** 40% cost savings over commercial ISR

### Phase 2 Design Requirements (ISR Platform)

**Performance:**
- **Endurance:** 8-12 hours (minimum for maritime patrol)
- **Range:** 100-150 km operational radius
- **Cruise Speed:** 60-80 km/h (35-50 mph) for fuel efficiency
- **Dash Speed:** 100+ km/h (60+ mph) for repositioning
- **Stall Speed:** <50 km/h (30 mph) for safe recovery
- **Wind Tolerance:** 20-30 mph sustained winds
- **Ceiling:** 3,000-4,500 m (10,000-15,000 ft)
- **Climb Rate:** 3-5 m/s (600-1000 fpm)

**Physical:**
- **Wingspan:** 3.5-4.5 m (11.5-15 ft)
- **Length:** 1.5-2.0 m (5-6.5 ft)
- **Takeoff Weight:** 40-50 lbs (18-23 kg) - Stay under Part 107 55 lb limit
- **Empty Weight:** 25-30 lbs (11-14 kg)
- **Wing Loading:** 40-60 g/dm² (8-12 oz/ft²)

**Propulsion:**
- **Option 1 (Gasoline):** 2-4 HP 2-stroke engine, 0.5-1 gal fuel
- **Option 2 (Electric):** High-capacity LiPo, solar panels (experimental)
- **Propeller:** 16-20" diameter, 2-blade or 3-blade
- **Power-to-Weight:** 50-80 W/lb for long endurance

**Payload:**
- **Primary Sensor:** Gimbaled EO/IR camera (FLIR or similar)
- **Optional Sensors:** AIS receiver, SAR radar, laser designator
- **Datalink:** Long-range digital video (10-50 km)
- **Total Payload:** 5-10 lbs (2-5 kg)

**Launch/Recovery:**
- **Launch:** Catapult, bungee, or pneumatic launcher
- **Recovery:** Parachute + net, or belly landing on prepared surface
- **No Runway:** Designed for field deployment

### JPA Privateer Mission Requirements

From the Anti-Cartel Privateer Business Plan, here are the ISR mission requirements:

#### Phase 1: Intelligence & Surveillance (ISR Contractor)

**Mission Profile:**
- Long-endurance maritime patrol (8-12 hours per mission)
- Coverage of 500-1000 square nautical miles
- 3-5 missions per week
- 150-250 operational hours per month
- Support for 10-20 federal investigations simultaneously

**Operational Areas:**
1. **Gulf of Mexico** (Primary)
   - Texas coast approaches
   - Cartel smuggling routes from Mexico
   - 60-70% of Caribbean drug trafficking

2. **Southern California Coast**
   - Tijuana-San Diego corridor
   - Channel Islands area

3. **Caribbean Approaches**
   - Florida Keys
   - Puerto Rico
   - Transshipment routes

**Required Capabilities:**
- **Sensors:**
  - EO (electro-optical) camera for vessel identification
  - IR (infrared) camera for night operations
  - AIS receiver for vessel tracking
  - Optional: SAR radar for all-weather detection

- **Communications:**
  - Real-time video downlink to ground station
  - Encrypted telemetry (federal agency coordination)
  - Beyond visual line of sight (BVLOS) datalink
  - Integration with federal fusion centers (JIATF-S, CBP)

- **Navigation:**
  - GPS-based navigation
  - Automatic target tracking
  - Pre-programmed patrol patterns (racetrack, orbit)
  - Waypoint navigation

- **Endurance:**
  - Minimum 8 hours on station
  - 12+ hours total flight time (with transit)

**Operating Cost Target:**
- **Goal:** <$500/hour (compete with commercial alternatives)
- **Comparison:** Commercial ISR at $750/hour
- **Advantage:** 40% cost savings critical for contract competitiveness

#### Intelligence Reporting Requirements

**Real-Time:**
- Vessel position, course, speed
- Imagery of contacts
- Suspicious activity alerts

**Post-Mission:**
- Intelligence reports (SALUTE format)
- Pattern-of-life analysis
- Target development packages
- Evidence-quality imagery for prosecution

**Classification:**
- Unclassified to Secret (requires security clearances for operators)

#### Federal Agency Coordination

**Primary Customers:**
1. **U.S. Customs and Border Protection (CBP)**
   - Maritime ISR contracts
   - Daily intelligence reports

2. **Drug Enforcement Administration (DEA)**
   - Case development support
   - Intelligence fusion

3. **U.S. Coast Guard (USCG)**
   - Joint patrols
   - Operational deconfliction

4. **JIATF-South (Joint Interagency Task Force South)**
   - Intelligence sharing
   - Targeting coordination

**Contract Value:**
- **Year 1:** $400K-$800K (initial contracts)
- **Year 2:** $800K-$1.5M (expanded contracts)
- **Year 3:** $1.2M-$2M (mature contract base)

**Success Metrics:**
- Operational availability >85%
- Mission success rate >90%
- Cost per flight hour <$500
- Real-time reporting latency <5 minutes

---

## Aircraft Design Process

### Conceptual Design Phase

#### 1. Mission Requirements Analysis

**Key Questions:**
- What is the primary mission? (ISR patrol, endurance, payload)
- What are the performance requirements? (speed, endurance, range)
- What are the environmental conditions? (wind, weather, maritime)
- What are the regulatory constraints? (Part 107, weight limits)
- What is the budget? (cost vs. capability trade-off)

**Output:** Design Requirements Specification (DRS)

#### 2. Configuration Selection

**Wing Placement:**
- **High Wing:** Stability, camera clearance, ground effect advantage
- **Mid Wing:** Balanced handling, better aerodynamics
- **Low Wing:** Speed, less drag, harder to hand launch

**Tail Configuration:**
- **Conventional (H-tail):** Proven, simple, good control
- **T-tail:** Better elevator authority, complex structure
- **V-tail:** Reduced drag/weight, complex control mixing
- **Tailless:** Low drag, poor stability, hard to design

**Propulsion Placement:**
- **Tractor (Front):** Traditional, good cooling, prop in clean air
- **Pusher (Rear):** Clear camera view, safer, less efficient
- **Twin:** Redundancy, complexity, weight penalty

**Landing Gear:**
- **Tricycle:** Stable, conventional, adds weight
- **Taildragger:** Lighter, harder to control on ground
- **None (Belly/Skid):** Lightest, limits reusability, field deployment
- **Catapult Launch + Parachute Recovery:** No gear needed, proven for UAVs

**Recommendation for ISR Platform:**
- **High wing** (stability, camera clearance)
- **Conventional tail** (simplicity, reliability)
- **Pusher propeller** (camera field-of-view)
- **Catapult launch, parachute/net recovery** (no landing gear weight)

#### 3. Initial Sizing

**Methodology:** Historical regression or first-principles

**Historical Regression:**
- Find similar aircraft (Aerosonde, RQ-7, ScanEagle)
- Scale based on payload, endurance requirements
- Adjust for differences in technology, materials

**First-Principles:**
- Estimate required lift (= weight)
- Select wing loading for mission (low for endurance)
- Calculate wing area: S = W / (0.5 * ρ * V² * CL)
- Estimate aspect ratio (AR = 8-12 for endurance)
- Calculate wingspan: b = √(AR * S)
- Estimate power required: P = D * V = (W / L/D) * V
- Select power-to-weight ratio
- Size battery/fuel based on endurance requirement

**Output:** Initial geometry (wingspan, area, weight, power)

#### 4. Mass Budget

**Categories:**
- **Structure:** Wings, fuselage, tail, landing gear (if any)
- **Propulsion:** Engine/motor, fuel/battery, propeller, ESC
- **Systems:** Avionics, autopilot, sensors, datalink
- **Payload:** Camera, gimbal, optional sensors
- **Margin:** 10-15% contingency for unknowns

**Historical Mass Fractions (typical UAV):**
- Structure: 35-45% of empty weight
- Propulsion: 20-30% of empty weight
- Systems: 15-25% of empty weight
- Payload: 10-20% of takeoff weight
- Fuel/Battery: 20-40% of takeoff weight

**Output:** Detailed mass breakdown, weight and balance

#### 5. Aerodynamic Preliminary Design

**Airfoil Selection:** (See detailed section below)
- Low Reynolds number (Re = 200,000 - 1,000,000)
- High L/D for endurance
- Gentle stall for safety
- Common choices: Eppler E423, Selig S1223, NACA 4412

**Lift and Drag Estimation:**
- Cruise CL (lift coefficient) = W / (0.5 * ρ * V² * S)
- Induced drag: CDi = CL² / (π * AR * e)
- Parasitic drag: CD0 from component buildup
- Total drag: CD = CD0 + CDi
- L/D ratio = CL / CD

**Stability and Control:**
- Longitudinal stability: CG location, tail volume coefficient
- Directional stability: Vertical tail sizing
- Control surface sizing: Elevator, rudder, ailerons

**Output:** Aerodynamic coefficients, L/D estimate, stability derivatives

#### 6. Propulsion Sizing

**Power Required:**
- P_required = (D * V) / η_prop
- D = 0.5 * ρ * V² * S * CD
- η_prop = propeller efficiency (~0.7-0.85)

**Motor Selection (Electric):**
- Power = Voltage * Current
- Select motor Kv (RPM/V) for desired propeller size
- Match ESC to motor current requirements

**Engine Selection (Gasoline):**
- Power-to-weight: 2-4 HP for 40-50 lb aircraft
- Fuel consumption: ~0.3-0.5 lb/hp/hr
- Fuel weight for 10-hour mission: 6-10 lbs

**Battery Sizing (Electric):**
- Energy required = Power * Time / Efficiency
- Battery capacity (Wh) = Energy / Discharge rate
- LiPo energy density: ~150-200 Wh/kg
- Weight = Capacity / Energy density

**Output:** Motor/engine specification, battery/fuel sizing

#### 7. Performance Analysis

**Key Metrics:**
- **Stall Speed:** V_stall = √(2 * W / (ρ * S * CL_max))
- **Cruise Speed:** Optimize for L/D_max for endurance
- **Dash Speed:** Maximum speed at full throttle
- **Climb Rate:** Excess power / Weight
- **Endurance:** Fuel/Battery capacity / Power consumption
- **Range:** Endurance * Cruise speed

**Endurance Optimization:**
- Maximize L/D ratio
- Fly at speed for (L/D)_max (typically ~0.76 * V_best_range)
- Minimize parasitic drag (smooth surfaces, sealing)
- Optimize propeller for cruise (not climb)

**Output:** Performance envelope (V-n diagram, endurance vs. speed)

---

### Detailed Design Phase

#### 8. Structural Design

**Load Cases:**
- **Flight Loads:** Maneuver (n_max = 4-6 g), gust loads
- **Landing Loads:** Hard landing, catapult launch
- **Ground Handling:** Lifting, transport

**Materials Selection:**
- **Foam:** EPP, EPO (low cost, easy to work, moderate strength)
- **Balsa/Plywood:** Traditional, good strength-to-weight
- **Composite:** Carbon fiber, fiberglass (high strength, expensive)
- **3D Printing:** PLA, PETG, nylon (complex shapes, moderate strength)

**Wing Structure:**
- **Spar:** Main load-bearing member (carbon tube or I-beam)
- **Ribs:** Shape and distribute loads (balsa, foam, 3D printed)
- **Skin:** Aerodynamic surface (foam, balsa, composite)
- **Covering:** Sealing and finish (film, fabric, fiberglass)

**Fuselage Structure:**
- **Monocoque:** Skin carries all loads (foam, composite)
- **Semi-monocoque:** Skin + stringers/bulkheads (fiberglass)
- **Truss:** Separate structure + non-structural skin (balsa frame)

**Output:** CAD model (SolidWorks, Fusion 360), structural drawings

#### 9. Control System Design

**Flight Controls:**
- **Elevator:** Pitch control (tail or canard)
- **Rudder:** Yaw control (vertical stabilizer)
- **Ailerons:** Roll control (outboard wings) OR
- **Flaperons:** Combined flap/aileron function
- **Servos:** Torque sizing based on surface area and airspeed

**Control Surface Sizing:**
- Elevator area: ~20-25% of horizontal stabilizer
- Rudder area: ~25-30% of vertical stabilizer
- Aileron area: ~10-15% of wing area (outboard)
- Deflection: ±20-30° typical

**Autopilot Integration:**
- **Sensors:** GPS, IMU, barometer, airspeed, magnetometer
- **Outputs:** PWM signals to servos and ESC
- **Modes:** Manual, stabilize, auto (waypoint navigation)
- **Failsafes:** Return-to-launch (RTL), geofence, low battery

**Output:** Control linkage design, servo selection, autopilot configuration

#### 10. Systems Integration

**Electrical System:**
- **Power Distribution:** Battery → ESC → Motor
- **Avionics Power:** BEC (battery eliminator circuit) or separate battery
- **Wiring:** Gauge selection, connector types, routing

**Avionics Layout:**
- **Autopilot:** Central location, vibration isolation
- **GPS:** Clear sky view (top of fuselage or wing)
- **Airspeed Sensor:** Pitot tube in clean airflow
- **Telemetry Antenna:** Unobstructed view (vertical orientation)

**Payload Integration:**
- **Camera Gimbal:** Vibration isolation, mounting
- **Gimbal Control:** Autopilot or separate controller
- **Video Downlink:** Transmitter, antenna placement

**Output:** Systems diagram, wiring harness, integration checklist

---

### Manufacturing and Testing Phase

#### 11. Manufacturing Planning

**Techniques:**
- **Hot Wire Cutting:** Foam wings, fuselage shells
- **CNC Machining:** Ribs, bulkheads, molds
- **Hand Lay-up:** Fiberglass or carbon fiber parts
- **3D Printing:** Complex fittings, brackets, cowlings

**Tooling:**
- Wing mold or build jig
- Fuselage mold or plug
- Assembly fixtures

**Output:** Manufacturing drawings, tooling plan, build sequence

#### 12. Prototype Fabrication

**Build Sequence:**
1. Wing structure (spar, ribs, skin)
2. Wing covering and finishing
3. Fuselage structure
4. Systems installation (avionics, servos)
5. Empennage (tail) construction
6. Final assembly and rigging
7. Surface prep and painting

**Quality Control:**
- Dimensional checks (wingspan, length, incidence angles)
- Mass properties (weight, CG location)
- Control surface throws and neutral positions
- Systems testing (electrical, servo, autopilot)

**Output:** Completed airframe, ready for ground testing

#### 13. Ground Testing

**Pre-Flight Checks:**
- Control surface direction and travel
- Motor/propeller thrust test
- Autopilot sensor calibration (accelerometer, compass, airspeed)
- Telemetry range test (ground range check)
- Failsafe testing (RC loss, low battery, geofence)

**Taxi Tests:**
- Ground handling (if applicable)
- Acceleration and braking
- Steering control

**Catapult Launch Test:**
- Incremental testing (low power → full power)
- Capture on video for review
- Check launch angle, acceleration

**Output:** Ground test report, adjustments/fixes identified

#### 14. Flight Testing

**First Flight:**
- **Conditions:** Calm winds (<5 mph), clear weather
- **Pilot:** Experienced RC pilot (manual control)
- **Checklist:** Pre-flight inspection, control checks, telemetry link
- **Objectives:** Basic handling, trim adjustments, landing

**Envelope Expansion:**
- **Flight 2-5:** Explore speed range, climb/descent rates, turning
- **Flight 6-10:** Test autopilot modes (stabilize, loiter, auto)
- **Flight 11+:** Endurance testing, payload testing, mission simulation

**Data Collection:**
- Onboard logs (autopilot telemetry)
- Groundstation logs
- Video (onboard FPV, external observer)
- Pilot notes and observations

**Iterative Improvement:**
- Trim adjustments (CG, control surface rigging)
- Autopilot tuning (PID gains for pitch, roll, yaw)
- Performance validation (endurance, speed, climb)

**Output:** Flight test report, validated performance data, certified aircraft

---

## OpenVSP Workflow

### Introduction to OpenVSP

**OpenVSP (Open Vehicle Sketch Pad)** is a free, open-source parametric aircraft geometry tool developed by NASA. It's widely used for conceptual aircraft design, allowing rapid modeling and analysis of aerodynamic shapes.

**Capabilities:**
- Parametric geometry creation (wing, fuselage, propeller, etc.)
- Mass properties calculation
- Wetted area and drag buildup
- Export to CFD and structural analysis tools
- Visualization and rendering

**Download:** [https://openvsp.org](https://openvsp.org)

### Workflow for Drone Design

#### Step 1: Define Design Parameters

Before opening OpenVSP, gather your requirements:
- Wingspan, length, wing area
- Airfoil selection
- Fuselage diameter/cross-section
- Tail configuration and sizes
- Propeller diameter and location

**Example (Phase 1 Drone):**
- Wingspan: 2.2 m
- Wing area: 0.55 m²
- Airfoil: Eppler E423
- Fuselage length: 1.3 m
- Fuselage max diameter: 0.15 m
- H-tail span: 0.7 m

#### Step 2: Create Wing Geometry

1. **Add Wing Component:** 
   - Component → Add → Wing
   
2. **Set Wing Planform:**
   - **Span:** 2.2 m
   - **Root Chord:** 0.28 m (calculated from area and taper)
   - **Tip Chord:** 0.22 m (taper ratio ~0.8)
   - **Sweep:** 0° (straight wing for simplicity)
   - **Dihedral:** 2-3° (slight upward angle for stability)
   - **Twist:** -2° at tip (washout for stall characteristics)

3. **Set Airfoil:**
   - Select airfoil type: "Airfoil File"
   - Import E423 airfoil coordinates (download from UIUC database)
   - Apply to all sections or vary from root to tip

4. **Positioning:**
   - **Z-position:** Adjust for high-wing configuration
   - **Incidence Angle:** 0-2° (angle of attack at cruise)

#### Step 3: Create Fuselage Geometry

1. **Add Fuselage Component:**
   - Component → Add → Fuselage (or Stack)

2. **Define Cross-Sections:**
   - **Nose:** Elliptical or circular (small diameter)
   - **Mid-section:** Circular or rectangular (max diameter 0.15 m)
   - **Tail:** Taper to small diameter for tail boom

3. **Length and Shaping:**
   - Total length: 1.3 m
   - Position cross-sections along X-axis
   - Adjust diameters for smooth aerodynamic shape

4. **Payload Bay:**
   - Widen mid-section slightly for avionics/battery
   - Flat bottom for camera mounting

#### Step 4: Create Tail Surfaces

1. **Horizontal Stabilizer:**
   - Component → Add → Wing (duplicate and modify)
   - **Span:** 0.7 m
   - **Root Chord:** 0.18 m
   - **Airfoil:** Symmetric (NACA 0012 or flat plate)
   - **Position:** Rear of fuselage, aligned with tail boom

2. **Vertical Stabilizer:**
   - Component → Add → Wing (rotate 90°)
   - **Height:** 0.25 m
   - **Root Chord:** 0.20 m
   - **Airfoil:** Symmetric (NACA 0012)
   - **Position:** Top of fuselage, aft

3. **Control Surfaces:**
   - Define elevator and rudder as sub-surfaces
   - Typical: 25% of tail surface area

#### Step 5: Add Propulsion System

1. **Propeller:**
   - Component → Add → Prop (or Disk for simple)
   - **Diameter:** 13 inches (0.33 m)
   - **Position:** Rear of fuselage (pusher)
   - **Rotation:** Define direction (clockwise/counterclockwise)

2. **Motor:**
   - Add simple cylinder or import CAD (optional for visualization)

#### Step 6: Calculate Mass Properties

1. **Set Component Masses:**
   - Wing: 1.1 kg
   - Fuselage: 0.7 kg
   - Tail: 0.2 kg
   - Motor: 0.2 kg
   - Avionics: 0.5 kg
   - Battery: 3.0 kg
   - Payload: 0.5 kg

2. **Calculate CG:**
   - Analysis → Mass Properties
   - OpenVSP calculates total mass and center of gravity
   - **Target:** CG at 25-30% of mean aerodynamic chord (MAC)

3. **Adjust Component Positions:**
   - Move heavy components (battery) to achieve desired CG
   - Iterate until CG is in stable range

#### Step 7: Parasite Drag Buildup

1. **Wetted Area Calculation:**
   - Analysis → Comp Geom → Wetted Area
   - OpenVSP computes surface area of all components

2. **Drag Estimation:**
   - Use wetted area method:
   - CD0 = (Swet / Sref) * Cf
   - Cf = skin friction coefficient (~0.005-0.010 for UAV)
   - Sref = wing reference area

3. **Interference Drag:**
   - Add 10-20% for wing-fuselage, tail-fuselage intersections

#### Step 8: Aerodynamic Analysis (Optional)

1. **VSPAERO (Vortex Lattice Method):**
   - Analysis → VSPAERO
   - Define flight conditions (altitude, speed, angle of attack)
   - Run analysis to get CL, CD, Cm
   - Provides quick estimates for conceptual design

2. **Export for CFD:**
   - File → Export → STL or STEP
   - Import into CFD software (OpenFOAM, ANSYS Fluent, XFLR5)
   - Run higher-fidelity simulations if needed

#### Step 9: Visualization and Export

1. **Rendering:**
   - View → Fit View
   - Adjust lighting and camera angle
   - Screenshot for presentations

2. **Export Geometry:**
   - **For manufacturing:** Export → DXF (2D profiles for CNC/laser)
   - **For CAD:** Export → STEP or IGES (3D solid model)
   - **For 3D printing:** Export → STL

3. **Save Project:**
   - File → Save (.vsp3 file)
   - Keep version control (e.g., Drone_v1.vsp3, Drone_v2.vsp3)

### Typical Iterations

**Iteration 1:** Basic geometry, rough sizing
- Check: Does it look reasonable? Are proportions correct?

**Iteration 2:** Refine based on mass properties
- Adjust: Move components to get CG in correct location

**Iteration 3:** Aerodynamic validation
- Check: L/D ratio, drag estimate, stability
- Adjust: Wing area, tail sizing, airfoil

**Iteration 4:** Final design
- Output: Detailed geometry for manufacturing

---

## Airfoil Selection

### Airfoil Fundamentals

**What is an airfoil?**
- The cross-sectional shape of a wing
- Generates lift by creating pressure difference (Bernoulli + Newton)

**Key Parameters:**
- **Camber:** Curvature of the mean line (affects lift)
- **Thickness:** Maximum thickness as % of chord (affects drag and structure)
- **Reynolds Number (Re):** ρ * V * c / μ (affects boundary layer behavior)

**Performance Metrics:**
- **Lift Coefficient (Cl):** Lift / (0.5 * ρ * V² * area)
- **Drag Coefficient (Cd):** Drag / (0.5 * ρ * V² * area)
- **L/D Ratio:** Cl / Cd (higher is better for efficiency)
- **Stall Angle:** Angle of attack where lift suddenly drops

### Reynolds Number for Drone Design

**Phase 1 Drone:**
- Chord: c = 0.25 m (average)
- Speed: V = 18 m/s (cruise)
- Air density: ρ = 1.225 kg/m³ (sea level)
- Viscosity: μ = 1.81 x 10⁻⁵ kg/(m·s)
- **Re = (1.225 * 18 * 0.25) / (1.81 x 10⁻⁵) ≈ 300,000**

**Phase 2 ISR Drone:**
- Chord: c = 0.35 m
- Speed: V = 22 m/s (cruise)
- **Re ≈ 500,000**

**Category:** Both are in **low Reynolds number regime** (Re < 500,000)

### Low Reynolds Number Airfoils

**Challenges:**
- Laminar boundary layer prone to separation
- Lower L/D than high-Re airfoils
- Sensitive to surface roughness
- Limited selection compared to full-scale aircraft

**Best Airfoils for UAVs:**

#### 1. **Eppler E423**

**Characteristics:**
- **Re range:** 200,000 - 500,000
- **Max Cl:** ~1.5
- **L/D max:** ~40-50 (at Re=200,000)
- **Thickness:** 12% chord
- **Type:** Cambered airfoil with laminar flow emphasis

**Pros:**
- Excellent L/D for endurance
- Gentle stall
- Good performance across speed range
- Well-documented performance data

**Cons:**
- Not as high lift as some alternatives
- Requires smooth surface finish

**Best For:** Long-endurance cruise, efficiency

**Recommendation:** **Primary choice for Phase 2 ISR drone**

---

#### 2. **Selig S1223**

**Characteristics:**
- **Re range:** 60,000 - 300,000
- **Max Cl:** ~2.2 (very high)
- **L/D max:** ~25-35
- **Thickness:** 11.5% chord
- **Type:** High-lift, low-Re specialist

**Pros:**
- Extremely high lift (low stall speed)
- Excellent slow-flight characteristics
- Forgiving handling
- Popular in model aircraft

**Cons:**
- Lower L/D than E423 (higher drag)
- More sensitive to Re changes
- Not as efficient at higher speeds

**Best For:** Slow flight, hand launch/landing, trainer aircraft

**Recommendation:** **Good for Phase 1 trainer**

---

#### 3. **SD7037**

**Characteristics:**
- **Re range:** 100,000 - 500,000
- **Max Cl:** ~1.7
- **L/D max:** ~35-45
- **Thickness:** 9.7% chord
- **Type:** General-purpose low-Re airfoil

**Pros:**
- Balanced performance (lift and drag)
- Good over wide Re range
- Moderate stall
- Widely used in RC and small UAVs

**Cons:**
- Not specialized (not best at anything specific)
- Thinner (less internal volume)

**Best For:** General-purpose UAVs, moderate endurance

**Recommendation:** Alternative to E423 if thinner wing preferred

---

#### 4. **NACA 4412**

**Characteristics:**
- **Re range:** 500,000+ (better at higher Re, but usable lower)
- **Max Cl:** ~1.6
- **L/D max:** ~40
- **Thickness:** 12% chord
- **Type:** Traditional NACA 4-digit series

**Pros:**
- Well-understood performance
- Robust across conditions
- Easy to manufacture (simple coordinates)
- Good structural depth

**Cons:**
- Designed for higher Re (not optimal for small drones)
- Lower L/D than modern low-Re airfoils
- Not as efficient as Eppler or Selig

**Best For:** Simple designs, proven performance, moderate efficiency

**Recommendation:** Fallback choice if Eppler/Selig unavailable

---

### Airfoil Selection Matrix

| Airfoil | Best For | Max Cl | L/D | Re Range | Phase |
|---------|----------|--------|-----|----------|-------|
| **E423** | Efficiency, endurance | 1.5 | 40-50 | 200K-500K | **Phase 2** |
| **S1223** | Slow flight, high lift | 2.2 | 25-35 | 60K-300K | **Phase 1** |
| **SD7037** | General purpose | 1.7 | 35-45 | 100K-500K | Both |
| **NACA 4412** | Simple, proven | 1.6 | 40 | 500K+ | Phase 2 |

### Airfoil Data Sources

**UIUC Airfoil Database:**
- [https://m-selig.ae.illinois.edu/ads.html](https://m-selig.ae.illinois.edu/ads.html)
- Download coordinates, performance data, plots

**XFLR5 Software:**
- Free airfoil analysis tool
- Visualize pressure distributions, polars (Cl vs. alpha)
- Design and test custom airfoils

**JavaFoil:**
- Online airfoil analysis
- Quick performance estimates

### Surface Finish Considerations

**Critical for Low-Re Airfoils:**
- Smooth surfaces maintain laminar flow
- Roughness trips boundary layer → increased drag
- Aim for: Sanded smooth, filled seams, painted/sealed

**Surface Finishes:**
- **Foam (raw):** Acceptable, but not optimal
- **Foam + spackle/filler:** Better, sanded smooth
- **Fiberglass/carbon:** Excellent if finished properly
- **Painted:** Good finish, protective

**Tip:** Test different finishes in flight, measure performance difference

---

## Ardupilot Integration

### Why Ardupilot?

**Ardupilot** is an open-source autopilot system widely used in drones and UAVs. It's a mature platform with extensive community support.

**Key Features:**
- Full autonomous flight (takeoff, waypoint navigation, landing)
- Multiple vehicle types (plane, copter, rover, sub, etc.)
- Advanced sensors (GPS, compass, barometer, airspeed, lidar, etc.)
- Safety features (geofence, failsafes, return-to-launch)
- Ground control station (Mission Planner, QGroundControl, etc.)
- Extensive documentation and community

**Alternatives:**
- **PX4:** Similar open-source autopilot, more focused on research/development
- **Pixhawk:** Hardware platform (runs Ardupilot or PX4 firmware)
- **DJI:** Proprietary, limited customization
- **Custom:** Roll your own (not recommended unless expert)

**Recommendation:** **Ardupilot on Pixhawk hardware**

### Hardware Selection

#### Flight Controller Options

**1. Pixhawk 4 (Recommended for Phase 1)**

**Specs:**
- Processor: STM32F765 (32-bit ARM, 216 MHz)
- Sensors: IMU (accel, gyro), barometer, compass
- Connectivity: GPS, telemetry, RC, servos, I2C, CAN
- Cost: $200-$250

**Pros:**
- Widely supported, proven
- Good balance of features and cost
- Extensive documentation

**Cons:**
- Larger/heavier than some alternatives

---

**2. Cube Orange+ (Recommended for Phase 2)**

**Specs:**
- Processor: STM32H743 (faster, more memory)
- Triple redundant IMUs
- Vibration isolation
- Industrial-grade quality
- Cost: $300-$400

**Pros:**
- High reliability (triple redundancy)
- Better for professional/commercial use
- Vibration damping built-in

**Cons:**
- More expensive
- Overkill for simple trainer

---

**3. Pixhawk Mini / Pix32 v6 (Budget Option)**

**Specs:**
- Smaller form factor
- Reduced features (fewer ports)
- Cost: $80-$150

**Pros:**
- Lightweight
- Affordable
- Sufficient for simple drones

**Cons:**
- Fewer expansion options
- Less redundancy

---

### Sensor Suite

**Required Sensors:**

1. **GPS Module:**
   - uBlox M8N or M9N
   - Compass integrated (magnetometer)
   - Cost: $30-$80

2. **Airspeed Sensor:**
   - Pitot tube (measures dynamic pressure)
   - Critical for fixed-wing autopilot
   - MS4525 or MS5525 sensor
   - Cost: $40-$60

3. **Power Module:**
   - Measures battery voltage and current
   - Enables battery monitoring and failsafe
   - Hall-effect sensor
   - Cost: $15-$30

**Optional Sensors:**

4. **Lidar / Rangefinder:**
   - Measures altitude above ground
   - Useful for landing and terrain following
   - Benewake TFmini, Lightware, etc.
   - Cost: $40-$200

5. **Optical Flow:**
   - Camera-based position hold (without GPS)
   - Indoor flight or GPS-denied environments
   - Cost: $80-$150

6. **ADS-B Receiver:**
   - Detect nearby manned aircraft
   - Collision avoidance
   - Cost: $150-$300

### Telemetry and RC

**Telemetry Radio:**
- **Purpose:** Two-way communication between drone and ground station
- **Frequency:** 433 MHz (long range) or 900 MHz (less crowded)
- **Range:** 5-50 km (depending on power, antenna, terrain)
- **Recommended:** RFD900x or HolyBro telemetry radios
- **Cost:** $80-$200 (pair)

**RC Receiver:**
- **Purpose:** Manual control override, safety pilot
- **Protocol:** FrSky (ACCST/ACCESS), Spektrum, FlySky, etc.
- **Channels:** Minimum 8, recommend 16 for advanced features
- **Recommended:** FrSky X8R or R9 (long range)
- **Cost:** $30-$80

**RC Transmitter:**
- **Purpose:** Pilot control during manual flight, failsafe
- **Recommended:** FrSky Taranis X9D, Radiomaster TX16S
- **Cost:** $200-$300

### Power System

**Battery:**
- **Type:** LiPo (Lithium Polymer) for high power density
- **Voltage:** 4S (14.8V) or 6S (22.2V)
- **Capacity:** 10,000-20,000 mAh for Phase 1
- **C-Rating:** 25C-50C (discharge rate)
- **Cost:** $100-$300 per pack

**ESC (Electronic Speed Controller):**
- **Rating:** Match to motor current (60-100A typical)
- **Protocol:** PWM or DShot (DShot preferred for better control)
- **BEC:** Battery eliminator circuit to power servos
- **Cost:** $50-$150

**Motor:**
- **Type:** Brushless outrunner
- **Size:** 4010-5010 stator dimensions
- **Kv:** 200-400 Kv for large propellers
- **Power:** 1000-2000W
- **Cost:** $80-$200

**Propeller:**
- **Size:** 13-16 inch diameter for Phase 1
- **Pitch:** 6-10 inch (lower pitch for endurance)
- **Type:** 2-blade or 3-blade folding
- **Material:** Carbon fiber or composite
- **Cost:** $20-$80

### Ardupilot Software Setup

#### 1. Firmware Installation

**Tools:**
- Mission Planner (Windows) or QGroundControl (cross-platform)
- USB cable to flight controller

**Steps:**
1. Connect flight controller to computer
2. Open Mission Planner
3. Select COM port
4. Go to: Setup → Install Firmware
5. Select vehicle type: **ArduPlane**
6. Wait for download and flash
7. Flight controller will reboot

#### 2. Frame Configuration

**Frame Type:**
- Fixed-wing (not quadplane, not VTOL for now)
- Conventional control (aileron, elevator, rudder, throttle)

**In Mission Planner:**
1. Config → Basic Params → Frame Type: Normal (plane)
2. Set: SERVO1 = Aileron, SERVO2 = Elevator, SERVO3 = Throttle, SERVO4 = Rudder
3. (Adjust based on actual wiring)

#### 3. Sensor Calibration

**Accelerometer:**
- Config → Accel Calibration
- Follow on-screen prompts (level, nose up, nose down, left, right, upside down)
- Critical for attitude estimation

**Compass:**
- Config → Compass
- Select: Use external compass (GPS module)
- Calibration: Rotate drone in all orientations (figure-8 pattern)
- Critical for heading accuracy

**Radio Calibration:**
- Config → Radio Calibration
- Move all RC sticks and switches through full range
- Verify channel assignments

**Airspeed Sensor (if installed):**
- Config → Optional Hardware → Airspeed
- Enable sensor, set type (MS4525 or MS5525)
- Calibrate: Cover pitot tube, record zero offset

#### 4. Flight Mode Setup

**Recommended Flight Modes:**
1. **Manual:** Full pilot control (no stabilization)
2. **FBWA (Fly-By-Wire A):** Stabilized flight, pilot sets bank angle
3. **FBWB (Fly-By-Wire B):** Stabilized, pilot sets speed and altitude
4. **Cruise:** Autopilot maintains altitude and heading
5. **Auto:** Full autonomous waypoint navigation
6. **RTL (Return to Launch):** Emergency return home
7. **Loiter:** Circle at current location

**Assign to RC switches:**
- Mode switch (3-position): Manual / FBWA / Auto
- Emergency switch: RTL

#### 5. Tuning

**PID Gains:**
- Proportional, Integral, Derivative gains for pitch, roll, yaw control
- Default values usually work for first flight
- Tune after initial flights based on performance

**Autotune:**
- Ardupilot has AUTOTUNE mode
- Fly in AUTOTUNE, toggle switch, autopilot learns optimal gains
- Requires stable flight conditions

**Critical Params:**
- **SERVO_AUTO_TRIM:** Auto-adjust servo neutrals in flight
- **STALL_PREVENTION:** Prevent low-speed stalls
- **ARSPD_FBW_MIN / MAX:** Airspeed limits in fly-by-wire modes

#### 6. Geofence and Failsafes

**Geofence:**
- Set maximum distance from home (e.g., 5 km)
- Set maximum altitude (e.g., 400 ft / 120 m for Part 107)
- Action on breach: RTL or loiter

**Failsafes:**
- **RC Loss:** If no RC signal for X seconds → RTL
- **GCS Loss:** If no telemetry for X seconds → Continue mission or RTL
- **Low Battery:** If voltage drops below threshold → RTL
- **GPS Loss:** Maintain last known position or loiter

**Configuration:**
- Config → Failsafe
- Set timeouts and actions

### Mission Planning with Ardupilot

**Waypoint Missions:**
1. Open Mission Planner → Flight Plan
2. Right-click map → Add Waypoint
3. Set altitude, speed, loiter time for each waypoint
4. Define takeoff and landing sequences
5. Upload mission to drone

**Auto Takeoff:**
- Waypoint 0: Takeoff command
- Set altitude (e.g., 100 ft)
- Throttle max, climb to altitude
- Transition to next waypoint

**Auto Land:**
- Final waypoint: Land command
- Drone descends, flares, touches down
- Disarms automatically

**Survey Grid:**
- Built-in tool for automated survey patterns
- Define area, overlap, altitude
- Generates waypoint grid automatically

### Telemetry and Logging

**Real-Time Telemetry:**
- Flight Data screen in Mission Planner
- View: Altitude, airspeed, battery, GPS, attitude, etc.
- Overlaid on moving map

**Onboard Logging:**
- Ardupilot logs all sensor data to SD card
- Download logs after flight
- Analyze with Mission Planner or https://logs.px4.io

**Review Flight:**
- Replay flight path on map
- Graph any parameter (altitude vs. time, airspeed vs. throttle, etc.)
- Identify issues (vibration, compass errors, tuning problems)

---

## TitanPlanner Ground Station

### What is TitanPlanner?

**TitanPlanner** is a modified version of **Mission Planner**, the most popular ground control station (GCS) for Ardupilot. It's developed by Titan Dynamics and includes UI/UX improvements and custom features.

**Official Repo:** [https://github.com/Titan-Dynamics/TitanPlanner](https://github.com/Titan-Dynamics/TitanPlanner)

**Base Software:** ArduPilot Mission Planner (C# .NET)

### Key Features of TitanPlanner

Based on the GitHub repository review:

**UI/UX Improvements:**
1. **Full Parameter List Overhaul:**
   - Asynchronous loading for faster access
   - No more delay when opening full param list

2. **Removal of Confirmation Dialogs:**
   - Faster parameter writing workflow
   - Less clicking for experienced users

3. **Servo Output Tab:**
   - Easy servo trimming with sliders
   - "Equidistant" feature for endpoint calculation
   - Increments of 10 for precision

4. **Params Tab on Main Screen:**
   - Edit parameters without leaving Flight Data view
   - Tree view collapsed by default

5. **Tuning Tab for All Vehicles:**
   - Plane, Copter, Rover tuning on Flight Data screen
   - No more switching between CONFIG and FLIGHT DATA

6. **3D Map View Enhancements:**
   - Improved visualization
   - Easier mission planning

**Why Use TitanPlanner?**
- Same core functionality as Mission Planner
- Better user experience for frequent users
- Faster workflow for parameter tuning
- All ArduPilot features supported

### Installation

**Platform:** Windows (C# .NET application)

**Steps:**
1. Download latest release from GitHub
2. Extract ZIP file
3. Run TitanPlanner.exe
4. (No installation required, portable application)

**System Requirements:**
- Windows 7/10/11
- .NET Framework 4.8 (usually already installed)
- USB port for flight controller connection
- Serial port or telemetry radio for wireless connection

### Connecting to Drone

**USB Connection:**
1. Connect flight controller to PC via USB
2. In TitanPlanner: Select COM port (top right)
3. Click "Connect"
4. Wait for parameter download

**Telemetry Connection:**
1. Connect telemetry radio to PC via USB
2. Power on drone (telemetry radio on drone powers up)
3. In TitanPlanner: Select COM port of telemetry radio
4. Set baud rate (57600 or 115200 typical)
5. Click "Connect"

**Network Connection (Optional):**
- If drone has WiFi/cellular modem
- Set up UDP or TCP connection
- Enter IP address and port

### Mission Planning Workflow

**Step 1: Set Home Location**
- Flight Plan → Right-click map → Set Home Here
- Or: Automatically set on GPS lock

**Step 2: Create Waypoints**
- Right-click map → Draw Polygon or Add Waypoint
- Set altitude for each waypoint (AGL or MSL)
- Set speed (optional, uses cruise speed if not set)

**Step 3: Define Takeoff**
- Waypoint 0 or 1: Takeoff command
- Set takeoff altitude (e.g., 100 ft / 30 m)

**Step 4: Add Survey Grid (Optional)**
- Auto WP → Survey (Grid)
- Define area by clicking corners
- Set altitude, overlap, camera settings
- Grid auto-generated

**Step 5: Define Landing**
- Final waypoint: Land command
- Or: Do_Land_Start + approach waypoints

**Step 6: Upload Mission**
- Click "Write WPs" (write waypoints to drone)
- Verify on drone's telemetry screen

**Step 7: Pre-Flight Check**
- Actions → Pre-Flight Checklist
- Verify: GPS lock, compass calibrated, mode set, geofence active

**Step 8: Fly Mission**
- Switch to Auto mode (on RC transmitter)
- Drone executes mission automatically
- Monitor on map, ready to take manual control if needed

### Real-Time Monitoring

**Flight Data Screen:**
- **Attitude Indicator:** Pitch, roll, heading
- **Altitude Graph:** Altitude vs. time
- **Airspeed Graph:** Speed vs. time
- **Battery Status:** Voltage, current, remaining
- **GPS Status:** Satellite count, HDOP
- **Mode:** Current flight mode
- **Messages:** Warnings, errors from autopilot

**Map View:**
- Drone position in real-time
- Flight path trail
- Waypoints and mission overlay
- Home location

**Quick Actions:**
- Mode change (Manual, Auto, RTL)
- Arm/Disarm
- Emergency stop

### Post-Flight Analysis

**Download Logs:**
1. Flight Data → Dataflash Logs
2. Download Log via Mavlink
3. Select log file, click "Download"

**Review Flight:**
1. Click "Log Browse"
2. Select downloaded log
3. View flight path on map
4. Graph any parameters (e.g., altitude, vibration, battery)

**Analyze Performance:**
- Check for vibrations (IMU graphs)
- Validate autopilot tuning (desired vs. actual attitude)
- Review battery consumption
- Identify any errors or warnings

---

## ISR Platform Considerations

### Mission-Specific Requirements

Based on the JPA Privateer business plan, here are the operational requirements for the full-size ISR drone:

#### 1. Maritime Environment Adaptations

**Salt Water Corrosion Resistance:**
- **Materials:** Composite (fiberglass, carbon fiber) preferred over aluminum
- **Coatings:** Protective paint, anti-corrosion treatments
- **Electronics:** Conformal coating on circuit boards
- **Sealing:** All openings sealed against moisture

**High Humidity:**
- **Desiccant packs:** Inside electronics bays
- **Ventilation:** Avoid condensation in fuselage
- **Regular maintenance:** Inspect for corrosion after each mission

**Sea Spray:**
- **Launch/recovery:** Protect from direct spray
- **Wipe down:** After each mission, clean surfaces

#### 2. Long-Endurance Design

**Battery vs. Gasoline:**

**Electric (LiPo Battery):**
- **Pros:** Simple, quiet, no fuel handling, instant power
- **Cons:** Heavy, limited energy density (~200 Wh/kg), 2-4 hours max
- **Best for:** Phase 1 trainer, short ISR missions

**Gasoline Engine:**
- **Pros:** High energy density (~12,000 Wh/kg), 8-12+ hours endurance
- **Cons:** Noisy, vibration, fuel handling, more complex
- **Best for:** Phase 2 ISR platform (Aerosonde-class)

**Hybrid (Electric + Solar):**
- **Pros:** Extended endurance, quiet, renewable
- **Cons:** Complex, heavy, depends on sunlight, expensive
- **Best for:** Experimental, future Phase 3

**Recommendation for ISR Platform:** **Gasoline engine** (2-4 HP)

**Engine Selection:**
- DLE 30cc (~3.5 HP, 2-stroke)
- Zenoah G38 (~3.8 HP, 2-stroke)
- EME 35cc (~4.0 HP, 2-stroke)
- Custom: Modify RC engine for reliability and endurance

**Fuel Capacity:**
- 10-hour mission @ 3 HP, 0.4 lb/hp/hr = 12 lbs fuel
- Tank size: ~2 gallons (12 lbs @ 6 lb/gal for gasoline)

#### 3. Payload Integration

**EO/IR Camera (Primary Sensor):**

**Requirements:**
- **EO (Electro-Optical):** Visible light camera, 4K resolution, 30x+ zoom
- **IR (Infrared):** Thermal imaging, 640x480 or better, uncooled sensor
- **Gimbal:** 2-axis or 3-axis stabilization
- **Weight:** 2-5 lbs (1-2 kg)
- **Datalink:** HD video downlink, low latency (<200ms)

**Commercial Options:**
1. **FLIR Duo Pro R:**
   - 4K visible + 640x512 thermal
   - 2-axis gimbal
   - Weight: ~1 lb (0.5 kg)
   - Cost: $3,000-$5,000

2. **Workswell WIRIS Pro:**
   - 30 MP visible + 640x512 thermal
   - Radiometric (temperature measurement)
   - Weight: ~1.5 lbs (0.7 kg)
   - Cost: $10,000-$15,000

3. **Custom:**
   - GoPro (visible) + FLIR Lepton (thermal)
   - DIY gimbal
   - Weight: <1 lb
   - Cost: $1,000-$2,000

**Recommendation:** Start with **FLIR Duo Pro R** for capability, or **custom** for budget

**AIS Receiver (Vessel Tracking):**
- **Purpose:** Automatic Identification System - receive vessel position broadcasts
- **Device:** dAISy USB receiver or similar
- **Integration:** Connect to autopilot (serial or USB)
- **Software:** Log AIS data, overlay on map
- **Weight:** <0.2 lbs
- **Cost:** $100-$200

**Optional Sensors:**
- **Laser Rangefinder/Designator:** Measure distance to target
- **SAR Radar:** All-weather detection (expensive, heavy)
- **Communications Relay:** Extend radio range for ground teams

#### 4. Datalink and Communications

**Video Downlink:**
- **Analog:** 5.8 GHz, 1.3 GHz (simple, low latency, lower quality)
- **Digital HD:** 2.4 GHz, 5.8 GHz (higher quality, higher latency, more complex)
- **Encrypted:** Military-grade encryption for sensitive missions
- **Range:** 10-50 km (depending on power, antenna, altitude)

**Recommended System:**
- **Ubiquiti Rocket M2/M5:** Long-range WiFi bridge
- **HD Video:** 1080p at 30 fps
- **Telemetry:** Embedded in video stream
- **Range:** 20-50 km line-of-sight
- **Cost:** $200-$500

**Telemetry:**
- **RFD900x:** 900 MHz long-range radio
- **Range:** 40+ km (depending on antenna, power)
- **Encrypted:** Optional AES encryption
- **Cost:** $200 (pair)

**Satellite Comms (Optional for BVLOS):**
- **Iridium:** Global coverage, expensive ($1-$2/min)
- **Starlink:** High bandwidth, requires tracking antenna (heavy)
- **For Phase 2:** If operating beyond line-of-sight

#### 5. Launch and Recovery Systems

**Catapult Launch:**

**Why:**
- No runway required
- Field deployment
- Proven for military UAVs (ScanEagle, Aerosonde, etc.)

**Types:**
1. **Bungee Launcher:**
   - Elastic bungee stretched, released
   - Simple, portable, cheap ($500-$1,000)
   - Suitable for <30 lb drones

2. **Pneumatic Launcher:**
   - Compressed air accelerates drone
   - More power, smoother launch
   - Complex, expensive ($5,000-$15,000)
   - Suitable for 30-60 lb drones

3. **Hydraulic Launcher:**
   - Hydraulic cylinder accelerates
   - Very powerful, used by military
   - Expensive ($20,000+)

**Recommendation for Phase 1:** **Bungee launcher**

**Recommendation for Phase 2:** **Pneumatic launcher** (or bungee for light design)

**Recovery Methods:**

1. **Parachute + Net:**
   - Parachute deploys, drone descends
   - Lands in net (protects airframe)
   - Simple, low cost ($500-$1,000)
   - Requires clear landing area

2. **Belly Landing:**
   - Drone lands on prepared surface (grass, foam)
   - Skid plate on fuselage bottom
   - Simplest, but risks damage
   - Cost: $0 (just design consideration)

3. **Skyhook (Vertical Recovery):**
   - Drone snags cable suspended between poles
   - Hangs from cable, lowered by winch
   - Used by Aerosonde, ScanEagle
   - Complex, expensive ($10,000-$20,000)

**Recommendation for Phase 1:** **Belly landing** (foam runway)

**Recommendation for Phase 2:** **Parachute + net** (low-risk recovery)

**Future (Phase 3):** **Skyhook** if high-volume operations justify cost

---

### Offensive Platform Considerations

While the JPA plan focuses on ISR (Phase 1) with potential transition to interdiction (Phase 2), here are considerations if offensive capabilities are ever required:

#### 1. Weapons Integration (Hypothetical)

**Legal Framework:**
- Requires federal authorization (Letter of Marque or similar)
- International law considerations (UN conventions)
- ROE (Rules of Engagement) compliance
- Extensive legal review required

**Potential Payloads:**
- **Non-Lethal:** LRAD (acoustic deterrent), dazzler laser, water cannon (if large enough)
- **Kinetic:** Small munitions, 40mm grenades (highly regulated, unlikely for privateer)
- **Marking:** Smoke grenades, dye markers (for tracking vessels)

**Design Considerations:**
- **Hardpoints:** Wing or fuselage mounts for payload
- **Release Mechanism:** Servo-actuated release
- **Targeting:** Laser designator, GPS-guided
- **Safety:** Arming/disarming logic, abort capability

**Recommendation:** **Focus on ISR**, offensive capabilities are high-risk legally and technically

#### 2. Kamikaze/Loitering Munition

**Concept:**
- Drone loiters over area, identifies target, dives to impact
- Used by military (Switchblade, Harop, etc.)

**Challenges:**
- Legal: Use of force by private entity (extremely difficult to authorize)
- Ethical: Risk of collateral damage
- Technical: Precision guidance, warhead design
- Cost: One-way mission = expensive per use

**Recommendation:** **Not suitable for Privateer mission** (focus on ISR support to federal agencies)

#### 3. Communications Relay / Jamming

**Relay:**
- Extend radio range for ground teams
- Relay between vessels and base station
- Useful for coordinating interdiction operations

**Jamming (Electronic Warfare):**
- Disrupt cartel communications
- Likely illegal without federal authorization (FCC regulations)
- Technically complex

**Recommendation:** **Communications relay feasible**, jamming not recommended

---

## Regulatory Compliance

### FAA Part 107 (Small UAS Rules)

**Summary:**
Part 107 governs commercial operation of small unmanned aircraft (<55 lbs) in the United States.

**Key Requirements:**

1. **Remote Pilot Certificate:**
   - Pass FAA knowledge test
   - TSA background check
   - Recurrent training every 24 months
   - Cost: $175 test fee

2. **Aircraft Registration:**
   - Register drone with FAA
   - Display registration number on aircraft
   - Cost: $5 per aircraft (3 years)

3. **Operational Limits:**
   - Maximum altitude: 400 ft AGL (Above Ground Level)
   - Must maintain visual line of sight (VLOS)
   - Daylight operations only (unless waiver)
   - No operations over people (unless waiver or certified aircraft)
   - No operations from moving vehicle (unless over sparsely populated area)
   - Yield right-of-way to manned aircraft

4. **Airspace:**
   - Class G (uncontrolled): OK without authorization
   - Class B, C, D, E (controlled): Requires LAANC authorization or manual waiver
   - Restricted, prohibited areas: No operations

**Waivers:**
- Can apply for waiver to exceed limits (night, BVLOS, over people, etc.)
- Part 107 waiver application online (DroneZone)
- Approval time: 90-120 days (can be expedited for government contractors)

### Part 107 vs. Part 91 (Manned Aircraft Rules)

**If Drone Exceeds 55 lbs:**
- No longer "small UAS" under Part 107
- Must comply with Part 91 (general aviation)
- Requires airworthiness certificate (very difficult for custom UAV)
- Extensive paperwork and inspections

**Recommendation:** **Stay under 55 lbs** to remain in Part 107

**Aerosonde-Class Drone:**
- Mk 4.7G: 71-79 lbs (exceeds Part 107)
- Custom design: Target 40-50 lbs to stay under 55 lb limit
- Trade-off: Endurance vs. regulatory simplicity

### Beyond Visual Line of Sight (BVLOS)

**Why BVLOS is Critical for ISR:**
- Maritime patrol requires 100+ km range
- Visual line of sight is typically <5 km
- Must operate BVLOS to be effective

**BVLOS Waiver Requirements:**
1. **Detect and Avoid (DAA):**
   - Ability to see other aircraft (ADS-B receiver, radar, or visual observer network)
   - Procedures to avoid collisions

2. **Communications:**
   - Reliable command and control link
   - Lost link procedures (automatic return)

3. **Operations Manual:**
   - Detailed procedures for all phases of flight
   - Emergency procedures
   - Training program

4. **Risk Mitigation:**
   - Flight over sparsely populated areas (ocean is ideal)
   - Geofencing, altitude limits
   - Coordination with ATC (Air Traffic Control)

**FAA Part 107 Waiver for BVLOS:**
- Apply via DroneZone
- Provide: Aircraft specs, ops manual, safety case, DAA method
- Approval time: 120+ days
- May require iterative submissions

**Alternative: COA (Certificate of Authorization):**
- For public aircraft (government agencies)
- Faster approval if working as government contractor
- Requires sponsorship by federal agency (CBP, DEA, etc.)

**Recommendation:**
- **Phase 1:** Operate VLOS (within Part 107 limits)
- **Phase 2:** Apply for BVLOS waiver OR operate as federal contractor under COA

### FAA Part 135 (Commercial Operator Certificate)

**What is Part 135:**
- Certification for commercial operators (charter flights, cargo, etc.)
- Extends to drone package delivery (Amazon, UPS, etc.)

**When Required:**
- If operating drone for hire in a way that resembles charter/cargo
- Typically not required for ISR (data collection, not transport)

**Recommendation:** **Not required for ISR mission**

### Export Controls (ITAR)

**International Traffic in Arms Regulations (ITAR):**
- Controls export of defense-related technology
- Applies to military-grade UAVs, sensors, encryption

**Potential ITAR Items:**
- Encrypted datalinks
- Thermal imaging cameras (high-resolution)
- Autopilot with weapons integration

**Compliance:**
- Register with State Department (DDTC)
- Obtain export license if selling/transferring abroad
- Restrict access to foreign nationals

**Recommendation:**
- Use commercial, non-ITAR components where possible
- If using ITAR items, consult export attorney
- For Privateer mission (domestic operations), ITAR less of a concern

### Maritime Regulations (USCG)

**Operating Over Water:**
- FAA rules still apply (Part 107 or COA)
- Coordination with Coast Guard recommended (not legally required for drone)
- If launched from vessel: Vessel must comply with USCG regulations

**Best Practices:**
- Notify USCG of operations (avoid interference with rescues, patrols)
- Use marine radio to announce drone operations in area
- File NOTAM (Notice to Airmen) for airspace awareness

---

## Development Roadmap

### Phase 1: Starter Drone (Months 1-6)

**Month 1: Design and Procurement**
- [ ] Finalize Phase 1 design requirements
- [ ] Create OpenVSP model (geometry, mass properties)
- [ ] Select airfoil (E423 or S1223)
- [ ] Calculate performance (L/D, endurance, speed)
- [ ] Source components:
  - [ ] Foam sheets, carbon spars, composites
  - [ ] Motor, ESC, battery, propeller
  - [ ] Pixhawk 4, GPS, airspeed sensor, telemetry
  - [ ] RC transmitter and receiver
  - [ ] Camera and gimbal
- [ ] Budget: $2,000-$3,000

**Month 2-3: Fabrication**
- [ ] Hot-wire cut foam wings (or CNC ribs)
- [ ] Build fuselage (foam or fiberglass mold)
- [ ] Construct tail surfaces
- [ ] Assemble structure (epoxy, CA glue)
- [ ] Install servos, linkages, pushrods
- [ ] Mount motor, ESC, battery tray
- [ ] Install avionics (Pixhawk, GPS, telemetry)
- [ ] Surface finish (spackle, sand, paint)

**Month 4: Ground Testing**
- [ ] Balance (check CG at 25-30% MAC)
- [ ] Control surface checks (direction, throws)
- [ ] Motor bench test (thrust, current, temperature)
- [ ] Ardupilot configuration:
  - [ ] Frame type, servo assignments
  - [ ] Sensor calibration (accel, compass, airspeed)
  - [ ] Radio calibration, flight modes
  - [ ] Geofence, failsafes
- [ ] Telemetry range test (walk out to 1+ km)
- [ ] Catapult launcher test (or hand launch practice)

**Month 5: Flight Testing**
- [ ] Week 1: First flight (manual mode, calm winds)
  - Hand launch or catapult
  - Stabilize, fly circuit, land (belly or parachute)
  - Log review: Vibration, airspeed, battery
- [ ] Week 2-3: Envelope expansion
  - Test speed range (slow to fast)
  - Test bank angles, climbs, descents
  - Trim adjustments
- [ ] Week 4: Autopilot testing
  - FBWA (fly-by-wire) mode
  - Loiter mode (circle at location)
  - Auto mode (simple waypoint mission)

**Month 6: Endurance and Payload Testing**
- [ ] Endurance test (fly until battery low, measure time)
  - Target: 30-60 minutes
  - Optimize speed for maximum endurance
- [ ] Camera payload test
  - Mount camera, test gimbal control
  - Record video, check quality
- [ ] Mission simulation
  - Program ISR patrol mission (racetrack or survey grid)
  - Fly autonomously, review imagery
- [ ] Document lessons learned
  - What worked, what didn't
  - Design changes for Phase 2

**Deliverables:**
- Functional fixed-wing UAV (30-60 min endurance)
- Proven Ardupilot configuration
- Flight test data (performance validation)
- Operator proficiency (FAA Part 107 certification)
- Lessons learned document

**Budget:** $5,000-$10,000

---

### Phase 2: Full-Size ISR Platform (Months 7-18)

**Month 7-9: Detailed Design**
- [ ] Finalize Phase 2 requirements (based on JPA mission profile)
- [ ] Trade study: Custom design vs. commercial purchase
  - Custom: $50K-$100K, full control, learning
  - Commercial (Aerosonde-like): $100K-$200K, proven, faster
- [ ] If custom design:
  - [ ] OpenVSP detailed model (airframe geometry)
  - [ ] CFD analysis (XFLR5 or OpenFOAM for drag validation)
  - [ ] FEA stress analysis (wing spar, fuselage)
  - [ ] Propulsion sizing (gasoline engine, fuel capacity)
  - [ ] Payload integration (EO/IR camera, AIS, datalink)
  - [ ] Launch/recovery system design (catapult, parachute)
- [ ] If commercial purchase:
  - [ ] RFQ to vendors (Textron, Insitu, etc.)
  - [ ] Evaluate systems (cost, capability, support)
  - [ ] Negotiate purchase or lease

**Month 10-12: Procurement and Fabrication (Custom Path)**
- [ ] Source materials:
  - [ ] Composite materials (fiberglass, carbon fiber, epoxy)
  - [ ] Gasoline engine (DLE 30cc or similar)
  - [ ] Fuel tank, fuel pump, fuel lines
  - [ ] Advanced avionics (Cube Orange+, RTK GPS, etc.)
  - [ ] EO/IR camera (FLIR Duo Pro R or similar)
  - [ ] Long-range telemetry (RFD900x)
  - [ ] Datalink (Ubiquiti or encrypted system)
- [ ] Fabrication:
  - [ ] CNC mold for composite fuselage
  - [ ] Composite layup (fiberglass shell, carbon reinforcements)
  - [ ] Wing construction (foam core, carbon spar, fiberglass skin)
  - [ ] Tail surfaces (composite)
  - [ ] Integration of engine, fuel system
  - [ ] Avionics installation
  - [ ] Wiring harness (power, datalink, sensors)

**Month 13-14: Ground Testing**
- [ ] Static engine run (break-in, tuning)
- [ ] Weight and balance (target CG location)
- [ ] Control surface rigging
- [ ] Ardupilot configuration (engine-specific params)
- [ ] Sensor calibration
- [ ] Payload testing (camera, gimbal, datalink)
- [ ] Catapult launcher construction and testing
- [ ] Parachute recovery system testing

**Month 15-16: Flight Testing**
- [ ] First flight (manual control, experienced pilot)
- [ ] Engine reliability testing (multiple flights)
- [ ] Autopilot mode testing (FBWA, Auto, RTL)
- [ ] Endurance testing (8-12 hour flights)
  - Incremental (2 hr, 4 hr, 8 hr, 12 hr)
  - Fuel consumption validation
- [ ] Payload testing (camera quality, gimbal stability, datalink range)

**Month 17-18: Operational Testing and Certification**
- [ ] Mission simulations:
  - [ ] Maritime patrol (racetrack pattern over water)
  - [ ] Target tracking (follow moving vessel)
  - [ ] Intelligence reporting (capture imagery, transmit to GCS)
- [ ] TitanPlanner integration:
  - [ ] Mission planning workflow
  - [ ] Real-time telemetry monitoring
  - [ ] Post-flight log review
- [ ] FAA Part 107 BVLOS waiver application (if not already approved)
- [ ] Federal agency demonstration:
  - [ ] Invite CBP, DEA, or USCG to observe flight
  - [ ] Showcase capabilities (endurance, sensors, datalink)
  - [ ] Discuss contract opportunities

**Deliverables:**
- Aerosonde-class ISR UAV (8-12 hour endurance)
- Integrated EO/IR camera with HD datalink
- TitanPlanner ground control station configured for ISR missions
- Flight test report (performance validation)
- FAA BVLOS waiver (or COA if federal contractor)
- Demonstrated capability to federal agencies

**Budget:**
- **Custom Design:** $50,000-$100,000
- **Commercial Purchase:** $100,000-$200,000

---

### Phase 3: Operational Deployment (Month 19+)

**Month 19-24: Contract Pursuit**
- [ ] Federal contracting preparation:
  - [ ] SAM.gov registration (System for Award Management)
  - [ ] Capability statement (showcase UAV capabilities)
  - [ ] Past performance (if any prior contracts)
- [ ] Identify contract opportunities:
  - [ ] CBP maritime surveillance contracts
  - [ ] DEA intelligence support
  - [ ] USCG joint operations
  - [ ] JIATF-South ISR support
- [ ] Submit bids/proposals
- [ ] Award and contract negotiation

**Month 24+: Operations**
- [ ] Execute ISR missions:
  - [ ] 3-5 missions per week (per JPA plan)
  - [ ] 150-250 flight hours per month
  - [ ] Coverage of 500-1000 square nautical miles
- [ ] Intelligence reporting:
  - [ ] Real-time vessel tracking
  - [ ] Post-mission intelligence reports (SALUTE format)
  - [ ] Pattern-of-life analysis
- [ ] Maintenance:
  - [ ] Post-flight inspections
  - [ ] Engine maintenance (oil changes, spark plugs, etc.)
  - [ ] Structural inspections (composite repairs as needed)
  - [ ] Avionics calibration and updates
- [ ] Continuous improvement:
  - [ ] Lessons learned from each mission
  - [ ] Autopilot tuning refinements
  - [ ] Payload upgrades (better cameras, additional sensors)

**Year 2-3: Scaling**
- [ ] Build additional airframes (fleet of 2-4 UAVs)
- [ ] Hire and train additional pilots/operators
- [ ] Expand operational areas (Gulf of Mexico, Caribbean, California)
- [ ] Pursue privateer transition (Phase 2 operations) if legislation passes

---

## Summary and Next Steps

### Key Takeaways

1. **Phased Approach is Critical:**
   - Start small (Phase 1 trainer) to build skills before scaling to full-size ISR platform
   - Reduces risk and cost of learning curve

2. **Aerosonde is the Benchmark:**
   - 8-12 hour endurance, 71-79 lb takeoff weight
   - Gasoline engine for long endurance
   - Proven design for maritime ISR

3. **Stay Under 55 lbs for Regulatory Simplicity:**
   - Part 107 is much easier than Part 91
   - Design custom drone at 40-50 lbs to remain in Part 107
   - Apply for BVLOS waiver for maritime operations

4. **TitanPlanner + Ardupilot is the Stack:**
   - Open-source, proven, extensive community
   - TitanPlanner provides better UX for frequent users
   - Full mission planning and telemetry capabilities

5. **JPA Privateer Mission Drives Requirements:**
   - 8-12 hour endurance mandatory
   - EO/IR camera and datalink critical
   - Operating cost target: <$500/hour
   - Contract value: $400K-$2M annually (Year 1-3)

6. **OpenVSP Enables Rapid Design Iteration:**
   - Free tool for geometry, mass properties, aero estimates
   - Export to CAD for manufacturing

7. **Airfoil Selection Matters:**
   - E423 for efficiency (Phase 2 ISR)
   - S1223 for high lift (Phase 1 trainer)
   - Low Reynolds number considerations

### Immediate Next Steps (Week 1-2)

1. **Set Up Tools:**
   - [ ] Download and install OpenVSP
   - [ ] Download and install TitanPlanner (or Mission Planner)
   - [ ] Install XFLR5 for airfoil analysis
   - [ ] Set up CAD software (Fusion 360, SolidWorks, etc.)

2. **Design Review:**
   - [ ] Review this plan with team/stakeholders
   - [ ] Finalize Phase 1 requirements
   - [ ] Make go/no-go decision on custom vs. commercial for Phase 2

3. **Budget and Schedule:**
   - [ ] Confirm budget ($5K-$10K for Phase 1, $50K-$200K for Phase 2)
   - [ ] Set timeline (6 months for Phase 1, 12 months for Phase 2)
   - [ ] Identify funding sources (personal, investor, contract advance)

4. **Regulatory Prep:**
   - [ ] Obtain FAA Part 107 Remote Pilot Certificate (if not already have)
   - [ ] Register with FAA (once aircraft is built)
   - [ ] Research BVLOS waiver requirements (for Phase 2)

5. **Begin Phase 1 Design:**
   - [ ] Create OpenVSP model (start with basic geometry)
   - [ ] Calculate mass budget
   - [ ] Estimate performance (endurance, speed, L/D)
   - [ ] Select components (motor, battery, propeller)

### Questions to Answer Before Proceeding

1. **What is the primary goal?**
   - Learning and skill development (favor custom design, Phase 1 focus)
   - Fastest path to operational capability (favor commercial purchase, Phase 2 focus)
   - Cost optimization (favor custom design, accept longer timeline)

2. **What is the risk tolerance?**
   - High (go straight to Phase 2 custom design, accept risk of failure)
   - Moderate (do Phase 1 trainer, then Phase 2 custom)
   - Low (buy commercial drone for Phase 2, skip custom design)

3. **What are the team capabilities?**
   - Aerospace engineering experience (custom design feasible)
   - RC aircraft experience (assembly and flight testing feasible)
   - Software development (Ardupilot customization, datalink development)
   - Fabrication skills (composite layup, CNC machining, etc.)

4. **What is the timeline pressure?**
   - Urgent (6-12 months to operational): Buy commercial or use contractor
   - Moderate (12-24 months): Custom design feasible
   - Long-term (24+ months): Iterate through multiple prototypes

5. **What is the funding situation?**
   - Self-funded: Minimize cost, phased approach
   - Investor-funded: Faster timeline, commercial purchase acceptable
   - Contract-funded: Build to spec, proven capability

### Recommended Path

**For someone with your background (commercial drone pilot, regulatory knowledge):**

1. **Start with Phase 1 Trainer:**
   - Build hands-on experience with fixed-wing design
   - Validate OpenVSP workflow
   - Develop Ardupilot proficiency
   - Prove concept before scaling
   - Cost: $5,000-$10,000
   - Timeline: 6 months

2. **Evaluate Custom vs. Commercial for Phase 2:**
   - Decision point after Phase 1 flight testing
   - If Phase 1 successful and team has capability: Custom design
   - If timeline critical or funding available: Commercial purchase
   - Hybrid: Buy commercial, customize payload/datalink

3. **Focus on ISR Mission (Not Offensive):**
   - Legal and regulatory path is clearer
   - Federal contracts are available today (no legislation needed)
   - Offensive capabilities are high-risk, low-probability

4. **Integrate with JPA Business Plan:**
   - ISR capability is core to Phase 1 contract revenue
   - Demonstrate to CBP/DEA during operational testing (Month 17-18)
   - Leverage for contract awards (Year 1-2)

---

**Document Prepared By:** Claude (AI Assistant)  
**Based On:** User requirements, Aerosonde research, JPA business plan, OpenVSP workflow, Ardupilot documentation  
**Next Review:** After Phase 1 design completion (Month 1-2)
