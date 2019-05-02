from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
import random


class GameStatus(Enum):
    IN_PROGRESS = 0
    WINED_BY_P1 = 1
    WINED_BY_P2 = 2
    DRAW = 3


class GameModel:
    def __init__(self, board_height=6, board_width=7):
        self.board_height = board_height
        self.board_width = board_width

    def get_next_state(self, board, player, column_to_drop):
        new_board = [x[:] for x in board]
        if player == 1:
            player_turn = 2
        else:
            player_turn = 1
        for i in range(self.board_height):
            if new_board[self.board_height - i - 1][column_to_drop] == 0:
                # this is where the dice falls
                new_board[self.board_height - i - 1][column_to_drop] = player
                break
        return player_turn, new_board

    def play_random_rollout(self, player_turn, board):
        temp_board = [x[:] for x in board]
        temp_player_turn = player_turn
        game_status = self._get_game_status(temp_board)
        while game_status == GameStatus.IN_PROGRESS:
            actions = self.get_possible_actions(temp_board)
            action = random.choice(actions)
            temp_player_turn, temp_board = self.get_next_state(temp_board, temp_player_turn, action)
            game_status = self._get_game_status(temp_board)
        # returning final game status
        return game_status

    def _get_game_status(self, board):
        # can be implemented better
        is_board_full = True
        for i in range(self.board_height):
            for j in range(self.board_width):
                if board[i][j] == 1:
                    if self._check_for_line(board, i, j, 1) is True:
                        return GameStatus.WINED_BY_P1
                elif board[i][j] == 2:
                    if self._check_for_line(board, i, j, 2) is True:
                        return GameStatus.WINED_BY_P2
                elif board[i][j] == 0:
                    is_board_full = False
        if is_board_full is True:
            return GameStatus.DRAW
        else:
            return GameStatus.IN_PROGRESS

    def _check_for_line(self, board, i, j, player):
        # checking horizontal line
        if (j + 3) < self.board_width:
            if board[i][j + 1] == player and board[i][j + 2] == player and board[i][j + 3] == player:
                return True

        # checking vertical line:
        if (i + 3) < self.board_height:
            if board[i + 1][j] == player and board[i + 2][j] == player and board[i + 3][j] == player:
                return True

        # checking diagonal right:
        if (j + 3) < self.board_width and (i + 3) < self.board_height:
            if board[i + 1][j + 1] == player and board[i + 2][j + 2] == player and board[i + 3][j + 3] == player:
                return True

        # checking diagonal left:
        if (j - 3) >= 0 and (i + 3) < self.board_height:
            if board[i + 1][j - 1] == player and board[i + 2][j - 2] == player and board[i + 3][j - 3] == player:
                return True
        return False

    def get_possible_actions(self, board):
        actions = []
        for i in range(self.board_width):
            if board[0][i] == 0:
                actions.append(i)
        return actions


class GameEngine:
    def __init__(self, board_height=6, board_width=7):
        self.player_turn = 1
        self.board_height = board_height
        self.board_width = board_width
        self.board = []
        for i in range(board_height):
            row = []
            for j in range(board_width):
                row.append(0)
            self.board.append(row)

    def register_action(self, player, column_to_drop):
        assert player == self.player_turn, "It's not your turn to register an action ;( "

        if player == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1
        for i in range(self.board_height):
            if self.board[self.board_height - i - 1][column_to_drop] == 0:
                # this is where the dice falls
                self.board[self.board_height - i - 1][column_to_drop] = player
                return
        raise Exception("Invalid Action!")

    def reset_game(self):
        self.player_turn = 1
        for i in range(self.board_height):
            for j in range(self.board_width):
                self.board[i][j] = 0

    def get_game_status(self):
        is_board_full = True
        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.board[i][j] == 1:
                    if self._check_for_line(i, j, 1) is True:
                        return GameStatus.WINED_BY_P1
                elif self.board[i][j] == 2:
                    if self._check_for_line(i, j, 2) is True:
                        return GameStatus.WINED_BY_P2
                elif self.board[i][j] == 0:
                    is_board_full = False
        if is_board_full is True:
            return GameStatus.DRAW
        else:
            return GameStatus.IN_PROGRESS

    def _check_for_line(self, i, j, player):
        # checking horizontal line
        if (j + 3) < self.board_width:
            if self.board[i][j+1] == player and self.board[i][j+2] == player and self.board[i][j+3] == player:
                return True

        # checking vertical line:
        if (i + 3) < self.board_height:
            if self.board[i+1][j] == player and self.board[i+2][j] == player and self.board[i+3][j] == player:
                return True

        # checking diagonal right:
        if (j + 3) < self.board_width and (i + 3) < self.board_height:
            if self.board[i+1][j+1] == player and self.board[i+2][j+2] == player and self.board[i+3][j+3] == player:
                return True

        # checking diagonal left:
        if (j - 3) >= 0 and (i + 3) < self.board_height:
            if self.board[i+1][j-1] == player and self.board[i+2][j-2] == player and self.board[i+3][j-3] == player:
                return True
        return False

    def get_possible_actions(self):
        actions = []
        for i in range(self.board_width):
            if self.board[0][i] == 0:
                actions.append(i)
        return actions

    def get_game_state(self):
        player_turn = self.player_turn
        export_board = [x[:] for x in self.board]
        return export_board, player_turn

    def show_board(self):
        plt.matshow(np.array(self.board))
        plt.show()

