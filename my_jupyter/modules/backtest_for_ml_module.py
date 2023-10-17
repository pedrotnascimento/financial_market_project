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


class BacktestForMLModule:
    def __init__(self, strategy: StrategyBase):
        self.strategy = strategy

    def run_bt(
        self,
        from_file="",
        from_stock_market_data=None,
        quantity_previous_bar=5,
        take_action=None,
        **kwargs,
    ):
        data = None
        if from_file != "":
            data = self._read_file(from_file)
        elif from_stock_market_data is not None:
            data = self.read_market_data(from_stock_market_data, **kwargs)
        strategy_in_test = BacktestStrategyForMLModule

        bt = Backtest(
            data,
            strategy_in_test,
            commission=0.002,
            exclusive_orders=True,
            cash=10**12,
        )
        output_data = {"index": [], "act": []}

        bt._strategy.set_custom_strategy(
            bt._strategy,
            self.strategy,
            output_data,
            quantity_previous_bar,
            take_action=take_action,
        )
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

    def read_market_data(self, stock, quantity_of_bars_in_thousands=6):
        mt_rep = MarketDataRepository()
        data_nparray = mt_rep.read_data(
            stock, mt_rep.mt.TIMEFRAME_M1, 10**quantity_of_bars_in_thousands - 1
        )[240:]
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


class EnumAct:
    BUY = 2
    SELL = 0
    WAIT = 1


class BacktestStrategyForMLModule(Strategy):
    def init(self):
        self.ohlc = self.I(data, self.data.df,plot=False)
        self.ohlc_custom = []
        self.count = -1  ## delaying 2 before to sync with counting

    def set_custom_strategy(
        self,
        strategy: StrategyBase,
        output_data,
        quantity_previous_bar=5,
        take_action=[],
    ):
        self.strategy = strategy
        self.output_data = output_data
        self.quantity_previous_bar = quantity_previous_bar
        self.take_action = take_action

    def next(self):
        self.count += 1
        ohlc = self.ohlc

        self.ohlc_custom.insert(0, (ohlc[0][-1], ohlc[1][-1], ohlc[2][-1], ohlc[3][-1]))

        caracteristica = ["open", "high", "low", "close"]
        ohlc = np.array(self.ohlc_custom, dtype=[(k, "f4") for k in caracteristica])

        while len(self.ohlc_custom) < 30:
            return

        self.ohlc_custom.pop()

        act = EnumAct.WAIT
        if self.position.is_long:
            if self.strategy.buy_close(ohlc):
                self.position.close()
            else:
                act = EnumAct.BUY
                self.insert_data_to_ml_input(act)
            return
        elif self.position.is_short:
            if self.strategy.sell_close(ohlc):
                self.position.close()
            else:
                act = EnumAct.SELL
                self.insert_data_to_ml_input(act)
            return

        if self.strategy.check_buy_signal(ohlc):
            a = self.buy()
            act = EnumAct.BUY
        elif self.strategy.check_sell_signal(ohlc):
            a = self.sell()
            act = EnumAct.SELL

        self.insert_data_to_ml_input(act)

    def insert_data_to_ml_input(self, acao, labels_dict={"close": 3}, skip=1):
        # if  acao not in self.take_action:
        #     return
        for key, inx_ in labels_dict.items():
            try:
                for j in range(skip, self.quantity_previous_bar + 1):
                    if not f"{key}-{j}" in self.output_data:
                        self.output_data[f"{key}-{j}"] = []
                    self.output_data[f"{key}-{j}"].append(self.ohlc_custom[j][inx_])
            except Exception as e:
                print(e)
                print("ERRO>>>", self.ohlc_custom)
                return
            self.output_data[f"act"].append(acao)
            self.output_data[f"index"].append(self.count)
        # output_data[f"date"].append(WINV23M1.iloc[self.count].name)

    def get_result_for_ia(self):
        def normalize_values_to_rated_values(df_in):
            df_out = df_in.drop("act", axis=1)

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

        def normalize_quantity_of_data(data, remain_data_at_least):
            # data.drop("index", axis=1, inplace=True)
            # data.drop("Unnamed: 0", axis=1, inplace=True)
            # data.drop("counting_bar", axis=1, inplace=True)
            # data.drop("close-0", axis=1, inplace=True)
            # data.drop("date", axis=1, inplace=True)

            indexRemove = data.loc[data["act"] == EnumAct.SELL].index[
                remain_data_at_least - 1 :
            ]
            data.drop(indexRemove, inplace=True)

            indexRemove = data.loc[data["act"] == EnumAct.WAIT].index[
                remain_data_at_least - 1 :
            ]
            data.drop(indexRemove, inplace=True)

            indexRemove = data.loc[data["act"] == EnumAct.BUY].index[
                remain_data_at_least - 1 :
            ]
            data.drop(indexRemove, inplace=True)

            return data

        def filter_by_mean_and_std(df):
            operations = [EnumAct.SELL, EnumAct.WAIT, EnumAct.BUY]
            for op in operations:
                mean, std = df[df["act"] == op].mean(), df[df["act"] == op].std()
                for i in df:
                    if i == "act":
                        continue
                    lower_std = mean[i] - std[i]
                    upper_std = mean[i] + std[i]
                    indexRemove = df[
                        (df["act"] == op) & ((df[i] < lower_std) | (df[i] > upper_std))
                    ].index
                    df.drop(indexRemove, inplace=True)

            return df

        initial_df = pd.DataFrame.from_dict(self.output_data)

        qntOfBuys = len(initial_df.loc[initial_df["act"] == EnumAct.BUY])
        qntOfSells = len(initial_df.loc[initial_df["act"] == EnumAct.SELL])
        qntOfWait = len(initial_df.loc[initial_df["act"] == EnumAct.WAIT])
        least_data = min(qntOfBuys, qntOfSells, qntOfWait)
        print("before filter", qntOfBuys, qntOfSells, qntOfWait)

        initial_df.drop("index", axis=1, inplace=True)
        df_filtered_by_quantity = normalize_quantity_of_data(initial_df, least_data)
        df_out_IA_normalized = normalize_values_to_rated_values(df_filtered_by_quantity)
        df_filtered_by_values = filter_by_mean_and_std(df_out_IA_normalized)

        df_out = df_filtered_by_values
        qntOfBuysAfter = len(df_out.loc[df_out["act"] == EnumAct.BUY])
        qntOfSellsAfter = len(df_out.loc[df_out["act"] == EnumAct.SELL])
        qntOfWaitAfter = len(df_out.loc[df_out["act"] == EnumAct.WAIT])
        print("after filter", qntOfBuysAfter, qntOfSellsAfter, qntOfWaitAfter)

        return df_out
