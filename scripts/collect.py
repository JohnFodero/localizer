from scanner import *
from localizer import *
from tools import *
from mapping import *
import numpy as np
from time import sleep
import datetime
import cv2


wifi = jetson_wifi_scanner()

office_loc = localizer(wifi)

#m = mapping('maps/NEBfourthfloor.png', 'maps/obstacle_bitmap.bmp')
#m.initiate_display()
#m.update_kobuki(200,200)
f, wr = start_capture()
cam1 = cv2.VideoCapture(1)
cam2 = cv2.VideoCapture(2)
path='../datasets/images/'
print('Cameras started')

while True:
    # get kobuki location
#    input('left-click location on map and hit enter')
#    x, y = m.get_location()
    x = input('X: ')
    y = input('Y: ')
    print('Collecting at :', x, y)
    input('press enter to begin')
    name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    path1 = path + name + '_cam1.jpg'
    path2 = path + name + '_cam2.jpg'
    s1, img1 = cam1.read()
    s2, img2 = cam2.read()
    img1 = rotate_about_center(img1, 90)
    img2 = rotate_about_center(img2, 90)
    cv2.imwrite(path1, img1)
    cv2.imwrite(path2, img2)
    print('images captured')
    for i in range(10):
        # get mag readings
        # read image anyway even though we aren't saving it..
        s1, img1 = cam1.read()
        s2, img2 = cam2.read()
        write_line(wr, office_loc, x, y, mag_x=0.0, mag_y=0.0, mag_z=0.0, img1=path1, img2=path2)
        sleep(1)
        print('sample ', i)
cam1.release()
cam2.release()
m.close_display()
stop_capture(f)
