#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist
import threading
import time

robot1_cmd_vel = rospy.Publisher("/robot1/cmd_vel", Twist, queue_size=10)
robot2_cmd_vel = rospy.Publisher("/robot2/cmd_vel", Twist, queue_size=10)



# Constants
stop_time = 5
Turn_flag = 1
Vcmd = 0
Wcmd = 0
Vel_cmd = Twist()
Vel_cmd.linear.x = Vcmd
Vel_cmd.angular.z = Wcmd


def Stop_cmd(robot):
    start_time = time.time()
    while (time.time() - start_time) < stop_time: 
    	robot.publish(Vel_cmd)
	time.sleep(0.001)
    print('Release')
    return

if __name__ == '__main__':
    rospy.init_node('stop_vel_cmd', anonymous= True)
    rate = rospy.Rate(1000)
    print("#####################")
    print("# Command list:     #")
    print("# Stop robot1 : 'A' #")
    print("# Stop robot2 : 'B' #")
    print("# Stop node : 'S'   #")
    print("#####################")
    while Turn_flag:
	command = input("Command: ")
	if command == 'A':
		print("Stop robot1 " + str(stop_time) + " s")
		t = threading.Thread(target=Stop_cmd, args=(robot1_cmd_vel,))
		t.start()
	elif command == 'B':
		print("Stop robot2 " + str(stop_time) + " s")
		t = threading.Thread(target=Stop_cmd, args=(robot2_cmd_vel,))
		t.start()
	elif command == 'S':
		print("Bye!")
		Turn_flag = 0
	else:
		print("Command error!")
       
