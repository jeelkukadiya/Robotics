from env import WinStackEnvironment 
from agent import QLearningAgent
import numpy as np

env = WinStackEnvironment()
agent = QLearningAgent(env)

# Train the agent
num_episodes = 10
agent.train(num_episodes)

# Evaluate the agent
env.reset()
print("Initial Board:")
env.print_board()

while True:
    action = agent.select_action(env.board)
    ball_type = 1  # Assume the agent is always 'O' for simplicity
    if env.make_move(action, ball_type):
        print(f"\nAfter 'O' Move:")
        env.print_board()
        if env.is_winner(ball_type):
            print("'O' wins!")
            break

    # Opponent's move (random for simplicity)
    opponent_action = np.random.choice([i for i in range(env.num_stacks) if 0 in env.board[i]])
    env.make_move(opponent_action, 2)  # Assume the opponent is always 'X' for simplicity
    print(f"\nAfter 'X' Move:")
    env.print_board()
    if env.is_winner(2):
        print("'X' wins!")
        break
