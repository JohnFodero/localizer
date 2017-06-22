from keras.layers import Dense, Flatten, Dropout
from keras.models import Sequential
import numpy as np
import csv
import re
from wifi_listener import *
import h5py
import os
def load_data(file_name):
    raw_X = []
    location = int(file_name[-1])
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cells = []
            for net in wifi.profile_cells(row[1:]):
                data = net.split(' ')
                cells.append([data[1], data[2]])
            raw_X.append(cells)
    raw_X = np.array(raw_X)
    raw_y = np.zeros((raw_X.shape[0], 2))
    raw_y[:, location] = 1

    return np.array(raw_X), raw_y

if __name__ == '__main__':
    wifi = wifi_listener('wlp3s0')
    wifi.load_profile()
    print('profile length: ', len(wifi.profile))
    X = np.array([])
    y = np.array([])
    for file_name in os.listdir('../datasets'):
        X_temp, y_temp = load_data('../datasets/' + file_name)
        X.concatenate(np.array(X_temp))
        y.concatenate(np.array(y_temp))
        print('{} loaded'.format(file_name))
    
    p = np.random.permutation(len(X))
    X, y = X[p], y[p]
    shape_str = '{:10s} | {:10s} | {:10s}'
    
    ttsplit = int(0.9 * X.shape[0])
    X_train, X_test = X[:ttsplit], X[ttsplit: ]
    y_train, y_test = y[:ttsplit], y[ttsplit: ]
    print(shape_str.format('', 'X shape', 'y shape'))
    print(shape_str.foramat('TRAIN', str(X_train.shape), str(y_train.shape)))
    print(shape_str.format('TEST', str(X_test.shape), str(y_test.shape)))
    print(shape_Str.format('TOTAL', str(X.shape), str(y.shape)))

    # --- build model ---
    model = Sequential()
    model.add(Dense(24, input_shape=(5, 3), activation='relu'))
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
