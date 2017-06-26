from scanner import *
from localizer import *
from tools import *
from models import *
import numpy as np
import h5py
from keras.models import load_model

wifi = wifi_scanner('wlp3s0')

office_loc = localizer(wifi)

capture_data(office_loc)

X , y = load_data_from_folder('../datasets')

print(X.shape)


