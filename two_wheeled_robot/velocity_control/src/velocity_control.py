#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == "nt":
	import msvcrt
else:
	import tty, termios

MAX_LIN_VEL = 1.0 #0.22
MAX_ANG_VEL = 5.0 #2.84

LIN_VEL_STEP = 0.1
ANG_VEL_STEP = 0.1

msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d
        x

w/x : increase/decrease linear velocity (Burger : ~ 0.22)
a/d : increase/decrease angular velocity (Burger : ~ 2.84)

space key, s : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""

def get_key():
	tty.setraw(sys.stdin.fileno())
	rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
	if rlist:
		key = sys.stdin.read(1)
	else:
		key = ''

	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

def print_vel(target_linear_vel, target_angular_vel):
	return "currently:\tlinear velocity %s\t angular velocity %s " % (target_linear_vel,target_angular_vel)

def makeSimpleProfile(output, input, slope):
	if input > output:
		output = min(input, output+slope)
	elif input < output:
		output = max(input, output-slope)
	else:
		output = input
	return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
	vel = constrain(vel, -MAX_LIN_VEL, MAX_LIN_VEL)
	return vel

def checkAngularLimitVelocity(vel):
	vel = constrain(vel, -MAX_ANG_VEL, MAX_ANG_VEL)
	return vel

if __name__=="__main__":
	if os.name != "nt":
		settings = termios.tcgetattr(sys.stdin)
	rospy.init_node('velocity_control')
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

	#status = 0
	target_linear_vel   = 0.0
	target_angular_vel  = 0.0
	control_linear_vel  = 0.0
	control_angular_vel = 0.0

	try:
		print msg
		while(1):
			key = get_key()
			if key == 'w' :
				target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP)
				#status = status + 1
				print print_vel(target_linear_vel,target_angular_vel)
			elif key == 'x' :
				target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP)
				#status = status + 1
				print print_vel(target_linear_vel,target_angular_vel)
			elif key == 'd' :
				target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP)
				#status = status + 1
				print print_vel(target_linear_vel,target_angular_vel)
			elif key == 'a' :
				target_angular_vel = checkAngularLimitVelocity(target_angular_vel - ANG_VEL_STEP)
				#status = status + 1
				print print_vel(target_linear_vel,target_angular_vel)
			elif key == ' ' or key == 's' :
				target_linear_vel   = 0.0
				control_linear_vel  = 0.0
				target_angular_vel  = 0.0
				control_angular_vel = 0.0
				print print_vel(target_linear_vel, target_angular_vel)
			else:
			    if (key == '\x03'):
			        break

			twist = Twist()

			control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP/2.0))
			twist.linear.x = control_linear_vel
			twist.linear.y = 0.0
			twist.linear.z = 0.0

			control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP/2.0))
			twist.angular.x = 0.0
			twist.angular.y = 0.0
			twist.angular.z = control_angular_vel

			pub.publish(twist)

	except:
		print e

	finally:
	    twist = Twist()
	    twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
	    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
	    pub.publish(twist)

	if os.name != "nt":
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)