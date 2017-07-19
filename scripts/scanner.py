# wifi scanner

import os
if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.")

from wifi import Cell
import pickle
import os
import numpy as np
from subprocess import check_output

DEFAULT_RSSI = -100
DEFAULT_QUALITY = 0

class jetson_wifi_scanner():
    def __init__(self):
        self.sorted = True
        self.device = 'wlan0'
 
    def get_ap_group(self, ret_type='dict'):
        if ret_type != 'dict' and ret_type != 'list':
            print('ret_type {} invalid'.format(ret_type))
            return None
        ap_dict = {}
        ap_list_sorted = []
        ap_str = ''
        while ap_str == '':
            ap_str = check_output('sudo iw dev wlan0 scan | egrep "signal|^BSS" | sed -e "s/\\tsignal: \(-[0-9]\{2\}\).*/\\1/" -e "s/^BSS \([0-9a-z:]\{17\}\)(on wlan0).*/\\1/" | awk \'{ORS = (NR % 2 == 0)? "\\n" : " "; print}\'', shell=True).decode()

        ap_list = ap_str.splitlines()
        for ap in ap_list:
            address, rssi = ap.split(' ')
            mac_addr = str(int(address.replace(':', ''), base=16))
            ap_dict[mac_addr] = int(rssi)
            ap_list_sorted.append([mac_addr, int(rssi)])
        if ret_type == 'dict':
            return ap_dict
        elif ret_type == 'list':
            ap_list_sorted.sort(key=lambda x: x[1], reverse=True)
            return np.array(ap_list_sorted)
        

    def get_profiled_cells(self, profile=None):
        if profile is not None:
            ap_dict = self.get_ap_dict()
            rssi_list = []
            for address in profile:
                try:
                    rssi = ap_dict[str(address)]
                except KeyError:
                    rssi = -100
                rssi_list.append(rssi)
            return np.array(rssi_list)
        return None

class wifi_scanner():
    def __init__(self, device):
        self.device = device

    def make_cell_line(self, cell):
        mac_addr = str(int(cell.address.replace(':', ''), base=16))
        rssi = str(cell.signal)
        qual = cell.quality.split('/')
        quality = '{:0.0f}'.format(100*float(qual[0]) / float(qual[1]))

        return '{} {} {}'.format(mac_addr, rssi, quality)

    def parse_cell_line(self, cell):
        mac_addr, rssi, quality = cell.split(' ')
        return mac_addr, rssi, quality

    def get_wifi_cells(self, profile=None, item='both'):
        cells = None
        while cells is None:
            try:
                cells = Cell.all(self.device)
            except:
                pass
        cells = sorted([cell for cell in cells], 
                key=lambda x: int(x.signal), reverse=True)
        cells = [self.make_cell_line(cell) for cell in cells]
        cells = np.array(cells).flatten()
        if profile is None:
            #return np.array(cells)
            return cells
        else:
            profiled_cells = []
            for p_cell in profile:
                for cell in cells:
                    mac_addr, rssi, quality = self.parse_cell_line(cell)
                    if mac_addr == p_cell:
                        if item == 'rssi':
                            profiled_cells.append([int(rssi)])
                        elif item == 'quality':
                            profiled_cells.append([int(quality)])
                        else:
                            profiled_cells.append([int(rssi), int(quality)])
                        break
                else:
                    if item == 'rssi':
                        profiled_cells.append([int(DEFAULT_RSSI)])
                    elif item == 'quality':
                        profiled_cells.append([int(DEFAULT_QUALITY)])
                    else:
                        profiled_cells.append([int(DEFAULT_RSSI), int(DEFAULT_QUALITY)])
            return np.array(profiled_cells).flatten()

def main():
    scanner = jetson_wifi_scanner()
    print(scanner.get_ap_dict())

if __name__ == '__main__':
    main()
