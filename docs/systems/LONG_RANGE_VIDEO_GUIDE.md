# Long Range Video Transmission Guide

**Last Updated:** January 2026
**Purpose:** HD video, telemetry, and control links for MegaDrone
**Focus:** Open source and DIY solutions

---

## Table of Contents

1. [Overview](#overview)
2. [System Comparison](#system-comparison)
3. [OpenHD Build Guide](#openhd-build-guide)
4. [DroneBridge Build Guide](#dronebridge-build-guide)
5. [Hardware Reference](#hardware-reference)
6. [ArduPilot Integration](#ardupilot-integration)
7. [Antenna Guide](#antenna-guide)
8. [Troubleshooting](#troubleshooting)
9. [Resources](#resources)

---

## Overview

### What These Systems Provide

| Function | Description |
|----------|-------------|
| **HD Video** | Low-latency live video from drone to ground |
| **Telemetry** | Flight data (altitude, speed, battery, GPS) |
| **RC Control** | Joystick/radio control uplink (optional) |
| **OSD** | On-screen display overlay |

### Technology: WiFi Broadcast

These open source systems use a clever approach:
- Standard WiFi hardware (2.4GHz or 5.8GHz)
- Custom "broadcast" mode (no association/handshake)
- Forward Error Correction (FEC) for reliability
- Packet injection for transmission
- Works beyond normal WiFi range

### Why Not Commercial?

| System | Range | Cost |
|--------|-------|------|
| DJI Lightbridge | 5km | $1,500+ |
| Herelink V1.1 | 20km | $1,000 |
| SprintLink 5W | 100km | $2,000+ |
| **RunCam WifiLink** | **varies** | **$70-115** |
| **OpenHD (DIY)** | **50km+** | **$200-350** |

### Production-Ready Alternative: RunCam WifiLink

For those who prefer a production-ready solution over DIY, **RunCam WifiLink** (based on OpenIPC) offers:

| Feature | Specification |
|---------|---------------|
| Video | 1080p @ 90fps |
| Sensor | Sony IMX415, 160° FOV |
| Voltage | 9-22V DC |
| TX Power | 630mW (FCC) / 100mW (CE) |
| Weight | 30g (with fan) |
| Price | $70 (VTX only) / $115 (with network card) |

**Ground Station Options:**
- **Mobile:** RTL8812AU adapter ($25) + Android phone + PixelPilot app
- **Dedicated:** RunCam WifiLink-RX ($80) with HDMI output for goggles

**Links:**
- [RunCam Store](https://shop.runcam.com/runcam-wifilink2-based-on-openipc/)
- [OpenIPC Documentation](https://docs.openipc.org/hardware/runcam/vtx/runcam-wifilink-v2/)

**Recommendation:** Use RunCam WifiLink for V1-VID and beyond. The DIY OpenHD approach below is for educational purposes or custom requirements.

---

## System Comparison

### Open Source Options

| System | Range | Latency | Difficulty | Active Dev |
|--------|-------|---------|------------|------------|
| **OpenHD** | 50km+ | 100-150ms | Medium | Yes |
| **WFB-NG** | 20km+ | 30-50ms | Medium | Yes |
| **DroneBridge** | 10km+ | 100-200ms | Easy | Yes |
| **EZ-WifiBroadcast** | 5km+ | 100-200ms | Easy | Limited |

### Recommendation by Use Case

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Beginner/Learning | DroneBridge | Simpler setup |
| General long range | OpenHD | Best features, active community |
| FPV racing/low latency | WFB-NG | Lowest latency |
| Maximum range | OpenHD + high-gain antennas | Proven 50km+ |

---

## OpenHD Build Guide

**Website:** [openhdfpv.org](https://openhdfpv.org/)
**Documentation:** [openhd.gitbook.io](https://openhd.gitbook.io/open-hd/)
**GitHub:** [github.com/OpenHD/OpenHD](https://github.com/OpenHD/OpenHD)

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         AIR UNIT (Drone)                        │
│  ┌──────────┐    ┌──────────────┐    ┌────────────────────┐    │
│  │  Camera  │───►│ Raspberry Pi │───►│ WiFi Adapter       │    │
│  │ (CSI/HDMI)│    │  Zero 2W     │    │ (5.8GHz TX)        │────┼──►
│  └──────────┘    └──────┬───────┘    └────────────────────┘    │
│                         │                                       │
│                  ┌──────┴───────┐                               │
│                  │ Flight       │                               │
│                  │ Controller   │                               │
│                  │ (MAVLink)    │                               │
│                  └──────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ 5.8GHz Broadcast
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GROUND STATION                             │
│  ┌────────────────────┐    ┌──────────────┐    ┌──────────┐    │
│  │ WiFi Adapter(s)    │───►│ Raspberry Pi │───►│ Display  │    │
│  │ (5.8GHz RX)        │    │  4 / 5       │    │ (HDMI)   │    │
│  └────────────────────┘    └──────┬───────┘    └──────────┘    │
│                                   │                             │
│                            ┌──────┴───────┐                     │
│                            │ GCS Software │                     │
│                            │ (QGC/Mission │                     │
│                            │  Planner)    │                     │
│                            └──────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

### Bill of Materials

#### Minimum Build (~$200)

| Component | Model | Qty | Price | Source |
|-----------|-------|-----|-------|--------|
| **Air SBC** | Raspberry Pi Zero 2W | 1 | $15 | [rpilocator.com](https://rpilocator.com) |
| **Ground SBC** | Raspberry Pi 4 (2GB+) | 1 | $35-45 | [rpilocator.com](https://rpilocator.com) |
| **WiFi Adapter** | ASUS USB-AC56 | 2 | $25-40 ea | eBay, Amazon |
| **Camera** | Raspberry Pi Camera V2 | 1 | $30 | Amazon, Adafruit |
| **SD Cards** | 16GB+ Industrial | 2 | $10-15 ea | Amazon |
| **Air BEC** | 5V 3A UBEC | 1 | $8-12 | Amazon, HobbyKing |
| **Ground Power** | 5V 3A USB-C supply | 1 | $10 | Amazon |
| **CSI Cable** | 22-pin (for Pi Zero) | 1 | $5 | Amazon |
| **USB Cables** | USB-A extensions | 2 | $10 | Amazon |
| **Misc** | Heatsinks, thermal tape | 1 | $10 | Amazon |
| | | | **~$200** | |

#### Recommended Build (~$350)

| Component | Model | Qty | Price | Notes |
|-----------|-------|-----|-------|-------|
| **Air SBC** | Raspberry Pi 4 (2GB) | 1 | $35 | Better processing |
| **Ground SBC** | Raspberry Pi 4 (4GB) | 1 | $55 | Smoother video |
| **WiFi Adapter** | ASUS USB-AC56 | 3 | $30 ea | 1 air, 2 ground diversity |
| **Camera** | Pi HQ Camera + lens | 1 | $60 | Better image quality |
| **Antennas** | 5.8GHz panel + omni | 1 set | $30 | Extended range |
| **SD Cards** | 32GB Industrial | 2 | $15 ea | Reliability |
| **BECs** | 5.3V adjustable | 2 | $15 ea | Optimal voltage |
| **Enclosures** | 3D printed or aluminum | 2 | $20 | Protection |
| **Cables/Misc** | Various | 1 | $30 | |
| | | | **~$350** | |

#### Maximum Range Build (~$500)

| Component | Model | Qty | Price | Notes |
|-----------|-------|-----|-------|-------|
| **Air SBC** | Raspberry Pi 4 | 1 | $35 | |
| **Ground SBC** | Raspberry Pi 4 (8GB) | 1 | $75 | Recording capability |
| **WiFi Adapter** | ALFA AWUS036ACH | 4 | $40 ea | Higher power, 2 air + 2 ground |
| **Camera** | Pi HQ + C-mount lens | 1 | $100 | Professional quality |
| **Antennas** | Patch + Yagi | 1 set | $60 | Maximum range |
| **Tracker** | Pan/tilt antenna tracker | 1 | $80 | Auto-tracking |
| **Power** | LiPo + high-quality BEC | 1 | $50 | |
| **Misc** | Enclosures, cables, heatsinks | 1 | $60 | |
| | | | **~$500** | |

### Supported Hardware

#### Single Board Computers (SBCs)

| SBC | Air Unit | Ground | Notes |
|-----|----------|--------|-------|
| **Raspberry Pi Zero 2W** | Good | No | Small, light, limited processing |
| **Raspberry Pi 4** | Best | Best | Recommended for both |
| **Raspberry Pi 5** | Best | Best | Newest, most powerful |
| **Radxa Rock 5** | Experimental | Experimental | High performance alternative |
| **x86 PC** | No | Yes | Laptop/PC as ground station |

#### WiFi Adapters (Chipsets)

| Chipset | Adapters | Band | Power | Recommended |
|---------|----------|------|-------|-------------|
| **RTL8812AU** | ASUS USB-AC56, ALFA AWUS036ACH | 5.8GHz | High | Yes - most popular |
| **RTL8812BU** | Various | 5.8GHz | Medium | Yes |
| **RTL8811AU** | Various | 5.8GHz | Medium | Yes |
| **AR9271** | TP-Link TL-WN722N v1 | 2.4GHz | Low | Budget option |

**Best Choice:** ASUS USB-AC56 (RTL8812AU) - widely available, proven, good range.

#### Cameras

| Camera | Resolution | Interface | Notes |
|--------|------------|-----------|-------|
| **Pi Camera V2** | 1080p | CSI | Good, affordable |
| **Pi HQ Camera** | 12MP | CSI | Best quality, interchangeable lens |
| **USB Webcam** | Varies | USB | Higher latency |
| **HDMI Camera** | Varies | HDMI→CSI | Use action cams, etc. |

### Software Installation

#### Step 1: Download OpenHD Image

```bash
# Download latest release from:
# https://github.com/OpenHD/OpenHD/releases

# For Raspberry Pi:
# openhd-X.X.X-raspberrypi.img.xz
```

#### Step 2: Flash SD Cards

Using Raspberry Pi Imager or balenaEtcher:

```bash
# Linux/Mac with dd:
xz -d openhd-X.X.X-raspberrypi.img.xz
sudo dd if=openhd-X.X.X-raspberrypi.img of=/dev/sdX bs=4M status=progress
sync
```

Flash two cards - one for air unit, one for ground station.

#### Step 3: Configure Air Unit

Edit `openhd-settings-1.txt` on the SD card:

```ini
# Air Unit Configuration
IS_AIR=Y
WIFI_CHANNEL=149          # 5.8GHz channel
WIFI_REGION=US            # Regulatory region
VIDEO_BITRATE=8000        # kbps
VIDEO_WIDTH=1280
VIDEO_HEIGHT=720
VIDEO_FPS=30
```

#### Step 4: Configure Ground Station

Edit `openhd-settings-1.txt`:

```ini
# Ground Station Configuration
IS_AIR=N
WIFI_CHANNEL=149          # Must match air unit
WIFI_REGION=US
ENABLE_RC=N               # Enable if using RC over OpenHD
```

#### Step 5: First Boot

1. Insert SD cards into respective Pis
2. Connect WiFi adapters via USB
3. Connect camera to air unit (CSI cable)
4. Connect display to ground station (HDMI)
5. Power on both units
6. Wait 30-60 seconds for boot
7. Video should appear with OSD overlay

### Wiring Diagram - Air Unit

```
                    ┌─────────────────────────────────────┐
                    │         Raspberry Pi Zero 2W        │
                    │                                     │
   ┌────────┐       │  ┌─────┐                           │
   │ Camera ├───────┼──┤ CSI │                           │
   │ (V2)   │       │  └─────┘                           │
   └────────┘       │                    ┌─────┐         │
                    │                    │ USB │─────────┼────► WiFi Adapter
   ┌────────┐       │  ┌─────┐          └─────┘         │      (ASUS AC56)
   │ FC     ├───────┼──┤UART │                           │
   │(MAVLink)│       │  │TX/RX│                           │
   └────────┘       │  └─────┘                           │
                    │                                     │
   ┌────────┐       │  ┌─────┐                           │
   │ BEC    ├───────┼──┤ 5V  │                           │
   │ 5.3V   │       │  │ GND │                           │
   └────────┘       │  └─────┘                           │
                    └─────────────────────────────────────┘

   From main
   battery via
   BEC (12V→5.3V)
```

### Wiring Diagram - Ground Station

```
                    ┌─────────────────────────────────────┐
                    │           Raspberry Pi 4            │
                    │                                     │
                    │  ┌──────┐         ┌──────┐         │
   WiFi Adapter 1 ──┼──┤ USB  │         │ USB  │─────────┼── WiFi Adapter 2
   (RX Primary)     │  └──────┘         └──────┘         │   (RX Diversity)
                    │                                     │
                    │  ┌──────┐                          │
   Display ─────────┼──┤ HDMI │                          │
   (Monitor/Goggles)│  └──────┘                          │
                    │                                     │
                    │  ┌──────┐                          │
   5V Power ────────┼──┤USB-C │                          │
   (3A supply)      │  └──────┘                          │
                    │                                     │
                    │  ┌──────┐                          │
   Joystick ────────┼──┤ USB  │  (Optional - RC control) │
                    │  └──────┘                          │
                    └─────────────────────────────────────┘
```

### FC Connection (MAVLink Telemetry)

Connect flight controller to air unit Pi:

| FC Pin | Pi Pin | Notes |
|--------|--------|-------|
| TX | GPIO 15 (RXD) | FC transmit → Pi receive |
| RX | GPIO 14 (TXD) | Pi transmit → FC receive |
| GND | GND | Common ground |

**ArduPilot Configuration:**

```
SERIALx_PROTOCOL = 2       # MAVLink2
SERIALx_BAUD = 115200      # Baud rate
```

### OpenHD Settings Reference

| Setting | Default | Range | Description |
|---------|---------|-------|-------------|
| `WIFI_CHANNEL` | 149 | 1-14, 36-165 | WiFi channel |
| `VIDEO_BITRATE` | 4000 | 1000-12000 | Video bitrate (kbps) |
| `VIDEO_WIDTH` | 1280 | 640-1920 | Video width |
| `VIDEO_HEIGHT` | 720 | 480-1080 | Video height |
| `VIDEO_FPS` | 30 | 24-60 | Frames per second |
| `CTS_PROTECTION` | auto | auto/Y/N | RTS/CTS protection |
| `DATARATE` | 6 | 1-12 | MCS rate |

### Channel Selection

| Band | Channels | Notes |
|------|----------|-------|
| **2.4GHz** | 1-14 | Longer range, more interference |
| **5.8GHz** | 36-165 | Shorter range, less interference |

**Recommended 5.8GHz Channels (US):**
- 149, 153, 157, 161, 165 (high power allowed)

---

## DroneBridge Build Guide

**GitHub:** [github.com/DroneBridge/DroneBridge](https://github.com/DroneBridge/DroneBridge)

### Overview

DroneBridge is simpler than OpenHD, good for beginners or shorter range applications.

### Hardware Required

| Component | Air | Ground | Notes |
|-----------|-----|--------|-------|
| Raspberry Pi | Zero W / Zero 2W | Any Pi | |
| WiFi Adapter | 1× RTL8812AU | 1× RTL8812AU | |
| Camera | Pi Camera | - | |
| SD Card | 8GB+ | 8GB+ | |

### Installation

```bash
# Download image from GitHub releases
# Flash to SD cards
# Configure via web interface after first boot
```

### Features

- Android companion app
- Web-based configuration
- ESP32 support for lightweight builds
- Simpler setup than OpenHD

---

## Hardware Reference

### WiFi Adapter Comparison

| Adapter | Chipset | Band | TX Power | Price | Notes |
|---------|---------|------|----------|-------|-------|
| **ASUS USB-AC56** | RTL8812AU | 5.8GHz | High | $30-50 | Most popular |
| **ALFA AWUS036ACH** | RTL8812AU | 2.4/5.8GHz | Very High | $40-60 | Best range |
| **ALFA AWUS036ACS** | RTL8811AU | 5.8GHz | Medium | $30-40 | Compact |
| **TP-Link Archer T2U** | RTL8812AU | 5.8GHz | Medium | $20-30 | Budget |
| **TP-Link TL-WN722N v1** | AR9271 | 2.4GHz | Low | $15 | Budget, 2.4GHz only |

**Note:** Adapter version matters! TP-Link TL-WN722N must be v1 (AR9271), not v2/v3 (different chipset).

### Power Requirements

| Component | Voltage | Current | Notes |
|-----------|---------|---------|-------|
| Pi Zero 2W | 5.0-5.3V | 0.5-1A | Sensitive to voltage |
| Pi 4 | 5.0-5.3V | 1-3A | Needs good power |
| WiFi Adapter | 5.0V | 0.5-1A | From Pi USB or separate |
| Camera | 3.3V | 0.3A | From Pi |

**Important:** Use 5.2-5.3V for best stability. Below 5V causes issues. Above 5.4V damages hardware.

### BEC Recommendations

| BEC | Output | Current | Price | Notes |
|-----|--------|---------|-------|-------|
| Matek UBEC | 5-12V adj | 5A | $10 | Adjustable, reliable |
| Pololu 5V | 5V fixed | 2.5A | $8 | Simple, reliable |
| HobbyKing UBEC | 5V | 3A | $5 | Budget option |

---

## ArduPilot Integration

### Telemetry Setup

OpenHD receives MAVLink telemetry from the flight controller and displays it as OSD.

**Connection:**
```
FC TELEM port ──► Pi UART (GPIO 14/15)
```

**ArduPilot Parameters:**

```
# On spare serial port (e.g., SERIAL2)
SERIAL2_PROTOCOL = 2       # MAVLink2
SERIAL2_BAUD = 115200      # Match OpenHD setting
SR2_POSITION = 2           # Position stream rate
SR2_EXTRA1 = 4             # Attitude stream rate
SR2_EXTRA2 = 4             # VFR HUD stream rate
SR2_EXTRA3 = 2             # Status stream rate
SR2_PARAMS = 10            # Param stream rate
```

### OSD Elements

OpenHD displays:
- Altitude (AGL/MSL)
- Speed (ground/air)
- Battery voltage/current
- GPS status and position
- Flight mode
- Heading
- Home direction/distance
- RSSI/Link quality
- Bitrate
- Latency

### Ground Control Station

OpenHD ground station can forward telemetry to:
- QGroundControl
- Mission Planner
- Any MAVLink-compatible GCS

```
Pi ──► USB ──► Laptop running QGC
```

Or via network:
```
Pi (WiFi/Ethernet) ──► Laptop
```

---

## Antenna Guide

### Antenna Types

| Type | Gain | Beam Width | Best For |
|------|------|------------|----------|
| **Omni (dipole)** | 2-5 dBi | 360° | Short range, all directions |
| **Patch/Panel** | 8-14 dBi | 60-90° | Medium range, directional |
| **Yagi** | 10-18 dBi | 30-60° | Long range, directional |
| **Helical** | 10-14 dBi | 40-60° | Long range, circular polarization |
| **Parabolic** | 20+ dBi | 10-20° | Maximum range, very directional |

### Recommended Configurations

| Range Target | Air Antenna | Ground Antenna |
|--------------|-------------|----------------|
| < 2 km | Omni (stock) | Omni |
| 2-10 km | Omni | Patch (8-10 dBi) |
| 10-30 km | Omni | Patch (12-14 dBi) |
| 30-50 km | 5 dBi omni | Yagi or Helical |
| 50+ km | Directional | Tracking + high gain |

### Polarization

Match polarization between air and ground:
- **Linear (vertical/horizontal):** Simple, common
- **Circular (RHCP/LHCP):** Better for moving aircraft, rejects multipath

### Antenna Tracking

For maximum range, use an antenna tracker:

| Tracker | Type | Price | Notes |
|---------|------|-------|-------|
| DIY Pan/Tilt | Servo-based | $50-100 | ArduPilot antenna tracker firmware |
| Commercial | Motorized | $200-500 | Ready to use |

ArduPilot Antenna Tracker:
- Uses second flight controller
- Tracks aircraft automatically
- Points high-gain antenna at drone

---

## Troubleshooting

### No Video

| Symptom | Cause | Solution |
|---------|-------|----------|
| Black screen | Camera not detected | Check CSI cable, camera enable |
| Black screen | Channel mismatch | Match WIFI_CHANNEL on both |
| Frozen video | Interference | Change channel |
| Artifacts | Low signal | Improve antennas, reduce range |

### Poor Range

| Issue | Solution |
|-------|----------|
| Less than expected | Check antenna connections |
| Drops at distance | Add ground diversity adapter |
| Intermittent | Change channel, check interference |
| One direction worse | Antenna polarization mismatch |

### High Latency

| Cause | Solution |
|-------|----------|
| High bitrate | Reduce VIDEO_BITRATE |
| Processing | Use Pi 4 instead of Zero |
| Interference | Change channel |
| USB issues | Use powered USB hub |

### Boot Issues

| Symptom | Solution |
|---------|----------|
| No boot | Reflash SD card |
| Boot loop | Check power supply (5.2V+) |
| WiFi not starting | Check adapter compatibility |

---

## Resources

### Official Documentation

| Resource | Link |
|----------|------|
| OpenHD Docs | [openhd.gitbook.io](https://openhd.gitbook.io/open-hd/) |
| OpenHD GitHub | [github.com/OpenHD/OpenHD](https://github.com/OpenHD/OpenHD) |
| DroneBridge GitHub | [github.com/DroneBridge/DroneBridge](https://github.com/DroneBridge/DroneBridge) |
| WFB-NG | [github.com/svpcom/wifibroadcast](https://github.com/svpcom/wifibroadcast) |

### Community

| Resource | Link |
|----------|------|
| OpenHD Discord | Via openhdfpv.org |
| OpenHD Forum | Community support |
| RCGroups | Forum discussions |

### YouTube Tutorials

| Channel | Content |
|---------|---------|
| CurryKitten | OpenHD reviews, ExpressLRS |
| MarioFPV | OpenHD, RubyFPV, WFB-NG experiments |
| TreeOrbit | OpenHD, RubyFPV experiments |
| Painless360 | General long-range setup |

### Hardware Sources

| Component | Source |
|-----------|--------|
| Raspberry Pi | [rpilocator.com](https://rpilocator.com) |
| WiFi Adapters | Amazon, eBay, AliExpress |
| Antennas | Amazon, [getfpv.com](https://getfpv.com), AliExpress |
| Cameras | [adafruit.com](https://adafruit.com), Amazon |

### Related Projects

| Project | Description |
|---------|-------------|
| ArduPilot Antenna Tracker | Auto-tracking ground station |
| MAVLink Router | Route telemetry to multiple endpoints |
| QGroundControl | Ground control station software |

---

## MegaDrone Implementation Plan

### By Version

| Version | Video System | Budget | Notes |
|---------|--------------|--------|-------|
| **V0** | Basic FPV (analog/Walksnail) | $100-200 | Learning, short range |
| **V1** | OpenHD Basic | $200 | 10km range |
| **V1-ACAP** | OpenHD + SBC integration | $250 | Integrated with autopilot SBC |
| **V2** | OpenHD Recommended | $350 | 30km range, diversity |
| **V3/V4** | OpenHD Maximum | $500 | 50km+, tracking antenna |

### Integration with V1-ACAP

The V1-ACAP uses an SBC for autopilot. Consider:
- Use same Pi for autopilot AND OpenHD air unit
- Reduces weight and complexity
- Single SBC handles: stabilization interface, navigation, video encoding

---

*Document Version: 1.0*
*Created: January 2026*
*Project: MegaDrone*
