from scanner import *
from localizer import *
from tools import *
from mapping import *
from kobuki import *
import numpy as np
from time import sleep
import datetime
import cv2

loc = localizer(jetson_wifi_scanner())

kob = kobuki('/dev/ttyUSB0')
kob.initialize()

m = mapping('maps/NEBfourthfloor.png', 'maps/obstacle_bitmap.bmp')
m.initiate_display()
m.update_kobuki(200,200)
print('mapping started')

f, wr = start_capture()
cam1 = cv2.VideoCapture(1)
cam2 = cv2.VideoCapture(2)
path='../datasets/images/'
print('Cameras started')

while True:
    x, y = m.get_location()
    print('Collecting at :', x, y)
    kob.drive(thr=1, steer=0)
    for i in range(25):
        # get mag readings
        name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
        path1 = path + name + '_cam1.jpg'
        path2 = path + name + '_cam2.jpg'
        s1, img1 = cam1.read()
        s2, img2 = cam2.read()
        img1 = rotate_about_center(img1, 180)
#        img2 = rotate_about_center(img2, 90)
        cv2.imwrite(path1, img1)
        cv2.imwrite(path2, img2)
        write_line(wr, loc, x, y, mag_x=0.0, mag_y=0.0, mag_z=0.0, img1=path1, img2=path2)
        sleep(1)
        print('sample ', i)
    # stop kobuki
    kob.stop()
    
kob.deinitialize()
stop_capture(f)
cam1.release()
cam2.release()
m.close_display()

