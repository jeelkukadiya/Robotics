class Reward:
    def __init__(self):
        self.red_reward = 0
        self.blue_reward = 0
        self.blue_win = 0
        self.red_win = 0

    def reward_func(self, final_silo_state):
        self.blue_win = 0
        self.red_win = 0
        self.red_reward = 0
        self.blue_reward = 0

        for i in final_silo_state:
            if i == [1, 1, 1] or i == [1, -1, 1] or i == [-1, 1, 1]:
                self.blue_reward += 10
                self.red_reward  += -10
                self.blue_win += 1
            elif i == [-1, -1, -1] or i == [-1, 1, -1] or i == [1, -1, -1]:
                self.blue_reward += -10
                self.red_reward  += 10
                self.red_win += 1

        if self.blue_win == 3:
            self.blue_reward += 100
            self.red_reward  += -100
        elif self.red_win == 3:
            self.red_reward += 100
            self.blue_reward += -100

        return self.blue_reward