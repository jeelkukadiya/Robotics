import numpy as np

class CustomEnvironment:
    def __init__(self):
        self.basket_stacks = [[0, 0, 0] for _ in range(5)]
        self.current_player = 1
        self.max_balls = 15
        self.game_over = False

    def reset(self):
        self.basket_stacks = [[0, 0, 0] for _ in range(5)]
        self.current_player = 1
        self.game_over = False

    def get_state(self):
        # Flatten the list of basket configurations to represent the state
        return np.array(self.basket_stacks).flatten()

    def take_action(self, basket_index):
        if not self.game_over and 0 <= basket_index < len(self.basket_stacks):
            # Check if the selected basket has an empty space
            if 0 in self.basket_stacks[basket_index]:
                # Place a ball based on the current player
                ball_value = 1 if self.current_player == 1 else -1
                empty_slot = self.basket_stacks[basket_index].index(0)
                self.basket_stacks[basket_index][empty_slot] = ball_value

                # Check for game termination conditions
                self.game_over = self.check_win() or self.total_balls() == self.max_balls

                # Switch to the next player
                self.current_player *= -1

    def check_win(self):
        # Check if any player has achieved a winning condition
        for i in self.basket_stacks:
            if i == [1, 1, 1] or i == [1, -1, 1] or i == [-1, 1, 1]:
                return True
            elif i == [-1, -1, -1] or i == [-1, 1, -1] or i == [1, -1, -1]:
                return True
        return False

    def total_balls(self):
        # Count the total number of balls in the baskets
        return sum(sum(ball != 0 for ball in basket) for basket in self.basket_stacks)