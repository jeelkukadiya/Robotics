import random

def initialize_game():
    # Initialize the game board and players
    game_board = [[''] * 3 for _ in range(5)]

    player_turn = random.choice(['O', 'X'])
    o_balls = 12
    x_balls = 12

    return game_board, player_turn, o_balls, x_balls

def print_board(game_board):
    # Print the current state of the game board
    for row in game_board:
        print('|'.join(row))
        print('-' * 9)

def make_move(game_board, player_turn, stack_index):
    # Make a move by placing a ball in the specified stack
    
    if 0 <= stack_index < 5:
        stack = game_board[stack_index]
        # Find the first empty space in the stack and place the ball
        if stack.count('') < 1:
            # The stack is full, cannot make a move
            return False
        
        for i in range(3):
            if stack[i] == '':
                stack[i] = player_turn
                return True

    # Invalid stack index
    return False

# Example Usage:
game_board, player_turn, o_balls, x_balls = initialize_game()

while True:
    print_board(game_board)
    print(f"Player {player_turn}'s turn")

    # Example: Player makes a move by choosing a stack (index 0 to 4)
    stack_choice = int(input("Choose a stack (0 to 4): "))
    if make_move(game_board, player_turn, stack_choice):
        # Move successful, switch to the other player
        player_turn = 'O' if player_turn == 'X' else 'X'
    else:
        print("Invalid move. Try again.")
