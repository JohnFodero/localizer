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