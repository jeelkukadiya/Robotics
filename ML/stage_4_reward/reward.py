#from Environment import siloEnvironment as ev

class reward:
  def __init__(self):
    self.red_reward = 0
    self.blue_reward = 0
    self.bluewin = 0
    self.redwin = 0

  def reward_func(self,intial_Silo_state,final_Silo_state,Silo_number,agent,s):

    reward = 0

    for j in final_Silo_state:
      if j == ['o','o','o'] or j == ['o','x','o'] or j == ['x','o','o']:
          self.bluewin +=1
      elif j == ['x','x','x'] or j == ['x','o','x'] or j == ['o','x','x']:
          self.redwin +=1    

    i = final_Silo_state[Silo_number]

    if agent == 0:
      if i == ['o','o','o'] or i == ['o','x','o'] or i == ['x','o','o']:
        self.blue_reward += 10
      """elif i == ['x','x','x'] or i == ['x','o','x'] or i == ['o','x','x']:
        self.blue_reward += -10"""

      if self.bluewin == 3:
         self.blue_reward += 100
      """elif self.redwin == 3:
         self.blue_reward += -100"""
      
      reward = self.blue_reward
      self.blue_reward = 0
    else:
      """if i == ['o','o','o'] or i == ['o','x','o'] or i == ['x','o','o']:
        self.red_reward += -10"""
      if i == ['x','x','x'] or i == ['x','o','x'] or i == ['o','x','x']:
        self.red_reward += 10

      """if self.bluewin == 3:
         self.red_reward += -100"""
      if self.redwin == 3:
         self.red_reward += 100     

      reward = self.red_reward
      self.red_reward = 0

    return reward

    

    



       
      

    
    

