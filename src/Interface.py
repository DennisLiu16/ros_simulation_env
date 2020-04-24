#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:52:53 2020

@author: BreezeCat
"""
import serial
import threading
import rospy
from geometry_msgs.msg import Twist

feedback_vel = rospy.Publisher("FeedBack_Vel", Twist, queue_size=10)

COM_Name = '/dev/ttyACM3'
BAUTRATE = 9600
Stop_flag = 1

Cmd_R = 0.0
Cmd_L = 0.0
Vel_R = 0.0
Vel_L = 0.0

def VW2RL(V, W):
    return V, W

def RL2VW(R, L):    
    return R, L

def floatmodify(NUM):
    if NUM < 0:
        STR = str('%.2f'%NUM)
        if len(STR) < 6:
            STR = STR[0] + '0' + STR[1:]
    else:
        STR = str('%.2f'%NUM)
        while len(STR) < 6:
            STR = '0' + STR
    return STR           
        

def Cmd_pub(Serial):
    Command_String = 's' + floatmodify(Cmd_R) + floatmodify(Cmd_L) + 'e'  
    Serial.write(Command_String)
    return

def FeedBack_pub():
    Vel_FB = Twist()
    Vel_FB.linear.x, Vel_FB.angular.z = RL2VW(Vel_R, Vel_L)
    feedback_vel.publish(Vel_FB)
    return

def Cmd_CB(data):
    global Cmd_R, Cmd_L
    Cmd_V = data.linear.x
    Cmd_W = data.angular.z
    Cmd_R, Cmd_L = VW2RL(Cmd_V, Cmd_W)
    return
    

def Connect_STM(COM, baudrate):
    try:
        ser = serial.Serial(COM, baudrate)
    except:
        print('Connect Error!')
        return 'Error'
    return ser

def Read_data(Serial):
    global Vel_R, Vel_L
    while(Stop_flag):
        data = Serial.readline()
        R, L = data.split(',')
        Vel_R = float(R)
        Vel_L = float(L)  
    return
    
if __name__ == '__main__':
    rospy.init_node('TX2_STM_INTERFACE', anonymous= True)
    rate = rospy.Rate(10)
    cmd_sub = rospy.Subscriber("/cmd_vel", Twist, Cmd_CB)     
    try:
        STM = Connect_STM(COM_Name, BAUTRATE)
        if STM != 'Error':
            t = threading.Thread(target=Read_data, args=(STM,))
            t.start()
            while not rospy.is_shutdown():
                Cmd_pub(STM)
                FeedBack_pub()
                rate.sleep()
        
 
    except KeyboardInterrupt:
        Stop_flag = 0
        STM.close()   
        print('bye!')
