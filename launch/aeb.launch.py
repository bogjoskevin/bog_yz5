from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='bog_yz5',
            executable='gen_range_twist',
            name='gen_range_twist',
            output='screen'
        ),
        Node(
            package='bog_yz5',
            executable='control_node',
            name='control_node',
            output='screen'
        ),
    ])