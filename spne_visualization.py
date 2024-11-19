import math
import networkx as nx
import matplotlib.pyplot as plt

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
        self.is_optimal = False  # Flag to mark if the node is part of the SPNE path

    def add_child(self, child_node):
        self.children.append(child_node)

# Generate the game tree (similar logic as before)
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

# SPNE Calculation
def find_spne(node):
    if not node.children:
        node.utility = node.expected_goals_i - node.expected_goals_j
        return node.utility

    child_utilities = []
    for child in node.children:
        utility = find_spne(child)
        child_utilities.append((utility, child))

    # Determine the best child based on the player's turn
    if node.turn == 'i':
        best_child = max(child_utilities, key=lambda x: x[0])
    else:
        best_child = min(child_utilities, key=lambda x: x[0])

    # Update the node's utility and mark only the best child as optimal
    node.utility = best_child[0]
    node.best_child = best_child[1]
    node.best_child.is_optimal = True  # Mark the best child as part of the SPNE path

    return node.utility

# Visualization with networkx
def visualize_game_tree(node, graph=None, parent=None, pos=None, level=0, x=0, dx=1.0):
    if graph is None:
        graph = nx.DiGraph()
        pos = {}

    node_label = f"{node.turn}, {node.expected_goals_i:.2f}, {node.expected_goals_j:.2f}\n({node.formation})"
    graph.add_node(node_label, color='green' if node.is_optimal else 'black')
    pos[node_label] = (x, -level)
    
    if parent:
        graph.add_edge(parent, node_label)

    for i, child in enumerate(node.children):
        visualize_game_tree(child, graph, node_label, pos, level + 1, x - dx / 2 + i * dx, dx / 2)
    
    return graph, pos

# Initialize parameters and root node
s_ai, s_di, s_aj, s_dj = 0.5, 0.5, 0.5, 0.5
root_node = GameTreeNode('i', 0, 0)
generate_game_tree(0, root_node)
find_spne(root_node)

# Visualize the game tree
graph, pos = visualize_game_tree(root_node)
node_colors = [graph.nodes[node]['color'] for node in graph.nodes()]

plt.figure(figsize=(12, 8))
nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=2000, font_size=6, font_color='white')
plt.title("Game Tree Visualization with Optimal Subgames Highlighted")
plt.show()