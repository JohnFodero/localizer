# localizer

import os
from scanner import *
from tools import *
import numpy as np
import pickle


class localizer():
    def __init__(self, wifi):
        self.wifi = wifi
        self.profile_path = './network_profiles/'
        self.profile_name = None
        self.profile = None

    def __str__(self):
        print_str = '----------------------------------------'
        print_str += '\nLocalizer\nWifi Device: {}\n'.format(self.wifi.device)
        if self.profile_name is not None:
            print_str += 'Profile: {} Length: {}\nRouters:'.format(self.profile_name, len(self.profile))
            for router in self.profile:
                print_str += '\n    {}'.format(router)
        print_str += '\n----------------------------------------'
        return print_str

    def make_profile(self, profile_name, length=None):
        print('Creating new profile: {}'.format(profile_name))
        cells = self.wifi.get_wifi_cells()[:length]
        profile = []
        for cell in cells:
            mac_addr, rssi, quality = self.wifi.parse_cell_line(cell)
            profile.append(mac_addr)
        with open(self.profile_path + profile_name + '.p', 'wb') as f:
            pickle.dump(profile, f)
        self.profile = profile
        self.profile_name = profile_name

    def load_profile(self, profile_name):
        if os.path.isfile(self.profile_path + profile_name + '.p'):
            with open(self.profile_path + profile_name + '.p', 'rb') as f:
                self.profile = pickle.load(f)
                self.profile_name = profile_name
                print('Loaded profile: {}'.format(profile_name))
        else:
            self.make_profile(profile_name=profile_name)

    def add_cells_to_profile(self, profile_name, num_add=5):
        if os.path.isfile(self.profile_path + profile_name + '.p'):
            with open(self.profile_path + profile_name + '.p', 'rb') as f:
                profile = pickle.load(f)
                cells = self.wifi.get_wifi_cells()
                count = num_add
                for cell in cells:
                    mac_addr, rssi, quality = self.wifi.parse_cell_line(cell)
                    if mac_addr not in profile:
                        profile.append(mac_addr)
                        num_add -= 1
                    if num_add <= 0:
                        break
            with open(self.profile_path + profile_name + '.p', 'wb') as f:
                pickle.dump(profile, f)
            self.profile = profile
        else:
            print('{}: Is not a valid profile name.'.format(profile_name))

    def train_model(self):
        pass

    def predict_xy(self):
        pass

