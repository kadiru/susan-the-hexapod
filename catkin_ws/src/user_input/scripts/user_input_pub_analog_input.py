#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy
from user_input.msg import UserInput

pub = None
deadzone = 0.05

def callback(data):
  global pub
  command = UserInput()
  left_right = data.axes[0]
  up_down = data.axes[1]
  if abs(left_right) > deadzone or abs(up_down) > deadzone:
    if abs(left_right) > abs(up_down):
      command.speed = abs(left_right)
      if left_right < 0:
        command.dir = "right"
      else:
        command.dir = "left" 
    else:
      command.speed = abs(up_down)
      if up_down < 0:
        command.dir = "backwards"
      else:
        command.dir = "forward"
  else:
    command.dir = "stop"
    command.speed = 0
  pub.publish(command)

def start():
  global pub
  rospy.init_node('user_input_publisher', anonymous=True)
  pub = rospy.Publisher('user_input_pub', UserInput, queue_size=1)
  rospy.Subscriber("joy", Joy, callback)
  rospy.spin()

if __name__ == '__main__':
  start()
