# MegaDrone Development Roadmap

## Reference Design: ALTI Transition

V2, V3, and V4 are inspired by the [ALTI Transition](https://altiunmanned.com/transition) VTOL UAS.

**ALTI Transition Specs:** (Source: [bvlos.tech](https://bvlos.tech/transition))
| Parameter | Value |
|-----------|-------|
| Wingspan | 3,000 mm (3.0m) |
| Length | 2,300 mm (2.3m) |
| MTOW | 18 kg |
| Payload Capacity | **1 kg** (or 1.5 kg with reduced fuel) |
| Endurance | **Up to 12 hours** |
| **Flight Range** | **900 km** |
| Link Range | 150 km (datalink limited) |
| Cruise Speed | 75 km/h |
| Operating Cost | $3.50/hr |
| Propulsion | Hybrid (Electric VTOL + Petrol fixed-wing) |
| Configuration | Twin-boom, 4 VTOL motors, 1 gas pusher |
| Autopilot | ArduPilot (PX4-based ALTI Avionics) |

### ALTI Radio/Datalink Solution
| Component | Specs |
|-----------|-------|
| Primary Datalink | Microhard pMDDL2450 MIMO 2.4GHz encrypted |
| Video Downlink | HD video via pMDDL2450 |
| Standard Range | ~50 km |
| Extended Range | **100 km (62 mi)** with Range Extension Package |
| Range Extension | 10W Microhard amplifier + pneumatic mast + directional grid antenna |

---

## Starlink Integration (V2/V3/V4)

For BVLOS operations beyond line-of-sight datalink range, Starlink Mini provides global satellite connectivity.

### Starlink Mini Specifications
| Parameter | Value |
|-----------|-------|
| Weight (unit only) | 1.10 kg (2.43 lb) |
| Weight (with mount/cable) | **~1.5 kg** |
| Power Consumption | 25-40W |
| Dimensions | 430 × 334 × 79 mm |
| Environmental | IP67, -30°C to 50°C |
| Wind Rating | 96+ km/h operational |

### Payload Configuration Options

| Config | ISR Payload | Starlink | Total Payload | Use Case |
|--------|-------------|----------|---------------|----------|
| **ISR Only** | 1 kg | - | 1 kg | Standard missions, datalink range |
| **Starlink Only** | - | 1.5 kg | 1.5 kg | Long-range relay, BVLOS comms |
| **ISR + Starlink** | 1 kg | 1.5 kg | **2.5 kg** | Full BVLOS ISR capability |

**Note:** V2/V3/V4 specs below are scaled to support 2.5 kg payload (ISR + Starlink) while maintaining performance.

Sources: [Dronebotics Starlink Mini Test](https://en.dronebotics.nl/tested-starlink-mini-drone-applications/), [Event38 Starlink Integration](https://dronedj.com/2024/08/12/event38-adding-spacex-starlink-to-drones-for-bvlos-flights/)

---

## Version Overview

| Version | Type | Configuration | Wingspan | Length | AUW | Payload | Endurance | Speed | Propulsion | FC |
|---------|------|---------------|----------|--------|-----|---------|-----------|-------|------------|-----|
| **V0** | Fixed-Wing | Conventional pusher | 1.0-1.2m | 0.6m | 0.9 kg | 200g | 20-25 min | 54 km/h | 1x Electric | Pixhack / SpeedyBee F405 |
| **V1** | Fixed-Wing | Conventional pusher | 1.0-1.2m | 0.6m | **1.1 kg** | 300g | **45-50 min** | 54 km/h | 1x Electric | Pixhack / SpeedyBee F405 |
| **V1-ACAP** | Fixed-Wing | Conventional pusher | 1.0-1.2m | 0.6m | 0.86 kg | 200g | 20-25 min | 54 km/h | 1x Electric | **dRehmFlight + SBC** |
| **V1-LE** | Fixed-Wing | Conventional pusher | 1.8-2.0m | 0.9m | 1.5 kg | 300g | **2-2.5 hrs** | 45-50 km/h | 1x Electric | Pixhack / SpeedyBee F405 |
| **V1-Fast** | Fixed-Wing | Conventional pusher | 1.5-1.7m | 0.85m | 1.5 kg | 300g | 1-1.3 hrs | **55-65 km/h** | 1x Electric | Pixhack / SpeedyBee F405 |
| **V1-Fast 2hr** | Fixed-Wing | Conventional pusher | 2.2-2.4m | 1.1m | 2.1 kg | 500g | **2+ hrs** | **55-60 km/h** | 1x Electric | Pixhack / SpeedyBee F405 |
| **V1-VID** | Fixed-Wing | Conventional pusher | 1.0-1.2m | 0.6m | **1.15 kg** | 300g | **40-45 min** | 54 km/h | 1x Electric | Pixhack / SpeedyBee F405 |
| **V2** | Fixed-Wing | Alti-style twin-boom | **3.2m** | 2.4m | **12 kg** | **2.5 kg** | **3-4 hrs** | 70-80 km/h | 1x Electric | Pixhawk 6C |
| **V3** | VTOL | Alti-style QuadPlane | **3.2m** | 2.4m | **15 kg** | **2.5 kg** | **~3 hrs** | 70-75 km/h | 4+1 Electric | Pixhawk 6C |
| **V4** | VTOL | Alti-style QuadPlane | **3.2m** | 2.4m | **20 kg** | **2.5 kg** | **8-12 hrs** | 75 km/h | 4 Elec + Gas | Pixhawk 6X |

---

## V0 - Skills Development Platform

### Purpose
- Learn construction techniques with expendable materials
- Develop piloting and autopilot tuning skills
- Validate hardware integration
- Low-cost, low-risk experimentation

### Configuration: Conventional Pusher
```
    Top View:
                    ┌─────┐
                    │  V  │ ← Vertical stab
              ┌─────┴──┬──┴─────┐
              │   H-Stab        │ ← Horizontal stab
              └────────┼────────┘
                       │
                      [P] ← Pusher prop
                       │
              ┌────────┴────────┐
              │    Fuselage     │
              └────────┬────────┘
         ┌─────────────┼─────────────┐
         │            Wing           │
         └───────────────────────────┘


    Side View:
                     ╱│
                    ╱ │ V-stab
         ══════════╱══╧══[P]
           H-stab  │     Pusher
                   │
         ══════════╪══════════ Wing
                   │
              ┌────┴────┐
              │ Fuselage│
              └─────────┘
```

### Specifications
| Parameter | Value | Notes |
|-----------|-------|-------|
| Wingspan | 1.0-1.2m (40-48") | Trainer size |
| Length | 0.6m (24") | Compact |
| Chord | 150-180mm | ~15% thickness airfoil |
| Wing Area | 15-20 dm² | Low wing loading |
| Aspect Ratio | 6-7 | Forgiving flight characteristics |
| AUW | 800-1000g | With existing hardware |
| Wing Loading | 40-55 g/dm² | Easy handling |
| Cruise Speed | 12-18 m/s | Slow and stable |
| Stall Speed | ~8 m/s | Hand-launchable |
| Flight Time | 15-25 min | Conservative estimate |

### Existing Hardware (Use As-Is)
| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| Battery | 2200mAh 3S LiPo | 180g | $0 (owned) |
| Motor | 2212 920kv | 55g | $0 (owned) |
| ESC | 30A | 30g | $0 (owned) |
| Flight Controller | Pixhack | 40g | $0 (owned) |
| GPS | (existing) | 25g | $0 (owned) |
| Receiver | FS-IA6B | 10g | $0 (owned) |

### To Purchase
| Component | Model | Weight | Est. Cost |
|-----------|-------|--------|-----------|
| TX/RX | ELRS (RadioMaster Zorro + EP1) | - | $120-150 |
| Servos | 4x 9g micro (SG90 or MG90S) | 36g | $10-15 |
| Propeller | 9x6 or 10x4.5 pusher | 15g | $5-8 |
| Airframe Materials | Foam board, hot glue, tape | ~400g | $20-30 |

### Construction Materials (Local/Cheap)
- **Wing:** Dollar Tree foam board or Depron (3-5mm)
- **Fuselage:** Foam board box construction
- **Reinforcement:** Bamboo skewers, popsicle sticks, fiberglass tape
- **Covering:** Packing tape or heat shrink film
- **Adhesive:** Hot glue, foam-safe CA

### Weight Budget
| Component | Mass (g) | % |
|-----------|----------|---|
| Airframe (foam) | 300-350 | 35% |
| Battery | 180 | 20% |
| Motor + Prop | 70 | 8% |
| ESC | 30 | 3% |
| FC + GPS | 65 | 7% |
| Receiver | 10 | 1% |
| Servos (4x) | 36 | 4% |
| Wiring/Hardware | 50 | 5% |
| **Margin** | 150 | 17% |
| **Total** | ~900g | 100% |

### V0 Budget Summary
| Category | Cost |
|----------|------|
| Existing Hardware | $0 |
| ELRS TX/RX | $130 |
| Servos | $12 |
| Propellers (3x) | $15 |
| Foam/Materials | $25 |
| Misc Hardware | $20 |
| **Total** | **~$200** |

---

## V1 - Durable Construction Platform

### Purpose
- Transition to permanent construction techniques
- Test camera and gimbal configurations
- Refine autopilot tuning
- Develop repeatable build processes

### Configuration
Same as V0: conventional pusher fixed-wing with upgraded construction.

### Specifications
| Parameter | Value | Notes |
|-----------|-------|-------|
| Wingspan | 1.0-1.2m | Same as V0 |
| Length | 0.6m | Same as V0 |
| **AUW** | **~1100g** | **Larger battery** |
| **Battery** | **3S 5000mAh (55 Wh)** | **Upgrade from V0** |
| **Flight Time** | **45-50 min** | **Nearly 2x V0 endurance** |

### Construction Upgrade
| V0 Material | V1 Upgrade | Benefit |
|-------------|------------|---------|
| Foam board | Depron/EPP + carbon spar | Durability, stiffness |
| Packing tape | Heat shrink film (Oracover) | Cleaner surface, lighter |
| Hot glue | Epoxy + foam-safe CA | Stronger joints |
| Bamboo skewers | Carbon fiber tubes/rods | Strength-to-weight |

### Camera Test Configurations
| Config | Camera | Gimbal | Weight | Purpose |
|--------|--------|--------|--------|---------|
| A | GoPro (bare) | Fixed mount | 120g | Baseline video |
| B | RunCam 5 Orange | Fixed mount | 60g | Lighter option |
| C | Caddx Peanut | 2-axis micro gimbal | 100g | Stabilized FPV |
| D | Sony RX0 II | 2-axis brushless | 200g | High-quality stills |

### Gimbal Options to Test
| Gimbal | Axes | Payload | Weight | Cost |
|--------|------|---------|--------|------|
| FeiyuTech Mini 3D | 3 | 200g | 85g | $80 |
| Tarot T-2D | 2 | 200g | 110g | $60 |
| Custom micro (3D printed) | 2 | 100g | 50g | $30 |

### V1 Additional Budget
| Item | Cost |
|------|------|
| Depron/EPP sheets | $30 |
| Carbon tubes/rods | $25 |
| Heat shrink covering | $20 |
| Test cameras (2-3) | $150-300 |
| Micro gimbal | $60-80 |
| **Total Additional** | **~$350** |

---

## V1-ACAP - As Cheap As Possible (dRehmFlight + SBC)

### Purpose
- **Custom autopilot stack** at fraction of commercial FC cost
- Full autopilot capability (GPS, waypoints, RTH) via programming
- Learn flight control fundamentals from the ground up
- Complete code access for customization
- Platform for experimental navigation algorithms

### Architecture: Two-Layer Control System

```
┌─────────────────────────────────────────────────────────────────┐
│                    OUTER LOOP (Navigation)                       │
│                    SBC (RPi / ESP32 / Orange Pi)                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  • GPS waypoint navigation                              │    │
│  │  • Return-to-home logic                                 │    │
│  │  • Mission planning                                     │    │
│  │  • Telemetry (WiFi/cellular)                           │    │
│  │  • Position hold                                        │    │
│  │  • Geofencing                                           │    │
│  │  • Failsafe decisions                                   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                     Serial (UART)                                │
│                   Roll/Pitch/Yaw/Throttle commands               │
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

This is the **same architecture** used by professional autopilots:
- **Pixhawk**: STM32 (inner loop) + optional companion computer (outer loop)
- **DJI**: Dedicated ASIC (inner) + ARM processor (outer)
- **V1-ACAP**: Teensy (inner) + SBC (outer)

### Full Autopilot Capabilities

With SBC + GPS + custom code, V1-ACAP provides:
- ✅ GPS waypoint navigation
- ✅ Return-to-home (RTH)
- ✅ Autonomous missions
- ✅ Failsafe RTL
- ✅ Position hold / loiter
- ✅ Geofencing
- ✅ Telemetry (WiFi, cellular, radio)
- ✅ Ground station connectivity
- ✅ Full code access (Python/C++/MicroPython)

### Hardware

#### SBC Options (Navigation Computer)

| SBC | CPU | RAM | WiFi | Weight | Cost | Notes |
|-----|-----|-----|------|--------|------|-------|
| **Raspberry Pi Zero 2W** | 1GHz Quad | 512MB | Yes | 10g | $15 | Best Linux support |
| **ESP32-S3** | 240MHz Dual | 512KB | Yes | 3g | $8 | Lowest power, MicroPython |
| **Orange Pi Zero 3** | 1.5GHz Quad | 1GB | Yes | 26g | $20 | More RAM, faster |
| **Radxa Zero** | 1.8GHz Quad | 1-4GB | Yes | 10g | $25 | RPi-compatible, faster |
| **Milk-V Duo** | 1GHz RISC-V | 64MB | No | 5g | $9 | Ultra-light, limited |
| **Seeed XIAO ESP32S3** | 240MHz | 8MB | Yes | 3g | $13 | Tiny, camera support |

**Recommended:** RPi Zero 2W (best balance) or ESP32-S3 (ultra-light/cheap)

#### Flight Control Stack
| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| **Inner Loop FC** | Teensy 4.0 | 5g | $24 |
| **IMU** | MPU6050 (GY-521) or MPU9250 | 3g | $3-8 |
| **Outer Loop Computer** | SBC (see table above) | 3-26g | $8-25 |
| **GPS** | BN-880 (GPS + compass) | 10g | $15 |
| **Barometer** | BMP280 (optional) | 1g | $3 |
| **Subtotal (FC stack)** | | **22-45g** | **$53-75** |

#### Comparison: FC Stack Cost
| Solution | Weight | Cost | Code Access |
|----------|--------|------|-------------|
| **V1-ACAP (Teensy + ESP32-S3 + GPS)** | 22g | **$50** | ✅ Full (C++/MicroPython) |
| **V1-ACAP (Teensy + RPi Zero 2W + GPS)** | 29g | **$57** | ✅ Full (Python/C++) |
| SpeedyBee F405 Wing + GPS | 35g | $65 | ⚠️ Config only |
| Pixhawk 6C Mini + GPS | 50g | $260 | ⚠️ ArduPilot params |
| Pixhawk 6C + GPS | 80g | $325 | ⚠️ ArduPilot params |

#### Complete Aircraft
| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| **FC Stack** | Teensy + SBC + GPS | 22-29g | $50-57 |
| **Receiver** | FS-IA6B (PPM/iBUS) | 10g | $12 |
| **Motor** | 2212 920kv (generic) | 55g | $8 |
| **ESC** | 30A SimonK/BLHeli | 25g | $8 |
| **Battery** | 3S 2200mAh | 180g | $18 |
| **Servos** | 4x SG90 (9g micro) | 36g | $6 |
| **Propeller** | 9x6 pusher | 15g | $3 |
| **Airframe** | Foam board (Dollar Tree) | 300g | $10 |
| **Misc** | Wires, connectors, hot glue | 30g | $8 |

### System Wiring

```
                        ┌──────────────────┐
                        │       SBC        │
                        │  (RPi/ESP32/etc) │
                        │                  │
    BN-880 GPS ────────►│ UART (GPS)       │
    (TX/RX)             │                  │
                        │ UART (Teensy) ───┼────► Teensy 4.0
                        │                  │      (Serial1)
    WiFi Telemetry ◄────│ WiFi             │
    (Ground Station)    │                  │
                        │ GPIO ────────────┼────► Status LED
                        │                  │
                        │ 5V ◄─────────────┼──── BEC (from ESC)
                        └──────────────────┘

                        ┌──────────────────┐
                        │    Teensy 4.0    │
                        │   (dRehmFlight)  │
                        │                  │
    SBC Commands ──────►│ Serial1 (RX)     │
                        │                  │
    MPU6050 ───────────►│ I2C (SDA/SCL)    │
                        │                  │
    RC Receiver ───────►│ Pins 15-18 (PPM) │
                        │                  │
                        │ Pin 0 ───────────┼────► Aileron L
                        │ Pin 1 ───────────┼────► Aileron R
                        │ Pin 2 ───────────┼────► Elevator
                        │ Pin 3 ───────────┼────► Rudder
                        │ Pin 4 ───────────┼────► ESC
                        │                  │
                        │ 5V ◄─────────────┼──── BEC
                        └──────────────────┘

Power Distribution:
    Battery 3S ──► ESC ──► BEC 5V ──┬──► Teensy VIN
                         │          ├──► SBC 5V
                         │          ├──► GPS VCC
                         │          └──► Servos
                         └──► Motor
```

### Software Stack

#### Teensy (Inner Loop) - dRehmFlight Modified

```cpp
// dRehmFlight modifications for SBC integration

// Add serial command reception
void loop() {
    // Check for commands from SBC
    if (Serial1.available()) {
        parseSBCCommand();  // Roll, pitch, yaw, throttle targets
    }

    // Original dRehmFlight stabilization loop
    getIMUdata();
    calculateAttitude();
    controlMixer();

    // Output to servos/ESC
    commandServos();
}

void parseSBCCommand() {
    // SBC sends: $CMD,roll,pitch,yaw,throttle,mode*checksum
    // Mode: 0=manual, 1=stabilize, 2=auto (accept SBC commands)

    if (flightMode == AUTO) {
        // Use SBC navigation commands as setpoints
        roll_setpoint = sbc_roll_cmd;
        pitch_setpoint = sbc_pitch_cmd;
        yaw_setpoint = sbc_yaw_cmd;
        throttle_setpoint = sbc_throttle_cmd;
    } else {
        // Use RC receiver inputs
        roll_setpoint = rc_roll;
        pitch_setpoint = rc_pitch;
        // ...
    }
}
```

#### SBC (Outer Loop) - Python Example

```python
# autopilot.py - Navigation controller (runs on any Linux SBC)

import serial
from dataclasses import dataclass
from typing import List
import math

@dataclass
class Waypoint:
    lat: float
    lon: float
    alt: float

class NavigationController:
    def __init__(self, teensy_port='/dev/ttyS0', gps_port='/dev/ttyAMA0'):
        self.teensy = serial.Serial(teensy_port, 115200)
        self.gps = serial.Serial(gps_port, 9600)
        self.home_position = None
        self.waypoints: List[Waypoint] = []
        self.current_wp_idx = 0

    def update(self):
        """Main navigation loop - runs at 10-50 Hz"""
        pos = self.parse_gps()

        if self.mode == 'RTH':
            target = self.home_position
        elif self.mode == 'WAYPOINT':
            target = self.waypoints[self.current_wp_idx]
        else:
            return  # Manual mode, no commands

        # Calculate bearing and distance to target
        bearing = self.calc_bearing(pos, target)
        distance = self.calc_distance(pos, target)

        # Simple navigation controller
        heading_error = bearing - pos.heading
        roll_cmd = self.heading_pid.update(heading_error)

        # Altitude hold
        alt_error = target.alt - pos.alt
        pitch_cmd = self.alt_pid.update(alt_error)

        # Send commands to Teensy
        self.send_command(roll_cmd, pitch_cmd, 0, self.cruise_throttle)

        # Check if waypoint reached
        if distance < 20:  # 20m threshold
            self.current_wp_idx += 1

    def send_command(self, roll, pitch, yaw, throttle):
        """Send attitude commands to Teensy"""
        msg = f"$CMD,{roll:.2f},{pitch:.2f},{yaw:.2f},{throttle:.2f}*\n"
        self.teensy.write(msg.encode())

    def failsafe_check(self):
        """Return to home if signal lost"""
        if self.rc_signal_lost() or self.gps_fix_lost():
            self.mode = 'RTH'
```

#### ESP32-S3 (Outer Loop) - MicroPython Example

```python
# main.py - Navigation controller for ESP32-S3

from machine import UART, Pin
import time

class SimpleAutopilot:
    def __init__(self):
        self.teensy = UART(1, baudrate=115200, tx=17, rx=18)
        self.gps = UART(2, baudrate=9600, tx=43, rx=44)
        self.home_lat = None
        self.home_lon = None

    def parse_nmea(self, line):
        """Parse GPRMC sentence for position"""
        if line.startswith('$GPRMC'):
            parts = line.split(',')
            if parts[2] == 'A':  # Valid fix
                lat = float(parts[3][:2]) + float(parts[3][2:])/60
                lon = float(parts[5][:3]) + float(parts[5][3:])/60
                return lat, lon
        return None, None

    def send_to_teensy(self, roll, pitch, yaw, throttle):
        cmd = f"$CMD,{roll},{pitch},{yaw},{throttle}*\n"
        self.teensy.write(cmd.encode())

    def run(self):
        while True:
            # Read GPS
            if self.gps.any():
                line = self.gps.readline().decode()
                lat, lon = self.parse_nmea(line)
                if lat and self.home_lat is None:
                    self.home_lat, self.home_lon = lat, lon

            # Navigation logic here...
            time.sleep_ms(50)  # 20 Hz loop
```

### Weight Budget

| Component | Mass (g) | % |
|-----------|----------|---|
| Airframe (foam) | 300 | 35% |
| Battery (3S 2200mAh) | 180 | 21% |
| Motor + Prop | 70 | 8% |
| ESC | 25 | 3% |
| Teensy 4.0 + MPU6050 | 8 | 1% |
| **SBC (RPi Zero 2W)** | 10 | 1% |
| **GPS (BN-880)** | 10 | 1% |
| Receiver | 10 | 1% |
| Servos (4x) | 36 | 4% |
| Wiring/Hardware | 60 | 7% |
| **Margin** | 150 | 17% |
| **Total** | ~860g | 100% |

### V1-ACAP Budget Summary

| Category | Cost |
|----------|------|
| Teensy 4.0 | $24 |
| MPU6050 module | $3 |
| **SBC (RPi Zero 2W or ESP32-S3)** | $8-15 |
| **BN-880 GPS** | $15 |
| Receiver (FS-IA6B) | $12 |
| Motor (2212 920kv) | $8 |
| ESC (30A) | $8 |
| Battery (3S 2200mAh) | $18 |
| Servos (4x SG90) | $6 |
| Propeller | $3 |
| Foam board + materials | $10 |
| Misc (wires, connectors) | $8 |
| **Total** | **~$125-130** |

### Comparison: V1-ACAP vs Commercial Solutions

| Aspect | V1-ACAP ($130) | SpeedyBee F405 ($180) | Pixhawk 6C ($400+) |
|--------|----------------|----------------------|-------------------|
| **Autopilot** | ✅ Full custom | ✅ iNav/ArduPilot | ✅ ArduPilot |
| **GPS Navigation** | ✅ Custom code | ✅ Built-in | ✅ Built-in |
| **Failsafe RTL** | ✅ Custom code | ✅ Built-in | ✅ Built-in |
| **Autonomous** | ✅ Python/C++ | ✅ Mission Planner | ✅ Mission Planner |
| **Telemetry** | ✅ WiFi/cellular | ⚠️ Radio only | ⚠️ Radio only |
| **Code Access** | ✅ **Full** | ❌ Config only | ❌ Config only |
| **Custom Algorithms** | ✅ **Unlimited** | ❌ Limited | ❌ Limited |
| **Learning Value** | ✅ **Maximum** | ⚠️ Configuration | ⚠️ Configuration |
| **Community Support** | ⚠️ DIY | ✅ Large | ✅ Large |
| **Reliability** | ⚠️ Depends on code | ✅ Proven | ✅ Proven |

### When to Choose V1-ACAP

✅ **Good for:**
- Learning autopilot development from scratch
- Custom navigation algorithms
- Research/experimental platforms
- Adding features not in commercial FCs
- WiFi/cellular telemetry integration
- Computer vision integration (SBC camera)
- Machine learning experiments
- Maximum flexibility and control
- Cost-sensitive full-autopilot builds

⚠️ **Consider alternatives if:**
- You need proven, reliable autopilot quickly
- Limited programming experience
- Production/commercial use
- Time-constrained project

### Development Roadmap for V1-ACAP Software

```
Phase 1: Basic Stabilization (Week 1-2)
├── Flash dRehmFlight to Teensy
├── Tune PID for your airframe
├── Verify stable manual flight
└── Test angle mode (self-leveling)

Phase 2: SBC Integration (Week 3-4)
├── Set up SBC (RPi/ESP32)
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
├── Mission upload/download
├── Real-time map display
└── Command interface
```

### Resources

- **dRehmFlight GitHub:** https://github.com/nickrehm/dRehmFlight
- **dRehmFlight Documentation:** https://cdn.hackaday.io/files/1747687477274112/dRehmFlight%20VTOL%20Documentation.pdf
- **Teensy 4.0:** https://www.pjrc.com/store/teensy40.html
- **RPi Zero 2W:** https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/
- **ESP32-S3 MicroPython:** https://docs.micropython.org/en/latest/esp32/quickref.html
- **BN-880 GPS Datasheet:** https://www.u-blox.com/en/product/neo-m8-series

---

## V1 Variants - Speed vs Endurance Trade-offs

The base V1 can be scaled for different mission profiles. Three variants are documented below.

### Power vs Speed Relationship

Power required increases significantly with speed (roughly V² to V³):

| Cruise Speed | Power Required | Endurance (74Wh battery) |
|--------------|----------------|--------------------------|
| 12 m/s (43 km/h) | ~25W | 2.4 hrs |
| 14 m/s (50 km/h) | ~32W | 1.8 hrs |
| 15 m/s (54 km/h) | ~40W | 1.5 hrs |
| 17 m/s (61 km/h) | ~55W | 1.1 hrs |
| 20 m/s (72 km/h) | ~80W | 0.7 hrs |

### V1 Variant Comparison

| Parameter | V1 (Base) | V1-LE (Long Endurance) | V1-Fast | V1-Fast 2hr |
|-----------|-----------|------------------------|---------|-------------|
| **Purpose** | Skills/Training | Max endurance | Speed + agility | Speed + endurance |
| **Wingspan** | 1.0-1.2m | 1.8-2.0m | 1.5-1.7m | 2.2-2.4m |
| **Length** | 0.6m | 0.9-1.0m | 0.8-0.9m | 1.1-1.2m |
| **Wing Area** | 15-18 dm² | 35-40 dm² | 25-30 dm² | 40-45 dm² |
| **Aspect Ratio** | 6-7 | 9-10 | 8-9 | 10-11 |
| **AUW** | 0.9 kg | 1.4-1.6 kg | 1.4-1.6 kg | 2.0-2.2 kg |
| **Wing Loading** | 50 g/dm² | 40 g/dm² | 55-60 g/dm² | 50 g/dm² |
| **Battery** | 3S 2200mAh | 4S 5000mAh | 4S 4000mAh | 6S 5000mAh |
| **Battery Capacity** | 24 Wh | 74 Wh | 59 Wh | 111 Wh |
| **Motor** | 2212 920kv | 2212 1000kv | 2212 1000kv | 2216 900kv |
| **Cruise Speed** | 15 m/s (54 km/h) | 12-14 m/s (43-50 km/h) | 15-17 m/s (55-65 km/h) | 15-17 m/s (55-60 km/h) |
| **Cruise Power** | ~40W | 25-30W | 45-50W | ~50W |
| **Endurance** | 25-30 min | 2-2.5 hrs | 1.0-1.3 hrs | 2+ hrs |
| **Payload** | 200-300g | 300g | 300g | 400-500g |

### V1-LE: Long Endurance Variant

Optimized for maximum flight time at slow cruise speeds.

```
    V1-LE (1.8-2.0m wingspan)

              ┌────┐
    ══════════╪════╧════[P]
              │
    ══════════╪════════════════
              └────┘

    - High aspect ratio (9-10) for best L/D
    - Low wing loading (40 g/dm²) for efficiency
    - Slow cruise (43-50 km/h) minimizes power
    - 2+ hour endurance
```

#### V1-LE Specifications
| Parameter | Value | Notes |
|-----------|-------|-------|
| Wingspan | 1.8-2.0m | High AR for efficiency |
| Length | 0.9-1.0m | Proportional scaling |
| Wing Area | 35-40 dm² | Large for low wing loading |
| Aspect Ratio | 9-10 | Optimized for L/D |
| AUW | 1.4-1.6 kg | With 4S 5000mAh |
| Wing Loading | 40 g/dm² | Low for efficiency |
| L/D (cruise) | 12-14 | High efficiency |
| Cruise Speed | 12-14 m/s (43-50 km/h) | Slow for endurance |
| Stall Speed | 8-9 m/s | Hand-launchable |
| Cruise Power | 25-30W | Efficient cruise |
| Endurance | 2-2.5 hrs | Primary advantage |

#### V1-LE Hardware
| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| Motor | 2212 1000kv | 55g | $15 |
| ESC | 30A BLHeli | 30g | $0 (existing) |
| Battery | 4S 5000mAh 35C | 450g | $45 |
| Propeller | 11x7 or 12x6 | 20g | $8 |
| Servos | 4x 9g | 36g | $0 (existing) |
| FC | Pixhack | 40g | $0 (existing) |
| GPS | Existing | 25g | $0 (existing) |
| Receiver | ELRS | 5g | $0 (existing) |

#### V1-LE Budget
| Item | Cost |
|------|------|
| V1 base investment | $550 |
| Larger battery (4S 5000mAh) | $45 |
| Motor upgrade (optional) | $15 |
| Larger propeller | $8 |
| Additional airframe materials | $40 |
| **Total** | **~$660** |

---

### V1-Fast: Speed-Optimized Variant

Balanced design for higher cruise speed with acceptable endurance.

```
    V1-Fast (1.5-1.7m wingspan)

            ┌───┐
    ════════╪═══╧═══[P]
            │
    ════════╪═══════════
            └───┘

    - Moderate aspect ratio (8-9)
    - Higher wing loading (55-60 g/dm²)
    - Fast cruise (55-65 km/h)
    - Better wind penetration
    - 1.0-1.3 hour endurance
```

#### V1-Fast Specifications
| Parameter | Value | Notes |
|-----------|-------|-------|
| Wingspan | 1.5-1.7m | Compact, agile |
| Length | 0.8-0.9m | Proportional |
| Wing Area | 25-30 dm² | Smaller, faster |
| Aspect Ratio | 8-9 | Balance of efficiency/handling |
| AUW | 1.4-1.6 kg | Similar to V1-LE |
| Wing Loading | 55-60 g/dm² | Higher for speed |
| L/D (cruise) | 10-12 | Good efficiency |
| Cruise Speed | 15-17 m/s (55-65 km/h) | Fast cruise |
| Stall Speed | 10-11 m/s | Needs launcher or runway |
| Cruise Power | 45-50W | Higher power cruise |
| Endurance | 1.0-1.3 hrs | Acceptable |

#### V1-Fast Hardware
| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| Motor | 2212 1000kv | 55g | $15 |
| ESC | 30A BLHeli | 30g | $0 (existing) |
| Battery | 4S 4000mAh 45C | 380g | $40 |
| Propeller | 10x6 or 11x5.5 | 18g | $8 |
| Servos | 4x 9g | 36g | $0 (existing) |
| FC | Pixhack | 40g | $0 (existing) |

#### V1-Fast Budget
| Item | Cost |
|------|------|
| V1 base investment | $550 |
| Battery (4S 4000mAh) | $40 |
| Motor upgrade (optional) | $15 |
| Propeller | $8 |
| Airframe materials | $35 |
| **Total** | **~$650** |

---

### V1-Fast 2hr: Speed + Endurance Variant

Scaled up for both high speed and long endurance.

```
    V1-Fast 2hr (2.2-2.4m wingspan)

                ┌─────┐
    ════════════╪═════╧═════[P]
                │
    ════════════╪══════════════════
                └─────┘

    - High aspect ratio (10-11)
    - Moderate wing loading (50 g/dm²)
    - Fast cruise (55-60 km/h) AND 2+ hour endurance
    - Largest V1 variant
    - Requires motor upgrade to 2216
```

#### V1-Fast 2hr Specifications
| Parameter | Value | Notes |
|-----------|-------|-------|
| Wingspan | 2.2-2.4m | Large platform |
| Length | 1.1-1.2m | Proportional |
| Wing Area | 40-45 dm² | Large wing area |
| Aspect Ratio | 10-11 | High efficiency |
| AUW | 2.0-2.2 kg | Heavier with big battery |
| Wing Loading | 50 g/dm² | Moderate |
| L/D (cruise) | 12-14 | High efficiency |
| Cruise Speed | 15-17 m/s (55-60 km/h) | Fast |
| Stall Speed | 10-11 m/s | Needs launcher |
| Cruise Power | ~50W | Efficient at speed |
| Endurance | 2+ hrs | Large battery |
| Payload | 400-500g | Increased capacity |

#### V1-Fast 2hr Hardware
| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| Motor | 2216 900kv | 68g | $25 |
| ESC | 40A BLHeli_32 | 35g | $20 |
| Battery | 6S 5000mAh 35C | 620g | $70 |
| Propeller | 12x6 or 13x6.5 | 25g | $12 |
| Servos | 4x 12g digital | 48g | $25 |
| FC | Pixhack | 40g | $0 (existing) |

#### V1-Fast 2hr Budget
| Item | Cost |
|------|------|
| V1 base investment | $550 |
| Motor (2216 900kv) | $25 |
| ESC upgrade (40A) | $20 |
| Battery (6S 5000mAh) | $70 |
| Propeller | $12 |
| Servos upgrade | $25 |
| Additional airframe materials | $60 |
| **Total** | **~$760** |

---

### V1-VID: RunCam WifiLink (OpenIPC) Communication System

Adds production-ready HD video and telemetry using RunCam WifiLink based on OpenIPC firmware.

```
    V1-VID (RunCam WifiLink / OpenIPC)

              ┌───┐
    ══════════╪═══╧═══[P]
              │
    ══════════╪══════════
              └───┘
         [WifiLink VTX]

    - Same V1 airframe
    - RunCam WifiLink replaces analog video + separate telemetry
    - Production-ready 1080p @ 90fps HD video
    - Integrated MAVLink telemetry
    - Low cost: $70-115 for complete air unit
```

#### Purpose
- Develop long-range HD video and telemetry capability
- Production-ready alternative to DIY OpenHD builds
- Foundation for V2/V3 communication architecture
- Learn digital FPV and OpenIPC ecosystem

#### RunCam WifiLink System Overview

| Feature | Specification |
|---------|---------------|
| Video | **1080p HD @ 90fps** |
| Sensor | Sony IMX415 |
| FOV | 160° |
| Latency | Low (digital FPV optimized) |
| Telemetry | MAVLink integrated via UART |
| Frequency | 5.8 GHz WiFi (5180-5885 MHz) |
| TX Power | 630mW (FCC) / 100mW (CE) |
| Protocol | OpenIPC / WFB-NG |

#### Hardware

##### Air Unit (RunCam WifiLink 2)
| Component | Specs | Weight | Cost |
|-----------|-------|--------|------|
| WifiLink 2 VTX | IMX415, 1080p90, 9-22V | 30g | $90 |
| Lens | M12, 160° FOV, Vista compatible | incl. | incl. |
| Antennas | Dual IPEX, 5.8GHz | 5g | incl. |
| Mounting | 25.5mm × 25.5mm (M2) | - | incl. |
| **Air Unit Total** | 30.6mm × 33mm PCB | **~35g** | **~$90** |

##### Ground Station Options

**Option A: Mobile/Tablet (Recommended for V1)**
| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| WiFi Adapter | RTL8812AU USB | 15g | $25 |
| Android Device | Phone/Tablet (Android 13+) | - | (owned) |
| App | PixelPilot | - | Free |
| **GS Total (Mobile)** | | **~15g** | **~$25** |

**Option B: Dedicated Receiver**
| Component | Model | Weight | Cost |
|-----------|-------|--------|------|
| RunCam WifiLink-RX | HDMI out, supports goggles | 50g | $80 |
| Display/Goggles | Any HDMI input | varies | varies |
| **GS Total (Dedicated)** | | **~50g** | **~$80** |

#### Weight Budget (V1-VID)

| Component | Mass (g) | % |
|-----------|----------|---|
| V1 Airframe (foam) | 300 | 31% |
| Battery (3S 2200mAh) | 180 | 19% |
| Motor + Prop | 70 | 7% |
| ESC | 30 | 3% |
| FC + GPS | 65 | 7% |
| Servos (4x) | 36 | 4% |
| **WifiLink Air Unit** | **35** | **4%** |
| Wiring/Hardware | 50 | 5% |
| **Margin** | 194 | 20% |
| **Total** | ~960g | 100% |

#### V1-VID Budget

| Category | Cost |
|----------|------|
| V1 base investment | $550 |
| WifiLink 2 VTX/Cam | $90 |
| RTL8812AU adapter | $25 |
| **Total (Mobile GS)** | **~$665** |
| | |
| *Or with dedicated RX:* | |
| WifiLink-RX | +$80 |
| **Total (Dedicated GS)** | **~$720** |

#### ArduPilot Integration

```
# WifiLink connects via UART for MAVLink telemetry
SERIALx_PROTOCOL = 2      # MAVLink2
SERIALx_BAUD = 115200
```

WifiLink provides:
- Bidirectional MAVLink telemetry
- 1080p @ 90fps HD video stream
- OSD overlay support
- RSSI and link quality monitoring
- Low-latency digital FPV

#### Reference Documentation

- [RunCam WifiLink Store](https://shop.runcam.com/runcam-wifilink2-based-on-openipc/)
- [OpenIPC Documentation](https://docs.openipc.org/hardware/runcam/vtx/runcam-wifilink-v2/)
- [Long Range Video Guide](../systems/LONG_RANGE_VIDEO_GUIDE.md) for DIY alternatives

---

### V1 Modular Wing System

Rather than building separate aircraft, use **one fuselage with interchangeable wings** to optimize for different missions.

```
    MODULAR V1 CONCEPT

    Same Fuselage + Tail:
              ┌───┐
              │ F │══[P]
              │ U │
              │ S │
              └─┬─┘

    + Interchangeable Wings:

    LE Wing (1.8-2.0m):        Fast Wing (1.5-1.7m):       Base Wing (1.0-1.2m):
    ════════════════════       ══════════════════          ════════════════
         Endurance                  Speed                    Training
```

#### Wing Set Options

| Wing | Span | Area | Wing Loading | Speed | Endurance | Build Cost |
|------|------|------|--------------|-------|-----------|------------|
| **Base Wing** | 1.0-1.2m | 15-18 dm² | 50 g/dm² | 54 km/h | 25-30 min | $30 |
| **LE Wing** | 1.8-2.0m | 35-40 dm² | 40 g/dm² | 45-50 km/h | 2-2.5 hrs | $60 |
| **Fast Wing** | 1.5-1.7m | 25-30 dm² | 55 g/dm² | 55-65 km/h | 1-1.3 hrs | $45 |

#### Design Requirements for Modularity

1. **Common wing spar interface** - Same mounting system for all wings
2. **Wing spar tube** - 12mm carbon tube passes through fuselage
3. **Quick-release mechanism** - Nylon bolts or wing tube rubber bands
4. **Servo wiring** - Standardized aileron servo connectors
5. **CG adjustment** - Battery position shifts to maintain balance

#### Fuselage Design for Wing Swaps

```
    Fuselage Cross-Section:

         Wing Spar Tube (12mm)
              ┌─────┐
    ══════════╪═════╪══════════  ← Wing slides onto tube
              │     │
              │ [B] │  ← Battery slides fore/aft for CG
              │     │
              └─────┘
```

| Wing Installed | Battery Position | CG Location |
|----------------|------------------|-------------|
| Base (1.0-1.2m) | Center | 25-30% MAC |
| LE (1.8-2.0m) | Forward | 25-30% MAC |
| Fast (1.5-1.7m) | Slightly forward | 25-30% MAC |

#### Cost Savings: Modular vs Separate Aircraft

| Approach | Components | Total Cost |
|----------|------------|------------|
| **3 Separate Aircraft** | 3 fuselages, 3 tails, 3 wings | ~$450 materials |
| **1 Modular Aircraft** | 1 fuselage, 1 tail, 3 wings | ~$180 materials |
| **Savings** | | **~$270** |

#### Modular V1 Complete Kit

| Component | Cost |
|-----------|------|
| V1 Base (fuselage + tail + base wing) | $550 |
| LE Wing add-on | +$60 |
| Fast Wing add-on | +$45 |
| Larger battery (4S 5000mAh) for LE | +$45 |
| **Total Modular System** | **~$700** |

This gives you **3 mission profiles** with one aircraft and interchangeable wings.

---

### V1 Variant Selection Guide

| Mission Profile | Wing | Key Trade-off |
|-----------------|------|---------------|
| Training/Learning | Base (1.0-1.2m) | Cheap, expendable |
| Aerial photography (calm) | LE (1.8-2.0m) | Max loiter time |
| Aerial photography (windy) | Fast (1.5-1.7m) | Better wind handling |
| Long-range mapping | LE (1.8-2.0m) | Maximize coverage time |
| Camera/gimbal testing | LE or Fast | Either works |
| Autonomous waypoint missions | LE (1.8-2.0m) | Maximize coverage time |
| Quick inspection flights | Fast (1.5-1.7m) | Get there fast |

### V1 Variant Progression

```
                         V1 (Base)
                        1.0-1.2m, 30min
                             │
        ┌────────────────────┼────────────────────┬────────────────────┐
        │                    │                    │                    │
        ▼                    ▼                    ▼                    ▼
    V1-LE              V1-Fast            V1-Fast 2hr            V1-VID
   1.8-2.0m           1.5-1.7m             2.2-2.4m             1.0-1.2m
   2+ hrs             1.0-1.3 hrs          2+ hrs               25-30 min
   45-50 km/h         55-65 km/h           55-60 km/h           54 km/h
     $660               $650                 $760           $665 (WifiLink)
        │                                                          │
        │   ┌─────────────────────────────────────┐                │
        │   │  ALTERNATIVE (custom autopilot):    │                │
        │   │                                     │                ▼
        │   │    V1-ACAP (dRehmFlight + SBC)      │        ┌───────────────┐
        │   │    1.0-1.2m, full code access       │        │ Foundation    │
        │   │    $130 - Custom autopilot stack    │        │ for V2/V3     │
        │   └─────────────────────────────────────┘        │ comm system   │
                                                           └───────────────┘
```

---

## V2 - ALTI-Style Twin-Boom Pusher (Fixed-Wing)

### Purpose
- Develop full-scale ALTI-style airframe
- Test twin-boom structural design
- Validate aerodynamics at scale
- Prepare airframe for V3 VTOL conversion

### Configuration: ALTI Transition Style
```
    Top View:

    ┌───────────────────────────────────────────────────────┐
    │                        WING                           │
    │                      (3.0m span)                      │
    └───────────┬───────────────────────────────┬───────────┘
                │                               │
         ┌──────┴──────┐                 ┌──────┴──────┐
         │    BOOM     │                 │    BOOM     │
         │   (Left)    │                 │   (Right)   │
         │             │   ┌─────────┐   │             │
         │             │   │         │   │             │
         │             │   │ FUSELAGE│   │             │
         │             │   │ (center)│   │             │
         │             │   │         │   │             │
         │             │   │   [P]   │   │             │  ← Pusher
         │             │   │  Motor  │   │             │
         │             │   └─────────┘   │             │
         │             │                 │             │
         └──────┬──────┘                 └──────┬──────┘
                │                               │
                ╲                               ╱
                 ╲                             ╱
                  ╲───────────────────────────╱
                          Inverted V-Tail


    Side View:

                                    ╱
                                   ╱ V-tail
    ═══════════════════════════════╱════════
              Wing                 │   Boom
                                   │
              ┌────────────────────┤
              │     Fuselage       │
              │        [P]─────────┤ Pusher
              └────────────────────┘


    Front View:

                  3.0m wingspan
    ←─────────────────────────────────────────→

         ╲                               ╱
          ╲                             ╱
           ╲                           ╱
    ════════╲═════════════════════════╱════════
             ╲         │             ╱
              ╲   ┌────┴────┐       ╱
               ╲  │ Fuselage│      ╱
                ╲ │   [P]   │     ╱
                 ╲└─────────┘    ╱
                  ╲             ╱
                   ╲    ▼▼▼    ╱  ← Inverted V-tail
                    ╲         ╱
                     ╲       ╱

    Length: 2.3m (nose to tail)
```

### Specifications (Scaled for Starlink + ISR Payload)
| Parameter | Value | Notes |
|-----------|-------|-------|
| Wingspan | **3.2m (126")** | Scaled up for payload |
| Length | **2.4m (94")** | Proportional |
| Chord | 270-320mm | ~12-15% thickness |
| Wing Area | **90-105 dm²** | Increased for higher AUW |
| Aspect Ratio | 10-11 | High efficiency |
| AUW | **12 kg** | Scaled for 2.5 kg payload |
| Wing Loading | 115-135 g/dm² | Moderate loading |
| Cruise Speed | 19-22 m/s (70-80 km/h) | Optimized for endurance |
| Stall Speed | 13-15 m/s | Requires runway/launcher |
| **Endurance** | **3-4 hours** | No VTOL weight penalty |
| **Payload Capacity** | **2.5 kg** | ISR (1 kg) + Starlink (1.5 kg) |

### Why V2 Exceeds VTOL Endurance
The ALTI Transition VTOL achieves 3+ hours. V2 as pure fixed-wing saves:
- No VTOL motors: -660g
- No VTOL ESCs: -160g
- No VTOL arms/mounts: -300g
- No hover reserve needed: 100% battery for cruise
- **Total savings: ~1.1 kg → more battery capacity or lighter aircraft**

### Inverted V-Tail Design
| Parameter | Value |
|-----------|-------|
| V-angle | 110-120° (inverted) |
| Span | 600-800mm |
| Chord | 150-180mm |
| Area | 15-20 dm² |
| Ruddervator deflection | ±25° |

### Propulsion System (Optimized for 3-4hr Endurance)
| Component | Model | Specs | Weight | Cost |
|-----------|-------|-------|--------|------|
| Motor | SunnySky X4112S-320kv | 800W max, efficient cruise | 190g | $55 |
| ESC | 60A BLHeli_32 | 6S, telemetry | 60g | $35 |
| Battery | 6S 22000mAh (2x 11Ah) | 22.2V, 488Wh total | 2400g | $240 |
| Propeller | 18x10 folding | Carbon fiber, high efficiency | 50g | $40 |

### Endurance Calculation
| Parameter | Value |
|-----------|-------|
| Battery capacity | 488 Wh (6S 22Ah) |
| Usable capacity (80%) | 390 Wh |
| Cruise power (9kg @ 20m/s) | 100-120W |
| **Cruise endurance** | **3.2-3.9 hours** |
| Reserve (20%) | ~45 min |

### Flight Controller
| Component | Model | Features | Cost |
|-----------|-------|----------|------|
| FC | Pixhawk 6C | STM32H7, triple IMU | $200 |
| GPS | Holybro M9N | Multi-constellation | $60 |
| Airspeed | MS4525DO | Digital I2C | $30 |
| Power Module | Holybro PM07 | High current | $35 |

### Structural Design
| Component | Material | Construction |
|-----------|----------|--------------|
| Wing spar | Carbon fiber tube (25mm OD) | Continuous through fuselage |
| Wing ribs | Laser-cut plywood + foam | Built-up construction |
| Wing skin | Fiberglass/balsa sandwich | Vacuum bagged |
| Booms | Carbon fiber tubes (30mm OD) | Off-the-shelf |
| Fuselage | Carbon/fiberglass composite | Molded or 3D printed core |
| V-tail | Foam core + fiberglass | Vacuum bagged |
| Motor mount | Aluminum CNC or 3D printed | Vibration isolated |

### Weight Budget
| Component | Mass (g) | % |
|-----------|----------|---|
| Wing structure | 1500 | 17% |
| Fuselage | 800 | 9% |
| Booms | 400 | 4% |
| V-tail | 300 | 3% |
| Motor + mount | 250 | 3% |
| ESC | 60 | 1% |
| **Battery (6S 22Ah)** | **2400** | **27%** |
| FC + avionics | 300 | 3% |
| Servos (4x) | 150 | 2% |
| Wiring/hardware | 400 | 4% |
| **Payload (camera+gimbal)** | **1000** | **11%** |
| **Margin** | 1440 | 16% |
| **Total** | ~9000g | 100% |

### Payload Options (V2/V3/V4 - 1 kg max)

#### ALTI Transition Factory Payloads

**ALTI sources payloads from third-party OEM manufacturers** (not built in-house):

| Payload | OEM Manufacturer | Location | Type |
|---------|------------------|----------|------|
| **Raptor** | [Height Technologies](https://heighttechnologies.com/) | Netherlands | Military/tactical UAV specialist |
| **E95** | [Edge Autonomy](https://edgeautonomy.io/) (Octopus ISR) | USA (now Redwire) | Defense-grade gimbals |
| **Photogrammetry** | Sony + EMLID | Japan / International | Commercial components |

##### Raptor (by Height Technologies)

| Spec | Value |
|------|-------|
| EO Camera | 1280×720 HD |
| EO Zoom | 40x optical + 2x digital (80x continuous) |
| Thermal | 1280×720, uncooled 8-14μm LWIR |
| IR Zoom | 8x digital |
| Stabilization | 3-axis mechanical + electronic |
| Features | Object tracking, Geo-Lock, Target GPS, Real-time stabilization |
| Optional | 200mW 850nm laser illuminator |
| Weight | ~500g (est.) |
| Est. Price | $4,000-8,000* |

##### E95 (by Edge Autonomy / Octopus ISR)

| Spec | Value |
|------|-------|
| EO Camera | 1920×1080 Full HD, global shutter |
| EO Zoom | 20x (1080p) / 45x (480p) + 4x digital |
| Thermal | 640×512 LWIR uncooled (dual sensors) |
| IR Zoom | 4x digital |
| Weight | **570g (1.25 lbs)** |
| Dimensions | 95mm × 134mm (3.8" × 5.3") |
| Rating | IP64 ruggedized |
| Features | Auto tracking, PiP, dual video, 32GB onboard, artillery support |
| Est. Price | $8,000-15,000* |

##### Photogrammetry Package

| Component | Manufacturer | Price |
|-----------|--------------|-------|
| Sony ILX-LR1 (61MP, 243g) | Sony | $2,950 |
| 24mm f/2.8 G lens | Sony | ~$600 |
| EMLID multi-band GNSS | EMLID | ~$1,500-2,000 |
| Integration/housing | ALTI | ~$500 |
| **Total** | | **$5,500-7,000** |

**Photogrammetry Features:**
- 61MP full-frame (1.57cm GSD @ 100m)
- Centimeter-level PPK positioning
- 100km PPK baseline
- Camera sync for precise timing

*Prices are estimates - defense/military gimbals require direct quotes*

**Sources:**
- [Height Technologies](https://heighttechnologies.com/products/raven/)
- [Edge Autonomy E95](https://www.unmannedsystemstechnology.com/company/edge-autonomy/octopus-isr-e95-multiple-application-payload-camera/)
- [Sony ILX-LR1 - B&H Photo](https://www.bhphotovideo.com/c/product/1785754-REG/sony_ilx_lr1_industrial_camera.html)

---

#### Equivalent/Alternative Payloads for MegaDrone

##### Electro-Optical (EO) Cameras
| Config | Components | Weight | Cost | Capability |
|--------|------------|--------|------|------------|
| **Action Cam** | GoPro Hero 12 + mount | 160g | $400 | 5.3K video, simple |
| **Compact EO** | Sony RX0 II + 2-axis gimbal | 400g | $900 | 4K video, 15MP stills |
| **Compact Zoom** | Sony RX100 VII + 2-axis gimbal | 550g | $1,500 | 24-200mm equiv, 20MP |
| **High Zoom** | Siyi ZT30 (30x optical) | 480g | $1,800 | 30x zoom, 4K, similar to Raptor |

##### SLR / Mirrorless (High Resolution)
| Config | Components | Weight | Cost | Capability |
|--------|------------|--------|------|------------|
| **APS-C Mirrorless** | Sony A6700 + 20mm pancake | 550g | $1,600 | 26MP, interchangeable lens |
| **Full Frame** | Sony A7C II + 28mm f/2.8 | 650g | $2,500 | 33MP full frame, low light |
| **High-Res Mapping** | Sony A7R V + 35mm | 850g | $4,000 | 61MP (matches ALTI ILX-R1) |
| **ALTI-Equivalent** | Sony ILX-R1 + 24mm G + EMLID | 950g | $5,500 | 61MP, RTK, survey-grade |

##### Thermal / EO+IR
| Config | Components | Weight | Cost | Capability |
|--------|------------|--------|------|------------|
| **Budget Thermal** | FLIR Lepton 3.5 + Raspberry Pi | 200g | $400 | 160×120 thermal, DIY |
| **Entry EO/IR** | Siyi ZT6 (EO + 640×512 thermal) | 360g | $2,200 | Similar to E95 thermal |
| **Mid EO/IR** | Siyi ZT30 (4K + 640×512 thermal) | 480g | $2,800 | 30x zoom + thermal |
| **Pro Thermal** | Workswell Wiris Pro | 450g | $8,000 | 640×512, radiometric |
| **ALTI E95 Equiv** | Custom 1080p + 640×512 gimbal | 600g | $5,000-8,000 | Matches E95 specs |

##### LiDAR
| Config | Components | Weight | Cost | Capability |
|--------|------------|--------|------|------------|
| **Entry LiDAR** | Livox Mid-360 | 265g | $1,000 | 360° FOV, 40m range |
| **Mapping LiDAR** | Livox Avia + EMLID Reach | 750g | $2,000 | 70° FOV, 450m range, RTK |
| **Pro LiDAR** | Ouster OS0-32 + IMU | 450g | $4,000 | 90° FOV, 50m range, 32ch |
| **Survey LiDAR** | Livox Avia + APX-15 IMU | 950g | $15,000 | Survey-grade accuracy |

##### Multi-Sensor / Mapping
| Config | Components | Weight | Cost | Capability |
|--------|------------|--------|------|------------|
| **Basic Mapping** | Sony RX100 + EMLID Reach M2 | 600g | $1,300 | 20MP + PPK positioning |
| **Pro Mapping** | Sony A6700 + EMLID Reach M+ | 800g | $2,800 | 26MP + RTK/PPK |
| **LiDAR + Photo** | Livox Mid-360 + Sony RX0 II | 550g | $1,500 | Point cloud + photos |
| **Full Survey** | Livox Avia + A6700 + EMLID | 1000g | $4,500 | LiDAR + photo + RTK |
| **ALTI Photo Equiv** | Sony A7R V + EMLID Reach RS3 | 950g | $5,000 | 61MP + PPK, matches ALTI |

#### Payload Cost Summary
| Category | Budget | Mid-Range | ALTI-Equivalent |
|----------|--------|-----------|-----------------|
| **EO Only** | $400-900 | $1,500-2,500 | $4,000-5,500 |
| **EO/IR (ISR)** | $2,200 | $2,800-5,000 | $5,000-8,000 |
| **Thermal Only** | $400 | $2,200 | $8,000 |
| **LiDAR** | $1,000 | $2,000-4,000 | $15,000+ |
| **Photogrammetry** | $1,300 | $2,800 | $5,000-5,500 |

### V2 Budget
| Category | Cost |
|----------|------|
| Pixhawk 6C + GPS + sensors | $325 |
| Motor + ESC | $90 |
| Battery (6S 22Ah, 2x packs) | $240 |
| Propeller | $40 |
| Carbon tubes (booms, spar) | $150 |
| Composite materials | $200 |
| Plywood/foam for ribs | $50 |
| Servos (4x digital) | $60 |
| Hardware/fasteners | $75 |
| Camera + gimbal (1kg payload) | $600 |
| **Total** | **~$1,830** |

---

## V3 - ALTI-Style VTOL QuadPlane

### Purpose
- Add VTOL capability to V2 airframe
- Develop transition tuning expertise
- Enable runway-independent operations
- Validate hybrid propulsion integration

### Configuration: QuadPlane (V2 + 4 VTOL Motors)
```
    Top View:

         [M1]                                           [M2]
           ○─────────────────────────────────────────────○
           │                                             │
    ┌──────┴─────────────────────────────────────────────┴──────┐
    │                          WING                             │
    │                        (3.0m span)                        │
    └───────────┬───────────────────────────────────┬───────────┘
                │                                   │
         ┌──────┴──────┐                     ┌──────┴──────┐
         │    BOOM     │                     │    BOOM     │
         │             │   ┌─────────────┐   │             │
         │             │   │             │   │             │
         │             │   │   FUSELAGE  │   │             │
         │             │   │             │   │             │
         │             │   │     [P]     │   │             │  ← Pusher
         │             │   └─────────────┘   │             │
         │             │                     │             │
         └──────┬──────┘                     └──────┬──────┘
                │                                   │
           ○────┴─────────────╲       ╱─────────────┴────○
         [M3]                  ╲     ╱                  [M4]
                                ╲   ╱
                            Inverted V-Tail


    Front View (Hover Mode):

         [M1]▼                                       ▼[M2]
           │                                           │
    ═══════╪═══════════════════════════════════════════╪═══════
           │              │       │                    │
           │         ┌────┴───────┴────┐               │
           │         │    Fuselage     │               │
           │         │       [P]       │               │
           │         └─────────────────┘               │
           │                                           │
         [M3]▼             ╲     ╱                   ▼[M4]
                            ╲   ╱
                             ╲ ╱


    Motor Positions:
    - M1, M2: Front (on wing, outboard)
    - M3, M4: Rear (on boom ends, near V-tail)
    - P: Center pusher (rear of fuselage)
```

### Specifications (Scaled for Starlink + ISR Payload)
| Parameter | Value | Notes |
|-----------|-------|-------|
| Wingspan | **3.2m** | Same as V2 (scaled) |
| Length | **2.4m** | Same as V2 (scaled) |
| AUW | **15 kg** | +VTOL system weight |
| **Payload** | **2.5 kg** | ISR (1 kg) + Starlink (1.5 kg) |
| VTOL Thrust | 4x 4.5kg | 18 kg total, 1.2:1 TWR |
| Transition Speed | 15-17 m/s | Wing takes over lift |
| Hover Time | 5-8 min | Takeoff/landing reserve |
| Cruise Time | **~3 hrs** | Forward flight |
| Cruise Speed | 70-75 km/h | Efficient cruise |
| Wing Loading | **145-165 g/dm²** | Higher than V2 |

### VTOL Motor Configuration
| Position | Motor | Prop | Thrust | Weight |
|----------|-------|------|--------|--------|
| M1 (Front-Left) | **T-Motor U7 V2** | 20x6 | **4.5 kg** | 195g |
| M2 (Front-Right) | **T-Motor U7 V2** | 20x6 | **4.5 kg** | 195g |
| M3 (Rear-Left) | **T-Motor U7 V2** | 20x6 | **4.5 kg** | 195g |
| M4 (Rear-Right) | **T-Motor U7 V2** | 20x6 | **4.5 kg** | 195g |
| P (Pusher) | SunnySky X4112S | 16x10 | 4.0 kg | 190g |

**Total VTOL thrust:** 18 kg (for 15 kg AUW = **1.2:1 TWR**)

### Power System
| Component | Specs | Weight | Count |
|-----------|-------|--------|-------|
| VTOL ESC | **50A BLHeli_32** | 50g | 4 |
| Main Battery | **6S 22000mAh** | **2400g** | 1 |
| Battery Capacity | **488 Wh** | Same as V2 | - |
| Pusher shares main battery | - | - | - |

### VTOL Arm Design
| Parameter | Value |
|-----------|-------|
| Front arm span | 800mm from centerline |
| Rear arms | Integrated into boom ends |
| Arm material | Carbon fiber tube (20mm) |
| Motor tilt | 0° (vertical) or 5° forward |

### ArduPilot QuadPlane Configuration
```
Frame Class:     Q_FRAME_CLASS = 1 (Quad)
Frame Type:      Q_FRAME_TYPE = 1 (X configuration)
Transition:      Q_TRANSITION_MS = 5000 (5 sec)
Assist Speed:    Q_ASSIST_SPEED = 14 (m/s)
Tilt Mask:       Q_TILT_MASK = 0 (no tilt)
```

### Weight Budget
| Component | Mass (g) | % |
|-----------|----------|---|
| V2 Airframe | 3000 | 20% |
| **VTOL Motors (4x U7 V2)** | **780** | 5% |
| **VTOL ESCs (4x 50A)** | **200** | 1% |
| VTOL Arms/Mounts | 350 | 2% |
| Pusher Motor + ESC | 250 | 2% |
| **Battery (6S 22Ah)** | **2400** | 16% |
| FC + Avionics | 350 | 2% |
| Camera + Gimbal | 1000 | 7% |
| Wiring/Hardware | 500 | 3% |
| **Subtotal** | **8830g** | 59% |
| **Margin/Starlink** | 6170g | 41% |
| **AUW (ISR only)** | **~12000g** | |
| **AUW (with Starlink)** | **~15000g** | 100% |

### V3 Additional Budget (over V2)
| Category | Cost |
|----------|------|
| **VTOL Motors (4x T-Motor U7 V2)** | **$480** |
| **VTOL ESCs (4x 50A)** | **$160** |
| VTOL Props (4x 20") | $100 |
| Motor mounts + arms | $120 |
| Wiring/connectors | $60 |
| **Total Additional** | **~$920** |

---

## V4 - Gas-Electric Hybrid VTOL

### Purpose
- Extended range and endurance (2+ hours)
- Operational ISR prototype
- Validate gas engine integration
- Test long-duration missions

### Configuration
Same as V3 but with gasoline pusher replacing electric pusher.

```
    Power Architecture:

    ┌─────────────────┐          ┌─────────────────┐
    │   GAS ENGINE    │          │   LiPo BATTERY  │
    │  (Cruise Only)  │          │  (VTOL + Avionics)│
    │    DLE 35cc     │          │   6S 10000mAh   │
    └────────┬────────┘          └────────┬────────┘
             │                            │
             ▼                            ▼
    ┌─────────────────┐          ┌─────────────────┐
    │  PUSHER PROP    │          │  4x VTOL MOTORS │
    │    18x10        │          │ (T-Motor U8 Pro)│
    └─────────────────┘          └─────────────────┘

    Flight Modes:
    - VTOL: Electric quad motors only
    - Transition: Quad + gas pusher
    - Cruise: Gas pusher only (quad stopped/folded)
```

### Specifications (Scaled for Starlink + ISR Payload)
| Parameter | Value | Notes |
|-----------|-------|-------|
| Wingspan | **3.2m** | Scaled up from ALTI |
| Length | **2.4m** | Scaled up from ALTI |
| **MTOW** | **20 kg** | Scaled for 2.5 kg payload |
| **Payload** | **2.5 kg** | ISR (1 kg) + Starlink (1.5 kg) |
| Cruise Speed | 75 km/h (21 m/s) | ALTI spec maintained |
| Stall Speed | 14-16 m/s | Higher wing loading |
| Fuel Capacity | 3.5-4.5 L | For 8-12hr endurance |
| **Cruise Endurance** | **8-12 hours** | Gas powered |
| VTOL Endurance | 8-10 min | Electric reserve |
| **Flight Range** | **900 km** | Full fuel load |
| **Link Range** | **Unlimited** | Via Starlink |
| Operating Cost | ~$4/hr | Fuel + Starlink |

### Gas Engine Options
| Engine | Displacement | Power | Weight | Fuel Consumption | Cost |
|--------|--------------|-------|--------|------------------|------|
| DLE 35 | 35cc | 3.5 HP | 870g | 450 mL/hr | $250 |
| DLE 40 | 40cc | 4.0 HP | 1050g | 500 mL/hr | $280 |
| NGH GT35 | 35cc | 3.2 HP | 820g | 420 mL/hr | $180 |
| Zenoah G38 | 38cc | 3.8 HP | 1100g | 480 mL/hr | $350 |

**Recommended:** DLE 35 (proven reliability, good power-to-weight)

### Gas Engine Integration
| Component | Specs | Weight | Cost |
|-----------|-------|--------|------|
| Engine | DLE 35cc twin | 3.5 HP @ 7500 RPM | 870g | $250 |
| Muffler | Pitts style | Low backpressure | 80g | $30 |
| Fuel tank | 2L aluminum | Clunk pickup | 150g | $40 |
| Fuel lines | Tygon + filter | UV resistant | 50g | $15 |
| Ignition | CDI electronic | Separate battery | 100g | incl. |
| Kill switch | Optocoupler | FC controlled | 10g | $10 |
| Throttle servo | 25kg metal gear | High torque | 60g | $25 |
| Vibration mount | Rubber standoffs | Engine isolation | 50g | $20 |

### Flight Controller Upgrade
| Component | Model | Reason | Cost |
|-----------|-------|--------|------|
| FC | Pixhawk 6X | Redundant IMU, more I/O | $400 |
| GPS | Holybro H-RTK F9P | RTK capable, cm accuracy | $300 |
| Airspeed | Dual MS4525DO | Redundancy | $60 |
| RPM Sensor | Hall effect | Engine monitoring | $15 |
| CHT Sensor | K-type thermocouple | Engine temp | $20 |

### Weight Budget (20 kg MTOW - Starlink Capable)
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
| **ISR Payload (camera + gimbal)** | **1000** | **5%** |
| **Starlink Mini + mount** | **1500** | **8%** |
| Wiring/Hardware | 700 | 4% |
| **Margin** | 4200 | 21% |
| **MTOW** | **20000g** | 100% |

**Payload Configurations:**
- ISR only (1 kg): Full fuel → 12 hr, 900 km
- Starlink only (1.5 kg): Full fuel → 11 hr, 825 km
- **ISR + Starlink (2.5 kg):** Full fuel → **10 hr, 750 km, unlimited link range**

### V4 Budget
| Category | Cost |
|----------|------|
| Pixhawk 6X + RTK GPS | $700 |
| Gas engine (DLE 35) | $250 |
| Fuel system | $100 |
| Engine sensors | $50 |
| Airframe modifications | $150 |
| VTOL battery (6S 10Ah) | $120 |
| EO/IR camera upgrade | $600 |
| Misc hardware | $100 |
| **Total Additional** | **~$2,070** |

---

## Development Summary

### Version Comparison Chart

| Version | Config | Wingspan | Length | AUW | Payload | Speed | Endurance | FC | New Cost |
|---------|--------|----------|--------|-----|---------|-------|-----------|-----|----------|
| **V0** | Pusher FW | 1.0-1.2m | 0.6m | 0.9 kg | 200g | 54 km/h | 20-25 min | Pixhack | $200 |
| **V1** | Pusher FW | 1.0-1.2m | 0.6m | **1.1 kg** | 300g | 54 km/h | **45-50 min** | Pixhack | $385 |
| **V1-ACAP** | Pusher FW | 1.0-1.2m | 0.6m | 0.86 kg | 200g | 54 km/h | 20-25 min | **dRehmFlight + SBC** | **$130** |
| **V1-LE** | Pusher FW | 1.8-2.0m | 0.9m | 1.5 kg | 300g | 45-50 km/h | **2-2.5 hrs** | Pixhack | $110 |
| **V1-Fast** | Pusher FW | 1.5-1.7m | 0.85m | 1.5 kg | 300g | **55-65 km/h** | 1-1.3 hrs | Pixhack | $100 |
| **V1-Fast 2hr** | Pusher FW | 2.2-2.4m | 1.1m | 2.1 kg | 500g | **55-60 km/h** | **2+ hrs** | Pixhack | $210 |
| **V1-VID** | Pusher FW | 1.0-1.2m | 0.6m | **1.15 kg** | 300g | 54 km/h | **40-45 min** | Pixhack | $150 |
| **V2** | ALTI FW | **3.2m** | 2.4m | **12 kg** | **2.5 kg** | 70-80 km/h | **3-4 hrs** | Pixhawk 6C | $2,200 |
| **V3** | ALTI VTOL | **3.2m** | 2.4m | **15 kg** | **2.5 kg** | 70-75 km/h | **~3 hrs** | Pixhawk 6C | $1,020 |
| **V4** | ALTI VTOL | **3.2m** | 2.4m | **20 kg** | **2.5 kg** | 75 km/h | **8-12 hrs** | Pixhawk 6X | $2,300 |

### Cumulative Investment

**Primary Development Path (V0 → V1 → V2 → V3 → V4):**

| Milestone | Cumulative Cost | Capability |
|-----------|-----------------|------------|
| V0 Complete | $200 | Basic flying, autopilot tuning |
| V1 Complete | $550 | Durable airframe, camera testing |
| V2 Complete | $2,750 | 3-4 hr endurance, 2.5 kg payload (Starlink capable) |
| V3 Complete | $3,770 | VTOL, ~3 hr, 2.5 kg payload |
| V4 Complete | $6,000 | 8-12 hr gas-hybrid, Starlink + ISR, unlimited range |

**V1 Variant Costs (standalone or built after V1 base):**

| Variant | Standalone Cost | Key Advantage | Autopilot? |
|---------|-----------------|---------------|------------|
| **V1-ACAP** | **$130** | Minimum cost, full code access | ✅ Custom (dRehmFlight + SBC) |
| V1-LE | $660 | Max endurance (2+ hrs @ 45-50 km/h) | ✅ Full (ArduPilot/iNav) |
| V1-Fast | $650 | Speed (55-65 km/h, 1+ hr) | ✅ Full (ArduPilot/iNav) |
| V1-Fast 2hr | $760 | Speed + endurance (55-60 km/h, 2+ hrs) | ✅ Full (ArduPilot/iNav) |
| **V1-VID** | **$665** | **WifiLink/OpenIPC comm system** | ✅ Full (ArduPilot/iNav) |

### Recommended Timeline

```
Month 1-2:   V0 - Build, crash, learn, repeat
Month 3-4:   V1 - Refined build, camera integration
Month 5-8:   V2 - Full-scale ALTI airframe, flight testing
Month 9-12:  V3 - VTOL conversion, transition tuning
Month 13-16: V4 - Gas integration, endurance testing
```

---

## Hardware Progression Matrix

| Component | V0 | V1 | V1-ACAP | V1-VID | V2 | V3 | V4 |
|-----------|-----|-----|---------|--------|-----|-----|-----|
| **Flight Controller** | Pixhack | Pixhack | **Teensy 4.0 + SBC** | Pixhack | Pixhawk 6C | Pixhawk 6C | Pixhawk 6X |
| **GPS** | Existing | Existing | **BN-880** | Existing | Holybro M9N | Holybro M9N | H-RTK F9P |
| **Pusher Motor** | 2212 920kv | 2212 920kv | 2212 920kv | 2212 920kv | X4112S 320kv | X4112S 320kv | DLE 35 gas |
| **VTOL Motors** | - | - | - | - | - | **4x T-Motor U7 V2** | **4x T-Motor U8 Pro** |
| **Main Battery** | 3S 2200mAh | **3S 5000mAh** | 3S 2200mAh | **3S 5000mAh** | 6S 22000mAh | 6S 22000mAh | 6S 10000mAh |
| **Receiver** | ELRS | ELRS | FS-IA6B | ELRS | ELRS | ELRS | ELRS |
| **Comm System** | ELRS | ELRS | ELRS | **WifiLink** | **WifiLink** | **WifiLink** | **Starlink** |
| **Airspeed** | - | - | - | - | MS4525DO | MS4525DO | Dual MS4525DO |
| **Wingspan** | 1.0-1.2m | 1.0-1.2m | 1.0-1.2m | 1.0-1.2m | **3.2m** | **3.2m** | **3.2m** |
| **Length** | 0.6m | 0.6m | 0.6m | 0.6m | **2.4m** | **2.4m** | **2.4m** |
| **Payload** | 200g | 300g | 200g | 300g | **2.5 kg** | **2.5 kg** | **2.5 kg** |
| **Starlink** | - | - | - | - | Optional | Optional | **Integrated** |
| **Datalink** | LOS | LOS | LOS | **WifiLink** | **WifiLink** | **WifiLink** | **Starlink (unlimited)** |
| **Endurance** | 20-25 min | **45-50 min** | 20-25 min | **40-45 min** | **3-4 hrs** | 2-2.5 hrs | **8-12 hrs** |
| **Autopilot** | ✅ Full | ✅ Full | ✅ Custom | ✅ Full | ✅ Full | ✅ Full | ✅ Full |

---

## SWAP Analysis (Size, Weight, And Power)

Comprehensive mass and power budgets for all versions including communication systems.

### Complete Weight Budgets

#### V0/V1 Weight Budget
| Component | V0 Mass (g) | V1 Mass (g) | Notes |
|-----------|-------------|-------------|-------|
| Airframe (foam) | 300 | 320 | V1 slightly heavier (Depron) |
| Battery | 180 | **380** | V0: 3S 2200mAh (24Wh), **V1: 3S 5000mAh (55Wh)** |
| Motor (2212 920kv) | 55 | 55 | |
| Propeller (9x6) | 15 | 15 | |
| ESC (30A) | 30 | 30 | |
| FC (Pixhack) | 40 | 40 | |
| GPS | 25 | 25 | |
| Receiver (ELRS) | 5 | 5 | |
| Servos (4x 9g) | 36 | 36 | |
| **Remote ID (ESP32)** | - | **8** | DIY ArduRemoteID |
| Camera (if any) | - | 60 | RunCam 5 or similar |
| Wiring/Hardware | 50 | 65 | |
| **Subtotal** | **736g** | **1039g** | |
| **Margin** | 164g | 61g | |
| **AUW** | **~900g** | **~1100g** | |

#### V1-VID Weight Budget (with WifiLink)
| Component | Mass (g) | Notes |
|-----------|----------|-------|
| Airframe (foam/Depron) | 320 | |
| **Battery (3S 5000mAh)** | **380** | **55 Wh** |
| Motor (2212 920kv) | 55 | |
| Propeller (9x6) | 15 | |
| ESC (30A) | 30 | |
| FC (Pixhack) | 40 | |
| GPS | 25 | |
| Receiver (ELRS) | 5 | Backup RC link |
| Servos (4x 9g) | 36 | |
| **Remote ID (ESP32)** | **8** | DIY ArduRemoteID |
| **WifiLink 2 VTX** | **35** | **1080p @ 90fps (incl. camera)** |
| Wiring/Hardware | 60 | Includes WifiLink cables |
| **Subtotal** | **1009g** | |
| **Margin** | 141g | |
| **AUW** | **~1150g** | |

#### V2 Weight Budget (3.2m Fixed-Wing with WifiLink)
| Component | Mass (g) | Power (W) | Notes |
|-----------|----------|-----------|-------|
| **Structure** | | | |
| Airframe (composite) | 3000 | - | Wing, booms, fuse, tail |
| **Propulsion** | | | |
| Battery (6S 22Ah) | 2400 | - | 488 Wh |
| Motor (X4112S 320kv) | 190 | 110 | Cruise power |
| Propeller (18x10) | 50 | - | Folding CF |
| ESC (60A) | 60 | 2 | BLHeli_32 |
| **Avionics** | | | |
| FC (Pixhawk 6C) | 45 | 1.5 | |
| GPS (M9N) | 25 | 0.3 | |
| Power Module | 35 | - | PM07 |
| Airspeed Sensor | 10 | 0.1 | MS4525DO |
| Receiver (ELRS) | 5 | 0.3 | |
| **Remote ID** | **8** | **0.5** | Commercial module |
| Servos (4x digital) | 150 | 3.0 | 25kg metal gear |
| **Communications** | | | |
| **WifiLink 2 VTX** | **35** | **5.0** | 1080p @ 90fps |
| **Payload** | | | |
| Camera (EO) | 400 | 5.0 | Sony or similar |
| Gimbal (3-axis) | 350 | 4.0 | Brushless |
| Gimbal Controller | 50 | incl. | |
| **Safety & Lighting** | | | |
| Nav Lights (strobes) | 30 | 2.0 | Wingtip + tail |
| Cooling Fan | 15 | 1.0 | ESC/FC cooling |
| **Infrastructure** | | | |
| Wiring/Connectors | 300 | - | |
| Mounting Hardware | 100 | - | |
| **Subtotal** | **7258g** | **~135W** | |
| **Margin** | 742g | - | 10% margin |
| **AUW (Base)** | **~8000g** | | |
| **AUW (1kg ISR payload)** | **~9000g** | | +1kg camera upgrade |
| **AUW (with Starlink)** | **~10500g** | | +1500g Starlink |

#### V3 Weight Budget (VTOL QuadPlane with WifiLink - 3hr Config)
| Component | Mass (g) | Power (W) | Notes |
|-----------|----------|-----------|-------|
| **Structure** | | | |
| Airframe (composite) | 3000 | - | Same as V2 |
| **VTOL System** | | | |
| **VTOL Motors (4x U7 V2)** | **780** | **480 hover** | 4.5kg thrust each |
| **VTOL ESCs (4x 50A)** | **200** | **10** | BLHeli_32 |
| **VTOL Props (4x 20")** | **120** | - | CF folding |
| **VTOL Arms/Mounts** | **350** | - | Carbon fiber |
| **Propulsion (Cruise)** | | | |
| **Battery (6S 22Ah)** | **2400** | - | **488 Wh** (same as V2) |
| Pusher Motor (X4112S) | 190 | 110 | Cruise power |
| Pusher ESC (60A) | 60 | 2 | BLHeli_32 |
| Pusher Prop (16x10) | 40 | - | Folding CF |
| **Avionics** | | | |
| FC (Pixhawk 6C) | 45 | 1.5 | |
| GPS (M9N) | 25 | 0.3 | |
| Power Module | 35 | - | PM07 |
| Airspeed Sensor | 10 | 0.1 | MS4525DO |
| Receiver (ELRS) | 5 | 0.3 | |
| **Remote ID** | **8** | **0.5** | Commercial module |
| Servos (4x digital) | 150 | 3.0 | 25kg metal gear |
| **Communications** | | | |
| **WifiLink 2 VTX** | **35** | **5.0** | 1080p @ 90fps |
| **Payload** | | | |
| Camera (EO) | 600 | 5.0 | Sony or similar |
| Gimbal (3-axis) | 350 | 4.0 | Brushless |
| Gimbal Controller | 50 | incl. | |
| **Safety & Lighting** | | | |
| Nav Lights (strobes) | 30 | 2.0 | Wingtip + tail |
| Cooling Fan | 15 | 1.0 | ESC/FC cooling |
| **Infrastructure** | | | |
| Wiring/Connectors | 400 | - | More complex wiring |
| Mounting Hardware | 100 | - | |
| **Subtotal** | **8998g** | **~615W hover / ~135W cruise** | |
| **Margin/Starlink Option** | 6002g | - | 40% margin |
| **AUW (ISR only)** | **~12000g** | | |
| **AUW (with Starlink)** | **~15000g** | | +1500g Starlink + margin |

#### V4 Weight Budget (Hybrid VTOL with Starlink)
| Component | Mass (g) | Power (W) | Notes |
|-----------|----------|-----------|-------|
| **Structure** | | | |
| Airframe (composite) | 5000 | - | Strengthened for 20kg MTOW |
| **Gas Engine System** | | | |
| **Gas Engine (DLE 35)** | **870** | - | 3.5 HP, 450 mL/hr |
| Engine Mount + Vibration | 200 | - | Rubber standoffs |
| **Fuel (4L)** | **3000** | - | ~10 hr endurance |
| Fuel Tank + Lines | 350 | - | Aluminum tank |
| Ignition System | 100 | 5 | CDI + battery |
| Throttle Servo | 60 | 1 | 25kg metal gear |
| CHT/RPM Sensors | 20 | 0.2 | Engine monitoring |
| **VTOL System** | | | |
| **VTOL Motors (4x U8 Pro)** | **1160** | **600 hover** | 6.5kg thrust each, 1.3:1 TWR |
| **VTOL ESCs (4x 50A)** | **250** | **10** | BLHeli_32 |
| **VTOL Props (4x 28")** | **160** | - | CF folding |
| VTOL Arms/Mounts | 350 | - | Carbon fiber |
| VTOL Battery (6S 10Ah) | 1100 | - | 222 Wh (VTOL only) |
| **Avionics** | | | |
| FC (Pixhawk 6X) | 60 | 2.0 | Redundant IMU |
| GPS (H-RTK F9P) | 40 | 0.5 | RTK capable |
| Power Module | 40 | - | PM02D |
| Airspeed Sensors (dual) | 20 | 0.2 | MS4525DO x2 |
| Receiver (ELRS) | 5 | 0.3 | |
| **Remote ID** | **8** | **0.5** | Commercial module |
| Servos (4x digital) | 150 | 3.0 | 25kg metal gear |
| **Communications** | | | |
| **WifiLink 2 VTX** | **35** | **5.0** | Backup/local video |
| **Starlink Mini** | **1500** | **25-40** | Primary comms |
| Starlink Mount | 100 | - | Vibration isolated |
| **Payload** | | | |
| Camera (EO/IR) | 600 | 8.0 | Dual sensor |
| Gimbal (3-axis) | 350 | 4.0 | Brushless |
| Gimbal Controller | 50 | incl. | |
| **Safety & Lighting** | | | |
| Nav Lights (strobes) | 40 | 3.0 | High visibility |
| Cooling Fans (2x) | 30 | 2.0 | Engine + avionics |
| **Infrastructure** | | | |
| Wiring/Connectors | 500 | - | Complex hybrid system |
| Mounting Hardware | 200 | - | |
| **Subtotal** | **16498g** | **~720W hover / ~60W cruise** | |
| **Margin** | 3502g | - | 18% margin |
| **MTOW** | **20000g** | | |

### Complete Electrical Power Breakdown

#### V0 Power Budget (Skills Platform)
| Component | Power (W) | Notes |
|-----------|-----------|-------|
| **Propulsion** | 40 | Motor at cruise (2212 920kv) |
| Flight Controller | 1.5 | Pixhack |
| GPS | 0.3 | |
| Receiver (ELRS) | 0.3 | |
| Servos (4x cruise) | 2.0 | Light load at cruise |
| **Total Cruise** | **~44W** | |

#### V1 Power Budget (3S 5000mAh)
| Component | Power (W) | Notes |
|-----------|-----------|-------|
| **Propulsion** | 50 | Motor at cruise (heavier aircraft) |
| Flight Controller | 1.5 | Pixhack |
| GPS | 0.3 | |
| Receiver (ELRS) | 0.3 | |
| Servos (4x cruise) | 2.0 | |
| Remote ID (ESP32) | 0.5 | DIY ArduRemoteID |
| Camera (RunCam) | 2.0 | If equipped |
| **Total Cruise** | **~57W** | |

#### V1-VID Power Budget (with WifiLink)
| Component | Power (W) | Notes |
|-----------|-----------|-------|
| **Propulsion** | 50 | Motor at cruise |
| Flight Controller | 1.5 | Pixhack |
| GPS | 0.3 | |
| Receiver (ELRS) | 0.3 | Backup RC link |
| Servos (4x cruise) | 2.0 | |
| Remote ID (ESP32) | 0.5 | DIY ArduRemoteID |
| **WifiLink 2 VTX** | **5.0** | 1080p @ 90fps (includes camera) |
| **Total Cruise** | **~60W** | |

#### V2 Power Budget (3.2m Fixed-Wing)
| Component | Power (W) | Notes |
|-----------|-----------|-------|
| **Propulsion** | 110 | X4112S at cruise |
| Flight Controller | 1.5 | Pixhawk 6C |
| GPS (M9N) | 0.3 | |
| Receiver (ELRS) | 0.3 | |
| Servos (4x digital) | 3.0 | Higher torque |
| Airspeed Sensor | 0.1 | MS4525DO |
| Remote ID | 0.5 | Commercial module |
| **WifiLink 2 VTX** | **5.0** | |
| **Camera** | **5.0** | EO camera |
| **Gimbal** | **4.0** | 3-axis brushless |
| Navigation Lights | 2.0 | Wingtip strobes |
| Cooling Fan | 1.0 | ESC/FC cooling |
| **Total Cruise** | **~133W** | |

#### V3 Power Budget (VTOL QuadPlane) - Proposed 3hr Config
| Component | Cruise (W) | Hover (W) | Notes |
|-----------|------------|-----------|-------|
| **Propulsion (Pusher)** | 110 | 0 | X4112S |
| **VTOL Motors (4x U7)** | 0 | **480** | 4× 120W hover |
| Flight Controller | 2.0 | 2.0 | Pixhawk 6C |
| GPS (M9N) | 0.3 | 0.3 | |
| Receiver (ELRS) | 0.3 | 0.3 | |
| Servos (4x digital) | 3.0 | 1.0 | Less load in hover |
| Airspeed Sensor | 0.1 | 0.1 | |
| Remote ID | 0.5 | 0.5 | Commercial module |
| **WifiLink 2 VTX** | **5.0** | **5.0** | |
| **Camera** | **5.0** | **5.0** | EO or EO/IR |
| **Gimbal** | **4.0** | **4.0** | 3-axis brushless |
| Navigation Lights | 3.0 | 3.0 | Wingtip + tail strobes |
| Cooling Fans | 2.0 | 3.0 | Higher in hover |
| **Total** | **~135W** | **~504W** | |

#### V4 Power Budget (Gas-Electric Hybrid)
| Component | Cruise (W) | Hover (W) | Notes |
|-----------|------------|-----------|-------|
| **Gas Engine** | 0 (fuel) | - | DLE 35cc, 450mL/hr |
| Ignition (CDI) | 5.0 | - | Spark system |
| **VTOL Motors (4x U8)** | 0 | **600** | 4× 150W hover @ 20kg |
| Flight Controller | 2.0 | 2.0 | Pixhawk 6X |
| GPS (RTK F9P) | 0.5 | 0.5 | |
| Receiver (ELRS) | 0.3 | 0.3 | |
| Servos (4x digital) | 3.0 | 1.0 | |
| Airspeed Sensors (dual) | 0.2 | 0.2 | Redundant |
| Remote ID | 0.5 | 0.5 | Commercial module |
| **WifiLink 2 VTX** | **5.0** | **5.0** | Backup/local video |
| **Starlink Mini** | **35.0** | **35.0** | Primary BVLOS comms |
| **Camera (ISR)** | **6.0** | **6.0** | EO/IR gimbal |
| **Gimbal** | **5.0** | **5.0** | 3-axis heavy duty |
| Navigation Lights | 4.0 | 4.0 | Full lighting package |
| Cooling Fans | 2.0 | 3.0 | |
| Avionics Heater | 2.0 | 2.0 | Cold weather ops |
| **Total Electrical** | **~71W** | **~665W** | |

### Power Summary Table

| Version | Cruise Power | Hover Power | Notes |
|---------|--------------|-------------|-------|
| **V0** | 44W | - | Basic trainer |
| **V1** | 57W | - | With camera + Remote ID |
| **V1-VID** | 60W | - | With WifiLink |
| **V2** | 133W | - | Full ISR package |
| **V3** | 135W | 504W | VTOL QuadPlane |
| **V4** | 71W | 665W | Gas cruise, electric avionics |

### Starlink Power Requirements (V4)

| Mode | Power Draw | Notes |
|------|------------|-------|
| Idle/Search | 25W | Acquiring satellites |
| Active Streaming | 30-40W | Video + telemetry |
| Peak | 50W | Initial connection |
| **Average Mission** | **35W** | Typical BVLOS ops |

**Power Source for Starlink:**
- During cruise: Generator/alternator from gas engine (planned V4.1)
- During VTOL: VTOL battery (limits hover time to ~5 min with Starlink active)
- Recommendation: Separate Starlink battery (3S 5000mAh, ~140g) for VTOL reserve

### Endurance Impact Summary (Revised)

| Version | Battery/Fuel | Usable | Total Power | Endurance |
|---------|--------------|--------|-------------|-----------|
| **V0** | 24 Wh | 19 Wh (80%) | 44W | **26 min** |
| **V1** | 55 Wh | 44 Wh (80%) | 57W | **46 min** |
| **V1-VID** | 55 Wh | 44 Wh (80%) | 60W | **44 min** |
| **V2** | 488 Wh | 390 Wh (80%) | 133W | **2.9 hrs** |
| **V2+Starlink** | 488 Wh | 390 Wh (80%) | 168W | **2.3 hrs** |
| **V3** | 488 Wh | 390 Wh (80%) | 135W | **2.9 hrs** |
| **V3+Starlink** | 488 Wh | 390 Wh (80%) | 170W | **2.3 hrs** |
| **V4** | 4L fuel | 3.6L (90%) | Gas + 71W elec | **8-10 hrs** |

*V3 now uses 6S 22Ah battery (same as V2) with upgraded U7 VTOL motors*

---

## Configuration Evolution

```
V0/V1: Conventional Pusher (Small)
┌─────────────────────────┐
│    Simple trainer       │
│    1 pusher motor       │
│    Conventional tail    │
│    Foam construction    │
└─────────────────────────┘
            │
            ▼
V2: ALTI-Style Fixed-Wing (Full Scale)
┌─────────────────────────┐
│    3m wingspan          │
│    Twin-boom            │
│    Inverted V-tail      │
│    1 electric pusher    │
│    Composite build      │
└─────────────────────────┘
            │
            ▼
V3: ALTI-Style VTOL
┌─────────────────────────┐
│    V2 airframe          │
│    + 4 VTOL motors      │
│    QuadPlane config     │
│    All-electric         │
└─────────────────────────┘
            │
            ▼
V4: ALTI-Style Hybrid VTOL
┌─────────────────────────┐
│    V3 airframe          │
│    Gas pusher engine    │
│    Electric VTOL        │
│    2-3 hour endurance   │
└─────────────────────────┘
```

---

## Risk Mitigation

| Version | Primary Risks | Mitigation |
|---------|---------------|------------|
| V0 | Crashes, build errors | Cheap materials, expect failures |
| V1 | Overweight, CG issues | Careful weight tracking |
| **V1-ACAP** | **Custom code bugs, untested failsafes** | **Extensive SITL testing, conservative flying, incremental feature additions** |
| **V1-VID** | **Link loss, interference, latency** | **Ground testing first, RSSI monitoring, failsafe RTH on link loss** |
| V2 | Structural integrity at scale | FEA analysis, conservative SF |
| V3 | Transition failures, VTOL tuning | Extensive SITL, large TWR margin |
| V4 | Gas vibration, fuel system leaks | Vibration isolation, redundant ignition |

---

## Skills Development Path

| Version | Skills Developed |
|---------|-----------------|
| V0 | Foam construction, soldering, ArduPilot basics, RC flying |
| V1 | Composite basics, camera integration, PID tuning |
| **V1-ACAP** | **Flight control code, PID fundamentals, manual tuning, Arduino/C++** |
| **V1-VID** | **WifiLink/OpenIPC configuration, antenna tuning, digital FPV, long-range comms** |
| V2 | Large-scale composites, CAD, structural design |
| V3 | VTOL dynamics, transition tuning, hybrid power management |
| V4 | Gas engine operation, long-endurance ops, fuel systems |

---

*Document Version: 2.1*
*Created: 2025-01-21*
*Updated: 2026-01-23 - Added V1-VID (RunCam WifiLink/OpenIPC communication system)*
*Reference: ALTI Transition VTOL UAS*
*Project: MegaDrone Development Roadmap*
