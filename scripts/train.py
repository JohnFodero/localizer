import numpy as np
np.random.seed(7)
from scanner import *
from localizer import *
from tools import *
from models import *
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import mean_squared_error

wifi = wifi_scanner('wlp3s0')

localizers = []
lab_loc = localizer(wifi)
lab_loc.load_profile('lab_profile')
localizers.append(lab_loc)


print(lab_loc)

# load and scale the data
X_train, y_train, X_test, y_test = load_data_from_folder('../datasets', lab_loc.profile, train_test_split=0.9, keep_percent=1.0, item='rssi')

shape_str = '{:10s} | {:15s} | {:15s}'
print(shape_str.format('', 'X shape', 'y shape'))
print(shape_str.format('TRAIN', str(X_train.shape), str(y_train.shape)))
print(shape_str.format('TEST', str(X_test.shape), str(y_test.shape)))

# 1) build model
# 2) compile model(s)
models = []
model = WifiOnlyXY(input_shape=X_train.shape[1:], output_shape=2).model
models.append((model, 'WifiStandard'))
model2 = MinimalWifiOnlyXY(input_shape=X_train.shape[1:], output_shape=2).model
models.append((model2, 'WifiSimple'))


# 3) fit model
epochs = 1000
batch_size = 32

for localizer in localizers:
    loc_name = localizer.name
    for model in models:

        checkpoint = ModelCheckpoint(filepath='../models/{}-{}.hdf5'.format(loc_name, model[1]), monitor='val_loss', verbose=0, save_best_only=True, mode='min')
        model[0].fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=0, callbacks=[checkpoint])

        # 4) evaluate model
        print('{}-{}'.format(loc_name, model[1]))
        print('Training MSE: {}'.format(model.evaluate(X_train, y_train, verbose=0)))
        print('Testing MSE: {}'.format(model.evaluate(X_test, y_test, verbose=0)))

# 5) predict
# see find.py