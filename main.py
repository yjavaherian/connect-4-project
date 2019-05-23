from game_engine import GameStatus
from game_engine import GameEngine
from ai import AI
import pickle
import time
import numpy as np
import config

config.init()
# import resource
# creating an NN for now
#nn = ValueEstimator(2, 42, 50)
#
running_train_time = 60
train_start_time = time.time()
# creating a new game and two ais:
ai1 = AI(1)
ai2 = AI(2)
game = GameEngine()
# loading database from pickle file
try:
    new_file = open("database_dump.pkl", "rb")
    database = pickle.load(new_file)
    new_file.close()
except:
    database = []
    new_file = open("database_dump.pkl","wb")
    pickle.dump(database, new_file)
    new_file.close()

batch=[]
while time.time() - train_start_time < running_train_time:
    game.reset_game()
    batch.clear()
    while game.get_game_status() == GameStatus.IN_PROGRESS:
        board, player = game.get_game_state()
        batch.append(board)
        if player == 1:
            action = ai1.select_action(board)
        else:
            action = ai2.select_action(board)
        game.register_action(player, action)
    # we now have a complete history of a game between two ais:
    # we now update the database:
    game_value = 0
    if game.get_game_status() is GameStatus.WINED_BY_P1:
        game_value = 1
    elif game.get_game_status() is GameStatus.WINED_BY_P2:
        game_value = -1
    # for state in batch:
    #     database.index()
    #     database.setdefault(np.array(state), np.zeros(2))
    #     database[np.array(state)][0] += game_value
    #     database[np.array(state)][1] += 1
    # informing the result to the NN:
    # new idea lets pass the whole database:
    X_train = np.array(batch)
    y_train = np.full(X_train.shape[0], game_value)
    config.nn.train(X_train, y_train)
# updating the database file :
pickle.dump(database, open("database_dump.pkl", "wb"))
config.nn.save_model()
# print("Consumed %sB memory" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
# ValueEstimator(5, 42, 10)
