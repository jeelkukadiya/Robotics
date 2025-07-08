import numpy as np
import pandas as pd
from IPython.display import display

class connect_x:

    def __init__(self):
        self.board_height = 3
        self.board_width = 5
        self.board_state = np.zeros([self.board_height, self.board_width], dtype=np.int8)
        self.players = {'p1': 1, 'p2': 2}
        self.isDone = False
        self.reward = {'win': 1, 'draw': 0.5, 'lose': -1}
    
    def render(self):
        rendered_board_state = self.board_state.copy().astype(str)
        rendered_board_state[self.board_state == 0] = ' '
        rendered_board_state[self.board_state == 1] = 'O'
        rendered_board_state[self.board_state == 2] = 'X'
        display(pd.DataFrame(rendered_board_state))
    
    def reset(self):
        self.__init__()
        
    def get_available_actions(self):
        available_cols = []
        for j in range(self.board_width):
            if np.sum([self.board_state[:, j] == 0]) != 0:
                available_cols.append(j)
        return available_cols
    
    def check_win(self):
        return False
    
    def check_game_done(self, player):
        #self.isDone = False

        if self.check_win():
            self.isDone=True
        elif self.get_available_actions() == []:
            self.isDone=True
        else:
            self.isDone=False

        """if player == 'p1':
            check = '1 1 1 1'
        else:
            check = '2 2 2 2'
        
        # check vertically then horizontally
        for j in range(self.board_width):
            if check in np.array_str(self.board_state[:, j]):
                self.isDone = True
        for i in range(self.board_height):
            if check in np.array_str(self.board_state[i, :]):
                self.isDone = True
        
        # check left diagonal and right diagonal
        for k in range(0, self.board_height - 4 + 1):
            left_diagonal = np.array([self.board_state[k + d, d] for d in \
                            range(min(self.board_height - k, min(self.board_height, self.board_width)))])
            right_diagonal = np.array([self.board_state[d + k, self.board_width - d - 1] for d in \
                            range(min(self.board_height - k, min(self.board_height, self.board_width)))])
            if check in np.array_str(left_diagonal) or check in np.array_str(right_diagonal):
                self.isDone = True
        for k in range(1, self.board_width - 4 + 1):
            left_diagonal = np.array([self.board_state[d, d + k] for d in \
                            range(min(self.board_width - k, min(self.board_height, self.board_width)))])
            right_diagonal = np.array([self.board_state[d, self.board_width - 1 - k - d] for d in \
                            range(min(self.board_width - k, min(self.board_height, self.board_width)))])
            if check in np.array_str(left_diagonal) or check in np.array_str(right_diagonal):
                self.isDone = True"""
        
        if self.isDone:
            return self.reward['win']
        # check for draw
        elif np.sum([self.board_state == 0]) == 0:
            self.isDone = True
            return self.reward['draw']
        else:
            return 0.
        
    def make_move(self, a, player):
        # check if move is valid
        if a in self.get_available_actions():
            i = np.sum([self.board_state[:, a] == 0]) - 1
            self.board_state[i, a] = self.players[player]
        else:
            print('Move is invalid')
            self.render()

        reward = self.check_game_done(player)
        
        # give feedback as new state and reward
        return self.board_state.copy(), reward


env = connect_x()
env.make_move(2,'p1')
env.make_move(2,'p1')
env.make_move(2,'p1')
env.render()
x=env.get_available_actions()
print(x)
