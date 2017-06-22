
from keras.models import load_model
from wifi_listener import *
import numpy as np
if __name__ == '__main__':
    model_path = '../models/model.h5'
    model = load_model(model_path)
    w = wifi_listener('wlp3s0')
    while True:
        data = w.get_data()[:5]
        packet = []
        for net in data:
            packet.append(net.split(' '))
        packet = np.expand_dims(np.array(packet), axis=0)
        print(model.predict([packet]))
