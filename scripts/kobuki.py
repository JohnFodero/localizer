#!/usr/bin/env pythoni
# coding:utf-8
#
# kobuki.py

from serial import Serial
import numpy as np
import cv2
import time
import csv
import os
from datetime import datetime

class kobuki :
    # initialize Kobuki
    def __init__(self, dev_path) :
        self.dev_path = dev_path

    def initialize(self) :
        #initialize Serial communication
        self.serial = Serial(self.dev_path, 115200)
        print("Serial connection to Kobuki initialized")
        # throttle and steering variables
        self.thr = 0
        self.steer = 0.5

    # send a command to Kobuki
    def send(self, commands) :
        sub_payloads = commands
        payload = []
        for sub_payload in sub_payloads :
            payload.append(sub_payload)
        header = [0xAA, 0x55]
        
        body = [len(payload)] + payload

        checksum = 0
        for x in body:
            checksum ^= x
                
        packets = header+body+[checksum]
        write_str = ''.join(map(chr, packets))
        self.serial.write(write_str.encode('latin-1'))
    
    # destructor
    # def __del__(self) :
    def deinitialize(self) :
        self.stop()
        self.serial.close()
        print("Serial connection to Kobuki closed")
        
        cv2.destroyAllWindows()
        print("OpenCV terminated")
        
    # Prepare byte string for speed and turn radius of Kobuki
    def base_control(self, speed, radius) :

        speed_lsb = 0xff & speed
        speed_msb = 0xff & (speed>>8)
        radius_lsb = 0xff & radius
        radius_msb = 0xff & (radius>>8)
        return [0x01, 0x04, speed_lsb, speed_msb, radius_lsb, radius_msb]

    # Stop the Kobuki
    def stop(self):
        self.send(self.base_control(0,0))

    def move(self, speed, radius):
        self.send(self.base_control(speed, radius))
       
    def drive(self, thr, steer) :
        radius = 0
        speed = 0
        if (thr == 1) :
            speed = 100

        elif (thr == 0) :
            speed = 0
            
        else :
            print("Wrong throttle value, setting to zero")
            speed = 0


        if (steer == 0.5) :
            radius = 0

        elif (steer == 0) :
            radius = 1

        elif (steer == 1) :
            radius = -1

        else :
            print("Wrong steering values, setting to 0.5")
            radius = 0

        self.send(self.base_control(speed,radius))
    
    # Main run loop
    def run(self) :

        # Create window for robot control input
        cv2.namedWindow('display', cv2.WINDOW_NORMAL)

        # Main loop
        while (True) :
            char = '\0'
            char = cv2.waitKey(10) & 255
            if(char == 27) :
                print("\tEscape key detected!")
                break

            elif char == ord('w'):
                self.thr = 1
                self.steer = 0.5
    
            elif char == ord('a') :
                self.thr = 1
                self.steer = 0

            elif char == ord('d') :
                self.thr = 1
                self.steer = 1
                
            elif char == ord('s') :
                self.thr = 0
                self.steer = 0.5
                
                
            self.drive(self.thr,self.steer)
        # Stop robot and exit
        self.stop()
        
if __name__ == '__main__' :
    kob = kobuki('/dev/ttyUSB0')
    kob.initialize()
    kob.run()
    kob.deinitialize()
