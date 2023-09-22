class FilterBase:
    def __init__(self, period):
        self.candles_needed = period
        pass

    def ok_to_buy(self, ohlc):
        pass

    def ok_to_sell(self, ohlc):
        pass
