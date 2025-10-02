#!/bin/bash

# Change to ROS workspace directory
cd ~/nunbot_ros_ws

# Source ROS 2 workspace setup file
source ./install/setup.bash

# Run ROS 2 launch file (replace with your launch command)
ros2 launch nunbot full_system_launch.py use_sim_time:=false > /dev/null 2>&1 &

echo "Starting script."

echo "Waiting 20 seconds before next task"
sleep 20

echo "Starting Nav"
# Change to ROS workspace directory
cd ~/nunbot_ros_ws

# Source ROS 2 workspace setup file
source ./install/setup.bash

echo "Starting Nav script."

# Launch second ROS 2 launch file
ros2 run nunbot_navigation simplified_navigator

