from keras.layers import Dense, Flatten, Dropout
from keras.models import Sequential
import numpy as np
import csv
import re
from wifi_listener import *
from tools import *
import h5py
import os

def get_xy(model, wifi_obj):
    x = 0.0
    y = 0.0
    cells = wifi_obj.get_cells()
    profiled_cells = wifi_obj.profile_cells(cells)
    #print(model.predict(profiled_cells))

    return x, y


if __name__ == '__main__':
    wifi = wifi_listener('wlp3s0')
    wifi.make_profile(num_cells=20)
    profile_length = len(wifi.profile)
    print('profile length: ', profile_length)
    
    # --- load data ---
    X, y = load_data_from_folder('../datasets')
    print('X: ', X.shape)
    print('Y: ', y.shape)

     # randomize the array
#    we may not want to do this...
#    p = np.random.permutation(len(X))
#    X, y = X[p], y[p]

    ttsplit = int(0.9 * X.shape[0])
    X_train, X_test = X[:ttsplit], X[ttsplit: ]
    y_train, y_test = y[:ttsplit], y[ttsplit: ]
    
    shape_str = '{:10s} | {:15s} | {:15s}'
    print(shape_str.format('', 'X shape', 'y shape'))
    print(shape_str.format('TRAIN', str(X_train.shape), str(y_train.shape)))
    print(shape_str.format('TEST', str(X_test.shape), str(y_test.shape)))
    print(shape_str.format('TOTAL', str(X.shape), str(y.shape)))

    # --- build model ---
    model = Sequential()
    model.add(Dense(24, input_shape=(profile_length, 2), activation='relu'))
#    model.add(Dropout(0.2))
    model.add(Dense(24, activation='relu'))
#    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(2, activation='softmax'))
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    model.fit(X_train, y_train, epochs=10, batch_size=32)
    score = model.evaluate(X_test, y_test, batch_size = 128)
    print(model.metrics_names)
    print(score)
    print(model.predict(X_test))
    
    model.save('../models/model.h5')
    print('model saved.')

    wifi.get_profiled_frame()
