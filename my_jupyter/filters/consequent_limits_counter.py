from my_jupyter.filters.filter_base import FilterBase
from my_jupyter.indicator.consequent_limits_counter import ConsequentLimitsCounterIndicator


class ConsequentLimitsCounterFilter(FilterBase):
    def __init__(self, candles=5):
        super().__init__(candles)
        self.period = candles
        self.candle_counter = ConsequentLimitsCounterIndicator(candles)

    def is_going_up(self, ohlc):
        o = self.candle_counter.output(ohlc)
        
        if o >= self.period:
            return True
        return False

    def is_going_down(self, ohlc):
        o = self.candle_counter.output(ohlc)
        period_neg = -self.period
        if o <= period_neg:
            return True
        return False

    def ok_to_buy(self, ohlc):
        return self.is_going_up(ohlc)

    def ok_to_sell(self, ohlc):
        return self.is_going_down(ohlc)
