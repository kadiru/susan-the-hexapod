#!/usr/bin/env python3
import rospy
import serial
import time
from user_input.msg import UserInput

serl12 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313930351C05231-if00', 115200, timeout=1);
serl34 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00', 115200, timeout=1);
serl56 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313637351115182-if00', 115200, timeout=1);

lin_act_time = 1500#2000
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

we = "we\n"
rq = "rq\n"
qe = "qe\n"
wr = "wr\n"
# rotation codes
# f = forwards, b = backwards, n = neutral
f1 = "t\n"
b1 = "y\n"
f2 = "u\n"
b2 = "i\n"
n1 = "o\n"
n2 = "p\n"

ti = "ti\n"
tu = "tu\n"
yu = "yu\n"
yi = "yi\n"
op = "op\n"

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
    #sendAndWait(f1, f1, f1, stepper_time)
    #sendAndWait(f2, f2, f2, stepper_time)
    sendAndWait(e1,e1,e1, 0)
    
    sendAndWait(ti,ti,ti, lin_act_time)
    
    #Raising 2,4,6 Lowering 1,3,5
    sendAndWait(we,we,we, lin_act_time)
    sendAndWait(yu,yu,yu, lin_act_time)
    
    for i in range(7):
    	
    	#Raising 1,3,5 Lowering 2,4,6
    	sendAndWait(rq,rq,rq, lin_act_time)
    	sendAndWait(ti,ti,ti, lin_act_time)
    
    	#Raising 2,4,6 Lowering 1,3,5
    	sendAndWait(we,we,we, lin_act_time)
    	sendAndWait(yu,yu,yu, lin_act_time)
    
    #Raising 1,3,5 Lowering 2,4,6
    #sendAndWait(rq,rq,rq, lin_act_time)
    #sendAndWait(ti,ti,ti, lin_act_time)    
    
    #Raising 2,4,6 Lowering 1,3,5
    #sendAndWait(we,we,we, lin_act_time)
    #sendAndWait(yu,yu,yu, lin_act_time)
    
    #Raising 1,3,5 Lowering 2,4,6
    #sendAndWait(rq,rq,rq, lin_act_time)
    #sendAndWait(ti,ti,ti, lin_act_time)    
    
    #Raising 2,4,6 Lowering 1,3,5
    #sendAndWait(we,we,we, lin_act_time)
    #sendAndWait(yu,yu,yu, lin_act_time)


    #Raising 1,3,5 Lowering 2,4,6
    sendAndWait(rq,rq,rq, lin_act_time)
    sendAndWait(op,op,op, lin_act_time)
    sendAndWait(r1,r1,r1, lin_act_time)
    
    
  if direction == "backwards":
    sendAndWait(e1,e1,e1, 0)
    sendAndWait(yu,yu,yu, lin_act_time)
    #Raise 2,4,6 Lower 1,3,5
    sendAndWait(we,we,we, lin_act_time)
    sendAndWait(ti,ti,ti, lin_act_time)

    for i in range(7):
    	#Raise 1,3,5 Lower 2,4,6
    	sendAndWait(rq,rq,rq, lin_act_time)
    	sendAndWait(yu,yu,yu, lin_act_time)
    
    	#Raise 2,4,6 Lower 1,3,5
    	sendAndWait(we,we,we, lin_act_time)
    	sendAndWait(ti,ti,ti, lin_act_time)
    
    
    #Raise 1,3,5 Lower 2,4,6
    sendAndWait(rq,rq,rq, lin_act_time)
    sendAndWait(op,op,op, lin_act_time)
    sendAndWait(r1,r1,r1, lin_act_time)
  if direction == "right":
    sendAndWait(e1, e1, e1, lin_act_time)
    sendAndWait(ti, tu, yu, lin_act_time)
    sendAndWait(we, we, we, lin_act_time)
    sendAndWait(yu, yi, ti, lin_act_time)    
    sendAndWait(rq, rq, rq, lin_act_time)
    sendAndWait(op, op, op, lin_act_time)
    sendAndWait(r1, r1, r1, lin_act_time)    
  if direction == "left":
    sendAndWait(e1, e1, e1, lin_act_time)
    sendAndWait(yu, yi, ti, lin_act_time)
    sendAndWait(we, we, we, lin_act_time)
    sendAndWait(ti, tu, yu, lin_act_time)    
    sendAndWait(rq, rq, rq, lin_act_time)
    sendAndWait(op, op, op, lin_act_time)
    sendAndWait(r1, r1, r1, lin_act_time)  
  #if direction == "left":  
  #  sendAndWait(none, none, r1, lin_act_time)
      
      
def listener():
  rospy.init_node('try_node', anonymous=True)
  rospy.loginfo("Node started")

  rospy.Subscriber('user_input_pub', UserInput, callback)
  rospy.loginfo("Subscribed to user input")
  rospy.spin()

if __name__ == '__main__':
  listener()
