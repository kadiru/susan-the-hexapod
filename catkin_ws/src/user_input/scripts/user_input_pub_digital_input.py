#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy
from user_input.msg import UserInput

pub = None

def callback(data):
  global pub
  command = UserInput()
  left_right = data.axes[6]
  up_down = data.axes[7]
  retract_button = data.buttons[0]
  slow_button = data.buttons[1]
  if retract_button:
    command.dir = "lower"
    command.speed = 0
  elif abs(left_right) > 0 or abs(up_down) > 0:
    if slow_button:
      command.speed = 0.5
    else:
      command.speed = 1.0
    if abs(left_right) > abs(up_down):
      if left_right < 0:
        command.dir = "right"
      else:
        command.dir = "left" 
    else:
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
