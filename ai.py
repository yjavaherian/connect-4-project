import numpy as np
from game_engine import GameModel
from game_engine import GameStatus
import time
import collections
import config

epsilon = 1 / 1000
exploration_constant = 2
move_time_limit = 0.3


class AI:
    def __init__(self, player_number, board_height=6, board_width=7):
        # simple version of monte carlo tree search
        self.player_number = player_number
        self.model = GameModel(board_height, board_width)
        self.root = None
        return

    def select_action(self, board):
        tick = time.time()
        itr = 0
        if self.root is None or self.root.find_next_root(board) is None:
            # we need to create the root.
            self.root = Node(self.player_number, [x[:] for x in board], None, self.model, self.player_number, parent=DummyNode())
        else:
            self.root = self.root.find_next_root(board)

        # while itr < move_itr_limit:
        while (time.time() - tick) < move_time_limit:
            itr += 1
            # doing the loop
            leaf = self.root.select_leaf()
            if leaf.number_visits == 0 or leaf.is_endgame:
                value_estimate = config.nn.make_prediction(leaf.board, leaf.player_turn)
                # end_game_status = self.model.play_random_rollout(leaf.player_turn, leaf.board)
                # if end_game_status == GameStatus.DRAW:
                #     value_estimate = 0
                # elif end_game_status == GameStatus.WINED_BY_P1 and self.player_number == 1:
                #     value_estimate = +1
                # elif end_game_status == GameStatus.WINED_BY_P1 and self.player_number == 2:
                #     value_estimate = -1
                # elif end_game_status == GameStatus.WINED_BY_P2 and self.player_number == 1:
                #     value_estimate = -1
                # elif end_game_status == GameStatus.WINED_BY_P2 and self.player_number == 2:
                #     value_estimate = +1
                leaf.backup(value_estimate)
            else:
                leaf.is_expanded = True
        print("{} iterations of the algorithm was done!".format(itr))
        print("ai {} root arrays:\nhchild to action map :{}\nchild total values:{}\nchild visit number:{}".
              format(self.player_number, self.root.list_of_actions, self.root.child_total_value, self.root.child_number_visits))
        return self.root.list_of_actions[np.argmax(self.root.child_number_visits)]


class DummyNode:
    def __init__(self):
        self.parent = None
        self.child_total_value = collections.defaultdict(float)
        self.child_number_visits = collections.defaultdict(float)


class Node:
    def __init__(self, player_turn, board, move, model, our_player_number, parent=None):
        self.player_turn = player_turn
        self.our_player_number = our_player_number
        self.model = model
        self.board = board
        self.is_endgame = False
        if model._get_game_status(board) != GameStatus.IN_PROGRESS:
            self.is_endgame = True
        self.move = move
        self.is_expanded = False
        self.parent = parent
        self.children = {}
        self.list_of_actions = model.get_possible_actions(board)
        self.number_of_children = len(self.list_of_actions)
        self.child_total_value = np.zeros(shape=self.number_of_children, dtype=np.float32)
        self.child_number_visits = np.zeros(shape=self.number_of_children, dtype=np.float32)

    @property
    def number_visits(self):
        return self.parent.child_number_visits[self.move]

    @number_visits.setter
    def number_visits(self, value):
        self.parent.child_number_visits[self.move] = value

    @property
    def total_value(self):
        return self.parent.child_total_value[self.move]

    @total_value.setter
    def total_value(self, value):
        self.parent.child_total_value[self.move] = value

    def find_next_root(self, board):
        if np.argmax(self.child_number_visits) not in self.children:
            return None
        parent_node = self.children[np.argmax(self.child_number_visits)]
        for node in parent_node.children.values():
            if node.board == board:
                return node
        return None

    def best_child(self):
        UCB = self.child_total_value / (self.child_number_visits + epsilon) + exploration_constant * np.sqrt(np.log(self.number_visits) /(epsilon + self.child_number_visits))
        return np.argmax(UCB)

    def select_leaf(self):
        current = self
        while current.is_expanded and not current.is_endgame:
            best_child = current.best_child()
            # best_move = current.list_of_actions[best_child]
            current = current.maybe_add_child(best_child)
        return current

    def maybe_add_child(self, move):
        if move not in self.children:
            next_player_turn, next_board = self.model.get_next_state(self.board, self.player_turn, self.list_of_actions[move])
            self.children[move] = Node(next_player_turn, next_board, move, self.model, self.our_player_number, parent=self)
        return self.children[move]

    def backup(self, value_estimate: float):
        current = self
        while current.parent is not None:
            current.number_visits += 1
            if current.player_turn == current.our_player_number:
                current.total_value -= value_estimate
            else:
                current.total_value += value_estimate
            current = current.parent