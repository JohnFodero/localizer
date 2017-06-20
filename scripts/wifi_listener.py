# wifi control library

import os
if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.")
from wifi import Cell
from decimal import Decimal


class wifi_listener():
    def __init__(self, device):
        self.device = device

    def get_all(self):
        raw = []
        cells = Cell.all(self.device)
        # returns a sorted list of cells sorted by RSSI
        return sorted([cell for cell in cells], key=lambda x: int(x.signal), reverse=True)  
    
    def get_data(self):
        cell_list = []
        items = self.get_all()
        for item in items:
            qual = item.quality.split('/')
            # returns a list of (MAC address, RSSI (dB), quality (%)) tuples
            cell_list.append((item.address, int(item.signal), int('{:3.0f}'.format(100*float(qual[0])/float(qual[1]))) ))
        return cell_list
