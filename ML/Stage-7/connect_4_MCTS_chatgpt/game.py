# game.py

import copy
import random

class ConnectFourGame:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[0] * cols for _ in range(rows)]
        self.current_player = 1  # Initialize current player

    def get_valid_moves(self):
        return [col for col in range(self.cols) if self.board[0][col] == 0]

    def make_move(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return True
        return False

    def check_win(self, player):
        # Check rows
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        # Check columns
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Check diagonals
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True
                if all(self.board[row + i][col + 3 - i] == player for i in range(4)):
                    return True

        return False

    def is_full(self):
        return all(self.board[0][col] != 0 for col in range(self.cols))
    
    def display(self):
        for row in self.board:
            print(row)
    
    def copy(self):
        return copy.deepcopy(self)

    def switch_player(self):
        self.current_player = -self.current_player

    def get_winner(self):
        if self.check_win(1):
            return 1
        elif self.check_win(-1):
            return -1
        else:
            return 0
