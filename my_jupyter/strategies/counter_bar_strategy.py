from my_jupyter.filters.consequent_closing_filter import ConsequentClosingFilter
from my_jupyter.filters.directioned_bars_filter import DirectionedBarsFilter
from my_jupyter.filters.filter_base import FilterBase
from my_jupyter.indicator import directioned_bars_counter
from my_jupyter.strategies.strategy_base import StrategyBase


class CounterBarStrategy(StrategyBase):
    def __init__(self, period=5, filters: list[FilterBase] = None):
        # filters = [DirectionedBarsFilter(candles=5)]
        filters = [ConsequentClosingFilter(candles=5)]
        super().__init__(period + 1, filters=filters)
        self.period = period

    def check_buy_signal(self, ohlc) -> bool:
        if not self.check_filter_for_buy_context(ohlc):
            return False
        return True

    def check_sell_signal(self, ohlc) -> bool:
        if not self.check_filter_for_sell_context(ohlc):
            return False
        return True
        

    def buy_close(self, ohlc):
        if self.check_filter_for_buy_context(ohlc):
            return False
        return True

    def sell_close(self, ohlc):
        if self.check_filter_for_sell_context(ohlc):
            return False
        return True
         

    def __str__(self):
        return "CounterBarStrategy"
