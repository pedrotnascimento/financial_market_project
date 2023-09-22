from my_jupyter.indicator.indicator_base import IndicatorBase


class MovingAverage(IndicatorBase):
    def __init__(self, period=21):
        super().__init__(period)
        self.period = period

    def get(self, ohlc):
        closes = ohlc["close"]
        closes_mean = closes.rolling(self.period).mean()
        return closes_mean