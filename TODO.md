# MegaDrone — TODO List

**Last Updated:** March 25, 2026

---

## VA-6 PEREGRINE (Interceptor Drone)

### Design (Complete)
- [x] System-of-systems architecture (detection, BMS, interceptor, comms)
- [x] OpenVSP aerodynamic model (v16)
- [x] Propulsion analysis (2207 2750KV + 5x4" prop, T/W 5.1)
- [x] Stability analysis (17.4% static margin)
- [x] Fin effectiveness analysis (2-3G aero + differential thrust)
- [x] Structural loads analysis (fuselage, fins, motor mounts)
- [x] Nose/tail shape optimization (tangent ogive + boat-tail)
- [x] Custom prop analysis → settled on off-the-shelf 5x4" 2-blade
- [x] Mass budget (2.91 kg MTOW, 0.8 kg warhead payload)
- [x] Cost analysis (~$673/unit)
- [x] DXF cross-section for Onshape CAD
- [x] 3D print section export (nose + aft body + 4 fins)
- [x] Controller board architecture (dual-processor STM32H743 + CM4)
- [x] AI tier architecture (3 tiers × 4 subsystems)

### AI Software — Tier 1 (Classical CV) — START HERE
| # | Task | Status |
|---|------|--------|
| AI-1 | Frame differencing detector (`src/detection/frame_differencing.py`) — OpenCV absdiff on webcam/camera frames, morphological filtering, blob detection | [ ] Pending |
| AI-2 | Centroid tracker (`src/detection/centroid_tracker.py`) — Track largest/brightest blob, output pixel coordinates, persistence filter | [ ] Pending |
| AI-3 | Proportional navigation guidance (`src/guidance/proportional_navigation.py`) — Convert seeker pixel error to roll/pitch/yaw commands | [ ] Pending |
| AI-4 | MAVLink bridge (`src/software/ros2_ws/src/va6_mavlink_bridge/`) — ROS 2 node translates va6_msgs/AttitudeCmd → PX4 VehicleRatesSetpoint over uxrce-dds. Mode-gated so only HIL_ENGAGED or FULL_AUTO commands forward. | [~] Scaffolded (pending bench) |
| AI-5 | Decision logic (`src/decision/engage_logic.py`) — Rule-based: IF locked AND target in velocity gate → ARM | [ ] Pending |
| AI-6 | Bench test: webcam + RPi + frame differencing on moving target | [ ] Pending |
| AI-7 | Bench test: RPi → Pixhawk MAVLink command loop | [ ] Pending |

### AI Software — Tier 2 (Neural Classifier)
| # | Task | Status |
|---|------|--------|
| AI-8 | YOLOv8-nano detector (`src/detection/yolo_detector.py`) — Run on Coral/Hailo NPU, classify target type | [ ] Pending |
| AI-9 | Synthetic training data generator (`src/training/synthetic_data.py`) — Render Shahed-136 silhouettes in various conditions | [ ] Pending |
| AI-10 | Train YOLOv8-nano on Shahed dataset | [ ] Pending |
| AI-11 | Threat scorer (`src/decision/threat_scorer.py`) — Combine speed + size + classification → threat probability | [ ] Pending |
| AI-12 | Bench test: Coral NPU + YOLO on live webcam feed at 30fps | [ ] Pending |

### AI Software — Tier 3 (RL + Swarm)
| # | Task | Status |
|---|------|--------|
| AI-13 | RL pursuit policy — Train in JSBSim or custom 6-DOF sim | [ ] Pending |
| AI-14 | Multi-modal fusion (LWIR + visible + acoustic) | [ ] Pending |
| AI-15 | Cooperative swarm logic — LoRa mesh target sharing | [ ] Pending |

### Detection System (Ground Segment)
| # | Task | Status |
|---|------|--------|
| DET-1 | Pixel-to-voxel detection system — Adapt PixelToVoxelProjector for ENU coords | [ ] Pending |
| DET-2 | Sky background model — Accumulate normal sky, enable background subtraction | [ ] Pending |
| DET-3 | Acoustic bearing estimator — GCC-PHAT on 4-mic array | [ ] Pending |
| DET-4 | Sensor fusion — Multi-sensor Kalman track fusion | [ ] Pending |
| DET-5 | Battle management system — Track manager, intercept planner, display | [ ] Pending |

### Hardware — Custom Controller Board

**Reference designs (open source, downloadable schematics + gerbers):**
- [MAVERICK H743 V1.0 (EasyEDA/OSHWLab)](https://oshwlab.com/hawaii0707/h743v1.0-flight-control-oshwhub-) — STM32H743VIH6, dual gyro BMI270+ICM42688-P, DPS310 baro. Supports ArduPilot/BetaFlight/INAV/PX4. CC-BY-NC-SA 4.0. **Best starting point — modify this design.**
- [MOONPILOT H743 (OSHWLab)](https://oshwlab.com/hawaii0707/moonpilot-h743-flight-control-se) — Similar H743, EasyEDA project.
- [HadesFCS (KiCad, GitHub)](https://github.com/pms67/HadesFCS) — Complete FC designed from scratch in KiCad. Great reference for custom board design.
- [Open source H743 for fixed-wing (ArduPilot forum)](https://discuss.ardupilot.org/t/fully-open-source-design-of-h743-flight-controller-for-fixed-wing-aircraft/126482) — Based on Blue Robotics Navigator, fixed-wing focused.
- [AET-H743-Basic (ArduPilot docs)](https://ardupilot.org/plane/docs/common-AET-H743-Basic.html) — ArduPilot-supported H743 with documented pinout.

**Approach:** Download MAVERICK H743 V1.0 EasyEDA project, modify to add CM4 connector, Lepton SPI header, LoRa SPI header, safe/arm circuit, proximity fuze GPIO. Use JLCPCB SMT assembly for 0201/BGA components (~$30-50/board qty 5).

| # | Task | Status |
|---|------|--------|
| HW-1 | Download MAVERICK H743 V1.0 EasyEDA project as baseline | [ ] Pending |
| HW-2 | Modify schematic — Add CM4 connector (2x 100-pin) for AI board | [ ] Pending |
| HW-3 | Modify schematic — Add Lepton 3.5 SPI header, LoRa SPI header | [ ] Pending |
| HW-4 | Modify schematic — Add safe/arm circuit + proximity fuze GPIO | [ ] Pending |
| HW-5 | Design AI processor board (top board) — CM4/Radxa + Hailo-8L M.2 + camera CSI | [ ] Pending |
| HW-6 | PCB layout — 4-layer, 36×36mm FC form factor, both boards | [ ] Pending |
| HW-7 | Component sourcing — BOM from LCSC/Digikey/Mouser | [ ] Pending |
| HW-8 | PCB fabrication + SMT assembly — Send to JLCPCB (incl. 0201/BGA soldering) | [ ] Pending |
| HW-9 | Firmware — ArduPilot port for flight MCU (define board target) | [ ] Pending |
| HW-10 | Integration test — AI board + flight board + motors on bench | [ ] Pending |

### Prototype Assembly
| # | Task | Status |
|---|------|--------|
| PROTO-0 | Connect Ubuntu LabDesktop (192.168.86.43) to Mac network — either direct ethernet cable, bridge routers, or move Ubuntu to Verizon WiFi (192.168.1.x). SSH key is installed, login: mattuh | [ ] Blocked — different subnets |
| PROTO-1 | Prototype AI with existing hardware (RPi + Pixhawk + webcam) | [ ] Pending |
| PROTO-2 | Buy prototype components (see BOM below) | [ ] Pending |
| PROTO-3 | 3D print nose section (Bambu P1S, PETG) | [ ] Pending |
| PROTO-4 | 3D print aft body section | [ ] Pending |
| PROTO-5 | 3D print 4x fins | [ ] Pending |
| PROTO-6 | Cut 5" PVC pipe body section (250mm) | [ ] Pending |
| PROTO-7 | Assemble airframe — glue/bolt sections | [ ] Pending |
| PROTO-8 | Motor/ESC/prop bench test — verify thrust + T/W | [ ] Pending |
| PROTO-9 | First flight test (no AI, manual/autopilot only) | [ ] Pending |
| PROTO-10 | AI flight test — frame differencing + PN guidance on RPi | [ ] Pending |

### CAD / Manufacturing
| # | Task | Status |
|---|------|--------|
| CAD-1 | Build parametric model in Onshape from DXF cross-section | [ ] In Progress |
| CAD-2 | Shell/hollow fuselage sections (3mm wall) | [ ] Pending |
| CAD-3 | Add section joint features (slip-fit rings, bolt holes) | [ ] Pending |
| CAD-4 | Add internal mounting features (FC standoffs, battery rails) | [ ] Pending |
| CAD-5 | Export STL sections for Bambu Studio | [ ] Pending |

---

## AI PROTOTYPE BOM (Using Existing Hardware + New Purchases)

### Hardware On Hand
- [ ] Raspberry Pi (model: _____)
- [ ] Pixhawk (version: _____)
- [ ] USB Webcam

### Hardware To Buy
| Item | Purpose | Cost | Source |
|------|---------|------|--------|
| FLIR Lepton 3.5 + PureThermal Mini | IR seeker prototype | $300 | GroupGets/Digikey |
| Google Coral USB Accelerator | NPU for YOLO at 30fps | $35 | Amazon/coral.ai |
| LoRa SX1276 HAT for RPi | Datalink prototype | $15 | Amazon |
| USB GPS dongle (u-blox) | Position for ground test | $12 | Amazon |
| 4x 2207 2750KV motors | Propulsion test | $40 | Amazon/RDQ |
| 4x 30A ESC | Motor control | $40 | Amazon/RDQ |
| 4x 5x4" props (Gemfan/HQ) | Thrust test | $8 | Amazon |
| 6S 5000mAh LiPo | Power | $60 | Amazon |
| 2-axis servo gimbal (SG90) | Point camera at target | $8 | Amazon |
| Foam RC target plane | Test target | $30 | Amazon |
| **Total new purchases** | | **~$548** | |
| **Without Lepton** (start visible-only) | | **~$248** | |

---

## PRIORITY ORDER

1. **AI-1 to AI-5** — Tier 1 software (webcam + RPi, no new hardware needed)
2. **PROTO-1** — Bench test RPi → Pixhawk MAVLink
3. **AI-6, AI-7** — Bench integration tests
4. **HW-1 to HW-3** — Custom controller board schematic + PCB layout
5. **CAD-1 to CAD-5** — Onshape model for 3D printing
6. **PROTO-2** — Buy remaining components
7. **HW-4, HW-5** — Send boards for manufacture
8. **AI-8 to AI-12** — Tier 2 neural classifier
9. **PROTO-3 to PROTO-9** — Physical prototype build + first flight

---

## DOCUMENTS

| Document | Location |
|----------|----------|
| System architecture | `docs/design/VA6_PEREGRINE_SYSTEM_PLAN.md` |
| Controller board | `docs/design/VA6_CONTROLLER_BOARD.md` |
| Print interfaces | `docs/design/VA6_PRINT_INTERFACES.md` |
| OpenVSP model | `designs/va6/VA6_Peregrine.vsp3` (latest) |
| DXF cross-section | `designs/va6/VA6_Peregrine_v16_OML.dxf` |
| STL (mm scale) | `designs/va6/VA6_Peregrine_v16_mm.stl` |
| Section STLs | `designs/va6/sections/*_mm.stl` |
