from keras.models import Sequential
from keras.layers import Dense

class ValueEstimator:
    def __init__(self,n_layers,input_dim,hidden_dim):
        self.n_layers=n_layers
        self.input_dim=input_dim
        self.model = Sequential()
        self.model.add(Dense(hidden_dim, input_dim=input_dim, activation='relu'))
        for i in range(n_layers-2):
            self.model.add(Dense(hidden_dim, input_dim=hidden_dim, activation='relu'))
        self.model.add(Dense(1, activation='tanh'))


    def make_prediction(self,input, player_turn):
        self.model.
