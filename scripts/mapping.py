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

<<<<<<< HEAD
class Mapping():
	def __init__(self, path_to_map_img, path_to_bitmap):

		# read map png file
		self.map_img = cv2.imread(path_to_map_img, 1)
		# height and width of map in pixels
		self.map_width_pixel, self.map_height_pixel = self.map_img.shape[:2]
		# height and width of the display
		self.map_width_display = floor(self.map_width_pixel*DISPLAY_SCALE)
		self.map_height_display = floor(self.map_height_pixel*DISPLAY_SCALE)

		# scale conversion from global units to local units
		self.x_scale = MAP_WIDTH_GLOBAL / self.map_width_pixel # 1 local unit = 1 pixel
		self.y_scale = MAP_HEIGHT_GLOBAL / self.map_height_pixel # Y_global_value (in meters) = Y_local_value (arbitrary) * Y_SCALE

		# Kobuki diameter in local scale
		self.kobuki_radius_local = floor((KOBUKI_DIAMETER_GLOBAL/2) / self.x_scale)

		# read obstacle bitmap
		self.bitmap = cv2.imread(path_to_bitmap, 0)
	
		# position of robot
		self.X = 0
		self.Y = 0

	# Update the robot's location
	def put_location(self, x, y):
		self.X = x
		self.Y = y

	# return the robots current location
	def get_location(self):
		return self.X, self.Y

	def initialize_display(self):
		cv2.namedWindow('map', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('map', self.map_height_display, self.map_width_display)
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

		cv2.waitKey(30)
	
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
			self.X = x
			self.Y = y
			print("LOCAL-> x: ", x, " y: ", y, " GLOBAL-> x: ", x*self.x_scale, " y: ", y*self.y_scale)
			self.update_kobuki(x,y)

		elif(event==cv2.EVENT_RBUTTONDBLCLK):
			print("LOCAL-> x: ", x, " y: ", y, " GLOBAL-> x: ", x*self.x_scale, " y: ", y*self.y_scale)

	def close_display(self):
		cv2.waitKey(0)
		cv2.destroyAllWindows()
=======
class mapping():
    def __init__(self, path_to_map_img, path_to_bitmap):

        # read map png file
        self.map_img = cv2.imread(path_to_map_img, 1)
        # height and width of map in pixels
        self.map_width_pixel, self.map_height_pixel = self.map_img.shape[:2]
        # height and width of the display
        self.map_width_display = floor(self.map_width_pixel*DISPLAY_SCALE)
        self.map_height_display = floor(self.map_height_pixel*DISPLAY_SCALE)

        # scale conversion from global units to local units
        self.x_scale = MAP_WIDTH_GLOBAL / self.map_width_pixel # 1 local unit = 1 pixel
        self.y_scale = MAP_HEIGHT_GLOBAL / self.map_height_pixel # Y_global_value (in meters) = Y_local_value (arbitrary) * Y_SCALE

        # Kobuki diameter in local scale
        self.kobuki_radius_local = floor((KOBUKI_DIAMETER_GLOBAL/2) / self.x_scale)

        # read obstacle bitmap
        self.bitmap = cv2.imread(path_to_bitmap, 0)
    
        # position of robot
        self.X = 0
        self.Y = 0

    # Update the robot's location
    def put_location(self, x, y):
        self.X = x
        self.Y = y

    # return the robots current location
    def get_location(self):
        print('Press <s> to confirm location')
        while cv2.waitKey(1) != ord('s'):
            pass
        return self.X, self.Y

    def initiate_display(self):
        cv2.namedWindow('map', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('map', self.map_height_display, self.map_width_display)
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
            self.X = x
            self.Y = y
            print("x: ", x, " y: ", y)
            self.update_kobuki(x,y)

        elif(event==cv2.EVENT_RBUTTONDBLCLK):
            print("x: ", x, " y: ", y)

    #def update_kobuki_with_click(self):

    def get_click_location(self):
        return

    def close_display(self):
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
>>>>>>> upstream/kobuki



def main():
<<<<<<< HEAD
	M = Mapping('maps/NEBfourthfloor.png', 'maps/obstacle_bitmap.bmp')
	M.initialize_display()
	M.update_kobuki(200,200)
	#M.update_kobuki_with_click()
	M.close_display()
=======
    M = mapping('maps/NEBfourthfloor.png', 'maps/obstacle_bitmap.bmp')
    M.initiate_display()
    M.update_kobuki(200,200)
    M.close_display()
>>>>>>> upstream/kobuki

if __name__ == '__main__':
    main()
