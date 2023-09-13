class MinMaxStrategy:
    def __init__(self, candles_range=2):
        self.candles_range = candles_range

    def check_buy_signal(self, ohlc) -> bool:
        interval = ohlc["low"][1 : self.candles_range + 1]
        lowest_low = min(interval)
        if ohlc["low"][0] <= lowest_low:
            return True

    def check_sell_signal(self, ohlc) -> bool:
        interval = ohlc["high"][1 : self.candles_range + 1]
        highest_high = max(interval)
        if ohlc["high"][0] >= highest_high:
            return True
