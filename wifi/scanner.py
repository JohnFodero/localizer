from wifi import Cell
from time import sleep

while True:
    cells = Cell.all('wlp3s0')
    wifilist = [cell for cell in cells]
    wifilist.sort(key=lambda x: int(x.signal), reverse=True)
    print(len(wifilist))
    print([net.ssid for net in wifilist[:3]])
    print([net.quality for net in wifilist[:3]])
    print([net.signal for net in wifilist[:3]])

    sleep(1)
