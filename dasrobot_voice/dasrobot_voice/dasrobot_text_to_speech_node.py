#!/usr/bin/env python3

import rclpy
import pyttsx3

from rclpy.node import Node
from std_msgs.msg import String


class DASRobotTextToSpeechNode(Node):
    def __init__(self):
        super().__init__('dasrobot_text_to_speech_node')

        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 100)
        self.tts.setProperty('volume', 1.0)

        voices = self.tts.getProperty('voices')
        selected = False
        
        for v in voices:
            if 'ru' in v.id.lower() or 'russian' in v.name.lower():
                self.tts.setProperty('voice', v.id)
                selected = True
                break

        if not selected and voices:
            self.tts.setProperty('voice', voices[0].id)
            self.get_logger().info("Russian launage not fround. Installed default launage.")
        
        self.subscription = self.create_subscription(
            String, 
            '/dasrobot/voice/output', 
            self.speak_callback, 
            10
        )

        self.get_logger().info("Starting TTS node.")


    def speak_callback(self, msg):
        self.tts.say(msg.data)
        self.tts.runAndWait()


def main(args=None):
    rclpy.init(args=args)
    node = DASRobotTextToSpeechNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()