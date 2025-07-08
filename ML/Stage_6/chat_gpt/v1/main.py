import torch
import numpy as np

# Import custom files
from environment import CustomEnvironment
from model import LinearQNet
from replay_buffer import ReplayBuffer
from agent import QTrainer
from reward import Reward
from Def_Off_2 import Demo
from helper import plot

# Parameters
input_size = 15  # size of the flattened basket_stacks
hidden_size_1 = 64
hidden_size_2 = 32
output_size = 15  # possible actions (basket indices)
lr = 0.001
gamma = 0.99
buffer_capacity = 200000
batch_size = 64
target_update = 10

# Initialize components
env = CustomEnvironment()
model = LinearQNet(input_size, hidden_size_1, hidden_size_2, output_size)
target_model = LinearQNet(input_size, hidden_size_1, hidden_size_2, output_size)
target_model.load_state_dict(model.state_dict())
target_model.eval()
replay_buffer = ReplayBuffer(buffer_capacity)
trainer = QTrainer(model, lr, gamma)
reward_func = Reward()
demo = Demo()

# Training loop
num_games = 10
scores = []
mean_scores = []

for game in range(num_games):
    env.reset()
    state = env.get_state()
    total_reward = 0

    while not env.game_over:
        # Choose action
        if np.random.rand() < 0.1:  # Exploration (10% of the time)
            action = np.random.randint(0, output_size)
        else:
            q_values = model(torch.tensor(state, dtype=torch.float))
            action = torch.argmax(q_values).item()

        # Take action
        env.take_action(action)
        next_state = env.get_state()
        reward = reward_func.reward_func(env.basket_stacks)
        done = env.game_over

        # Store transition in replay buffer
        replay_buffer.push((state, action, reward, next_state, done))

        # Update Q-network
        if len(replay_buffer) > batch_size:
            trainer.train_step(*zip(*replay_buffer.sample(batch_size)))

        # Update target network
        if game % target_update == 0:
            target_model.load_state_dict(model.state_dict())

        # Update state and total reward
        state = next_state
        total_reward += reward

    scores.append(total_reward)
    mean_score = np.mean(scores[-10:])
    mean_scores.append(mean_score)
    plot(scores, mean_scores)

print("Training complete!")