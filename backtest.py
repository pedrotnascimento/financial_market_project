import os, sys
dir1 = os.path.abspath('..\..')
sys.path.append(dir1+ "\\")

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG
import pandas as pd
# custom
from my_jupyter.strategies.min_max_strategy import MinMaxStrategy
from my_jupyter.filters.moving_average import MovingAverageFilter
from my_jupyter.filters.directioned_bars_filter import DirectionedBarsFilter
filters = [DirectionedBarsFilter(candles=5), MovingAverageFilter(), MovingAverageFilter(period=200)]


def _read_file(filename):
    from os.path import dirname, join, abspath

    return pd.read_csv(join(abspath('.'), filename),
                       index_col=0, parse_dates=True, infer_datetime_format=True)
WINV23M1 = _read_file('my_jupyter\daemons\dataset\WINV23M1 copy.csv')

def data(arr):
    return arr.rename(columns={'Close': 'close','High': 'high', 'Low':'low', 'Open':'open'})

class MinMaxStrategyBacktest(Strategy):
    def init(self):
        self.min_max = MinMaxStrategy()
        self.ohlc = self.I(data, self.data.df)
        # self.data.df = self.data.df.rename(columns={'Close': 'close','High': 'high', 'Low':'low', 'Open':'open'})

    def next(self):
        ohlc = self.ohlc #.rename(columns={'Close': 'close','High': 'high', 'Low':'low', 'Open':'open'})
        ohlc={
            'open': list(ohlc[0][::-1]),
            'high': list(ohlc[1][::-1]),
            'low': list(ohlc[2][::-1]),
            'close': list(ohlc[3][::-1]),
        }
        ohlc = pd.DataFrame.from_dict(ohlc)[::-1]
        while len(ohlc) < self.min_max.candles_needed:
            return 
        if self.position.is_long:
            if self.min_max.buy_close(ohlc):
                self.position.close()
            return
        elif self.position.is_short:
            if self.min_max.sell_close(ohlc):
                self.position.close()
            return

        if self.min_max.check_buy_signal(ohlc):
            a = self.buy()
        elif self.min_max.check_sell_signal(ohlc):
            a = self.sell()


bt = Backtest(WINV23M1, MinMaxStrategyBacktest, commission=0.002, exclusive_orders=True, cash=10**12)
stats = bt.run()
# bt.plot()