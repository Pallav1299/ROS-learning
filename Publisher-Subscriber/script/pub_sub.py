#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    data = data.data + "cup"
    pub.publish(data)

def subscribing():
    global pub

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Preparing_Hot_Coffee', anonymous=True) # Preparing_Hot_Coffee is the name of the node
    rospy.Subscriber('ingredients', String, callback) # ingredients is the topic
    pub = rospy.Publisher("Your_Coffee", String, queue_size=10)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    subscribing()