from my_jupyter.filters.filter_base import FilterBase
from my_jupyter.filters.moving_average import MovingAverageFilter
from my_jupyter.strategies.strategy_base import StrategyBase


class MinMaxStrategy(StrategyBase):
    def __init__(self, period=2, filters: list[FilterBase] = None):
        super().__init__(period + 1, filters=filters)
        self.period = period

    def check_buy_signal(self, ohlc) -> bool:
        interval = ohlc["low"][1 : self.period + 1]
        lowest_low = min(interval)

        if not self.check_filter_for_buy_context(ohlc):
            return False
        if ohlc["close"][0] < lowest_low:
            return True
        return False

    def check_sell_signal(self, ohlc) -> bool:
        interval = ohlc["high"][1 : self.period + 1]
        highest_high = max(interval)

        if not self.check_filter_for_sell_context(ohlc):
            return False
        if ohlc["close"][0] > highest_high:
            return True
        return False

    def buy_close(self, ohlc):
        interval = ohlc["high"][1 : self.period + 1]
        highest_high = max(interval)
        if ohlc["close"][0] > highest_high:
            return True
        return False

    def sell_close(self, ohlc):
        interval = ohlc["low"][1 : self.period + 1]
        lowest_low = min(interval)
        print(ohlc["close"][0] < lowest_low, ohlc["close"][0], lowest_low)
        if ohlc["close"][0] < lowest_low:
            return True
        return False

    def __str__(self):
        return "MinMaxStrategy"
