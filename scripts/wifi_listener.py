# wifi control library
from wifi import Cell

class wifi_listener():
    def __init__(self, device):
        self.device = device

    def get_info(self):
        raw = []
        cells = Cell.all(adapter)
        return [cell for cell in cells].sort(key=lambda x: int(x.signal), reverse=True)

