from keras.models import Sequential
from keras.layers import Dense

class ValueEstimator:
    def __init__(self,n_layers,input_dim):
        self.n_layers=n_layers
        self.input_dim=input_dim
        self.model = Sequential()
        for i in range(n_layers):
            self.model.add(Dense(, input_dim=8, activation='relu'))

        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))
