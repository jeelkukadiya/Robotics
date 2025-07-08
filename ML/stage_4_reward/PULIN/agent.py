import torch,random,numpy as np
from Def_Off import demo as D 
from collections import deque
from Environment import siloEnvironment
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY=100_000_000
BATCH_SIZE=1000
LR=0.001

class blueAgent:
    def __init__(self):
        # Initialize your agent's parameters and policy here
        self.n_games=0
        self.epsilon=0 # control the randomness
        self.gamma=0.9 # discount rate
        self.memory=deque(maxlen=MAX_MEMORY) # pop from left is max memory get full 
        self.model = Linear_QNet(3, 256, 5) 
        self.trainer = QTrainer(self.model, LR, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_silo_number(self,state):
        # random moves: tradeoff exploration / exploitation
        try:
            self.epsilon = 80 - self.n_games
            silo_selected = [0,0,0,0,0]
            if random.randint(0, 200) < self.epsilon:
                move = random.randint(0, 4)
                silo_selected[move] = 1
            else:
                #state0 = torch.tensor(state, dtype=torch.float)
                state0 = torch.tensor([[float(item) if item else 0.0 for item in inner_list] for inner_list in state], dtype=torch.float32)
                prediction = self.model(state0)
                move = torch.argmax(prediction).item()
                silo_selected[move] = 1
        except:
            print("An error generated")
        finally:
            silo_selected[1]=1

        return silo_selected

    def take_action(self,state_old,silo_selected):

        if 0<=silo_selected<=4: # Checking wheather the selected silo number is in five
            if len(state_old[silo_selected])<4: # checking wheather the silo is empty
                for i in range(len(state_old[silo_selected])):
                    if state_old[silo_selected][i] == '':
                        state_old[silo_selected][i] = '0'
                        break
            else:
                print("Silo is already filled")
        else:
            print("Error in Silo Number",silo_selected)
        return state_old

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0

    #why need of record?
    record = 0

    agent = blueAgent()
    game = siloEnvironment()
    
    # get old state
    state_old = game.Silo_State
    # created tensor of state_old
    tensor_state_old = torch.tensor([[float(item) if item else 0.0 for item in inner_list] for inner_list in state_old], dtype=torch.float32)
    # tensor_state_old = torch.tensor([[float(item) for item in inner_list] for inner_list in state_old], dtype=torch.float32)

    i=0
    while True:

        # not taking this for first for loop  
        if i>=1:
            state_old = state_new
            tensor_state_old = torch.tensor([[float(item) if item else 0.0 for item in inner_list] for inner_list in state_old], dtype=torch.float32)
        
        # get move
        silo_selected_list =agent.get_silo_number(state_old)
        for j in silo_selected_list:
            if silo_selected_list[j] == 1:
                silo_selected=j

        s = random.randint(0,1)
        if s==0:
            # perform move and get new state
            state_new = agent.take_action(state_old,silo_selected)
        elif s==1:
            temp_instance=D() # instance of Deff_off
            state_new=temp_instance.main(state_old)

        game.rewardCalculate(state_old,state_new)
        tensor_state_new = torch.tensor([[float(item) if item else 0.0 for item in inner_list] for inner_list in state_new], dtype=torch.float32)
        # tensor_state_new = torch.tensor([[float(item) for item in inner_list] for inner_list in state_new], dtype=torch.float32)


        # train short memory
        agent.train_short_memory(tensor_state_old,silo_selected_list,game.reward,tensor_state_new,game.game_Over)

        # remember
        agent.remember(tensor_state_old,silo_selected_list,game.reward,tensor_state_new,game.game_Over)

        #check game over condition and check winning condition
        game.check_Win_Condition(state_new)
        game.check_Game_Over(state_new)
        print('\n------------------------------------------------------------------------------')
        print("Round :",i+1,' Agent Selected :',s,"SIlo Selected : ",silo_selected,"reward : ",game.reward,"\nCurrent state : ",state_new)
        print('------------------------------------------------------------------------------\n')
        i=i+1
        if i==15:
            game.game_Over=True

        if game.game_Over:
            # train long memory, plot result
            print('Final State : ',state_new)
            game.reset()
            agent.n_games+=1
            agent.train_long_memory()
            
            if game.reward>record:
                record=game.reward
                agent.model.save() 

            print('Game', agent.n_games, 'Score', game.reward, 'Record:', record)

            plot_scores.append(game.reward)
            total_score += game.reward
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__=="__main__":
    train()