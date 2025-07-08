import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        # Convert input data to PyTorch tensors
        states = torch.tensor(state, dtype=torch.float32)
        actions = torch.tensor(action, dtype=torch.long)
        rewards = torch.tensor(reward, dtype=torch.float32)
        next_states = torch.tensor(next_state, dtype=torch.float32)
        dones = torch.tensor(done, dtype=torch.float32)

        # Compute Q-values for the current state and next state
        q_values_current = self.model(states)
        q_values_next = self.model(next_states)

        # Gather Q-values for the selected actions
        q_values_current_selected = q_values_current.gather(1, actions.unsqueeze(1))

        # Compute target Q-values using the Bellman equation
        target_q_values = rewards + self.gamma * torch.max(q_values_next, dim=1).values * (1.0 - dones)

        # Calculate the TD error
        td_error = F.mse_loss(q_values_current_selected, target_q_values.unsqueeze(1))

        # Optimize the Q-network
        self.optimizer.zero_grad()
        td_error.backward()
        self.optimizer.step()
        
        """state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)
        # i=1 # temp for trial purpose
        if len(state.shape) == 1: # if len(state.shape)==1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )
            # i=i+1
        done = (done, )    
        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()"""