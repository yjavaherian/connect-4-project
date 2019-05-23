from game_engine import GameStatus
from game_engine import GameEngine
from ai import AI
import pickle
import time
import numpy as np
import config

config.init()
ai1 = AI(1)
ai2 = AI(2, dont_use_nn=True)
game = GameEngine()
game.reset_game()
game.show_board()
# lets put two ais in front of each other:
while game.get_game_status() == GameStatus.IN_PROGRESS:
    board, player = game.get_game_state()
    if player == 1:
        action = ai1.select_action(board)
    else:
        action = ai2.select_action(board)
        # action = int(input("select a column to drop your block: "))
    game.register_action(player, action)
    print("player {} took action {}".format(player, action))
    game.show_board()
print("game state {}".format(game.get_game_status()))
# print("Consumed %sB memory" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
# ValueEstimator(5, 42, 10)
