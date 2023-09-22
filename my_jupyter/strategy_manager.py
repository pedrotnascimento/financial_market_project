from datetime import datetime
from my_jupyter.market_data_repository import MarketDataRepository
from my_jupyter.operation import Operation
from my_jupyter.strategies.strategy_base import StrategyBase
from my_jupyter.tools.alert_module import Mbox
from my_jupyter.user import User


class StrategyManager:
    user: User = None

    def __init__(self, market_data=None, user: User = None):
        self.market_data: MarketDataRepository = market_data
        self.user = user

    def run_strategies(self):
        if self.user.enable_buy:
            self.add_order_buy()
        if self.user.enable_sell:
            self.add_order_sell()

    def add_order_buy(self):
        if self.can_operate():
            self.check_signal(self.buy_operate)

    def add_order_sell(self):
        if self.can_operate():
            self.check_signal(self.sell_operate)

    def can_operate(self):
        now = datetime.now()
        trading_time_on = (
            self.user.trading_time_start <= now and now <= self.user.trading_time_end
        )
        return self.user.enable_trading and trading_time_on

    def check_signal(self, operate):
        for o in self.user.operations:
            for s in self.user.strategies:
                operate(o, s)

    def buy_operate(self, operation: Operation, strategy: StrategyBase):
        positions = self.market_data.positions(operation.stock)
        positions_buy = list(filter(lambda x: x.type == 0, positions))
        if len(positions_buy) > 0:
            return
        ohlc = self.market_data.read_data(
            operation.stock, operation.timeframe, strategy.candles_range + 1
        )
        if operation.can_buy and strategy.check_buy_signal(ohlc):
            print("buying")
            ret = self.market_data.buy(operation.stock, operation.volume)
            if ret:
                Mbox.BoxOkCancelAsync(
                    "Comprado",
                    f"Stock:{operation.stock} Strat:{strategy} Vol:{operation.volume}",
                )

    def sell_operate(self, operation, strategy):
        positions = self.market_data.positions(operation.stock)
        positions_sell = list(filter(lambda x: x.type != 0, positions))
        if len(positions_sell) > 0:
            return
        ohlc = self.market_data.read_data(
            operation.stock, operation.timeframe, strategy.candles_range
        )
        if operation.can_sell and strategy.check_sell_signal(ohlc):
            print("selling")
            ret = self.market_data.sell(operation.stock, operation.volume)
            if ret:
                Mbox.BoxOkCancelAsync(
                    "Comprado",
                    f"Stock:{operation.stock} Strat:{strategy} Vol:{operation.volume}",
                )
