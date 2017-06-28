from scripts import tools, scanner, localizer
import numpy as np
import h5py
from keras.models import load_model
from time import sleep
wifi = scanner.wifi_scanner('wlp3s0')

office_loc = localizer.localizer(wifi)

locations = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
f, wr = tools.start_capture()
for x, y in locations:
    print('Collecting at :', x, y)
    input('Press enter to begin..')
    for i in range(100):
        tools.write_line(wr, office_loc, x, y, mag_x=0.0, mag_y=0.0, mag_z=0.0, img1='na', img2='na')
        sleep(1)
        print('sample ', i, end='\r')

tools.stop_capture(f)
