import cv2
from math import floor

# Map origin is 

DISPLAY_SCALE = 0.5
KOBUKI_RADIUS_GLOBAL = 0.35 # in meters
# coversion factor from global scale in meters to local scale
X_SCALE = 0.01 # 1 unit = 0.01m = 1cm
Y_SCALE = 0.01 # Y_global_value (in meters) = Y_local_value (arbitrary) * Y_SCALE
# dimensions of map in meters
MAP_WIDTH_GLOBAL = 100
MAP_HEIGHT_GLOBAL = 200

class mapping():
	def __init__(self, path_to_map_img, path_to_bitmap):

		# read map png file
		self.map_img = cv2.imread(path_to_map_img, 0)
		# height and width of map in pixels
		self.map_width_pixel, self.map_height_pixel = self.map_img.shape[:2]
		# height and width of the display
		self.map_width_display = floor(self.map_width_pixel*DISPLAY_SCALE)
		self.map_height_display = floor(self.map_height_pixel*DISPLAY_SCALE)

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

	def display(self, mode):
		cv2.namedWindow('map', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('map', self.map_height_display, self.map_width_display)

		# mode 0 = only show map
		if(mode == 0):
			cv2.imshow('map', self.map_img)
		# mode 1 = map + bitmap
		
		# mode 2 = only bitmap


	def get_obstacle_bitmap(self):
		return self.bitmap

	def put_obstacle_bitmap(self, bitmap):
		self.bitmap = bitmap

	def close_map(self):
		cv2.waitKey(0)
		cv2.destroyAllWindows()


def main():
	M = mapping('maps/NEBfourthfloor.png', '')
	M.display(0)
	M.close_map()

if __name__ == '__main__':
	main()
