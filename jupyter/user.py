class User:
    strategy = []
    def __init__(
        self,
        enable_trading=True,
        trading_time=True,
        strategies=[],
        risk_money=10,
        enable_buy=True,
        enable_sell=True,
    ) -> None:
        self.enable_trading = enable_trading
        self.trading_time = trading_time
        self.strategies = strategies
        self.risk_money = risk_money
        self.enable_buy = enable_buy
        self.enable_sell = enable_sell
    
    def subscribe_strategy(self,strategy):
        self.strategies.append(strategy)
