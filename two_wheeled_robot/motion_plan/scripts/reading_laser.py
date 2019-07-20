#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def laser_callback(msg):
	regions = [
        min(min(msg.ranges[:143]), 10),
        min(min(msg.ranges[144:287]), 10),
        min(min(msg.ranges[288:431]), 10),
        min(min(msg.ranges[432:575]), 10),
        min(min(msg.ranges[576:713]), 10),
    ]
	rospy.loginfo(regions)

if __name__=="__main__":
	rospy.init_node ("reading_laser")
	sub = rospy.Subscriber("m2wr/laser/scan", LaserScan, laser_callback)
	rospy.spin()