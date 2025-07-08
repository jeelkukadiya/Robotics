import numpy as np

class WinStackEnvironment:
    def __init__(self, num_stacks=5, stack_height=3, num_o_balls=12, num_x_balls=12):
        self.num_stacks = num_stacks
        self.stack_height = stack_height
        self.num_o_balls = num_o_balls
        self.num_x_balls = num_x_balls
        self.current_player = None
        self.board = np.zeros((num_stacks, stack_height), dtype=np.int)  # 0 represents an empty space

    def reset(self):
        self.board = np.zeros((self.num_stacks, self.stack_height), dtype=np.int)
        self.num_o_balls = 12
        self.num_x_balls = 12
        self.current_player = np.random.choice(['O', 'X'])
        return self.get_state()

    def get_state(self):
        # Represent the state of the board as a flat array
        return self.board.flatten()

    def is_valid_move(self, stack_idx):
        # Check if the selected stack is not full
        return self.board[stack_idx][-1] == 0

    def make_move(self, stack_idx):
        if self.is_valid_move(stack_idx):
            ball_type = 'O' if self.current_player == 'O' else 'X'
            for i in range(self.stack_height - 1, -1, -1):
                if self.board[stack_idx][i] == 0:
                    self.board[stack_idx][i] = ball_type
                    break

            # Decrease the count of available balls for the current player
            if ball_type == 'O':
                self.num_o_balls -= 1
            else:
                self.num_x_balls -= 1

            # Switch to the other player
            self.current_player = 'X' if self.current_player == 'O' else 'O'

            return True
        else:
            # Invalid move
            return False

    def check_win(self):
        # Check for a win in three stacks
        for i in range(self.num_stacks):
            for j in range(self.stack_height - 2):  # Need at least two balls on top for a win
                if (
                    self.board[i][j] != 0
                    and self.board[i][j] == self.board[i][j + 1]
                    and self.board[i][j] == self.board[i][j + 2]
                ):
                    return True

        return False

    def is_game_over(self):
        return self.check_win() or (self.num_o_balls == 0 and self.num_x_balls == 0)
