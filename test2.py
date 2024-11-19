class GameNode:
    def __init__(self, state, player, actions, utilities=None):
        self.state = state
        self.player = player  # The player making a decision at this node
        self.actions = actions  # List of possible actions
        self.utilities = utilities  # Utilities if it's a terminal node
        self.children = {}  # Maps actions to resulting GameNode objects
        self.optimal_action = None

    def add_child(self, action, child_node):
        self.children[action] = child_node

def compute_spne_path(node):
    # If terminal node, return the utility and empty path
    if node.utilities:
        return node.utilities, []

    # Otherwise, compute utilities recursively for each action
    optimal_utility = None
    spne_path = []

    for action in node.actions:
        child_node = node.children[action]
        child_utility, child_path = compute_spne_path(child_node)

        # Choose the optimal action for the current player
        if optimal_utility is None or (
            node.player == 1 and child_utility[0] > optimal_utility[0]
        ) or (
            node.player == 2 and child_utility[1] > optimal_utility[1]
        ):
            optimal_utility = child_utility
            node.optimal_action = action
            spne_path = [(node.player, action, node.state)] + child_path

    return optimal_utility, spne_path

# Define the game tree
root = GameNode(state="Start", player=1, actions=["4-3-3", "4-4-2"])
child1 = GameNode(state="After 4-3-3", player=2, actions=["4-4-2", "4-5-1"])
child2 = GameNode(state="After 4-4-2", player=2, actions=["4-3-3", "3-5-2"])
child1.add_child("4-4-2", GameNode(state="Terminal 1", player=None, actions=[], utilities=(5, 3)))
child1.add_child("4-5-1", GameNode(state="Terminal 2", player=None, actions=[], utilities=(4, 4)))
child2.add_child("4-3-3", GameNode(state="Terminal 3", player=None, actions=[], utilities=(2, 5)))
child2.add_child("3-5-2", GameNode(state="Terminal 4", player=None, actions=[], utilities=(3, 2)))

root.add_child("4-3-3", child1)
root.add_child("4-4-2", child2)

# Compute SPNE path
_, spne_path = compute_spne_path(root)
for step in spne_path:
    print(f"Player {step[0]} chooses {step[1]} at state {step[2]}")