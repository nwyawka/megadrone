# VA-6 Flight Software

ROS 2 Humble-based onboard software for the VA-6 drone. Runs on the CM4 2 GB
alongside a PX4-firmware STM32H743 flight controller.

See the approved plan in `/Users/matthewoneil/.claude/plans/linked-churning-stream.md`
for the complete architecture. This README is the quick-start for bringing
Phase 1 up.

## Status

| Phase | Goal | Status |
|---|---|---|
| 1 | MAVLink bridge spine — CM4 can command motor rates via ROS 2 | scaffold done; bench test pending hardware |
| 2 | Frame-differencing + centroid tracker + classical PN | not started |
| 3 | YOLO-nano on Hailo-8L | not started |
| 4 | 4-camera pipeline via CSI mux | not started |

## Architecture

```
  CM4 (Ubuntu 22.04 + ROS 2 Humble)
    ├── camera_node × N         → /camera/<n>/image_raw
    ├── detector_node × N       → /detections/<n>
    ├── fusion_node             → /target/track
    ├── guidance_node           → /guidance/attitude_cmd
    ├── state_machine_node         (gates commands)
    ├── mavlink_bridge_node     → UART/MAVLink → STM32H7
    ├── health_node, logger_node
    └── ELRS RX ──────────────→ PX4 (CRSF)
             └─ mode switch    → /rc/channel_5  (via uxrce-dds)
```

Mode state machine: `IDLE` → `MANUAL` / `HIL` / `FULL_AUTO` / `FAILSAFE`.

## Phase 1 setup — CM4

1. Flash Ubuntu 22.04 LTS (aarch64) on the CM4 eMMC. Use the Raspberry Pi Imager.
2. Boot; first-boot script installs ROS 2 Humble + dependencies:
   ```sh
   sudo bash src/software/setup/install_ubuntu_22.04.sh
   ```
3. Clone this repo to `~/va6` on the CM4.
4. Build the workspace:
   ```sh
   cd ~/va6/src/software/ros2_ws
   colcon build --symlink-install
   source install/setup.bash
   ```
5. Enable the systemd unit that launches the stack at boot:
   ```sh
   sudo cp src/software/setup/systemd/va6-core.service /etc/systemd/system/
   sudo systemctl enable va6-core.service
   ```

## Phase 1 setup — STM32H743

1. Clone PX4 v1.14 from https://github.com/PX4/PX4-Autopilot.
2. Board target: `make custom_va6_default` (board definition lives under
   `boards/custom/va6/` — add it if not present; mirrors the standard Durandal
   H7 with our UART mapping).
3. Set the following PX4 params:
   ```
   MAV_1_CONFIG = TELEM2     (UART to CM4)
   SER_TEL2_BAUD = 921600
   UXRCE_DDS_CFG = TELEM2
   COM_RC_LOSS_T = 2.0
   COM_LOW_BAT_ACT = 3       (land)
   ```
4. Flash via DFU over USB-C.

## Phase 1 bench test

```sh
# Terminal 1: start micro-ros agent
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 921600

# Terminal 2: start the bridge node
ros2 launch va6_launch bench_mavlink.launch.py

# Terminal 3: command motors (PROPS OFF!)
ros2 topic pub -r 50 /guidance/attitude_cmd va6_msgs/AttitudeCmd \
  "{roll_rate: 0.0, pitch_rate: 0.0, yaw_rate: 0.5, thrust: 0.05, mode: 3}"
```

Exit criterion: motors spin at the commanded yaw rate with < 10 ms round-trip
latency measured via timestamped topics.

## Repo layout

```
src/software/
├── ros2_ws/src/
│   ├── va6_msgs/              custom message definitions
│   ├── va6_mavlink_bridge/    Phase 1 spine — ROS 2 → PX4 MAVLink
│   ├── va6_camera/            (Phase 2) picamera2 → ROS 2 image publisher
│   ├── va6_detection/         (Phase 2/3) frame-diff + YOLO-Hailo
│   ├── va6_fusion/            (Phase 4) multi-camera target fusion
│   ├── va6_guidance/          (Phase 2) proportional navigation
│   ├── va6_state_machine/     mode FSM, command gating
│   ├── va6_health/            watchdog + failsafe trigger
│   └── va6_launch/            launch files (bench, flight, sim)
├── setup/                     install scripts, systemd units
├── docker/                    dev container (CM4 env on x86 for CI)
└── training/                  (Phase 3) YOLO training + .hef compile
```
