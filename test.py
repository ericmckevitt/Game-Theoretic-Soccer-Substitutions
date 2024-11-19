import itertools

class SoccerGameWithInduction:
    def __init__(self, max_decisions=3):
        self.formations = ["4-3-3", "4-4-2", "5-3-2"]
        self.max_decisions = max_decisions
        self.game_tree = {}
        self.optimal_path = []  # To store the path through the game tree
        self.initialize_game_tree()

    def initialize_game_tree(self):
        """ Initializes the game tree with all possible states """
        for decision_count in range(1, self.max_decisions + 1):
            for team1_formation in self.formations:
                for team2_formation in self.formations:
                    for g1, g2 in itertools.product(range(6), repeat=2):  # Example score range [0, 5]
                        state = (decision_count, team1_formation, team2_formation, g1, g2)
                        self.game_tree[state] = None  # No utility assigned yet

    def expected_goals_scored(self, formation1, formation2):
        """ Simple function to calculate expected goals scored based on formations (dummy values) """
        if formation1 == "4-3-3":
            return 1.2 - 0.3 * (formation2 == "5-3-2")  # Example adjustment for opponent's formation
        elif formation1 == "4-4-2":
            return 1.0
        elif formation1 == "5-3-2":
            return 0.8 + 0.2 * (formation2 == "4-3-3")  # Example
        return 1.0

    def compute_utilities(self):
        """ Compute utilities for all states in the game tree using backward induction """
        for state in reversed(sorted(self.game_tree.keys(), key=lambda x: x[0])):  # Sort by decision depth
            decision_count, f1, f2, g1, g2 = state
            if decision_count == self.max_decisions:
                # Terminal state: assign a simple utility
                utility = g1 - g2  # Difference in goals as utility, can be adjusted
                self.game_tree[state] = utility
            else:
                # Compute expected utility based on possible future states
                max_utility = float('-inf')
                best_action = None

                # Iterate over all possible next formations for each team
                for next_f1 in self.formations:
                    for next_f2 in self.formations:
                        next_g1 = g1 + self.expected_goals_scored(next_f1, f2)
                        next_g2 = g2 + self.expected_goals_scored(next_f2, f1)

                        # Cap the goals to keep it realistic
                        next_g1 = min(int(next_g1), 5)
                        next_g2 = min(int(next_g2), 5)

                        next_state = (decision_count + 1, next_f1, next_f2, next_g1, next_g2)
                        next_utility = self.game_tree.get(next_state, 0)  # Default to 0 if not found

                        if next_utility > max_utility:
                            max_utility = next_utility
                            best_action = (next_f1, next_f2, next_g1, next_g2)

                # Assign the maximum utility found
                self.game_tree[state] = max_utility

                # Store the best action taken at this state for tracing the path
                if best_action:
                    self.optimal_path.append((state, best_action, max_utility))

    def display_optimal_path(self):
        """ Display the optimal path through the game tree with utilities """
        print("Optimal Path Through the Game Tree:")
        for state, action, utility in self.optimal_path:
            print(f"State: {state} -> Next Action: {action}, Utility: {utility}")

# Initialize and solve the game
soccer_game = SoccerGameWithInduction()
soccer_game.compute_utilities()
soccer_game.display_optimal_path()