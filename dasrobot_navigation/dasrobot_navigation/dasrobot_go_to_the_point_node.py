#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Point, PoseStamped
from nav2_smile_commander.robot_navigator import BasicNavigator

class DASRobotGoToThePointNode(Node):
    def __init__(self):
        super().__init__('dasrobot_go_to_the_point_node')

        self.navigator = BasicNavigator()
        self.navigator.waitUntilNav2Active()
        self.busy = False

        self.subscription = self.create_subscription(
            Point,
            'dasrobot/navigation/target_point',
            self.point_callback,
            10
        )

        self.get_logger().info("Starting go to the point node.")

    def point_callback(self. msg: Point):

        if self.busy:
            self.get_logger().warn('Navigator is busy, ignoring new goal')
            return


