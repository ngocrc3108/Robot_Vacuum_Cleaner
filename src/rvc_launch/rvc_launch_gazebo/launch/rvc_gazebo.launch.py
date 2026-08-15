from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    rvc_launch_common_share_dir = FindPackageShare('rvc_launch_common')
    rvc_launch_gazebo_share_dir = FindPackageShare('rvc_launch_gazebo')

    robot_description_file = PathJoinSubstitution([FindPackageShare('rvc_robot_description_gazebo'), 'urdf', 'robot.urdf.xacro'])

    common_launch = IncludeLaunchDescription(
        PathJoinSubstitution([rvc_launch_common_share_dir, 'launch', 'rvc_common.launch.py']),
        launch_arguments={
            'use_sim_time' : 'true',
            'robot_description_file' : robot_description_file,
        }.items(),
    )

    gazebo_node = IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py']),
        launch_arguments={
            'extra_gazebo_args': [
                TextSubstitution(text='--ros-args --params-file '),
                PathJoinSubstitution([rvc_launch_gazebo_share_dir, 'config', 'gazebo_params.yaml']),
            ],
        }.items()
    )

    robot_spawner_node = Node(
        package='gazebo_ros', executable='spawn_entity.py',
        arguments=[
            '-topic', '/robot_description',
            '-entity', 'Robot_Vacuum_Cleaner',
            '-x', '0.0',
            '-y', '0.0',
        ],
        output='screen')

    ld = LaunchDescription()

    ld.add_action(common_launch)
    ld.add_action(gazebo_node)
    ld.add_action(robot_spawner_node)

    return ld
