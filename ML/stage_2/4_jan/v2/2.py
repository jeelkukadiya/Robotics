import numpy as np
from main import WinStackEnvironment

class QLearningAgent:
    def __init__(self, num_stacks, stack_height, num_actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.num_stacks = num_stacks
        self.stack_height = stack_height
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = np.zeros(tuple([3] * (num_stacks * stack_height) + [num_actions]))

    def select_action(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(self.num_actions)
        else:
            return np.argmax(self.q_table[tuple(state)])

    def update_q_table(self, state, action, reward, next_state):
        # Q-value update using the Bellman equation
        current_q_value = self.q_table[tuple(state)][action]
        max_future_q_value = np.max(self.q_table[tuple(next_state)])
        new_q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * max_future_q_value - current_q_value)
        self.q_table[tuple(state)][action] = new_q_value

# Assuming WinStackEnvironment is already defined
num_stacks = 5
stack_height = 3
num_actions = num_stacks

# Create WinStack environment and Q-learning agent
env = WinStackEnvironment(num_stacks=num_stacks, stack_height=stack_height)
agent = QLearningAgent(num_stacks=num_stacks, stack_height=stack_height, num_actions=num_actions)

# Training loop
num_episodes = 1000

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0

    while not env.is_game_over():
        action = agent.select_action(state)
        next_state = state.copy()
        if env.make_move(action):
            reward = 1  # Positive reward for making a valid move
        else:
            reward = -1  # Negative reward for making an invalid move
        total_reward += reward
        agent.update_q_table(state, action, reward, next_state)
        state = next_state

    if episode % 100 == 0:
        print(f"Episode {episode}, Total Reward: {total_reward}")

# After training, you can use the learned Q-table to make optimal moves in the game.
