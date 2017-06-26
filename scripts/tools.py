# tools for wifi localizing
from time import sleep
import csv
import datetime
import numpy as np
import os

def capture_data(localizer, num_samples=1000, delay_sec=1):
    x = 1.
    y = 0.
    
    file_path = '../datasets/'
    file_name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M') + 'loc' + str(x) + str(y)
    
    mag = 'none'
    img = 'none'
    with open(file_path + file_name, 'wt') as f:
        wr = csv.writer(f, delimiter=',')
        for i in range(num_samples):
            master_list =[]
            # !!! use np.flatten instead !!!
            cells = localizer.wifi.get_wifi_cells(localizer.profile).flatten()
            wr.writerow([x, y, mag, img, *cells])
            print('sample ', i, end='\r')
            sleep(delay_sec)

def load_data_from_file(file_path):

    X_data = None
    y_data = None
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            x = float(row[0])
            y = float(row[1])
            mag = row[2]
            img = row[3]
            rssi = np.array(row[4::2])
            quality = np.array(row[5::2])
            cells = np.expand_dims(np.stack((rssi, quality), axis=-1), axis=0)
            y_val = np.expand_dims(np.array([x, y]), axis=0)
            if X_data is None:
                X_data = np.array(cells)
                y_data = np.array(y_val)
            else:
                X_data = np.concatenate((X_data, cells), axis=0)
                y_data = np.concatenate((y_data, y_val), axis=0)
    return X_data, y_data

def load_data_from_folder(folder_path):
    X = None
    y = None
    file_count = 0
    for file_name in os.listdir(folder_path):
        X_temp, y_temp = load_data_from_file(folder_path + '/' + file_name)
        if X is None:
            X = np.array(X_temp)
            y = np.array(y_temp)
        else:
            X = np.concatenate((X, X_temp))
            y = np.concatenate((y, y_temp))
        print('{} loaded'.format(file_name))
        file_count += 1
    print('Loaded {} files from {}'.format(file_count, folder_path))
    return X, y
