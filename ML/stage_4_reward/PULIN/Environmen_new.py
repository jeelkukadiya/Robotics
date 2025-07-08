from reward import reward as r

class sioEnvironment:
    def __init__(self):
        self.Silo_State=[[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        self.red_won_silo=0
        self.blue_won_silo=0
        self.total_balls=0
        self.reward=0
        self.game_Over = False

    def reset(self):
        self.Silo_State=[[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        self.red_won_silo=0
        self.blue_won_silo=0
        #self.total_balls_count=0
        self.reward=0
        self.game_Over=False
    
    def check_win(self,state):
        for i in state:
            if i == [1,1,1] or i == [1,-1,1] or i == [-1,1,1]:
                self.blue_won_silo+=1
            elif i == [-1,-1,-1] or i == [-1,1,-1] or i == [1,-1,-1]:
                self.red_won_silo+=1
        if self.blue_won_silo==3 or self.red_won_silo==3 or self.total_balls==15:
            return True
        #TODO: i think it may not needed
        #self.blue_won_silo=0
        #self.red_won_silo=0
        return False
    
    def total_balls(self,state):

        total_balls_count = 0
        for i, basket in enumerate(state):
            for j in basket:
                if basket[j] != 0:
                    total_balls_count += 1
        
        return total_balls_count
    

    #TODO: check if game over or not for two conditions(win,full_silo)
    def check_Game_Over(self,state):

        if self.check_win(state):
            self.game_Over=True
        elif self.total_balls(state) == 15:
            self.game_Over=True
        else:
            self.game_Over=False
        """if self.game_Over:
            self.reset()"""

    def rewardCalculate(self,state_old,state_new):
        rewd=r()
        self.reward=rewd.reward_func(state_old,state_new)