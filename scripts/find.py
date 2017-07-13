from scanner import *
from localizer import *
from tools import *
import numpy as np
from keras.models import load_model
from time import sleep

wifi = wifi_scanner('wlp3s0')

lab_loc = localizer(wifi)
lab_loc.load_profile('4thHall_profile')
print(len(lab_loc.profile))
print(lab_loc)

model = load_model('../models/4thHall_profile-Normal.hdf5')
model.summary()

'''
# for testing a file as model input data
X_temp, y_temp = load_data_from_file('../datasets/old_datasets/2017-07-06_08:46', lab_loc.profile, keep_percent=1.0)
X_temp = X_temp[:,::2]
print(X_temp.shape)
print(X_temp)
for item in X_temp:
    cells = np.expand_dims(item, axis=0)
    print(cells)
    print(cells.shape)
    print(model.predict(cells))
    sleep(0.5)
'''
while True:
    cells = np.expand_dims(lab_loc.wifi.get_wifi_cells(lab_loc.profile, item='rssi'), axis=0)
    cells = scale_inputs(cells)
    preds = model.predict(cells)
#    print('Predictions: ', preds)
    scaled_x, scaled_y = scale_xy(preds[0,0], preds[0,1], imin=0., imax=1., omin=0., omax=69.75)
    print('Scaled predictions: ', scaled_x, scaled_y)
    sleep(0.5)
