from my_jupyter.filters.moving_average import MovingAverageFilter
from my_jupyter.strategies.strategy_base import StrategyBase


class MinMaxStrategy(StrategyBase):
    def __init__(self, candles_range=2, filters: list[MovingAverageFilter] = None):
        super().__init__(filters)

        self.candles_range = candles_range

    def check_buy_signal(self, ohlc) -> bool:
        interval = ohlc["low"][1 : self.candles_range + 1]
        lowest_low = min(interval)

        if not self.check_filter_for_buy_context():
            return False

        if ohlc["close"][0] < lowest_low:
            return True
        return False

    def check_sell_signal(self, ohlc) -> bool:
        interval = ohlc["high"][1 : self.candles_range + 1]
        highest_high = max(interval)

        if not self.check_filter_for_sell_context():
            return False

        if ohlc["close"][0] > highest_high:
            return True
        return False

    def __str__(self):
        return "MinMaxStrategy"
