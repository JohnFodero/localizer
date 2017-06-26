from scanner import *
from localizer import *
from tools import *
from models import *
import numpy as np
import h5py
from keras.models import load_model
wifi = wifi_scanner('wlp3s0')

lab_loc = localizer(wifi)
lab_loc.load_profile('lab_profile')

print(lab_loc)

x, y = load_data_from_folder('../datasets', lab_loc.profile)
print(x.shape)
print(y.shape)

model = aModel().build_model(X.shape[1:])
model.summary()
model.save('../models/testa.hdf5')
print('modela')
modela = load_model('../models/testa.hdf5')
modela.summary()

