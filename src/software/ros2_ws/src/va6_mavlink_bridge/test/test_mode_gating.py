"""Unit test: verify that the bridge only forwards commands in the
correct modes (HIL_ENGAGED, FULL_AUTO) and drops commands in all others."""

from va6_msgs.msg import AttitudeCmd

try:
    from va6_mavlink_bridge.bridge_node import FORWARD_MODES
    IMPORT_OK = True
except ImportError:
    FORWARD_MODES = None
    IMPORT_OK = False


def test_forward_modes_cover_exactly_engaged_and_auto():
    assert IMPORT_OK, "va6_mavlink_bridge module must import"
    expected = {
        AttitudeCmd.MODE_HIL_ENGAGED,
        AttitudeCmd.MODE_FULL_AUTO,
    }
    assert FORWARD_MODES == expected


def test_non_forward_modes():
    """These modes must NOT be in FORWARD_MODES — AI authority is suppressed."""
    assert IMPORT_OK
    for mode in (
        AttitudeCmd.MODE_IDLE,
        AttitudeCmd.MODE_MANUAL,
        AttitudeCmd.MODE_HIL_ARMED,
        AttitudeCmd.MODE_FAILSAFE,
    ):
        assert mode not in FORWARD_MODES, (
            f"mode {mode} must NOT be forwarded — safety critical")
