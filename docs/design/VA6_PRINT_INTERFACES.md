# VA-6 Peregrine — 3D Print Parts & Interface Design

**Printer:** Bambu Lab P1S (256 × 256 × 256mm build volume)
**Material:** PETG (primary) or ASA (UV resistant alternative)
**Wall thickness:** 3mm throughout
**Print orientation:** Sections printed nose-down (vertical) for best surface finish on outer mold line

---

## Parts List (7 printed parts)

| Part | Dimensions | Print Time (est) | Weight (est) |
|------|-----------|------------------|--------------|
| 1. Nose shell | 230mm long × 140mm dia | ~4 hrs | 120g |
| 2. Body shell | 250mm long × 140mm dia | ~5 hrs | 180g |
| 3. Aft shell | 200mm long × 140→40mm dia | ~3 hrs | 100g |
| 4-7. Fins × 4 | 160mm span × 80mm chord × 6.4mm thick | ~45 min each | 25g each |

**Not printed** (purchased or CNC):
- 4× motor pods (carbon fiber tube or aluminum, 32mm OD)
- 4× motor mounts (aluminum plate or 3D printed nylon-CF)
- 4× 4.5×2.9" custom props (CNC carbon fiber)

**Total printed weight:** ~500g (leaves 400g for purchased airframe hardware)

---

## Interface 1: Nose ↔ Body (at 230mm station)

```
CROSS-SECTION AT JOINT:

         ┌──────────────────────────┐
         │  Nose section (aft end)  │
         │                          │
    ─────┤   ┌──────────────────┐   ├─────
  140mm  │   │  Male ring       │   │  3mm wall
  OD     │   │  134mm OD        │   │
         │   │  15mm long       │   │
    ─────┤   └──────────────────┘   ├─────
         │                          │
         └──────────────────────────┘

         ┌──────────────────────────┐
         │  Body section (fwd end)  │
         │                          │
    ─────┤   ┌──────────────────┐   ├─────
  140mm  │   │  Female recess   │   │  3mm wall
  OD     │   │  134.4mm ID      │   │  (0.2mm clearance per side)
         │   │  15mm deep       │   │
    ─────┤   └──────────────────┘   ├─────
         │                          │
         └──────────────────────────┘
```

**Design details:**
- **Type:** Slip-fit ring joint with 4× M3 cross-bolts
- **Male ring:** Inner diameter wall of nose section extends 15mm past the end, 134mm OD (3mm step-in from 140mm OD)
- **Female recess:** Body forward end has 134.4mm ID recess, 15mm deep (0.2mm clearance per side for slip fit)
- **Alignment key:** One flat (D-cut) on the male ring, 10mm wide — prevents rotation, ensures fin alignment
- **Fastening:** 4× M3×12mm socket head cap screws through body wall into threaded brass inserts (M3 heat-set) in nose ring, spaced 90° apart
- **Sealing:** Optional O-ring groove in female recess (not critical for prototype)

**Assembly:** Slide nose ring into body recess, align D-key, drive 4 bolts. Reversible for maintenance access to warhead bay.

---

## Interface 2: Body ↔ Aft (at 480mm station)

Same joint design as Interface 1 — identical dimensions since both sections are 140mm OD at the joint.

```
Body (aft end):     Male ring, 134mm OD, 15mm long, D-key
Aft (forward end):  Female recess, 134.4mm ID, 15mm deep
Fastening:          4× M3×12mm bolts + M3 heat-set inserts
```

**Why identical joints:** Simplifies tooling and assembly. Same bolts, same inserts, same procedure for both joints. Only difference is which section has the male ring.

---

## Interface 3: Fins ↔ Aft Body

```
SIDE VIEW (one fin):

     Aft fuselage wall (3mm)
     ┌─────────────────────────────┐
     │                             │
     │   ┌─────────────┐           │
     │   │  Fin root    │           │
     │   │  tab (20mm)  │           │
     │   │  slides into │           │
     │   │  slot in     │           │
     │   │  fuselage    │           │
     │   └──────┬───────┘           │
     │          │                   │
     └──────────┼───────────────────┘
                │
                │  Fin blade
                │  160mm span
                │  80mm chord
                │  6.4mm thick
                │
                ▼
              [motor pod]


TOP VIEW (fin root tab):

    ┌────────────────────────────────┐
    │         Fuselage wall          │
    │                                │
    │   ┌────────────────────┐       │
    │   │    SLOT             │ ←── 7mm wide × 80mm long
    │   │    (through wall)   │      (fin thickness + 0.6mm clearance)
    │   └────────────────────┘       │
    │                                │
    └────────────────────────────────┘

          ┌──────────────────┐
          │   FIN ROOT TAB   │  ←── 20mm tall × 80mm long × 6.4mm thick
          │                  │
          │  2× M3 bolt holes│  ←── 25mm apart, centered on tab
          │                  │
          └──────────────────┘
          │                  │
          │   FIN BLADE      │
          │   (airfoil)      │
```

**Design details:**
- **Type:** Tab-and-slot with 2× M3 through-bolts per fin
- **Fin root tab:** 20mm extension beyond the airfoil root, same thickness (6.4mm). Slides through slot in fuselage wall.
- **Fuselage slot:** 7mm wide × 80mm long (chord) cut through aft section wall. 4 slots at 90° intervals.
- **Fastening:** 2× M3×20mm bolts pass through fin tab from inside fuselage, with nuts or heat-set inserts on the outside tab face
- **Fillet:** 5mm radius printed fillet at fin-fuselage junction (reduce interference drag + stress concentration). Print as part of the aft shell, or glue on separately.
- **Alignment:** Slot edges act as alignment — fin can only insert at correct angle

**Assembly:** Slide fin tab through slot from outside, reach inside fuselage to insert bolts (or use blind nuts). Field-replaceable: damaged fin → unbolt, slide out, slide in new fin.

---

## Interface 4: Motor Pods ↔ Fin Tips

```
SIDE VIEW:

    Fin tip
    ┌────────────────┐
    │                │
    │   ┌────────┐   │
    │   │ Pocket │   │  ←── 34mm dia × 10mm deep pocket in fin tip
    │   │ 34mm   │   │      (fits 32mm pod + 1mm clearance per side)
    │   └────┬───┘   │
    │        │       │
    └────────┼───────┘
             │
     ┌───────┴────────────┐
     │   Motor pod tube    │  ←── 32mm OD × 90mm long
     │   (carbon tube)     │
     │                     │
     │   ┌──────────┐      │
     │   │  Motor   │      │  ←── 2207 motor bolted to aft bulkhead
     │   └──────────┘      │
     └─────────────────────┘


END VIEW (looking along pod axis):

         Fin tip (6.4mm thick)
              │
    ┌─────────┼─────────┐
    │         │         │
    │    ┌────┴────┐    │
    │    │  Pod    │    │  ←── Pod passes through fin thickness
    │    │  32mm   │    │
    │    └────┬────┘    │
    │         │         │
    └─────────┼─────────┘
              │
```

**Design details:**
- **Pod material:** 32mm OD carbon fiber tube (lightweight, strong) or 3D printed PETG cylinder
- **Fin tip pocket:** 34mm diameter × 10mm deep circular pocket molded into fin tip (printed as part of fin)
- **Fastening:** 1× M3 pinch bolt through fin tip into pod wall (clamps pod in pocket). Or 2× M2 screws.
- **Pod internals:**
  - Forward: Pointed nose cone (printed separately, press-fit or glued)
  - Center: ESC mounted with double-sided tape
  - Aft: Motor mount bulkhead (2mm aluminum or printed CF-nylon plate)
  - Motor bolts: 4× M3×8mm through bulkhead into motor face

**Pod sub-assembly (pre-assembled before fin mounting):**
```
[nose cone] → [ESC] → [bulkhead + motor]
←── 90mm total ──→
```

---

## Interface 5: Internal Component Mounting

### Nose Section (0-230mm)

```
INTERNAL LAYOUT:

    0mm              120mm              230mm
    │←── Nose cone ──→│←── Warhead bay ──→│
    │                  │                   │
    │  Seeker window   │  Warhead          │
    │  (30mm dia)      │  (800g)           │
    │                  │                   │
    │  Lepton 3.5      │  Frag sleeve      │
    │  on printed      │  secured by       │
    │  mount shelf     │  foam cradle      │
    │                  │  + zip ties       │
```

- **Seeker mount:** Printed shelf at 50mm from nose tip, holds Lepton 3.5 + Pi Zero 2W
- **Seeker window:** 30mm clear aperture in nose tip (thin PETG wall or cut-out with polycarbonate insert)
- **Warhead cradle:** Printed foam-lined rails, warhead slides in from aft end before body section is attached

### Body Section (230-480mm)

```
INTERNAL LAYOUT:

    230mm         280mm         380mm         480mm
    │←─ Avionics ─→│←── Battery bay ──→│←─ Wiring ─→│
    │               │                   │             │
    │  FC + GPS     │  6S 5000mAh       │  ESC wires  │
    │  on standoffs │  LiPo on rails    │  to aft     │
    │               │  with velcro      │             │
    │  LoRa module  │  strap            │  Connector  │
    │  on wall      │                   │  bulkhead   │
```

- **FC mount:** 4× M3 standoffs (20mm tall) printed into body wall, standard 30.5mm FC mounting pattern
- **Battery rails:** 2× printed rails along floor, battery sits between them, velcro strap holds it in
- **Connector bulkhead:** Aft face has printed cable pass-throughs for motor/ESC wires running to aft section
- **Access:** Remove nose section to access avionics; remove aft section to access battery

### Aft Section (480-680mm)

```
INTERNAL LAYOUT:

    480mm              530mm                    680mm
    │←── Taper start ──→│←── Fin zone + taper ──→│
    │                    │                        │
    │  Wire routing      │  4× fin slots          │
    │  from body         │  4× ESC wires exit     │
    │                    │  through fin roots      │
    │                    │  to pods                │
```

- **Wire channels:** Printed internal grooves route ESC power wires from body connector to each fin slot
- **Fin slots:** 4× through-wall slots accept fin root tabs
- **Minimal internal structure** — this section tapers to 40mm, not much room. Keep it light.

---

## Assembly Order

1. **Pre-assemble motor pods** (4×): nose cone + ESC + bulkhead + motor → test motor spin
2. **Attach pods to fins** (4×): slide pod into fin tip pocket, pinch bolt
3. **Install seeker** in nose section: mount Lepton + Pi Zero on shelf, route ribbon cable
4. **Install warhead** in nose section: slide into cradle from aft end
5. **Install avionics** in body: FC on standoffs, GPS antenna on top, LoRa module on wall
6. **Insert battery** in body: slide onto rails, velcro strap
7. **Route wires** through body aft connector bulkhead
8. **Join body → aft**: slide male ring into female recess, align D-key, 4× M3 bolts
9. **Insert fins** through aft slots (4×): 2× M3 bolts each from inside
10. **Join nose → body**: slide, align, 4× M3 bolts
11. **Connect wiring**: ESC signal to FC, power to battery, seeker to Pi Zero
12. **Pre-flight check**: motor spin test, seeker image, GPS lock, LoRa link

**Total assembly time (trained operator): ~20-30 minutes**
**Disassembly for battery swap: ~2 minutes** (remove 4 aft bolts, slide aft off, swap battery)

---

## Print Settings (Bambu Studio)

| Setting | Value |
|---------|-------|
| Material | PETG (or ASA for UV) |
| Layer height | 0.2mm (standard) |
| Wall loops | 4 (gives ~1.6mm wall per side, total ~3.2mm) |
| Infill | 15% gyroid (fuselage shells) / 100% solid (fin root tabs, mounting bosses) |
| Top/bottom layers | 4 |
| Supports | Tree supports for nose cone interior |
| Orientation | Vertical (nose/tail end down) for best OML surface |
| Seam | Aligned to bottom (hidden on assembled drone) |

---

## Fastener BOM

| Fastener | Qty | Where |
|----------|-----|-------|
| M3×12mm socket head | 8 | Section joints (4 per joint × 2 joints) |
| M3×20mm socket head | 8 | Fin root tabs (2 per fin × 4 fins) |
| M3×8mm socket head | 16 | Motor face bolts (4 per motor × 4 motors) |
| M3 heat-set insert | 8 | In nose/aft male rings for joint bolts |
| M3 nut | 8 | Fin root tabs (outside face) |
| M3×6mm standoff | 4 | FC mount in body |
| M2×8mm screw | 4-8 | Pod pinch bolts + seeker mount |
| **Total M3 bolts** | **32** | |
| **Total M3 inserts/nuts** | **16** | |
