from scanner import *
from localizer import *
from tools import *
from mapping import *
from kobuki import *
from magnetometer import *
import numpy as np
from time import *
import datetime
import cv2
import sys

class capture():
    def __init__(self):
        self.loc = localizer(jetson_wifi_scanner())

        self.cam1 = cv2.VideoCapture(1)
        self.cam2 = cv2.VideoCapture(2)
        self.path='../datasets/images/'
        while not self.cam1.isOpened() and not self.cam2.isOpened():
            print('waiting for cameras to open...')
            sleep(1)

        self.kob = kobuki('/dev/ttyUSB0')
        self.kob.initialize()

        '''
        m = mapping('maps/NEBfourthfloor.png', 'maps/obstacle_bitmap.bmp')
        m.initialize_display()
        m.update_kobuki(200,200)
        print('mapping started')
        '''

        self.f, self.wr = start_capture()

        self.mag = magnetometer(port=1, address=0x1E, declination=(-5,53))

        self.frames_per_location = 50   # samples per location
        self.interval = 0.5               # seconds per sample
    
    def rotate_capture(self):
        while True:
            x = input("enter x location: ")
            y = input("enter y location: ")
        #    x, y = m.get_location()
            print('Collecting at :', x, y)

            count = 0
            start_time = time()
            while count < self.frames_per_location:
                self.kob.drive(thr=1, steer=0)
                if time() - start_time > self.interval:
                    heading = self.mag.get_heading()
                    name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
                    path1 = self.path + name + '_cam1.jpg'
                    path2 = self.path + name + '_cam2.jpg'
                    s1, img1 = self.cam1.retrieve(f1)
                    s2, img2 = self.cam2.retrieve(f1)
                    if s1 and s2:
                        img1 = rotate_about_center(img1, 180)
                        cv2.imwrite(path1, img1)
                        cv2.imwrite(path2, img2)
                        write_line(self.wr, self.loc, x, y, mag_x=heading, mag_y=0.0, mag_z=0.0, img1=path1, img2=path2)
                        print('sample ', count, 'Heading: ', heading)
                        count += 1
                        start_time = time()
                f1 = self.cam1.grab()
                f2 = self.cam2.grab()

            # stop kobuki
            self.kob.stop()
            
    def shutdown(self):
        self.kob.deinitialize()
        stop_capture(self.f)
        self.cam1.release()
        self.cam2.release()
        #m.close_display()

def main():
    cap = capture()
    try:
        cap.rotate_capture()
    except KeyboardInterrupt:
        cap.shutdown()
        sys.exit()
        
if __name__ == '__main__':
    main()
