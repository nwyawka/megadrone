# Phase 1 Bench Test — MAVLink Bridge Spine

Goal: prove that a ROS 2 `va6_msgs/AttitudeCmd` published on the CM4
produces the correct motor response on the FC, with round-trip latency
< 10 ms, and that mode-gating keeps motors silent in non-authorized modes.

This is the first integration test of the VA-6 software stack. Pass here
unblocks Phase 2 (frame-diff + centroid tracker).

---

## 1. Hardware shopping list

### Compute + flight-control
| Item | Part | Qty | Approx cost |
|---|---|---|---|
| CM4 module | Raspberry Pi CM4 2 GB eMMC (CM4002032) | 1 | $65 |
| CM4 carrier | Waveshare CM4-IO-BASE-A or official CM4 IO | 1 | $30 |
| microSD (boot tools only) | 32 GB SDHC | 1 | $10 |
| Flight controller | Holybro Kakute H7 V2 (or any STM32H743 FC) | 1 | $80 |
| 4-in-1 ESC | HGLRC Zeus 60 A / SpeedyBee BLS 50 A | 1 | $55 |
| Motor(s) | iFlight XING2 2207 2750 KV — **1 motor is enough** for bench | 1 | $24 |
| Battery | 4S or 6S LiPo, any 2500+ mAh, 50C+ | 1 | $40 |
| Battery checker / alarm | HobbyMate / any low-voltage alarm | 1 | $8 |
| LiPo charger (if none) | SkyRC iMAX B6 or similar | 1 | $45 |

### Radio control
| Item | Part | Qty | Approx cost |
|---|---|---|---|
| RC transmitter | RadioMaster Pocket (ELRS) or TX16S | 1 | $65 |
| RC receiver | RadioMaster RP3 ELRS 2.4 GHz | 1 | $22 |

### Cables + wiring
| Item | Spec | Qty |
|---|---|---|
| Dupont jumpers (F-F) | 10 cm | 10 |
| XT60 power lead | 12 AWG silicone | 1 |
| ESC signal cable | preferably already on 4-in-1 ESC | — |
| USB-C cable | CM4 power | 1 |
| USB-A → Micro-USB / USB-C | PX4 programming | 1 |
| Soldering kit | iron, solder, flux, tweezers | — |

### Bench / safety gear
| Item | Spec | Qty |
|---|---|---|
| Motor test stand | Any clamp that securely holds one motor shaft-up | 1 |
| **DO NOT use props** | — if you must spin with a prop, use a 2 " training prop only | — |
| Fire extinguisher | LiPo-rated (Class D dry chem) | 1 |
| Safety glasses | — | 1 per person |
| LiPo-safe bag | — | 1 |

**Total hardware cost ≈ $450** (most are one-time purchases reusable for Phase 2–4).

---

## 2. Software prerequisites

### On the CM4 (target)
- Ubuntu 22.04 LTS (aarch64) on eMMC
- ROS 2 Humble installed via `src/software/setup/install_ubuntu_22.04.sh`
- `micro-ros-agent` either installed system-wide or built from source
- `src/software/ros2_ws` built with `colcon build --symlink-install`
- `ubuntu` user in `dialout` group (installer already does this)

### On the STM32H7 (target)
- PX4 v1.14 firmware, built from https://github.com/PX4/PX4-Autopilot
- Board target: your specific FC's target (e.g. `holybro_kakuteh7_default`). The project will have a `custom_va6_default` target later — use the off-the-shelf target for bench now.
- Parameters:
  ```
  MAV_1_CONFIG       = TELEM2     # UART to CM4
  SER_TEL2_BAUD      = 921600
  UXRCE_DDS_CFG      = TELEM2
  COM_RC_LOSS_T      = 2.0
  COM_OBL_RC_ACT     = 4          # Land on offboard+RC loss
  CBRK_IO_SAFETY     = 22027      # bypass safety switch for bench
  COM_DISARM_LAND    = 0.5
  RATES_PID_DEFAULTS = 1          # first pass, retune later
  ```

### On your laptop (host)
- QGroundControl v4.3+ (for PX4 param editing + log download)
- SSH client
- Git

---

## 3. Wiring

Bench test uses a single motor and a single FC ↔ CM4 UART link.

```
                 +-------------- Battery (4S/6S) -------------+
                 |                                            |
                 v                                            |
          +-------------+                                     |
          |   4-in-1    |  (motor phase wires to M1 only)     |
          |    ESC      |─── Motor #1 (secure on test stand)  |
          +------+------+                                     |
                 | DShot signal                               |
                 v                                            |
    +------------+---------------+                            |
    |   Holybro Kakute H7 V2     |  <-------- USB-C (prog) ---+
    |   (or any STM32H743 FC)    |
    |                            |
    |  TELEM2  TX  RX  GND       |
    +----+----+----+----+----+---+
         |    |    |    |
         |    |    |    |
         +---+| RX |    |
             ||    |    +-------------- GND
             |+----+---+
                     |
                   TELEM2 @ 921600 baud
                     |
         +-----------v---------+
         |        CM4          |
         |  (GPIO14/15 UART0   |
         |   OR USB-UART FTDI) |
         +---------+-----------+
                   |
                   v
             SSH / laptop
```

Details:

1. **CM4 ↔ STM32 UART**: cross-connect (STM32 TX → CM4 RX, STM32 RX → CM4 TX, common GND). 3.3 V logic both sides — no level shifter needed. Use GPIO14 (TX) / GPIO15 (RX) on the CM4 if you disable Bluetooth, or use a USB-UART dongle (easier for first bench).

2. **ESC signal**: one pin from FC M1 output → ESC signal input.

3. **Motor**: ONE motor on the ESC's M1 channel. Shaft pointed up, clamped firmly. **NO PROP.** If you must, a 5030 "training" 2" prop is OK, but bare shaft is safer.

4. **RC receiver** (ELRS): CRSF to a dedicated FC UART. Not strictly required for the bridge test but needed to test mode switching.

5. **Battery**: connect last; disconnect first. Use a smoke-stopper (XT60 inline current-limit plug) on the first power-up.

---

## 4. Step-by-step procedure

1. **Boot CM4** and SSH in. Confirm: `ros2 doctor` returns no errors.

2. **Connect battery** to the ESC power rail (smoke-stopper for first power-up). FC should boot; ESC will chirp its arm tones.

3. **Start the uxrce-dds agent** on the CM4:
   ```sh
   ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 921600
   ```
   You should see `create_participant` / `create_topic` lines scroll by as PX4 declares its topics.

4. **Verify topic visibility** (new terminal):
   ```sh
   ros2 topic list | grep fmu
   ```
   Expect a dozen `/fmu/in/*` and `/fmu/out/*` topics.

5. **Start the VA-6 bridge**:
   ```sh
   ros2 launch va6_mavlink_bridge bench_mavlink.launch.py
   ```
   Log line: `va6_mavlink_bridge ready; waiting for /guidance/attitude_cmd`.

6. **Arm the FC** (via QGroundControl or RC arm switch). At this point the ESC should be armed but motor still idle (throttle at 0).

7. **Switch PX4 to Offboard mode** — either via QGC flight-mode menu or with:
   ```sh
   ros2 service call /fmu/in/vehicle_command px4_msgs/srv/VehicleCommand \
     "{command: 176, param1: 1, param2: 6}"   # SET_MODE → OFFBOARD
   ```

8. **Publish a mode-gated test command** (mode 3 = HIL_ENGAGED → forwards):
   ```sh
   ros2 topic pub -r 50 /guidance/attitude_cmd va6_msgs/AttitudeCmd \
     "{header: {stamp: now}, roll_rate: 0.0, pitch_rate: 0.0, \
       yaw_rate: 0.5, thrust: 0.05, mode: 3}"
   ```
   The motor should spin at low thrust (~5 %).

9. **Measure round-trip latency** (new terminal):
   ```sh
   ros2 topic echo /bridge/latency_us --once
   ```
   Should report a value < 10 000 (10 ms).

10. **Test mode gating** — change `mode` to `1` (MANUAL) in the publisher. Motor must **stop immediately** — this is the safety check. If motor continues, the bridge is broken — halt the test.

11. **Stop** — ctrl-C everything, then disarm, then disconnect battery.

---

## 5. Pass / fail criteria

| Check | Pass |
|---|---|
| Bridge node starts without errors | Log shows "ready; waiting..." |
| PX4 topics visible on CM4 | `ros2 topic list` shows `/fmu/*` |
| Motor responds to `mode=3` commands | Motor spins at commanded rate |
| Motor ignores `mode=1/2/5` commands | Motor immediately idle |
| Round-trip latency | `/bridge/latency_us` reports < 10 000 |
| Forward ratio | Bridge log `fwd/rx` matches expected (1.0 for mode=3, 0.0 for mode=1) |
| Unit test passes | `colcon test --packages-select va6_mavlink_bridge` green |

---

## 6. Common failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| No `/fmu/*` topics appear | uxrce-dds agent not running, wrong serial device, baud mismatch | Check `dmesg | tail` for USB-UART; confirm PX4 `UXRCE_DDS_CFG = TELEM2` + `SER_TEL2_BAUD = 921600` |
| Motor briefly twitches then stops | PX4 dropping out of offboard (heartbeat too slow) | `va6_mavlink_bridge` publishes `OffboardControlMode` at 20 Hz; confirm with `ros2 topic hz /fmu/in/offboard_control_mode` |
| Latency > 10 ms | USB-UART driver overhead, CM4 CPU loaded, ROS DDS reliable QoS | Switch to native CM4 UART (GPIO14/15), set `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`, lock the bridge to CPU core via taskset |
| Motor spins with mode=1 | Bridge mode-gating regressed | Run `colcon test --packages-select va6_mavlink_bridge` — `test_mode_gating.py` should catch it |
| ESC won't arm | PX4 safety switch / CBRK_IO_SAFETY | Set `CBRK_IO_SAFETY = 22027` in QGC param editor |
| QGC refuses offboard switch | RC link not detected, arm refused | Keep ELRS RC connected even for bench; arm via switch |

---

## 7. What's next after pass

- Phase 2 (frame-diff + centroid tracker + PN) — hardware is the same, add one Pi Cam v2 on CSI-1.
- Phase 3 (YOLO on Hailo) — mostly desktop work, then drop the new detector in.
- Phase 4 (4-camera pipeline) — add the Arducam Cammux v2.2 + three more Pi Cams.
