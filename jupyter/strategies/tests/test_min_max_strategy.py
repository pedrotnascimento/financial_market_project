import unittest

from jupyter.strategies.min_max_strategy import MinMaxStrategy


class MinMaxTest(unittest.TestCase):
    def setUp(self):
        self.module = MinMaxStrategy()

    def test_should_buy(self):
        ohcl = {"low": [1, 2, 3]}
        res = self.module.check_buy_signal(ohcl)
        self.assertTrue(res)

    def test_should_not_buy(self):
        ohcl = {"low": [3, 2, 3]}
        res = self.module.check_buy_signal(ohcl)
        self.assertIsNone(res)

    def test_should_sell(self):
        ohcl = {"high": [3, 2, 3]}
        res = self.module.check_sell_signal(ohcl)
        self.assertTrue(res)

    def test_should_not_sell(self):
        ohcl = {"high": [2, 2, 3]}
        res = self.module.check_sell_signal(ohcl)
        self.assertIsNone(res)
