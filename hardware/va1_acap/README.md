# V1-ACAP - As Cheap As Possible (dRehmFlight + SBC)

**Type:** Fixed-Wing | **Config:** Conventional Pusher | **Status:** Development

## Quick Specs

| Parameter | Value |
|-----------|-------|
| Wingspan | 1.0-1.2m |
| Length | 0.6m |
| AUW | 860g |
| Payload | 200g |
| Endurance | 20-25 min |
| Cruise Speed | 54 km/h (15 m/s) |
| Flight Controller | **dRehmFlight (Teensy 4.0) + SBC** |
| Propulsion | 1x Electric (2212 920kv) |

## Purpose

- **Custom autopilot stack** at fraction of commercial FC cost
- Full autopilot capability (GPS, waypoints, RTH) via programming
- Learn flight control fundamentals from the ground up
- Complete code access for customization
- Platform for experimental navigation algorithms

## Architecture: Two-Layer Control System

```
┌─────────────────────────────────────────────────────────────────┐
│                    OUTER LOOP (Navigation)                       │
│                    SBC (RPi / ESP32 / Orange Pi)                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  • GPS waypoint navigation                              │    │
│  │  • Return-to-home logic                                 │    │
│  │  • Mission planning                                     │    │
│  │  • Telemetry (WiFi/cellular)                           │    │
│  │  • Failsafe decisions                                   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                     Serial (UART)                                │
│                            ▼                                     │
├─────────────────────────────────────────────────────────────────┤
│                    INNER LOOP (Stabilization)                    │
│                    Teensy 4.0 + dRehmFlight                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  • Attitude stabilization (1000+ Hz)                    │    │
│  │  • Rate control (acro mode)                             │    │
│  │  • Angle control (self-leveling)                        │    │
│  │  • Servo/ESC output                                     │    │
│  │  • IMU sensor fusion                                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                      PWM Outputs                                 │
│                            ▼                                     │
│              Servos (ailerons, elevator, rudder) + ESC           │
└─────────────────────────────────────────────────────────────────┘
```

## Full Autopilot Capabilities

With SBC + GPS + custom code:
- ✅ GPS waypoint navigation
- ✅ Return-to-home (RTH)
- ✅ Autonomous missions
- ✅ Failsafe RTL
- ✅ Position hold / loiter
- ✅ Geofencing
- ✅ Telemetry (WiFi, cellular, radio)
- ✅ Full code access (Python/C++/MicroPython)

## SBC Options

| SBC | CPU | RAM | WiFi | Weight | Cost |
|-----|-----|-----|------|--------|------|
| **ESP32-S3** | 240MHz Dual | 512KB | Yes | 3g | $8 |
| **Raspberry Pi Zero 2W** | 1GHz Quad | 512MB | Yes | 10g | $15 |
| Orange Pi Zero 3 | 1.5GHz Quad | 1GB | Yes | 26g | $20 |
| Radxa Zero | 1.8GHz Quad | 1-4GB | Yes | 10g | $25 |

**Recommended:** RPi Zero 2W (best balance) or ESP32-S3 (ultra-light/cheap)

## Flight Control Stack

| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| Inner Loop FC | Teensy 4.0 | 5g | $24 |
| IMU | MPU6050 (GY-521) | 3g | $3 |
| Outer Loop Computer | SBC (see above) | 3-26g | $8-25 |
| GPS | BN-880 (GPS + compass) | 10g | $15 |
| **Subtotal** | | **22-45g** | **$50-67** |

## Cost Comparison

| Solution | Weight | Cost | Code Access |
|----------|--------|------|-------------|
| **V1-ACAP (Teensy + ESP32-S3 + GPS)** | 22g | **$50** | ✅ Full |
| **V1-ACAP (Teensy + RPi Zero 2W + GPS)** | 29g | **$57** | ✅ Full |
| SpeedyBee F405 Wing + GPS | 35g | $65 | ⚠️ Config only |
| Pixhawk 6C Mini + GPS | 50g | $260 | ⚠️ Config only |

## Complete Aircraft Budget

| Category | Cost |
|----------|------|
| Teensy 4.0 | $24 |
| MPU6050 module | $3 |
| SBC (RPi Zero 2W or ESP32-S3) | $8-15 |
| BN-880 GPS | $15 |
| Receiver (FS-IA6B) | $12 |
| Motor (2212 920kv) | $8 |
| ESC (30A) | $8 |
| Battery (3S 2200mAh) | $18 |
| Servos (4x SG90) | $6 |
| Propeller | $3 |
| Foam board + materials | $10 |
| Misc (wires, connectors) | $8 |
| **Total** | **~$125-130** |

## When to Choose V1-ACAP

✅ **Good for:**
- Learning autopilot development from scratch
- Custom navigation algorithms
- Research/experimental platforms
- WiFi/cellular telemetry integration
- Computer vision integration
- Maximum flexibility and control
- Cost-sensitive full-autopilot builds

⚠️ **Consider alternatives if:**
- You need proven, reliable autopilot quickly
- Limited programming experience
- Production/commercial use

## Software Development Roadmap

```
Phase 1: Basic Stabilization (Week 1-2)
├── Flash dRehmFlight to Teensy
├── Tune PID for your airframe
└── Test angle mode (self-leveling)

Phase 2: SBC Integration (Week 3-4)
├── Serial communication Teensy ↔ SBC
├── GPS integration (NMEA parsing)
└── Basic telemetry logging

Phase 3: Navigation (Week 5-8)
├── Heading hold controller
├── Altitude hold controller
├── Waypoint navigation
├── Return-to-home logic
└── Failsafe implementation

Phase 4: Ground Station (Week 9-12)
├── WiFi telemetry link
├── Web-based ground station
└── Mission upload/download
```

## Resources

- **dRehmFlight GitHub:** https://github.com/nickrehm/dRehmFlight
- **Teensy 4.0:** https://www.pjrc.com/store/teensy40.html
- **RPi Zero 2W:** https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Custom code bugs | Extensive SITL testing |
| Untested failsafes | Incremental feature additions |

---

*See [Development Roadmap](../../docs/roadmap/development_roadmap.md) for complete specifications.*
