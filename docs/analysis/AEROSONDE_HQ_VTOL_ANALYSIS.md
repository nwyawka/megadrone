# Aerosonde HQ VTOL Analysis

**Variant:** Aerosonde Mk 4.7 HQ (Hybrid Quadcopter)  
**Manufacturer:** Textron Systems  
**Type:** Fixed-wing with vertical takeoff/landing (VTOL) capability  
**Source:** https://www.textronsystems.com/products/aerosonde-uas  
**Date:** January 8, 2026

---

## Key Capabilities from Textron Article

### Performance Specifications

**Endurance:**
- **Up to 20 hours** flight time
- Significantly longer than standard fixed-wing variants (10-16 hours)
- Enabled by hybrid propulsion (electric VTOL + gasoline cruise)

**Range:**
- **Over 140 km** (87 miles) operational radius
- Easily extended with "spoke sites" (forward operating locations)
- Total coverage area can exceed 300+ km with relay sites

**Operations:**
- **Day and night** operations (advanced sensors)
- **All-weather** capability (within limits)
- **Real-time data transmission** to ground stations

**Total Flight Hours:**
- **Over 700,000 flight hours** across all Aerosonde variants
- Proven reliability in military operations

---

## VTOL Configuration

### Hybrid Design Philosophy

**Fixed-Wing (Cruise Flight):**
- Main wing provides lift during forward flight
- Pusher propeller (gasoline 2-stroke engine)
- High efficiency, long endurance

**Quadcopter (Vertical Flight):**
- Four electric motors/propellers for VTOL
- Used only for takeoff and landing (5-10 minutes)
- Stowed or feathered during cruise to reduce drag

**Benefits:**
1. **No runway required** - operate from ships, rooftops, small clearings
2. **Rapid deployment** - vertical takeoff in <2 minutes
3. **Precision landing** - GPS-guided touchdown
4. **Ship-based operations** - land on moving vessels

---

## Hybrid Propulsion System

### Cruise Propulsion (Forward Flight)

**Engine:** 2-stroke gasoline (similar to NGH GT25 or DLE 30)
- **Power:** 2.5-4.0 HP
- **Fuel:** Gasoline (1-2 gallons for 20-hour mission)
- **Propeller:** Pusher configuration, 18-22" diameter
- **Use:** 95% of flight time (cruise, loiter, transit)

### VTOL Propulsion (Vertical Flight)

**Motors:** 4x electric brushless outrunners
- **Power:** 500-1000W each (2-4 kW total)
- **Battery:** High-discharge LiPo, 6S or 12S
- **Propellers:** 12-16" diameter, high pitch
- **Use:** 5% of flight time (takeoff, landing, hover)

**Battery Sizing:**
- Takeoff/landing: ~5-10 minutes total
- Hover power: ~2-3 kW (50% of total for 40 lb aircraft)
- Energy required: 2.5 kW * 0.15 hr = **0.38 kWh** (380 Wh)
- Battery capacity: 380 Wh / 0.85 (discharge efficiency) = **450 Wh**
- Example: 6S (22.2V) * 20 Ah = **444 Wh** ✓
- Battery weight: ~4.5 lbs (2 kg) for VTOL only

---

## Configuration Comparison

| Feature | Aerosonde Mk 4.7 (Fixed-Wing) | Aerosonde Mk 4.7 HQ (VTOL) |
|---------|-------------------------------|---------------------------|
| **Wingspan** | 12-14.5 ft (3.8-4.4 m) | **17.03 ft (5.19 m)** (larger for added weight) |
| **Takeoff Weight** | 71-79 lbs (32-36 kg) | **~80-90 lbs (36-41 kg)** (est., with VTOL system) |
| **Launch** | Catapult/launcher | **Vertical takeoff** |
| **Recovery** | Net/parachute/skyhook | **Vertical landing** |
| **Endurance** | 10-16 hours | **Up to 20 hours** |
| **Range** | 60-100 NM | **140+ km (75+ NM)** |
| **Propulsion** | Gasoline engine only | **Hybrid (gas + electric)** |
| **Deployment** | Requires launcher | **Fully autonomous VTOL** |
| **Cost** | $150K-$200K (system) | **$200K-$300K** (est., +$50K for VTOL) |

---

## Design Implications for Our Project

### Advantages of VTOL for ISR Mission

**JPA Privateer Application:**

1. **Ship-Based Operations:**
   - Launch from patrol vessel (47' MLB or similar)
   - No catapult needed (saves deck space, complexity)
   - Land on deck in rough seas (GPS-guided precision)

2. **Field Deployment:**
   - Launch from unprepared sites (beaches, parking lots, rooftops)
   - Operate from Florida Keys (small islands, no runways)
   - Quick response (no launcher setup time)

3. **Safety:**
   - Controlled landing (less crash risk than net/parachute)
   - Abort capability (can hover and re-attempt landing)
   - Safer for personnel (no catapult or recovery crew in danger zone)

4. **Operational Tempo:**
   - Faster turnaround (vertical takeoff/landing vs. launcher setup)
   - Multiple sorties per day
   - 3-5 missions per week (per JPA requirement) more achievable

### Disadvantages (Trade-offs)

1. **Increased Weight:**
   - VTOL motors, ESCs, props: +5-8 lbs
   - VTOL battery: +4-5 lbs
   - Structural reinforcement: +2-3 lbs
   - **Total added weight:** 11-16 lbs (20-30% increase)

2. **Increased Complexity:**
   - Two propulsion systems to maintain
   - Transition logic (VTOL → forward flight)
   - Additional failure modes

3. **Reduced Endurance (or increased weight):**
   - If keeping same fuel load: Heavier = less efficient = shorter endurance
   - To maintain 20-hour endurance: Need more fuel = even heavier

4. **Higher Cost:**
   - Additional motors, ESCs, props, battery
   - Development cost (VTOL transition logic)
   - Est. **+$5,000-$10,000** for Phase 2 custom design

---

## VTOL Configuration Options

### Option 1: Quadplane (ArduPilot Term)

**Configuration:**
- Main wing with pusher propeller (gasoline)
- Four vertical motors on booms/wings
- Motors tilt or are fixed vertical

**Used By:**
- ArduPilot "QuadPlane" firmware
- Vertical Technologies VTOL platforms
- Aerosonde HQ (likely this configuration)

**Pros:**
- Proven in ArduPilot (extensive support)
- Redundancy (can fly on wing or VTOL motors separately)
- Simple transition logic

**Cons:**
- Drag from VTOL motors in cruise (must fold or feather props)
- Heavy (need strong wing structure for motor mounts)

---

### Option 2: Tiltrotor

**Configuration:**
- Two large motors on wing tips
- Motors tilt from vertical (hover) to horizontal (cruise)
- Can use same motors/props for VTOL and cruise

**Used By:**
- Bell V-22 Osprey (manned)
- Arcturus JUMP 20 (unmanned)

**Pros:**
- Lighter (use same motors for both modes)
- Less drag (no extra motors in cruise)
- Fewer components (motors do double duty)

**Cons:**
- Complex tilt mechanism (motors rotate 90°)
- Single motor failure = loss of control in VTOL
- ArduPilot support less mature

---

### Option 3: Tailsitter

**Configuration:**
- Aircraft sits on tail for takeoff
- Takes off vertically, then pitches forward to horizontal flight
- Wing provides lift in both modes

**Used By:**
- Martin Marietta X-24 (experimental)
- Some small UAVs (experimental)

**Pros:**
- No extra motors (use main propulsion for VTOL)
- Lightest weight
- Minimal drag penalty

**Cons:**
- Difficult transition (high pilot/autopilot skill required)
- Poor visibility in VTOL mode (pointing up)
- Hard to land precisely (pointing up makes sensing ground difficult)
- Not suitable for our ISR mission

---

### Recommendation: Quadplane (Option 1)

**Rationale:**
- **ArduPilot support:** QuadPlane firmware is mature, well-documented
- **Reliability:** Redundancy (can fly on either system if one fails)
- **Ease of development:** Proven configuration, less risk
- **Operational safety:** Stable hover, precise landing
- **Trade-off:** Accept weight penalty for reliability and simplicity

---

## Quadplane Design for Phase 2

### VTOL Motor Placement

**Configuration:** "H" or "X" quad layout

**Option A: Wing-Mounted (Booms)**
- Motors on outrigger booms attached to wings
- Pros: Easy to build, motors far from fuselage (less interference)
- Cons: Drag from booms, added wing bending loads

**Option B: Fuselage-Mounted**
- Motors on fuselage sides/front/rear
- Pros: No booms, simpler structure
- Cons: Propwash interference with wing/tail, less stable hover

**Recommendation:** **Wing-mounted booms** (like Aerosonde HQ)
- Attach carbon fiber tubes to wing (front and rear of center section)
- Mount motors at end of booms
- Layout: "H" configuration (2 motors front, 2 rear)

---

### VTOL Motor Specifications

**For 45 lb (20 kg) Quadplane:**

**Thrust Required:**
- Total weight: 45 lbs (200 N)
- Hover thrust: 1.5 x weight = 300 N (67 lbs) for stability
- Per motor (4 total): 300 N / 4 = **75 N (17 lbs) thrust**

**Motor Selection:**
- **Type:** Brushless outrunner, 800-1200 Kv
- **Power:** 750-1000W per motor (3-4 kW total)
- **Example:** T-Motor MN4010 or similar
- **Propeller:** 13-15" diameter, high pitch (5-6" pitch)
- **Cost:** $100-150 per motor x 4 = **$400-600**

**ESC (Electronic Speed Controller):**
- **Rating:** 40-60A per ESC
- **Type:** SimonK or BLHeli firmware (fast response)
- **Cost:** $40-60 per ESC x 4 = **$160-240**

**Total VTOL Propulsion Cost:** $560-840

---

### VTOL Battery Sizing

**Energy Required (Takeoff + Landing):**
- Hover power: 3 kW (conservative, includes inefficiency)
- Hover time: 5 minutes (takeoff: 2 min, landing: 2 min, reserve: 1 min)
- Energy: 3 kW * (5/60) hr = **250 Wh**

**Battery Specification:**
- Capacity: 250 Wh / 0.8 (80% depth of discharge) = **312 Wh**
- Voltage: 6S (22.2V nominal)
- Amp-hours: 312 Wh / 22.2V = **14 Ah**
- **Battery:** 6S 14,000 mAh LiPo (or 2x 6S 7000 mAh in parallel)
- **Weight:** ~3.5-4.0 lbs (1.6-1.8 kg)
- **Cost:** $150-250

**Note:** This is separate from cruise propulsion (gasoline engine)

---

### Transition Logic (VTOL ↔ Forward Flight)

**Takeoff Sequence (ArduPilot QuadPlane):**
1. **Pre-flight:** Arm in QSTABILIZE mode (Q = quad mode)
2. **Vertical takeoff:** Throttle up, climb to 50-100 ft AGL
3. **Transition altitude:** Switch to QLOITER (GPS hold)
4. **Accelerate:** Increase forward speed (quad motors + main motor)
5. **Transition:** At transition speed (~15-20 m/s), wing takes over lift
6. **Cruise:** Quad motors idle or stop, main motor provides thrust
7. **Mode change:** Switch to FBWA or AUTO (fixed-wing modes)

**Landing Sequence:**
1. **Approach:** Fly waypoint pattern to landing point (fixed-wing mode)
2. **Transition altitude:** 100-150 ft AGL, switch to QLOITER
3. **Decelerate:** Reduce forward speed, quad motors spin up
4. **Transition:** At transition speed, switch to quad lift
5. **Descent:** QLAND mode (automated vertical landing)
6. **Touchdown:** GPS-guided, descend to ground
7. **Disarm:** Auto-disarm after touchdown

**Critical Parameters (ArduPilot):**
- **Q_TRANSITION_MS:** Time to transition (2-5 seconds typical)
- **Q_ASSIST_SPEED:** Speed below which quad motors help in forward flight
- **ARSPD_FBW_MIN:** Minimum airspeed in forward flight (stall prevention)

---

## Weight and Performance Impact

### Weight Breakdown (45 lb Quadplane)

| Component | Fixed-Wing Only | Quadplane (VTOL) | Delta |
|-----------|-----------------|------------------|-------|
| **Airframe** | 12 lbs | 14 lbs | +2 lbs (stronger structure) |
| **Main Propulsion** | 2 lbs | 2 lbs | - |
| **Fuel (gasoline)** | 10 lbs | 10 lbs | - |
| **VTOL Motors/ESCs** | - | 3 lbs | +3 lbs |
| **VTOL Battery** | - | 4 lbs | +4 lbs |
| **VTOL Booms/Mounts** | - | 2 lbs | +2 lbs |
| **Avionics** | 2 lbs | 2 lbs | - |
| **Payload (Camera)** | 2 lbs | 2 lbs | - |
| **Total Empty** | 18 lbs | 29 lbs | **+11 lbs** |
| **Total Loaded** | 30 lbs | 41 lbs | **+11 lbs** |

**Impact:**
- **Weight increase:** ~37% (30 lbs → 41 lbs)
- **Wing loading increase:** Higher weight/area = faster cruise speed
- **Drag increase:** Booms and motors add parasitic drag (~10-15%)
- **Endurance decrease:** ~10-20% reduction (or need more fuel to maintain)

**To Maintain 20-Hour Endurance:**
- Need to increase fuel from 10 lbs to 12-13 lbs
- Total weight: 43-44 lbs
- Wing loading: Must increase wing area or accept higher speed

---

## Cost Analysis: Fixed-Wing vs. VTOL

### Phase 2 Custom Design Cost Comparison

| Category | Fixed-Wing | Quadplane VTOL | Delta |
|----------|------------|----------------|-------|
| **Airframe** | $15,000 | $17,000 | +$2,000 (stronger structure, booms) |
| **Main Propulsion** | $1,000 | $1,000 | - |
| **VTOL Motors/ESCs** | - | $800 | +$800 |
| **VTOL Battery** | - | $200 | +$200 |
| **Avionics (Ardupilot)** | $1,500 | $1,500 | - (same Pixhawk, runs QuadPlane) |
| **Sensors/Payload** | $5,000 | $5,000 | - |
| **Development** | $10,000 | $15,000 | +$5,000 (VTOL tuning, testing) |
| **Total** | **$32,500** | **$40,500** | **+$8,000** (25% increase) |

**Verdict:**
- VTOL adds **~$8,000** to Phase 2 custom design
- **Worth it if:** Ship-based operations, no runway access, frequent deployments
- **Not worth it if:** Operating from airfields, cost-sensitive, low flight rate

---

## Recommendation for MegaDrone Project

### Phase 1: Build Fixed-Wing Trainer (No VTOL)

**Rationale:**
- Learn basic fixed-wing design and flight
- Simpler, cheaper, faster to build
- Validate OpenVSP workflow, airfoil selection, etc.
- No need for VTOL (hand launch or bungee launcher sufficient)

**Cost:** $5,000-$10,000  
**Timeline:** 6 months

---

### Phase 2: Decision Point (Fixed-Wing vs. VTOL)

**Build VTOL Quadplane if:**
1. **Ship-based operations** are required (JPA Privateer mission)
2. **No runway access** at operating locations
3. **Budget allows** +$8,000 for VTOL system
4. **Willing to accept** 10-20% endurance reduction (or heavier design)

**Build Fixed-Wing Only if:**
1. **Land-based operations** from airfields or prepared sites
2. **Catapult/bungee launch** is acceptable
3. **Maximizing endurance** is critical (20+ hours)
4. **Budget-constrained** (save $8,000)

**My Recommendation:**
- **Start with fixed-wing** (Phase 2a): Prove 10-12 hour endurance, validate NGH GT25
- **Add VTOL later** (Phase 2b): Once fixed-wing is proven, retrofit VTOL system
- **Modular design:** Design airframe with hard points for future VTOL motor booms

---

## ArduPilot QuadPlane Resources

**Documentation:**
- QuadPlane Overview: https://ardupilot.org/plane/docs/quadplane-overview.html
- Parameters: https://ardupilot.org/plane/docs/quadplane-parameters.html
- First Flight: https://ardupilot.org/plane/docs/quadplane-first-flight.html

**Community:**
- ArduPilot Forum (QuadPlane): https://discuss.ardupilot.org/c/arduplane/quadplane
- Examples: Many users building VTOL fixed-wings

**Hardware:**
- Pixhawk autopilot supports QuadPlane out-of-the-box
- No special hardware needed (same as fixed-wing + quad motors)

---

## Next Steps

1. **Phase 1:** Build fixed-wing trainer (no VTOL)
2. **Study ArduPilot QuadPlane:** Read documentation, watch videos
3. **Phase 2 Decision:** After Phase 1 success, decide fixed-wing vs. VTOL
4. **If VTOL:** Design motor booms, select VTOL motors/ESCs, size battery
5. **OpenVSP Modeling:** Create both variants in OpenVSP (see Python scripts)

---

**Document Prepared:** January 8, 2026  
**Aerosonde HQ Analysis:** VTOL hybrid configuration  
**Recommendation:** Start with fixed-wing, add VTOL in Phase 2b if needed  
**Cost Impact:** +$8,000 (25% increase) for VTOL system
