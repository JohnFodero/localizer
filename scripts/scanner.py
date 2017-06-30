# wifi scanner

import os
if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.")

from wifi import Cell
import pickle
import os
import numpy as np

DEFAULT_RSSI = -100
DEFAULT_QUALITY = 0

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

    def get_wifi_cells(self, profile=None):
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
                        profiled_cells.append([int(rssi), int(quality)])
                        break
                else:
                     profiled_cells.append([DEFAULT_RSSI, DEFAULT_QUALITY])
            return np.array(profiled_cells).flatten()

