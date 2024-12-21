import math
import networkx as nx
import matplotlib.pyplot as plt

# Define diminishing returns function
def diminishing_returns(x):
    return 1 - math.e ** (-0.7 * x)

allowed_formations = ['4-3-3', '4-4-2', '5-3-2', '4-5-1', '3-5-2']
# allowed_formations = ['4-4-2', '5-3-2']

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

def generate_game_tree(depth, current_node, current_turn='i', max_depth=5):
    if depth >= max_depth:  # Base case: terminal node
        return
    
    for formation in allowed_formations:
        # Calculate new expected goals for formations
        if current_turn == 'i':
            new_goals_i = max(current_node.expected_goals_i + s_ai * diminishing_returns(int(formation[0])) - s_dj * diminishing_returns(int(formation[2])), 0)
            new_goals_j = current_node.expected_goals_j
            # Create a child node for this formation
            child = GameTreeNode('j', new_goals_i, new_goals_j, formation=formation)
        else:
            new_goals_j = max(current_node.expected_goals_j + s_aj * diminishing_returns(int(formation[0])) - s_di * diminishing_returns(int(formation[2])), 0)
            new_goals_i = current_node.expected_goals_i
            # Create a child node for this formation
            child = GameTreeNode('i', new_goals_i, new_goals_j, formation=formation)

        # Add the child to the current node
        current_node.add_child(child)

        # Recursively generate the tree for the child
        generate_game_tree(depth + 1, child, 'j' if current_turn == 'i' else 'i', max_depth)

# SPNE Calculation with Path Retrieval
def find_spne_with_path(node):
    if not node.children:
        node.utility = node.expected_goals_i - node.expected_goals_j
        node.is_optimal = True  # Mark leaf node as part of SPNE
        return node.utility, [node]

    child_utilities = []
    for child in node.children:
        utility, path = find_spne_with_path(child)
        child_utilities.append((utility, child, path))

    # Determine the best child based on the player's turn
    if node.turn == 'i':
        best_child = max(child_utilities, key=lambda x: x[0])
    else:
        best_child = min(child_utilities, key=lambda x: x[0])

    # Update the node's utility
    node.utility = best_child[0]
    node.best_child = best_child[1]

    # Mark this node and the best child as part of the SPNE path
    node.is_optimal = True
    best_child[1].is_optimal = True

    # Return the utility and path (including the current node)
    return node.utility, [node] + best_child[2]

# Function to display the SPNE path as text
def display_spne_path(path):
    print("SPNE Path:")
    for step, node in enumerate(path):
        print(f"Step {step + 1}:")
        print(f"  Turn: {node.turn}")
        print(f"  Formation: {node.formation}")
        print(f"  Expected Goals - Team i: {node.expected_goals_i:.2f}, Team j: {node.expected_goals_j:.2f}")
        print()

# Function to display the SPNE path as a tuple
def display_spne_path_as_tuples(path):
    print("SPNE Path:\n")
    for step, node in enumerate(path):
        # Determine the formations for both teams
        formation_i = node.formation if node.turn == 'i' else path[step - 1].formation
        formation_j = node.formation if node.turn == 'j' else path[step - 1].formation if step > 0 else None
        
        # Print the tuple and the decision being made
        print(f"Step {step + 1}: {node.turn}'s turn")
        print(f"  Decision Tuple: ({node.turn}, {formation_i or 'None'}, {formation_j or 'None'})")
        if node.formation:
            print(f"  -> {node.turn} picks formation: {node.formation}")
        print(f"  Expected Goals - Team i: {node.expected_goals_i:.2f}, Team j: {node.expected_goals_j:.2f}")
        print()

# Visualization with networkx
def visualize_game_tree(node, graph=None, parent=None, pos=None, level=0, x=0, dx=1.0, parent_edge_label=None, is_root=True):
    if graph is None:
        graph = nx.DiGraph()
        pos = {}

    # Create a unique identifier for internal use and a separate display label
    unique_id = f"{node.turn}_{id(node)}"  # Unique internal ID for the node
    display_label = f"{node.turn}, {node.expected_goals_i:.2f}, {node.expected_goals_j:.2f}"
    
    # Set node color: green if it is part of the SPNE path, otherwise black
    node_color = 'green' if node.is_optimal else 'black'
    
    # Add the node using the unique identifier but display only the label
    graph.add_node(unique_id, label=display_label, color=node_color)
    pos[unique_id] = (x, -level)
    
    if parent:
        # Add edge from parent to current node with the formation as the label
        graph.add_edge(parent, unique_id)
        nx.set_edge_attributes(graph, {(parent, unique_id): parent_edge_label}, "label")

    for i, child in enumerate(node.children):
        # Pass the formation of the child node as the label for the edge
        visualize_game_tree(child, graph, unique_id, pos, level + 1, x - dx / 2 + i * dx, dx / 2, child.formation, is_root=False)
    
    return graph, pos

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

if __name__ == "__main__":
    mode = input("Select Text Output (t) or Graphical Output (g): ").lower()
    while mode not in ["g", "t"]:
        print("Invalid selection.")
        mode = input("Select Text Output (t) or Graphical Output (g): ").lower()

    # Initialize parameters and root node
    s_ai, s_di, s_aj, s_dj = 0.76, 0.88, 0.71, 0.35
    root_node = GameTreeNode('i', 0, 0)

    # Generate the game tree
    generate_game_tree(0, root_node, max_depth=4)
    # Find the SPNE and retrieve the path
    _, spne_path = find_spne_with_path(root_node)

    if mode == "t":
        
        # Display the SPNE path
        display_spne_path_as_tuples(spne_path)
        
    elif mode == "g":
        root_node = GameTreeNode('i', 0, 0)
        generate_game_tree(0, root_node)
        find_spne(root_node)

        # Visualize the game tree
        graph, pos = visualize_game_tree(root_node)
        node_colors = [graph.nodes[node]['color'] for node in graph.nodes()]
        node_labels = nx.get_node_attributes(graph, 'label')  # Retrieve node labels for display
        edge_labels = nx.get_edge_attributes(graph, 'label')  # Retrieve edge labels for display

        plt.figure(figsize=(12, 8))
        nx.draw(graph, pos, labels=node_labels, with_labels=True, node_color=node_colors, edge_color='gray', node_size=1500, font_size=5, font_color='white')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)  # Draw edge labels
        plt.title("Game Tree Visualization with Root Node Always Green")
        plt.show()