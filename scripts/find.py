from scanner import *
from localizer import *
from tools import *
from models import *
import numpy as np
import h5py
from keras.models import load_model
from time import sleep

wifi = wifi_scanner('wlp3s0')

lab_loc = localizer(wifi)
lab_loc.load_profile('lab_profile')
print(len(lab_loc.profile))
print(lab_loc)

model = load_model('../models/lab_xy2.hdf5')
model.summary()

while True:
    cells = np.expand_dims(lab_loc.wifi.get_wifi_cells(lab_loc.profile), axis=0)[:, ::2]
    cells = scale_inputs(cells)
    print(model.predict(cells))
    sleep(0.5)
