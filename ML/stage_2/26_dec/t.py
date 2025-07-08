class TreeNode:
    def __init__(self, State):
        self.State = State
        self.nextState = []

def print_tree(node, level=0):
    if node:
        print("  " * level + str(node.State))
        print_tree(node.nextState, level + 1)

root = TreeNode([["","",""],["","",""],["","",""]])

root.nextState = [["","",""],["","",""],["","","O"]]

print_tree(root)


