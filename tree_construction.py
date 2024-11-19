import math

# Define diminishing returns function
def diminishing_returns(x):
    return 1 - math.e ** (-0.7 * x)

# Define a class for game tree nodes
class GameTreeNode:
    def __init__(self, turn, expected_goals_i, expected_goals_j, formation=None):
        self.turn = turn  # Whose turn it is to make a decision (i or j)
        self.expected_goals_i = expected_goals_i  # Expected goals for team i
        self.expected_goals_j = expected_goals_j  # Expected goals for team j
        self.formation = formation  # Formation chosen to reach this node
        self.children = []  # Child nodes (branches)

    def add_child(self, child_node):
        self.children.append(child_node)

# Define initial skill levels for teams i and j
s_ai = 0.5  # Skill of team i in attacking
s_di = 0.5  # Skill of team i in defending
s_aj = 0.5  # Skill of team j in attacking
s_dj = 0.5  # Skill of team j in defending

# Generate the game tree
def generate_game_tree(depth, current_node, current_turn='i', max_depth=3):
    if depth >= max_depth:  # Base case: terminal node
        return
    
    # Calculate new expected goals for both formations for current player
    if current_turn == 'i':
        new_goals_i_1 = max(current_node.expected_goals_i + s_ai * diminishing_returns(4) - s_dj * diminishing_returns(3), 0)
        new_goals_i_2 = max(current_node.expected_goals_i + s_ai * diminishing_returns(5) - s_dj * diminishing_returns(2), 0)
        new_goals_j = current_node.expected_goals_j
        # Create children nodes for both formations
        child1 = GameTreeNode('j', new_goals_i_1, new_goals_j, formation='4-3-3')
        child2 = GameTreeNode('j', new_goals_i_2, new_goals_j, formation='5-3-2')
    else:
        new_goals_j_1 = max(current_node.expected_goals_j + s_aj * diminishing_returns(4) - s_di * diminishing_returns(3), 0)
        new_goals_j_2 = max(current_node.expected_goals_j + s_aj * diminishing_returns(5) - s_di * diminishing_returns(2), 0)
        new_goals_i = current_node.expected_goals_i
        # Create children nodes for both formations
        child1 = GameTreeNode('i', new_goals_i, new_goals_j_1, formation='4-3-3')
        child2 = GameTreeNode('i', new_goals_i, new_goals_j_2, formation='5-3-2')

    # Add children to the current node
    current_node.add_child(child1)
    current_node.add_child(child2)

    # Recursively generate tree for each child
    generate_game_tree(depth + 1, child1, 'j' if current_turn == 'i' else 'i', max_depth)
    generate_game_tree(depth + 1, child2, 'j' if current_turn == 'i' else 'i', max_depth)

# Initialize the root node and generate the game tree
root_node = GameTreeNode('i', 0, 0)
generate_game_tree(0, root_node)

# Function to display the game tree
def display_game_tree(node, depth=0):
    formation_info = f", Formation = {node.formation}" if node.formation else ""
    print(f"{' ' * (depth * 2)}Node: ({node.turn}, {node.expected_goals_i:.3f}, {node.expected_goals_j:.3f}{formation_info})")
    for child in node.children:
        display_game_tree(child, depth + 1)

# Display the generated game tree
# display_game_tree(root_node)

def find_spne(node):
    # Base case: if the node is a terminal node (no children)
    if not node.children:
        # Utility for team 'i' is calculated as (G_i - G_j)
        node.utility = node.expected_goals_i - node.expected_goals_j
        return node.utility

    # Recursive case: calculate SPNE for each child node
    child_utilities = []
    for child in node.children:
        utility = find_spne(child)
        child_utilities.append((utility, child))

    # Select the move with the maximum utility based on whose turn it is
    if node.turn == 'i':
        # Maximize team 'i's utility
        best_child = max(child_utilities, key=lambda x: x[0])
    else:
        # Minimize team 'i's utility (equivalent to maximizing team 'j's utility)
        best_child = min(child_utilities, key=lambda x: x[0])

    # Update the node's utility to reflect the optimal choice
    node.utility = best_child[0]
    node.best_child = best_child[1]  # Track the best move

    return node.utility

def display_spne_path(node, depth=0):
    # Display the node and its optimal move
    print(f"{' ' * (depth * 2)}Node: ({node.turn}, {node.expected_goals_i:.3f}, {node.expected_goals_j:.3f}), Utility: {node.utility:.3f}")
    if hasattr(node, 'best_child') and node.best_child:
        formation = getattr(node.best_child, 'formation', 'N/A')  # Safely get formation
        print(f"{' ' * (depth * 2)}--> Optimal Move: Formation = {formation}")
        display_spne_path(node.best_child, depth + 1)

# Calculate the SPNE starting from the root node
find_spne(root_node)

# Display the optimal path (SPNE)
display_spne_path(root_node)