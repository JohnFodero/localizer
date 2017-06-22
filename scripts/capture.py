from wifi_listener import wifi_listener
from time import sleep
import datetime
import csv

num_samples = 1000
cells = 5
sample_delay_sec = 1

# to test localization
# location 0) John's desk
# location 1) Shiv's desk
location = 0
x_loc = 0
y_loc = 0

file_path = '../datasets/'
file_name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M') + 'loc' + str(location)
img_path = 'N/A'

wifi = wifi_listener('wlp3s0')

with open(file_path + file_name, 'wt') as csv_file:
    wr = csv.writer(csv_file, delimiter=',')
    for i in range(num_samples):
        wr.writerow([x_loc, y_loc, img_path, *wifi.get_cells()])
        print('sample ', i, end='\r')
        sleep(sample_delay_sec)
