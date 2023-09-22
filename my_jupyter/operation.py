class Operation:
    stock = None
    volume = 0
    timeframe = None
    can_buy = True
    can_sell = True
    enable = True

    def __init__(
        self,
        stock,
        volume,
        timeframe,
        can_buy=True,
        can_sell=True,
        enable=True,
        watch_for_sell=True,
        watch_for_buy=True,
    ):
        (
            self.stock,
            self.volume,
            self.timeframe,
            self.can_buy,
            self.can_sell,
            self.enable,
            self.watch_for_sell,
            self.watch_for_buy,
        ) = (
            stock,
            volume,
            timeframe,
            can_buy,
            can_sell,
            enable,
            watch_for_sell,
            watch_for_buy,
        )
