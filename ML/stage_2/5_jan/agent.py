import numpy as np

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, min_exploration_rate=0.01, exploration_decay=0.995):
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.min_exploration_rate = min_exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = np.zeros((env.num_stacks, env.stack_height, 2))  # Q-values for each state-action pair

    def select_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(['O', 'X'])  # Explore
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (
            reward + self.discount_factor * self.q_table[next_state][best_next_action] - self.q_table[state][action]
        )

    def train(self, num_episodes):
        for episode in range(num_episodes):
            state = self.env.board.copy()

            while True:
                action = self.select_action(state)
                ball_type = episode % 2 + 1  # Alternate between 'O' and 'X'
                if self.env.make_move(action, ball_type):
                    next_state = self.env.board.copy()
                    reward = 1 if self.env.is_winner(ball_type) else 0
                    self.update_q_table(state, action, reward, next_state)
                    state = next_state

                    if reward == 1:
                        break

            # Decay exploration rate
            self.exploration_rate *= self.exploration_decay
            self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate)

