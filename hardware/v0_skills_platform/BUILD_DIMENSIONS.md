# V0 Build Dimensions - Complete Specification

**Target AUW:** 900g | **Wingspan:** 1100mm | **Length:** 600mm

---

## Summary Dimensions

| Component | Dimension |
|-----------|-----------|
| **Wingspan** | 1100mm (43.3") |
| **Wing Chord** | 165mm (6.5") |
| **Wing Area** | 18.15 dm² |
| **Fuselage Length** | 600mm (23.6") |
| **Overall Length** | 650mm (25.6") |
| **H-Stab Span** | 350mm |
| **V-Stab Height** | 120mm |

---

## Wing

### Planform

```
                    1100mm (43.3")
    ←─────────────────────────────────────────→

    ┌─────────────────────────────────────────┐
    │                                         │  ↑
    │              WING                       │  165mm
    │                                         │  ↓
    └─────────────────────────────────────────┘

    ├────────────┤
       Aileron
       200mm
```

| Parameter | Value |
|-----------|-------|
| **Span** | 1100mm |
| **Chord** | 165mm (constant, rectangular) |
| **Area** | 1815 cm² (18.15 dm²) |
| **Aspect Ratio** | 6.67 |
| **Airfoil** | Flat-bottom (Clark Y profile) or 10% flat plate |
| **Dihedral** | 5° per side (10° total) |
| **Incidence** | +2° (leading edge up relative to fuselage) |
| **Twist** | 0° (none for simplicity) |

### Wing Construction

```
    Cross-Section (looking from wingtip):

         ┌──────────────────────────────┐
        ╱                                ╲    ← 10% thickness
       ╱                                  ╲      (16.5mm max)
      ╱           Spar @ 30%               ╲
     ────────────────┬─────────────────────────
                     │
                     │ ← 6mm carbon tube or bamboo
                     │   at 50mm from LE (30% chord)
```

| Parameter | Value |
|-----------|-------|
| **Thickness** | ~16.5mm (10% of chord) |
| **Spar Location** | 50mm from leading edge (30% chord) |
| **Spar Material** | 6mm carbon tube or bamboo skewer |
| **Skin Material** | 5mm foam board (Dollar Tree) |
| **Covering** | Packing tape (full coverage) |

### Wing Panels (2 pieces)

Each panel:
| Parameter | Value |
|-----------|-------|
| **Panel Span** | 550mm (half wingspan) |
| **Root Chord** | 165mm |
| **Tip Chord** | 165mm |
| **Dihedral Angle** | 5° |
| **Dihedral Rise** | 48mm at tip (550mm × tan(5°)) |

### Ailerons (2x)

| Parameter | Value |
|-----------|-------|
| **Span** | 200mm each |
| **Chord** | 40mm (24% of wing chord) |
| **Location** | Outboard, 50mm from wingtip |
| **Hinge** | Tape hinge on bottom surface |
| **Deflection** | ±15° |
| **Servo** | 9g micro, mounted in wing |

```
    Aileron Location (per wing panel):

    ├──── 300mm ────┼─── 200mm ───┼─50mm─┤
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

    ←───────────────── 600mm ─────────────────→

                                        ┌──┐
                                       ╱│  │
                                      ╱ │  │ V-stab
         ════════════════════════════╱══╧══│     ↑
              H-stab                 │     │    120mm
                                     │     │     ↓
         ════════════════════════════╪═════│────────
              Wing @ 200mm           │     │
                     ↓               │     │
    ┌────────────────────────────────┴─────┤
    │            FUSELAGE                  │[P] ← Motor
    │  80mm height                         │
    └──────────────────────────────────────┘

    ├─100mm─┼────── 300mm ──────┼─200mm─┤
      Nose      Electronics       Tail boom
```

| Parameter | Value |
|-----------|-------|
| **Total Length** | 600mm |
| **Nose Section** | 100mm (battery bay) |
| **Center Section** | 300mm (electronics bay) |
| **Tail Boom** | 200mm |
| **Width** | 80mm |
| **Height** | 80mm (box fuselage) |
| **Material** | 5mm foam board, box construction |

### Top View

```
    ←───────────────── 600mm ─────────────────→

    ┌──────────────────────────────────────────┐
    │                                          │  ↑
    │              FUSELAGE                    │  80mm
    │                                          │  ↓
    └──────────────────────────────────────────┘

    ├─100mm─┤
     Battery
      Bay
```

### Fuselage Sections

| Section | Length | Purpose |
|---------|--------|---------|
| **Nose** | 100mm | Battery (slide forward/back for CG) |
| **Bay 1** | 150mm | FC, GPS, Receiver |
| **Bay 2** | 150mm | ESC, wiring |
| **Tail Boom** | 200mm | To tail surfaces |

### Construction

```
    Cross-Section:

         ┌────── 80mm ──────┐
         │                  │
         │                  │  80mm
         │    [Battery]     │
         │    [FC/GPS]      │
         └──────────────────┘

    Material: 5mm foam board sides
              Reinforced with bamboo skewers at corners
```

---

## Horizontal Stabilizer

```
    ←─────────── 350mm ───────────→

    ┌─────────────────────────────┐
    │                             │  ↑
    │        H-STAB               │  100mm
    │                             │  ↓
    └──────────┬──────────────────┘
               │
           Elevator
            80mm
```

| Parameter | Value |
|-----------|-------|
| **Span** | 350mm |
| **Chord** | 100mm |
| **Area** | 350 cm² (3.5 dm²) |
| **H-Stab Ratio** | 19% of wing area |
| **Airfoil** | Flat plate (symmetric) |
| **Incidence** | 0° |
| **Location** | Top of tail boom, 550mm from nose |

### Elevator

| Parameter | Value |
|-----------|-------|
| **Span** | 300mm (full span minus tips) |
| **Chord** | 30mm (30% of H-stab chord) |
| **Deflection** | ±20° |
| **Servo** | 9g micro, in fuselage |
| **Linkage** | Push rod, ~250mm |

---

## Vertical Stabilizer

```
              ↑
              │
              │  120mm
              │
    ┌─────────┴─────────┐
    │                   │
    │      V-STAB       │  ← 80mm chord
    │                   │
    └───────────────────┘
              │
          Rudder
           30mm
```

| Parameter | Value |
|-----------|-------|
| **Height** | 120mm |
| **Root Chord** | 80mm |
| **Tip Chord** | 60mm (tapered) |
| **Area** | ~84 cm² |
| **Location** | Rear of fuselage, on top |

### Rudder

| Parameter | Value |
|-----------|-------|
| **Height** | 100mm |
| **Chord** | 25mm (30% of V-stab chord) |
| **Deflection** | ±25° |
| **Servo** | 9g micro, in tail boom |
| **Linkage** | Push rod or pull-pull cables |

---

## Motor Mount

```
    Rear View:

              ▲
             ╱│╲
            ╱ │ ╲
           ╱  │  ╲   V-stab
          ╱   │   ╲
         ─────┴─────
              │
              │
         ┌────┴────┐
         │  Motor  │  ← 2212 920kv
         │   [●]   │    Pusher config
         └─────────┘
              │
              ▼
           9x6 prop
```

| Parameter | Value |
|-----------|-------|
| **Location** | Rear of fuselage, centerline |
| **Height** | Prop clears H-stab by 20mm |
| **Thrust Line** | Aligned with CG (0° down/right thrust) |
| **Motor** | 2212 920kv |
| **Prop** | 9x6 pusher (or 10x4.5) |
| **Mount** | 3D printed or plywood plate |

### Motor Mount Plate

| Parameter | Value |
|-----------|-------|
| **Size** | 50mm × 50mm |
| **Material** | 3mm plywood or 3D printed |
| **Hole Pattern** | 16mm or 19mm (check motor) |
| **Attachment** | Epoxy + screws to fuselage |

---

## Center of Gravity (CG)

**Critical for stable flight!**

```
    Side View with CG Location:

    ←───────────────── 600mm ─────────────────→

         Wing Leading Edge
              ↓
              │
    ┌─────────┼──────────────────────────────┐
    │    ●    │                              │
    │   CG    │                              │
    └─────────┴──────────────────────────────┘

    ├─200mm───┤
      CG from nose

         ├─50mm─┤
         CG from wing LE
         (30% MAC)
```

| Parameter | Value |
|-----------|-------|
| **CG from Nose** | 200mm |
| **CG from Wing LE** | 50mm (30% of 165mm chord) |
| **CG Range** | 45-55mm from wing LE (27-33% MAC) |

### CG Adjustment

| If CG is... | Action |
|-------------|--------|
| Too far forward (nose heavy) | Move battery back |
| Too far back (tail heavy) | Move battery forward, add nose weight |

**Test:** With wing at fingertips at CG point, nose should drop slightly (5-10°).

---

## Component Placement

```
    Top View - Component Layout:

    ←───────────────── 600mm ─────────────────→

    ┌────────┬─────────────────────────────────┐
    │        │                                 │
    │ [BATT] │  [FC]  [GPS]  [RX]  [ESC]      │
    │        │                                 │
    └────────┴─────────────────────────────────┘

    ├──100mm─┼──150mm──┼──150mm──┼───200mm────┤
      Battery   FC Bay    ESC Bay    Tail Boom
```

| Component | Location (from nose) | Notes |
|-----------|---------------------|-------|
| **Battery** | 0-100mm | Slide for CG adjustment |
| **Flight Controller** | 120-150mm | Center of aircraft |
| **GPS** | 150-180mm | On top, clear view of sky |
| **Receiver** | 180-200mm | Antenna routing |
| **ESC** | 250-300mm | Near motor, heat dissipation |
| **Motor** | 580-600mm | Rear pusher |

### Servo Placement

| Servo | Location |
|-------|----------|
| **Aileron L** | In left wing, 350mm from centerline |
| **Aileron R** | In right wing, 350mm from centerline |
| **Elevator** | In fuselage, ~400mm from nose |
| **Rudder** | In tail boom, ~500mm from nose |

---

## Control Surface Throws

| Surface | Travel | High Rate | Low Rate |
|---------|--------|-----------|----------|
| **Ailerons** | ±15° | ±15° | ±10° |
| **Elevator** | ±20° | ±20° | ±12° |
| **Rudder** | ±25° | ±25° | ±15° |

### Expo Settings (recommended)

| Surface | Expo |
|---------|------|
| Ailerons | 30% |
| Elevator | 30% |
| Rudder | 20% |

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

Per 14 CFR 89.501, home-builders are exempt from production requirements but must meet operational requirements (broadcast ASTM F3411 compliant messages).

| Component | Cost | Notes |
|-----------|------|-------|
| ESP32-S3 DevKitC | $12 | BT + WiFi broadcast |
| Wiring to FC | $5 | Uses FC GPS via MAVLink |
| **Total** | **~$17** | vs $35-79 commercial |

**Open Source Resources:**

| Project | Link |
|---------|------|
| ArduRemoteID | [github.com/ArduPilot/ArduRemoteID](https://github.com/ArduPilot/ArduRemoteID) |
| OpenDroneID | [github.com/opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| ESP32 Tutorial | [hackster.io/...drone-id-requirement](https://www.hackster.io/user462411/esp32-for-government-drone-id-requirement-64a5c9) |

**Wiring (MAVLink):**
```
FC TX  ──►  ESP32 RX (GPIO18)
FC RX  ◄──  ESP32 TX (GPIO17)
GND    ◄─►  GND
5V     ──►  5V
```

**ArduPilot Config:** `SERIALx_PROTOCOL = 45`, `SERIALx_BAUD = 57600`

### Installation

```
    Top View - Remote ID Placement:

    ┌────────┬─────────────────────────────────┐
    │        │  ┌─────────┐                    │
    │ [BATT] │  │ RemoteID│  [FC]  [GPS]      │
    │        │  └─────────┘                    │
    └────────┴─────────────────────────────────┘

              @ 160-180mm from nose (on top)
```

| Parameter | Value |
|-----------|-------|
| **Location** | Top of fuselage, 160-180mm from nose |
| **Mounting** | Velcro or double-sided tape |
| **Antenna** | Must have clear sky view |
| **Power** | 5V from FC BEC |
| **Weight** | 6-8g (add to weight budget) |

### Updated Weight Budget

| Component | Mass (g) | % |
|-----------|----------|---|
| Airframe (foam) | 300-350 | 33% |
| Battery | 180 | 19% |
| Motor + Prop | 70 | 7% |
| ESC | 30 | 3% |
| FC + GPS | 65 | 7% |
| Receiver | 10 | 1% |
| Servos (4×) | 36 | 4% |
| Wiring/Hardware | 50 | 5% |
| **Remote ID** | **8** | **1%** |
| **Margin** | 142 | 15% |
| **Total** | **~908g** | 100% |

---

## Material Cut List

### Foam Board (5mm Dollar Tree)

| Part | Quantity | Size (mm) |
|------|----------|-----------|
| **Wing Panel** | 2 | 550 × 165 |
| **Fuselage Side** | 2 | 600 × 80 |
| **Fuselage Top** | 1 | 600 × 80 |
| **Fuselage Bottom** | 1 | 600 × 80 |
| **H-Stab** | 1 | 350 × 100 |
| **V-Stab** | 1 | 120 × 80 (tapered) |
| **Elevator** | 1 | 300 × 30 |
| **Rudder** | 1 | 100 × 25 |
| **Ailerons** | 2 | 200 × 40 |
| **Motor Mount Plate** | 1 | 50 × 50 (plywood) |

### Carbon/Bamboo

| Part | Quantity | Size |
|------|----------|------|
| **Wing Spar** | 1 | 6mm × 1100mm carbon tube |
| **Fuselage Longerons** | 4 | 3mm × 600mm bamboo |
| **Push Rods** | 3 | 2mm × 300mm steel wire |

### Hardware

| Part | Quantity |
|------|----------|
| Control horns | 6 |
| Clevises | 6 |
| Servo screws | 16 |
| Zip ties | 20 |
| Velcro (battery) | 1 strip |

---

## Assembly Order

1. **Build wing panels** (cut, add spar, shape LE)
2. **Join wing panels** (dihedral gauge: 48mm rise at 550mm)
3. **Cut fuselage sides**
4. **Assemble fuselage box**
5. **Add reinforcement** (corner longerons)
6. **Mount wing to fuselage** (rubber bands or bolt)
7. **Build H-stab and V-stab**
8. **Attach tail surfaces**
9. **Install motor mount**
10. **Install servos**
11. **Run pushrods**
12. **Install electronics** (FC, GPS, RX, ESC)
13. **Install Remote ID module** (top of fuselage, 160-180mm)
14. **Wire Remote ID** (5V from FC BEC)
15. **Cover with packing tape**
16. **Balance CG**
17. **Register Remote ID** (FAA DroneZone)
18. **Range check**
19. **Fly!**

---

## Pre-Flight Checklist

### Structure
- [ ] CG at 50mm from wing LE (30% MAC)
- [ ] All control surfaces move correct direction
- [ ] Battery secure
- [ ] Prop tight, correct rotation (pusher)

### Electronics
- [ ] Range check passed
- [ ] Failsafe set (throttle to zero, level flight)

### Remote ID (FAA Required)
- [ ] Remote ID module powered on
- [ ] Remote ID has GPS lock (LED indication)
- [ ] Registered in FAA DroneZone
- [ ] Serial number matches registration

### Environment
- [ ] Wind < 10 km/h for first flight
- [ ] Not in restricted airspace (check B4UFLY app)

---

## Drawing Templates

### Wing Rib (full size at 100%)

```
    ←───────── 165mm ─────────→

    ┌──────────────────────────┐
   ╱                            ╲   ↑
  ╱              ●               ╲  16.5mm
 ────────────────┴────────────────  ↓
                 │
            Spar hole
            @ 50mm
            (6mm dia)
```

### Dihedral Gauge

```
    Set wing panel at this angle:

           ╱
          ╱  5°
         ╱
        ╱
    ───┴───

    At 550mm span: tip is 48mm higher than root
```

---

*Document Version: 1.0*
*Created: January 2026*
*Aircraft: MegaDrone V0 Skills Platform*
