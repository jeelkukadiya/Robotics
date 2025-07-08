class demo:
    two_o_mode_check=False

    def check_2_o_winning_condition(self, basket_stacks):
        cnt = 0
        for i, basket in enumerate(basket_stacks):
            if basket == ['o','o','o'] or  basket == ['o','x','o'] or basket == ['x','o','o']:
                cnt += 1
        if cnt == 2:
            return True
        else:
            return False


    def evaluate_priority(self, basket):
        if self.two_o_mode_check:
            if basket == ['', '', '']:
                return 3
            elif basket == ['x', '', '']:
                return 2
            elif basket == ['o', '', '']:
                return 1
            elif basket == ['x', 'o', '']:
                return 7
            elif basket == ['x', 'x', '']:
                return 4
            elif basket == ['x', 'x', '']:
                return 6
            elif basket == ['o', 'o', '']:
                return 5
            else:
                return 0  # Def_for_2_x
        else:
            if basket == ['', '', '']:
                return 3
            elif basket == ['x', '', '']:
                return 2
            elif basket == ['o', '', '']:
                return 1
            elif basket == ['x', 'o', '']:
                return 7
            elif basket == ['x', 'x', '']:
                return 5
            elif basket == ['o', 'x', '']:
                return 6
            elif basket == ['o', 'o', '']:
                return 4
            else:
                return 0  # Off


    def apply_move(self, basket_stack):
        for i, ball in enumerate(basket_stack):
            if ball == '':
                basket_stack[i] = 'x'
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

    def main(self,basket_stacks):
        
        self.two_o_mode_check = self.check_2_o_winning_condition(basket_stacks)

        selected_move = self.select_move(basket_stacks)
        print("Silo Selected By Red team : ",selected_move)

        self.apply_move(basket_stacks[selected_move])

        # print("Next state of basket stacks:", basket_stacks)

        return selected_move