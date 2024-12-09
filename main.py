from utilities import Formation, Team, utility

class GameNode:
    def __init__(self, state, player, depth):
        self.state = state  # Tuple representing the game state 
        self.player = player  # Player making the move
        self.children = []  # Subsequent states
        self.utility = None  # Utility value, to be determined later
        self.depth = depth  # Depth in the tree

def build_game_tree(state, player, depth, max_depth):
    if depth == max_depth:
        node = GameNode(state, player, depth)
        # Assuming t1 and t2 are passed to the function or globally accessible
        t1.formation = state[0]  # Assigning Team 1's formation
        t2.formation = state[1]  # Assigning Team 2's formation (assuming a two-player state tuple)
        node.utility = utility(0, 0, t1, t2)  # TODO: You can customize G1 and G2 as needed
        return node
    
    node = GameNode(state, player, depth)
    next_player = "Player 1" if player == "Player 2" else "Player 2"
    
    for formation in allowed_formations:
        new_state = state + (formation,)
        child_node = build_game_tree(new_state, next_player, depth + 1, max_depth)
        node.children.append(child_node)
    
    return node

def backward_induction(node):
    if not node.children:
        return node.utility  # Terminal node, return calculated utility

    if node.player == "Player 1":
        # Maximizing player
        node.utility = max(backward_induction(child) for child in node.children)
    else:
        # Player 2 responds optimally (minimizing strategy)
        node.utility = min(backward_induction(child) for child in node.children)
    
    return node.utility

allowed_formations = [
    Formation(4, 3, 3),
    Formation(4, 4, 2),
    Formation(5, 3, 2),
    Formation(4, 5, 1),
    Formation(3, 5, 2),
]

t1 = Team("ManchesterCity", Formation(4, 3, 3))
t2 = Team("FCDallas", Formation(4, 5, 1))
t1.load_stats_from_file("./team_data.csv")
t2.load_stats_from_file("./team_data.csv")

# Build and solve the game tree
initial_state = ()  # No moves made yet
root = build_game_tree(initial_state, "Player 1", 0, 10)
optimal_strategy = backward_induction(root)
print("optimal strategy:", optimal_strategy)