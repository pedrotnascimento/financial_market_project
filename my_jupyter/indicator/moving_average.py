class MovingAverage:
    def __init__(self, period=21):
        self.periodo = period

    def get(self, ohlc):
        closes = ohlc["close"]
        closes_mean = closes.rolling(self.period).mean()
        return closes_mean