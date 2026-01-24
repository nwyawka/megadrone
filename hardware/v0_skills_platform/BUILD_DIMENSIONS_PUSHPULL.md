# V0 Push-Pull Twin Build Dimensions

**Target AUW:** 1100g | **Wingspan:** 1000mm | **Length:** 800mm | **Config:** Inline Twin (Push-Pull) with V-Tail

---

## Design Philosophy

This variant uses two motors in a push-pull (centerline thrust) configuration for:
- **Redundancy** - Single engine failure is survivable
- **Torque cancellation** - Counter-rotating props neutralize roll
- **Easy CG** - Motors at both ends balance naturally
- **Higher speed** - Increased wing loading for sportier flight
- **Extended endurance** - Single-engine cruise mode option
- **Upgradeable** - Modular wing and battery options

---

## Summary Dimensions

| Component | Dimension |
|-----------|-----------|
| **Wingspan** | 1000mm (39.4") |
| **Wing Chord** | 160mm (6.3") |
| **Wing Area** | 16.0 dm² |
| **Aspect Ratio** | 6.25 |
| **Fuselage Length** | 700mm (27.6") |
| **Overall Length** | 800mm (31.5") |
| **H-Stab Span** | 320mm |
| **V-Stab Height** | 110mm |
| **Wing Loading** | 68.75 g/dm² |

---

## Performance Specs

| Parameter | Value |
|-----------|-------|
| **Stall Speed** | 30 km/h (8.3 m/s) |
| **Landing Speed** | 36 km/h (10 m/s) |
| **Cruise Speed** | 65 km/h (18 m/s) |
| **Max Speed** | 100 km/h (28 m/s) |
| **Static Thrust** | 1530g |
| **Thrust/Weight** | 1.39:1 |
| **Endurance** | 15-17 min (3000mAh) |

### Speed Comparison

| Speed | V0 Single | V0 Push-Pull | Increase |
|-------|-----------|--------------|----------|
| Stall | 25 km/h | 30 km/h | +20% |
| Landing | 30 km/h | 36 km/h | +20% |
| Cruise | 54 km/h | 65 km/h | +20% |
| Max | 80 km/h | 100 km/h | +25% |

---

## Wing

### Planform

```
                      1000mm (39.4")
    ←───────────────────────────────────────→

    ┌───────────────────────────────────────┐
    │                                       │  ↑
    │               WING                    │  160mm
    │                                       │  ↓
    └───────────────────────────────────────┘

    ├──────────┤                  ├─────────┤
      Aileron                       Aileron
       180mm                         180mm
```

| Parameter | Value |
|-----------|-------|
| **Span** | 1000mm |
| **Chord** | 160mm (constant, rectangular) |
| **Area** | 1600 cm² (16.0 dm²) |
| **Aspect Ratio** | 6.25 |
| **Airfoil** | Clark Y or 10% flat plate |
| **Dihedral** | 4° per side (8° total) |
| **Incidence** | +2° (leading edge up) |
| **Twist** | 0° |

### Wing Construction

```
    Cross-Section (looking from wingtip):

         ┌────────────────────────────────┐
        ╱                                  ╲    ← 10% thickness
       ╱                                    ╲      (16mm max)
      ╱             Spar @ 30%               ╲
     ──────────────────┬──────────────────────
                       │
                       │ ← 6mm carbon tube
                       │   at 48mm from LE (30% chord)
```

| Parameter | Value |
|-----------|-------|
| **Thickness** | ~16mm (10% of chord) |
| **Spar Location** | 48mm from leading edge (30% chord) |
| **Spar Material** | 6mm carbon tube or bamboo |
| **Skin Material** | 5mm foam board |
| **Covering** | Packing tape (full coverage) |

### Wing Panels (2 pieces)

Each panel:

| Parameter | Value |
|-----------|-------|
| **Panel Span** | 500mm (half wingspan) |
| **Root Chord** | 160mm |
| **Tip Chord** | 160mm |
| **Dihedral Angle** | 4° |
| **Dihedral Rise** | 35mm at tip (500mm × tan(4°)) |

### Ailerons (2×)

| Parameter | Value |
|-----------|-------|
| **Span** | 180mm each |
| **Chord** | 40mm (25% of wing chord) |
| **Location** | Outboard, 40mm from wingtip |
| **Hinge** | Tape hinge on bottom surface |
| **Deflection** | ±18° (increased for higher speed) |
| **Servo** | 9g micro, mounted in wing |

```
    Aileron Location (per wing panel):

    ├──── 280mm ────┼─── 180mm ───┼─40mm─┤
                    │   AILERON   │
                    │    40mm     │
    ────────────────┴─────────────┴──────
         Fixed           Moves      Tip
```

---

## Fuselage

### Dimensions

```
    Side View:

    ←──────────────────── 700mm ────────────────────→

    ▲                                  V-tail       ▲
   ╱│╲                                 ╲ │ ╱       ╱│╲
    │                                   ╲│╱         │
   [M]────────────────────────────────────┴────────[M]
    │     ┌────────────────────────────────┐        │
    │     │          Fuselage              │        │
    ▼     │           80mm                 │        ▼
          └───────────┬────────────────────┘
   Front              │                           Rear
   Motor           Wing @ 250mm                  Motor

    ├─100mm─┼─100mm─┼────── 300mm ──────┼─50mm┼─150mm─┤
      Nose   Battery      Electronics   V-tail  Motor
```

| Parameter | Value |
|-----------|-------|
| **Total Length** | 700mm |
| **Nose Section** | 100mm (front motor mount) |
| **Battery Bay** | 100mm |
| **Electronics Bay** | 300mm |
| **Tail Boom** | 200mm (rear motor) |
| **Width** | 80mm |
| **Height** | 80mm (box fuselage) |
| **Material** | 5mm foam board, box construction |

### Top View

```
    ←──────────────────── 700mm ────────────────────→

    ┌────────────────────────────────────────────────┐
    │                                                │  ↑
   [●]               FUSELAGE                       [●] 80mm
    │                                                │  ↓
    └────────────────────────────────────────────────┘
   Front                                            Rear
   Motor                                           Motor

    ├─100mm─┤
     Motor
     Mount
```

### Fuselage Sections

| Section | Length | Position | Purpose |
|---------|--------|----------|---------|
| **Nose** | 100mm | 0-100mm | Front motor mount + firewall |
| **Battery Bay** | 100mm | 100-200mm | 3000mAh 3S (slide for CG) |
| **Bay 1** | 150mm | 200-350mm | FC, GPS, Receiver |
| **Bay 2** | 150mm | 350-500mm | 2× ESC, wiring, Remote ID |
| **V-Tail Mount** | 50mm | 500-550mm | V-tail attachment point |
| **Motor Bay** | 150mm | 550-700mm | Rear motor + firewall |

### Cross-Section

```
         ┌────── 80mm ──────┐
         │                  │
         │                  │  80mm
         │    [Battery]     │
         │    [FC/GPS]      │
         └──────────────────┘

    Material: 5mm foam board sides
              Reinforced with bamboo at corners
              Extra reinforcement at motor mounts
```

---

## Motor Mounts

### Front Motor (Tractor)

```
    Side View:

                      Firewall (3mm ply)
                            │
    ▲                       │
   ╱│╲  9×6 Prop            │
    │      25mm             │
   [●]─────────────────────┼─────────────
    │      Motor            │   Fuselage
    ▼                       │
                            │
```

| Parameter | Value |
|-----------|-------|
| **Firewall Size** | 60mm × 60mm |
| **Firewall Material** | 3mm plywood |
| **Motor Standoff** | 10mm (for prop clearance) |
| **Prop Clearance** | 25mm to fuselage |
| **Thrust Angle** | 2° right thrust, 2° down thrust |
| **Hole Pattern** | 16mm or 19mm (match motor) |

### Rear Motor (Pusher)

```
    Side View:
                                          Firewall
                                              │
                                              │       ▲
     ─────────────────────────────────────────┼──────[●]
                              Fuselage        │       │
                                              │      ╱│╲
                                              │       ▼
                                              │    9×6 Prop
```

| Parameter | Value |
|-----------|-------|
| **Firewall Size** | 50mm × 50mm |
| **Firewall Material** | 3mm plywood |
| **Prop Clearance** | 20mm to H-stab |
| **Thrust Angle** | 0° (aligned with fuselage) |
| **Mount Style** | Same as single pusher V0 |

### Counter-Rotating Props

```
    Front View:

         ↺ CCW                         CW ↻
          ╲│╱                         ╲│╱
           ●───────── Fuselage ────────●
          ╱│╲                         ╱│╲
        Front                        Rear
       (Tractor)                   (Pusher)

    CRITICAL: Props must counter-rotate!
    - Front: CCW when viewed from front
    - Rear: CW when viewed from rear
    - Result: Torque cancels, no roll tendency
```

| Motor | Rotation | Prop Type |
|-------|----------|-----------|
| **Front** | CCW (from front) | 9×6 Tractor (normal) |
| **Rear** | CW (from rear) | 9×6 Pusher (reverse pitch) |

---

## V-Tail (Ahead of Pusher)

The V-tail is positioned **forward of the rear pusher motor** for:
- Clean prop airflow (pusher operates in undisturbed air)
- Protected control surfaces (no prop wash on ruddervators)
- Simplified construction (no separate H-stab and V-stab)
- Reduced parts count (2 servos instead of separate elevator + rudder)

```
    Rear View:

              ╲         ╱
               ╲   V   ╱
                ╲     ╱  ← V-tail (110° included angle)
                 ╲   ╱
                  ╲ ╱
                   │
                  [●] ← Motor BEHIND V-tail
                  ╱│╲
                   ▼
                  Prop
```

```
    Side View:

                    V-tail
                      │
    ─────────────────/┴\─────────[●]────
                   ╱    ╲        Motor
                  ╱      ╲

    ├────────────550mm───────────┼──150mm──┤
         V-tail position          Motor
```

```
    Top View:

                 ╲         ╱
                  ╲       ╱
                   ╲     ╱
    ────────────────╲   ╱────────[●]────
                     ╲ ╱         Motor
                      │
                  Fuselage
```

### V-Tail Dimensions

| Parameter | Value |
|-----------|-------|
| **Included Angle** | 110° (55° from horizontal each side) |
| **Panel Span** | 180mm each (360mm tip-to-tip) |
| **Panel Chord** | 100mm |
| **Total Area** | 360 cm² (3.6 dm²) |
| **Tail Volume** | 0.45 (adequate for stability) |
| **Airfoil** | Flat plate (symmetric) |
| **Location** | 550mm from nose (150mm ahead of rear motor) |

### Ruddervators (2×)

V-tail control surfaces combine elevator and rudder functions:

| Parameter | Value |
|-----------|-------|
| **Span** | 160mm each |
| **Chord** | 30mm (30% of panel chord) |
| **Deflection** | ±25° |
| **Servo** | 9g micro each (2 total) |
| **Linkage** | Push rods, ~100mm |

### V-Tail Mixing

| Stick Input | Left Ruddervator | Right Ruddervator | Result |
|-------------|------------------|-------------------|--------|
| Elevator UP | UP | UP | Pitch up |
| Elevator DOWN | DOWN | DOWN | Pitch down |
| Rudder LEFT | DOWN | UP | Yaw left |
| Rudder RIGHT | UP | DOWN | Yaw right |

**FC Setup:** Enable V-tail mixing in ArduPilot/Betaflight, or use transmitter mixing:
- Left ruddervator = Elevator + Rudder
- Right ruddervator = Elevator - Rudder

### V-Tail Construction

```
    V-Tail Panel (make 2, mirror):

    ←───── 100mm chord ─────→

    ┌───────────────────────┐
    │                       │  ↑
    │      V-TAIL PANEL     │  180mm
    │                       │  span
    └───────────────────────┘

    Hinge line for ruddervator:
    ├──── 70mm ────┼─ 30mm ─┤
         Fixed      Moves
```

| Construction | Details |
|--------------|---------|
| **Material** | 5mm foam board |
| **Spar** | 3mm bamboo at 30% chord |
| **Hinge** | Tape hinge on bottom |
| **Root Block** | Foam block for fuselage attachment |

### V-Tail Angle Jig

```
    Build jig to set 110° included angle:

              ╲         ╱
               ╲  110° ╱
                ╲     ╱
                 ╲   ╱
                  ╲ ╱
                   │
              ─────┴─────
                 Jig

    Each panel: 55° from horizontal
    Measure: 35° from vertical
```

---

## Propulsion System

### Motors (2×)

| Parameter | Value |
|-----------|-------|
| **Model** | 2212 920kv (both identical) |
| **Weight** | 55g each (110g total) |
| **Max Current** | 15A each |
| **Recommended Prop** | 9×6 |

### Props

| Position | Prop | Type | Thrust |
|----------|------|------|--------|
| **Front** | 9×6 | Tractor (normal) | ~850g |
| **Rear** | 9×6 | Pusher (reverse) | ~680g* |
| **Total** | — | — | **~1530g** |

*Rear prop operates in disturbed air, ~80% efficiency

### ESCs (2×)

| Parameter | Value |
|-----------|-------|
| **Rating** | 30A each |
| **Weight** | 30g each (60g total) |
| **BEC** | 5V 3A (one provides system power) |
| **Location** | Electronics bay, 350-400mm from nose |

### Battery

| Parameter | Value |
|-----------|-------|
| **Recommended** | 3000mAh 3S LiPo |
| **Weight** | 240g |
| **Dimensions** | ~135 × 45 × 25mm |
| **C Rating** | 30C minimum |
| **Max Current** | 30A continuous |

### Power Budget

| Phase | Current | Power | Notes |
|-------|---------|-------|-------|
| **Cruise (dual)** | 14A | 155W | 65 km/h |
| **Cruise (single)** | 8A | 88W | 50 km/h |
| **Climb** | 25A | 275W | 3 m/s climb |
| **Max** | 40A | 440W | Full throttle |
| **Endurance (dual)** | — | — | 15-17 min |
| **Endurance (single)** | — | — | **25-30 min** |

---

## Single-Engine Cruise Mode

For extended endurance, shut down one motor during cruise:

```
    Single-Engine Mode:

    Front OFF          OR          Rear OFF
       ╳                              ●
       │                              │
    ───┴─────────────────────────────[●]───
                                    Active

       │                              │
    ──[●]────────────────────────────┴───
     Active                           ╳
```

### Single-Engine Performance

| Parameter | Both Motors | Front Only | Rear Only |
|-----------|-------------|------------|-----------|
| **Thrust** | 1530g | 850g | 680g |
| **T/W** | 1.39 | 0.77 | 0.62 |
| **Cruise Speed** | 65 km/h | 55 km/h | 50 km/h |
| **Cruise Current** | 14A | 8A | 7A |
| **Endurance** | 15-17 min | 25-28 min | 28-32 min |

### Recommended: Rear Motor Only

Running on the **rear pusher only** is preferred:
1. **Cleaner airflow** - No prop wash over wing
2. **Torque compensation** - Easier to trim
3. **CG forward** - Dead front motor acts as nose weight
4. **Restart capability** - Front can restart in-flight if needed

### How to Implement

**Option 1: Manual switch**
- Assign motor kill to switch (CH5 or CH6)
- Cut throttle to front motor only
- Rear motor at cruise throttle (~50%)

**Option 2: ArduPilot automation**
- Set up motor interlock per motor
- Create flight mode with single motor
- Auto-switch based on mission phase

**Option 3: Simple Y-cable disconnect**
- Physical disconnect of front ESC signal
- Manual re-connect for takeoff/landing

### Flight Procedure

| Phase | Motors | Throttle |
|-------|--------|----------|
| **Takeoff** | Both | 70% |
| **Climb to altitude** | Both | 60% |
| **Cruise transition** | Shut front | 50% rear |
| **Extended cruise** | Rear only | 45-55% |
| **Pre-landing** | Restart front | 40% both |
| **Approach** | Both | As needed |
| **Landing** | Both | Idle |

### Single-Engine Considerations

| Concern | Mitigation |
|---------|------------|
| **Asymmetric thrust** | None - centerline motor |
| **Yaw trim** | Slight rudder trim for torque |
| **Restart failure** | Land on one motor (possible) |
| **Emergency power** | Restart front for go-around |

---

## Upgrade Paths

This design supports modular upgrades for improved performance:

### Battery Upgrades

| Battery | Weight | AUW | Endurance (Dual) | Endurance (Single) |
|---------|--------|-----|------------------|-------------------|
| 3000mAh 3S (stock) | 240g | 1100g | 15-17 min | 25-30 min |
| **4000mAh 3S** | 320g | 1180g | 20-23 min | 35-40 min |
| **5000mAh 3S** | 400g | 1260g | 25-28 min | 45-50 min |
| **4000mAh 4S** | 350g | 1210g | 18-20 min* | 30-35 min* |

*4S requires different props (8×6) and ESC programming

### Wing Upgrades

| Wing | Span | Chord | Area | Wing Loading | Cruise Speed | Stall |
|------|------|-------|------|--------------|--------------|-------|
| **Stock** | 1000mm | 160mm | 16 dm² | 69 g/dm² | 65 km/h | 30 km/h |
| **Endurance** | 1200mm | 180mm | 21.6 dm² | 51 g/dm² | 50 km/h | 22 km/h |
| **Speed** | 900mm | 140mm | 12.6 dm² | 87 g/dm² | 80 km/h | 38 km/h |

### Endurance Wing Specs

For maximum loiter time:

| Parameter | Value |
|-----------|-------|
| **Span** | 1200mm |
| **Chord** | 180mm |
| **Area** | 21.6 dm² |
| **Aspect Ratio** | 6.67 |
| **Dihedral** | 5° per side |
| **Spar** | 6mm carbon × 1200mm |
| **Expected Endurance** | 45+ min (single engine, 5000mAh) |

### Speed Wing Specs

For maximum speed:

| Parameter | Value |
|-----------|-------|
| **Span** | 900mm |
| **Chord** | 140mm |
| **Area** | 12.6 dm² |
| **Aspect Ratio** | 6.43 |
| **Dihedral** | 3° per side |
| **Spar** | 6mm carbon × 900mm |
| **Expected Max Speed** | 110+ km/h |

### Wing Attachment System

Design fuselage wing saddle for quick wing swaps:

```
    Wing Saddle (top of fuselage):

    ┌─────────────────────────────┐
    │  ○               ○          │  ← Bolt holes (4×)
    │                             │
    │      Wing Saddle            │  100mm × 200mm
    │                             │
    │  ○               ○          │
    └─────────────────────────────┘

    Wings attach with 4× M3 nylon bolts
    or rubber bands through hooks
```

---

## Remote ID Module

**Required for FAA compliance** (effective March 2024)

### Option 1: Commercial Modules

| Module | Weight | Cost | Notes |
|--------|--------|------|-------|
| **Dronetag Mini** | 6g | $79 | Built-in GPS, Bluetooth |
| **Cube ID** | 8g | $35 | Requires FC GPS feed |
| **BlueMark db120** | 5g | $49 | Integrated, standalone |

### Option 2: DIY (Home-Built for Education/Recreation)

Per 14 CFR 89.501, home-builders are exempt from production requirements but must meet operational requirements (broadcast compliant ASTM F3411 messages).

| Component | Cost | Notes |
|-----------|------|-------|
| ESP32-S3 DevKitC | $12 | BT + WiFi broadcast |
| Wiring to FC | $5 | Uses FC GPS via MAVLink |
| **Total** | **~$17** | vs $35-79 commercial |

**Open Source Firmware:**

| Project | Description |
|---------|-------------|
| [ArduRemoteID](https://github.com/ArduPilot/ArduRemoteID) | Official ArduPilot implementation |
| [OpenDroneID](https://github.com/opendroneid/opendroneid-core-c) | Core C library (ASTM F3411) |
| [ESP32 Tutorial](https://www.hackster.io/user462411/esp32-for-government-drone-id-requirement-64a5c9) | DIY build guide |

**Wiring (MAVLink to FC):**
```
FC TX  ──►  ESP32 RX (GPIO18)
FC RX  ◄──  ESP32 TX (GPIO17)
GND    ◄─►  GND
5V     ──►  5V
```

**ArduPilot Config:**
```
SERIALx_PROTOCOL = 45
SERIALx_BAUD = 57600
```

### Installation Location

```
    Top View - Remote ID Placement:

    [M]──────┬────────────────────────────────[M]
             │
             │  ┌─────────┐
             │  │ RemoteID│  ← Top of fuselage
             │  │  Module │     Clear sky view
             │  └─────────┘
             │
    ─────────┴──────────────────────────────────
              @ 280-300mm from nose
```

| Parameter | Value |
|-----------|-------|
| **Location** | Top of fuselage, 280-300mm from nose |
| **Mounting** | Velcro or double-sided tape |
| **Antenna** | Must have clear sky view |
| **Power** | 5V from FC BEC or separate battery |

### Remote ID Wiring

```
    From FC 5V BEC:

    FC ────┬──── Servos
           │
           └──── Remote ID Module
                 (5V, GND only - no data)
```

### Weight Addition

| Component | Weight |
|-----------|--------|
| Remote ID Module | 6g |
| Wiring | 2g |
| **Total Addition** | **8g** |

**Updated AUW with Remote ID: 1108g**

---

## Center of Gravity (CG)

```
    Side View with CG Location:

    ←──────────────────── 700mm ────────────────────→

         Wing Leading Edge
              @ 250mm
                 ↓
                 │
    [M]──────────┼─────────────────────────────[M]
         ●       │
        CG      Wing
    @ 290mm      │
                 │
    ├───290mm────┤
      CG from nose

         ├─40mm─┤
         CG from wing LE
         (25% MAC)
```

| Parameter | Value |
|-----------|-------|
| **CG from Nose** | 290mm |
| **CG from Wing LE** | 40mm (25% of 160mm chord) |
| **CG Range** | 35-48mm from wing LE (22-30% MAC) |

### CG Notes

Push-pull configuration makes CG balancing easier:
- Front motor pulls CG forward
- Rear motor pulls CG backward
- Battery position is less critical than single-motor designs
- Aircraft naturally balances near center

### CG Adjustment

| If CG is... | Action |
|-------------|--------|
| Too far forward | Move battery back 10-20mm |
| Too far back | Move battery forward 10-20mm |
| Still off | Add ballast (nose or tail) |

**Balance Test:** Aircraft should hang level or nose-down 5° when suspended from CG point.

---

## Component Placement

```
    Top View - Component Layout:

    ←──────────────────── 700mm ────────────────────→

    ┌────────────────────────────────────────────────┐
    │                                                │
   [M]  [BATT]  [FC]  [GPS]  [RX]  [ESC1] [ESC2]  [M]
    │                                                │
    └────────────────────────────────────────────────┘

    ├100mm┼─100mm─┼──────── 300mm ────────┼──200mm──┤
     Motor  Battery       Electronics        Motor
```

| Component | Location (from nose) | Notes |
|-----------|---------------------|-------|
| **Front Motor** | 0-50mm | On firewall |
| **Battery** | 100-200mm | Slide for CG |
| **Flight Controller** | 220-250mm | Center of aircraft |
| **GPS** | 260-290mm | On top, clear sky view |
| **Receiver** | 290-320mm | Antenna routing |
| **ESC #1 (Front)** | 350-380mm | Near front motor wires |
| **ESC #2 (Rear)** | 380-410mm | Near rear motor wires |
| **Rear Motor** | 650-700mm | On rear firewall |

### Servo Placement

| Servo | Location |
|-------|----------|
| **Aileron L** | In left wing, 320mm from centerline |
| **Aileron R** | In right wing, 320mm from centerline |
| **Ruddervator L** | In V-tail root, ~520mm from nose |
| **Ruddervator R** | In V-tail root, ~520mm from nose |

**Note:** 4 servos total (same as conventional tail, but V-tail mixing required)

---

## Wiring Diagram

```
                         ┌─────────────────┐
                         │    Battery      │
                         │  3000mAh 3S     │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │  ESC #1  │  │    FC    │  │  ESC #2  │
              │  Front   │  │  + GPS   │  │   Rear   │
              │   30A    │  │  + RX    │  │   30A    │
              └────┬─────┘  └──────────┘  └────┬─────┘
                   │                           │
                   │    ┌─────────────┐        │
                   │    │   Servos    │        │
                   │    │  (4× 9g)    │        │
                   │    └─────────────┘        │
                   │                           │
                   ▼                           ▼
              ┌──────────┐               ┌──────────┐
              │  Motor   │               │  Motor   │
              │  Front   │               │   Rear   │
              │  2212    │               │   2212   │
              └──────────┘               └──────────┘
```

### FC Channel Assignments

| Channel | Function | Notes |
|---------|----------|-------|
| CH1 | Aileron | Y-cable to both servos |
| CH2 | Ruddervator L | V-tail mixed |
| CH3 | Throttle Front | ESC #1 |
| CH4 | Ruddervator R | V-tail mixed |
| CH7 | Throttle Rear | ESC #2 |

**V-Tail Mixing:** Enable in FC (ArduPilot: VTAIL_OUTPUT) or transmitter.

**Throttle Options:**
1. **Y-cable** - Both motors same speed (simpler wiring)
2. **Separate channels** - Allows differential thrust mixing (more control)

---

## Control Surface Throws

| Surface | Travel | High Rate | Low Rate |
|---------|--------|-----------|----------|
| **Ailerons** | ±18° | ±18° | ±12° |
| **Elevator** | ±25° | ±25° | ±15° |
| **Rudder** | ±30° | ±30° | ±18° |

### Expo Settings (recommended for higher speed)

| Surface | Expo |
|---------|------|
| Ailerons | 35% |
| Elevator | 40% |
| Rudder | 25% |

**Note:** Higher expo recommended due to increased control sensitivity at higher speeds.

---

## Weight Budget

| Component | Mass (g) | % |
|-----------|----------|---|
| Airframe (foam) | 360 | 33% |
| Battery | 240 | 22% |
| Motors (×2) | 110 | 10% |
| Props (×2) | 30 | 3% |
| ESCs (×2) | 60 | 5% |
| FC + GPS | 65 | 6% |
| Receiver | 10 | 1% |
| Servos (4×) | 36 | 3% |
| Wiring/Hardware | 75 | 7% |
| Motor mounts (ply) | 30 | 3% |
| **Margin** | 84 | 8% |
| **Total** | **~1100g** | 100% |

---

## Material Cut List

### Foam Board (5mm Dollar Tree)

| Part | Qty | Size (mm) | Notes |
|------|-----|-----------|-------|
| **Wing Panel** | 2 | 500 × 160 | Left and right |
| **Fuselage Side** | 2 | 700 × 80 | Longer than single |
| **Fuselage Top** | 1 | 700 × 80 | |
| **Fuselage Bottom** | 1 | 700 × 80 | |
| **V-Tail Panel** | 2 | 180 × 100 | Left and right (mirror) |
| **Ruddervator** | 2 | 160 × 30 | Cut from V-tail panels |
| **Ailerons** | 2 | 180 × 40 | |
| **Nose Doubler** | 2 | 100 × 80 | Extra strength |
| **V-Tail Root Block** | 1 | 80 × 80 × 40 | Foam block, shaped |

### Plywood (3mm)

| Part | Qty | Size (mm) | Notes |
|------|-----|-----------|-------|
| **Front Firewall** | 1 | 60 × 60 | Motor mount |
| **Rear Firewall** | 1 | 50 × 50 | Motor mount |
| **Bulkheads** | 2 | 70 × 70 | Internal structure |

### Carbon/Bamboo

| Part | Qty | Size | Notes |
|------|-----|------|-------|
| **Wing Spar** | 1 | 6mm × 1000mm | Carbon tube |
| **Fuselage Longerons** | 4 | 3mm × 700mm | Bamboo |
| **Push Rods** | 3 | 2mm × 250mm | Steel wire |

### Hardware

| Part | Qty |
|------|-----|
| Control horns | 6 |
| Clevises | 6 |
| Servo screws | 16 |
| Motor screws | 8 |
| Zip ties | 30 |
| Velcro (battery) | 1 strip |
| Y-cable (throttle) | 1 (optional) |

---

## Assembly Order

### Phase 1: Wing (Day 1)

1. **Cut wing panels** - 2× 500 × 160mm
2. **Score spar channel** - 48mm from LE, both panels
3. **Insert wing spar** - 6mm carbon tube
4. **Join panels at dihedral** - Use gauge: 35mm rise at 500mm
5. **Cut ailerons** - Score and separate 180 × 40mm
6. **Hinge ailerons** - Tape hinge on bottom
7. **Install aileron servos** - In wing, 320mm from center
8. **Cover wing** - Packing tape, full coverage

### Phase 2: Fuselage (Day 2)

9. **Cut fuselage sides** - 2× 700 × 80mm
10. **Cut fuselage top/bottom** - 2× 700 × 80mm
11. **Install front firewall** - 60 × 60mm ply at nose
12. **Install rear firewall** - 50 × 50mm ply at tail
13. **Assemble box** - Hot glue, check square
14. **Add corner longerons** - 4× 700mm bamboo
15. **Install bulkheads** - At 200mm and 400mm
16. **Reinforce nose** - Extra foam doublers

### Phase 3: V-Tail (Day 2)

17. **Cut V-tail panels** - 2× 180 × 100mm
18. **Add spar** - 3mm bamboo at 30% chord each panel
19. **Cut ruddervators** - Score and separate 160 × 30mm
20. **Hinge ruddervators** - Tape hinge on bottom
21. **Build V-tail root block** - 80 × 80 × 40mm foam
22. **Attach panels to root** - 110° included angle (use jig)
23. **Install ruddervator servos** - In root block
24. **Attach V-tail assembly** - 550mm from nose, ahead of motor

### Phase 4: Motors (Day 3)

25. **Mount front motor** - On front firewall, 10mm standoff
26. **Mount rear motor** - On rear firewall (behind V-tail)
27. **Check prop clearances** - 25mm front, 20mm to V-tail rear
28. **Install props** - CCW front, CW rear (counter-rotating!)

### Phase 5: Electronics (Day 3)

29. **Install FC** - Center of fuselage, 220-250mm
30. **Mount GPS** - On top, 260-290mm
31. **Install receiver** - 290-320mm
32. **Mount Remote ID** - On top, 280-300mm, clear sky view
33. **Mount ESCs** - 350-410mm area
34. **Wire motors to ESCs** - Check rotation direction
35. **Wire ESCs to FC** - CH3 front, CH7 rear (or Y-cable to CH3)
36. **Wire Remote ID** - 5V from FC BEC
37. **Run pushrods** - Connect to V-tail ruddervators

### Phase 6: Final Assembly (Day 4)

38. **Attach wing to fuselage** - Rubber bands or bolts
39. **Install battery** - Velcro mount, 100-200mm
40. **Cover all surfaces** - Packing tape
41. **Balance CG** - Target 290mm from nose
42. **Program FC** - Enable V-tail mixing, set control directions
43. **Register Remote ID** - FAA DroneZone
44. **Range check** - Full range test
45. **Ground test motors** - Both directions correct

---

## Pre-Flight Checklist

### Structure
- [ ] CG at 290mm from nose (40mm from wing LE)
- [ ] Wing secure (rubber bands tight)
- [ ] V-tail secure, 110° angle correct
- [ ] All control surfaces move freely
- [ ] No loose parts or rattles

### Controls (V-Tail Mixing)
- [ ] Ailerons: Stick right → right aileron UP
- [ ] Elevator: Stick back → BOTH ruddervators UP
- [ ] Rudder: Stick right → left ruddervator DOWN, right UP
- [ ] Throttle: Stick up → both motors increase

### Propulsion
- [ ] Both props tight
- [ ] Props counter-rotating (CCW front, CW rear)
- [ ] Front prop clears fuselage (25mm)
- [ ] Rear prop clears V-tail (20mm)
- [ ] Motors spin correct direction

### Electronics
- [ ] Battery secure
- [ ] Battery voltage OK (>11.4V for 3S)
- [ ] Receiver bound
- [ ] Failsafe set (throttle zero, level flight)
- [ ] Range check passed (30m minimum)

### Remote ID (FAA Required)
- [ ] Remote ID module powered on
- [ ] Remote ID has GPS lock (LED indication)
- [ ] Registered in FAA DroneZone
- [ ] Serial number matches registration

### Environment
- [ ] Wind < 15 km/h (first flights < 10 km/h)
- [ ] Clear area for takeoff/landing
- [ ] No people in prop arc
- [ ] Not in restricted airspace (check B4UFLY app)

---

## Flight Notes

### First Flight

1. **Use low rates** - Ailerons ±12°, Elevator ±15°, Rudder ±18°
2. **Start with 50% throttle** - Get feel for aircraft
3. **Higher landing speed** - 36 km/h vs 30 km/h for single
4. **More momentum** - Heavier aircraft, plan approaches earlier
5. **Check both motors** - Listen for sync, no vibration

### Handling Characteristics

| Characteristic | Notes |
|----------------|-------|
| **Roll rate** | Quick, responsive |
| **Pitch authority** | Strong |
| **Yaw** | Rudder + differential thrust (if enabled) |
| **Stall behavior** | Clean break, easy recovery |
| **Glide** | Good, both props windmill |

### Emergency: Single Engine

If one motor fails:
1. **Reduce throttle** - Prevent asymmetric thrust
2. **Both motors off** - Use as glider
3. **Gentle turns** - Away from dead motor
4. **Land immediately** - Don't attempt to fly on one motor

---

## Drawing Templates

### Wing Panel (500 × 160mm)

```
    ←─────────── 500mm ───────────→

    ┌─────────────────────────────┐
   ╱                               ╲   ↑
  ╱               ●                 ╲  16mm
 ────────────────┴───────────────────  ↓
                 │
            Spar hole @ 48mm
                (6mm dia)

    ← 160mm chord →
```

### Dihedral Gauge (4°)

```
    Set wing panel at this angle:

           ╱
          ╱  4°
         ╱
        ╱
    ───┴───

    At 500mm span: tip is 35mm higher than root
```

### Motor Rotation Check

```
    View from FRONT of aircraft:

         ↺ CCW              CW ↻
          ╲│╱              ╲│╱
           ●────────────────●
          ╱│╲              ╱│╲
        FRONT             REAR

    If motors spin wrong direction:
    - Swap any 2 of the 3 motor wires
    - Or reverse in ESC programming
```

---

## Specifications Summary

| Parameter | Value |
|-----------|-------|
| **Configuration** | Push-Pull, V-Tail |
| **Wingspan** | 1000mm |
| **Length** | 800mm |
| **Wing Area** | 16.0 dm² |
| **V-Tail Area** | 3.6 dm² |
| **AUW** | 1108g (incl. Remote ID) |
| **Wing Loading** | 69.25 g/dm² |
| **Thrust** | 1530g |
| **T/W Ratio** | 1.38:1 |
| **Stall Speed** | 30 km/h |
| **Landing Speed** | 36 km/h |
| **Cruise Speed** | 65 km/h |
| **Max Speed** | 100 km/h |
| **Endurance (Dual)** | 15-17 min |
| **Endurance (Single)** | 25-30 min |
| **Battery** | 3000mAh 3S |
| **Motors** | 2× 2212 920kv |
| **Props** | 9×6 tractor + 9×6 pusher |
| **Remote ID** | Required (6g module) |

---

*Document Version: 1.0*
*Created: January 2026*
*Aircraft: MegaDrone V0 Push-Pull Skills Platform*
*FAA Remote ID Compliant*
