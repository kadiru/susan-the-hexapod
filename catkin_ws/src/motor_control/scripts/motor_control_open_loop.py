#!/usr/bin/env python3
import rospy
import serial
import time
from user_input.msg import UserInput

serl12 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313930351C05231-if00', 115200, timeout=1);
serl34 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00', 115200, timeout=1);
serl56 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313637351115182-if00', 115200, timeout=1);

lin_act_time = 2000
stepper_time = 3000
small_stepper_time = 2500

grounded = [True, True]
active_group = 0 # 0 is odd legs, 1 is even

# serial command codes
# linear actuator codes
# e = extend, r = retract
e1 = "q\n"
r1 = "w\n"
e2 = "e\n"
r2 = "r\n"
# rotation codes
# f = forwards, b = backwards, n = neutral
f1 = "t\n"
b1 = "y\n"
f2 = "u\n"
b2 = "i\n"
n1 = "o\n"
n2 = "p\n"
# s = slow
sf1 = "a\n"
sb1 = "s\n"
sf2 = "d\n"
sb2 = "f\n"
none = "na\n"

"""
Leg ordering
1H6
2H5
3H4
"""

# function to send the specified string to each serial device
# and wait wait_time ms
def sendAndWait(str12, str34, str56, wait_time):
  serl12.write(str.encode(str12))
  serl34.write(str.encode(str34))
  serl56.write(str.encode(str56))
  start_time = time.time()*1000
  curr_time = time.time()*1000
  while curr_time - start_time < wait_time:
    curr_time = time.time()*1000

  return True


def callback(data):
  global active_group
  global grounded
  direction = data.dir
  speed = data.speed
  rospy.loginfo(direction)
  if direction == "forward":
    if active_group == 0:
      if grounded[active_group]:
        # raise 1
        sendAndWait(e1, none, none, lin_act_time)
        # raise 3
        sendAndWait(none, e1, none, lin_act_time)
        # raise 5
        sendAndWait(none, none, e1, lin_act_time)
        #sendAndWait(e1, e1, e1, lin_act_time)
        grounded[active_group] = False
      # rotate 1,3,5 forward
      if speed > 0.5:
        sendAndWait(f1, f1, f1, stepper_time)
      else:
        sendAndWait(sf1, sf1, sf1, small_stepper_time)
      # lower 1
      sendAndWait(r1, none, none, lin_act_time)
      # lower 3
      sendAndWait(none, r1, none, lin_act_time)
      # lower 5
      sendAndWait(none, none, r1, lin_act_time)
      #sendAndWait(r1, r1, r1, lin_act_time)
      grounded[active_group] = True
      # raise 2
      sendAndWait(e2, none, none, lin_act_time)
      # raise 4
      sendAndWait(none, e2, none, lin_act_time)
      # raise 6
      sendAndWait(none, none, e2, lin_act_time)
      #sendAndWait(e2, e2, e2, lin_act_time)
      grounded[1] = False
      # rotate 1,3,5 neutral
      sendAndWait(n1, n1, n1, stepper_time)
      # lower 2
      sendAndWait(r2, none, none, lin_act_time)
      # lower 4
      sendAndWait(none, r2, none, lin_act_time)
      # lower 6
      sendAndWait(none, none, r2, lin_act_time)
      #sendAndWait(r2, r2, r2, lin_act_time)
      grounded[1] = True
      active_group = 1
    else:
      # active group is 1
      if grounded[active_group]:
        # raise 2
        sendAndWait(e2, none, none, lin_act_time)
        # raise 4
        sendAndWait(none, e2, none, lin_act_time)
        # raise 6
        sendAndWait(none, none, e2, lin_act_time)
        #sendAndWait(e2, e2, e2, lin_act_time)
        grounded[active_group] = False
      # rotate 2,4,6 forward
      if speed > 0.5:
        sendAndWait(f2, f2, f2, stepper_time)
      else:
        sendAndWait(sf2, sf2, sf2, small_stepper_time)
      # lower 2
      sendAndWait(r2, none, none, lin_act_time)
      # lower 4
      sendAndWait(none, r2, none, lin_act_time)
      # lower 6
      sendAndWait(none, none, r2, lin_act_time)
      #sendAndWait(r2, r2, r2, lin_act_time)
      grounded[active_group] = True
      # raise 1
      sendAndWait(e1, none, none, lin_act_time)
      # raise 3
      sendAndWait(none, e1, none, lin_act_time)
      # raise 5
      sendAndWait(none, none, e1, lin_act_time)
      #sendAndWait(e1, e1, e1, lin_act_time)
      grounded[0] = False
      # rotate 2,4,6 neutral
      sendAndWait(n2, n2, n2, stepper_time)
      # lower 1
      sendAndWait(r1, none, none, lin_act_time)
      # lower 3
      sendAndWait(none, r1, none, lin_act_time)
      # lower 5
      sendAndWait(none, none, r1, lin_act_time)
      #sendAndWait(r1, r1, r1, lin_act_time)
      grounded[0] = True
      active_group = 0
  elif direction == "backwards":
    if active_group == 0:
      if grounded[active_group]:
        # raise 1
        sendAndWait(e1, none, none, lin_act_time)
        # raise 3
        sendAndWait(none, e1, none, lin_act_time)
        # raise 5
        sendAndWait(none, none, e1, lin_act_time)
        #sendAndWait(e1, e1, e1, lin_act_time)
        grounded[active_group] = False
      # rotate 1,3,5 backwards
      if speed > 0.5:
        sendAndWait(b1, b1, b1, stepper_time)
      else:
        sendAndWait(sb1, sb1, sb1, small_stepper_time)
      # lower 1
      sendAndWait(r1, none, none, lin_act_time)
      # lower 3
      sendAndWait(none, r1, none, lin_act_time)
      # lower 5
      sendAndWait(none, none, r1, lin_act_time)
      #sendAndWait(r1, r1, r1, lin_act_time)
      grounded[active_group] = True
      # raise 2
      sendAndWait(e2, none, none, lin_act_time)
      # raise 4
      sendAndWait(none, e2, none, lin_act_time)
      # raise 6
      sendAndWait(none, none, e2, lin_act_time)
      #sendAndWait(e2, e2, e2, lin_act_time)
      grounded[1] = False
      # rotate 1,3,5 neutral
      sendAndWait(n1, n1, n1, stepper_time)
      # lower 2
      sendAndWait(r2, none, none, lin_act_time)
      # lower 4
      sendAndWait(none, r2, none, lin_act_time)
      # lower 6
      sendAndWait(none, none, r2, lin_act_time)
      #sendAndWait(r2, r2, r2, lin_act_time )
      grounded[1] = True
      active_group = 1
    else:
      # active group is 1
      if grounded[active_group]:
        # raise 2
        sendAndWait(e2, none, none, lin_act_time)
        # raise 4
        sendAndWait(none, e2, none, lin_act_time)
        # raise 6
        sendAndWait(none, none, e2, lin_act_time)
        #sendAndWait(e2, e2, e2, lin_act_time)
        grounded[active_group] = False
      # rotate 2,4,6 backwards
      if speed > 0.5:
        sendAndWait(b2, b2, b2, stepper_time)
      else:
        sendAndWait(sb2, sb2, sb2, small_stepper_time)
      # lower 2
      sendAndWait(r2, none, none, lin_act_time)
      # lower 4
      sendAndWait(none, r2, none, lin_act_time)
      # lower 6
      sendAndWait(none, none, r2, lin_act_time)
      #sendAndWait(r2, r2, r2, lin_act_time )
      grounded[active_group] = True
      # raise 1
      sendAndWait(e1, none, none, lin_act_time)
      # raise 3
      sendAndWait(none, e1, none, lin_act_time)
      # raise 5
      sendAndWait(none, none, e1, lin_act_time)
      #sendAndWait(e1, e1, e1, lin_act_time)
      grounded[0] = False
      # rotate 2,4,6 neutral
      sendAndWait(n2, n2, n2, stepper_time)
      # lower 1
      sendAndWait(r1, none, none, lin_act_time)
      # lower 3
      sendAndWait(none, r1, none, lin_act_time)
      # lower 5
      sendAndWait(none, none, r1, lin_act_time)
      #sendAndWait(r1, r1, r1, lin_act_time )
      grounded[0] = True
      active_group = 0
  elif direction == "left":
    if active_group == 0:
      if grounded[active_group]:
        # raise 1
        sendAndWait(e1, none, none, lin_act_time)
        # raise 3
        sendAndWait(none, e1, none, lin_act_time)
        # raise 5
        sendAndWait(none, none, e1, lin_act_time)
        grounded[active_group] = False
      # rotate 1,3 backwards, 5 forwards
      if speed > 0.5:
        sendAndWait(b1, b1, f1, stepper_time)
      else:
        sendAndWait(sb1, sb1, sf1, small_stepper_time)
      # lower 1
      sendAndWait(r1, none, none, lin_act_time)
      # lower 3
      sendAndWait(none, r1, none, lin_act_time)
      # lower 5
      sendAndWait(none, none, r1, lin_act_time)
      grounded[active_group] = True
      # raise 2
      sendAndWait(e2, none, none, lin_act_time)
      # raise 4
      sendAndWait(none, e2, none, lin_act_time)
      # raise 6
      sendAndWait(none, none, e2, lin_act_time)
      grounded[1] = False
      # rotate 1,3,5 neutral
      sendAndWait(n1, n1, n1, stepper_time)
      # lower 2
      sendAndWait(r2, none, none, lin_act_time)
      # lower 4
      sendAndWait(none, r2, none, lin_act_time)
      # lower 6
      sendAndWait(none, none, r2, lin_act_time)
      grounded[1] = True
      active_group = 1
    else:
      # active group is 1
      if grounded[active_group]:
        # raise 2
        sendAndWait(e2, none, none, lin_act_time)
        # raise 4
        sendAndWait(none, e2, none, lin_act_time)
        # raise 6
        sendAndWait(none, none, e2, lin_act_time)
        grounded[active_group] = False
      # rotate 2 backwards, 4,6 forward
      if speed > 0.5:
        sendAndWait(b2, f2, f2, stepper_time)
      else:
        sendAndWait(sb2, sf2, sf2, small_stepper_time)
      # lower 2
      sendAndWait(r2, none, none, lin_act_time)
      # lower 4
      sendAndWait(none, r2, none, lin_act_time)
      # lower 6
      sendAndWait(none, none, r2, lin_act_time)
      grounded[active_group] = True
      # raise 1
      sendAndWait(e1, none, none, lin_act_time)
      # raise 3
      sendAndWait(none, e1, none, lin_act_time)
      # raise 5
      sendAndWait(none, none, e1, lin_act_time)
      grounded[0] = False
      # rotate 2,4,6 neutral
      sendAndWait(n2, n2, n2, stepper_time)
      # lower 1
      sendAndWait(r1, none, none, lin_act_time)
      # lower 3
      sendAndWait(none, r1, none, lin_act_time)
      # lower 5
      sendAndWait(none, none, r1, lin_act_time)
      grounded[0] = True
      active_group = 0       
  elif direction == "right":
    if active_group == 0:
      if grounded[active_group]:
        # raise 1
        sendAndWait(e1, none, none, lin_act_time)
        # raise 3
        sendAndWait(none, e1, none, lin_act_time)
        # raise 5
        sendAndWait(none, none, e1, lin_act_time)
        grounded[active_group] = False
      # rotate 1,3 forwards, 5 back
      if speed > 0.5:
        sendAndWait(f1, f1, b1, stepper_time)
      else:
        sendAndWait(sf1, sf1, sb1, small_stepper_time)
      # lower 1
      sendAndWait(r1, none, none, lin_act_time)
      # lower 3
      sendAndWait(none, r1, none, lin_act_time)
      # lower 5
      sendAndWait(none, none, r1, lin_act_time)
      grounded[active_group] = True
      # raise 2
      sendAndWait(e2, none, none, lin_act_time)
      # raise 4
      sendAndWait(none, e2, none, lin_act_time)
      # raise 6
      sendAndWait(none, none, e2, lin_act_time)
      grounded[1] = False
      # rotate 1,3,5 neutral
      sendAndWait(n1, n1, n1, stepper_time)
      # lower 2
      sendAndWait(r2, none, none, lin_act_time)
      # lower 4
      sendAndWait(none, r2, none, lin_act_time)
      # lower 6
      sendAndWait(none, none, r2, lin_act_time)
      grounded[1] = True
      active_group = 1
    else:
      # active group is 1
      if grounded[active_group]:
        # raise 2
        sendAndWait(e2, none, none, lin_act_time)
        # raise 4
        sendAndWait(none, e2, none, lin_act_time)
        # raise 6
        sendAndWait(none, none, e2, lin_act_time)
        grounded[active_group] = False
      # rotate 2 forward, 4,6 back
      if speed > 0.5:
        sendAndWait(f2, b2, b2, stepper_time)
      else:
        sendAndWait(sf2, sb2, sb2, small_stepper_time)
      # lower 2
      sendAndWait(r2, none, none, lin_act_time)
      # lower 4
      sendAndWait(none, r2, none, lin_act_time)
      # lower 6
      sendAndWait(none, none, r2, lin_act_time)
      grounded[active_group] = True
      # raise 1
      sendAndWait(e1, none, none, lin_act_time)
      # raise 3
      sendAndWait(none, e1, none, lin_act_time)
      # raise 5
      sendAndWait(none, none, e1, lin_act_time)
      grounded[0] = False
      # rotate 2,4,6 neutral
      sendAndWait(n2, n2, n2, stepper_time)
      # lower 1
      sendAndWait(r1, none, none, lin_act_time)
      # lower 3
      sendAndWait(none, r1, none, lin_act_time)
      # lower 5
      sendAndWait(none, none, r1, lin_act_time)
      grounded[0] = True
      active_group = 0    
  elif direction == "lower":
    if not grounded[0]:
      # lower 1
      sendAndWait(r1, none, none, lin_act_time)
      # lower 3
      sendAndWait(none, r1, none, lin_act_time)
      # lower 5
      sendAndWait(none, none, r1, lin_act_time)
      grounded[0] = True
    if not grounded[1]:
      # lower 2
      sendAndWait(r2, none, none, lin_act_time)
      # lower 4
      sendAndWait(none, r2, none, lin_act_time)
      # lower 6
      sendAndWait(none, none, r2, lin_act_time)
      grounded[1] = True
      
      
def listener():
  rospy.init_node('motor_control_open_loop', anonymous=True)
  rospy.loginfo("Node started")

  rospy.Subscriber('user_input_pub', UserInput, callback)
  rospy.loginfo("Subscribed to user input")
  rospy.spin()

if __name__ == '__main__':
  listener()
