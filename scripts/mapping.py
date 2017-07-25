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

        # define BGR colorspace dictionary
        self.color_space = {"RED" : (0,0,255), "LIME" : (0,255,0), "BLUE" : (255,0,0), "YELLOW" : (0,255,255), "CYAN" : (255,255,0), "MAGENTA" : (255,0,255), "MAROON" : (0,0,128), "OLIVE" : (0,128,128), "GREEN" : (0,128,0), "PURPLE" : (128,0,128), "TEAL" : (128,128,0), "NAVY" : (128,0,0)}

        # only BGR colors
        self.colors = ((0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,255,0), (255,0,255), (0,0,128), (0,128,128), (0,128,0), (128,0,128), (128,128,0), (128,0,0))

    # Update the robot's location in pixels
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

    # Update the robot's location in meters
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

    # return the robot's current location in pixels
    def get_location(self):
        print('Press <s> to confirm location')
        while cv2.waitKey(1) != ord('s'):
            pass
        return self.X, self.Y

    # return the robot's current location in meters
    def get_location_global(self):
        print('Press <s> to confirm location')
        while cv2.waitKey(1) != ord('s'):
            pass
        return self.X_global, self.Y_global

    # initialize the display
    def initialize_display(self):
        cv2.namedWindow('map', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('map', self.map_width_display, self.map_height_display)
        cv2.setMouseCallback("map", self.click_and_update)
        self.__update_display(0)

    # internal function to update display
    def __update_display(self, mode):
        # mode 0 = only show map
        if(mode == 0):
            cv2.imshow('map', self.map_img)
        # mode 1 = map + kobuki
        if(mode == 1):
            cv2.imshow('map', self.map_img_kobuki)
        # mode 2 = map + kobuki history
        if(mode == 2):
            cv2.imshow('map', self.map_img_kobuki_history)

        cv2.waitKey(50)
    
    # internal function to draw the kobuki's circle
    def __draw_kobuki(self, x, y, color):
        self.map_img_kobuki = self.map_img.copy()
        cv2.circle(self.map_img_kobuki, (x, y), self.kobuki_radius_local, color, -1)

    # internal function to draw multiple kobukis
    def __draw_kobuki_history(self, x, y, color=(0,0,255)):
        cv2.circle(self.map_img_kobuki_history, (x, y), self.kobuki_radius_local, color, -1)

    # get the obstacle bitmap
    def get_obstacle_bitmap(self):
        return self.bitmap

    # change the obstacle bitmap
    def put_obstacle_bitmap(self, bitmap):
        self.bitmap = bitmap

    # change the kobuki's display scale, default is 2
    def put_kobuki_scale(self, scale):
        # kobuki scale for drawing
        self.kobuki_scale = scale

        # Kobuki diameter in local scale
        self.kobuki_radius_local = floor(((KOBUKI_DIAMETER_GLOBAL/2)*self.kobuki_scale) / self.x_scale)

    # update the display with kobuki's new location and color (look at self.color_space dicitonary for color options)
    def update_kobuki(self, x, y, color = (0,0,255)):
        self.put_location(x,y)
        self.__draw_kobuki(x,y,color)
        self.__update_display(1)

    # plot the history of kobuki's oath using a list of lists. Colors will be cycled through self.colors
    def plot_path(self, coords):
        c = 0
        self.map_img_kobuki_history = self.map_img.copy()
        for i in range(len(coords)):
            for j in coords[i]:
                self.__draw_kobuki_history(j[0], j[1] , self.colors[c])
            c = c+1
            if(c==len(self.colors)):
                c = 0
        self.__update_display(2)

    # clear display
    def remove_kobuki(self):
        self.__update_display(0)

    # internal funtion for mouse click updates
    def click_and_update(self, event, x, y, flags, param):
        if(event==cv2.EVENT_LBUTTONDBLCLK):
            self.update_kobuki(x,y)

            print("x: ", x, " y: ", y)
            print("x(m): ", self.X_global, "y(m): ", self.Y_global)

        elif(event==cv2.EVENT_RBUTTONDBLCLK):
            print("x: ", x, " y: ", y)
            print("x(m): ", x*self.x_scale, "y(m): ", y*self.y_scale)

    # close display
    def close_display(self):
        #cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    M = mapping('maps/NEBfourthfloor.png', 'maps/obstacle_bitmap.bmp')
    M.initialize_display()
    M.update_kobuki(200,200)
    coords = [[(10,10), (20, 20), (30, 30)], [(40, 40), (50, 50)], [(60,60)], [(70,70)], [(80,80)], [(90,90)], [(100,100)], [(110,110)], [(120,120), (190, 190), (200, 200), (210, 210), (220, 220)], [(130,130)], [(140,140)], [(150,150)], [(160,160)], [(170,170)], [(180,10)]]
    M.plot_path(coords)
    M.close_display()

if __name__ == '__main__':
    main()
