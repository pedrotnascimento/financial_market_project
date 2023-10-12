import pandas as pd
from my_jupyter.market_data_repository import MarketDataRepository
from my_jupyter.strategies.strategy_base import StrategyBase
from datetime import datetime as dt
from backtesting import Backtest, Strategy
import pandas as pd
import numpy as np
from os.path import join, abspath


def data(arr):
    return arr.rename(
        columns={"Close": "close", "High": "high", "Low": "low", "Open": "open"}
    )


class BacktestModule:
    def __init__(self, strategy: StrategyBase):
        self.strategy = strategy

    def run_bt(self, from_file="", from_stock_market_data=None):
        data = None
        if from_file != "":
            data = self._read_file(from_file)
        elif from_stock_market_data is not None:
            data = self.read_market_data(from_stock_market_data)
        strategy_in_test = BacktestStrategyModule

        bt = Backtest(
            data,
            strategy_in_test,
            commission=0.002,
            exclusive_orders=True,
            cash=10**12,
        )
        output_data = {"index": [], "act": []}
        bt._strategy.set_custom_strategy(bt._strategy, self.strategy, output_data)
        stats = bt.run()
        self.bt = bt
        self.strategy_in_test = strategy_in_test

        return stats

    def _read_file(self, filename):
        return pd.read_csv(
            join(abspath("."), filename),
            index_col=0,
            parse_dates=True,
            infer_datetime_format=True,
        )

    def read_market_data(self, stock):
        mt_rep = MarketDataRepository()
        data_nparray = mt_rep.read_data(stock, mt_rep.mt.TIMEFRAME_M1, 99999)
        self.stock = stock
        dataframe = pd.DataFrame(data_nparray).rename(
            columns={"close": "Close", "open": "Open", "high": "High", "low": "Low"}
        )
        dataframe.drop("time", axis=1, inplace=True)
        # dataframe.set_index("time")
        # dataset = _read_file("dataset\WINV23.csv")

        return dataframe

    def save_file(self):
        dataframe = self.get_result_for_ia()
        result_name = dt.now().strftime(f"%Y%m%d{self.stock}")
        dataframe.to_csv(f"tensor_flow_ia_input-{result_name}.csv")

    def get_result_for_ia(self):
        dataframe = self.bt._strategy.get_result_for_ia(self.bt._strategy)
        return dataframe

    def plot_it(self):
        self.bt.plot()


class BacktestStrategyModule(Strategy):
    def init(self):
        self.ohlc = self.I(data, self.data.df)
        self.ohlc_custom = []
        self.count = -1  ## delaying 2 before to sync with counting

    def set_custom_strategy(self, strategy: StrategyBase, output_data):
        self.strategy = strategy
        self.output_data = output_data

    def next(self):
        self.count += 1
        ohlc = self.ohlc

        self.ohlc_custom.insert(0, (ohlc[0][-1], ohlc[1][-1], ohlc[2][-1], ohlc[3][-1]))

        caracteristica = ["open", "high", "low", "close"]
        ohlc = np.array(self.ohlc_custom, dtype=[(k, "f4") for k in caracteristica])

        while len(self.ohlc_custom) < 30:
            return

        self.ohlc_custom.pop()
        if self.position.is_long:
            if self.strategy.buy_close(ohlc):
                self.position.close()
            return
        elif self.position.is_short:
            if self.strategy.sell_close(ohlc):
                self.position.close()
            return
        acao = 1
        if self.strategy.check_buy_signal(ohlc):
            a = self.buy()
            acao = 2
        elif self.strategy.check_sell_signal(ohlc):
            a = self.sell()
            acao = 0

        # for inx_ in range(0,len(caracteristica)):
        #     inx_label=caracteristica[inx_]
        inx_label = "close"
        inx_ = 3
        try:
            for j in range(1, 6):
                if not f"{inx_label}-{j}" in self.output_data:
                    self.output_data[f"{inx_label}-{j}"] = []
                self.output_data[f"{inx_label}-{j}"].append(self.ohlc_custom[j][inx_])
        except Exception as e:
            print(e)
            print("ERRO>>>", self.ohlc_custom)
            return
        self.output_data[f"act"].append(acao)
        self.output_data[f"index"].append(self.count)
        # output_data[f"date"].append(WINV23M1.iloc[self.count].name)

    def get_result_for_ia(self):
        df_out_IA_tensor_flow = pd.DataFrame.from_dict(self.output_data)

        def normalize(df_in):
            df_out = df_in.drop("act", axis=1)
            df_out = df_out.drop("index", axis=1)
            leng = len(df_out)

            for i in range(0, leng):
                curr = df_out.iloc[i]
                # curr_min = min(curr)
                curr_min = curr[-1]

                df_out.iloc[i] = curr_min - df_out.iloc[i]
            for col in df_out:
                df_in[col] = df_out[col]
            df_out = df_in
            return df_out

        df_out_IA_normalized = normalize(df_out_IA_tensor_flow)
        df_filtered = self._process_dataframe(df_out_IA_normalized)

        return df_filtered

    def _process_dataframe(self, data):
        data.drop("index", axis=1, inplace=True)
        # data.drop("Unnamed: 0", axis=1, inplace=True)
        # data.drop("counting_bar", axis=1, inplace=True)
        # data.drop("close-0", axis=1, inplace=True)
        # data.drop("date", axis=1, inplace=True)

        qntOfBuys = len(data.loc[data["act"] == 2])
        qntOfSells = len(data.loc[data["act"] == 0])
        least_data = min(qntOfBuys, qntOfSells)
        indexRemove = data.loc[data["act"] == 0].index[least_data - 1 :]
        data.drop(indexRemove, inplace=True)
        indexRemove = data.loc[data["act"] == 1].index[least_data - 1 :]
        data.drop(indexRemove, inplace=True)
        indexRemove = data.loc[data["act"] == 2].index[least_data - 1 :]
        data.drop(indexRemove, inplace=True)
        print(qntOfBuys, qntOfSells)
        return data
