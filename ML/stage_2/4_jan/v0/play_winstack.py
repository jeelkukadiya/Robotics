from winstack_environment import WinStackEnvironment
from q_learning_agent import QLearningAgent
import train_agent

# Assuming WinStackEnvironment and QLearningAgent classes are already defined

def play_game():
    env = WinStackEnvironment(num_stacks=5, stack_height=3)
    agent = QLearningAgent(num_stacks=5, stack_height=3, num_actions=5)

    # Train the agent (you can load a pre-trained agent here if needed)
    train_agent()

    state = env.reset()
    total_reward = 0

    while not env.is_game_over():
        action = agent.select_action(state)
        print(f"Player {env.current_player} moves to stack {action}")
        env.make_move(action)
        env.print_board()
        total_reward += 1  # You can modify the reward based on your own criteria

    print(f"Game Over! Total Reward: {total_reward}")

if __name__ == "__main__":
    play_game()
