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
import threading
import json

class capture():
    DRIVE_TIME = 9.16
    DRIVE_TIME_CAL = 1.83
    FORWARD_SPEED = 100
    PIVOT_SPEED = 50
    MIN_SPEED = 40
    def __init__(self):
        self.loc = localizer(jetson_wifi_scanner())
        self.location = '4th Floor NEB'
        self.file_name = location.replace(' ', '_') + '-' + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M') + '.json'
        self.cam1 = cv2.VideoCapture(1)
        self.cam2 = cv2.VideoCapture(2)
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

        self.mag = magnetometer(port=1, address=0x1E, declination=(-5,53))

        self.frames_per_location = 20     # samples per location
        self.interval = 0.25               # seconds per sample
    '''
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
    def pivot_worker(self, speed, direction):
        while self.count < self.frames_per_location:
            self.kob.move(speed, direction)
        print('Thread ended')
        return
    '''
    def save_data(self, data):
        with open(self.file_name, 'w') as f:
            json.dump(self.data, f)
            print('Data saved')
        return
    
    def drive_capture(self):
        x_start = int(input('Enter start x: '))
        y_start = int(input('Enter starty y: '))
        x_delta = int(input('Enter distance per move in x: '))
        y_delta = int(input('Enter distance per move in y: '))
        x = x_start
        y = y_start
        data = {}
        data['location'] = self.location
        data['datapoints'] = []
        while True:
            for i in range(4):
                # collect data points
                pivot_direction = -1 + (2 * (i % 2)) 
                start_heading = self.mag.get_heading()
                self.count = 0
                start_time = time() 
                t = threading.Thread(target=self.pivot_worker, args=(self.PIVOT_SPEED, pivot_direction))
                t.daemon = True
                t.start()
                while self.count < self.frames_per_location:
                    self.kob.move(speed=self.PIVOT_SPEED, radius=pivot_direction)
                    if time() - start_time > self.interval:
                        name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
                        path1 = self.path + name + '_cam1.jpg'
                        path2 = self.path + name + '_cam2.jpg'
                        s1, img1 = self.cam1.retrieve(f1)
                        s2, img2 = self.cam2.retrieve(f1)
                        heading = self.mag.get_heading()
                        if s1 and s2:
                            img1 = rotate_about_center(img1, 180)
                            cv2.imwrite(path1, img1)
                            cv2.imwrite(path2, img2)
                            print('sample ', self.count, 'Heading: ', heading)
                            data['datapoints'].append({})
                            data['datapoints'][-1]['x'] = x
                            data['datapoints'][-1]['y'] = y
                            data['datapoints'][-1]['heading'] = heading
                            data['datapoints'][-1]['img1'] = path1
                            data['datapoints'][-1]['img2'] = path2
                            data['datapoints'][-1]['access_points'] = self.loc.get_ap_group(ret_type='dict')
                            self.count += 1
                            start_time = time()
                        else:
                            print('Camera error - Retrying')
                    f1 = self.cam1.grab()
                    f2 = self.cam2.grab()
                while t.isAlive():
                    pass
                print('Finished collecting, recentering...')
                while abs(self.mag.get_heading() - start_heading) > 1:
                    self.kob.move(speed=max(self.PIVOT_SPEED-20, self.MIN_SPEED), radius=pivot_direction)
                self.kob.stop()
                sleep(1)
                start_time = time()
                while time() - start_time < self.DRIVE_TIME + self.DRIVE_TIME_CAL:
                    self.kob.move(speed=self.FORWARD_SPEED, radius=0)
                self.kob.stop()
                sleep(1)
                
                x += x_delta
                y += y_delta
            # write json to file as a backup
            self.save_data(data)
            input(Re-center the bot.\nPress any key to begin')

            
    def shutdown(self):
        self.save_data()
        self.kob.deinitialize()
        self.cam1.release()
        self.cam2.release()
        #m.close_display()

def main():
    cap = capture()
    try:
        cap.drive_capture()
    except KeyboardInterrupt:
        cap.shutdown()
        sys.exit()
        
if __name__ == '__main__':
    main()
