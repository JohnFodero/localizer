import cv2
from math import floor
import numpy as np
from time import sleep

# Map origin is top left corner

DISPLAY_SCALE = 0.5
KOBUKI_DIAMETER_GLOBAL = 0.35 # in meters

# dimensions of map in meters
MAP_WIDTH_GLOBAL = 72.2475
MAP_HEIGHT_GLOBAL = 54.1775

class mapping():
    def __init__(self, path_to_map_img, path_to_bitmap):

        # read map png file
        self.map_img = cv2.imread(path_to_map_img, 1)
        # height and width of map in pixels
        self.map_height_pixel, self.map_width_pixel = self.map_img.shape[:2]
        # height and width of the display
        self.map_width_display = floor(self.map_width_pixel*DISPLAY_SCALE)
        self.map_height_display = floor(self.map_height_pixel*DISPLAY_SCALE)

        # scale conversion from global units to local units
        self.x_scale = MAP_WIDTH_GLOBAL / (self.map_width_pixel) # 1 local unit = 1 pixel
        self.y_scale = MAP_HEIGHT_GLOBAL / (self.map_height_pixel) # Y_global_value (in meters) = Y_local_value (arbitrary) * self.y_scale

        # kobuki scale for drawing
        self.kobuki_scale = 2

        # Kobuki diameter in local scale
        self.kobuki_radius_local = floor(((KOBUKI_DIAMETER_GLOBAL/2)*self.kobuki_scale) / self.x_scale)

        # read obstacle bitmap
        self.bitmap = cv2.imread(path_to_bitmap, 0)
    
        # position of robot in pixels
        self.X = 0
        self.Y = 0

	# position of robot in global coordinates
        self.X_global = self.X * self.x_scale
        self.Y_global = self.Y * self.y_scale

        # kobuki scale for drawing
        self.kobuki_scale = 2

    # Update the robot's location
    def put_location(self, x, y):
        if(x>=self.map_width_pixel):
            print("X coordinate exceeds max dimension")
            x = self.map_width_pixel - 1
        elif(x<0):
            print("X coordinate exceeds min dimension")
            x = 0

        if(y>=self.map_height_pixel):
            print("Y coordinate exceeds max dimension")
            y = self.map_height_pixel - 1
        elif(y<0):
            print("Y coordinate exceeds min dimension")
            y = 0

        self.X = x
        self.Y = y

        self.X_global = self.X * self.x_scale
        self.Y_global = self.Y * self.y_scale

    def put_location_global(self, x_global, y_global):
        if(x_global>MAP_WIDTH_GLOBAL):
            print("X_global coordinate exceeds max dimension")
            x_global = MAP_WIDTH_GLOBAL
        elif(x_global<0):
            print("X_global coordinate exceeds min dimension")
            x_global = 0

        if(y_global>=MAP_HEIGHT_GLOBAL):
            print("Y_global coordinate exceeds max dimension")
            y_global = MAP_HEIGHT_GLOBAL
        elif(y_global<0):
            print("Y_global coordinate exceeds min dimension")
            y_global = 0

        self.X_global = x_global
        self.Y_global = y_global

        self.X = floor(self.X_global / self.x_scale)
        self.Y = floor(self.Y_global / self.y_scale)

    # return the robots current location
    def get_location(self):
        print('Press <s> to confirm location')
        while cv2.waitKey(1) != ord('s'):
            pass
        return self.X, self.Y

    def get_location_global(self):
        print('Press <s> to confirm location')
        while cv2.waitKey(1) != ord('s'):
            pass
        return self.X_global, self.Y_global

    def initialize_display(self):
        cv2.namedWindow('map', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('map', self.map_width_display, self.map_height_display)
        cv2.setMouseCallback("map", self.click_and_update)
        self.update_display(0)

    def update_display(self, mode):
        # mode 0 = only show map
        if(mode == 0):
            cv2.imshow('map', self.map_img)
        # mode 1 = map + kobuki
        if(mode == 1):
            cv2.imshow('map', self.map_img_kobuki)
        # mode 2 = only bitmap

        cv2.waitKey(50)
    
    def draw_kobuki(self, x, y):
        self.map_img_kobuki = self.map_img.copy()
        cv2.circle(self.map_img_kobuki, (x, y), self.kobuki_radius_local, (255,0,0), -1)

    def get_obstacle_bitmap(self):
        return self.bitmap

    def put_obstacle_bitmap(self, bitmap):
        self.bitmap = bitmap

    def update_kobuki(self, x, y):
        self.put_location(x,y)
        self.draw_kobuki(x,y)
        self.update_display(1)

    def remove_kobuki(self):
        self.update_display(0)

    def click_and_update(self, event, x, y, flags, param):
        if(event==cv2.EVENT_LBUTTONDBLCLK):
            self.update_kobuki(x,y)

            print("x: ", x, " y: ", y)
            print("x(m): ", self.X_global, "y(m): ", self.Y_global)

        elif(event==cv2.EVENT_RBUTTONDBLCLK):
            print("x: ", x, " y: ", y)
            print("x(m): ", x*self.x_scale, "y(m): ", y*self.y_scale)

    def close_display(self):
        #cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    M = mapping('maps/NEBfourthfloor.png', 'maps/obstacle_bitmap.bmp')
    M.initialize_display()
    M.update_kobuki(200,200)
    coords = [[(10,10), (20, 20), (30, 30)], [(40, 40), (50, 50)]]
    M.close_display()

if __name__ == '__main__':
    main()
