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



class Board():
    """A class to represent the connect 4 board"""

    MARGIN_X = 300
    MARGIN_Y = 150

    def __init__(self, num_rows, num_columns):
        """
        Initialize a board with num_rows rows and num_columns columns
        """
        self.container = [[Slot(i, j, Slot.SIZE, Slot.SIZE,
                                j*Slot.SIZE + Board.MARGIN_X,
                                i*Slot.SIZE + Board.MARGIN_Y) for j in range(num_columns)] for i in range(num_rows)]
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.total_slots = num_rows * num_columns
        self.num_slots_filled = 0
        self.last_visited_nodes = []
        self.last_value = 0

        self.state = [[0 for j in range(num_columns)] for i in range(num_rows)]
        self.prev_state = None
        self.prev_move = (None, None, None)
        # initialize the internal graph representation of the board
        # where every node is connected to all the other nodes in the 8
        # directions surrounding it to which it already contains pointers
        self.representation = [[SlotTrackerNode() for j in range(num_columns)] for i in range(num_rows)]
        for i in range(num_rows):
            prev_row_index = i - 1
            next_row_index = i + 1
            for j in range(num_columns):
                prev_col_index = j - 1
                next_col_index = j + 1
                current_node = self.representation[i][j]
                if prev_row_index >= 0 and prev_col_index >=0:
                    current_node.top_left = self.representation[prev_row_index][prev_col_index]
                if prev_row_index >=0:
                    current_node.top = self.representation[prev_row_index][j]
                if prev_row_index >=0 and next_col_index < num_columns:
                    current_node.top_right = self.representation[prev_row_index][next_col_index]
                if prev_col_index >= 0:
                    current_node.left = self.representation[i][prev_col_index]

                if next_col_index < num_columns:
                    current_node.right = self.representation[i][next_col_index]
                if next_row_index < num_rows and prev_col_index >= 0:
                    current_node.bottom_left = self.representation[next_row_index][prev_col_index]

                if next_row_index < num_rows:
                    current_node.bottom = self.representation[next_row_index][j]
                if next_row_index < num_rows and next_col_index < num_columns:
                    current_node.bottom_right = self.representation[next_row_index][next_col_index]

    def draw(self, background):
        """
        Method to draw the entire board on the screen
        """
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                self.container[i][j].draw(background)

    def get_slot(self, row_index, col_index):
        """
        Return a slot on the board given its row and column indices
        """
        return self.container[row_index][col_index]

    def check_column_fill(self, col_num):
        """
        Return True iff the column col_num on the board is filled up
        """
        for i in range(len(self.container)):
            # if a slot isn't filled then the column is not filled
            if not self.container[i][col_num].check_slot_fill():
                return False
        return True

    def insert_coin(self, coin, background, game_logic):
        """
        Insert the coin in the board and update board state and
        internal representation
        """
        col_num = coin.get_column()
        if not self.check_column_fill(col_num):
            row_index = self.determine_row_to_insert(col_num)
            self.container[row_index][col_num].set_coin(coin)
            if (self.prev_move[0] == None):
                self.prev_state = [[0 for j in range(self.num_columns)] for i in range(self.num_rows)]
            else:
                (prev_row, prev_col, value) = self.prev_move
                self.prev_state[prev_row][prev_col] = value
            self.prev_move = (row_index, col_num, coin.get_coin_type())
            self.state[row_index][col_num] = coin.get_coin_type()
            self.update_slot_tracker(row_index, col_num, coin.get_coin_type())
            self.num_slots_filled += 1
            self.last_value = coin.get_coin_type()
            coin.drop(background, row_index)

        else:
            raise ColumnFullException('Column is already filled!')

        result = game_logic.check_game_over()

        return result

    def determine_row_to_insert(self, col_num):
        """
        Determine the row in which the coin can be dropped into
        """
        for i in range(len(self.container)):
            if self.container[i][col_num].check_slot_fill():
                return (i - 1)

        return self.num_rows - 1

    def get_dimensions(self):
        """
        Return the dimensions of the board
        """
        return (self.num_rows, self.num_columns)

    def check_board_filled(self):
        """
        Return true iff the board is completely filled
        """
        return (self.total_slots == self.num_slots_filled)

    def get_representation(self):
        """
        Return the internal graph representation of the board
        """
        return self.representation

    def get_available_actions(self):
        """
        Return the available moves
        """
        actions = []
        for i in range(self.num_columns):
            if (not self.check_column_fill(i)):
                actions.append(i)
        return actions

    def get_state(self):
        """
        Return the 2d list numerical representation of the board
        """
        result = tuple(tuple(x) for x in self.state)

        return result

    def get_prev_state(self):
        """
        Return the previous state of the board
        """
        result = tuple(tuple(x) for x in self.prev_state)

        return result

    def get_last_filled_information(self):
        """
        Return the last visited nodes during the update step of the scores
        within the internal graph representation and also return the last
        coin type inserted into the board
        """
        return (self.last_visited_nodes, self.last_value)

    def update_slot_tracker(self, i, j, coin_type):
        """
        Update the internal graph representation based on the latest insertion
        into the board
        """
        self.last_visited_nodes = []
        start_node = self.representation[i][j]
        start_node.value = coin_type
        self.traverse(start_node, coin_type, i, j, self.last_visited_nodes)
        # reset all the nodes as if it hadn't been visited
        for indices in self.last_visited_nodes:
            self.representation[indices[0]][indices[1]].visited = False


    def traverse(self, current_node, desired_value, i, j, visited_nodes):
        """
        Recursively update the scores of the relevant nodes based on its
        adjacent nodes (slots). If a coin type 1 is inserted into the board in
        some position i, j, then update all adjacent slots that contain 1 with
        an updated score reflecting how many slots have 1 in a row in the top
        left, top right, etc directions
        """
        current_node.visited = True
        visited_nodes.append((i,j))
        if current_node.top_left:
            top_left_node = current_node.top_left
            if top_left_node.value == desired_value:
                current_node.top_left_score = top_left_node.top_left_score + 1
                if not top_left_node.visited:
                    self.traverse(top_left_node, desired_value, i - 1, j - 1, visited_nodes)
        if current_node.top:
            top_node = current_node.top
            if top_node.value == desired_value:
                current_node.top_score = top_node.top_score + 1
                if not top_node.visited:
                    self.traverse(top_node, desired_value, i - 1, j, visited_nodes)
        if current_node.top_right:
            top_right_node = current_node.top_right
            if top_right_node.value == desired_value:
                current_node.top_right_score = top_right_node.top_right_score + 1
                if not top_right_node.visited:
                    self.traverse(top_right_node, desired_value, i - 1, j + 1, visited_nodes)

        if current_node.left:
            left_node = current_node.left
            if left_node.value == desired_value:
                current_node.left_score = left_node.left_score + 1
                if not left_node.visited:
                    self.traverse(left_node, desired_value, i, j - 1, visited_nodes)

        if current_node.right:
            right_node = current_node.right
            if right_node.value == desired_value:
                current_node.right_score = right_node.right_score + 1
                if not right_node.visited:
                    self.traverse(right_node, desired_value, i, j + 1, visited_nodes)

        if current_node.bottom_left:
            bottom_left_node = current_node.bottom_left
            if bottom_left_node.value == desired_value:
                current_node.bottom_left_score = bottom_left_node.bottom_left_score + 1
                if not bottom_left_node.visited:
                    self.traverse(bottom_left_node, desired_value, i + 1, j - 1, visited_nodes)

        if current_node.bottom:
            bottom_node = current_node.bottom
            if bottom_node.value == desired_value:
                current_node.bottom_score = bottom_node.bottom_score + 1
                if not bottom_node.visited:
                    self.traverse(bottom_node, desired_value, i + 1, j, visited_nodes)

        if current_node.bottom_right:
            bottom_right_node = current_node.bottom_right
            if bottom_right_node.value == desired_value:
                current_node.bottom_right_score = bottom_right_node.bottom_right_score + 1
                if not bottom_right_node.visited:
                    self.traverse(bottom_right_node, desired_value, i + 1, j + 1, visited_nodes)
