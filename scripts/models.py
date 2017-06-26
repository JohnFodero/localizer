from keras.layers import Dense, Dropout, Flatten, Activation
from keras.models import Sequential, load_model

class BaseModel(object):
    def __init__(self):
        pass
    
    def build_model(self):
        return self.model

class aModel(BaseModel):
        
    def build_model(self, input_shape):
        model = Sequential()
        model.add(Flatten(input_shape=input_shape))
        model.add(Dense(100))
        model.add(Activation('relu'))
        model.add(Dense(1))
        model.add(Activation('softmax'))

        model.compile(optimizer='adam', loss='mse')
        self.model = model
        return self.model

class bModel(BaseModel):
    
    def build_model(self, input_shape):
        model = Sequential()
        model.add(Dense(100, input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(1))
        model.add(Activation('softmax'))
        
        model.compile(optimizer='adam', loss='mse')
        self.model = model
        return self.model

