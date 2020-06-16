#!/bin/bash
self_IP=$(ifconfig "wlan0"| grep "inet addr"| awk '{print $2}'|awk -F: '{print $2}'
)
echo "export ROS_IP=$self_IP" >> ~/.bashrc

