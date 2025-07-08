def check_2_x_winning_condition(basket_stacks):
    cnt = 0
    for i, basket in enumerate(basket_stacks):
        if basket == ['x','x','x'] or  basket == ['x','o','x'] or basket == ['o','x','x']:
            cnt += 1
    if cnt == 2:
        return True
    else:
        return False

#base stretegy for offensive and deffensive
def evaluate_priority(basket):
    if two_x_mode_check:
        if basket == ['', '', '']:
            return 3
        elif basket == ['o', '', '']:
            return 2
        elif basket == ['x', '', '']:
            return 1
        elif basket == ['o', 'x', '']:
            return 7
        elif basket == ['o', 'o', '']:
            return 4
        elif basket == ['x', 'o', '']:
            return 6
        elif basket == ['x', 'x', '']:
            return 5
        else:
            return 0  # Def_for_2_x
    else:
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
            return 0  # Offensive


def apply_move(basket_stack):
    for i, ball in enumerate(basket_stack):
        if ball == '':
            basket_stack[i] = 'o'
            return


def select_move(basket_stacks):
    max_priority = 0
    selected_move = None

    for i, basket in enumerate(basket_stacks):
        priority = evaluate_priority(basket)
        if priority > max_priority:
            max_priority = priority
            selected_move = i

    return selected_move


# Example usage:
#right_mostplace=top &left_mostplace=bottom

#silo_state input from CV
basket_stacks =   [['o', 'x', ''], ['x', '', ''], ['o', '', ''], ['x', 'x', ''], ['o', 'o', 'o']]

#deffensive mode on or not?
two_x_mode_check = check_2_x_winning_condition(basket_stacks)
#print(two_x_mode_check)

selected_move = select_move(basket_stacks)
print("selected silo:",selected_move+1)

# apply_move(basket_stacks, selected_move)

apply_move(basket_stacks[selected_move])

print("Next state of silo state:")
print(basket_stacks)