import numpy as np

class QLearningAgent:
    def __init__(self, num_stacks, stack_height, num_actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.num_stacks = num_stacks
        self.stack_height = stack_height
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = np.zeros(tuple([3] * (num_stacks * stack_height) + [num_actions]), dtype='U1')

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
