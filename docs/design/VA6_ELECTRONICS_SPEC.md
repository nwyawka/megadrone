# VA-6 Electronics Specification Sheet

**Status:** Draft — consolidates parts already specified in
`VA6_CONTROLLER_BOARD.md` / `VA6_PEREGRINE_SYSTEM_PLAN.md` / `TODO.md` and
adds the five items that were previously unspecified (RC receiver, antennas,
battery monitoring, status LEDs, airspeed sensor).

**Scope:** complete electrical bill of materials for one airframe, both
VA-6 Peregrine (interceptor) and the ISR-surveillance twin. Where the two
variants diverge, this sheet notes the differences.

---

## 1. Summary table

| # | Function | Part | Spec | Qty | Location | Notes |
|---|---|---|---|---|---|---|
| 1 | Flight controller MCU | **STM32H743VIT6** | 480 MHz Cortex-M7, 2 MB flash | 1 | FC board, main sled electronics compartment | Specified in `VA6_CONTROLLER_BOARD.md` |
| 2 | Companion / AI compute | **Raspberry Pi CM4 2 GB (lite eMMC)** | Quad A72 1.5 GHz, WiFi/BT optional | 1 | Top of main sled electronics compartment | CM4 picked over Radxa Zero 3W for better community support + Hailo-8L compatibility |
| 3 | AI accelerator | **Hailo-8L M.2 2242** | 13 TOPS, M.2 key M | 1 | M.2 socket on AI board atop CM4 | Required for Tier-2 YOLO vision; optional for basic autopilot |
| 4 | GPS receiver | **u-blox MAX-M10S** | L1/L5 multiband, 25×25 mm module | 1 | Top of main sled, near aft bulkhead for clear sky view | Uses UART to FC; 1 Hz nav fix |
| 5 | IMU | **InvenSense ICM-42688-P** | 6-axis, ±16 g / ±2000 dps, SPI | 1 | FC board, vibration-isolated | High-rate EKF input |
| 6 | Barometer | **Bosch BMP390** | 0.25 m resolution, SPI | 1 | FC board | Altitude-hold + vertical-rate |
| 7 | Magnetometer | **QMC5883L** | 3-axis, I²C | 1 | FC board, >30 mm from PDB | Heading hold |
| 8 | Airspeed sensor (NEW) | **TE MS4525DO-DS5AI001DP** + 5 mm pitot tube | Differential 0–1 psi, I²C | 1 | Pitot tube in nose tip aperture region; sensor on FC board | Required for true-airspeed control at ≥100 km/h; calibrated pitot dynamic pressure |
| 9 | Battery current/voltage (NEW) | **Holybro PM02D** | 0–60 A hall sensor, 2–14S, I²C | 1 | Between battery and ESC power lead | Reports Vbatt, Ibatt, mAh consumed to FC; inline fuse |
| 10 | ESC (BLHeli32 4-in-1) | **HGLRC Zeus 60 A 4-in-1** | 6S, 60 A continuous, DShot600, BLHeli_32 | 1 | Main sled, aft of battery | Sized for 2207 motors at 6S peak current |
| 11 | Motors | **iFlight XING2 2207 2750 KV** | 27.9 mm OD, 16 mm M3 hex, 29 g | 4 | Wing-tip motor pads | See `motor plan` for prop selection |
| 12 | Battery | **CNHL G+ Plus 6S1P 5000 mAh 100 C** | 22.2 V, 111 Wh, 165×53×52 mm, ~735 g | 1 | Main sled battery bay (centered on drone axis) | See motor plan |
| 13 | Cameras | **Raspberry Pi Camera v2 (IMX219)** | 8 MP, CSI-2, M12 lens mount, 25×24 mm PCB | 4 | Camera cage in nose — fore / port / starboard / down | Matches camera cage mount footprint |
| 14 | RC receiver (NEW) | **RadioMaster RP3 ELRS 2.4 GHz** | ExpressLRS v3, diversity, 10 × 10 mm | 1 | Top of forward payload sled | Manual-override link; ≥ 10 km LoS range on 100 mW |
| 15 | Primary datalink (VA-6R) | **Semtech SX1276** LoRa module | 868/915 MHz, +20 dBm | 1 | FC board | Telemetry + command uplink |
| 16 | Secondary datalink (VA-6F stretch) | Fiber-optic SFP module (part TBD) | 1.25 Gb SFP, 1310 nm single-mode | 1 | Aft of payload sled, fiber spool on pay-out reel | F-variant only; not required for ISR use |
| 17 | Antennas (NEW) | See §3 below | | multiple | See §3 | |
| 18 | Status / arm LEDs (NEW) | **WS2812B 5 mm PCB LED ring (8-LED)** | 5 V, individually addressable | 1 | Top of aft payload sled, visible through PVC wall | Arm / GPS-lock / battery-low patterns |
| 19 | Safety arm circuit | Discrete MOSFET + relay (schematic TBD) | GPIO-controlled high-side arm to warhead/payload | 1 | Warhead bay on VA-6 only | Interlocked with CDM324 proximity + manual safe pin |
| 20 | Proximity fuze | **CDM324** 24 GHz Doppler radar | Detects target approach at < 5 m | 1 | Nose, ahead of warhead (VA-6 only) | Interceptor only, NOT in ISR variant |
| 21 | Power rail 5 V | **TI TPS5430** | 3 A buck, 95% eff | 1 | FC board | Supplies CM4 + cameras + RX |
| 22 | Power rail 3.3 V | **AMS1117-3.3** | 1 A LDO | 1 | FC board | STM32 + sensor bus |

Grand total active parts: 22.

---

## 2. Power budget (at 22.2 V / 6S nominal)

| Subsystem | Current (A) | Power (W) | Notes |
|---|---|---|---|
| 4× motors at cruise (371 W shaft / 80 % eff) | ~21 | 464 | 92 W shaft per motor × 4 |
| 4× motors peak (dash) | ~70 (burst) | 1 550 | 300 km/h dash, 2 sec burst |
| CM4 + Hailo-8L | 0.45 | 10 | YOLO Tier-2 active |
| 4× Pi Cameras | 0.15 | 3 | 4× 250 mA @ 3.3 V |
| FC board (STM32 + sensors + radios) | 0.10 | 2 | All active |
| ELRS RX | 0.02 | 0.4 | 100 mW TX |
| LoRa TX (transmit) | 0.13 | 3 | +20 dBm burst |
| LED ring | 0.1 | 2 | Max brightness |
| **Total non-motor** | **≈ 1 A** | **≈ 20 W** |  |
| **Total cruise** | **~ 22 A** | **~ 485 W** |  |
| **Total dash (2 sec burst)** | **~ 70 A** | **~ 1 570 W** |  |

Battery must deliver ≥ 70 A pulsed → 100 C × 5 Ah = 500 A burst capability ✓.

---

## 3. Antennas (NEW — details)

### 3a. GPS antenna
- **Part:** u-blox ANN-MB-00 active patch antenna, 25 × 25 mm, SMA(M)
- **Placement:** top surface of the antenna mount block (already in CAD at `build_antenna_mount()`, block top face +Z side). Two M5 CSK screws through the block secure the patch ground plane.
- **Ground plane:** aluminum disc ≥ 50 × 50 mm, on top of antenna mount block — or use the PCB-integrated ground plane on the u-blox reference design.
- **Cable:** RG-178 SMA(M) → UFL to MAX-M10S, 150 mm.

### 3b. ELRS RC receiver antenna
- **Part:** 2 × dipole 2.4 GHz 50 mm "T-antenna" (comes with most ELRS RX)
- **Placement:** one in each wing tip region, routed through the existing spar hole in the wing (no CAD change required). Cable 50 mm UFL.
- **Polarization:** one vertical, one horizontal (diversity).

### 3c. LoRa telemetry antenna
- **Part:** helical quarter-wave whip 868 MHz, ~8 cm, SMA(M) (e.g. Linx ANT-868-CW-HW)
- **Placement:** rear of payload sled, penetrating PVC tube at the antenna-mount block's aft end (or routed out through the aft boattail open face).
- **Ground plane:** ≥ 1/4 λ radial, lives on the FC board.

---

## 4. Physical placement map

```
  X=0                         X=127            X=700       X=745
  ┌─────────────────────────┐┌─────────────────────────┐┌──────────┐
  │  NOSE (cameras)         ││  BODY (PVC tube)        ││ BOATTAIL │
  │                         ││                         ││          │
  │  • 4× Pi Cam v2 (cage)  ││  Payload sled (fore):   ││ Open aft │
  │  • Camera cage (rigid)  ││   • ELRS RX + antennas  ││ (exhaust)│
  │  • pitot tube (airspd)  ││   • GPS antenna (top)   ││          │
  │                         ││   • LED ring            ││          │
  │                         ││   • LoRa antenna (SMA)  ││          │
  │                         ││                         ││          │
  │                         ││  Main sled (aft):       ││          │
  │                         ││   • 6S 5 Ah battery     ││          │
  │                         ││   • PM02D PDB + sensor  ││          │
  │                         ││   • HGLRC Zeus ESC      ││          │
  │                         ││   • FC board (STM32)    ││          │
  │                         ││   • CM4 + Hailo-8L      ││          │
  └─────────────────────────┘└─────────────────────────┘└──────────┘
      ↑                            ↑                          ↑
    Apex cam, 3× side            Antenna mount block       Open boattail
    cameras, camera cage         (top, +Z)                  (cable egress)
```

Bay lengths (main sled):
- Payload (fore): 40 mm — ELRS RX, LED ring driver
- Battery (middle): 170 mm — 6S 5 Ah pack
- Electronics (aft): 30 mm — ESC + FC + CM4 + PM02D

---

## 5. Wiring / bus map

| Bus | Peripherals | Speed |
|---|---|---|
| SPI1 | ICM-42688-P IMU, BMP390 baro | 10 MHz |
| I²C1 | QMC5883L mag, MS4525DO airspeed, PM02D battery monitor | 400 kHz |
| UART1 | u-blox GPS | 115 200 |
| UART2 | ELRS RX (CRSF) | 420 000 |
| UART3 | LoRa SX1276 | 115 200 |
| UART4 | ESC telemetry (BLHeli_32 passthrough) | 115 200 |
| USB-HS | CM4 ↔ STM32 command/control | USB 2.0 |
| CSI-2 | 4× Pi Cam (via MIPI multiplexer to CM4) | 1.5 Gb/s per lane |
| GPIO | LED ring (SPI-bitbang), arm circuit, safe-pin detect | — |

---

## 6. What's still TBD

- **Fiber-optic SFP module** (item 16) — only needed for VA-6F variant. Wait until after VA-6R proves out LoRa link.
- **Safety arm discrete HW** (item 19) — schematic pending `HW-4`. Interceptor variant only.
- **ELRS TX** on ground side — not part of the airframe BOM.
- **Pitot tube mechanical integration** — needs a 5 mm aperture through the front camera window or a separate small aperture alongside it. Add to CAD in a follow-up pass.
- **WS2812 driver** — assume FC STM32 SPI bit-bang; no external driver IC.

---

## 7. Change log

- 2026-04-19: Initial consolidation. Added items 8 (airspeed), 9 (PM02D current/voltage), 14 (ELRS RX), 17 (antennas), 18 (LED ring) to the previously-specified parts list. Battery spec updated from 4S 5 Ah to 6S 5 Ah per motor plan.
