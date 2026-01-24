# V0 Build Guide

**Aircraft:** Skills Development Platform
**Type:** Foam board conventional pusher
**Skill Level:** Beginner-Intermediate

---

## Table of Contents

1. [Overview](#overview)
2. [Tools Required](#tools-required)
3. [Build Sequence](#build-sequence)
4. [Wing Construction](#wing-construction)
5. [Fuselage Construction](#fuselage-construction)
6. [Tail Assembly](#tail-assembly)
7. [Electronics Installation](#electronics-installation)
8. [Control Surface Setup](#control-surface-setup)
9. [CG and Balance](#cg-and-balance)
10. [Pre-Flight Checklist](#pre-flight-checklist)

---

## Overview

### Dimensions

| Parameter | Value |
|-----------|-------|
| Wingspan | 1.0m (40") |
| Wing Chord | 180mm (7") |
| Wing Area | 18 dm² |
| Fuselage Length | 600mm (24") |
| Target AUW | 850-950g |
| Wing Loading | 50 g/dm² |

### Airfoil

- **Type:** Flat-bottom or KFm2 (foam board step)
- **Thickness:** ~12% chord

---

## Tools Required

### Essential

- [ ] Hot glue gun (high temp)
- [ ] Hobby knife (fresh blades)
- [ ] Metal ruler (24"+)
- [ ] Cutting mat or cardboard
- [ ] Soldering iron
- [ ] Wire strippers
- [ ] Hex drivers (1.5mm, 2mm)

### Recommended

- [ ] Heat gun (for covering)
- [ ] Foam-safe CA glue
- [ ] Masking tape
- [ ] Sharpie marker
- [ ] Square/triangle

---

## Build Sequence

```
Day 1: Cut wing panels, fuselage sides
Day 2: Assemble wing, add spar
Day 3: Build fuselage box
Day 4: Cut and attach tail surfaces
Day 5: Install motor, ESC, wiring
Day 6: Mount FC, GPS, receiver
Day 7: Install servos, control horns
Day 8: Balance, program, ground test
```

---

## Wing Construction

### Step 1: Cut Wing Panels

1. Mark foam board: 500mm x 180mm (two panels)
2. Cut with sharp blade, multiple light passes
3. Sand edges smooth

### Step 2: Create Airfoil Shape

**KFm2 Method (Recommended):**

1. Cut 50mm strip of foam board
2. Glue strip to top surface at 50% chord (90mm from LE)
3. This creates turbulator step for better lift

**Alternative - Curved Undercamber:**

1. Score underside of wing at 25% and 75% chord
2. Gently curve wing to create undercamber
3. Tape leading edge to hold shape

### Step 3: Add Wing Spar

1. Cut bamboo skewer or carbon rod to wingspan
2. Create channel in wing 30% back from LE
3. Glue spar in place, full span
4. Reinforce with fiberglass tape on top

### Step 4: Join Wing Panels

1. Apply dihedral (5° per panel = 10° total)
2. Use wood block to set angle
3. Glue center joint with reinforcement
4. Add fiberglass tape across joint

### Step 5: Add Wingtips (Optional)

1. Cut foam triangles for wingtips
2. Round edges for reduced drag
3. Glue at 90° to wing

### Wing Diagram

```
    Leading Edge
    ────────────────────────────────────
    │                                  │
    │   ┌─────────────────────────┐    │ ← KFm2 step (50mm wide)
    │   │   Turbulator Strip      │    │
    │   └─────────────────────────┘    │
    │         ○ Spar location          │
    │                                  │
    ────────────────────────────────────
    Trailing Edge

    ←─────── 180mm chord ───────→
```

---

## Fuselage Construction

### Step 1: Cut Fuselage Sides

1. Mark two identical sides: 600mm x 80mm
2. Taper from 80mm at nose to 50mm at tail
3. Cut both together for symmetry

### Step 2: Cut Formers

| Former | Width | Height | Location |
|--------|-------|--------|----------|
| F1 (nose) | 50mm | 80mm | 0mm |
| F2 | 60mm | 80mm | 150mm |
| F3 (wing) | 70mm | 80mm | 200mm |
| F4 | 60mm | 70mm | 400mm |
| F5 (tail) | 40mm | 50mm | 580mm |

### Step 3: Assemble Box

1. Glue F1 between fuselage sides at nose
2. Add F2, F3, F4, F5 working back
3. Cut bottom sheet to fit between sides
4. Glue bottom in place
5. Leave top open for electronics access

### Step 4: Motor Mount

1. Cut plywood or hardwood: 50mm x 50mm x 3mm
2. Mark motor bolt pattern (16mm or 19mm)
3. Drill holes for motor screws
4. Glue to rear of fuselage (F5)

### Step 5: Wing Seat

1. Cut saddle in top of fuselage at F3
2. Wing should sit flush with fuselage top
3. Test fit wing, adjust as needed

### Fuselage Diagram

```
Side View:
                                    Motor Mount
    ┌──────────────────────────────────┐ ←[M]
    │  F1   F2   F3     F4         F5  │
    │   │    │    │      │          │  │
    └───┴────┴────┴──────┴──────────┴──┘

    ←──────────── 600mm ─────────────→

Top View:
         ┌───┐
        /     \
       /       \
      │  F1     │
      │         │
      │  F2     │
      │         │
      │  F3 ════│════ Wing attachment
      │         │
      │  F4     │
      │         │
      └─────────┘
         F5
```

---

## Tail Assembly

### Horizontal Stabilizer

| Parameter | Value |
|-----------|-------|
| Span | 350mm |
| Chord | 100mm |
| Area | 3.5 dm² |
| Elevator | 30% chord (30mm) |

### Vertical Stabilizer

| Parameter | Value |
|-----------|-------|
| Height | 120mm |
| Chord | 100mm |
| Rudder | 30% chord (30mm) |

### Step 1: Cut Surfaces

1. H-stab: 350mm x 100mm rectangle
2. V-stab: 120mm x 100mm rectangle
3. Round leading edges

### Step 2: Cut Control Surfaces

1. Mark hinge line at 70% chord
2. Bevel cut at 45° for hinge
3. Attach with packing tape hinge

### Step 3: Mount to Fuselage

1. H-stab glues to top of fuselage tail
2. V-stab glues to top of H-stab
3. Ensure both are perpendicular and aligned

### Tail Diagram

```
                ┌───┐
                │ V │  ← Vertical Stab
                │   │
          ┌─────┴───┴─────┐
          │   H-Stab      │
          │               │
          └───────────────┘
              ▲
              │
          Fuselage
```

---

## Electronics Installation

### Wiring Diagram

```
Battery (3S)
    │
    ├──► ESC ──► Motor
    │     │
    │     └──► BEC 5V ──┬──► Flight Controller
    │                   │
    │                   ├──► Servos (4x)
    │                   │
    │                   ├──► Receiver
    │                   │
    │                   └──► Remote ID
    │
    └──► FC Power (if separate)
```

### Step 1: Mount Motor

1. Align motor with fuselage centerline
2. Secure with M3 screws to motor mount
3. Add prop adapter (if needed)

### Step 2: Mount ESC

1. Position ESC inside fuselage near motor
2. Allow airflow for cooling
3. Secure with velcro or zip ties
4. Route motor wires to motor

### Step 3: Mount Flight Controller

1. Position FC near CG (center of gravity)
2. Use foam tape for vibration isolation
3. Align arrow with aircraft nose
4. Secure cables to prevent vibration

### Step 4: Mount GPS

1. Position GPS on top of fuselage
2. Away from ESC and motor wires
3. Clear view of sky
4. Use foam tape mount

### Step 5: Mount Receiver

1. Position receiver antenna away from FC
2. Antenna should exit fuselage
3. Secure with foam tape

### Step 6: Mount Remote ID

1. Position module with GPS antenna up
2. Connect to FC serial port (if MAVLink)
3. Or standalone with own GPS

### Component Placement

```
Top View:
    ┌───────────────────────────────────┐
    │   [RX]    [GPS]                   │
    │                                   │
    │        [FC]     [Remote ID]       │
    │                                   │
    │   [ESC]                    [Motor]│
    └───────────────────────────────────┘
        Nose ─────────────────────► Tail
```

---

## Control Surface Setup

### Servo Positions

| Servo | Surface | Channel |
|-------|---------|---------|
| 1 | Right Aileron | CH1 |
| 2 | Left Aileron | CH1 (reversed) |
| 3 | Elevator | CH2 |
| 4 | Rudder | CH4 |

### Step 1: Install Servo

1. Cut servo pocket in wing/fuselage
2. Glue servo in place (flush with surface)
3. Route wire to fuselage

### Step 2: Control Horns

1. Mark horn position on control surface
2. Glue horn perpendicular to hinge line
3. Ensure horn is 90° to surface when neutral

### Step 3: Pushrods

1. Cut music wire or CF rod to length
2. Add Z-bend at servo arm
3. Adjust length for neutral position

### Control Throws

| Surface | Throw | Notes |
|---------|-------|-------|
| Ailerons | ±15° | Start conservative |
| Elevator | ±20° | Up/down equal |
| Rudder | ±25° | More throw OK |

---

## CG and Balance

### Target CG Location

**25-30% of wing chord from leading edge**

For 180mm chord: **45-54mm from LE**

### Step 1: Find CG

1. Mark CG location on wing
2. Support aircraft at CG marks
3. Should balance level or slightly nose-down

### Step 2: Adjust CG

| Balance | Action |
|---------|--------|
| Nose heavy | Move battery back |
| Tail heavy | Move battery forward / add nose weight |

### Step 3: Lateral Balance

1. Support aircraft at nose
2. Wings should be level
3. Add weight to light wingtip if needed

---

## Pre-Flight Checklist

### Before First Flight

- [ ] CG verified at 25-30% chord
- [ ] All control surfaces move freely
- [ ] Control directions correct (ArduPilot SETUP)
- [ ] Motor spins correct direction (pusher = CCW from rear)
- [ ] Propeller secure
- [ ] Battery secure, cannot shift
- [ ] All screws tight
- [ ] Range check passed
- [ ] Remote ID broadcasting (check with app)
- [ ] Failsafe configured (RTL or Circle)
- [ ] Arming switch works
- [ ] GPS lock acquired (6+ satellites)

### Control Direction Check

| Input | Aircraft Response |
|-------|-------------------|
| Roll right | Right aileron UP, left aileron DOWN |
| Pull elevator | Elevator UP |
| Rudder right | Rudder moves RIGHT |

### ArduPilot Parameters

```
SERVO1_FUNCTION = 4   (Aileron)
SERVO2_FUNCTION = 19  (Elevator)
SERVO4_FUNCTION = 21  (Rudder)
SERVO3_FUNCTION = 70  (Throttle)

ARMING_CHECK = 1
ARMING_RUDDER = 0     (Use switch instead)

FS_THR_ENABLE = 1     (Throttle failsafe)
FS_THR_VALUE = 975    (Failsafe PWM)
```

---

## First Flight Tips

1. **Choose calm day** - Wind < 5 mph
2. **Open field** - No obstacles
3. **Hand launch** - Firm throw, level attitude
4. **Climb immediately** - Full throttle until safe altitude
5. **Trim as needed** - Level flight, hands off
6. **Short flights** - 5 min max until confident
7. **Land into wind** - Slow approach, cut throttle over grass

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Nose drops on launch | CG too far forward | Move battery back |
| Stalls on launch | Too slow / nose high | Throw harder, level |
| Rolls on launch | Aileron trim | Adjust aileron neutral |
| Won't arm | Pre-arm checks failing | Check Mission Planner messages |
| Motor doesn't start | ESC calibration | Recalibrate ESC |
| GPS won't lock | Interference | Move GPS away from wires |

---

## Next Steps

After successful V0 flights:

1. **Tune PID** - Use ArduPilot autotune
2. **Add camera** - FPV or recording
3. **Extend range** - Test ELRS range
4. **Practice maneuvers** - Turns, figure-8s
5. **Plan V1** - Upgrade to larger battery

---

*See [SHOPPING_LIST.md](SHOPPING_LIST.md) for parts*
*See [BUILD_DIMENSIONS.md](BUILD_DIMENSIONS.md) for detailed dimensions*
