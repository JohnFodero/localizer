import smbus
import time
import math

class magnetometer():
    # register addresses
    CFGAAddress = 0
    CFGBAddress = 1
    MODEAddress = 2
    XAddressMSB = 3
    XAddressLSB = 4
    YAddressMSB = 7
    YAddressLSB = 8
    ZAddressMSB = 5
    ZAddressLSB = 6
    
    
    def __init__(self, port=0, address=0x1E, declination=(0,0)):
        self.bus = smbus.SMBus(port)
        self.address = address
        
        self.declination = (declination[0] + declination[1] / 60) * (math.pi / 180)
        
        # set samples to 15Hz and avg every 8 samples
        self.bus.write_byte_data(self.address, self.CFGAAddress, 0b01110000)
        
        # set gain to 230
        self.bus.write_byte_data(self.address, self.CFGBAddress, 0b11111111)
        
        # put in continuous mode
        self.bus.write_byte_data(self.address, self.MODEAddress, 0b00000000)
        time.sleep(.1)
        # read values to update gain setting
        self.get_xyz()
        
    def get_axis_reading(self, MSB_addr, LSB_addr):
        high = self.bus.read_byte_data(self.address, MSB_addr)
        low = self.bus.read_byte_data(self.address, LSB_addr)
        value = (high << 8) + low
        # twos complement
        if value >= 0x8000:
            return -((int(0xFFFF) - value) + 1)
        else:
            return value
    
    def get_xyz(self):
        x = self.get_axis_reading(self.XAddressMSB, self.XAddressLSB) - (33 - 1.5 + 2)
        y = self.get_axis_reading(self.YAddressMSB, self.YAddressLSB) - (-38 + 7.5 - 3)
        z = self.get_axis_reading(self.ZAddressMSB, self.ZAddressLSB)
        return x, y, z
    
    def get_heading(self):
        x, y, z = self.get_xyz()
        heading = math.atan2(y, x)
        heading += self.declination
        if heading > math.pi * 2:
            heading -= math.pi * 2
        elif heading < 0:
            heading += math.pi * 2
        # convert to degrees
        return heading * 180 / math.pi
        

def main():
    # http://www.magnetic-declination.com/
    mag = magnetometer(port=1, address=0x1E, declination=(-5,53))
    minx, miny = 1000, 1000
    maxx, maxy = 0, 0
    while True:
        x, y, z = mag.get_xyz()
        '''
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
        print(minx, miny, maxx, maxy)
        '''
        print(x, y, z)
        print(mag.get_heading())
        
        time.sleep(1)

if __name__ == '__main__':
    main()