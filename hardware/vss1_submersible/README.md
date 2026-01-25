# VSS-1 Submersible - Multi-Role Underwater Vehicle

**Type:** Unmanned Underwater Vehicle (UUV) | **Depth Rating:** 200m | **Status:** Concept

## Overview

The VSS-1 is a family of underwater vehicles designed for Gulf of Mexico operations. Three variants cover the full spectrum of underwater missions: close inspection, patrol/search, and long-duration passive monitoring.

### Design Philosophy
- **200m depth rating** - Continental shelf operations
- **Multi-platform deployment** - Shore, VS-1, or manned vessel
- **Common systems** - Shared electronics, comms where possible
- **Modular sensors** - Mission-configurable payloads

---

## Mission Baseline

```
VSS-1 OPERATIONAL CONCEPT

┌─────────────────────────────────────────────────────────────────────────────┐
│  DEPLOYMENT OPTIONS                                                          │
│                                                                              │
│  Shore Launch ───┐                                                           │
│                  │                                                           │
│  VS-1 Picket ────┼──► VSS-1 ──► Mission ──► Recovery ──► Data Offload       │
│                  │                                                           │
│  Manned Vessel ──┘                                                           │
└─────────────────────────────────────────────────────────────────────────────┘

Mission Types:
• VSS-1I: Hull inspection, close visual work, precision maneuvering
• VSS-1P: Area patrol, search patterns, transit between waypoints
• VSS-1S: Long-duration acoustic monitoring, passive surveillance
```

---

## Variant Comparison

| Parameter | VSS-1I (Inspector) | VSS-1P (Patrol) | VSS-1S (Sentry) |
|-----------|-------------------|-----------------|-----------------|
| **Form Factor** | ROV-style (multi-thruster) | Torpedo-style AUV | Glider / Bottom-sitter |
| **Length** | 0.6m | 1.5m | 1.8m (glider) |
| **Weight (air)** | 15-25 kg | 40-60 kg | 50-70 kg |
| **Depth Rating** | 200m | 200m | 200m |
| **Speed (max)** | 3 kts | 4-5 kts | 0.5 kts (glider) |
| **Speed (cruise)** | 1-2 kts | 2-3 kts | 0.3 kts |
| **Endurance** | 4-8 hrs | 12-24 hrs | Weeks-Months |
| **Hover Capability** | ✓ Yes | ✗ No | ✗ No (drift) |
| **Primary Sensors** | HD camera, lights | Side-scan sonar | Hydrophone array |
| **Navigation** | Visual + INS | INS + DVL | GPS surfacing + INS |
| **Comms (underwater)** | Tether option / acoustic | Acoustic modem | Acoustic / surface relay |
| **Deployment** | All platforms | All platforms | All platforms |
| **Recovery** | Manual / auto-dock | Manual / auto-surface | Auto-surface on schedule |
| **Best For** | Hull inspection, visual ID | Search, patrol, mapping | Passive monitoring, picket |

---

## Variant Details

### VSS-1I (Inspector)
**Best for:** Hull inspection, close-range visual work, precision tasks

```
VSS-1I PROFILE

     ┌─────────────────┐
     │   ═══     ═══   │  ← Vertical thrusters (depth/pitch)
     │  ┌─────────┐    │
     │  │ Camera  │    │  ← HD camera + lights
     │  │ Housing │    │
     │  └─────────┘    │
     │ ══           ══ │  ← Horizontal thrusters (forward/lateral)
     └─────────────────┘
         0.6m wide
```

| Component | Specification | Est. Cost |
|-----------|---------------|-----------|
| **Frame** | HDPE / aluminum, open frame | $300 |
| **Thrusters** | 6x Blue Robotics T200 | $1,200 |
| **Pressure Housing** | Aluminum, 4" diameter | $400 |
| **Buoyancy** | Syntactic foam blocks | $200 |
| **Camera** | 4K low-light, 180° tilt | $500 |
| **Lights** | 4x 1500 lumen LED | $400 |
| **Electronics** | Pixhawk + Raspberry Pi 4 | $300 |
| **Battery** | 18Ah LiFePO4 (14.8V) | $400 |
| **Depth Sensor** | Bar30 (300m rated) | $70 |
| **IMU** | Integrated with Pixhawk | Included |
| **Leak Sensors** | 3x internal | $50 |
| **Tether (optional)** | 100m fiber optic | $800 |
| **Acoustic Modem** | Low-cost USBL | $1,500 |

**Specifications:**
| Parameter | Value |
|-----------|-------|
| Dimensions | 0.6m L × 0.4m W × 0.3m H |
| Weight (air) | 18 kg |
| Weight (water) | Neutral (+/- 0.5 kg) |
| Depth Rating | 200m |
| Speed (max) | 3 kts |
| Endurance (untethered) | 4-6 hrs |
| Endurance (tethered) | Unlimited (surface power) |
| Thruster Config | 6-DOF (full maneuverability) |

**Capabilities:**
- 6-DOF movement (forward, lateral, vertical, pitch, roll, yaw)
- Hover in place for inspection
- Station-hold against current
- HD video recording and streaming (tethered)
- Low-light operation
- Obstacle avoidance

**Budget Estimate: ~$6,000-8,000**

---

### VSS-1P (Patrol)
**Best for:** Area search, autonomous patrol, seafloor mapping

```
VSS-1P PROFILE (Torpedo-style)

    ┌──────────────────────────────────────────────────┐
    │  ○                                           ═══ │
    │  Sonar     ════════════════════════════      Prop│
    │  nose                Pressure hull               │
    └──────────────────────────────────────────────────┘
                        1.5m length

    ════  Side-scan sonar arrays (port/starboard)
```

| Component | Specification | Est. Cost |
|-----------|---------------|-----------|
| **Hull** | Fiberglass torpedo body | $800 |
| **Propulsion** | Brushless thruster + fins | $600 |
| **Pressure Housing** | Aluminum, 6" diameter | $600 |
| **Buoyancy** | Syntactic foam, trim system | $400 |
| **Forward Sonar** | Ping360 scanning sonar | $2,500 |
| **Side-Scan Sonar** | StarFish 450F or similar | $5,000 |
| **Camera** | Forward-looking, LED lights | $400 |
| **Electronics** | Pixhawk + companion computer | $400 |
| **Battery** | 40Ah LiFePO4 (29.6V) | $800 |
| **DVL** | Water Linked DVL-A50 | $6,900 |
| **INS** | Integrated IMU + compass | $300 |
| **Acoustic Modem** | USBL transponder | $2,000 |
| **GPS Antenna** | Surface mast (retractable) | $200 |

**Specifications:**
| Parameter | Value |
|-----------|-------|
| Dimensions | 1.5m L × 0.2m diameter |
| Weight (air) | 50 kg |
| Weight (water) | Slightly positive (auto-surface) |
| Depth Rating | 200m |
| Speed (max) | 5 kts |
| Speed (cruise) | 2.5 kts |
| Endurance | 12-24 hrs (speed dependent) |
| Range | 30-60 nm |

**Capabilities:**
- Autonomous waypoint navigation
- Pre-programmed search patterns (lawnmower, expanding square)
- Side-scan sonar mapping
- Forward obstacle avoidance
- Auto-surface for GPS fix and data upload
- Acoustic communication while submerged
- DVL for precise dead-reckoning

**Budget Estimate: ~$20,000-25,000**

---

### VSS-1S (Sentry)
**Best for:** Long-duration passive monitoring, acoustic surveillance

Two configurations: **Glider** (mobile) or **Bottom-Sitter** (stationary)

#### VSS-1S-G (Glider Configuration)

```
VSS-1S-G PROFILE (Glider)

              ╱─────────────────────────╲
    ════════ ╱                           ╲ ════════
    Wing    │      Pressure hull          │    Wing
            │   ┌──────────────────┐      │
             ╲  │  Buoyancy engine │     ╱
              ╲─┴──────────────────┴────╱
                      1.8m length

    Moves by changing buoyancy → glides down/up
```

| Component | Specification | Est. Cost |
|-----------|---------------|-----------|
| **Hull** | Fiberglass, hydrodynamic | $1,000 |
| **Wings** | Carbon fiber, 1.2m span | $500 |
| **Buoyancy Engine** | Piston + oil bladder | $2,000 |
| **Pressure Housing** | Aluminum, 6" diameter | $600 |
| **Hydrophone Array** | 4-element, 10Hz-100kHz | $1,500 |
| **CTD Sensor** | Conductivity, temp, depth | $800 |
| **Electronics** | Low-power ARM processor | $300 |
| **Battery** | 60Ah lithium primary | $600 |
| **Iridium Modem** | Satellite comms at surface | $1,200 |
| **GPS** | Surface antenna | $100 |

**Specifications:**
| Parameter | Value |
|-----------|-------|
| Dimensions | 1.8m L × 1.2m wingspan |
| Weight (air) | 55 kg |
| Depth Rating | 200m |
| Speed | 0.3-0.5 kts (horizontal) |
| Glide Ratio | 3:1 |
| Endurance | 3-6 months |
| Range | 1,000+ nm (over deployment) |

#### VSS-1S-B (Bottom-Sitter Configuration)

```
VSS-1S-B PROFILE (Bottom-Sitter)

         ┌─────────────────────────┐
         │     Hydrophone mast     │
         │           │             │
    ═════│═══════════╪═════════════│═════  ← Release weight
         │    ┌──────┴──────┐      │
         │    │  Pressure   │      │       Sits on seafloor
         │    │   housing   │      │       listening
    ~~~~~│~~~~│~~~~~~~~~~~~~│~~~~~~│~~~~~  ← Seafloor
         └────┴─────────────┴──────┘
              Anchor frame
```

| Component | Specification | Est. Cost |
|-----------|---------------|-----------|
| **Frame** | Aluminum, weighted base | $400 |
| **Pressure Housing** | Glass sphere or aluminum | $800 |
| **Hydrophone Array** | 4-element vertical array | $2,000 |
| **Acoustic Processor** | Low-power DSP | $500 |
| **Electronics** | Ultra-low-power MCU | $200 |
| **Battery** | 100Ah lithium primary | $800 |
| **Acoustic Release** | Drop weight to surface | $1,500 |
| **Iridium Beacon** | Surface location transmit | $600 |
| **Flasher/Radio Beacon** | Recovery aids | $200 |

**Specifications:**
| Parameter | Value |
|-----------|-------|
| Dimensions | 0.8m L × 0.6m W × 1.2m H |
| Weight (air) | 70 kg (with anchor weight) |
| Weight (water) | Negative (sinks), positive after release |
| Depth Rating | 200m |
| Endurance | 6-12 months |
| Detection Range | Vessel: 5-20 nm, Diver: 500m |

**Common VSS-1S Capabilities:**
- Passive acoustic monitoring (no active sonar)
- Vessel signature detection and classification
- Diver detection
- Long-duration unattended operation
- Scheduled surface communication (glider) or end-of-mission recovery (sitter)
- Low probability of detection

**Budget Estimate:**
- VSS-1S-G (Glider): ~$10,000-12,000
- VSS-1S-B (Bottom-Sitter): ~$7,000-9,000

---

## Common Systems

All VSS-1 variants share these elements where practical:

| System | Specification | Notes |
|--------|---------------|-------|
| **Depth Sensor** | Bar30 (300m rated) | Blue Robotics, $70 |
| **Leak Detection** | 3-point internal sensors | Critical safety |
| **Recovery Beacon** | GPS + strobe + RF | Surface location |
| **Data Format** | Common log format | Cross-variant analysis |
| **Charging** | 24V DC input | Standard connector |

---

## Deployment Methods

### Shore Launch
- Boat ramp or beach entry
- Vehicle carried to water, released
- Best for: VSS-1I, VSS-1P short missions

### VS-1 Deployment
- VS-1 transits to location, deploys VSS
- VSS operates, VS-1 monitors/relays
- VS-1 recovers VSS or VSS auto-surfaces
- Best for: All variants, remote operations

### Manned Vessel Deployment
- Traditional over-the-side deployment
- Real-time tethered operation (VSS-1I)
- Best for: Hull inspection, supervised ops

---

## Variant Selection Guide

| If your mission is... | Choose | Why |
|-----------------------|--------|-----|
| **Hull inspection** | VSS-1I | Hover, precision, HD video |
| **Search & rescue** | VSS-1P | Area coverage, sonar |
| **Seafloor mapping** | VSS-1P | Side-scan sonar |
| **Contraband search** | VSS-1I + VSS-1P | Visual + sonar |
| **Harbor monitoring** | VSS-1S-B | Long-duration passive |
| **Wide area acoustic** | VSS-1S-G | Mobile, weeks duration |
| **Diver detection** | VSS-1S-B | Passive hydrophone |
| **Pipeline inspection** | VSS-1P | Transit + sonar |
| **Subsurface picket** | VSS-1S-G | Complements VS-1 |

---

## Budget Summary

| Variant | Unit Cost | Best For |
|---------|-----------|----------|
| **VSS-1I** | $6,000-8,000 | Inspection, visual ID |
| **VSS-1P** | $20,000-25,000 | Patrol, search, mapping |
| **VSS-1S-G** | $10,000-12,000 | Mobile acoustic monitoring |
| **VSS-1S-B** | $7,000-9,000 | Fixed acoustic monitoring |

### Development Priority

```
Phase 1: VSS-1I (Inspector)
├── Lowest cost entry point
├── Most versatile for initial ops
├── Can be tethered (lower risk)
└── Validates underwater operations

Phase 2: VSS-1S-B (Bottom-Sitter)
├── Passive monitoring capability
├── Complements VS-1 picket ops
├── Relatively simple (no propulsion)
└── Long-duration proof of concept

Phase 3: VSS-1P (Patrol)
├── Highest capability
├── Highest cost (DVL, sonar)
├── Requires proven navigation
└── Full autonomous operations

Phase 4: VSS-1S-G (Glider)
├── Most complex (buoyancy engine)
├── Longest endurance
├── Integrates with VS-1 for relay
└── Wide-area coverage
```

---

## Comparison to Commercial Systems

| Parameter | VSS-1I | VSS-1P | BlueROV2 | REMUS 100 |
|-----------|--------|--------|----------|-----------|
| Type | Inspection ROV | Patrol AUV | Inspection ROV | Survey AUV |
| Depth | 200m | 200m | 100m | 100m |
| Endurance | 4-8 hrs | 12-24 hrs | 2-4 hrs | 8-22 hrs |
| Speed | 3 kts | 5 kts | 3 kts | 5 kts |
| Cost | ~$7,000 | ~$22,000 | ~$5,000 | ~$100,000+ |
| Autonomy | Semi-auto | Full auto | Manual/semi | Full auto |

---

## Technical Challenges

| Challenge | Mitigation |
|-----------|------------|
| **Underwater comms** | Acoustic modem + scheduled surfacing |
| **Navigation drift** | DVL (VSS-1P), GPS surfacing, visual landmarks |
| **Pressure sealing** | Proven Blue Robotics components, pressure testing |
| **Recovery** | Auto-surface, RF/GPS beacon, strobe light |
| **Fouling** | Anti-foul coatings, mission duration limits |
| **Entanglement** | Prop guards, smooth hull, route planning |

---

## ArduPilot Integration

All variants use ArduPilot Sub firmware:
- VSS-1I: ArduSub (ROV mode)
- VSS-1P: ArduSub (AUV mode, waypoint navigation)
- VSS-1S: Custom low-power firmware for glider/sitter

ArduSub provides:
- Depth hold
- Attitude stabilization
- Waypoint navigation
- Failsafe behaviors (auto-surface on low battery, leak, lost comms)
- Joystick control via tether or acoustic link

---

*Document Version: 1.0*
*Status: Concept Development*
*Platform: VSS-1 (Subsurface)*
*Date: January 2026*
