from game_engine import GameStatus
from game_engine import GameEngine
from ai import AI
import pickle

# creating a new game and two ais:
ai1 = AI(1)
ai2 = AI(2)
game = GameEngine()
# game.show_board()
# lets put two ais in front of each other:
T = 0
fb = open("jhwy.txt", "rb")
with open("jhwy.txt", "rb") as fp:
    q = pickle.load(fp)

database = q
print(database)
batch=[]
batch2=[]
while T < 50:
    game.reset_game()
    batch.clear()
    while game.get_game_status() == GameStatus.IN_PROGRESS:
        T += 1
        board, player = game.get_game_state()
        if player == 1:
            action = ai1.select_action(board)
            batch.append(board)
        else:
            action = ai2.select_action(board)
            batch2.append(board)
        game.register_action(player, action)
    print("game took {} number of steps".format(T))

    for bj in batch :
         if bj in database:
             y = database.index(bj)
             num = database[y + 2]
             database[y + 2] += 1
             if game.get_game_status() == GameStatus.WINED_BY_P1:
                 database[y + 1] = (num * database[y + 1]) +1
                 database[y + 1] = database[y + 1] / database[y + 2]
             elif game.get_game_status() == GameStatus.WINED_BY_P2:
                 database[y + 1] = (num * database[y + 1]) - 1
                 database[y + 1] = database[y + 1] / database[y + 2]
             elif game.get_game_status() == GameStatus.DRAW :
                 database[y + 1] = (num * database[y + 1])
                 database[y + 1] = database[y + 1] / database[y + 2]
         else:
             database.append(bj)
             database.append(0)
             database.append(1)

             y = database.index(bj)

             if game.get_game_status() == GameStatus.WINED_BY_P1:
                 database[y+1] += 1
             elif game.get_game_status() == GameStatus.WINED_BY_P2:
                 database[y+1] -= 1
    for bj in batch2:
        if bj in database:
            y = database.index(bj)
            num = database[y + 2]
            database[y + 2] += 1
            if game.get_game_status() == GameStatus.WINED_BY_P2:
                database[y + 1] = (num * database[y + 1]) + 1
                database[y + 1] = database[y + 1] / database[y + 2]
            elif game.get_game_status() == GameStatus.WINED_BY_P2:
                database[y + 1] = (num * database[y + 1]) - 1
                database[y + 1] = database[y + 1] / database[y + 2]
            elif game.get_game_status() == GameStatus.DRAW:
                database[y + 1] = (num * database[y + 1])
                database[y + 1] = database[y + 1] / database[y + 2]
        else:
            database.append(bj)
            database.append(0)
            database.append(1)

            y = database.index(bj)

            if game.get_game_status() == GameStatus.WINED_BY_P2:
                database[y + 1] += 1
            elif game.get_game_status() == GameStatus.WINED_BY_P1:
                database[y + 1] -= 1
print(database)

# #
# p
with open("jhwy.txt","wb") as fp:
    pickle.dump(database,fp)




    #####################################
    # print("Took %s sec to run %s times" % (tock - tick, num_reads))
    # import resource
    # print("Consumed %sB memory" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
