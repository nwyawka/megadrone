# V4 - Gas-Electric Hybrid VTOL

**Type:** VTOL | **Config:** QuadPlane (4 Elec + Gas Pusher) | **Status:** Development

## Quick Specs

| Parameter | Value |
|-----------|-------|
| Wingspan | **3.2m** |
| Length | **2.4m** |
| MTOW | **20 kg** |
| Payload | **2.5 kg** (ISR + Starlink) |
| Cruise Endurance | **8-12 hours** |
| VTOL Endurance | 8-10 min |
| Cruise Speed | 75 km/h |
| Flight Range | **900 km** |
| Link Range | **Unlimited** (via Starlink) |
| Flight Controller | Pixhawk 6X |
| Propulsion | 4x Electric VTOL + 1x Gas Pusher |

## Purpose

- Extended range and endurance (8-12 hours)
- Operational ISR prototype
- Validate gas engine integration
- Test long-duration missions
- Full BVLOS capability with Starlink

## Configuration

Same as V3 but with gasoline pusher replacing electric pusher.

```
    Power Architecture:

    ┌─────────────────┐          ┌─────────────────┐
    │   GAS ENGINE    │          │   LiPo BATTERY  │
    │  (Cruise Only)  │          │  (VTOL + Avionics)│
    │    DLE 35cc     │          │   6S 12000mAh   │
    └────────┬────────┘          └────────┬────────┘
             │                            │
             ▼                            ▼
    ┌─────────────────┐          ┌─────────────────┐
    │  PUSHER PROP    │          │  4x VTOL MOTORS │
    │    18x10        │          │   (T-Motor U5)  │
    └─────────────────┘          └─────────────────┘

    Flight Modes:
    - VTOL: Electric quad motors only
    - Transition: Quad + gas pusher
    - Cruise: Gas pusher only (quad stopped/folded)
```

## Gas Engine Options

| Engine | Displacement | Power | Weight | Fuel Consumption | Cost |
|--------|--------------|-------|--------|------------------|------|
| **DLE 35** | 35cc | 3.5 HP | 870g | 450 mL/hr | $250 |
| DLE 40 | 40cc | 4.0 HP | 1050g | 500 mL/hr | $280 |
| NGH GT35 | 35cc | 3.2 HP | 820g | 420 mL/hr | $180 |
| Zenoah G38 | 38cc | 3.8 HP | 1100g | 480 mL/hr | $350 |

**Recommended:** DLE 35 (proven reliability, good power-to-weight)

## Gas Engine Integration

| Component | Specs | Weight | Cost |
|-----------|-------|--------|------|
| Engine | DLE 35cc twin, 3.5 HP @ 7500 RPM | 870g | $250 |
| Muffler | Pitts style, low backpressure | 80g | $30 |
| Fuel tank | 4L aluminum, clunk pickup | 200g | $50 |
| Fuel lines | Tygon + filter, UV resistant | 50g | $15 |
| Ignition | CDI electronic, separate battery | 100g | incl. |
| Kill switch | Optocoupler, FC controlled | 10g | $10 |
| Throttle servo | 25kg metal gear | 60g | $25 |
| Vibration mount | Rubber standoffs | 50g | $20 |

## Endurance Calculation

| Parameter | Value |
|-----------|-------|
| Fuel capacity | 4L |
| Fuel consumption | 450 mL/hr |
| **Cruise endurance** | **8.9 hours** |
| With reserves (10%) | **8 hours** |

## Flight Controller Upgrade

| Component | Model | Reason | Cost |
|-----------|-------|--------|------|
| FC | Pixhawk 6X | Redundant IMU, more I/O | $400 |
| GPS | Holybro H-RTK F9P | RTK capable, cm accuracy | $300 |
| Airspeed | Dual MS4525DO | Redundancy | $60 |
| RPM Sensor | Hall effect | Engine monitoring | $15 |
| CHT Sensor | K-type thermocouple | Engine temp | $20 |

## Weight Budget (20 kg MTOW)

| Component | Mass (g) | % |
|-----------|----------|---|
| Airframe (wing, booms, fuse, tail) | 5000 | 25% |
| Gas engine + mount | 1200 | 6% |
| **Fuel (4L for 10hr)** | **3000** | **15%** |
| Fuel tank + lines | 350 | 2% |
| VTOL Motors (4x) | 900 | 5% |
| VTOL ESCs (4x) | 250 | 1% |
| VTOL Battery (6S 12Ah) | 1300 | 7% |
| Ignition battery | 100 | 1% |
| FC + Avionics | 500 | 3% |
| **ISR Payload** | **1000** | **5%** |
| **Starlink Mini + mount** | **1500** | **8%** |
| Wiring/Hardware | 700 | 4% |
| **Margin** | 4200 | 21% |
| **MTOW** | **20000g** | 100% |

## Payload Configurations

| Config | ISR | Starlink | Fuel | Endurance | Range | Link Range |
|--------|-----|----------|------|-----------|-------|------------|
| ISR only | 1 kg | - | Full | 12 hr | 900 km | 100 km |
| Starlink only | - | 1.5 kg | Full | 11 hr | 825 km | **Unlimited** |
| **ISR + Starlink** | 1 kg | 1.5 kg | Full | **10 hr** | **750 km** | **Unlimited** |

## Starlink Integration

| Parameter | Value |
|-----------|-------|
| Unit | Starlink Mini |
| Weight (with mount) | ~1.5 kg |
| Power Consumption | 25-40W |
| Link Range | **Unlimited (global)** |
| Latency | 25-50ms |

## Budget

| Category | Cost |
|----------|------|
| Pixhawk 6X + RTK GPS | $700 |
| Gas engine (DLE 35) | $250 |
| Fuel system | $100 |
| Engine sensors | $50 |
| Airframe modifications | $150 |
| VTOL battery (6S 12Ah) | $120 |
| EO/IR camera upgrade | $600 |
| Misc hardware | $100 |
| **Total Additional** | **~$2,070** |

## Cumulative Investment

| Milestone | Cost |
|-----------|------|
| V0 Complete | $200 |
| V1 Complete | $550 |
| V2 Complete | $2,750 |
| V3 Complete | $3,700 |
| **V4 Complete** | **$6,000** |

## Operating Cost

| Item | Cost/hr |
|------|---------|
| Fuel (~0.5L/hr) | ~$1.50 |
| Starlink | ~$2.50 |
| **Total** | **~$4/hr** |

## Skills Developed

- Gas engine operation
- Long-endurance operations
- Fuel system management
- Hybrid power integration
- BVLOS operations

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Gas vibration | Vibration isolation mounts |
| Fuel system leaks | Redundant fuel lines, leak detection |
| Engine failure | Maintain VTOL reserve for emergency landing |

---

*See [Development Roadmap](../../docs/roadmap/development_roadmap.md) for complete specifications.*
