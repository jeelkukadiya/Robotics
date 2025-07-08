class SiloGame:
    def __init__(self):
        self.state = [
            ["", "", ""], ["", "", "O"], ["", "", "X"], ["", "O", "O"], ["", "X", "O"],
            ["", "O", "X"], ["", "X", "X"], ["O", "O", "O"], ["X", "O", "O"], ["O", "X", "O"],
            ["X", "X", "O"], ["O", "O", "X"], ["X", "O", "X"], ["O", "X", "X"], ["X", "X", "X"]
        ]
        self.init_list = [["", "", ""],["", "", ""],["", "", ""],["", "", ""],["", "", ""]]
        self.buffer = []
        self.reward=0
        self.Total_Silo = 5
        self.var = 0
    
    def reward_generator(self, selected_state):
        # print("buffer is filled with : ",selected_state)
        reward_list = []
        self.local_reward=0
        for i in range(5):
            if self.init_list[i]==selected_state[i]:
                self.reward+=0
                self.local_reward+=0
            elif self.init_list[i]==["", "", ""] and selected_state[i]==["", "", "o"]:
                self.reward+=3
                self.local_reward+=3
            elif self.init_list[i]==["", "", "o"] and selected_state[i]==["", "o", "o"]:
                self.reward+=2
                self.local_reward+=2
            elif self.init_list[i]==["", "", "x"] and selected_state[i]==["", "o", "x"]:
                self.reward+=1
                self.local_reward+=1
            elif self.init_list[i]==["", "o", "o"] and selected_state[i]==["o", "o", "o"]:
                self.reward+=7
                self.local_reward+=7
            elif self.init_list[i]==["", "x", "o"] and selected_state[i]==["o", "x", "o"]:
                self.reward+=6
                self.local_reward+=6
            elif self.init_list[i]==["", "o", "x"] and selected_state[i]==["o", "o", "x"]:
                self.reward+=5
                self.local_reward+=5
            elif self.init_list[i]==["", "x", "x"] and selected_state[i]==["o", "x", "x"]:
                self.reward+=4
                self.local_reward+=4
            else:
                print("An error occured in reward_generator function")
            reward_list.append(self.local_reward)
            self.local_reward=0
        print(reward_list)
            

    def state_selector(self, s):
        if 1 <= s <= 10:
            self.var = 0
            self.reward_generator(self.buffer[s-1])
            print("Reward generated is : ",self.reward)
            self.reward=0
            self.init_list = self.buffer[s-1]
            self.buffer.clear()
            return 1
        else:
            return 0

    def verify_index_generater(self):
        j = 0
        self.index_list = []
        for i in range(self.Total_Silo):
            for sublist in self.state:
                if sublist == self.init_list[i]:
                    j += 1
                    index = self.state.index(sublist)
                    self.index_list.append(index)
        if j == self.Total_Silo:
            return 1
        else:
            return 0

    def calculate_next_state(self, ball, Silo_number):
        self.next_state = []
        
        cal_list = list(map(lambda x: x + 1, self.index_list))
        
        number = cal_list[Silo_number - 1]
        
        if 8 <= number <= 15:
            print("The silo is already full")
            return
        elif number >= 15 or number <= 0:
            print("An error occurred")
        elif ball.lower() == 'x':
            number = (2 * number) + 1
        elif ball.lower() == 'o':
            number = 2 * number
        else:
            print("Invalid Input error")

        cal_list[Silo_number - 1] = number
        self.index_list = list(map(lambda y: y - 1, cal_list))

        for i in range(self.Total_Silo):
            self.next_state.append(self.state[self.index_list[i]])
        
        #print states
        print(f"State {self.var+1} is : ", self.next_state)
        self.var += 1
        self.buffer.append(self.next_state)
        self.reward_generator(self.next_state)


def nxt_level_print():
    if silo_game_instance.verify_index_generater() == 1:
        for i in range(5):
            silo_game_instance.calculate_next_state('o', i)
            silo_game_instance.verify_index_generater()
        for i in range(5):        
            silo_game_instance.calculate_next_state('x', i)
            silo_game_instance.verify_index_generater()
    else:
        print("There's an error in initial state initialization of Silos ")

# usage
silo_game_instance = SiloGame()

nxt_level_print()

for i in range(5):
    s = int(input("Enter the next state number to descend: "))
    if silo_game_instance.state_selector(s) == 1:
        nxt_level_print()
    else:
        print("Error in state input")
 