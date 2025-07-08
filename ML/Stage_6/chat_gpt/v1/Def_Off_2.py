class Demo:
    one_x_mode_check = False
    two_x_mode_check = False

    def check_2_x_winning_condition(self, basket_stacks):
        cnt = 0
        for i, basket in enumerate(basket_stacks):
            if basket == [-1, -1, -1] or  basket == [-1, 1, -1] or basket == [1, -1, -1]:
                cnt += 1
        return cnt == 2

    def check_1_x_winning_condition(self, basket_stacks):
        x_count = 0
        o_count = 0
        x_x_empty_count = 0
        xo_count = 0

        for basket in basket_stacks:
            if basket == [-1, -1, -1] or basket == [-1, 1, -1] or basket == [1, -1, -1]:
                x_count += 1
            elif basket == [-1, -1, 0]:
                x_x_empty_count += 1
            elif basket == [1, 1, 1] or basket == [1, -1, 1] or basket == [-1, 1, 1]:
                o_count += 1
            elif basket == [-1, 1, 0] or basket == [1, -1, 0]:
                xo_count += 1

        return x_count == 1 and o_count <= 2 and x_x_empty_count <= 2 and xo_count == 0

    def evaluate_priority(self, basket):
        if self.one_x_mode_check:
            if basket == [0, 0, 0]:
                return 3
            elif basket == [1, 0, 0]:
                return 2
            elif basket == [-1, 0, 0]:
                return 1
            elif basket == [1, -1, 0]:
                return 7
            elif basket == [1, 1, 0]:
                return 4
            elif basket == [-1, 1, 0]:
                return 6
            elif basket == [-1, -1, 0]:
                return 5
            else:
                return 0  # Def_for_1_x
        if self.two_x_mode_check:
            if basket == [0, 0, 0]:
                return 3
            elif basket == [1, 0, 0]:
                return 2
            elif basket == [-1, 0, 0]:
                return 1
            elif basket == [1, -1, 0]:
                return 7
            elif basket == [1, 1, 0]:
                return 4
            elif basket == [-1, 1, 0]:
                return 6
            elif basket == [-1, -1, 0]:
                return 5
            else:
                return 0  # Def_for_2_x
        else:
            if basket == [0, 0, 0]:
                return 3
            elif basket == [1, 0, 0]:
                return 2
            elif basket == [-1, 0, 0]:
                return 1
            elif basket == [1, -1, 0]:
                return 7
            elif basket == [1, 1, 0]:
                return 5
            elif basket == [-1, 1, 0]:
                return 6
            elif basket == [-1, -1, 0]:
                return 4
            else:
                return 0  # Off

    def apply_move(self, basket_stack):
        for i, ball in enumerate(basket_stack):
            if ball == 0:
                basket_stack[i] = 1
                return

    def select_move(self, basket_stacks):
        max_priority = 0
        selected_move = None

        for i, basket in enumerate(basket_stacks):
            priority = self.evaluate_priority(basket)
            if priority > max_priority:
                max_priority = priority
                selected_move = i

        return selected_move

    def main(self, basket_stacks):
        self.one_x_mode_check = self.check_1_x_winning_condition(basket_stacks)
        self.two_x_mode_check = self.check_2_x_winning_condition(basket_stacks)

        selected_move = self.select_move(basket_stacks)
        return selected_move