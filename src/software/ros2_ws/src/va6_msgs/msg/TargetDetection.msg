# Output of one detector on one camera frame.
# Pixel centroid + bbox in the source camera's image frame.
# Populated by frame_diff_node (Tier 1) or yolo_hailo_node (Tier 2+).

std_msgs/Header header

# Which camera this came from ("fore" / "port" / "starboard" / "down")
string camera_id

# Pixel-frame centroid and axis-aligned bounding box
float32 u              # pixel x of centroid
float32 v              # pixel y of centroid
float32 bbox_w         # bbox width in pixels
float32 bbox_h         # bbox height in pixels

# Image size that u,v,bbox_* are in (lets subscribers re-normalize)
uint32 image_width
uint32 image_height

# Classification (Tier 2+). For Tier 1, class_id = 0 and confidence = 1.0.
uint8 class_id
string class_name
float32 confidence     # 0.0 - 1.0

# Tier 1 class values (single-class detector):
uint8 CLASS_MOTION     = 0

# Tier 2+ class values:
uint8 CLASS_TARGET     = 1
uint8 CLASS_BIRD       = 2
uint8 CLASS_AIRCRAFT   = 3
uint8 CLASS_DECOY      = 4
uint8 CLASS_HELICOPTER = 5
