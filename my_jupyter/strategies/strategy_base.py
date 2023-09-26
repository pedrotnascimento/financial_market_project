from my_jupyter.filters.filter_base import FilterBase
from my_jupyter.filters.moving_average import MovingAverageFilter


class StrategyBase:
    def __init__(self, period=1,filters: list[FilterBase] = None):
        candles_needed_filter = [i.candles_needed for i in filters]
        self.candles_needed = max([period] + candles_needed_filter)
        if filters is not None:
            self.filters = filters

    def check_filter_for_buy_context(self, ohlc):
        for f in self.filters:
            if f.ok_to_buy(ohlc) is False:
                return False
        return True

    def check_buy_signal(self, ohlc) -> bool:
        pass

    def check_filter_for_sell_context(self, ohlc):
        for f in self.filters:
            if f.ok_to_sell(ohlc) is False:
                return False
        return True
    def check_sell_signal(self, ohlc) -> bool:
        pass
