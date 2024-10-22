import unittest
from NormalFormGame import NormalFormGame, parse_payoff


class TestParsePayoff(unittest.TestCase):

    def test_parse_payoff(self):
        normal_form = """2 4
4 4 -1 -1 0 3 0 3
3 3 -1 -1 0 4 0 4"""

        expected_output = [
            [(4, 3), (4, 3), (-1, -1), (-1, -1)],
            [(0, 0), (3, 4), (0, 0), (3, 4)]
        ]

        result = parse_payoff(normal_form)
        self.assertEqual(result, expected_output)


class TestNormalFormGame(unittest.TestCase):
    def setUp(self):
        payoff_matrix = [
            [(4, 3), (4, 3), (-1, -1), (-1, -1)],
            [(0, 0), (3, 4), (0, 0), (3, 4)]
        ]
        self.normalFormGame = NormalFormGame(payoff_matrix)

    def test_find_pareto_optimal(self):
        expected_optimal_solutions = [('A', 'W'), ('A', 'X'), ('B', 'X'), ('B', 'Z')]
        result = self.normalFormGame.find_pareto_optimal()
        self.assertEqual(result, expected_optimal_solutions)


if __name__ == '__main__':
    unittest.main()
