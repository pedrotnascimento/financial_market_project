from my_jupyter.indicator.moving_average import MovingAverage


class MovingAverageFilter:
    def __init__(self, period=21):
        self.moving_average = MovingAverage(period)

    def is_going_up(self, ohlc):
        closes = self.moving_average.get(ohlc)
        closes_mean = closes.values
        if closes_mean[0] > closes_mean[1] and closes_mean[1] > closes_mean[2]:
            return True
        return False
    
    def is_going_down(self, ohlc):
        closes = self.moving_average.get(ohlc)
        closes_mean = closes.values
        if closes_mean[0] < closes_mean[1] and closes_mean[1] < closes_mean[2]:
            return True
        return False
    
    def ok_to_buy(self, ohlc):
        return self.is_going_up(ohlc)
    
    def ok_to_sell(self, ohlc):
        return self.is_going_down(ohlc)
