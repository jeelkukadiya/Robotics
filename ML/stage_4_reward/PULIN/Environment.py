from reward import reward as r
class siloEnvironment:
    def __init__(self):
        self.Silo_State=[["", "", ""],["", "", ""],["", "", ""],["", "", ""],["", "", ""]]
        self.red_won_silo=0
        self.blue_won_silo=0
        self.total_balls=0
        self.reward=0
        self.game_Over = False
 
    def reset(self):
        self.Silo_State=[["", "", ""],["", "", ""],["", "", ""],["", "", ""],["", "", ""]]
        self.red_won_silo=0
        self.blue_won_silo=0
        self.total_balls=0
        self.reward=0
        self.game_Over=False

    def check_Win_Condition(self,state):
        for i in state:
            if i == ['0','0','0'] or i == ['0','1','0'] or i == ['1','0','0']:
                self.blue_won_silo+=1
            elif i == ['1','1','1'] or i == ['1','0','1'] or i == ['0','1','1']:
                self.red_won_silo+=1
        if self.blue_won_silo==3 or self.red_won_silo==3 or self.total_balls==15:
            self.game_Over=True
        self.blue_won_silo=0
        self.red_won_silo=0

    def check_Game_Over(self,state):
        k=0
        for i, ball in enumerate(state):
            if ball != '':
                k+=1
        if k==15:
            self.game_Over=True
        if self.game_Over:
            self.reset()

    def rewardCalculate(self,state_old,state_new):
        rewd=r()
        self.reward=rewd.reward_func(state_old,state_new)
