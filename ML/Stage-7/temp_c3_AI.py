import random
import numpy as np

# Constants
ROW_COUNT = 3
COLUMN_COUNT = 5
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    for c in range(COLUMN_COUNT):
        column = board[:, c]
        if np.array_equal(column, [piece]*3):
            return True
    return False

def evaluate_board(board):
    player1_wins = 0
    player2_wins = 0
    
    # Check each column for winning patterns
    for c in range(COLUMN_COUNT):
        column = board[:, c]
        # Check if player 1 has won the column
        if np.array_equal(column, [PLAYER_PIECE]*3):
            player1_wins += 1
        # Check if player 2 has won the column
        elif np.array_equal(column, [AI_PIECE]*3):
            player2_wins += 1

    # Return the difference in wins (favoring player 1)
    return player1_wins - player2_wins

def get_valid_moves(board):
    valid_moves = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_moves.append(col)
    return valid_moves

def minimax(board, depth, maximizing_player):
    if depth == 0:
        return None, evaluate_board(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_valid_moves(board):
            row = get_next_open_row(board, move)
            board_copy = board.copy()
            drop_piece(board_copy, row, move, PLAYER_PIECE)
            _, eval = minimax(board_copy, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move, max_eval
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_valid_moves(board):
            row = get_next_open_row(board, move)
            board_copy = board.copy()
            drop_piece(board_copy, row, move, AI_PIECE)
            _, eval = minimax(board_copy, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return best_move, min_eval

def get_best_move(board):
    return minimax(board, 3, True)[0]

def print_board(board):
    print(np.flip(board, 0))

def main():
    board = create_board()
    print_board(board)
    is_game_over = False

    while not is_game_over:
        # Player's turn
        col = int(input("Player's turn - Enter column: "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)
            if winning_move(board, PLAYER_PIECE):
                print("Player wins!")
                is_game_over = True
            print_board(board)

        # AI's turn
        col = minimax(board, 3, True)[0]  # Use Minimax algorithm
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI_PIECE)
        if winning_move(board, AI_PIECE):
            print("AI wins!")
            is_game_over = True
        print_board(board)

if __name__ == "__main__":
    main()
