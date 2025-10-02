import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    default_map_path = os.path.join(
        get_package_share_directory('nunbot'),
        'maps',
        'museum_nav2.yaml'
    )
    map_file = LaunchConfiguration('map')

    default_param_path = os.path.join(
        get_package_share_directory('nunbot'),
        'config',
        'nav2_params.yaml'
    )
    param_file = LaunchConfiguration('params_file')

    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=default_map_path,
            description='Full path to map file to load'),

        DeclareLaunchArgument(
            'params_file',
            default_value=default_param_path,
            description='Full path to param file to load'),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/bringup_launch.py']),
            launch_arguments={
                'map': map_file,
                'use_sim_time': use_sim_time,
                'params_file': param_file}.items(),
        ),
    ])