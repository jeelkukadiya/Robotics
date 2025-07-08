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

class Player():
    """A class that represents a player in the game"""

    def __init__(self, coin_type):
        """
        Initialize a player with their coin type
        """
        self.coin_type = coin_type

    def complete_move(self):
        """
        A method to make a move and update any learning parameters if any
        """
        pass

    def get_coin_type(self):
        """
        Return the coin type of the player
        """
        return self.coin_type

    def set_coin_type(self, coin_type):
        """
        Set the coin type of a player
        """
        self.coin_type = coin_type


class HumanPlayer(Player):
            """A class that represents a human player in the game"""

            def __init__(self, coin_type):
                """
                Initialize a human player with their coin type
                """
                Player.__init__(self, coin_type)


class ComputerPlayer(Player):
            """A class that represents an AI player in the game"""

            def __init__(self, coin_type, player_type):
                """
                Initialize an AI with the proper type which are one of Random and
                Q-learner currently
                """
                if (player_type == "random"):
                    self.player = RandomPlayer(coin_type)
                else:
                    self.player = QLearningPlayer(coin_type)

            def complete_move(self, coin, board, game_logic, background):
                """
                Move the coin and decide which slot to drop it in and learn from the
                chosen move
                """
                actions = board.get_available_actions()
                state = board.get_state()
                chosen_action = self.choose_action(state, actions)
                coin.move_right(background, chosen_action)
                coin.set_column(chosen_action)
                game_over = board.insert_coin(coin, background, game_logic)
                self.player.learn(board, actions, chosen_action, game_over, game_logic)

                return game_over

            def get_coin_type(self):
                """
                Return the coin type of the AI player
                """
                return self.player.get_coin_type()

            def choose_action(self, state, actions):
                """
                Choose an action (which slot to drop in) based on the state of the
                board
                """
                return self.player.choose_action(state, actions)

class RandomPlayer(Player):
            """A class that represents a computer that selects random moves based on the moves available"""

            def __init__(self, coin_type):
                """
                Initialize the computer player
                """
                Player.__init__(self, coin_type)

            def choose_action(self, state, actions):
                """
                Choose a random action based on the available actions
                """
                return random.choice(actions)

            def learn(self, board, action, game_over, game_logic):
                """
                The random player does not learn from its actions
                """
                pass
