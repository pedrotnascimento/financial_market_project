import unittest
from  unittest.mock import MagicMock
from my_jupyter.operation import Operation
from my_jupyter.strategies.min_max_strategy import MinMaxStrategy
from my_jupyter.strategy_manager import StrategyManager
from my_jupyter.user import User

class MarketDataRepoStub():
    def read_data(self, *args):
        bull_value = {'low':[2,3,4], 'open':[3,4,5],'close':[4,5,6],'high':[5,6,7]}
        return bull_value
    def buy(self, *args):
        return True
    def sell(self, *args):
        return True
    
    def positions(self, stock):
        return []


class TestStrategyManager(unittest.TestCase):

    def setUp(self) -> None:
        self.strategy_manager = StrategyManager()
        
    def tearDown(self) -> None:
        del self.strategy_manager
        return super().tearDown()
    
    def test_should_add_order_buy(self):
        # arrange
        market_data = MarketDataRepoStub()
        bull_values = {'low':[2,3,4], 'open':[3,4,5],'close':[2,5,6],'high':[5,6,7]}
        market_data.read_data = MagicMock(return_value =bull_values)
        market_data.buy = MagicMock()
        market_data.sell = MagicMock()
        self.strategy_manager.market_data = market_data

        self.strategy_manager.can_operate = MagicMock(return_value= True)

        user = User()
        op = Operation("ABCD", volume=1, timeframe=2, can_buy=True, can_sell=True, enable=True)
        strategy = MinMaxStrategy()
        user.add_operation(op)
        user.add_strategy(strategy)
        self.strategy_manager.user = user

        #act
        self.strategy_manager.add_order_buy()

        #assert
        self.strategy_manager.can_operate.assert_called_with()
        self.strategy_manager.market_data.buy.assert_called_once_with(op.stock, op.volume)
        self.strategy_manager.market_data.sell.assert_not_called()
    
    def test_should_add_order_sell(self):
        #arrange
        market_data = MarketDataRepoStub()
        bear_values = {'low':[4,3,2], 'open':[5,4,3],'close':[6,5,4],'high':[7,6,5]}
        market_data.read_data = MagicMock(return_value =bear_values)
        market_data.buy = MagicMock()
        market_data.sell = MagicMock()
        self.strategy_manager.market_data = market_data

        self.strategy_manager.can_operate = MagicMock(return_value= True)

        user = User()
        op = Operation("ABCD", volume=1, timeframe=2, can_buy=True, can_sell=True, enable=True)
        strategy = MinMaxStrategy()
        user.add_operation(op)
        user.add_strategy(strategy)
        self.strategy_manager.user = user

        #act
        self.strategy_manager.add_order_sell()

        #assert
        self.strategy_manager.can_operate.assert_called_with()
        self.strategy_manager.market_data.sell.assert_called_once_with(op.stock, op.volume)
        self.strategy_manager.market_data.buy.assert_not_called()
    
    def test_should_not_add_order_buy_when_the_operation_not_trigger_strategy(self):
        # arrange
        market_data = MarketDataRepoStub()
        bear_values = {'low':[4,3,2], 'open':[5,4,3],'close':[6,5,4],'high':[7,6,5]}
        market_data.read_data = MagicMock(return_value =bear_values)
        market_data.buy = MagicMock()
        market_data.sell = MagicMock()
        self.strategy_manager.market_data = market_data

        self.strategy_manager.can_operate = MagicMock(return_value= True)

        user = User()
        op = Operation("ABCD", volume=1, timeframe=2, can_buy=True, can_sell=True, enable=True)
        strategy = MinMaxStrategy()
        user.add_operation(op)
        user.add_strategy(strategy)
        self.strategy_manager.user = user

        #act
        self.strategy_manager.add_order_buy()

        #assert
        self.strategy_manager.can_operate.assert_called_with()
        self.strategy_manager.market_data.buy.assert_not_called()
        self.strategy_manager.market_data.sell.assert_not_called()
    
    def test_should_not_add_order_sell_when_the_operation_not_trigger_strategy(self):
        #arrange
        market_data = MarketDataRepoStub()
        bull_values = {'low':[2,3,4], 'open':[3,4,5],'close':[4,5,6],'high':[5,6,7]}
        market_data.read_data = MagicMock(return_value =bull_values)
        market_data.buy = MagicMock()
        market_data.sell = MagicMock()
        self.strategy_manager.market_data = market_data

        self.strategy_manager.can_operate = MagicMock(return_value= True)

        user = User()
        op = Operation("ABCD", volume=1, timeframe=2, can_buy=True, can_sell=True, enable=True)
        strategy = MinMaxStrategy()
        user.add_operation(op)
        user.add_strategy(strategy)
        self.strategy_manager.user = user

        #act
        self.strategy_manager.add_order_sell()

        #assert
        self.strategy_manager.can_operate.assert_called_with()
        self.strategy_manager.market_data.buy.assert_not_called()
        self.strategy_manager.market_data.sell.assert_not_called()