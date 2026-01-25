# VS-1 Picket - Long-Endurance Surface Surveillance Vessel

**Type:** Unmanned Surface Vehicle (USV) | **Config:** Monohull | **Status:** Concept

## Overview

The VS-1 is a long-endurance unmanned surface vessel designed for persistent maritime surveillance. Operating as a "picket" vessel, it stations in the Gulf of Mexico to monitor and report vessel traffic passing through designated areas.

### Design Philosophy
- **Dual-mode operation** - fast transit + efficient loiter
- **Minimal payload** - sensors only, no weapons
- **Solar-augmented power** - extends on-station endurance
- **Common systems** - shares control/video with VA-4 air platform

---

## Propulsion Variants

The VS-1 platform is available in three propulsion configurations to match operational requirements and budget.

### Mission Baseline

```
PICKET MISSION REQUIREMENTS

┌──────────────────────────────────────────────────────────────────────────────┐
│  SELF-DEPLOY         TRANSIT              ON-STATION          SELF-RECOVER  │
│                                                                              │
│  Home Base ────► 1,000 nm ────► Days to Weeks ────► 1,000 nm ────► Home Base│
│  (shore site)    to station     loiter in Gulf      return                   │
│                                 of Mexico                                    │
└──────────────────────────────────────────────────────────────────────────────┘

Key Requirements:
• Transit range: 1,000 nm each way (2,000 nm round trip capability)
• On-station endurance: Days to weeks of persistent surveillance
• Self-deploy/recover: Autonomous departure and return to shore facility
• Loiter speed: 5-8 knots (station-keeping, drift patrol)
• Weather capability: Sea State 3-4 (Gulf of Mexico conditions)
• Sensors: AIS receiver, camera, GPS - continuous operation
• Communications: Starlink for video/data relay
• Autonomy: Minimal human intervention throughout mission
```

### Variant Comparison

| Parameter | VS-1D (Diesel + Electric) | VS-1S (Sail-Assisted) |
|-----------|---------------------------|----------------------|
| **Propulsion** | 20 HP diesel + trolling motor | Wing sail + 10 HP diesel |
| **Sprint Speed** | 18-20 kts | 12-15 kts (motor) |
| **Economy Transit** | 8-10 kts | 6-8 kts (sail + motor) |
| **Loiter Speed** | 5-8 kts (electric) | 3-6 kts (sail only) |
| **Transit Range** | 1,000+ nm | 1,500+ nm |
| **Fuel Capacity** | 60 gal diesel | 30 gal diesel |
| **On-Station Endurance** | Weeks (solar-electric) | Months (sail + solar) |
| **Silent Loiter** | ✓ Yes | ✓ Yes |
| **Solar Autonomy** | ✓ Full (loiter) | ✓ Full (loiter + slow transit) |
| **Loiter Fuel Use** | 0 gal/day | 0 gal/day |
| **Weather Dependence** | Low | Moderate (wind) |
| **Complexity** | Medium (2 systems) | High (sail + motor) |
| **Maintenance** | Medium | Medium |
| **Unit Cost** | ~$14,000 | ~$16,000 |
| **Development Phase** | **Start here** | Future upgrade |

### Variant Details

#### VS-1D (Diesel + Electric)
**Best for:** Maximum operational flexibility, long-range self-deployment

| Component | Specification | Cost |
|-----------|---------------|------|
| Primary | Yanmar 20 HP diesel saildrive | $6,000 |
| Secondary | Minn Kota 80 lb trolling | $800 |
| Fuel Tank | 60 gallons diesel | $400 |
| Battery | 4x 100Ah LiFePO4 (4.8 kWh) | $1,000 |
| Solar | 500W array | $900 |

**Performance:**
| Mode | Speed | Consumption | Range |
|------|-------|-------------|-------|
| Sprint | 18-20 kts | 1.5 gal/hr | 800 nm |
| Economy transit | 8-10 kts | 0.5 gal/hr | 1,200 nm |
| Electric loiter | 5-8 kts | Solar-powered | Unlimited |

**Pros:**
- 1,000+ nm self-deploy range
- Silent electric loiter (weeks on station)
- Diesel efficiency for long transit
- Solar-autonomous on station
- Sprint capability when needed

**Cons:**
- Most complex (two propulsion systems)
- Higher cost
- Diesel saildrive installation complexity

---

#### VS-1S (Sail-Assisted)
**Best for:** Maximum autonomy, extended unattended deployment

| Component | Specification | Cost |
|-----------|---------------|------|
| Wing Sail | 8m² rigid wing (automated) | $4,000 |
| Motor | Yanmar 10 HP diesel saildrive | $4,500 |
| Fuel Tank | 30 gallons diesel | $300 |
| Battery | 4x 100Ah LiFePO4 (4.8 kWh) | $1,000 |
| Solar | 500W array | $900 |

**Performance:**
| Mode | Speed | Consumption | Range |
|------|-------|-------------|-------|
| Motor sprint | 12-15 kts | 0.8 gal/hr | 500 nm |
| Sail + motor | 6-8 kts | 0.2 gal/hr | 1,500+ nm |
| Sail only | 4-6 kts | 0 gal/hr | Unlimited |
| Electric loiter | 3-5 kts | Solar-powered | Unlimited |

**Pros:**
- Longest unattended endurance (months potential)
- Lowest fuel consumption
- Silent operation
- True autonomy (sail + solar)
- Smallest fuel logistics footprint

**Cons:**
- Slowest transit
- Wind-dependent performance
- Most complex (sail system)
- Higher initial cost
- Sail maintenance requirements

---

### Variant Selection Guide

| If your priority is... | Choose | Why |
|------------------------|--------|-----|
| **Start development** | **VS-1D** | Balanced capability, proven tech foundation |
| **1,000 nm + silent loiter** | VS-1D | Diesel range + electric loiter |
| **Maximum autonomy** | VS-1S | Sail + solar = months on station |
| **Fastest transit** | VS-1D | 18-20 kt sprint capability |
| **Lowest fuel logistics** | VS-1S | 30 gal tank, mostly sail-powered |
| **Covert/silent ops** | VS-1D or VS-1S | Electric/sail loiter |
| **All-weather reliability** | VS-1D | Not wind-dependent |

### Development Path

```
Phase 1: VS-1D Development
├── Build foam core hull
├── Install diesel saildrive + electric trolling motor
├── Validate 1,000 nm range
├── Prove solar-electric loiter capability
└── Operational deployment

Phase 2: VS-1S Development (leverages VS-1D lessons)
├── Same hull design (proven)
├── Add 8m² rigid wing sail system
├── Smaller diesel (10 HP vs 20 HP)
├── Extended autonomy testing
└── Months-long deployment capability
```

---

## Mission Profile

```
VS-1 PICKET MISSION

Deploy ──► Transit to Station ──► Loiter/Monitor ──► Report Contacts ──► Recover
              │                        │                    │
           20 kts                 Days/Weeks            AIS tracking
           gas outboard           Solar + battery       Video relay
                                  5-8 kts loiter        Position reports
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
| Beam | 1.4-1.6 meters |
| Draft | 0.4-0.5 meters |
| Displacement (empty) | 350-450 kg |
| Displacement (loaded) | 600-800 kg |
| Fuel Capacity | 60-100 gallons (variant dependent) |
| Fineness Ratio | 4.5-5 (semi-planing capable) |
| Construction | Foam core composite |
| Freeboard | 0.5-0.6 meters |
| Hull Type | Deep-V forward, flat aft (semi-planing) |

### Performance

| Parameter | VS-1D | VS-1S |
|-----------|-------|-------|
| Sprint Speed | 18-20 kts | 12-15 kts |
| Economy Transit | 8-10 kts | 6-8 kts |
| Loiter Speed | 5-8 kts (electric) | 3-6 kts (sail) |
| Transit Range | 1,000+ nm | 1,500+ nm |
| On-Station Endurance | Weeks | Months |
| Sea State | SS 4 | SS 3-4 |

### Power System (by Variant)

**VS-1D (Diesel + Electric):**
| Component | Specification |
|-----------|---------------|
| Primary Engine | Yanmar 20 HP diesel saildrive |
| Electric Motor | 80 lb thrust trolling motor |
| Fuel Capacity | 60 gallons diesel |
| Battery Bank | 4x 100Ah LiFePO4 (4.8 kWh) |
| Solar Array | 500W (5x 100W panels) |

**VS-1S (Sail-Assisted):**
| Component | Specification |
|-----------|---------------|
| Wing Sail | 8m² rigid wing, automated |
| Engine | Yanmar 10 HP diesel saildrive |
| Fuel Capacity | 30 gallons diesel |
| Battery Bank | 4x 100Ah LiFePO4 (4.8 kWh) |
| Solar Array | 500W (5x 100W panels) |

---

**Mission Fuel Budget (1,000 nm transit + 14 days loiter + 1,000 nm return):**

| Variant | Transit Out | Loiter (14 days) | Transit Back | Total | Reserve |
|---------|-------------|------------------|--------------|-------|---------|
| VS-1D (sprint) | 50 gal | 0 gal (electric) | 50 gal | 100 gal | ✗ Need refuel |
| VS-1D (economy) | 25 gal | 0 gal (electric) | 25 gal | 50 gal | ✓ 10 gal |
| VS-1S | 10 gal | 0 gal (sail) | 10 gal | 20 gal | ✓ 10 gal |

**Key Insight:** Both VS-1D (economy mode) and VS-1S can complete full 2,000 nm round-trip + 14-day loiter on single fuel load.

---

**Power Budget (24-hour loiter cycle - VS-1D/VS-1S electric loiter):**
| Load | Power | Daily Consumption |
|------|-------|-------------------|
| Propulsion (electric loiter) | 100W avg | 2,400 Wh |
| Electronics/sensors | 25W | 600 Wh |
| Communications | 30W avg | 720 Wh |
| **Total Daily** | | **~3,700 Wh** |

**Solar Output:** ~3-4 kWh/day (Gulf of Mexico)
**Net:** Solar covers 80-100% of daily consumption. Battery provides overnight/overcast buffer.

## Subsystems

### Propulsion

**Primary: Gas Outboard**
| Component | Specification | Cost |
|-----------|---------------|------|
| Motor | Yamaha F25 or Honda BF25 (25 HP) | $4,500 |
| Type | 4-stroke, EFI, tiller control | |
| Weight | ~140 lbs (63 kg) | |
| Fuel Consumption | 2 gal/hr @ WOT, 0.3 gal/hr @ idle | |
| Control | Electronic throttle + autopilot integration | $200 |

**Secondary: Electric Trolling Motor (for silent loiter)**
| Component | Specification | Cost |
|-----------|---------------|------|
| Motor | Minn Kota Riptide 80 lb thrust | $800 |
| Type | Saltwater, 24V brushless | |
| Control | PWM via autopilot | $50 |
| Purpose | Silent station-keeping, solar-powered loiter | |

**Propulsion Modes:**
- **Transit:** Gas outboard at 20 kts (75% throttle)
- **Repositioning:** Gas outboard at 10-15 kts (50% throttle)
- **Active Loiter:** Gas outboard at idle (5-8 kts)
- **Silent Loiter:** Electric trolling motor (solar-powered)

### Charging System

**Primary: Solar Array**
| Component | Specification | Cost |
|-----------|---------------|------|
| Panels | 4x 100W marine-grade flexible | $600 |
| Total Output | 400W peak | |
| Daily Yield | 2.5-3.0 kWh (Gulf of Mexico avg) | |
| Mounting | Flush deck mount, weatherproof | |
| Controller | MPPT 40A charge controller | $150 |

**Secondary: Outboard Alternator**
| Component | Specification | Cost |
|-----------|---------------|------|
| Output | 15A @ 12V (~180W) | Included |
| Charging | When outboard running (transit/repositioning) | |
| Note | 1 hour transit = ~1.5 kWh added to batteries | |

**Backup: Portable Generator (Optional)**
| Component | Specification | Cost |
|-----------|---------------|------|
| Model | Honda EU1000i | $900 |
| Purpose | Emergency charging in extended overcast | |
| Note | Can be omitted for cost savings | |

### Battery Bank

| Component | Specification | Cost |
|-----------|---------------|------|
| Type | LiFePO4 (Lithium Iron Phosphate) | |
| Capacity | 3x 100Ah 12V batteries | $750 |
| Total Energy | 3.6 kWh | |
| Weight | ~25 lbs each (75 lbs total) | |
| Cycles | 2000+ cycles | |
| BMS | Integrated per battery | |
| Configuration | Parallel for 12V system | |

**Battery provides 1+ day reserve for overnight and overcast periods.**

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
                          ════════════════════════════════════
                        /                                      \
    ═══════════════════          Deep-V fwd    Flat aft         ═══════
    Bow                                                           Stern
    (sharp entry)              (wave handling)  (planing)      (transom)


TOP VIEW (1.2-1.4m beam)
         ┌────────────────────────────────────────────────────┐
        /                                                      \
       /                      Solar Panels                      \
      │                         (4x 100W)                        │
       \                                                        /
        \                                                      /
         └────────────────────────────────────────────────────┘


CROSS SECTION (looking aft)
              ┌─────────────────┐
             /                   \
            /    Solar Panels     \
           /═══════════════════════\
          │                         │
          │      Equipment Bay      │
           \                       /
            ╲_____________________╱
                  Deep-V hull
```

**Design Notes:**
- Fineness ratio 5-6 (length/beam) for semi-planing capability
- Deep-V bow (18-20°) for wave penetration at speed
- Transitioning to flat aft sections for planing lift
- Wide beam (1.2-1.4m) for stability and solar panel area
- Transom stern for outboard mount
- Sealed compartments for flotation and fuel storage

## Budget Summary

### VS-1D (Diesel + Electric) - ~$14,000

| Category | Component | Cost |
|----------|-----------|------|
| **Hull** | Foam core composite (DIY) | $1,000 |
| **Propulsion** | Yanmar 20 HP diesel saildrive | $6,000 |
| | Electric trolling motor (80 lb) | $800 |
| | Fuel tank (60 gal) + plumbing | $500 |
| **Power** | LiFePO4 batteries (4x 100Ah) | $1,000 |
| | Solar panels (5x 100W) | $750 |
| | MPPT charge controller | $150 |
| | Wiring, fuses, switches | $250 |
| **Sensors** | dAISy AIS receiver | $80 |
| | Camera system | $150 |
| | GPS/IMU | $45 |
| **Comms** | Starlink Mini | $600 |
| | Backup radio | $50 |
| **Control** | Autopilot (Pixhawk) | $200 |
| | RC receiver | $50 |
| | Telemetry radio | $100 |
| **Misc** | Hardware, paint, sealant | $400 |
| | **TOTAL** | **~$12,125** |
| | **With 15% contingency** | **~$14,000** |

---

### VS-1S (Sail-Assisted) - ~$16,000

| Category | Component | Cost |
|----------|-----------|------|
| **Hull** | Foam core composite (DIY) | $1,000 |
| **Sail** | 8m² rigid wing sail (automated) | $4,000 |
| | Sail control actuators | $500 |
| **Propulsion** | Yanmar 10 HP diesel saildrive | $4,500 |
| | Fuel tank (30 gal) + plumbing | $350 |
| **Power** | LiFePO4 batteries (4x 100Ah) | $1,000 |
| | Solar panels (5x 100W) | $750 |
| | MPPT charge controller | $150 |
| | Wiring, fuses, switches | $250 |
| **Sensors** | dAISy AIS receiver | $80 |
| | Camera system | $150 |
| | GPS/IMU | $45 |
| | Wind sensor (for sail) | $100 |
| **Comms** | Starlink Mini | $600 |
| | Backup radio | $50 |
| **Control** | Autopilot (Pixhawk) | $200 |
| | RC receiver | $50 |
| | Telemetry radio | $100 |
| **Misc** | Hardware, paint, sealant | $500 |
| | **TOTAL** | **~$14,375** |
| | **With 15% contingency** | **~$16,500** |

---

**Operating Costs (per mission):**

| Variant | Fuel Cost | Starlink | Total/Mission |
|---------|-----------|----------|---------------|
| VS-1D | ~$200 (50 gal diesel) | ~$75 | ~$275 |
| VS-1S | ~$80 (20 gal diesel) | ~$75 | ~$155 |

**Notes:**
- Excludes labor (DIY build)
- Starlink monthly fee ~$50-150/month
- Diesel ~$4/gallon
- Both variants complete full mission on single fuel load

## Comparison to Reference Designs

| Parameter | VS-1D | VS-1S | Sea Baby | MAGURA V5 |
|-----------|-------|-------|----------|-----------|
| Length | 7m | 7m | 6m | 5.5m |
| Speed (max) | 18-20 kts | 12-15 kts | 48 kts | 54 kts |
| Speed (economy) | 8-10 kts | 6-8 kts | N/A | N/A |
| Range | 1,000+ nm | 1,500+ nm | 500-1000 nm | 450 nm |
| Loiter Endurance | Weeks | Months | Hours | 60 hrs |
| Payload | Sensors | Sensors | 400-2000 kg | 200-320 kg |
| Propulsion | Diesel + electric | Sail + diesel | Jet drive | Jet drive |
| Cost | ~$14,000 | ~$16,000 | $204,000 | Unknown |
| Role | Surveillance | Surveillance | Strike | Strike |

**Key Differences:**
- VS-1 variants optimize for endurance and range, not speed
- Self-deploy capability (1,000+ nm from home base)
- Solar/sail augmentation for extended unattended operation
- 10-15x lower cost than military USVs
- Silent loiter capability (electric or sail)

## Development Phases

### Phase 1: Hull & Propulsion
- Build foam core semi-planing hull
- Install and test outboard motor
- Validate 20 kt transit capability
- Test stability and handling at speed

### Phase 2: Power System
- Install battery bank and solar array
- Mount and test electric trolling motor
- Solar charging validation
- Dual-mode propulsion integration

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
| Larger battery bank | Extended overcast operation | $500 |
| Auxiliary fuel tank | Extended transit range | $300 |
| Satellite phone backup | Redundant comms | $500 |
| Hydrophone | Acoustic monitoring | $300 |
| Night vision camera | Low-light surveillance | $800 |
| Thermal camera | All-weather detection | $1,500 |

---

*Document Version: 2.0*
*Status: Development (VS-1D) / Planned (VS-1S)*
*Platform: VS-1 Picket (Surface)*
*Updated: January 2026 - 1,000 nm self-deploy, VS-1D and VS-1S variants*
