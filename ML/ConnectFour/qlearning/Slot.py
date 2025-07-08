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


class Slot():
    """A class that represents a single slot on the board"""
    SIZE=80
    def __init__(self, row_index, col_index, width, height, x1, y1):
        """
        Initialize a slot in a given position on the board
        """
        self.content = 0
        self.row_index = row_index
        self.col_index = col_index
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width*2, height*2))
        self.x_pos = x1
        self.y_pos = y1

    def get_location(self):
        """
        Return the location of the slot on the game board
        """
        return (self.row_index, self.col_index)

    def get_position(self):
        """
        Return the x and y positions of the top left corner of the slot on
        the screen
        """
        return (self.x_pos, self.y_pos)

    def set_coin(self, coin):
        """
        Set a coin in the slot, which can be one of two colors
        """
        self.content = coin.get_coin_type()

    def check_slot_fill(self):
        """
        Return true iff a coin is placed in the slot
        """
        return (self.content != 0)

    def get_content(self):
        """
        Return what is stored in the slot, 0 if it is empty
        """
        return self.content

    def draw(self, background):
        """
        Draws a slot on the screen
        """
        pygame.draw.rect(self.surface, GREEN, (0, 0, self.width, self.height))
        pygame.draw.rect(self.surface, WHITE, (1,1,self.width - 2,self.height - 2))
        self.surface = self.surface.convert()
        background.blit(self.surface, (self.x_pos, self.y_pos))
