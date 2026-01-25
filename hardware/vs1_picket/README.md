# VS-1 Picket - Long-Endurance Surface Surveillance Vessel

**Type:** Unmanned Surface Vehicle (USV) | **Config:** Monohull | **Status:** Concept

## Overview

The VS-1 is a long-endurance unmanned surface vessel designed for persistent maritime surveillance. Operating as a "picket" vessel, it stations in the Gulf of Mexico to monitor and report vessel traffic passing through designated areas.

### Design Philosophy
- **Maximum endurance** over speed
- **Minimal payload** - sensors only, no weapons
- **Hybrid power** - generator charges batteries for extended operations
- **Low cost** - target under $5,000
- **Common systems** - shares control/video with VA-4 air platform

## Mission Profile

```
VS-1 PICKET MISSION

Deploy ──► Transit to Station ──► Loiter/Monitor ──► Report Contacts ──► Recover
              │                        │                    │
           5-8 kts                Days/Weeks            AIS tracking
           low power              Generator cycles      Video relay
                                  Solar supplement      Position reports
```

### Operational Concept
1. Deploy from shore or vessel
2. Transit to designated patrol area (Gulf of Mexico)
3. Station-keep or drift in patrol box
4. Monitor all vessel traffic via AIS
5. Relay video/data via satellite link
6. Generator runs periodically to maintain battery charge
7. Recover for maintenance/refuel as needed

## Specifications

### Hull

| Parameter | Value |
|-----------|-------|
| Length | 7 meters (23 ft) |
| Beam | 0.6-0.8 meters |
| Draft | 0.3-0.4 meters |
| Displacement | 150-250 kg |
| Fineness Ratio | 10-12 (long/narrow for efficiency) |
| Construction | Foam core composite |
| Freeboard | 0.3-0.4 meters |

### Performance

| Parameter | Value |
|-----------|-------|
| Cruise Speed | 5-8 knots |
| Max Speed | 12-15 knots |
| Range (transit) | 200+ nm |
| Endurance (station) | Days to weeks |
| Sea State | Up to Sea State 3 (0.5-1.25m waves) |

### Power System

| Component | Specification |
|-----------|---------------|
| Primary Power | Lithium battery bank |
| Battery Capacity | 200 Ah @ 12V (2.4 kWh) |
| Generator | Honda EU1000i (900W continuous) |
| Generator Runtime | 8 hours per gallon |
| Fuel Capacity | 5-10 gallons |
| Solar (supplemental) | 100-200W panel |
| Propulsion Draw | 50-150W cruise |

**Power Budget (24-hour cycle):**
| Load | Power | Daily Consumption |
|------|-------|-------------------|
| Propulsion (station-keeping) | 50W avg | 1,200 Wh |
| Electronics/sensors | 25W | 600 Wh |
| Communications | 30W avg | 720 Wh |
| **Total Daily** | | **~2,500 Wh** |

Generator running 3-4 hours/day replenishes consumption with margin.

## Subsystems

### Propulsion

| Component | Specification | Cost |
|-----------|---------------|------|
| Motor | Electric trolling motor (55-80 lb thrust) | $300-500 |
| Type | 12V brushless or standard | |
| Control | PWM speed controller | $50 |
| Propeller | Weedless design | Included |

Alternative: Small electric outboard (Torqeedo Ultralight) for higher efficiency at increased cost.

### Generator

| Component | Specification | Cost |
|-----------|---------------|------|
| Model | Honda EU1000i | $900 |
| Output | 900W continuous / 1000W peak | |
| Weight | 28 lbs (12.7 kg) | |
| Noise | 59 dB (quieter than conversation) | |
| Runtime | 8 hours @ 1/4 load per gallon | |
| Charging | Via marine battery charger (35-50A) | |

**Generator Mounting:**
- Enclosed compartment with ventilation
- Exhaust routed overboard
- Fuel tank separate with anti-siphon valve
- Auto-start capability via relay

### Battery Bank

| Component | Specification | Cost |
|-----------|---------------|------|
| Type | LiFePO4 (Lithium Iron Phosphate) | |
| Capacity | 2x 100Ah 12V batteries | $500 |
| Total Energy | 2.4 kWh | |
| Weight | ~25 lbs each (50 lbs total) | |
| Cycles | 2000+ cycles | |
| BMS | Integrated | |

### Sensors

| Sensor | Model | Weight | Cost | Purpose |
|--------|-------|--------|------|---------|
| **AIS Receiver** | dAISy HAT or similar | <1 lb | $80 | Track vessel traffic |
| **Camera** | Same as VA-4 | 0.5 lb | $150 | Visual surveillance |
| **GPS** | u-blox M8N or similar | <0.5 lb | $30 | Position/navigation |
| **IMU** | MPU-9250 | <0.1 lb | $15 | Heading/attitude |

**AIS vs Radar Decision:**
- AIS receiver chosen over radar for VS-1
- All commercial vessels >300 GT required to have AIS
- AIS provides vessel ID, course, speed, destination
- Lower cost, weight, and power than radar
- Radar (Furuno DRS4W, $1,300) available as upgrade if needed

### Communications

| Component | Specification | Cost |
|-----------|---------------|------|
| Primary Link | Starlink Mini | $600 |
| Backup | LoRa mesh radio | $50 |
| Video TX | Same as VA-4 system | Shared |
| Antenna | Marine VHF/GPS combo | $100 |

**Starlink Integration:**
- Flat-mount marine antenna
- 12V power (40-60W when active)
- Provides internet for video streaming
- Can be duty-cycled to save power

### Autopilot/Control

| Component | Specification | Cost |
|-----------|---------------|------|
| Flight Controller | Pixhawk/ArduPilot (Rover firmware) | $200 |
| Compass | External, away from motor | $30 |
| RC Receiver | Shared with VA-4 | $50 |
| Telemetry | 900MHz or cellular | $100 |

**ArduPilot Rover Features:**
- Waypoint navigation
- Station-keeping (loiter)
- Return-to-home
- Geofencing
- Failsafe modes

## Hull Construction

### Foam Core Composite Method

The hull uses foam core construction for low cost, light weight, and unsinkability.

**Materials:**

| Material | Quantity | Cost |
|----------|----------|------|
| XPS foam board (2" thick) | 10 sheets | $200 |
| Fiberglass cloth (6 oz) | 50 yards | $150 |
| Polyester resin | 5 gallons | $150 |
| Marine plywood (stringers) | 2 sheets | $80 |
| Hardware (screws, epoxy) | Misc | $50 |
| **Total Hull Materials** | | **~$630** |

**Construction Process:**
1. Cut foam sheets to hull profile templates
2. Stack and glue foam blocks
3. Shape hull with hot wire cutter and sandpaper
4. Install plywood stringers for rigidity
5. Glass exterior with 2 layers fiberglass cloth
6. Fair and fill any voids
7. Glass interior of deck areas
8. Install motor mount, hatches, hardware

**Hull Shape:**
```
PROFILE VIEW (7m length)
                    ══════════════════════════════════
                   /                                    \
    ══════════════                                        ═══════
    Bow                     Flat bottom                        Stern
    (sharp entry)           (stability)                    (transom)


TOP VIEW
         ┌──────────────────────────────────────────────┐
        /                                                \
       /                                                  \
      │                    Deck                            │
       \                                                  /
        \                                                /
         └──────────────────────────────────────────────┘
```

**Design Notes:**
- Fineness ratio 10-12 (length/beam) for low drag at displacement speeds
- Sharp bow entry for wave penetration
- Flat sections amidships for stability
- Transom stern for motor mount
- Sealed compartments for flotation

## Budget Summary

| Category | Component | Cost |
|----------|-----------|------|
| **Hull** | Foam core composite (DIY) | $630 |
| **Power** | Honda EU1000i generator | $900 |
| | LiFePO4 batteries (2x 100Ah) | $500 |
| | Solar panel (100W) | $150 |
| | Wiring, fuses, charger | $150 |
| **Propulsion** | Electric trolling motor | $400 |
| | Speed controller | $50 |
| **Sensors** | dAISy AIS receiver | $80 |
| | Camera system | $150 |
| | GPS/IMU | $45 |
| **Comms** | Starlink Mini | $600 |
| | Backup radio | $50 |
| **Control** | Autopilot (Pixhawk) | $200 |
| | RC receiver | $50 |
| | Telemetry radio | $100 |
| **Misc** | Hardware, paint, sealant | $200 |
| | **TOTAL** | **~$4,255** |

**Notes:**
- Excludes labor (DIY build)
- Starlink has monthly service fee (~$50-150/month)
- Generator fuel costs extra
- Contingency: add 15% (~$640) for unexpected costs

## Comparison to Reference Designs

| Parameter | VS-1 | Sea Baby | MAGURA V5 |
|-----------|------|----------|-----------|
| Length | 7m | 6m | 5.5m |
| Speed (max) | 15 kts | 48 kts | 54 kts |
| Speed (cruise) | 5-8 kts | 30+ kts | 22 kts |
| Range | 200+ nm | 500-1000 nm | 450 nm |
| Endurance | Days/weeks | Hours | 60 hrs |
| Payload | Sensors only | 400-2000 kg | 200-320 kg |
| Cost | ~$4,500 | $204,000 | Unknown |
| Role | Surveillance | Strike | Strike |

**Key Difference:** VS-1 optimizes for endurance and low cost rather than speed and payload.

## Development Phases

### Phase 1: Hull & Propulsion
- Build foam core hull
- Install trolling motor
- Basic RC control testing
- Validate stability and handling

### Phase 2: Power System
- Install battery bank
- Mount and test generator
- Charging system integration
- Power budget validation

### Phase 3: Sensors & Comms
- Install AIS receiver
- Camera and video link
- Starlink integration
- Data relay testing

### Phase 4: Autonomy
- ArduPilot Rover setup
- Waypoint navigation testing
- Station-keeping validation
- Failsafe testing

### Phase 5: Field Trials
- Extended duration tests
- Generator cycling validation
- Communications range testing
- Operational procedures development

## Operational Considerations

### Deployment
- Launch from boat ramp or vessel davit
- Requires 2-person handling (150-250 kg)
- Pre-mission fuel and battery check
- Communications link verification

### Recovery
- Manual approach and capture
- Generator shutdown
- Secure for transport
- Refuel and recharge

### Maintenance
- Generator: Oil change every 50-100 hours
- Hull: Inspect for damage, clean marine growth
- Batteries: Monitor cell balance
- Electronics: Firmware updates, calibration

### Legal/Regulatory
- USCG regulations for unmanned vessels
- AIS carriage requirements (may need transponder for transmit)
- Operating area restrictions
- Insurance considerations

## Future Upgrades

| Upgrade | Purpose | Est. Cost |
|---------|---------|-----------|
| Radar (Furuno DRS4W) | Detect non-AIS vessels | $1,300 |
| AIS transponder | Transmit own position | $600 |
| Larger solar array | Reduce generator runtime | $300 |
| Diesel generator | Longer fuel range | $1,500 |
| Satellite phone backup | Redundant comms | $500 |
| Hydrophone | Acoustic monitoring | $300 |

---

*Document Version: 1.0*
*Status: Concept Development*
*Platform: VS-1 (Surface)*
