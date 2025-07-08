from Blue import demo as bdo
from Red import demo as rdo
from random import randint

class Environment:
    def __init__(self):
        self.red_var=0
        self.blue_var=0
        self.red_ball=0
        self.blue_ball=0
        self.Silos_State=[["", "", ""],["", "", ""],["", "", ""],["", "", ""],["", "", ""]]

        self.reset = 0

    def push_blue(self,temp):
        if 0<=temp<=4:
            if len(self.Silos_State[temp])<4:
                for i, ball in enumerate(self.Silos_State):
                    if ball == '':
                        self.Silos_State[i] = 'o'
            else:
                print("blue : Silo is already filled")
        else:
            print("Error in Silo Number Generation")

    def push_red(self,temp):
        if 0<=temp<=4:
            if len(self.Silos_State[temp])<4:
                for i, ball in enumerate(self.Silos_State):
                    if ball == '':
                        self.Silos_State[i] = 'x'
            else:
                print("red : Silo is already filled")
        else:
            print("Error in Silo Number Generation")

    def select_agent(self):
        s = randint(0,9)

        if s%2==0:
            self.Blue_instance=bdo()
            Silo_number=self.Blue_instance.main(self.Silos_State)
            self.push_blue(Silo_number)
        elif s%2!=0:
            self.Red_instance=rdo()
            Silo_number=self.Red_instance.main(self.Silos_State)
            self.push_red(Silo_number)
        else:
            print("Error in agent selsction")

        self.win_condition()

    def state_print(self):
        print(self.Silos_State)
    
    def win_condition(self):
        for i in self.Silos_State:
            if i == ['o','o','o'] or i == ['o','x','o'] or i == ['x','o','o']:
                self.blue_var+=1
            elif i == ['x','x','x'] or i == ['x','o','x'] or i == ['o','x','x']:
                self.red_var+=1
            else:
                for ball in self.Silos_State:
                    for i in ball:
                        if i == 'x':
                            self.red_ball+=1
                        elif i == 'o':
                            self.blue_ball+=1

        if self.blue_var>=3:
            print("Blue Team won the match")
            self.reset = 1
            print()
        elif self.red_var>=3:
            print("Red team won the match")
            self.reset = 1
            print()
        else:
            # print("No team won the match")
            # print("Red Team Point : ",self.red_ball)
            # print("Blue Team Point : ",self.blue_ball)
            print()

        self.blue_ball=0
        self.red_ball=0
        self.blue_var=0
        self.red_var=0
        
    def reset(self):
        self.blue_var=0
        self.red_var=0
        self.Silos_State=[["", "", ""],["", "", ""],["", "", ""],["", "", ""],["", "", ""]]

#game loop
game_instance=Environment()

for i in range(15):
    if game_instance.reset == 0:
      game_instance.select_agent()
      game_instance.state_print()
    else:
        break
#if tie
if game_instance.reset == 0:    
  print("Tie")
