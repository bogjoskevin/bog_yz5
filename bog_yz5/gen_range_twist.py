import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist


class GenRangeTwist(Node):

    def __init__(self):
        super().__init__('gen_range_twist')
        self.range_pub_ = self.create_publisher(Range, 'range', 10)
        self.twist_pub_ = self.create_publisher(Twist, 'twist', 10)

        self.count_ = 0
        
        self.timer_ = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('gen_range_twist node elindult.')

    def timer_callback(self):
        range_msg = Range()
        twist_msg = Twist()


        range_msg.header.stamp = self.get_clock().now().to_msg()
        range_msg.header.frame_id = 'laser'
        range_msg.radiation_type = Range.INFRARED
        range_msg.field_of_view = 3.14
        range_msg.min_range = 0.0
        range_msg.max_range = 25.0

        # Periodikusan valtozo tavolsag (0 es 20 m kozott)
        range_msg.range = float(abs(math.cos(self.count_ / 75.0)) * 20.0)

        # Sebesseg adatok szimulalasa
        twist_msg.linear.x = float((math.sin(self.count_ / 50.0) * 5.0) + 10.0)
        twist_msg.angular.z = float(math.sin(self.count_ / 20.0))

        self.count_ += 1

        self.range_pub_.publish(range_msg)
        self.twist_pub_.publish(twist_msg)


def main(args=None):
    rclpy.init(args=args)
    node = GenRangeTwist()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()