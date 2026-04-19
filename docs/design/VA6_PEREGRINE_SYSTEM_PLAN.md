# VA-6 "Peregrine" — Interceptor Drone System Architecture

**Date:** 2026-03-21
**Status:** Design Phase — OpenVSP modeling first
**Classification:** UNCLASSIFIED

---

## Context

Ukraine needs a cheap, mass-producible counter-UAS system to kill Shahed-136 one-way attack drones. Current solutions (IRIS-T at $430K/shot, Gepard at $7K/round) are economically unsustainable against $20-50K shaheed drones arriving in salvos of 10-50. The VA-6 targets **$1,000/interceptor, $2,000/engagement** — a 200x cost advantage over IRIS-T.

Reference platform: SkyFall P1-SUN — 3D-printed modular interceptor, quad motors on cruciform tail tips, 450 km/h max, $1,000 unit cost, battle-proven in Ukraine since 2025.

## System Architecture (4 Subsystems)

### 1. SkyWatch — Passive Detection Grid (Pixel-to-Voxel Volumetric Detection)

**Core concept**: Adapted from [PixelToVoxelProjector](https://github.com/ConsistentlyInconsistentYT/Pixeltovoxelprojector). Multiple ground cameras cast rays into a shared 3D voxel grid. After background subtraction (sky texture), brightness accumulates only where rays from 2+ cameras intersect — giving **3D position from cheap 2D cameras** without stereo calibration.

**How it works for drone detection:**
1. Each camera node builds a "sky background texture" over time
2. Frame differencing against this background isolates moving bright pixels (drone, not cloud)
3. For each bright pixel, cast a ray from camera position through 3D voxel space
4. Where rays from multiple cameras intersect at high brightness = **real target in 3D**
5. Voxel grid resolution determines position accuracy (~50-100m at 2-5 km range)
6. Background subtraction eliminates stars, planets, aircraft lights (project to infinity, not into local voxel grid)

**Per node (~$500-600):**
- Wide-angle camera: Sony IMX477 + 120-180 deg fisheye lens, 10 fps
- Acoustic array: 4x MEMS mics (INMP441), GCC-PHAT bearing estimation, 3-5 km detection
- Thermal: FLIR Lepton 3.5 (160x120 LWIR), hot exhaust against cold sky
- Processor: Raspberry Pi 5
- Comms: LoRa 868 MHz (2 Hz bearing reports)
- Power: 12V 50Ah LiFePO4 + 50W solar (7-10 day autonomy)

**Grid**: 5 nodes = 10 km fence. Minimum 3 nodes with overlapping FOV for voxel triangulation.

### 2. Raptor Controller — Battle Management System

Ruggedized laptop at launcher site.
- Track fusion: Triangulate from 2+ node bearings, Kalman filter smoothing
- Classification: Velocity gate (150-220 km/h), heading persistence, acoustic signature match
- Intercept calculator: Computes optimal launch time, engagement geometry, waypoints
- Launch decision: Auto-recommend at confidence >0.8, human confirms (or full-auto in mass attack)
- Salvo doctrine: 2 interceptors per target (96%+ Pk)

### 3. VA-6 Interceptor Vehicle (P1-SUN Class)

### Vehicle Specifications (v13)

| Parameter | VA-6 Design | P1-SUN Reference |
|-----------|-------------|------------------|
| Length | 680mm | ~800-1000mm |
| Fuselage diameter | 140mm | ~120-140mm est |
| Tail span (tip-to-tip) | ~460mm (cruciform) | Similar |
| MTOW | 2.91 kg (analyzed) | ~5-8 kg estimated |
| Payload (warhead only) | 0.8 kg | 0.8 kg |
| Max speed | 300 km/h (design) / 450 km/h (stretch) | 450 km/h |
| Cruise | 250 km/h | 300 km/h |
| Endurance (250 km/h) | 16 min | 14-17 min |
| Endurance (180 km/h loiter) | 35 min | — |
| Ceiling | 5 km | 5 km |

### Aerodynamic Design (Analyzed)

**Nose**: Von Karman profile, 120mm long, 30mm seeker window tip. Optimized for minimum pressure drag at subsonic speed.

**Body**: Constant 140mm diameter cylindrical section. Dominates drag (69% of total wetted area).

**Tail**: Optimized boat-tail, 150mm taper to 40mm end diameter (~8° half-angle). Biggest drag reduction vs blunt tail.

**Cruciform fins**: 4x rectangular fins, 160mm span × 80mm chord, NACA 0008 (8% t/c).
- AR = 2.0 (low, resists stall to ~22°)
- Provides stability (17.4% static margin) + 2-3G aerodynamic maneuvering
- Motors provide additional attitude control via differential thrust (18.9 Nm moment)
- No sweep needed at Mach 0.2
- 5mm root fillets recommended for junction drag reduction

**Motor pods**: 4x at fin tips, 32mm diameter × 90mm long, pointed nose cone. Rear aligns with fin trailing edge.

**Total drag at cruise (250 km/h)**: ~4.8 N (optimized from 6.3 N, 24% reduction)

### Propulsion (Analyzed)

**Motors**: 4x 2207 2750KV (~28mm diameter, ~28g each) — standard FPV race motor, widely available
**Props**: 4x 5x4" off-the-shelf (e.g., HQProp 5040, Gemfan 5040, DAL 5x4) — ~$2/prop
- Loiter efficiency: 70% at 180 km/h
- Cruise efficiency: 75% at 250 km/h
- Sprint efficiency: 80% at 300 km/h
- Static thrust: 3.7 kgf per motor (14.8 kgf total)
- **T/W = 5.1** (well above 1.2 requirement for vertical launch)

**Battery**: 6S 5000mAh LiPo (89 Wh usable)

**Differential thrust**: 4 motors provide pitch/yaw/roll control independent of airspeed. Critical for vertical launch when fins have no authority.

### Performance Summary (Analyzed)

| Condition | Drag | Prop Efficiency | Shaft Power | Endurance |
|-----------|------|-----------------|-------------|-----------|
| Loiter 180 km/h | 1.8 N | 70% | 129 W | **41 min** |
| Cruise 250 km/h | 4.0 N | 75% | 371 W | **14.5 min** |
| Sprint 300 km/h | 5.1 N | 80% | 531 W | **10 min** |

**Mission profile** (10s vertical launch + 30s sprint + loiter at 180): **38 min total**

### Stability (Analyzed)

- CG: 338mm from nose (52% of body length)
- AC: 451mm from nose (69% of body length)
- **Static margin: 17.4%** — very stable (dart configuration)
- Battery position not critical (SM stays >15% anywhere from 300-450mm)

### Structural (Analyzed)

- **Fuselage**: 3mm PETG wall, safety factor 753x at 3G launch — massively overbuilt (can thin walls to save weight)
- **Fins**: NACA 0008, safety factor 2.0x at 10G — marginal for extreme maneuvers, adequate for 3G intercept corrections. Carbon fiber spar recommended for production.
- **Motor mounts**: M3 bolts + loctite or bonded carbon plate, 36.8 N design load
- **Terminal impact**: 26,427 J kinetic energy at head-on closing speed (5x shotgun slug)

### Mass Budget (Analyzed)

| Category | Component | Weight | Cost |
|----------|-----------|--------|------|
| **PAYLOAD** | Fragmentation sleeve (steel cubes + pyro charge) | 650g | $50 |
| | Proximity fuze (CDM324 24GHz radar) | 10g | $5 |
| | Contact fuze (piezoelectric backup) | 5g | $2 |
| | Safe/arm mechanism + wiring | 35g | $15 |
| | Warhead casing | 100g | $10 |
| | **Payload subtotal** | **800g** | **$82** |
| **AVIONICS** | Flight controller (F405) + GPS + IMU | 15g | $55 |
| | Seeker processor (Pi 5 + Hailo-8L NPU) | 55g | $85 |
| | FLIR Lepton 3.5 + lens mount | 15g | $200 |
| | Visible camera (OV5647) | 5g | $10 |
| | LoRa radio module | 5g | $8 |
| | Avionics battery (2S 500mAh) | 30g | $8 |
| | Wiring + connectors | 20g | $10 |
| | **Avionics subtotal** | **145g** | **$376** |
| **PROPULSION** | 4x 2207 2750KV motors (~28g each) | 112g | $40 |
| | 4x 30A ESCs | 80g | $40 |
| | 4x 5x4" props (off-the-shelf) | 30g | $8 |
| | **Propulsion subtotal** | **222g** | **$88** |
| **POWER** | 6S 5000mAh LiPo | 650g | $60 |
| **AIRFRAME** | 3D-printed fuselage + cruciform tail | 900g | $40 |
| | Motor mounts + hardware | 100g | $15 |
| | **Airframe subtotal** | **1000g** | **$55** |
| | **Margin** | 93g | — |
| **TOTAL** | | **2,910g (2.91 kg)** | **~$673** |

**Launch**: Vertical (motor-powered, T/W 5.75) or pneumatic/bungee rail catapult at 30°.

---

## AI Subsystems

### AI Terminal Guidance (Onboard Seeker)

**Tier 1 — Classical CV (baseline, deploy first):**
- LWIR centroid tracker (blob detect + PID) → proportional navigation
- Frame differencing on visible camera as backup
- No ML model needed. This is what works in Ukraine today.
- Hardware: FLIR Lepton 3.5 + Pi Zero 2W ($230, 30g)

**Tier 2 — Neural Target Classifier (add after Tier 1 proven):**
- YOLOv8-nano or YOLOv10-nano (~2MB model) trained on Shahed-136 silhouettes (IR + visible, multiple angles)
- Classifies: shahed vs bird vs aircraft vs decoy vs helicopter
- Prevents wasting interceptors on false targets
- Hardware upgrade: Pi 5 + Hailo-8L NPU (13 TOPS, $85, 55g) — runs YOLO at 30+ fps
- Training data: Synthetic renders of Shahed models in various conditions + field recordings

**Tier 3 — Multi-Modal Fusion Seeker:**
- Fuses LWIR thermal + visible camera + acoustic mic on interceptor nose
- Neural network produces robust target classification even when single sensors degrade (fog/flares/wind)
- Same hardware as Tier 2 + additional sensors (~$280, 50g)

### AI Flight Control

**Tier 1 — Waypoint Autopilot (baseline):**
- ArduPilot or iNav on STM32 flight controller
- BMS uploads waypoints, interceptor follows
- Classical PID loops for attitude stabilization
- Proven, reliable, $30 hardware

**Tier 2 — Adaptive Terminal Maneuver:**
- Classical PN guidance for mid-course
- At <200m from target, switch to ML-trained aggressive maneuver policy
- Trained in simulation (JSBSim or custom 6-DOF) on thousands of terminal engagements
- Accounts for propeller wash, aerodynamic coupling, sensor lag, wind gusts
- Small model (~500KB ONNX), runs directly on flight controller MCU
- Advantage: Handles edge cases that classical PN misses (crossing shots, diving targets, last-second corrections)

**Tier 3 — Full Reinforcement Learning Pursuit:**
- End-to-end RL policy: seeker input → motor commands
- Trained in simulation against both non-maneuvering (current Shahed) AND maneuvering targets (future threats)
- Deploy as ONNX on Pi 5 / Hailo NPU
- Risk: Sim-to-real gap requires extensive hardware-in-the-loop testing
- Payoff: Adapts to targets that evade, maneuver, or deploy countermeasures

### AI Decision Logic (Autonomous Engagement)

**Tier 1 — Rule-Based (safest, deploy first):**
```
IF seeker_locked AND target_classified_as_shahed AND range < 500m:
    ARM warhead, ENGAGE via PN guidance
ELIF seeker_locked AND target_unclassified:
    REQUEST human confirmation (fiber video or LoRa command)
ELIF datalink_lost AND seeker_locked AND velocity_in_gate:
    ENGAGE autonomously (pre-authorized ROE)
ELSE:
    CONTINUE mid-course, keep searching
```
Simple, auditable, predictable. Human-in-the-loop for ambiguous targets.

**Tier 2 — Threat Scoring Network:**
- Input: thermal signature, target size, speed, heading, acoustic match, altitude, time-of-day
- Output: threat probability (0-1) + target class
- Auto-engage threshold: >0.95 threat score
- Below threshold: human decides via fiber/LoRa
- Critical for mass attacks: When 20+ targets come simultaneously, human cannot decide for each. AI auto-engages high-confidence, flags ambiguous.

**Tier 3 — Cooperative Swarm Logic:**
- Multiple VA-6s share target data via LoRa mesh network
- Distributed task allocation: each interceptor claims a target, avoids duplication
- If one seeker fails, nearest neighbor redirects
- Consensus: 2+ interceptors must agree on target identity before engagement
- Transforms individual interceptors into coordinated defense system

### Ground-Side AI (BMS Intelligence)

**Track Classification:**
- Train on voxel grid time-series data
- Classify tracks: shahed / civilian aircraft / helicopter / bird flock / weather
- Uses trajectory shape (shaheds fly straight GPS), speed profile, thermal signature
- Reduces false launch rate

**Intercept Optimizer:**
- Multiple targets + limited interceptors → optimal assignment
- Considers: target priority (proximity to defended asset), interceptor battery state, engagement geometry
- Linear programming or greedy heuristic for real-time allocation

**Post-Engagement Learning Loop:**
- Log every engagement: seeker video, flight telemetry, voxel tracks, kill/miss outcome
- After-action analysis identifies failure modes
- Retrain classifiers with real engagement data
- Continuous improvement cycle — each engagement makes the system smarter

### 4. Communications

**Option A: LoRa Radio (default)**
- Nodes to BMS: LoRa 868 MHz, bearing reports at 2 Hz
- BMS to Interceptor: LoRa 868/915 MHz, waypoints + mid-course corrections
- Interceptor to BMS: GPS position, speed, seeker status at 2-5 Hz
- Datalink lost: interceptor continues autonomously, activates seeker at pre-programmed point
- Pros: Wireless, simple, no tether constraints on flight path
- Cons: Jammable (Russian EW capability is significant), latency, limited bandwidth

**Option B: Fiber Optic Data Link (FODL)**
- Lightweight single-mode fiber spool on interceptor, pays out during flight
- Fiber: 125um cladding, ~0.4 g/m weight. 10 km spool = ~4 kg (significant weight penalty)
- Alternative: Ultra-thin 80um fiber at ~0.15 g/m. 10 km = ~1.5 kg (more feasible)
- Bandwidth: Effectively unlimited (Gbps) — can stream full seeker video back to BMS for human-in-the-loop terminal guidance
- Latency: Near-zero (<1ms round trip)
- EW immunity: **Complete** — fiber is unjammable, undetectable, no RF emissions
- BMS operator can directly control terminal engagement via live seeker feed
- Spool design: Stationary spool at launcher (fiber pays out from the back of the spool), or onboard spool (interceptor carries and pays out). Stationary spool is simpler — fiber unwinds as interceptor flies away.
- Break detection: If fiber breaks (maneuver too sharp, obstacle), interceptor falls back to autonomous seeker mode (same as LoRa datalink-lost behavior)
- Pros: Jam-proof, zero-latency, full video bandwidth, enables human-in-the-loop kill decision
- Cons: Weight penalty (~1.5-4 kg depending on fiber), constrains max range to spool length, fiber can break on sharp maneuvers, adds mechanical complexity

**Recommended**: Both options available as modular variants:
- **VA-6R** (Radio): LoRa datalink, fully autonomous terminal phase, lighter weight, longer range
- **VA-6F** (Fiber): FODL, human-in-the-loop terminal guidance via live seeker video, jam-proof, shorter effective range (~5-8 km limited by spool + weight penalty)
- Decision based on threat environment: high-EW → fiber; low-EW → radio; mixed → launch both

## Kill Chain Timeline (~60 seconds)

```
T+0:00  Acoustic array detects Shahed at 4 km
T+0:02  Second node confirms; BMS triangulates via voxel grid
T+0:05  BMS recommends launch
T+0:08  Operator confirms
T+0:10  Interceptor 1 launches
T+0:15  Interceptor 2 launches (salvo)
T+0:30  Mid-course correction uplinked
T+0:45  LWIR seeker activated, acquires target at ~2 km
T+0:50  Seeker locked, proportional navigation
T+0:55  Proximity fuze triggers — KILL
T+0:57  Kill assessment (simultaneous loss of target track + interceptor telemetry)
```

## Cost Summary

| Item | Cost |
|------|------|
| Per interceptor | ~$1,000 |
| Per engagement (salvo of 2) | ~$2,000 |
| Ground system (5 nodes + BMS + launcher) | ~$4,500 |
| Full battery (ground + 12 interceptors) | ~$16,500 |
| vs Shahed ($20-50K) | 10-25x cheaper |
| vs IRIS-T ($430K) | 200x cheaper |

## System of Systems Test Plan

### Level 1: Component Tests (bench/lab)

**1.1 Voxel Detection Pipeline**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Frame differencing accuracy | Synthetic video: moving dot on static sky | Detection rate >95%, false alarm <1/min |
| Background model convergence | 60s static sky feed, insert target | Target isolated with SNR >10 dB |
| Ray projection accuracy | Known camera position, inject bright pixel at known angle | Voxel position error <1 deg angular |
| Multi-camera voxel triangulation | 3 cameras, synthetic target at known 3D point | 3D position error <100m at 3 km |
| Voxel velocity estimation | Moving target across 10 frames | Velocity error <20% |
| Thermal blob detection | FLIR Lepton at heat source, varying distances | Detection to 500m |
| Day/night optical performance | Camera + frame diff at noon, dusk, night | Characterize detection range vs lighting |

**1.2 Acoustic Detection**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| GCC-PHAT bearing accuracy | 4-mic array, known speaker position | Bearing error <5 deg |
| Shahed signature matching | Recorded engine audio through speaker | Matched filter correlation >0.7 at 200m |
| Wind noise rejection | Test at 0, 10, 20, 30 km/h wind | Characterize max wind for detection |
| Range characterization | Speaker at 100m to 5km | Determine reliable detection range |

**1.3 Interceptor Propulsion**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Static thrust per motor | Thrust stand, sweep throttle | >1.5 kg thrust per motor at 100% |
| Combined thrust (4 motors) | Full cruciform tail on stand | >6 kg total (>1:1 T/W) |
| Current draw / efficiency | Log amps at cruise (~60-70%) | Confirm 14-17 min endurance |
| Thermal runaway test | Full throttle 2 min, monitor temps | No component exceeds rated temp |
| Differential thrust control | Command pitch/yaw via motor differential | Controllable moments in all axes |

**1.4 Airframe**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| 3D print structural test | Apply 5G load (30-35 kg) | No failure at 5G |
| Vibration test | Shaker at motor RPM, 30 min | No cracks, no loosening |
| Assembly time | Full assembly from boxed components | <30 min by trained operator |
| Crash survivability | Drop from 2m onto concrete | Avionics bay survives |

**1.5 Seeker**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| LWIR acquisition range | Heat source at 100m to 2km | Reliable at >1 km |
| Centroid tracking accuracy | Moving heat source on rail | Error <3 pixels at 500m |
| Processing latency | Measure full pipeline | <50ms image to guidance command |
| FOV tradeoff | Test 25 vs 50 deg lenses | Select optimal for 1-2 km with <5m CEP |

**1.6 Kill Mechanism**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Proximity fuze trigger distance | CDM324, approach at various speeds | Reliable at 3-5m |
| Fragmentation pattern | Static test (EOD supervised) | >50% fragments in 15 deg forward cone |
| Contact fuze reliability | Drop-test piezo at impact velocities | 100% trigger at >50 km/h |
| Safe/arm sequencing | Verify arm conditions | No arm on ground; reliable arm in flight |

**1.7 Communications**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| LoRa range ground-ground | 1, 5, 10, 15 km | Reliable 2 Hz at 10 km |
| LoRa range air-ground | Balloon at 500m alt | Reliable at 15+ km |
| Packet loss | 10-min at max range | <5% loss |
| Latency | Round-trip command/telemetry | <200ms |

### Level 2: Subsystem Integration Tests

**2.1 Detection to BMS**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Multi-node track formation | 3+ nodes, RC aircraft at 1-3 km | Track within 5s |
| 3D position accuracy | GPS on target vs voxel estimate | <200m 3D error at 3 km |
| Track velocity accuracy | RC at known speed | Error <15% |
| False track rate | 1-hour, no target | <0.5/hour |
| Acoustic to optical handoff | Acoustic first, optical confirms | Confirmation within 3s |

**2.2 BMS to Interceptor**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Launch sequence timing | Full detect-compute-launch | <10s from track to launch command |
| Waypoint upload | Compute + upload to interceptor | Received in <2s |
| Mid-course correction | Update during flight | Correction within 3s |
| Telemetry reception | Position, speed, seeker status | 2-5 Hz continuous |

**2.3 Interceptor Flight**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Catapult launch | Rail launch, verify stable flight | No tumble, positive climb in 3s |
| Cruise performance | 5 km leg | 250+ km/h at <70% throttle |
| Max speed | Full throttle dash | 300+ km/h |
| Endurance | Fly to battery cutoff | >14 min |
| Ceiling | Climb to 5 km | Controllable at altitude |

**2.4 Terminal Phase**

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Seeker acquisition in flight | Fly at towed IR target | Lock at >500m |
| PN guidance tracking | Locked seeker, verify steering | Smooth pursuit |
| Miss distance (inert) | Inert flyby of target | <5m miss distance |

### Level 3: Full System (Live Fire)

| Test | Method | Pass Criteria |
|------|--------|---------------|
| End-to-end (inert) | RC target, full SkyWatch-BMS-launch-seeker chain | Chain in <90s, miss <5m |
| Salvo coordination | 2 interceptors at same target | No collision; second re-targets |
| Night engagement | Same at night | Full chain functional |
| Mass attack | 2 RC targets simultaneously | Both engaged within 30s |
| Live warhead static | Ground detonation | Pattern matches design |
| Live warhead air | Fly at target, proximity trigger | Target destroyed |

### Level 4: Operational Testing

| Test | Method | Pass Criteria |
|------|--------|---------------|
| Field deployment | Full battery from vehicle | <4 hours |
| 24-hour endurance | Full system 24 hrs | No failures |
| Operator training | New operator trained + engages | Proficient in 4 hours |
| Reload time | Fresh interceptor on launcher | <60 seconds |
| Rain operation | Moderate rain | Functional with degradation |
| Wind operation | 30+ km/h sustained | Optical/thermal functional |
| Extreme cold | -20 deg C | Battery <20% reduction |

## OpenVSP Design (First Priority)

Build the VA-6 in OpenVSP before any software:

1. **Fuselage**: Dart body, ~100mm diameter, 800-1000mm length, circular cross-sections
2. **Cruciform tail**: 4 fins at 90 deg, each ~200-250mm span, NACA 0008
3. **Motor pods**: 4x nacelle fairings at fin tips
4. **Nose**: Ogive with flat seeker window
5. **Stub wings**: Optional — trade study (more lift vs more drag vs more weight)
6. **Mass properties**: Set CG, run CompGeom
7. **Propeller disks**: Model as actuator disks

**Key questions OpenVSP will answer:**
- Does dart body + cruciform tail produce enough L/D at 300 km/h?
- CG vs aerodynamic center — is it stable?
- Total parasite drag — can 4 motors overcome it?
- Do stub wings help or hurt?

## References
- [SkyFall P1-SUN](https://bavovna.ai/uav/p1-sun/)
- [PixelToVoxelProjector](https://github.com/ConsistentlyInconsistentYT/Pixeltovoxelprojector)
- [Ukrainian Interceptor Drones Guide](https://www.hisutton.com/Ukrainian-Interceptor-Drones.html)
- [P1-SUN at BEDEX 2026](https://www.armyrecognition.com/archives/archives-defense-exhibitions/2026-archives-news-defense-exhibitions/bedex-2026/ukraines-skyfall-positions-p1-sun-drone-interceptor-as-scalable-new-option-for-european-air-defense)
