import numpy as np
np.random.seed(7)
from scanner import *
from localizer import *
from tools import *
from models import *
import h5py
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from keras import backend
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

wifi = wifi_scanner('wlp3s0')

lab_loc = localizer(wifi)
lab_loc.load_profile('lab_profile')

print(lab_loc)

# load and scale the data
X, y = load_data_from_folder('../datasets', lab_loc.profile, keep_percent=1.0)
# get the RSSI only - for now..
X = X[:, ::2]
X = scale_inputs(X)

np.random.seed(7)
p = np.random.permutation(len(X))
X, y = X[p], y[p]

split = int(0.9 * X.shape[0])
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

shape_str = '{:10s} | {:15s} | {:15s}'
print(shape_str.format('', 'X shape', 'y shape'))
print(shape_str.format('TRAIN', str(X_train.shape), str(y_train.shape)))
print(shape_str.format('TEST', str(X_test.shape), str(y_test.shape)))
print(shape_str.format('TOTAL', str(X.shape), str(y.shape)))

# 1) build model
# 2) compile model
model = WifiOnlyXY(input_shape=X.shape[1:], output_shape=2).model
model.summary()

# 3) fit model
epochs = 100
batch_size = 32

checkpoint = ModelCheckpoint(filepath='../models/lab_xy2.hdf5', monitor='val_loss', verbose=1, save_best_only=True, mode='min')
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=2, callbacks=[checkpoint])
model.save('../models/lab_xy2.hdf5')

# 4) evaluate model
# is this a good evaluation?
print('Training MSE: ', model.evaluate(X_train, y_train, verbose=0))
print('Testing: ', model.evaluate(X_test, y_test, verbose=0))

# 5) predict
# find.py