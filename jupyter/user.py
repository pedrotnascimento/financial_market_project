from jupyter.operation import Operation
from jupyter.strategies.min_max_strategy import MinMaxStrategy
from datetime  import datetime
class User():
    # strategies: list[MinMaxStrategy] = []
    # operations: list[Operation] = []
    # enable_trading = True
    # trading_time_start = None
    # trading_time_end = None
    # risk_money = -1
    # enable_buy = True
    # enable_sell = True
    
    def __init__(
        self,
        enable_trading=True,
        trading_time_start=None,
        trading_time_end=None,
        strategies: list[MinMaxStrategy]=None,
        operations: list[Operation]=None,
        risk_money=10,
        enable_buy=True,
        enable_sell=True,
    ) -> None:
        self.enable_trading = enable_trading

        now = datetime.now()
        self.strategies = strategies
        if self.strategies is  None:
            self.strategies = []
        
        self.operations = operations
        if self.operations is  None:
            self.operations = []

        if trading_time_start:
            self.trading_time_start = trading_time_start
        else:
            start = datetime(now.year,now.month,now.day,12)
            self.trading_time_start = start

        if trading_time_end:
            self.trading_time_end = trading_time_end
        else:
            end = datetime(now.year,now.month,now.day,16,35)
            self.trading_time_end = end
            
        self.risk_money = risk_money
        self.enable_buy = enable_buy
        self.enable_sell = enable_sell
    
    def add_strategy(self,strategy):
        self.strategies.append(strategy)
    
    def add_operation(self,operation: Operation):
        self.operations.append(operation)
