import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F 
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size_1,hidden_size_2,hidden_size_3,hidden_size_4,hidden_size_5, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size_1)
        self.linear2 = nn.Linear(hidden_size_1,hidden_size_2)
        self.linear3 = nn.Linear(hidden_size_2,hidden_size_3)
        self.linear4 = nn.Linear(hidden_size_3,hidden_size_4)
        self.linear5 = nn.Linear(hidden_size_4,hidden_size_5)
        self.linear6 = nn.Linear(hidden_size_5,output_size)


    def forward(self, x):
        x = F.relu(self.linear1(x)) 
        x = F.relu(self.linear2(x)) 
        x = F.relu(self.linear3(x)) 
        x = F.relu(self.linear4(x)) 
        x = F.relu(self.linear5(x)) 

        x = self.linear6(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './Stage-5/model'
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
        
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)
        #print(state.shape,len(state.shape) == torch.Size([5, 3]))
        if len(state.shape) == 2: 
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        #done = (done, )    
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

        self.optimizer.step()




"""import torch
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
        model_folder_path = './Stage-5/model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.model.to('cuda')  # Move model to GPU
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float).to('cuda')
        next_state = torch.tensor(next_state, dtype=torch.float).to('cuda')
        action = torch.tensor(action, dtype=torch.long).to('cuda')
        reward = torch.tensor(reward, dtype=torch.float).to('cuda')

        if len(state.shape) == 2: 
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()"""

