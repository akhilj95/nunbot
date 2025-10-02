import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource, AnyLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import TimerAction


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # Use one of the following map names in the following path definition
    # 'museum_nav2.yaml'
    # 'nav2_map_labtech.yaml'
    map_file = LaunchConfiguration('map')

    # Paths to your existing nunbot launch files
    nunbot_pkg_share = get_package_share_directory('nunbot')
    urdf_launch_path = os.path.join(nunbot_pkg_share, 'launch', 'rsp.launch.py')  # Launch file for robot state publisher
    nav2_launch_path = os.path.join(nunbot_pkg_share, 'launch', 'nav2.launch.py')  # Launch Nav2 using Launch script

    # External launch files from other packages
    sllidar_launch_path = os.path.join(get_package_share_directory('sllidar_ros2'), 'launch', 'sllidar_a1_launch.py')
    sdpo_localization_launch_path = os.path.join(get_package_share_directory('sdpo_localization_odom'), 'launch', 'sdpo_localization_odom_wh.launch.xml')

    ld = LaunchDescription()

    # Declare use_sim_time argument
    ld.add_action(
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        )
    )

    # Declare map argument
    ld.add_action(
        DeclareLaunchArgument(
            'map',
            #default_value=os.path.join(nunbot_pkg_share, 'maps', 'museum_nav2.yaml'),
            default_value=os.path.join(nunbot_pkg_share, 'maps', 'nav2_map_labtech.yaml'),
            description='Full path to map file'
        )
    )

    # Include your nunbot URDF launch file
    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(urdf_launch_path),
            launch_arguments={'use_sim_time': use_sim_time}.items()
        )
    )

    # Include your nunbot Nav2 launch file
    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch_path),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'map': map_file
            }.items()
        )
    )

    # Include sllidar launch file (Python launch)
    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sllidar_launch_path),
            launch_arguments={'use_sim_time': use_sim_time}.items()
        )
    )

    # Include sdpo_localization launch file (XML launch)
    ld.add_action(
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(sdpo_localization_launch_path),
            launch_arguments={'use_sim_time': use_sim_time}.items()
        )
    )

    # Launch nunbot_base_node (node for communicating with robot base)
    ld.add_action(
        Node(
            package='nunbot_base',
            executable='nunbot_base_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
        )
    )
    return ld