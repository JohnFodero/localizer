from keras.layers import *
from keras.models import Sequential, load_model

class BaseModel(object):
    def __init__(self, input_shape=None, output_shape=None):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.model = self.build_model()
    
    def build_model(self):
        return self.model

class WifiOnly(BaseModel):
    '''
    A testing model to characterize wifi-only localization
    '''

    def build_model(self):
        model = Sequential()
        model.add(Dense(256, input_shape=self.input_shape))
        model.add(Activation('relu'))
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dense(32))
        model.add(Activation('relu'))
        model.add(Dense(self.output_shape))
        model.add(Activation('sigmoid'))

        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        return model
        
class WifiOnlyXY(BaseModel):
    '''
    A testing model to characterize wifi-only localization
    '''

    def build_model(self):
        model = Sequential()
        model.add(Dense(256, input_shape=self.input_shape, kernel_initializer='he_normal'))
        model.add(Activation('relu'))
#        model.add(Dropout(0.5))
        model.add(Dense(64, kernel_initializer='he_normal'))
        model.add(Activation('relu'))
        model.add(Dense(32, kernel_initializer='he_normal'))
        model.add(Activation('relu'))
        model.add(Dense(self.output_shape, kernel_initializer='he_normal'))
        model.add(Activation('linear'))

        model.compile(optimizer='rmsprop', loss='mse')
        return model

class Conv1D_WifiOnly(BaseModel):

    def build_model(self):
        model = Sequential()

        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        return model

class LSTM(BaseModel):
    '''
    LSTM Model
    '''
    def build_model(self):
        model = Sequential()
        return model

class TriInput(BaseModel):
    def __init__(self, wifi_input_shape, mag_input_shape, img_input_shape):
        self.wifi_input_shape = wifi_input_shape
        self.mag_input_shape = mag_input_shape
        self.img_input_shape = img_input_shape
        self.model = self.build_model()

    def build_model(self):

        # branch1: wifi
        branch1 = Sequential()
        branch1.add(Dense(256, input_shape=self.wifi_input_shape))
        branch1.add(Activation('relu'))
        branch1.add(Dense(128))
        branch1.add(Activation('relu'))
        branch1.add(Dense(32))
        branch1.add(Activation('relu'))
        branch1.add(BatchNormalization)
        # branch2: mag
        branch2 = Sequential()
        branch2.add(Dense(16, input_shape=self.mag_input_shape))
        branch2.add(Activation('relu'))
        branch2.add(Dense(4))
        branch2.add(Activation('relu'))
        branch2.add(BatchNormalization)
        # branch3: img
        branch3 = Sequential()
        branch3.add(Convolution2D(32, 3, 3, (3, 3), input_shape=self.img_input_shape))
        branch3.add(Activation('relu'))
        #branch3.add(MaxPooling2D(pool_size=(2, 2)))
        branch3.add(Convolution2D(16, 2, 2, (1, 1)))
        branch3.add(Activation('relu'))
        #branch3.add(MaxPooling2D(pool_size=(2, 2)))
        branch3.add(BatchNormalization)

        # merge branches
        model = Sequential()
        model.add(Merge([branch1, branch2, branch3], mode='concat'))
        model.add(Dense(2, activation='linear'))
        model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

        #model.fit([wifi, mag, img])
        return model

