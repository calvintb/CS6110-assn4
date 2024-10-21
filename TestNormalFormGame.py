import unittest
from NormalFormGame import NormalFormGame


class TestNormalFormGame(unittest.TestCase):

    def setUp(self):
        payoffs = {
            ('A', 'X'): 3,
            ('A', 'Y'): 2,
            ('B', 'X'): 1,
            ('B', 'Y'): 4,
        }
        self.game = NormalFormGame(payoffs)

    def test_pareto_optimal(self):
        self.assertTrue(self.game.is_pareto_optimal('A', 'X'))
        self.assertFalse(self.game.is_pareto_optimal('B', 'X'))
        self.assertTrue(self.game.is_pareto_optimal('B', 'Y'))

    def test_dominant_strategy(self):
        self.assertTrue(self.game.is_dominant_strategy(('A', 'X')))
        self.assertFalse(self.game.is_dominant_strategy(('B', 'Y')))


if __name__ == '__main__':
    unittest.main()
