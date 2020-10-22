from game_engine import GameStatus
from game_engine import GameEngine
from ai import AI
import pickle

# creating a new game and two ais:
ai1 = AI(1, dont_use_nn=True)
ai2 = AI(2, dont_use_nn=True)
game = GameEngine()
# game.show_board()
# lets put two ais in front of each other:
T = 0
database = {}
batch = []
while T < 50000:
    game.reset_game()
    batch.clear()
    while game.get_game_status() == GameStatus.IN_PROGRESS:
        T += 1
        board, player = game.get_game_state()
        batch.append(board)
        if player == 1:
            action = ai1.select_action(board)
        else:
            # action = ai2.select_action(board)
            action = int(input("select a column to drop your block: "))
        game.register_action(player, action)
        print("player {} took action {}".format(player, action))
        game.show_board()
    print("game state {}".format(game.get_game_status()))
    print("game took {} number of steps".format(T))
    for board in batch:
        database.setdefault(board, 0)
        database[board][0] += 1
        if game.get_game_state() == GameStatus.WINED_BY_P1:
            database[board][1] += 1
        elif game.get_game_state() == GameStatus.WINED_BY_P2:
            database[board][1] -= 1

file = open("boards.pickle", "wb")
pickle.dump(database, file)
file.close()

    #####################################
    # print("Took %s sec to run %s times" % (tock - tick, num_reads))
    # import resource
    # print("Consumed %sB memory" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)