import numpy as np
np.random.seed(7)
from scanner import *
from localizer import *
from tools import *
from models import *
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import mean_squared_error

wifi = wifi_scanner('wlp3s0')

lab_loc = localizer(wifi)
lab_loc.load_profile('lab_profile')

print(lab_loc)

# load and scale the data
X_train, y_train, X_test, y_test = load_data_from_folder('../datasets', lab_loc.profile, train_test_split=0.9, keep_percent=1.0, item='rssi')

shape_str = '{:10s} | {:15s} | {:15s}'
print(shape_str.format('', 'X shape', 'y shape'))
print(shape_str.format('TRAIN', str(X_train.shape), str(y_train.shape)))
print(shape_str.format('TEST', str(X_test.shape), str(y_test.shape)))

# 1) build model
# 2) compile model
model = WifiOnlyXY(input_shape=X.shape[1:], output_shape=2).model
model.summary()

# 3) fit model
epochs = 100
batch_size = 32

checkpoint = ModelCheckpoint(filepath='../models/lab_xyQ.hdf5', monitor='val_loss', verbose=0, save_best_only=True, mode='min')
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=0, callbacks=[checkpoint])

# 4) evaluate model
print('Training MSE: {}'.format(model.evaluate(X_train, y_train, verbose=0)))
print('Testing MSE: {}'.format(model.evaluate(X_test, y_test, verbose=0)))

# 5) predict
# find.py