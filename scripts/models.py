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


