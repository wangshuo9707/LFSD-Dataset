#!/usr/bin/env python
"""
Transform image , imu and GPS files to a ros bag file

Author: wangshuo
"""
from __future__ import print_function
import time
import cv2
import time, sys, os
import rosbag
import roslib
import rospy
#roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import Image,Imu
from std_msgs.msg import Int32, String
####import realsense2_camera.msg
from geometry_msgs.msg import Vector3
import numpy as np
from numpy import asarray
from cv_bridge import CvBridge
from PIL import ImageFile
from PIL import Image as ImagePIL
from sensor_msgs.msg import CameraInfo
####from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped

#####################################3
def ReadGPS_GROUNDTRUTH(filename):
    file = open(filename + "/groundtruth.txt",'r')
    all = file.readlines()
    timestamp = []
    groundtruth_data = []
    index = 0
    for f in all:
        index = index + 1
        if index == 1:
            continue
        line = f.rstrip('\n').split(' ')
        timestamp.append(line[0])
        groundtruth_data.append(line[1:])
    print("Total add %i imus!"%(index))
    return timestamp,groundtruth_data

def ReadGPS(filename):
    file = open(filename + "/gps.txt",'r')
    all = file.readlines()
    timestamp = []
    gps_data = []
    index = 0
    for f in all:
        index = index + 1
        if index == 1:
            continue
        line = f.rstrip('\n').split(',')
        timestamp.append(line[0])
        gps_data.append(line[1:])
    print("Total add %i imus!"%(index))
    return timestamp,gps_data

def Readaccel(filename):
    file = open(filename + "/accel.txt",'r')
    all = file.readlines()
    timestamp = []
    accel_data = []
    index = 0
    for f in all:
        index = index + 1
        if index == 1:
            continue
        line = f.rstrip('\n').split(' ')
        timestamp.append(line[0])
        accel_data.append(line[1:])
    print("Total add %i imus!"%(index))
    return timestamp,accel_data

def Readgyro(filename):
    file = open(filename + "/gyro.txt",'r')
    all = file.readlines()
    timestamp = []
    gyro_data = []
    index = 0
    for f in all:
        index = index + 1
        if index == 1:
            continue
        line = f.rstrip('\n').split(' ')
        timestamp.append(line[0])
        gyro_data.append(line[1:])
    print("Total add %i imus!"%(index))
    return timestamp,gyro_data


if __name__ == "__main__":
    path='' # file directory  , such as     '/media/wxc/datadisk/ws/_2022-04-25-14-11-40
    bag_revise = rosbag.Bag('*.bag',"w")  # The directory location of the generated rosbag file ,   such as   '/media/wxc/datadisk/ws/ws_all.bag'
    groundtruth_timestamp,groundtruth_data=ReadGPS_GROUNDTRUTH(path+'/GPS')
    gps_timestamp,gps_data=ReadGPS(path+'/GPS')
    accel_timestamp, accel_data=Readaccel(path+'/D435i')
    gyro_timestamp, gyro_data=Readgyro(path+'/D435i')


    ##groundtruth
    for i in range(len(groundtruth_data)):
      str = ' '
      a=str.join(groundtruth_data[i])
      s = String()
      s.data=a
      b=groundtruth_timestamp[i]
      # m=b.split(".")
      # time1 = rospy.Time(int(m[0]),int(m[0]))
      time1 = rospy.Time(float(groundtruth_timestamp[i]))
      #time1=rospy.rostime.Time.from_sec(float(groundtruth_timestamp[i]))
      bag_revise.write("/groundtruth",s,time1)
    ##gps
    for i in range(len(gps_data)):
      str0 = ' '
      a0=str.join(gps_data[i])
      s0 = String()
      s0.data=a0
      b0=gps_timestamp[i]
      # m=b.split(".")
      # time1 = rospy.Time(int(m[0]),int(m[0]))
      time0 = rospy.Time(float(gps_timestamp[i]))
      bag_revise.write("/gps",s0,time0)
    ##accel
    for i in range(len(accel_data)):
      str2 = ' '
      a2=str.join(accel_data[i])
      s2 = String()
      s2.data=a2
      b2=accel_timestamp[i]
      # m=b.split(".")
      # time1 = rospy.Time(int(m[0]),int(m[0]))
      time2 = rospy.Time(float(accel_timestamp[i]))
      bag_revise.write("/accel",s2,time2)
    ##gyro
    for i in range(len(gyro_data)):
      str3 = ' '
      a3=str.join(gyro_data[i])
      s3 = String()
      s3.data=a3
      b3=gyro_timestamp[i]
      # m=b.split(".")
      # time1 = rospy.Time(int(m[0]),int(m[0]))
      time3 = rospy.Time(float(gyro_timestamp[i]))
      bag_revise.write("/gyro",s3,time3)


    filename=(path+"/D435i")
    rgb_scan=os.listdir(os.path.join(filename,"RGB"))
    depth_scan = os.listdir(os.path.join(filename, "depth"))
    for i in range(len(rgb_scan)):
      # Adding depth image
      tt=rgb_scan[i].rsplit(".",1)
      Stamp = rospy.rostime.Time.from_sec(float(tt[0]) )  # Modify according to your own time unit
      '''set image information '''
      depth_image = ImagePIL.open(filename + "/depth/" + depth_scan[i])
      br = CvBridge()
      data = asarray(depth_image,dtype="uint16")
      depth_image_msg = br.cv2_to_imgmsg(data)  # Convert the depth image to a message
      depth_image_msg.header.stamp = Stamp
      depth_image_msg.header.frame_id = "camera"
      depth_image_msg.encoding = "16UC1"
      bag_revise.write('camera/depth', depth_image_msg, Stamp)

      rgb_image = ImagePIL.open(filename + "/RGB/" + rgb_scan[i])
      data = asarray(rgb_image)
      rgb_image_msg = br.cv2_to_imgmsg(data)  # Convert the color image to a message
      rgb_image_msg.header.stamp = Stamp
      rgb_image_msg.header.frame_id = "camera"
      rgb_image_msg.encoding = "rgb8"
      bag_revise.write('camera/color', rgb_image_msg, Stamp)

      print(Stamp)


    bag_revise.close()

    # b=0

