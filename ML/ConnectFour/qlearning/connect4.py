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

class Coin():
    """A class that represents the coin pieces used in connect 4"""

    RADIUS = 30

    def __init__(self, coin_type):
        """
        Initialize a coin with a given coin_type
        (integer that represents its color)
        """
        self.coin_type = coin_type
        self.surface = pygame.Surface((Slot.SIZE - 3, Slot.SIZE - 3))
        if (self.coin_type == 1):
            self.color = BLUE
        else:
            self.color = RED

    def set_position(self, x1, y1):
        """
        Set the position of the coin on the screen
        """
        self.x_pos = x1
        self.y_pos = y1

    def set_column(self, col):
        """
        Set the column on the board in which the coin belongs
        """
        self.col = col

    def get_column(self):
        """
        Get the column on the board in which the coin belongs in
        """
        return self.col

    def set_row(self, row):
        """
        Set the row on the board where the coin is
        """
        self.row = row

    def get_row(self):
        """
        Get the row on the board in which the coin belongs
        """
        return self.row

    def move_right(self, background, step=1):
        """
        Move the coin to the column that is right of its current column
        """
        self.set_column(self.col + 1)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos + step * Slot.SIZE, self.y_pos)
        self.draw(background)

    def move_left(self, background):
        """
        Move the coin to the column that is left of its current column
        """
        self.set_column(self.col - 1)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos - Slot.SIZE, self.y_pos)
        self.draw(background)

    def drop(self, background, row_num):
        """
        Drop the coin to the bottom most possible slot in its column
        """
        self.set_row(row_num)
        self.surface.fill((0,0,0))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.set_position(self.x_pos, self.y_pos + ((self.row + 1) * Slot.SIZE))
        self.surface.fill((255,255,255))
        background.blit(self.surface, (self.x_pos, self.y_pos))
        self.draw(background)

    def get_coin_type(self):
        """
        Return the coin type
        """
        return self.coin_type

    def draw(self, background):
        """
        Draw the coin on the screen
        """
        pygame.draw.circle(self.surface, self.color, (Slot.SIZE // 2, Slot.SIZE // 2), Coin.RADIUS)
        self.surface = self.surface.convert()
        background.blit(self.surface, (self.x_pos, self.y_pos))



class GameLogic():
    """A class that handles win conditions and determines winner"""
    WIN_SEQUENCE_LENGTH = 4

    def __init__(self, board):
        """
        Initialize the GameLogic object with a reference to the game board
        """
        self.board = board
        (num_rows, num_columns) = self.board.get_dimensions()
        self.board_rows = num_rows
        self.board_cols = num_columns
        self.winner_value = 0

    def check_game_over(self):
        """
        Check whether the game is over which can be because of a tie or one
        of two players have won
        """
        (last_visited_nodes, player_value) = self.board.get_last_filled_information()
        representation = self.board.get_representation()
        player_won = self.search_win(last_visited_nodes, representation)
        if player_won:
            self.winner_value = player_value

        return ( player_won or self.board.check_board_filled() )



    def search_win(self, last_visited_nodes, representation):
        """
        Determine whether one of the players have won
        """
        for indices in last_visited_nodes:
            current_node = representation[indices[0]][indices[1]]
            if ( current_node.top_left_score == GameLogic.WIN_SEQUENCE_LENGTH or
                 current_node.top_score == GameLogic.WIN_SEQUENCE_LENGTH or
                 current_node.top_right_score == GameLogic.WIN_SEQUENCE_LENGTH or
                 current_node.left_score == GameLogic.WIN_SEQUENCE_LENGTH or
                 current_node.right_score == GameLogic.WIN_SEQUENCE_LENGTH or
                 current_node.bottom_left_score == GameLogic.WIN_SEQUENCE_LENGTH or
                 current_node.bottom_score == GameLogic.WIN_SEQUENCE_LENGTH or
                 current_node.bottom_right_score == GameLogic.WIN_SEQUENCE_LENGTH ):
                return True

        return False

    def determine_winner_name(self):
        """
        Return the winner's name
        """
        if (self.winner_value == 1):
            return "BLUE"
        elif (self.winner_value == 2):
            return "RED"
        else:
            return "TIE"

    def get_winner(self):
        """
        Return the winner coin type value
        """
        return self.winner_value


class SlotTrackerNode():
    """A class that that represents the node in the internal graph
    representation of the game board"""

    def __init__(self):
        """
        Initialize the SlotTrackerNode with pointers to Nodes in all
        8 directions surrounding along with a score count in each direction
        """
        self.top_left = None
        self.top_right = None
        self.top = None
        self.left = None
        self.right = None
        self.bottom_left = None
        self.bottom = None
        self.bottom_right = None
        self.top_left_score = 1
        self.top_right_score = 1
        self.top_score = 1
        self.left_score = 1
        self.right_score = 1
        self.bottom_left_score = 1
        self.bottom_score = 1
        self.bottom_right_score = 1
        self.value = 0
        self.visited = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('iterations', nargs='?', default=20, action="store", help="Store the number of iterations to train computer")
    args = parser.parse_args()

    GameView(1200, 760).main_menu(int(args.iterations))
