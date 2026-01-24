# Phase 2 Engine Analysis: NGH GT25 25cc Two-Stroke

**Engine:** NGH GT25 25cc Two-Stroke Gasoline Engine  
**Source:** Motion RC  
**Link:** https://www.motionrc.com/products/ngh-gt25-25cc-two-stroke-engine-ngh-gt25  
**Date:** January 8, 2026

---

## Engine Specifications

### NGH GT25 Key Specs

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Displacement** | 25cc (1.53 cu in) | Good for 40-50 lb aircraft |
| **Power Output** | 2.5-3.0 HP @ 7500 RPM | Estimated (not specified by manufacturer) |
| **Bore x Stroke** | 35mm x 26mm | Oversquare design (better for high RPM) |
| **Weight** | 880g (31 oz / 1.94 lbs) | Light for the power |
| **Fuel Type** | Gasoline + 2-stroke oil | 25:1 or 30:1 mix typical |
| **Ignition** | Electronic CDI | Spark plug, no glow plug needed |
| **Starter** | Electric or pull-start | Electric start recommended for UAV |
| **RPM Range** | 1,500-9,000 RPM | Typical for RC engine |
| **Propeller Range** | 18x8 to 22x10 | Diameter x Pitch in inches |
| **Cost** | ~$400-$500 | Competitive pricing |

---

## Suitability for Phase 2 ISR Drone

### Target Aircraft: Aerosonde-Class UAV

**Design Requirements:**
- **Takeoff Weight:** 40-50 lbs (18-23 kg)
- **Endurance:** 8-12 hours
- **Cruise Speed:** 35-50 mph (60-80 km/h)
- **Power Required:** 2-4 HP

### Power Analysis

#### 1. Power-to-Weight Ratio

**NGH GT25:**
- Power: 2.5-3.0 HP
- Weight: 1.94 lbs (0.88 kg)
- **Specific Power:** 1.29-1.55 HP/lb (2.84-3.41 HP/kg)

**Comparison to Aerosonde:**
- Aerosonde uses ~3.5 HP engine
- NGH GT25 at 2.5-3 HP is **slightly underpowered** for 50 lb aircraft
- **Verdict:** Suitable for 35-45 lb aircraft, marginal for 50 lb

**Recommendation:** 
- For 40-45 lb design: **NGH GT25 is adequate**
- For 50 lb design: Consider **NGH GT35** (35cc, ~4 HP) or **DLE 30** (30cc, 3.5 HP)

---

#### 2. Fuel Consumption and Endurance

**Typical 2-Stroke Consumption:**
- 2-stroke engines: ~0.5-0.7 lb fuel per HP per hour
- NGH GT25 at 2.5 HP: ~1.25-1.75 lbs/hour at full power
- At cruise (50-60% power): ~0.75-1.0 lbs/hour

**Fuel Weight for 10-Hour Mission:**
- 10 hours @ 0.85 lb/hr = **8.5 lbs fuel**
- Fuel density (gasoline): ~6 lb/gallon
- **Fuel volume:** 8.5 lb / 6 lb/gal = **1.42 gallons**

**Fuel Tank Sizing:**
- Tank capacity: 1.5-2.0 gallons (safety margin + reserves)
- Tank weight (empty): 1-2 lbs (aluminum or composite)
- **Total fuel system weight:** 10-12 lbs (fuel + tank + lines)

**Impact on Design:**
- Fuel = 20-25% of takeoff weight (typical for long-endurance UAV)
- Reduces payload capacity
- But enables 10+ hour flights (vs. 2-4 hours electric)

---

#### 3. Cruise Performance Estimate

**Power Required for Cruise:**

Using simplified drag equation:
- P_required = D * V / η_prop
- D = 0.5 * ρ * V² * S * CD

**Assumptions:**
- Cruise speed: V = 45 mph (20 m/s)
- Wing area: S = 1.2 m² (13 ft²)
- Drag coefficient: CD = 0.035 (clean design, L/D ~15)
- Air density: ρ = 1.225 kg/m³ (sea level)
- Propeller efficiency: η_prop = 0.75

**Calculation:**
- Drag: D = 0.5 * 1.225 * 20² * 1.2 * 0.035 = **10.3 N** (2.3 lbs)
- Power: P = 10.3 * 20 / 0.75 = **274 W** (0.37 HP)

**Required Cruise Power:** ~0.4 HP (15-20% of max power)

**Engine Operating Point:**
- NGH GT25 at 15-20% throttle: ~1,500-2,500 RPM
- Fuel consumption: ~0.6-0.8 lb/hr
- **Endurance:** 8.5 lb fuel / 0.7 lb/hr = **12 hours**

**Verdict:** NGH GT25 is **well-suited** for 10-12 hour endurance missions

---

### Pros of NGH GT25 for UAV Application

1. **Good Power-to-Weight:**
   - 1.94 lbs for 2.5-3 HP is excellent
   - Lighter than many competitors

2. **Electronic Ignition:**
   - CDI ignition = reliable starting
   - No glow plug = simpler fuel (gasoline only)
   - More consistent performance

3. **Wide RPM Range:**
   - Can run slow (1,500 RPM loiter) or fast (9,000 RPM climb)
   - Important for variable mission profiles

4. **Cost-Effective:**
   - $400-500 is reasonable for this power class
   - Less than half the cost of "UAV-specific" engines

5. **Proven in RC:**
   - NGH engines are well-regarded in RC community
   - Reliability reports generally positive

6. **Gasoline Fuel:**
   - Gasoline is cheaper and safer than glow fuel
   - Easier to transport (no nitromethane)
   - Longer shelf life

---

### Cons of NGH GT25 for UAV Application

1. **RC Engine, Not UAV-Optimized:**
   - Designed for hobbyist use, not 24/7 commercial ops
   - May require modifications for reliability:
     - Dual ignition (redundancy)
     - Improved carburetor (fuel injection?)
     - Enhanced cooling
     - Vibration isolation

2. **Vibration:**
   - Single-cylinder 2-stroke = significant vibration
   - Requires careful engine mounting
   - Can affect autopilot sensors (IMU) and cameras
   - Mitigation: Rubber mounts, balanced propeller, vibration dampers

3. **Noise:**
   - 2-stroke engines are loud (~90-100 dB)
   - Not ideal for covert ISR missions
   - May require muffler (adds weight, reduces power)

4. **Maintenance:**
   - 2-stroke needs oil mix in fuel
   - Spark plug replacement (every 20-50 hours)
   - Carburetor tuning (altitude, temperature changes)
   - More maintenance than electric

5. **Cold Starting:**
   - Can be difficult to start in cold weather
   - May need glow plug assist or preheating
   - Electric start helps but adds weight/complexity

6. **Fuel System Complexity:**
   - Fuel tank, lines, filter, carburetor
   - More failure modes than battery+ESC
   - Fuel sloshing in turns (needs baffled tank)

---

## Comparison to Alternative Engines

### Option 1: DLE 30 (30cc, 3.5 HP)

| Parameter | NGH GT25 | DLE 30 | Advantage |
|-----------|----------|--------|-----------|
| **Displacement** | 25cc | 30cc | DLE 30 |
| **Power** | 2.5-3.0 HP | 3.5 HP | **DLE 30** (16% more) |
| **Weight** | 1.94 lbs | 2.42 lbs | **NGH GT25** (20% lighter) |
| **Cost** | $400-500 | $350-450 | DLE 30 (cheaper) |
| **Reliability** | Good | **Excellent** (industry standard) | **DLE 30** |

**Verdict:** DLE 30 is **more proven** for UAV use, but heavier

---

### Option 2: Zenoah G38 (38cc, 3.8 HP)

| Parameter | NGH GT25 | Zenoah G38 | Advantage |
|-----------|----------|------------|-----------|
| **Displacement** | 25cc | 38cc | Zenoah |
| **Power** | 2.5-3.0 HP | 3.8 HP | **Zenoah** (27% more) |
| **Weight** | 1.94 lbs | 3.08 lbs | **NGH GT25** (37% lighter) |
| **Cost** | $400-500 | $550-700 | **NGH GT25** (cheaper) |
| **Reliability** | Good | **Excellent** (used in commercial UAVs) | **Zenoah** |

**Verdict:** Zenoah is **most reliable**, used in Aerosonde and similar UAVs, but heavy and expensive

---

### Option 3: Custom Wankel Rotary (e.g., UAV Engines AR741)

| Parameter | NGH GT25 | AR741 Rotary | Advantage |
|-----------|----------|--------------|-----------|
| **Power** | 2.5-3.0 HP | 7.4 HP | Rotary (2.5x more) |
| **Weight** | 1.94 lbs | 4.4 lbs | **NGH GT25** (56% lighter) |
| **Vibration** | High (single cyl.) | **Low** (balanced rotary) | **Rotary** |
| **Cost** | $400-500 | **$3,500-5,000** | **NGH GT25** (8-10x cheaper!) |
| **Fuel Consumption** | 0.7 lb/hr cruise | 1.2 lb/hr | **NGH GT25** (40% better) |

**Verdict:** Rotary is **smoother and more powerful**, but **very expensive** and **thirsty**

---

## Recommendation Matrix

| Aircraft Weight | Endurance Goal | Recommended Engine | Cost | Notes |
|-----------------|----------------|-------------------|------|-------|
| **35-40 lbs** | 8-10 hours | **NGH GT25** | $400-500 | Best power/weight, adequate power |
| **40-45 lbs** | 10-12 hours | **NGH GT25** or DLE 30 | $400-500 | NGH marginal, DLE safer choice |
| **45-50 lbs** | 10-12 hours | **DLE 30** or Zenoah G38 | $450-700 | Need more power |
| **50+ lbs** | 12+ hours | **Zenoah G38** or custom | $700+ | Commercial UAV territory |

---

## Design Integration for Phase 2 Drone

### Engine Mount Design

**Requirements:**
- **Vibration Isolation:** 
  - Rubber mounts (Lord Mounts or similar)
  - Isolation frequency: <10 Hz (below engine firing frequency)
  
- **Cooling Airflow:**
  - Pusher configuration: air flows over cylinder head
  - Cowl with cooling baffles
  - Temperature monitoring (CHT sensor)

- **Accessibility:**
  - Easy access for spark plug changes
  - Removable cowl for maintenance

**Materials:**
- Engine mount: Aluminum or G10 fiberglass
- Firewall: Aluminum or steel (heat protection)

---

### Fuel System Design

**Components:**

1. **Fuel Tank:**
   - Capacity: 1.5-2.0 gallons (6-8 liters)
   - Material: Aluminum or composite (Kevlar-wrapped)
   - Features: Baffles (prevent sloshing), vent, fuel pickup

2. **Fuel Lines:**
   - Fuel-rated silicone or Tygon
   - Diameter: 1/4" (6mm)
   - Clamps: Zip ties or hose clamps

3. **Fuel Filter:**
   - Inline filter (10-40 micron)
   - Prevents debris from clogging carburetor

4. **Carburetor:**
   - Stock NGH carburetor (Walbro-style)
   - Consider upgrade: Fuel injection for altitude compensation (expensive)

5. **Fuel Pump (Optional):**
   - For inverted flight or acrobatics (not needed for ISR)
   - Gravity feed sufficient for level flight

**Weight Budget:**
- Fuel (full): 9-10 lbs
- Tank: 1.5 lbs
- Lines/filter/misc: 0.5 lbs
- **Total:** 11-12 lbs

---

### Propeller Selection

**NGH GT25 Propeller Recommendations:**

**Manufacturer Suggested:**
- 18x8 to 22x10 (Diameter x Pitch in inches)

**For Long Endurance (ISR Mission):**
- **Larger diameter, lower pitch** = better efficiency
- **Recommendation:** 20x8 or 22x8
  - 20-22" diameter: High thrust at low speed
  - 8" pitch: Low RPM cruise, quiet, efficient

**Material:**
- **Wood:** Beechwood propellers (cheap, $30-50)
- **Composite:** Carbon fiber (expensive, $100-200, more durable)

**Balancing:**
- Critical for reducing vibration
- Use prop balancer tool
- Target: <0.1g imbalance

---

### Ignition System Redundancy

**Single Point of Failure Risk:**
- Stock NGH GT25 has single CDI ignition
- If ignition fails → engine quits → loss of aircraft

**Mitigation Options:**

**Option 1: Dual Ignition (Complex)**
- Add second spark plug, second CDI
- Requires machining cylinder head
- Cost: $200-300 + labor
- Used in certified aircraft (Rotax 912, Lycoming, etc.)

**Option 2: Backup Battery for CDI**
- Ensure CDI has power even if main battery fails
- Separate battery or redundant BEC
- Cost: $50-100
- Simpler than dual ignition

**Option 3: Parachute Recovery**
- If engine fails, deploy parachute
- Save aircraft for inspection/repair
- Cost: $200-500 (parachute system)

**Recommendation:** **Option 2 (backup battery) + Option 3 (parachute)**
- Provides electrical redundancy
- Parachute is good practice for UAV anyway (safe recovery)

---

## Performance Estimates with NGH GT25

### Phase 2 Drone Configuration

**Assumptions:**
- Wingspan: 4.0 m (13 ft)
- Wing area: 1.2 m² (13 ft²)
- Takeoff weight: 42 lbs (19 kg)
  - Empty weight: 30 lbs
  - Fuel: 10 lbs
  - Payload: 2 lbs (camera)
- Engine: NGH GT25 (2.5 HP)
- Propeller: 20x8
- L/D: 15 (moderate efficiency)

### Endurance Calculation

**Cruise Power Required:**
- As calculated earlier: ~0.4 HP @ 45 mph

**Fuel Consumption:**
- At 16% throttle (0.4 HP): ~0.6 lb/hr

**Fuel Available:**
- 10 lbs (with reserve: 9 lbs usable)

**Endurance:**
- 9 lbs / 0.6 lb/hr = **15 hours** (ideal, no wind)
- With 15 mph headwind (worst case): ~10-12 hours
- **Target mission: 10 hours = achievable**

### Range Calculation

**At Cruise:**
- Speed: 45 mph (72 km/h)
- Endurance: 12 hours (conservative)
- **Range:** 45 mph * 12 hr = **540 miles** (870 km)

**Operational Radius:**
- With 20% reserve: 540 * 0.8 = 432 miles
- Out-and-back: 432 / 2 = **216 miles** (348 km)

**Maritime ISR Mission:**
- Patrol area: 100 km offshore
- Loiter: 6-8 hours on station
- Return: 100 km
- **Total mission:** 10-12 hours ✓

---

## Cost Analysis

### Engine and Propulsion System

| Component | Cost | Notes |
|-----------|------|-------|
| NGH GT25 Engine | $450 | From Motion RC |
| Electric Starter | $80 | Optional (hand-start alternative) |
| Propeller (20x8 wood) | $40 | Multiple spares recommended |
| Fuel Tank (2 gal aluminum) | $150 | Custom fabricated or off-shelf |
| Fuel Lines, Filter, Clamps | $50 | Misc hardware |
| Engine Mount (aluminum) | $100 | Custom fabricated |
| Vibration Isolators | $80 | Lord Mounts or equivalent |
| Exhaust/Muffler | $60 | Reduce noise |
| **Subtotal** | **$1,010** | Complete propulsion system |

### Comparison to Electric

**Electric Equivalent (10-hour endurance):**

| Component | Cost | Notes |
|-----------|------|-------|
| Motor (outrunner, 1500W) | $200 | |
| ESC (60A) | $100 | |
| Batteries (6S 30,000 mAh x3) | $900 | 3 large packs for 10 hours |
| **Subtotal** | **$1,200** | |

**Verdict:**
- NGH GT25 system: **$1,010**
- Electric 10-hour system: **$1,200**
- **Gasoline is cheaper** for long endurance
- But electric is quieter, simpler, less maintenance

---

## Testing and Validation Plan

### Bench Testing (Before Integration)

1. **Break-In:**
   - Run engine on test stand
   - 10-20 tanks of fuel at varying throttle
   - Monitor: Temperature, RPM, fuel consumption

2. **Propeller Testing:**
   - Test multiple propeller sizes
   - Measure: Thrust, RPM, current (electric starter)
   - Select optimal prop for cruise efficiency

3. **Vibration Measurement:**
   - Mount engine with accelerometer
   - Measure vibration at various RPM
   - Tune engine mounts to minimize transmission

4. **Fuel Consumption:**
   - Run at cruise throttle (15-20%)
   - Measure fuel consumed over 1-2 hours
   - Validate endurance predictions

### Flight Testing (After Integration)

1. **First Flights:**
   - Short flights (5-10 min)
   - Validate engine reliability, cooling, mixture

2. **Endurance Tests:**
   - Incremental: 1 hour, 2 hours, 4 hours, 8 hours, 10+ hours
   - Monitor: Fuel consumption, engine temperature, oil leakage

3. **Performance Validation:**
   - Measure: Cruise speed, climb rate, fuel burn
   - Compare to predictions
   - Optimize propeller and mixture settings

---

## Conclusion

### NGH GT25 Overall Assessment

**Suitability for Phase 2 ISR Drone: 8/10**

**Strengths:**
- Good power-to-weight ratio (1.29-1.55 HP/lb)
- Affordable ($450)
- Proven in RC community
- Adequate power for 35-45 lb aircraft
- Excellent fuel efficiency at cruise (12+ hour endurance possible)

**Weaknesses:**
- Vibration (single-cylinder 2-stroke)
- Not UAV-optimized (hobbyist design)
- Requires maintenance (spark plugs, carburetor tuning)
- Noise (90-100 dB)

**Recommendation:**
- **Use NGH GT25 for Phase 2 if:**
  - Aircraft weight ≤ 45 lbs
  - Budget is limited (<$1,000 for propulsion)
  - Willing to accept vibration and maintenance

- **Consider DLE 30 or Zenoah G38 if:**
  - Aircraft weight > 45 lbs
  - Need higher reliability (commercial operations)
  - Can afford $600-800 for engine system

---

**Next Steps:**

1. **Purchase NGH GT25** ($450 from Motion RC)
2. **Bench test** (break-in, prop selection, fuel consumption)
3. **Design engine mount** (vibration isolation)
4. **Integrate into Phase 2 airframe** (once OpenVSP design complete)
5. **Flight test** (validate 10+ hour endurance)

---

**Document Prepared:** January 8, 2026  
**Engine:** NGH GT25 25cc Two-Stroke  
**Application:** Phase 2 ISR Drone (Aerosonde-class)  
**Verdict:** **Recommended for 35-45 lb designs**
