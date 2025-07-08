# mcts.py
import random
import math

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.wins = 0
        self.visits = 0
        self.children = []

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_valid_moves())

    def select_child(self, exploration_parameter):
        max_ucb = -float('inf')
        selected_child = None
        for child in self.children:
            if child.visits == 0:
                ucb = float('inf')
            else:
                ucb = child.wins / child.visits + exploration_parameter * math.sqrt(math.log(self.visits) / child.visits)
            if ucb > max_ucb:
                max_ucb = ucb
                selected_child = child
        return selected_child

    def expand(self):
        valid_moves = self.state.get_valid_moves()
        for move in valid_moves:
            new_state = self.state.copy()
            new_state.make_move(move, new_state.current_player)
            self.children.append(Node(new_state, parent=self))

    def rollout(self):
        state = self.state.copy()
        while not state.is_full() and not state.check_win(1) and not state.check_win(-1):
            move = random.choice(state.get_valid_moves())
            state.make_move(move, state.current_player)
            state.switch_player()
        return state.get_winner()

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)


class MCTS:
    def __init__(self, exploration_parameter=1.41, iterations=1000):
        self.exploration_parameter = exploration_parameter
        self.iterations = iterations

    def search(self, initial_state):
        root = Node(initial_state)
        for _ in range(self.iterations):
            node = root
            # Selection
            while not node.state.is_full() and not node.state.check_win(1) and not node.state.check_win(-1) and node.is_fully_expanded():
                node = node.select_child(self.exploration_parameter)
            # Expansion
            if not node.state.is_full() and not node.state.check_win(1) and not node.state.check_win(-1):
                node.expand()
                node = random.choice(node.children)
            # Rollout
            result = node.rollout()
            # Backpropagation
            node.backpropagate(result)
        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.state.get_valid_moves()[0]  # Return the column of the best move
