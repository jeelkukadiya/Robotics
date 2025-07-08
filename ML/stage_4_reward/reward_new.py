#from Environment import siloEnvironment as ev

class reward:
  def __init__(self):
    self.red_reward = 0
    self.blue_reward = 0
    self.bluewin = 0
    self.redwin = 0

  def reward_func(self,final_Silo_state):

    self.bluewin = 0
    self.redwin = 0
    self.red_reward = 0
    self.blue_reward = 0

    #reward = [0,0]

    for i in final_Silo_state:
      if i == [1,1,1] or i == [1,-1,1] or i == [-1,1,1]:
        self.blue_reward += 10
        self.red_reward  += -10
        self.bluewin +=1
        
      elif i == [-1,-1,-1] or i == [-1,1,-1] or i == [1,-1,-1]:
        self.blue_reward += -10
        self.red_reward  += 10
        self.redwin +=1

    """for j in final_Silo_state:
      if j == [1,1,1] or j == [1,-1,1] or j == [-1,1,1]:
          self.bluewin +=1
      elif j == [-1,-1,-1] or j == [-1,1,-1] or j == [1,-1,-1]:
          self.redwin +=1"""
    
    if self.bluewin == 3:
         self.blue_reward += 100
         self.red_reward  += -100
    elif self.redwin == 3:
         self.red_reward += 100
         self.blue_reward += -100
         

    #reward = [self.blue_reward,self.red_reward]
    

    return self.blue_reward



       
      

    
    

