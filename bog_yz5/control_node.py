import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist


class ControlNode(Node):

    def __init__(self):
        super().__init__('control_node')

        self.sub_range_ = self.create_subscription(Range, 'range', self.range_callback, 10)
        self.sub_twist_ = self.create_subscription(Twist, 'twist', self.twist_callback, 10)
        self.pub_cmd_ = self.create_publisher(Twist, 'cmd_vel', 10)

        self.timer_ = self.create_timer(1.0, self.timer_callback)

        self.range_val_ = 20.0
        self.speed_val_ = 0.0
        self.angular_val_ = 0.0

        self.get_logger().info('control_node elindult és figyeli a szenzoradatokat.')

    def range_callback(self, msg):
        self.range_val_ = msg.range

    def twist_callback(self, msg):
        self.speed_val_ = msg.linear.x
        self.angular_val_ = msg.angular.z

    def timer_callback(self):
        cmd = Twist()

        # 1. Veszfek (< 5m)
        if self.range_val_ < 5.0:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.pub_cmd_.publish(cmd)
            self.get_logger().error(
                f'CRITICAL: Obstacle detected (Range: {self.range_val_:.2f} m < 5.0 m), EMERGENCY BRAKE active!'
            )

        # 2. Lassitas (5m - 10m)
        elif 5.0 <= self.range_val_ < 10.0:
            cmd.linear.x = float(self.speed_val_ * 0.4)
            cmd.angular.z = self.angular_val_
            self.pub_cmd_.publish(cmd)
            self.get_logger().warn(
                f'WARNING: Obstacle approaching (Range: {self.range_val_:.2f} m), decelerating to {cmd.linear.x:.2f} m/s.'
            )

        # 3. Normal haladas (>= 10m)
        else:
            cmd.linear.x = self.speed_val_
            cmd.angular.z = self.angular_val_
            self.pub_cmd_.publish(cmd)
            self.get_logger().info(
                f'NORMAL: Path clear (Range: {self.range_val_:.2f} m), moving robot with speed {self.speed_val_:.2f} m/s.'
            )


def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()