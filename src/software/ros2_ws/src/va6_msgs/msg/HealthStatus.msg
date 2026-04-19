# Per-subsystem health rollup, published by health_node at 1 Hz.
# state_machine_node uses this to trigger FAILSAFE transitions.

std_msgs/Header header

uint8 HEALTH_OK        = 0
uint8 HEALTH_WARNING   = 1
uint8 HEALTH_FAULT     = 2

uint8 cameras          # OK if all 4 cameras publishing within last 200 ms
uint8 detector         # OK if detections or heartbeat recent
uint8 fc_link          # OK if PX4 uxrce-dds heartbeat < 500 ms old
uint8 battery          # OK if voltage above threshold, mAh remaining > 20%
uint8 imu              # OK per PX4 SYS_STATUS
uint8 gps              # OK if fix type >= 3 and sats >= 8
uint8 rc_link          # OK if ELRS heartbeat < 1 s old
uint8 thermal          # OK if CM4 temp < 80 C

# Current key metrics for telemetry / logging
float32 battery_volts
float32 battery_mah_remaining
float32 cm4_temp_c
uint8 gps_sats

# Overall rollup (worst of the per-subsystem values above)
uint8 overall
