from NormalFormGame import *
from Player import *


def get_pareto_optimal_players(normal_game):
    pareto_optimal = normal_game.find_pareto_optimal()
    choices_p1 = []
    choices_p2 = []
    for strategy in pareto_optimal:
        choices_p1.append(get_action_index(strategy[0], len(payoff_matrix))[1])
        choices_p2.append(get_action_index(strategy[1], len(payoff_matrix))[1])
    return RandomChoice(choices_p1, "Picking Pareto Optimal"), RandomChoice(choices_p2, "Picking Pareto Optimal")


def get_nash_equilibria_players(normal_game):
    nash_equilibria = normal_game.find_nash_equilibria()
    choices_p1 = []
    choices_p2 = []
    for strategy in nash_equilibria:
        choices_p1.append(get_action_index(strategy[0], len(payoff_matrix))[1])
        choices_p2.append(get_action_index(strategy[1], len(payoff_matrix))[1])
    return RandomChoice(choices_p1, "Picking Nash Equilibria"), RandomChoice(choices_p2, "Picking Nash Equilibria")


def get_minimax_players(normal_game):
    minimax_strategy = normal_game.find_minimax_strategy()
    choices_p1 = []
    choices_p2 = []
    for strategy in minimax_strategy[0]:
        choices_p1.append(get_action_index(strategy, len(payoff_matrix))[1])
    for strategy in minimax_strategy[1]:
        choices_p2.append(get_action_index(strategy, len(payoff_matrix))[1])
    return RandomChoice(choices_p1, "Picking Minimax"), RandomChoice(choices_p2, "Picking Minimax")


if __name__ == '__main__':
    for file in ["data/prog4A.txt", "data/prog4B.txt", "data/prog4C.txt"]:
        normal_game = NormalFormGame(file)
        normal_game.report(file)

    Game(1000, Grudge(), AlwaysDefect())

    Game(1000, AlwaysCooperate(), AlwaysDefect())

    Game(1000, Random(), AlwaysDefect())

    Game(1000, TitForTat(), AlwaysCooperate())

    Game(100, TitForTat(), Random())

    for filename in ["data/prog4A.txt", "data/prog4B.txt", "data/prog4C.txt"]:
        print(f"------------------Simulating games for {filename}-----------------")
        print()
        with open(filename) as file:
            content = file.read()
        payoff_matrix = parse_payoff(content)
        normal_game = NormalFormGame(payoff_matrix)

        Game(1000, Random(), Random(), payoff_matrix)

        player1, player2 = get_pareto_optimal_players(normal_game)
        Game(1000, player1, player2, payoff_matrix)

        player1, player2 = get_nash_equilibria_players(normal_game)
        Game(1000, player1, player2, payoff_matrix)

        player1, player2 = get_minimax_players(normal_game)
        Game(1000, player1, player2, payoff_matrix)
        print()
