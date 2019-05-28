#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def publishing():
    pub = rospy.Publisher('ingredients', String, queue_size=10) ## ingredients is a topic
    rospy.init_node('Coffee_ingredients', anonymous=True) ## Coffee_ingredients
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        data = "sugar,milk,coffee"
        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()

if __name__ == '__main__':
    try:
        publishing()
    except rospy.ROSInterruptException:
        pass