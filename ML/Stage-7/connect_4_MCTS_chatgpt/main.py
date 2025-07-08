# main.py

from game import ConnectFourGame
from mcts import MCTS

def main():
    game = ConnectFourGame()
    mcts = MCTS()

    while not game.is_full() and not game.check_win(1) and not game.check_win(-1):
        game.display()
        if game.current_player == 1:
            print("-----PLAYER-MOVE-----")
            move = int(input("Enter column (0-6): "))
            while move not in game.get_valid_moves():
                print("Invalid move! Please enter a valid column.")
                move = int(input("Enter column (0-6): "))
        else:
            print("-----MCTS-MOVE-----")
            move = mcts.search(game)
        game.make_move(move, game.current_player)
        game.switch_player()

    game.display()
    if game.check_win(1):
        print("Player 1 wins!")
    elif game.check_win(-1):
        print("MCTS wins!")
    else:
        print("Draw!")

if __name__ == "__main__":
    main()
