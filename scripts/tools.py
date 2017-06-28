# tools for wifi localizing
from time import sleep
import csv
import datetime
import numpy as np
import os

def start_capture(file_name=None, file_path=None):
    if file_path is None:
        file_path = '../datasets/'
    if file_name is None:
        file_name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')
    f = open(file_path + file_name, 'wt')
    return f, csv.writer(f, delimiter=',')

def write_line(writer=None, localizer=None, x=0.0, y=0.0, mag_x=0.0, mag_y=0.0, mag_z=0.0, img1='na', img2='na'):
    if localizer is not None and writer is not None:
        cells = localizer.wifi.get_wifi_cells()
        writer.writerow([x, y, mag_x, mag_y, mag_z, img1, img2, *cells])

def stop_capture(file_obj):
    file_obj.close()


def capture(localizer, num_samples=1000, delay_sec=1):
    '''
    All-in-one method for capturing
    '''
    file_path = '../datasets/'
    file_name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M') + 'loc' + str(x) + str(y)
    x = 0.0
    y = 0.0
    mag_x = 0.
    mag_y = 0.
    mag_z = 0.
    img1 = 'none'
    img2 = 'none'
    with open(file_path + file_name, 'wt') as f:
        wr = csv.writer(f, delimiter=',')
        for i in range(num_samples):
            cells = localizer.wifi.get_wifi_cells()
            wr.writerow([x, y, mag_x, mag_y, mag_z, img1, img2, *cells])
            print('sample ', i, end='\r')
            sleep(delay_sec)


def load_data_from_file(file_path, profile=None):
    X_data = None
    y_data = None
    if profile is not None:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                X = float(row[0])
                y = float(row[1])
                mag_x, mag_y, mag_z = float(row[2]), float(row[3]), float(row[4])
                img1, img2 = row[5], row[6]
                cells = []
                count = 0
                for addr in profile:
                    for cell in row[7:]:
                        mac, rssi, quality = cell.split(' ')
                        if addr == mac:
                            cells.append(rssi)
                            cells.append(quality)
                            break
                    else:
                        cells.append(0)
                        cells.append(0)
                cells = np.expand_dims(np.array(cells), axis=0)
                y_val = np.expand_dims(np.array([X, y]), axis=0)
                if X_data is None:
                    X_data = cells
                    y_data = y_val
                else:
                    X_data = np.concatenate((X_data, cells), axis=0)
                    y_data = np.concatenate((y_data, y_val), axis=0)
    else:
        print('No profile provided.. returning empty')
    return X_data, y_data

def load_data_from_folder(folder_path, profile=None):
    X = None
    y = None
    file_count = 0
    if profile is not None:
        for file_name in os.listdir(folder_path):
            X_temp, y_temp = load_data_from_file(folder_path + '/' + file_name, profile)
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
