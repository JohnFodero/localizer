from scanner import *
from localizer import *
from tools import *
from mapping import *
from kobuki import *
from magnetometer import *
from time import *
import datetime
import cv2
import sys


            
if __name__ == '__main__':
    kob = kobuki('/dev/ttyUSB0')
    kob.initialize()
    mag = magnetometer(port=1, address=0x1E, declination=(-5,53))
    print('Resetting Calibration to 0, 0')
    mag.calibration = [0.0, 0.0]
    minx, miny = 1000, 1000
    maxx, maxy = -1000, -1000
    print('Begin calibration')
    for i in range(250):
        kob.drive(thr=1, steer=0)
        x, y, z = mag.get_xyz(scaled=False)
        if minx > x:
            minx = x
        if miny > y:
            miny = y
        if maxx < x:
            maxx = x
        if maxy < y:
            maxy = y
        if i % 10 == 0:
            print('X ', minx, maxx, 'Y ', miny, maxy)
        sleep(.1)
    kob.stop()
    x_off = (maxx + minx) / 2.
    y_off = (maxy + miny) / 2.
    print('X offset: ', x_off, 'Y offset: ', y_off)
    with open('mag_calibration.p', 'wb') as f:
        pickle.dump([x_off, y_off], f)
   
    kob.deinitialize()

# test new offsets
    input('Continue?')
    new_mag = magnetometer(port=1, address=0x1E, declination=(-5,53))
    while True:
        heading = mag.get_heading() 
        print(heading)
        sleep(0.5)
