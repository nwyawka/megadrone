"""Phase 1 bench launch — brings up just the MAVLink bridge.

Used to verify round-trip CM4 -> PX4 -> motor on a test stand (PROPS OFF).
Assumes micro-ros-agent is already running externally on /dev/ttyUSB0.
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='va6_mavlink_bridge',
            executable='bridge_node',
            name='va6_mavlink_bridge',
            output='screen',
            emulate_tty=True,
        ),
    ])
