from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import keras
from keras.models import load_model

class ValueEstimator:
    def __init__(self,n_layers,input_dim,hidden_dim):
        self.n_layers = n_layers
        self.input_dim = input_dim
        try:
            fb = open('value_estimator_model.h5','rb')
            self.model = load_model('value_estimator_model.h5')
        except:
            self.model = Sequential()
            self.model.add(Dense(hidden_dim, input_dim=input_dim, activation='relu'))
            for i in range(n_layers-2):
                self.model.add(Dense(hidden_dim, input_dim=hidden_dim, activation='relu'))
            self.model.add(Dense(1, activation='tanh'))

    def make_prediction(self, input, player_turn):
        # turning input and player turn into network input:
        x = np.array(input)
        x=np.reshape(x,(1,42))
        out = self.model.predict(x)
        if player_turn == 1:
            return out
        else:
            return -out

        # x = np.array(input,player_turn)
        # print(x)
        # self.model.predict()

    def train(self,x_train,y_train,epochs=20):

        x_train=np.reshape(x_train,(-1,42))
        # xtrain=np.empty([42,1],dtype=np.array)
        # for item in x_train:
        #     temp=np.array(item)
        #     temp.reshape(42,1)
        #     xtrain=np.append(temp)
        # xtrain=xtrain[:,1:]
        self.model.compile(loss=keras.losses.mean_squared_error,optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True))
        self.model.fit(x_train,y_train,epochs=20,batch_size=x_train.shape[0])
    def save_model(self):
        self.model.save('value_estimator_model.h5')






