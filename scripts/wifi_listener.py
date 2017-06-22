# wifi control library

import os
if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.")
from wifi import Cell
import pickle
import os
class wifi_listener():
    def __init__(self, device):
        self.device = device
        self.profile = None
        self.profile_dir = './network_profiles'

    def process_cell(self, cell):
        # mac address
        mac_address = str(int(cell.address.replace(':', ''), base=16))
        # rssi
        rssi = str(cell.signal)
        # quality
        qual = cell.quality.split('/')
        quality = '{:0.0f}'.format(100*float(qual[0]) / float(qual[1]))
        return mac_address + ' ' + rssi + ' ' + quality

    def get_all(self):
        raw = []
        cells = None
        while cells is None:
            try:
                cells = Cell.all(self.device)
            except:
                pass
        # returns a sorted list of cells sorted by RSSI
        return sorted([cell for cell in cells], key=lambda x: int(x.signal), reverse=True)  
    
    def get_cells(self):
        cell_list = []
        items = self.get_all()
        for item in items:
            # returns a list of strings formatted with the mac addresses (as an integer), rssi, and quality (delimited by spaces)
            cell_list.append(self.process_cell(item))
        return cell_list


    def make_profile(self, num_cells=10, profile_name='default'):
        # a profile is a list of a given length of the strongest networks in the area to be scanned
        print('make profile')
        # scan networks
        # take top num_cells strongest networks
        cells = self.get_cells()[:num_cells]
        # make a list
        profile = []
        for cell in cells:
            mac_addr, rssi, quality = cell.split(' ')
            profile.append(mac_addr)
        # pickle the list
        pickle.dump(profile, open(self.profile_dir + '/' + profile_name + '.p', 'wb'))
        # set the active profile to that profile
        self.profile = profile

    def load_profile(self, profile_name='default'):
        if os.path.isfile('./network_profiles/' + profile_name + '.p'):
            self.profile = pickle.load(open(self.profile_dir + '/' + profile_name + '.p', 'rb'))
            print('loaded {} profile'.format(profile_name))
        else:
            self.make_profile()
    
    def append_profile(self, num_cells=10, profile_name='default'):
        # adds new cells to the profile
        new_profile = self.profile
        cells = self.get_cells()[:num_cells]
        new_cells = 0
        for cell in cells:
            mac_addr, rssi, quality  = cell.split(' ')
            if mac_addr not in self.profile:
                new_profile.append(mac_addr)
                new_cells += 1
        self.profile = new_profile
        pickle.dump(new_profile, open(self.profile_dir + '/' + profile_name + '.p', 'wb'))
        print('added {} new cells to the {} profile'.format(new_cells, profile_name))

    def profile_cells(self, cells_in):
        # input: a list of cells
        # output: a list of cells *only* described by the profile, in the order of the profile
        cells_out = []
        if self.profile is not None:
            for cell_name in self.profile:
                for i, cell in enumerate(cells_in):
                    mac_addr, rssi, profile = cell.split(' ')
                    if cell_name == mac_addr:
                        cells_out.append(cells_in[i])
                        break
                else:
                    # if the profile cell is not in the dataset
                    # set default values
                    print('{} cell not found.. appending default out-of-range values'.format(cell_name))
                    cells_out.append(cell_name + ' -100 0')
        return cells_out

