# tools for wifi localizing
from time import sleep
import csv
import datetime
import numpy as np
import os
import cv2
import math

DEFAULT_RSSI = -100.
DEFAULT_QUALITY = 0.

def rotate_about_center(src, angle, scale=1.):
    w = src.shape[1]
    h = src.shape[0]
    rangle = np.deg2rad(angle)  # angle in radians
    # now calculate new image width and height
    nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
    nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    return cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)

def scale_inputs(X, imin=-100, imax=-30, omin=0., omax=1.):
    X[X == 0.] = -100
    X[X < -100] = -100
    X[X > -30] = -30
    return (X - imin) * ((omax - omin) / (imax - imin)) + omin

def scale_single(x, imin=-100, imax=-30, omin=0., omax=1.):
    if x == 0:
        x = -100
    elif x < -100:
        x = -100
    elif x > -30:
        x = -30
    return (x - imin) * ((omax - omin) / (imax - imin)) + omin


def start_capture(file_name=None, file_path=None):
    if file_path is None:
        file_path = '../datasets/'
    if file_name is None:
        file_name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')
    f = open(file_path + file_name, 'wt')
    return f, csv.writer(f, delimiter=',')

def write_line(writer=None, localizer=None, x=0.0, y=0.0, mag_x=0.0, mag_y=0.0, mag_z=0.0, img1='na', img2='na'):
    if localizer is not None and writer is not None:
        cells = localizer.wifi.get_ap_group('list')
        mod_cells = []
        for row in cells:
            mod_cells.append(row[0] + ' ' + str(row[1]))
        #writer.writerow([x, y, mag_x, mag_y, mag_z, img1, img2, *mod_cells])
        writer.writerow([x, y, mag_x, mag_y, mag_z, img1, img2, mod_cells[:]])

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
            #wr.writerow([x, y, mag_x, mag_y, mag_z, img1, img2, *cells])
            wr.writerow([x, y, mag_x, mag_y, mag_z, img1, img2, cells[:]])
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
                for i, addr in enumerate(profile):
                    for cell in row[7:]:
                        mac, rssi, quality = cell.split(' ')
                        if addr == mac:
                            cells.append(scale_single(float(rssi)))
                            cells.append(float(quality)/100.)
                            break
                    else:
                        cells.append(scale_single(DEFAULT_RSSI))
                        cells.append(DEFAULT_QUALITY/100.)
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

def load_data_from_folder(folder_path, profile=None, train_test_split=0.8, keep_percent=1.0, item='both'):
    X = None
    y = None
    file_count = 0
    if profile is not None:
        for file_name in os.listdir(folder_path):
            X_temp, y_temp = load_data_from_file(folder_path + '/' + file_name, profile, keep_percent=keep_percent)
            if X is None:
                X = np.array(X_temp)
                y = np.array(y_temp)
            else:
                X = np.concatenate((X, X_temp))
                y = np.concatenate((y, y_temp))
            print('{} loaded'.format(file_name))
            file_count += 1
        print('Loaded {} files from {}'.format(file_count, folder_path))


    np.random.seed(7)
    p = np.random.permutation(len(X))
    X, y = X[p], y[p]
    if item == 'rssi':
        X = X[:,::2]
        X = scale_inputs(X)
    elif item == 'quality':
        X = X[:,1::2]
        X /= 100.

    split = int(train_test_split * X.shape[0])
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    return X_train, y_train, X_test, y_test
