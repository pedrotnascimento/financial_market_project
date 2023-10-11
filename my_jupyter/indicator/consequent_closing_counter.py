from my_jupyter.indicator.indicator_base import IndicatorBase


class ConsequentClosingCounterIndicator(IndicatorBase):
    def __init__(self, period):
        super().__init__(period + 1)
        self.period = period

    def output(self, ohlc):
        count = 0
        # past candles, only closed ones
        previous_candles = 1
        try:
            ohlc_previous = ohlc[previous_candles:]
            self.set_init(ohlc_previous)

            if self.is_bear_moviment():
                count -= 1
                self.next_inx()
                while self.is_bear_moviment():
                    count -= 1
                    self.next_inx()
            elif self.is_bull_moviment():
                count += 1
                self.next_inx()
                while self.is_bull_moviment():
                    count += 1
                    self.next_inx()

            return count
        except Exception as e:
            print(e)

    def set_init(self, ohlc_previous):
        self.inx = 0
        self.ohlc_previous = ohlc_previous
        self.ohlc_limited_len = len(ohlc_previous)

    def is_range_not_reached(self):
        return self.inx < self.ohlc_limited_len - 1

    def is_bear_bar(self):
        return (
            self.ohlc_previous["close"][self.inx] < self.ohlc_previous["open"][self.inx]
        )

    def is_bear_moviment(self):
        return self.is_range_not_reached() and (self.is_bear_bar())

    def is_bull_bar(self):
        return (
            self.ohlc_previous["close"][self.inx] > self.ohlc_previous["open"][self.inx]
        )

    def is_bull_moviment(self):
        return self.is_range_not_reached() and (self.is_bull_bar())

    def next_inx(self):
        self.inx += 1
