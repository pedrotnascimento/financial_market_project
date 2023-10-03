from my_jupyter.indicator.indicator_base import IndicatorBase


class ConsequentLimitsCounterIndicator(IndicatorBase):
    def __init__(self, period):
        super().__init__(period + 1)
        self.period = period

    def output(self, ohlc):
        count = 0
        previous_candles = 1
        try:
            ohlc_previous = ohlc[previous_candles:]
            self.set_init(ohlc_previous)
            self.is_range_not_reached()
            if self.is_bear_first_moviment():
                count -= 1
                while self.is_bear_moviment():
                    self.next_inx()
                    count -= 1
            elif self.is_bull_first_moviment():
                count += 1
                while self.is_bull_moviment():
                    self.next_inx()
                    count += 1

            return count
        except Exception as e:
            print(self.i, len(ohlc))
            print(e)

    def set_init(self, ohlc_previous):
        self.inx = 0
        self.ohlc_previous = ohlc_previous
        self.ohlc_limited_len = len(ohlc_previous[: self.period])

    def is_range_not_reached(self):
        return self.inx < self.ohlc_limited_len - 1

    def next_inx(self):
        self.inx += 1

    def is_bear_first_moviment(self):
        return self.is_range_not_reached() and (self.is_high_lower_than_previous_high())

    def is_bear_moviment(self):
        return self.is_range_not_reached() and (
            self.is_high_lower_or_equal_than_previous_high()
        )

    def is_high_lower_than_previous_high(self):
        return (
            self.ohlc_previous["high"][self.inx]
            < self.ohlc_previous["high"][self.inx + 1]
        )

    def is_high_lower_or_equal_than_previous_high(self):
        return (
            self.ohlc_previous["high"][self.inx]
            <= self.ohlc_previous["high"][self.inx + 1]
        )

    def is_bull_first_moviment(self):
        return self.is_range_not_reached() and (self.is_low_higher_than_previous_low())

    def is_bull_moviment(self):
        return self.is_range_not_reached() and (
            self.is_low_higher_than_previous_low()
            or self.is_low_higher_or_equal_than_previous_low()
        )

    def is_low_higher_than_previous_low(self):
        return (
            self.ohlc_previous["low"][self.inx]
            < self.ohlc_previous["low"][self.inx + 1]
        )

    def is_low_higher_or_equal_than_previous_low(self):
        return (
            self.ohlc_previous["low"][self.inx]
            <= self.ohlc_previous["low"][self.inx + 1]
        )
