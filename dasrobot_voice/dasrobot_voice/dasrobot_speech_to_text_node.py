#!/usr/bin/env python3

import rclpy
import speech_recognition

from rclpy.node import Node
from std_msgs.msg import String


class DASRobotSpeechToTextNode(Node):
    def __init__(self):
        super().__init__('dasrobot_speech_to_text_node')

        self.recognizer = speech_recognition.Recognizer()

        self.publisher_ = self.create_publisher(
            String, 
            '/dasrobot/voice/input', 
            10
        )

        self.get_logger().info("Starting STT node.")

        self.microphone = speech_recognition.Microphone()
        self.stop_listener = self.recognizer.listen_in_background(
            self.microphone,
            self.recognition_callback,
            #phrase_threshold = 0.3
        )


    def recognition_callback(self, recognizer, audio):
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            # self.get_logger().info(f"Recognized: '{text}'")

            msg = String()
            msg.data = text
            self.publisher_.publish(msg)

        except speech_recognition.UnknownValueError:
            self.get_logger().debug("Speech unintelligible.")
        except speech_recognition.RequestError as e:
            self.get_logger().error(f"Google API error: {e}")
        except Exception as e:
            self.get_logger().error(f"Unexpected error in recognition: {e}")



def main(args=None):
    rclpy.init(args=args)
    node = DASRobotSpeechToTextNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if hasattr(node, 'stop_listener'):
            node.stop_listener(wait_for_stop=True)
        node.destroy_node()
        rclpy.shutdown()
        

if __name__ == '__main__':
    main()