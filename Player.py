import random


class Player:
    def __init__(self):
        self.their_previous_actions = []
        self.your_previous_actions = []

    def play(self):
        pass

    def get_strategy(self):
        pass

    def learn(self, their_action):
        self.their_previous_actions.append(their_action)


class TitForTat(Player):
    def play(self):
        if len(self.their_previous_actions) == 0:
            return 0
        return self.their_previous_actions[-1]

    def get_strategy(self):
        return "Tit for Tat"


class Random(Player):
    def play(self):
        return random.randint(0, 1)

    def get_strategy(self):
        return "Random"


class RandomChoice(Player):
    def __init__(self, choices, strategy_name):
        super().__init__()
        self.choices = choices
        self.strategy_name = strategy_name

    def play(self):
        return random.choice(self.choices)

    def get_strategy(self):
        return self.strategy_name


class Grudge(Player):
    def play(self):
        return 0 if 1 not in self.their_previous_actions else 1

    def get_strategy(self):
        return "Grudge"


class AlwaysDefect(Player):
    def play(self):
        return 1

    def get_strategy(self):
        return "Always Defect"


class AlwaysCooperate(Player):
    def play(self):
        return 0

    def get_strategy(self):
        return "Always Cooperate"


class PlaySpecificStrategy(Player):
    def __init__(self, strategy_index, strategy_name):
        super().__init__()
        self.strategy_index = strategy_index
        self.strategy_name = strategy_name

    def play(self):
        return self.strategy_index

    def get_strategy(self):
        return f"Always Play {self.strategy_name}"


class Game:
    def __init__(self, simulations, player1, player2, payoffs=None):
        self.simulations = simulations
        self.player1 = player1
        self.player2 = player2
        self.payoffs = [[(2, 2), (-1, 3)], [(3, -1), (0, 0)]] if payoffs is None else payoffs
        self.player1_score = 0
        self.player2_score = 0
        self.simulate()
        self.report()

    def simulate(self):
        for i in range(self.simulations):
            player1_action = self.player1.play()
            player2_action = self.player2.play()

            self.player1.learn(player2_action)
            self.player2.learn(player1_action)
            self.player1_score += self.payoffs[player1_action][player2_action][0]
            self.player2_score += self.payoffs[player1_action][player2_action][1]

    def report(self):
        print(f"Game Over. End of {self.simulations} simulations")
        print(f"\tPlayer 1 scored: {self.player1_score} using {self.player1.get_strategy()}")
        print(f"\tPlayer 2 scored: {self.player2_score} using {self.player2.get_strategy()}")
        print()
