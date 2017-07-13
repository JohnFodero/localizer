from keras.layers import *
from keras.models import Sequential, load_model
from keras.regularizers import *
from keras.optimizers import *
from keras.constraints import *

class BaseModel(object):
    def __init__(self, input_shape=None, output_shape=None):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.model = self.build_model()
    
    def build_model(self):
        return self.model

        
class WifiOnlyXY(BaseModel):
    '''
    A testing model to characterize wifi-only localization
    '''

    def build_model(self):
        model = Sequential()
        model.add(Dense(256, kernel_initializer='he_normal', input_shape=self.input_shape))
        model.add(Activation('relu'))
        model.add(Dense(512, kernel_initializer='he_normal'))
        model.add(Activation('relu'))
        model.add(Dense(256, kernel_initializer='he_normal'))
        model.add(Activation('relu'))
        model.add(Dense(self.output_shape, kernel_initializer='he_normal'))
        model.add(Activation('linear'))

        model.compile(optimizer='rmsprop', loss='mse')
        return model

class RegWifiOnlyXY(BaseModel):
    '''
    A testing model to characterize wifi-only localization
    Based on the 'Dropout' paper
    Test:
        MaxoutDense keras layer?
        Max Norm Regularization Constraint c ~= 3-4
        Size (Am I making this too big? too small?)
        RMSProp learning rate 10x - 100x

    '''

    def build_model(self):
        model = Sequential()
        model.add(Dropout(0.2, input_shape=(self.input_shape)))
        model.add(Dense(256, kernel_initializer='he_normal', activity_regularizer=l2(0.01), kernel_constraint=max_norm(3.)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(512, kernel_initializer='he_normal', activity_regularizer=l2(0.01), kernel_constraint=max_norm(3.)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(256, kernel_initializer='he_normal', activity_regularizer=l2(0.01), kernel_constraint=max_norm(3.)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.output_shape, kernel_initializer='he_normal'))
        model.add(Activation('linear'))

        model.compile(optimizer=RMSprop(lr=0.0001), loss='mse')
        return model

class SDAWifiOnlyXY(BaseModel):
    '''
    SDA implementation
    '''

    def build_model(self):
        model = Sequential()
        model.add(Dense(128, input_shape=self.input_shape, kernel_initializer='he_normal'))
        model.add(Activation('relu'))
        model.add(Dense(self.output_shape, kernel_initializer='he_normal'))
        model.add(Activation('linear'))

        model.compile(optimizer='adam', loss='mse')
        return model


class MinimalWifiOnlyXY(BaseModel):
    '''
    A testing model to characterize wifi-only localization
    '''

    def build_model(self):
        model = Sequential()
        model.add(Dense(128, input_shape=self.input_shape, kernel_initializer='he_normal'))
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

