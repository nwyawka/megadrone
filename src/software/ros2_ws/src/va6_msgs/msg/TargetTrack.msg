# Fused target track from fusion_node. Single track regardless of how many
# cameras contributed. Expressed in the drone body frame — azimuth (+ToPort),
# elevation (+Up), optional range (meters) if monocular range estimate exists.

std_msgs/Header header

# Which cameras are currently contributing to this track
string[] contributing_cameras

# Target state in body frame:
float32 azimuth_rad        # + toward port (left)
float32 elevation_rad      # + up
float32 range_m            # estimated range in m; -1 if unknown
float32 azimuth_rate       # rad/s, low-passed line-of-sight rate
float32 elevation_rate     # rad/s

# Classification — the most confident class across contributing detectors
uint8 class_id
string class_name
float32 confidence         # 0.0 - 1.0

# Track health
float32 track_age_s        # how long this track has existed
bool locked                # has stayed above confidence threshold long enough
