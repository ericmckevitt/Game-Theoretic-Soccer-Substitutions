import math

# Define diminishing returns function
def diminishing_returns(x):
    return 1 - math.e ** (-0.7 * x)

# Define a class for game tree nodes
class GameTreeNode:
    def __init__(self, turn, expected_goals_i, expected_goals_j):
        self.turn = turn  # Whose turn it is to make a decision (i or j)
        self.expected_goals_i = expected_goals_i  # Expected goals for team i
        self.expected_goals_j = expected_goals_j  # Expected goals for team j
        self.children = []  # Child nodes (branches)

    def add_child(self, child_node):
        self.children.append(child_node)

# Define initial skill levels for teams i and j
s_ai = 0.8  # Skill of team i in attacking
s_di = 0.6  # Skill of team i in defending
s_aj = 0.65  # Skill of team j in attacking
s_dj = 0.75  # Skill of team j in defending

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
        child1 = GameTreeNode('j', new_goals_i_1, new_goals_j)
        child2 = GameTreeNode('j', new_goals_i_2, new_goals_j)
    else:
        new_goals_j_1 = max(current_node.expected_goals_j + s_aj * diminishing_returns(4) - s_di * diminishing_returns(3), 0)
        new_goals_j_2 = max(current_node.expected_goals_j + s_aj * diminishing_returns(5) - s_di * diminishing_returns(2), 0)
        new_goals_i = current_node.expected_goals_i
        # Create children nodes for both formations
        child1 = GameTreeNode('i', new_goals_i, new_goals_j_1)
        child2 = GameTreeNode('i', new_goals_i, new_goals_j_2)

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
    # print(f"{' ' * (depth * 2)}Node: Turn = {node.turn}, Expected Goals (i) = {node.expected_goals_i:.2f}, Expected Goals (j) = {node.expected_goals_j:.2f}")
    print(f"{' ' * (depth * 2)}Node: ({node.turn}, {node.expected_goals_i:.3f}, {node.expected_goals_j:.3f})")
    for child in node.children:
        display_game_tree(child, depth + 1)

# Display the generated game tree
display_game_tree(root_node)