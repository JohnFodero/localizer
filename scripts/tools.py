# tools for wifi localizing
from time import sleep
import csv
import datetime
import re

match_pattern = '[\'(.*)\' \'(.*)\']'
def capture_data(localizer, num_samples=100, delay_sec=1):
    x = 0.
    y = 0.
    
    file_path = '../datasets/'
    file_name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M') + 'loc' + str(x) + str(y)
    
    mag = 'none'
    img = 'none'
    with open(file_path + file_name, 'wt') as f:
        wr = csv.writer(f, delimiter=',')
        for i in range(num_samples):
            master_list =[]
            for item in localizer.wifi.get_wifi_cells(localizer.profile):
                for point in item:
                    master_list.append(point)
            wr.writerow([x, y, mag, img, master_list])
            print('sample ', i, end='\r')
            sleep(delay_sec)

def load_data(file_path):

    X_data = None
    y_data = None
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            x = float(row[0])
            y = float(row[1])
            mag = row[2]
            img = row[3]
            cells = []
            for cell in row[4:]:
                pass                
            print(cells)
    return X_data, y_data
    
