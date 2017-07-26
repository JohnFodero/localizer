import smbus
import time
import math
import pickle

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
        self.calibration = [0, 0]
        self.declination = (declination[0] +(declination[1] / 60)) * (math.pi / 180)
        # set samples to 15Hz and avg every 8 samples
        self.bus.write_byte_data(self.address, self.CFGAAddress, 0b01110000)
        
        # set gain
        self.bus.write_byte_data(self.address, self.CFGBAddress, 0b00100000)
        
        # put in continuous mode
        self.bus.write_byte_data(self.address, self.MODEAddress, 0b00000000)
        time.sleep(.1)
        # read values to update gain setting
        self.get_xyz()
        # load claibration
        try:
            with open('./mag_calibrations/mag_calibration.p', 'rb') as f:
                self.calibration = pickle.load(f)
                print('Loaded calibration: ', self.calibration[0], self.calibration[1])
        except:
            print('Using default calibration values')
        
    def get_axis_reading(self, MSB_addr, LSB_addr):
        high = self.bus.read_byte_data(self.address, MSB_addr)
        low = self.bus.read_byte_data(self.address, LSB_addr)
        value = (high << 8) + low
        # twos complement
        if value >= 0x8000:
            return -((65535 - value) + 1)
        else:
            return value
    
    def get_xyz(self, scaled=True):
        scale = 0.92
        x = self.get_axis_reading(self.XAddressMSB, self.XAddressLSB) - self.calibration[0]
        y = self.get_axis_reading(self.YAddressMSB, self.YAddressLSB) - self.calibration[1]
        z = self.get_axis_reading(self.ZAddressMSB, self.ZAddressLSB)
        if scaled:
            x *= scale
            y *= scale
            z *= scale
        return x, y, z
    
    def get_heading(self):
        x, y, z = self.get_xyz()
        heading = math.atan2(y, x)
        heading += self.declination
        if heading < 0:
            heading += math.pi * 2
        # convert to degrees
        return math.degrees(heading)
        

def main():
    # http://www.magnetic-declination.com/
    mag = magnetometer(port=1, address=0x1E, declination=(-5,53))
    while True:
        x, y, z = mag.get_xyz()
#        print('X: {:3.4f} Y: {:3.4f} Z: {:3.4f}'.format(x, y, z))
        print('Heading: ', mag.get_heading())
        
        time.sleep(.1)

if __name__ == '__main__':
    main()
