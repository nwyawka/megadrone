#!/usr/bin/env bash
#
# First-boot provisioning for a VA-6 CM4 running Ubuntu 22.04 LTS (aarch64).
# Installs ROS 2 Humble, PX4 dependencies, Hailo runtime, and the misc tooling
# the flight stack needs.
#
# Usage: sudo bash src/software/setup/install_ubuntu_22.04.sh
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Must run as root (use sudo)." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Base dependencies
# ---------------------------------------------------------------------------
apt update
apt install -y --no-install-recommends \
  curl gnupg lsb-release locales software-properties-common \
  build-essential cmake git python3-pip python3-venv \
  libssl-dev libffi-dev pkg-config

locale-gen en_US en_US.UTF-8
update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# ---------------------------------------------------------------------------
# ROS 2 Humble repository
# ---------------------------------------------------------------------------
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
  > /etc/apt/sources.list.d/ros2.list
apt update
apt install -y \
  ros-humble-ros-base \
  ros-humble-launch-xml ros-humble-launch-yaml \
  ros-humble-rclpy ros-humble-rclcpp \
  ros-humble-sensor-msgs ros-humble-geometry-msgs \
  ros-humble-vision-msgs ros-humble-image-transport \
  python3-colcon-common-extensions python3-rosdep python3-vcstool

rosdep init || true
sudo -u ubuntu rosdep update || true

# ---------------------------------------------------------------------------
# uxrce-dds agent + micro-ROS (for PX4 <-> ROS 2 over UART)
# ---------------------------------------------------------------------------
apt install -y ros-humble-micro-ros-agent-msgs || true
# The canonical build route is from source; the binary agent pkg may not be
# available on all mirrors. Fallback:
if ! command -v micro-ros-agent > /dev/null; then
  pip3 install micro-ros-agent || true
fi

# ---------------------------------------------------------------------------
# Camera / vision deps
# ---------------------------------------------------------------------------
apt install -y \
  libcamera-tools libcamera-dev \
  python3-libcamera python3-picamera2 \
  python3-opencv \
  v4l-utils

# ---------------------------------------------------------------------------
# Hailo runtime (must be downloaded manually from developer.hailo.ai;
# mirror the .deb in /opt/va6_vendor/ before running this script)
# ---------------------------------------------------------------------------
if [[ -f /opt/va6_vendor/hailort.deb ]]; then
  dpkg -i /opt/va6_vendor/hailort.deb || apt -f install -y
else
  echo "NOTE: Hailo runtime .deb not found at /opt/va6_vendor/hailort.deb"
  echo "Download from https://developer.hailo.ai and re-run, or install later."
fi

# ---------------------------------------------------------------------------
# Add 'ubuntu' user to groups needed for hardware access
# ---------------------------------------------------------------------------
usermod -aG dialout,video,i2c,gpio ubuntu || true

# ---------------------------------------------------------------------------
# PX4 build toolchain (for rebuilding firmware on the drone — rarely needed,
# but useful during development)
# ---------------------------------------------------------------------------
apt install -y \
  gcc-arm-none-eabi binutils-arm-none-eabi libnewlib-arm-none-eabi \
  gdb-multiarch

# ---------------------------------------------------------------------------
# Environment bootstrap for login shells
# ---------------------------------------------------------------------------
if ! grep -q "/opt/ros/humble/setup.bash" /home/ubuntu/.bashrc 2>/dev/null; then
  cat >> /home/ubuntu/.bashrc <<'EOF'

# ROS 2 Humble
source /opt/ros/humble/setup.bash
if [[ -f $HOME/va6/src/software/ros2_ws/install/setup.bash ]]; then
  source $HOME/va6/src/software/ros2_ws/install/setup.bash
fi
EOF
fi

echo ""
echo "===== Install complete ====="
echo "Next steps:"
echo "  1. Reboot."
echo "  2. cd ~/va6/src/software/ros2_ws && colcon build --symlink-install"
echo "  3. sudo cp src/software/setup/systemd/va6-core.service /etc/systemd/system/"
echo "     sudo systemctl enable va6-core.service"
