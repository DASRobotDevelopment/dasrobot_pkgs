import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition 
from launch.substitutions import LaunchConfiguration, FindExecutable, Command, PathJoinSubstitution

def generate_launch_description():
    
    # Параметры окружения
    description_pkg_name = 'dasrobot_description'
    description_file_name = 'robot.urdf.xacro'
    rviz2_config_file_name = 'description_config.rviz'
    
    # Аргументы запуска
    view_arg_declare = DeclareLaunchArgument(
        'view',
        default_value='true',
        description='Start RViz'
    )

    # Пути к пакетам
    description_pkg_path = get_package_share_directory(description_pkg_name)
    
    # Пути к конфигурационным файлам
    rviz_config_file_path = os.path.join(
        description_pkg_path,
        'config',
        rviz2_config_file_name
    )
    
    # Описание робота
    robot_description = Command([
        FindExecutable(name="xacro"),
        ' ',
        os.path.join(description_pkg_path, 'urdf', description_file_name)
    ])

    # Ноды
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        condition=IfCondition(LaunchConfiguration('view')),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file_path],
        output='screen',
        condition=IfCondition(LaunchConfiguration('view')),
        parameters=[{'robot_description': robot_description}] # ?
    )
    
    # Запуск
    ld = LaunchDescription()

    ld.add_action(view_arg_declare)
    
    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(rviz_node)

    return ld