from keras.layers import Dense, Dropout, Flatten, Activation
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
        model.add(Activation('softmax'))

        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        return model
        


