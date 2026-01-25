# ArduPilot Setup Guide - V0

**Aircraft:** V0 Skills Development Platform
**Firmware:** ArduPilot Plane 4.5+
**Ground Station:** Mission Planner (Windows) or QGroundControl (Mac/Linux)

---

## Table of Contents

1. [Firmware Installation](#firmware-installation)
2. [Initial Configuration](#initial-configuration)
3. [Radio Calibration](#radio-calibration)
4. [Flight Modes](#flight-modes)
5. [Servo Configuration](#servo-configuration)
6. [Failsafe Setup](#failsafe-setup)
7. [Remote ID Setup](#remote-id-setup)
8. [Pre-Flight Verification](#pre-flight-verification)
9. [First Flight Parameters](#first-flight-parameters)
10. [Tuning After First Flight](#tuning-after-first-flight)

---

## Firmware Installation

### Step 1: Connect FC to Computer

1. Connect flight controller via USB
2. Open Mission Planner or QGroundControl
3. Select correct COM port

### Step 2: Install ArduPilot Plane

**Mission Planner:**
1. Go to **Setup → Install Firmware**
2. Click **Plane** (stable version)
3. Wait for installation to complete
4. Disconnect and reconnect

**QGroundControl:**
1. Go to **Vehicle Setup → Firmware**
2. Select **ArduPilot**
3. Choose **Plane Stable**
4. Follow prompts

---

## Initial Configuration

### Step 3: Frame Type

```
FRAME_CLASS = 0        (Undefined - for planes)
```

No frame class needed for conventional fixed-wing.

### Step 4: Accelerometer Calibration

1. **Setup → Mandatory Hardware → Accel Calibration**
2. Click **Calibrate Accel**
3. Follow prompts for 6 positions:
   - Level
   - Nose up
   - Nose down
   - Left side
   - Right side
   - Upside down

### Step 5: Compass Calibration

1. **Setup → Mandatory Hardware → Compass**
2. Click **Start** under Onboard Mag Calibration
3. Rotate aircraft in all directions
4. Wait for completion (green bar)

### Step 6: Radio Calibration

1. **Setup → Mandatory Hardware → Radio Calibration**
2. Turn on transmitter
3. Click **Calibrate Radio**
4. Move all sticks to extremes
5. Click **Click when Done**

---

## Radio Calibration

### Channel Mapping

| Channel | Function | Stick/Switch |
|---------|----------|--------------|
| CH1 | Roll (Aileron) | Right stick left/right |
| CH2 | Pitch (Elevator) | Right stick up/down |
| CH3 | Throttle | Left stick up/down |
| CH4 | Yaw (Rudder) | Left stick left/right |
| CH5 | Flight Mode | 3-position switch |
| CH6 | Arm/Disarm | 2-position switch |

### ELRS Setup

If using ELRS receiver:

```
SERIAL1_PROTOCOL = 23    (RCIN for ELRS on UART1)
SERIAL1_BAUD = 115       (Not used for CRSF)
RSSI_TYPE = 3            (CRSF)
RC_PROTOCOLS = 512       (CRSF only)
```

### PWM Values

Verify these after calibration:

| Stick Position | PWM |
|----------------|-----|
| Min | 1000 |
| Center | 1500 |
| Max | 2000 |

---

## Flight Modes

### Recommended V0 Modes

| Switch Position | Mode | Purpose |
|-----------------|------|---------|
| **Position 1** | MANUAL | Full manual control |
| **Position 2** | FBWA | Stabilized, stick = bank angle |
| **Position 3** | RTL | Return to launch (emergency) |

### Flight Mode Parameters

```
FLTMODE_CH = 5           (Flight mode on CH5)

FLTMODE1 = 0             (MANUAL)
FLTMODE2 = 5             (FBWA)
FLTMODE3 = 11            (RTL)
FLTMODE4 = 11            (RTL)
FLTMODE5 = 11            (RTL)
FLTMODE6 = 11            (RTL)
```

### Mode Descriptions

| Mode | Control | Stabilization | GPS |
|------|---------|---------------|-----|
| **MANUAL** | Direct servo | None | No |
| **FBWA** | Bank/pitch angle | Yes | No |
| **STABILIZE** | Stick = rate | Yes | No |
| **RTL** | Automatic | Full | Required |
| **LOITER** | Circle point | Full | Required |
| **AUTO** | Waypoint | Full | Required |

---

## Servo Configuration

### Servo Output Assignment

```
SERVO1_FUNCTION = 4      (Aileron)
SERVO1_MIN = 1000
SERVO1_MAX = 2000
SERVO1_TRIM = 1500
SERVO1_REVERSED = 0      (Set to 1 if reversed)

SERVO2_FUNCTION = 19     (Elevator)
SERVO2_MIN = 1000
SERVO2_MAX = 2000
SERVO2_TRIM = 1500
SERVO2_REVERSED = 0

SERVO3_FUNCTION = 70     (Throttle)
SERVO3_MIN = 1000
SERVO3_MAX = 2000
SERVO3_TRIM = 1000

SERVO4_FUNCTION = 21     (Rudder)
SERVO4_MIN = 1000
SERVO4_MAX = 2000
SERVO4_TRIM = 1500
SERVO4_REVERSED = 0
```

### Verify Servo Direction

**In MANUAL mode:**

| Input | Expected Response |
|-------|-------------------|
| Roll right stick | Right aileron UP |
| Pull back on pitch | Elevator UP |
| Rudder right | Rudder moves RIGHT |
| Throttle up | Motor speeds up |

If any direction is wrong, set `SERVOx_REVERSED = 1`

---

## Failsafe Setup

### Throttle Failsafe

```
FS_THR_ENABLE = 1        (Enabled)
FS_THR_VALUE = 975       (PWM below this triggers failsafe)
THR_FAILSAFE = 1         (Throttle failsafe enabled)
FS_SHORT_ACTN = 0        (Continue in auto modes)
FS_LONG_ACTN = 1         (RTL on long failsafe)
FS_SHORT_TIMEOUT = 1.5   (Short timeout seconds)
FS_LONG_TIMEOUT = 5      (Long timeout seconds)
```

### GCS Failsafe (Telemetry Loss)

```
FS_GCS_ENABL = 1         (Enabled - RTL if GCS lost)
```

### Battery Failsafe

```
BATT_LOW_VOLT = 10.5     (3S low = 3.5V/cell)
BATT_CRT_VOLT = 9.9      (3S critical = 3.3V/cell)
BATT_FS_LOW_ACT = 1      (RTL on low)
BATT_FS_CRT_ACT = 2      (Land on critical)
```

### Geofence (Optional)

```
FENCE_ENABLE = 1
FENCE_TYPE = 7           (Altitude + Circle + Polygon)
FENCE_ALT_MAX = 120      (Max altitude meters)
FENCE_RADIUS = 300       (Max distance meters)
FENCE_ACTION = 1         (RTL on breach)
```

---

## Remote ID Setup

### For MAVLink-Connected Module (ArduRemoteID, BlueMark)

```
SERIALx_PROTOCOL = 45    (OpenDroneID)
SERIALx_BAUD = 57600
```

Where `x` is your serial port number (e.g., SERIAL2 for TELEM2)

### Wiring

```
FC TX  ──►  Remote ID RX
FC RX  ◄──  Remote ID TX
FC GND ◄─►  Remote ID GND
FC 5V  ──►  Remote ID 5V
```

### Verification

1. Connect to Mission Planner
2. Check **Messages** tab for "OpenDroneID" messages
3. Download OpenDroneID app on phone
4. Verify your drone appears on the app

---

## Pre-Flight Verification

### Arming Setup

```
ARMING_CHECK = 1         (All checks enabled)
ARMING_RUDDER = 0        (Disable rudder arming - use switch)
ARMING_REQUIRE = 1       (Require arm switch)
```

### Arm Switch Setup

```
RC6_OPTION = 153         (Arm/Disarm on CH6)
```

Or use:

```
RC6_OPTION = 41          (Arm/Disarm with AirMode)
```

### Pre-Arm Checks

Mission Planner will show pre-arm failures. Common ones:

| Failure | Solution |
|---------|----------|
| "GPS: No GPS" | Wait for GPS lock |
| "Compass not calibrated" | Run compass calibration |
| "Throttle not at zero" | Lower throttle stick |
| "RC not calibrated" | Run radio calibration |
| "Baro not healthy" | Check for air leaks, restart |

---

## First Flight Parameters

### Conservative Starting Parameters

```
# Throttle
THR_MIN = 0
THR_MAX = 100
TRIM_THROTTLE = 45       (Cruise throttle %)

# Speed
AIRSPEED_MIN = 10        (m/s - stall speed + margin)
AIRSPEED_MAX = 22        (m/s - never exceed)
AIRSPEED_CRUISE = 15     (m/s - cruise target)

# Pitch Limits
LIM_PITCH_MAX = 20       (degrees - climb)
LIM_PITCH_MIN = -15      (degrees - dive)

# Roll Limits
LIM_ROLL_CD = 4500       (45 degrees max bank)

# Navigation
NAVL1_PERIOD = 20        (seconds - lookahead)
WP_RADIUS = 30           (meters)

# RTL
RTL_ALTITUDE = 50        (meters - return altitude)
```

### Disable Features for First Flight

```
TKOFF_THR_MINACC = 0     (Disable auto-takeoff)
LAND_FLARE_SEC = 0       (Disable auto-land)
```

---

## Tuning After First Flight

### Autotune (Recommended)

1. Set flight mode to **AUTOTUNE**
2. Fly level at cruise throttle
3. Engage AUTOTUNE mode
4. Aircraft will make roll/pitch oscillations
5. Fly for 5-10 minutes
6. Land and parameters will be saved

### Manual Tuning

**If aircraft oscillates (too much gain):**
```
RLL_RATE_P = decrease
PTCH_RATE_P = decrease
```

**If aircraft is sluggish (not enough gain):**
```
RLL_RATE_P = increase
PTCH_RATE_P = increase
```

### Typical Starting PID Values (Small Foam)

```
# Roll
RLL_RATE_P = 0.08
RLL_RATE_I = 0.05
RLL_RATE_D = 0.003

# Pitch
PTCH_RATE_P = 0.08
PTCH_RATE_I = 0.05
PTCH_RATE_D = 0.003

# Yaw
YAW_RATE_P = 0.2
YAW_RATE_I = 0.01
YAW_RATE_D = 0
```

---

## Parameter File

Save this as `V0_params.param` for easy loading:

```
# V0 Skills Platform - ArduPilot Parameters
# ArduPilot Plane 4.5+

# Frame
FRAME_CLASS,0

# Flight Modes
FLTMODE_CH,5
FLTMODE1,0
FLTMODE2,5
FLTMODE3,11

# Servo Outputs
SERVO1_FUNCTION,4
SERVO2_FUNCTION,19
SERVO3_FUNCTION,70
SERVO4_FUNCTION,21

# Failsafe
FS_THR_ENABLE,1
FS_THR_VALUE,975
FS_LONG_ACTN,1
BATT_LOW_VOLT,10.5
BATT_FS_LOW_ACT,1

# Arming
ARMING_CHECK,1
ARMING_RUDDER,0

# Limits
LIM_PITCH_MAX,20
LIM_PITCH_MIN,-15
LIM_ROLL_CD,4500

# Speed (no airspeed sensor)
AIRSPEED_USE,0
TRIM_THROTTLE,45

# Navigation
NAVL1_PERIOD,20
RTL_ALTITUDE,50

# Remote ID (if connected)
# SERIAL2_PROTOCOL,45
# SERIAL2_BAUD,57600
```

### Loading Parameters

1. **Mission Planner:** Config → Full Parameter List → Load from file
2. Select `V0_params.param`
3. Click **Write Params**
4. Reboot flight controller

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Won't arm | Pre-arm failure | Check Messages tab |
| Servo jitter | Noise on power | Add capacitor to servo rail |
| GPS won't lock | Interference | Move GPS away from ESC/motor |
| Compass errors | Calibration | Recalibrate away from metal |
| Erratic flight | PID too high | Reduce P gains |
| Won't hold altitude | No airspeed | Enable synthetic airspeed |

---

## Resources

| Resource | Link |
|----------|------|
| ArduPilot Plane Docs | [ardupilot.org/plane](https://ardupilot.org/plane/) |
| First Flight Guide | [ardupilot.org/plane/docs/first-flight-landing-page.html](https://ardupilot.org/plane/docs/first-flight-landing-page.html) |
| Parameter Reference | [ardupilot.org/plane/docs/parameters.html](https://ardupilot.org/plane/docs/parameters.html) |
| Mission Planner | [ardupilot.org/planner/](https://ardupilot.org/planner/) |
| Discord Community | [discord.gg/ardupilot](https://discord.gg/ardupilot) |

---

*See [BUILD_GUIDE.md](BUILD_GUIDE.md) for hardware assembly*
*See [SHOPPING_LIST.md](SHOPPING_LIST.md) for parts*
