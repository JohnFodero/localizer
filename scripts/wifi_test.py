# basic wifi library useage
import wifi_listener as w
from time import sleep

wifi = w.wifi_listener('wlp3s0')
while True:    
    for network in wifi.get_data():
        print(network)
    print('----------------------------------')
    sleep(1)    
