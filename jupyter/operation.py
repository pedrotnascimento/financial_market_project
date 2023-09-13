class Operation:
    stock = None
    volume = 0
    timeframe = None
    buy = True 
    sell = True
    enable = True
    def __init__(self, stock, volume, timeframe, buy=True, sell=True, enable=True):
        self.stock, self.volume, self.timeframe, self.buy, self.sell, self.enable = (
            stock,
            volume,
            timeframe,
            buy,
            sell,
            enable,
        )
