import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_path = os.path.join(get_package_share_directory('nunbot'))
    ekf_config = os.path.join(pkg_path,'config','ekf.yaml')
    
    return LaunchDescription([
        # Existing robot description node here (adjust as needed)
        # Node(package='nunbot', executable='robot_description', ...),

        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_config],
        ),
    ])
