from scanner import *
from localizer import *
from tools import *
from models import *
from mapping import *
import numpy as np
import h5py
from keras.models import load_model
from time import sleep


wifi = wifi_scanner('wlp3s0')

office_loc = localizer(wifi)

m = mapping('maps/NEBfourthfloor.png', 'maps/obstacle_bitmap.bmp')
m.initiate_display()
m.update_kobuki(200,200)
f, wr = start_capture()
while True:
    # get kobuki location
    x, y = m.get_location()
    print('Collecting at :', x, y)
    input('press enter to begin')
    for i in range(100):
        # get mag readings
        # get image
        write_line(wr, office_loc, x, y, mag_x=0.0, mag_y=0.0, mag_z=0.0, img1='na', img2='na')
        sleep(1)
        print('sample ', i, end='\r')

stop_capture(f)
