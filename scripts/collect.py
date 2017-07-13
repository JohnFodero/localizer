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
cam1, cam2 = start_image_capture(1, 2)
print('Cameras started')

while True:
    # get kobuki location
#    input('left-click location on map and hit enter')
#    x, y = m.get_location()
    x = input('X: ')
    y = input('Y: ')
    print('Collecting at :', x, y)
    input('press enter to begin')
    path1, path2 = capture_images(cam1, cam2)
    print('images captured')
    for i in range(50):
        # get mag readings
        # get image
        write_line(wr, office_loc, x, y, mag_x=0.0, mag_y=0.0, mag_z=0.0, img1=path1, img2=path2)
        sleep(1)
        print('sample ', i)
m.close_display()
stop_capture(f)
