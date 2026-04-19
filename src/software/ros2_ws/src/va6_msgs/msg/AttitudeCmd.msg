# Attitude-rate command from guidance_node -> mavlink_bridge_node.
# Rates are expressed in the body frame in rad/s; thrust is 0-1 normalized.
# The mode field is checked by mavlink_bridge_node; commands are only
# forwarded to the FC when mode is HIL_ENGAGED or FULL_AUTO.

std_msgs/Header header

float32 roll_rate      # rad/s, body frame
float32 pitch_rate     # rad/s, body frame
float32 yaw_rate       # rad/s, body frame
float32 thrust         # 0.0 - 1.0, normalized collective thrust

# Mirror of ModeState.mode so the bridge can gate without a separate sub:
uint8 mode

# Mode values (keep in sync with ModeState.msg):
uint8 MODE_IDLE         = 0
uint8 MODE_MANUAL       = 1
uint8 MODE_HIL_ARMED    = 2
uint8 MODE_HIL_ENGAGED  = 3
uint8 MODE_FULL_AUTO    = 4
uint8 MODE_FAILSAFE     = 5
