"""VA-6 MAVLink bridge node.

Phase 1 spine: translate VA-6 AttitudeCmd messages from guidance_node into
PX4 VehicleRatesSetpoint messages over the uxrce-dds link.

Gates commands based on the AttitudeCmd.mode field — only forwards when
mode is HIL_ENGAGED or FULL_AUTO. In MANUAL or HIL_ARMED the pilot's ELRS
sticks flow through PX4 directly, and AI output is ignored here.

Publishes round-trip latency samples on /bridge/latency_us for bench
verification of the <10 ms goal.
"""

import time

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from std_msgs.msg import UInt32, Header
from va6_msgs.msg import AttitudeCmd

try:
    from px4_msgs.msg import VehicleRatesSetpoint, OffboardControlMode, VehicleCommand
    PX4_MSGS_AVAILABLE = True
except ImportError:
    # Allow bench/dev environments without px4_msgs installed to still import
    # the module. The node will fail to start but unit tests can import it.
    VehicleRatesSetpoint = None
    OffboardControlMode = None
    VehicleCommand = None
    PX4_MSGS_AVAILABLE = False


FORWARD_MODES = frozenset([
    AttitudeCmd.MODE_HIL_ENGAGED,
    AttitudeCmd.MODE_FULL_AUTO,
])


class MavlinkBridgeNode(Node):

    def __init__(self):
        super().__init__('va6_mavlink_bridge')

        if not PX4_MSGS_AVAILABLE:
            self.get_logger().error(
                "px4_msgs not installed. This node must run on a CM4 with "
                "uxrce-dds configured. See src/software/README.md.")
            return

        # PX4 expects reliable-sensor QoS: BEST_EFFORT + KEEP_LAST(1)
        px4_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # Subscribers
        self._att_sub = self.create_subscription(
            AttitudeCmd, '/guidance/attitude_cmd',
            self._on_attitude_cmd, 10)

        # Publishers
        self._rates_pub = self.create_publisher(
            VehicleRatesSetpoint, '/fmu/in/vehicle_rates_setpoint', px4_qos)
        self._offboard_pub = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', px4_qos)
        self._cmd_pub = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', px4_qos)
        self._latency_pub = self.create_publisher(
            UInt32, '/bridge/latency_us', 10)

        # Offboard-control heartbeat — PX4 requires this at >= 2 Hz or it'll
        # drop out of offboard mode.
        self._offboard_timer = self.create_timer(0.05, self._publish_offboard)

        # Stats
        self._cmd_count = 0
        self._forwarded_count = 0
        self._stats_timer = self.create_timer(5.0, self._log_stats)

        self.get_logger().info(
            "va6_mavlink_bridge ready; waiting for /guidance/attitude_cmd")

    def _on_attitude_cmd(self, msg: AttitudeCmd):
        """Forward the AttitudeCmd to PX4, only if mode permits."""
        self._cmd_count += 1
        recv_ns = self.get_clock().now().nanoseconds

        if msg.mode not in FORWARD_MODES:
            # Drop — pilot or state machine has not granted AI authority
            return

        rs = VehicleRatesSetpoint()
        rs.timestamp = int(recv_ns / 1_000)   # microseconds for PX4
        rs.roll = float(msg.roll_rate)
        rs.pitch = float(msg.pitch_rate)
        rs.yaw = float(msg.yaw_rate)
        rs.thrust_body = [0.0, 0.0, -float(msg.thrust)]   # -Z = down in FRD

        self._rates_pub.publish(rs)
        self._forwarded_count += 1

        # Latency measurement: difference between when guidance stamped the
        # command and right now (right before publish).
        sent_ns = (msg.header.stamp.sec * 1_000_000_000
                   + msg.header.stamp.nanosec)
        latency_us = max(0, (recv_ns - sent_ns) // 1_000)
        self._latency_pub.publish(UInt32(data=int(latency_us)))

    def _publish_offboard(self):
        """PX4 offboard-mode heartbeat @ 20 Hz."""
        ocm = OffboardControlMode()
        ocm.timestamp = int(self.get_clock().now().nanoseconds / 1_000)
        ocm.position = False
        ocm.velocity = False
        ocm.acceleration = False
        ocm.attitude = False
        ocm.body_rate = True
        self._offboard_pub.publish(ocm)

    def _log_stats(self):
        self.get_logger().info(
            f"bridge: rx={self._cmd_count}  fwd={self._forwarded_count}  "
            f"ratio={self._forwarded_count/max(1, self._cmd_count):.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = MavlinkBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
