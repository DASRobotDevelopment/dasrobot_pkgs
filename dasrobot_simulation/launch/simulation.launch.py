import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.conditions import IfCondition 
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, FindExecutable

def generate_launch_description():

    # Параметры окружения
    simulation_pkg_name = 'dasrobot_simulation'
    description_pkg_name = 'dasrobot_description'
    description_file_name = 'robot.urdf.xacro'
    rviz2_config_file_name = 'simulation_config.rviz'

    # Аргументы запуска
    robot_name_arg_declare = DeclareLaunchArgument(
        'robot_name',
        default_value='dasrobot',
        description='Robot name for the nodes.'
    )

    use_rviz_arg_declare = DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Start RViz'
    )

    # Пути к пакетам
    simulation_pkg_path = get_package_share_directory(simulation_pkg_name)
    description_pkg_path = get_package_share_directory(description_pkg_name)
    
    # Пути к конфигурационным файлам
    world_file_path = os.path.join(
        simulation_pkg_path,
        'worlds',
        'simulation_world.sdf'
    )

    gz_bridge_params_path = os.path.join(
        simulation_pkg_path,
        'config',
        'bridge.yaml'
    )

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
    
    # Вызов файлов запуска
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': f'-r -v 4 {world_file_path}',
            'on_exit_shutdown': 'true',
        }.items()
    )
    
    # Ноды
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description, 'use_sim_time': True}
        ],
        output='screen'
    )

    spawn_model_in_gazebo_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-entity', LaunchConfiguration('robot_name'),
            '-string', robot_description,
        ],
        output='screen',
    )

    gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args', '-p',
            f'config_file:={gz_bridge_params_path}'
        ],
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file_path],
        output='screen',
        condition=IfCondition(LaunchConfiguration('rviz')),
    )
    
    # Запуск
    ld = LaunchDescription()

    ld.add_action(robot_name_arg_declare)
    ld.add_action(use_rviz_arg_declare)

    ld.add_action(robot_state_publisher_node)
    ld.add_action(gazebo_launch)
    ld.add_action(spawn_model_in_gazebo_node)
    ld.add_action(gz_bridge_node)
    ld.add_action(rviz_node)
    
    return ld