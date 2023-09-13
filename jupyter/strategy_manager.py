from datetime import datetime
from jupyter.market_data_repository import MarketDataRepository
from jupyter.user import User


class StrategyManager:
    user: User = None

    def __init__(self, market_data=None, user: User = None):
        self.market_data: MarketDataRepository = market_data
        self.user = user

    def add_order_buy(self):
        if self.can_operate() and self.user.enable_buy:
            self.check_signal(self.buy_operate)

    def add_order_sell(self):
        if self.can_operate() and self.user.enable_sell:
            self.check_signal(self.sell_operate)

    def can_operate(self):
        now = datetime.now()
        return (
            self.user.enable_trading
            and self.user.trading_time_start <= now
            and now <= self.user.trading_time_end
        )

    def check_signal(self, operate):
        for o in self.user.operations:
            for s in self.user.strategies:
                operate(o, s)

    def buy_operate(self, operation, strategy):
        ohcl = self.market_data.read_data(
            operation.stock, operation.timeframe, strategy.candles_range
        )
        if strategy.check_buy_signal(ohcl):
            self.market_data.buy(operation.stock, operation.volume)

    def sell_operate(self, operation, strategy):
        ohcl = self.market_data.read_data(
            operation.stock, operation.timeframe, strategy.candles_range
        )
        if strategy.check_sell_signal(ohcl):
            self.market_data.sell(operation.stock, operation.volume)
