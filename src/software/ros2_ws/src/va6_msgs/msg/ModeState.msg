# Current flight mode, published by state_machine_node.
# Other nodes subscribe to gate their own behavior.

std_msgs/Header header

uint8 mode
uint8 MODE_IDLE         = 0    # disarmed, waiting for command
uint8 MODE_MANUAL       = 1    # ELRS pilot direct; AI advisory only
uint8 MODE_HIL_ARMED    = 2    # AI nominates, guidance computed but suppressed
uint8 MODE_HIL_ENGAGED  = 3    # operator has pressed ENGAGE; AI commands active
uint8 MODE_FULL_AUTO    = 4    # fully autonomous
uint8 MODE_FAILSAFE     = 5    # PX4 failsafe law active

# Entry reason (informational)
string reason

# Time in this state
float32 dwell_s
