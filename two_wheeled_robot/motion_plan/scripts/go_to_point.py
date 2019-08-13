#! /usr/bin/env python
import roslib
roslib.load_manifest('motion_plan')
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf import transformations

import math

current_position_ = Point()
yaw_ = 0
state_ = 0
desired_position_ = Point()
desired_position_.x = 0
desired_position_.y = 3
desired_position_.z = 0
yaw_precision_ = math.pi/90
distance_precision_ = 0.3
pub = None

def main():
	global pub
	rospy.init_node('go_to_goal')
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
	sub = rospy.Subscriber('odom', Odometry, odom_callback)
	rate = rospy.Rate(20)
	while not rospy.is_shutdown():
		if state_ == 0:
			correct_yaw(desired_position_)
		elif state_ == 1:
			correct_linear(desired_position_)
		elif state_ == 2:
			reached()
			pass
		else:
			rospy.logerr('Unknown state')
			pass
		rate.sleep()

def correct_yaw(des_position):
	global yaw_, pub, state_, yaw_precision_
	required_yaw = math.atan2(des_position.y-current_position_.y, des_position.x-current_position_.x)
	error_yaw = required_yaw-yaw_

	twist = Twist()
	if math.fabs(error_yaw) > yaw_precision_:
		print 'correcting yaw'
		if error_yaw>0:
			twist.angular.z = -0.3
		else:
			twist.angular.z = 0.3
	pub.publish(twist)

	if math.fabs(error_yaw) <= yaw_precision_:
		print 'Error in yaw: %s' % error_yaw
		update_state(1)

def correct_linear(des_position):
	global yaw_, pub, state_, yaw_precision_
	required_yaw = math.atan2(des_position.y-current_position_.y, des_position.x-current_position_.x)
	error_yaw = required_yaw-yaw_
	error_pos = math.sqrt(pow(des_position.y-current_position_.y,2) + pow(des_position.x-current_position_.x,2))

	if error_pos > distance_precision_:
		twist = Twist()
		twist.linear.x = 0.3
		pub.publish(twist)
	else:
		print 'Error in position: %s' % error_pos
		update_state(2)

	if math.fabs(error_yaw) > yaw_precision_:
		print 'Error in yaw: %s' % error_yaw
		update_state(0)

def reached():
	twist = Twist()
	twist.linear.x = 0
	twist.angular.z = 0
	pub.publish(twist)

def update_state(state):
	global state_
	state_ = state
	print 'State changed to: %s' % state_

def odom_callback(msg):
	global current_position_, yaw_
	current_position_ = msg.pose.pose.position
	quaternion_data = (msg.pose.pose.orientation.x,
				   msg.pose.pose.orientation.y,
				   msg.pose.pose.orientation.z,
				   msg.pose.pose.orientation.w)
	euler_data = transformations.euler_from_quaternion(quaternion_data)
	yaw_ = euler_data[2]

if __name__=='__main__':
		main()