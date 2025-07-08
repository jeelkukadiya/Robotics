from winstack_environment import WinStackEnvironment
from q_learning_agent import QLearningAgent

'''
# Assuming WinStackEnvironment and QLearningAgent classes are already defined

def train_agent(num_episodes=1000):
    env = WinStackEnvironment(num_stacks=5, stack_height=3)
    agent = QLearningAgent(num_stacks=5, stack_height=3, num_actions=5)

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

if __name__ == "__main__":
    train_agent()

'''


def train_agent(num_episodes=1000):
    env = WinStackEnvironment(num_stacks=5, stack_height=3)
    agent = QLearningAgent(num_stacks=5, stack_height=3, num_actions=5)

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

        #print(f"Episode {episode}, Total Reward: {total_reward}, Q-values: {agent.q_table[tuple(state.astype(int))]}")
        #print(f"Episode {episode}, Total Reward: {total_reward}, State: {state}, Q-values: {agent.q_table[tuple(state.astype(int))]}")
        #print(f"Episode {episode}, Total Reward: {total_reward}, State: {state}, Q-values: {agent.q_table[tuple(map(int, state))]}")
        print(f"Episode {episode}, Total Reward: {total_reward}, State: {state}, Q-values: {agent.q_table[tuple(int(x) if x else 0 for x in state)]}")


        if episode % 100 == 0:
            print(f"Episode {episode}, Total Reward: {total_reward}")

if __name__ == "__main__":
    train_agent()
