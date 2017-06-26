from scanner import *
from localizer import *
from tools import *
from models import *
import numpy as np
import h5py
from keras.models import load_model

wifi = wifi_scanner('wlp3s0')

office_loc = localizer(wifi)
#office_loc.make_profile('406', length=20)
office_loc.load_profile('406')
print('profile len: ', len(office_loc.profile))

#office_loc.add_cells_to_profile('test_prof', num_add=6)
#print('profile len: ', len(office_loc.profile))

capture_data(office_loc)

X , y = load_data_from_folder('../datasets')

print(X.shape)


