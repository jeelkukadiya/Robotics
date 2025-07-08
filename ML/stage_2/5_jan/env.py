import numpy as np

class WinStackEnvironment:
    def __init__(self, num_stacks=5, stack_height=3):
        self.num_stacks = num_stacks
        self.stack_height = stack_height
        self.reset()

    def reset(self):
        self.board = np.zeros((self.num_stacks, self.stack_height), dtype=int)  # 0 represents an empty space

    def make_move(self, stack_idx, ball_type):
        for i in range(self.stack_height):
            if self.board[stack_idx][i] == 0:
                self.board[stack_idx][i] = ball_type
                return True  # Move successful
        return False  # Stack is full

    def is_winner(self, ball_type):
        # Check for a win in any stack
        for stack_idx in range(self.num_stacks):
            for i in range(self.stack_height - 1, 1, -1):
                if (
                    self.board[stack_idx][i] == ball_type
                    and self.board[stack_idx][i - 1] == ball_type
                    and self.board[stack_idx][i - 2] == ball_type
                ):
                    return True  # Winning condition satisfied
        return False

    def print_board(self):
        for row in reversed(self.board.T):
            print('|'.join(map(str, row)))
            print('-' * 9)
