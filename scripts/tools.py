# tools for wifi localizing
from time import sleep
import csv
import datetime
import numpy as np
import os
import cv2
import math
import json

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

def split_dataset(X):
    cutoff_train = int(0.8 * len(X))
    cutoff_val = cutoff_train + int(0.1 * len(X))
    return X[:cutoff_train], X[cutoff_train:cutoff_val], X[cutoff_val:]

def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # resize 224 x 224 x 3
    image = cv2.resize(image, (224, 224))
    image = image.astype('float32')
    image /= 255.
    return image

def scale_rssi(rssi):
    return (rssi + 100) * (1./70.)
def classify_rssi(rssi):
    return classified
def scale_xy(xy):
    
    return (xy -10.1) * (1./(59.8-10.1))
def classify_xy(xy):
    
    return classified
def load_data(path, profile=None, classify=False, randomize=True):
    wifi = []
    mag = []
    img = []
    xy = []
    coordinates = []
    file_count = 0
    if profile is not None:
        for file_name in os.listdir(path):
            if os.path.isfile(path + file_name):
                print('-- loading from {}'.format(file_name))
                file_coords = []
                with open(path + file_name, 'r') as f:
                    data = json.load(f)
                    show = True
                    points = 0
                    print('-- -- Length', len(data['datapoints']))
                    for point in data['datapoints']:
                        points += 1
                        x = float(point['x'])
                        y = float(point['y'])
                        xy.append([x, y])
                        if (x, y) not in file_coords:
                            file_coords.append((x, y))

                        img1 = cv2.imread(point['img1'])
                        try:
                            img1 = preprocess_image(img1)
                        except:
                            print(points)
                            print(point['img1'])
                            return
                        img.append(img1)
                        if classify:
                            mag.append([int(point['heading']/90) / 4.])
                            wifi_row = []
                            for addr in profile:
                                try:
                                    wifi_row.append(int(10*scale_rssi(float(point['access_points'][addr]))/2.5)/4.)
                                except:
                                    wifi_row.append(int(10*scale_rssi(float(-100.))/2.5)/4.)

                        else:
                            mag.append([point['heading']/360.])
                            wifi_row = []
                            for addr in profile:
                                try:
                                    wifi_row.append(scale_rssi(float(point['access_points'][addr])))
                                except:
                                    wifi_row.append(scale_rssi(-100.0))
                        wifi.append(wifi_row)
                coordinates.append(file_coords)
                print('-- -- Added {} datapoints'.format(points))
                file_count += 1
        print('Loaded {} files from {}'.format(file_count, path))
        xy = scale_xy(np.array(xy))
        
        #assert
        if randomize:
            p = np.random.permutation(len(wifi))
            wifi, mag, img, xy = np.array(wifi)[p], np.array(mag)[p], np.float32(img)[p], xy[p]
            
        return wifi, mag, img, xy, coordinates