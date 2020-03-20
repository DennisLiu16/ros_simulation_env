#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 15:55:45 2020

@author: BreezeCat
"""

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

path_pub = rospy.Publisher("robot_path",Path,queue_size=10)

Px = []
Py = []

def Path_Publish():
    Robot_Path = Path()
    Robot_Path.header.frame_id = "map"
    for i in range(len(Px)):
        pose = PoseStamped()
        pose.pose.position.x = Px[i]
        pose.pose.position.y = Py[i]
        Robot_Path.poses.append(pose)
    path_pub.publish(Robot_Path)
    return
    


def Pose_CB(data):
    global Px, Py
    Px.append(data.linear.x)
    Py.append(data.linear.y)
    Path_Publish()
    return




if __name__ == '__main__':
    rospy.init_node('robot_path_pub',anonymous=True)
    rate = rospy.Rate(100)
    sub = rospy.Subscriber("/robot_pose",Twist,posecallback)
    while not rospy.is_shutdown():
        rate.sleep()