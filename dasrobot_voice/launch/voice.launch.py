import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Ноды
    tts_node = Node(
        package='dasrobot_voice',
        executable='dasrobot_tts',
        name='dasrobot_tts_node',
        output='screen'
    )

    stt_node = Node(
        package='dasrobot_voice',
        executable='dasrobot_stt',
        name='dasrobot_stt_node',
        output='screen'
    )
    
    # Запуск
    ld = LaunchDescription()

    ld.add_action(tts_node)
    ld.add_action(stt_node)    

    return ld