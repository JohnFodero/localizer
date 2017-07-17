from scanner import *
from localizer import *
from tools import *
#from models import *
from mapping import *
import numpy as np
#import h5py
#from keras.models import load_model
from time import sleep

wifi = jetson_wifi_scanner()

office_loc = localizer(wifi)

#m = mapping('maps/NEBfourthfloor.png', 'maps/obstacle_bitmap.bmp')
#m.initiate_display()
#m.update_kobuki(200,200)
f, wr = start_capture()
cam1 = cv2.VideoCapture(0)
path = '../datasets/images/'
print('Cameras started')

while True:
    # get kobuki location
#    input('left-click location on map and hit enter')
#    x, y = m.get_location()
    x = input('X: ')
    y = input('Y: ')
    print('Collecting at :', x, y)
    mag = input('Enter angle: ')
    input('press enter to begin')
    name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    path1 = path + name + '_cam1.jpg'
    path2 = path + name + '_cam2.jpg'
    t1, img1 = cam1.read()
    t1, img1 = cam1.read()
    t1, img1 = cam1.read()
    t1, img1 = cam1.read()
    t1, img1 = cam1.read()
    t1, img1 = cam1.read()

    
    cv2.imwrite(path1, img1)
    cv2.imwrite(path2, img1)
    print('images captured')
    for i in range(25):
        # get mag readings
        # get image
        write_line(wr, office_loc, x, y, mag_x=mag, mag_y=0.0, mag_z=0.0, img1=path1, img2=path2)
        sleep(1)
        print('sample ', i)

cam1.release()

m.close_display()
stop_capture(f)
