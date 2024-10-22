import operator
from copy import deepcopy


def get_action_name(action_index: int, is_row: bool, total_actions: int = 0) -> chr:
    if is_row:
        return chr(ord('A') + action_index)
    else:
        return chr(ord('Z') - total_actions + action_index + 1)


def get_action_index(action: chr, total_row_actions: int) -> (bool, int):
    is_row = ord(action) - ord('A') < total_row_actions
    if is_row:
        return True, ord(action) - ord('A')
    return False, ord('Z') - ord(action)


def is_col_dominated(payoff_matrix, eliminated, action: int, strongly: bool = True) -> bool:
    comparator = operator.le if strongly else operator.lt
    for j in range(len(payoff_matrix[0])):
        if j == action or get_action_name(j, False, len(payoff_matrix[0])) in eliminated:
            continue

        # Check if strategy at action is strongly dominated by strategy j
        is_dominated = True

        for k in range(len(payoff_matrix)):  # For each opponent's strategy
            if get_action_name(k, True, len(payoff_matrix)) in eliminated:
                continue
            p2_payoff_current = payoff_matrix[k][action][1]
            p2_payoff_other = payoff_matrix[k][j][1]

            if comparator(p2_payoff_other, p2_payoff_current):
                is_dominated = False
                break  # No need to check further

        if is_dominated:
            return True  # The strategy is strongly dominated

    return False  # The strategy is not strongly dominated


def is_row_dominated(payoff_matrix, eliminated: list[chr], action: int, strongly: bool = True) -> bool:
    comparator = operator.le if strongly else operator.lt
    for i in range(len(payoff_matrix)):
        if i == action or get_action_name(i, True, len(payoff_matrix)) in eliminated:
            continue

        # Check if strategy at action is strongly dominated by strategy j
        is_dominated = True

        for k in range(len(payoff_matrix[0])):  # For each opponent's strategy
            if get_action_name(k, False, len(payoff_matrix[0])) in eliminated:
                continue
            p1_payoff_current = payoff_matrix[action][k][0]
            p1_payoff_other = payoff_matrix[i][k][0]

            if not comparator(p1_payoff_current, p1_payoff_other):
                is_dominated = False
                break  # No need to check further

        if is_dominated:
            return True  # The strategy is strongly dominated

    return False  # The strategy is not strongly dominated


def is_strongly_dominated(payoff_matrix, action: int, is_row: bool) -> bool:
    if is_row:
        return is_row_dominated(payoff_matrix, [], action)
    else:
        return is_col_dominated(payoff_matrix, [], action)


def is_weakly_dominated(payoff_matrix, eliminated, action: int, is_row: bool) -> bool:
    if is_row:
        return is_row_dominated(payoff_matrix, eliminated,  action, False)
    else:
        return is_col_dominated(payoff_matrix, eliminated, action, False)


def eliminate(payoff_matrix, strategies: list[chr], total_row_actions):
    for strategy in strategies:
        is_row, action_index = get_action_index(strategy, total_row_actions)
        if is_row:
            del payoff_matrix[action_index]
        else:
            for i in range(len(payoff_matrix)):
                del payoff_matrix[i][action_index]


class NormalFormGame:
    """
    A class to represent a Normal Form game in the context of game theory
    :var payoffs is a double list of tuples representing the rewards. Player 1's action is the first index and Player 2's action is the second index In the tuple, the first entry is the first player's reward and the second entry is the second player's reward
    """
    def __init__(self, input_matrix):
        if isinstance(input_matrix, str):
            content: str
            with open(input_matrix) as file:
                content = file.read()
            self.payoffs: list[list[tuple[int, int]]] = parse_payoff(content)
        else:
            self.payoffs = input_matrix

    def __is_strategy_pareto_optimal(self, row_action: int, col_action: int) -> bool:
        strategy_payoff = self.payoffs[row_action][col_action]

        for i in range(len(self.payoffs)):
            for j in range(len(self.payoffs[0])):
                other_payoff = self.payoffs[i][j]
                # Check if there's an improvement for one player without hurting the other
                if (other_payoff[0] >= strategy_payoff[0] and other_payoff[1] > strategy_payoff[1]) or \
                   (other_payoff[0] > strategy_payoff[0] and other_payoff[1] >= strategy_payoff[1]):
                    return False

        return True

    def find_pareto_optimal(self) -> list[str]:
        pareto_optimal_solutions = []
        for i in range(len(self.payoffs)):
            for j in range(len(self.payoffs[i])):
                if self.__is_strategy_pareto_optimal(i, j):
                    row_action = get_action_name(i, True, len(self.payoffs))
                    col_action = get_action_name(j, False, len(self.payoffs[0]))
                    pareto_optimal_solutions.append(row_action + col_action)
        return pareto_optimal_solutions

    def print_pareto_optimal_solutions(self):
        print("Pareto Optimal: ", end='')
        strategies = self.find_pareto_optimal()
        print(", ".join(map(str, strategies)))

    def find_strongly_dominated_strategies(self, payoff_matrix, eliminated=None) -> list[chr]:
        if eliminated is None:
            eliminated = []
        strongly_dominated = []
        for i in range(len(payoff_matrix)):
            if get_action_name(i, True, len(payoff_matrix)) not in eliminated and is_strongly_dominated(payoff_matrix, i, True):
                strongly_dominated.append(get_action_name(i, True))
        for j in range(len(payoff_matrix[0])):
            if get_action_name(j, False, len(payoff_matrix[0])) not in eliminated and is_strongly_dominated(payoff_matrix, j, False):
                strongly_dominated.append(get_action_name(j, False, len(self.payoffs[0])))

        return strongly_dominated

    def find_weakly_dominated_strategies(self, payoff_matrix, eliminated=None) -> list[chr]:
        if eliminated is None:
            eliminated = []
        weakly_dominated = []
        for i in range(len(payoff_matrix)):
            if get_action_name(i, True, len(payoff_matrix)) not in eliminated and is_weakly_dominated(payoff_matrix, eliminated, i, True):
                weakly_dominated.append(get_action_name(i, True))
        for j in range(len(payoff_matrix[0])):
            if get_action_name(j, False, len(payoff_matrix[0])) not in eliminated and is_weakly_dominated(payoff_matrix, eliminated, j, False):
                weakly_dominated.append(get_action_name(j, False, len(self.payoffs[0])))

        return weakly_dominated

    def print_weakly_dominated_solutions(self):
        payoff_matrix = deepcopy(self.payoffs)
        eliminated = []
        print("Weakly Dominated: ")
        strategies = self.find_weakly_dominated_strategies(payoff_matrix)
        if not strategies:
            print("\tNo Weakly Dominated Strategies")
        while strategies:
            print("\tELIMINATE: " + ", ".join(map(str, strategies)))
            eliminated += strategies
            strategies = self.find_weakly_dominated_strategies(payoff_matrix, eliminated)

    def print_strongly_dominated_solutions(self):
        payoff_matrix = deepcopy(self.payoffs)
        eliminated = []
        print("Strongly Dominated: ")
        strategies = self.find_strongly_dominated_strategies(payoff_matrix)
        if not strategies:
            print("\tNo Strongly Dominated Strategies")
        while strategies:
            print("\tELIMINATE: " + ", ".join(map(str, strategies)))
            eliminated += strategies
            strategies = self.find_strongly_dominated_strategies(payoff_matrix, eliminated)

    def print_pure_strategy_equilibria(self):
        print("Pure Strategy Equilibria: ", end='')
        payoff_matrix = deepcopy(self.payoffs)
        nash_equilibria = []
        num_actions_player1 = len(payoff_matrix)
        num_actions_player2 = len(payoff_matrix[0])

        for action1 in range(num_actions_player1):
            for action2 in range(num_actions_player2):
                player1_reward = payoff_matrix[action1][action2][0]
                player2_reward = payoff_matrix[action1][action2][1]

                # Check if Player 1 can do better by changing their action
                player1_better = any(payoff_matrix[other_action][action2][0] > player1_reward
                                     for other_action in range(num_actions_player1))

                # Check if Player 2 can do better by changing their action
                player2_better = any(payoff_matrix[action1][other_action][1] > player2_reward
                                     for other_action in range(num_actions_player2))

                if not player1_better and not player2_better:
                    nash_equilibria.append(get_action_name(action1, True, len(payoff_matrix)) + get_action_name(action2, False, len(payoff_matrix[0])))
        print(", ".join(map(str, nash_equilibria)))
        return nash_equilibria

    def print_minimax_strategy(self):
        print("Minimax Strategy:")
        payoff_matrix = deepcopy(self.payoffs)
        num_actions_player1 = len(payoff_matrix)
        num_actions_player2 = len(payoff_matrix[0])
        minimum_regret = None
        best_action = []
        for action1 in range(num_actions_player1):
            regret_of_action = float('-inf')
            for action2 in range(num_actions_player2):
                best_reward = float('-inf')
                for alternative_action in range(num_actions_player1):
                    best_reward = max(best_reward, payoff_matrix[alternative_action][action2][0])
                regret_of_cell = best_reward - payoff_matrix[action1][action2][0]
                regret_of_action = max(regret_of_cell, regret_of_action)

            # Determine the maximum of the minimum payoffs
            if minimum_regret is None or regret_of_action < minimum_regret:
                minimum_regret = regret_of_action
                best_action = [get_action_name(action1, True)]
            elif regret_of_action == minimum_regret:
                best_action.append(get_action_name(action1, True))
        print("\tRow Player: Choose " + " or ".join(map(str, best_action)))

        minimum_regret = None
        best_action = []
        for action2 in range(num_actions_player2):
            regret_of_action = float('-inf')
            for action1 in range(num_actions_player1):
                best_reward = float('-inf')
                for alternative_action in range(num_actions_player2):
                    best_reward = max(best_reward, payoff_matrix[action1][alternative_action][1])
                regret_of_cell = best_reward - payoff_matrix[action1][action2][1]
                regret_of_action = max(regret_of_cell, regret_of_action)

            # Determine the maximum of the minimum payoffs
            if minimum_regret is None or regret_of_action < minimum_regret:
                minimum_regret = regret_of_action
                best_action = [get_action_name(action2, False, num_actions_player2)]
            elif regret_of_action == minimum_regret:
                best_action.append(get_action_name(action2, False, num_actions_player2))
        print("\tColumn Player: Choose " + " or ".join(map(str, best_action)))

    def print_maximin_strategy(self):
        print("Maximin Strategy:")

        payoff_matrix = deepcopy(self.payoffs)
        num_actions_player1 = len(payoff_matrix)
        num_actions_player2 = len(payoff_matrix[0])

        # Initialize variables to track the best action for both players
        best_action_player1 = None
        best_action_player2 = None
        max_of_mins_player1 = float('-inf')
        max_of_mins_player2 = float('-inf')

        # Calculate maximin strategy for Player 1
        for action1 in range(num_actions_player1):
            min_payoff_player1 = float('inf')

            for action2 in range(num_actions_player2):
                payoff_player1 = payoff_matrix[action1][action2][0]
                min_payoff_player1 = min(min_payoff_player1, payoff_player1)

            if min_payoff_player1 > max_of_mins_player1:
                max_of_mins_player1 = min_payoff_player1
                best_action_player1 = [get_action_name(action1, True)]
            elif min_payoff_player1 == max_of_mins_player1:
                best_action_player1.append(get_action_name(action1, True))

        print("\tRow Player: Choose " + " or ".join(map(str, best_action_player1)))
        # Calculate maximin strategy for Player 2
        for action2 in range(num_actions_player2):
            min_payoff_player2 = float('inf')

            for action1 in range(num_actions_player1):
                payoff_player2 = payoff_matrix[action1][action2][1]
                min_payoff_player2 = min(min_payoff_player2, payoff_player2)

            if min_payoff_player2 > max_of_mins_player2:
                max_of_mins_player2 = min_payoff_player2
                best_action_player2 = [get_action_name(action2, False, num_actions_player2)]
            elif min_payoff_player2 == max_of_mins_player2:
                best_action_player2.append(get_action_name(action2, False, num_actions_player2))
        print("\tColumn Player: Choose " + " or ".join(map(str, best_action_player2)))

        return (best_action_player1, max_of_mins_player1), (best_action_player2, max_of_mins_player2)

    def print_table(self):
        output = ""
        format_specifier = "^11s"
        output += format(" ", format_specifier)
        for action2 in range(len(self.payoffs[0])):
            output += format(get_action_name(action2, False, len(self.payoffs[0])), format_specifier)
        output += "\n"
        for action1 in range(len(self.payoffs)):
            output += format(get_action_name(action1, True), format_specifier)
            for action2 in range(len(self.payoffs[0])):
                output += format(str(self.payoffs[action1][action2]), format_specifier)
            output += "\n"
        print(output)

    def report(self):
        self.print_table()
        self.print_strongly_dominated_solutions()
        self.print_weakly_dominated_solutions()
        self.print_pure_strategy_equilibria()
        self.print_pareto_optimal_solutions()
        self.print_minimax_strategy()
        self.print_maximin_strategy()
        print("\n")


def parse_payoff(normal_form: str) -> list[list[tuple[int, int]]]:
    lines = normal_form.strip().split('\n')

    # The first line contains the number of actions for both players
    action_counts = list(map(int, lines[0].split()))
    num_actions_player1, num_actions_player2 = action_counts[0], action_counts[1]

    # Initialize the payoff matrix
    payoff_matrix = []

    # Retrieve payoffs for Player 1 and Player 2
    player1_payoffs = list(map(int, lines[1].split()))
    player2_payoffs = list(map(int, lines[2].split()))

    for i in range(num_actions_player1):
        row = []
        for j in range(num_actions_player2):
            index = j + i * num_actions_player2
            row.append((player1_payoffs[index], player2_payoffs[index]))
        payoff_matrix.append(row)

    return payoff_matrix
