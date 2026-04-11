import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.conditions import IfCondition 
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    # Параметры окружения
    navigation_pkg_name = 'dasrobot_navigation'
    rviz2_config_file_name = 'navigation_config.rviz'

    # Аргументы запуска
    use_simulation_arg_declare = DeclareLaunchArgument(
        'simulation',
        default_value='false',
        description='Use simulation at launch.'
    )

    use_sim_time_arg_declare = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time at launch.'
    )

    cmd_topic_name_declare = DeclareLaunchArgument(
        'cmd_topic', 
        default_value='/cmd_vel'
    )

    use_rviz_arg_declare = DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Start RViz'
    )

    # Пути к пакетам
    navigation_pkg_path = get_package_share_directory(navigation_pkg_name)

    # Пути к конфигурационным файлам
    slam_params_path = os.path.join(
        navigation_pkg_path, 
        'config', 
        'mapper_params_online_async.yaml'
    )

    twist_mux_params_path = os.path.join(
        navigation_pkg_path, 
        'config', 
        'twist_mux_params.yaml'
    )

    nav2_params_path = os.path.join(
        navigation_pkg_path, 
        'config', 
        'nav2_params.yaml'
    )

    rviz_config_file_path = os.path.join(
        navigation_pkg_path,
        'config',
        rviz2_config_file_name
    )

    # Вызов файлов запуска
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('slam_toolbox'), 
                'launch', 
                'online_async_launch.py'
            )
        ]),
        launch_arguments={
            'params_file': slam_params_path,
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }.items()
    )

    # Ноды
    twist_mux_node = Node(
        package='twist_mux',
        executable='twist_mux',
        name='twist_mux',
        output='screen',
        parameters=[twist_mux_params_path,
                    {'use_stamped': LaunchConfiguration('use_sim_time')}],
        remappings=[('/cmd_vel_out', LaunchConfiguration('cmd_topic'))]
    )

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[nav2_params_path]
    )

    controller_server_node = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_params_path],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static'),
            ('cmd_vel', '/cmd_vel_nav')
        ]
    )

    planner_server_node = Node(
        package='nav2_planner', 
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_params_path]
    )

    behavior_server_node = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[nav2_params_path]
    )

    bt_navigator_node = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_params_path]
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'autostart': True,
            'node_names': [
                'map_server',
                'controller_server', 
                'planner_server',
                "behavior_server",
                'bt_navigator'
            ]
        }]
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
    
    ld.add_action(use_simulation_arg_declare)
    ld.add_action(use_sim_time_arg_declare)
    ld.add_action(cmd_topic_name_declare)
    ld.add_action(use_rviz_arg_declare)

    ld.add_action(slam_launch)
    ld.add_action(twist_mux_node)
    ld.add_action(map_server_node)
    ld.add_action(controller_server_node)
    ld.add_action(planner_server_node)
    ld.add_action(behavior_server_node)
    ld.add_action(bt_navigator_node)
    ld.add_action(lifecycle_manager_node)
    ld.add_action(rviz_node)

    return ld