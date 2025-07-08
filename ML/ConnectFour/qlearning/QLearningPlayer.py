import pygame
import random
import argparse

# define some global variables
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BOARD_SIZE = (7,6)

class ColumnFullException(Exception):
    """An exception that will be thrown if a column of the board is full"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class QLearningPlayer(Player):
    """A class that represents an AI using Q-learning algorithm"""

    def __init__(self, coin_type, epsilon=0.2, alpha=0.3, gamma=0.9):
        """
        Initialize a Q-learner with parameters epsilon, alpha and gamma
        and its coin type
        """
        Player.__init__(self, coin_type)
        self.q = {}
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards

    def getQ(self, state, action):
        """
        Return a probability for a given state and action where the greater
        the probability the better the move
        """
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 1.0
        return self.q.get((state, action))

    def choose_action(self, state, actions):
        """
        Return an action based on the best move recommendation by the current
        Q-Table with a epsilon chance of trying out a new move
        """
        current_state = state

        if random.random() < self.epsilon: # explore!
            chosen_action = random.choice(actions)
            return chosen_action

        qs = [self.getQ(current_state, a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        return actions[i]

    def learn(self, board, actions, chosen_action, game_over, game_logic):
        """
        Determine the reward based on its current chosen action and update
        the Q table using the reward recieved and the maximum future reward
        based on the resulting state due to the chosen action
        """
        reward = 0
        if (game_over):
            win_value = game_logic.get_winner()
            if win_value == 0:
                reward = 0.5
            elif win_value == self.coin_type:
                reward = 1
            else:
                reward = -2
        prev_state = board.get_prev_state()
        prev = self.getQ(prev_state, chosen_action)
        result_state = board.get_state()
        maxqnew = max([self.getQ(result_state, a) for a in actions])
        self.q[(prev_state, chosen_action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)
