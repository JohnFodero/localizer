from scanner import *
from localizer import *
from tools import *
import numpy as np
wifi = wifi_scanner('wlp3s0')
cells = wifi.get_wifi_cells()
print(cells)
print(cells.shape)

office_loc = localizer(wifi)
#office_loc.make_profile('test_prof', length=12)
office_loc.load_profile('test_prof')
#print(office_loc.profile)
print('profile len: ', len(office_loc.profile))

#office_loc.add_cells_to_profile('test_prof', num_add=6)
#print('profile len: ', len(office_loc.profile))

capture_data(office_loc)

X = None
y = None
for file_name in os.listdir('../datasets'):
    X_temp, y_temp = load_data('../datasets/' + file_name)
    if X is None:
        X = np.array(X_temp)
        y = np.array(y_temp)
    else:
        X = np.concatenate((X, X_temp))
        y = np.concatenate((y, y_temp))
    print('{} loaded'.format(file_name))
print(X.shape)
