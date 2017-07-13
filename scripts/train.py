import numpy as np
np.random.seed(7)
from scanner import *
from localizer import *
from tools import *
from models import *
from keras.callbacks import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

wifi = wifi_scanner('wlp3s0')

lab_loc = localizer(wifi)
lab_loc.load_profile('4thHall_profile')


# load and scale the data
X_train, y_train, X_test, y_test = load_data_from_folder('../datasets', lab_loc.profile, train_test_split=0.9, item='rssi')
y_train_scaled = []
for i, element in enumerate(y_train):
    x_temp, y_temp = scale_xy(y_train[i,0], y_train[i,1], imin=0., imax=2023., omin=0.0, omax=1.0)
    y_train_scaled.append([x_temp, y_temp])
y_train = np.array(y_train_scaled)

y_test_scaled = []
for i, element in enumerate(y_test):
    x_temp, y_temp = scale_xy(y_test[i,0], y_test[i,1], imin=0., imax=2023., omin=0.0, omax=1.0)
    y_test_scaled.append([x_temp, y_temp])
y_test = np.array(y_test_scaled)


shape_str = '{:10s} | {:15s} | {:15s}'
print(shape_str.format('', 'X shape', 'y shape'))
print(shape_str.format('TRAIN', str(X_train.shape), str(y_train.shape)))
print(shape_str.format('TEST', str(X_test.shape), str(y_test.shape)))

# 1) build model
# 2) compile model(s)
models = []
model = MinimalWifiOnlyXY(input_shape=X_train.shape[1:], output_shape=2).model
models.append((model, 'Minimal'))
model2 = RegWifiOnlyXY(input_shape=X_train.shape[1:], output_shape=2).model
models.append((model2, 'Regularized'))
model3 = WifiOnlyXY(input_shape=X_train.shape[1:], output_shape=2).model
models.append((model3, 'Normal'))


# 3) fit model
epochs = 10000
batch_size = 4
loc_name = lab_loc.profile_name

for model in models[1:2]:
    print('Training: {}-{}'.format(loc_name, model[1]))

    # Save the model after each epoch if the validation loss improved.
    save_best = ModelCheckpoint('../models/{}-{}.hdf5'.format(loc_name, model[1]), monitor='val_loss', verbose=0,
                                          save_best_only=True, mode='min')

    # stop training if the validation loss doesn't improve for 5 consecutive epochs.
    early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=10,
                                         verbose=0, mode='auto')

    callbacks_list = [save_best]
    model[0].fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1,
                 verbose=1, callbacks=callbacks_list)

    # 4) evaluate model
    print('Training RMSE: {:.5f}'.format(np.sqrt(model[0].evaluate(X_train, y_train, verbose=0))))
    print('Testing RMSE: {:.5f}\n'.format(np.sqrt(model[0].evaluate(X_test, y_test, verbose=0))))

# 5) predict
# see find.py