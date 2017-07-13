from scanner import *
from localizer import *
from tools import *
from models import *
import numpy as np
import h5py
from keras.models import load_model
from time import sleep
wifi = wifi_scanner('wlp3s0')

wifi_loc = localizer(wifi)

f, wr = start_capture()
while True:
    x = float(input('Enter X: '))
    y = float(input('Enter Y: '))
    print('Collecting at :', x, y)
    input('Press enter to begin..')
    for i in range(100):
        write_line(wr, wifi_loc, x, y, mag_x=0.0, mag_y=0.0, mag_z=0.0, img1='na', img2='na')
        sleep(1)
        print('sample ', i)

stop_capture(f)
