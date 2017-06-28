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

X, y = load_data_from_folder('../datasets', lab_loc.profile)

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


model = WifiOnlyXY(input_shape=X.shape[1:], output_shape=2).model
model.summary()
model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=2)
model.save('../models/lab_xy.hdf5')

print(model.evaluate(X_train, y_train))
print(model.evaluate(X_test, y_test))
pred = model.predict(np.expand_dims(X[10], axis=0))
print(pred)
print(y[10])
