import unittest

from jupyter.strategies.min_max_strategy import MinMaxStrategy


class MinMaxTest(unittest.TestCase):
    def setUp(self):
        self.module = MinMaxStrategy()

    def test_should_buy(self):
        ohlc = {"low": [1, 2, 3]}
        res = self.module.check_buy_signal(ohlc)
        self.assertTrue(res)

    def test_should_not_buy(self):
        ohlc = {"low": [3, 2, 3]}
        res = self.module.check_buy_signal(ohlc)
        self.assertIsNone(res)

    def test_should_sell(self):
        ohlc = {"high": [3, 2, 3]}
        res = self.module.check_sell_signal(ohlc)
        self.assertTrue(res)

    def test_should_not_sell(self):
        ohlc = {"high": [2, 2, 3]}
        res = self.module.check_sell_signal(ohlc)
        self.assertIsNone(res)
