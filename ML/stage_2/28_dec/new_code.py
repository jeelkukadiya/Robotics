class SiloGame:
    def __init__(self,initial_state):
        self.state = [
            ["","",""],
            ["o","",""],
            ["x","",""],
            ["o","o",""],
            ["o","x",""],
            ["x","o",""],
            ["x","x",""],
            ["o","o","o"],
            ["o","o","x"],
            ["o","x","o"],
            ["o","x","x"],
            ["x","o","o"],
            ["x","o","x"],
            ["x","x","o"],
            ["x","x","x"]
        ]
        self.init_state = initial_state
        

    def  reward_generator(self):
        pass
 
    def evaluate_priority(self,basket):
      if basket == ['', '', '']:
          return 3
      elif basket == ['o', '', '']:
          return 2
      elif basket == ['x', '', '']:
          return 1
      elif basket == ['o', 'x', '']:
          return 7
      elif basket == ['o', 'o', '']:
          return 5
      elif basket == ['x', 'o', '']:
          return 6
      elif basket == ['x', 'x', '']:
          return 4
      else:
          return 0  # Default priority for other states    

    def select_move(self):
      max_priority = 0
      selected_move = None
      for i, basket in enumerate(initial_state):
          priority = self.evaluate_priority(basket)
          if priority > max_priority:
              max_priority = priority
              selected_move = i
      return selected_move
    
    
    
    def calculate_next_state(self, ball, Silo_number):
        buffer_stack = self.init_state

        for i,row in enumerate(self.init_state):
            for j,item in enumerate(row):
                 if(self.init_state[i][j] == ''):
                    self.init_state[i][j] = 'ball'
                    break   

    


def nxt_level_print():
    for i in range(5):
        silo_game.calculate_next_state('o', i)
    for j in range(5):
        silo_game.calculate_next_state('x', j)


initial_state = [["", "", ""],["", "", ""],["", "", ""],["", "", ""],["", "", ""]]

silo_game = SiloGame(initial_state)

selected_move = silo_game.select_move()
print(selected_move)

nxt_level_print()