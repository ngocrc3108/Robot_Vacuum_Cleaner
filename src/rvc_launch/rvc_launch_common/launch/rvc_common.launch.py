from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')

    robot_description_file = LaunchConfiguration('robot_description_file')

    rvc_launch_common_share_dir = FindPackageShare('rvc_launch_common')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true',
    )

    declare_rviz_config_file_cmd = DeclareLaunchArgument(
        name='rviz_config_file',
        default_value=PathJoinSubstitution([rvc_launch_common_share_dir, 'rviz', 'view.rviz']),
        description='Absolute path to rviz config file')

    declare_robot_description_file_cmd = DeclareLaunchArgument(
        'robot_description_file',
        description="Path to robot description file",
    )

    # Process xacro -> URDF
    robot_description = Command([
        'xacro',
        ' ',
        robot_description_file,
    ])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'use_sim_time' : use_sim_time,
                'robot_description': robot_description,
            }
        ]
    )

    # Rviz
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[
            {
                'use_sim_time' : use_sim_time,
            }
        ],
        arguments=['-d', LaunchConfiguration('rviz_config_file')],
    )

    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_rviz_config_file_cmd)
    ld.add_action(declare_robot_description_file_cmd)

    ld.add_action(robot_state_publisher_node)
    ld.add_action(rviz_node)

    return ld
