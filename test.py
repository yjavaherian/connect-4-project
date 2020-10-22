from game_engine import GameEngine, GameStatus
import random
import matplotlib.pyplot as plt

gm = GameEngine(6, 7)

gm.reset_game()

while gm.get_game_status() == GameStatus.IN_PROGRESS:
    gm.show_board()
    pa = gm.get_possible_actions()
    action = random.choice(pa)
    _, p = gm.get_game_state()
    gm.register_action(p, action)

gm.show_board()


