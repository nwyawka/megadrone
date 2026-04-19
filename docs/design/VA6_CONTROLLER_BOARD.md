# VA-6 Peregrine — Custom Controller Board Architecture

**Date:** March 2026
**Status:** Architecture defined, prototype phase next

## Dual-Processor Architecture

Two processors with different roles — real-time flight control + AI vision/guidance.

### Flight MCU: STM32H743VIT6
- 480MHz Cortex-M7, FPU, hardware DSHOT
- Runs: 1kHz PID loops, motor mixing, sensor fusion, safe/arm logic
- Interfaces: SPI (IMU, baro), I2C (mag), UART (GPS, AI processor), DSHOT (4x ESC)

### AI Processor: Raspberry Pi CM4 (2GB) or Radxa Zero 3W (RK3566)
- Quad-core A55, Linux, CSI camera port
- Runs: YOLO detection, PN guidance, target tracking, decision logic, LoRa comms
- Optional: Hailo-8L M.2 NPU (13 TOPS) for 30fps YOLO

### Communication Between Processors
- UART 115200 baud: AI sends guidance commands (roll, pitch, yaw, thrust)
- STM32 executes commands via PID loops
- Heartbeat: AI processor sends at 50Hz, STM32 detects loss → failsafe

## Component List

| Component | Part | Interface | Cost |
|-----------|------|-----------|------|
| Flight MCU | STM32H743VIT6 | — | $12 |
| AI Processor | RPi CM4 2GB or Radxa Zero 3W | UART to STM32 | $25-35 |
| AI Accelerator | Hailo-8L M.2 (13 TOPS) | M.2 on CM4 | $30 |
| IMU | ICM-42688-P (6-axis) | SPI | $4 |
| Barometer | BMP390 | SPI | $3 |
| Magnetometer | QMC5883L | I2C | $2 |
| GPS | u-blox MAX-M10S | UART | $12 |
| IR Seeker | FLIR Lepton 3.5 (160×120) | SPI + I2C | $200 |
| Visible Camera | OV5647 (CSI) | CSI to CM4 | $8 |
| LoRa Radio | SX1276 (868/915MHz) | SPI to CM4 | $5 |
| Proximity Fuze | CDM324 24GHz | GPIO to STM32 | $5 |
| Power (5V) | TPS5430 | — | $2 |
| Power (3.3V) | AMS1117-3.3 | — | $1 |
| PCB (4-layer, 36×36mm) | JLCPCB | — | $5 |
| **Total** | | | **~$333** |

## PCB: Two-Board Stack (36×36mm each)

**Bottom board:** STM32 + IMU + baro + mag + ESC pads + power regs
**Top board:** CM4 module + Hailo-8L + Lepton + LoRa + GPS
**Connected via:** 20-pin board-to-board connector

## Software Architecture

**AI Processor (Linux):**
- Camera drivers (Lepton SPI, OV5647 CSI)
- AI pipeline: frame differencing → YOLO detect → target track → classification
- Guidance: proportional navigation, intercept calc, terminal maneuver
- Decision logic: target classify, engage/abort, ROE rules
- Comms: LoRa telemetry, waypoint receive, video stream (fiber optic variant)

**Flight MCU (RTOS/bare-metal):**
- Sensor fusion: IMU 1kHz, baro 100Hz, mag 50Hz, GPS 10Hz
- PID controller: rate 1kHz, attitude 500Hz, position 50Hz
- Motor mixer: 4x DSHOT600, differential thrust
- Safe/arm: accel detect, altitude gate, timer, prox fuze arm
- Failsafe: link loss, low battery

## Propulsion (Updated)
- Motors: 4x 2207 2750KV (off-the-shelf FPV race motor)
- Props: 4x 5x4" 2-blade (off-the-shelf, ~$0.63/prop)
- Battery: 6S 5000mAh LiPo
- T/W: 5.1, endurance: 38 min mission profile
