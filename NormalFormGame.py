class NormalFormGame:
    def __init__(self, payoffs: list[list[tuple[int, int]]]):
        """
        payoff is a double list of tuples representing the rewards.
        Player 1's action is the first index and Player 2's action is the second index
        In the tuple, the first entry is the first player's reward and the second entry is the second player's reward
        """
        self.payoffs = payoffs
