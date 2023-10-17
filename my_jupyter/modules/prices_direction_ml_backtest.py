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


class PriceDirectionMLBacktest:
    def __init__(self):
        pass

    def run_bt(self, from_file="", from_stock_market_data=None, **kwargs):
        data = None
        if from_file != "":
            data = self._read_file(from_file)
        elif from_stock_market_data is not None:
            data = self.read_market_data(from_stock_market_data, **kwargs)
        strategy_in_test = PricesDirectionMLBacktestStrategy

        bt = Backtest(
            data,
            strategy_in_test,
            commission=0.002,
            exclusive_orders=True,
            cash=10**12,
        )
        output_data = {"index": []}
        bt._strategy.set_custom_strategy(bt._strategy, output_data)
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
        )
        self.stock = stock
        dataframe = pd.DataFrame(data_nparray).rename(
            columns={"close": "Close", "open": "Open", "high": "High", "low": "Low"}
        )
        dataframe.drop("time", axis=1, inplace=True)

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


class PricesDirectionMLBacktestStrategy(Strategy):
    def init(self):
        self.ohlc = self.I(data, self.data.df)
        self.ohlc_custom = []
        self.count = -1  ## delaying 2 before to sync with counting

    def set_custom_strategy(self, output_data):
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
        self.insert_data_to_ml_input(quantity_previous_bar=6)

    def insert_data_to_ml_input(
        self, labels_dict={"close": 3}, quantity_previous_bar=5, skip=1
    ):
        for key, inx_ in labels_dict.items():
            try:
                range_ = list(range(skip, quantity_previous_bar + 1))
                for j in range_[::-1]:
                    if not f"{key}-{j}" in self.output_data:
                        self.output_data[f"{key}-{j}"] = []
                    self.output_data[f"{key}-{j}"].append(self.ohlc_custom[j][inx_])
            except Exception as e:
                print(e)
                print("ERRO>>>", self.ohlc_custom)
                return
            self.output_data[f"index"].append(self.count)
        # output_data[f"date"].append(WINV23M1.iloc[self.count].name)

    def get_result_for_ia(self):
        def normalize_values_to_rated_values(df_in):
            leng = len(df_in)
            for i in range(0, leng):
                curr = df_in.iloc[i]
                df_in.iloc[i] = curr.diff().cumsum()

            df_in.drop(df_in.columns[0], axis=1, inplace=True)

            return df_in

        def normalize_quantity_of_data(data, remain_data_at_least):
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
            # df.drop("index",axis=1,inplace=True)
            buy_to_be_filtered = df.copy(deep=True)
            sell_to_be_filtered = df.copy(deep=True)
            wait_to_be_filtered = df.copy(deep=True)
            for col in df:
                mean, std = df[col].mean(), df[col].std()
                std_rate = std*0.5 
                upper_std = mean + std_rate
                lower_std = mean - std_rate

                buy_to_be_filtered = buy_to_be_filtered[
                    (buy_to_be_filtered[col] > (upper_std))
                ]
                sell_to_be_filtered = sell_to_be_filtered[
                    (sell_to_be_filtered[col] < (lower_std))
                ]
                wait_to_be_filtered = wait_to_be_filtered[
                    ((lower_std) < wait_to_be_filtered[col])
                    & (wait_to_be_filtered[col] < upper_std)
                ]
            mean, std = buy_to_be_filtered.mean(), buy_to_be_filtered.std()
            buy_to_be_filtered = buy_to_be_filtered[buy_to_be_filtered < mean + std]
            mean, std = sell_to_be_filtered.mean(), sell_to_be_filtered.std()
            sell_to_be_filtered = sell_to_be_filtered[sell_to_be_filtered > mean - std]

            buy_to_be_filtered["act"] = pd.Series(
                [EnumAct.BUY] * len(buy_to_be_filtered.values),
                index=buy_to_be_filtered.index,
            )
            sell_to_be_filtered["act"] = pd.Series(
                [EnumAct.SELL] * len(sell_to_be_filtered.values),
                index=sell_to_be_filtered.index,
            )
            wait_to_be_filtered["act"] = pd.Series(
                [EnumAct.WAIT] * len(wait_to_be_filtered.values),
                index=wait_to_be_filtered.index,
            )
            buy_to_be_filtered=buy_to_be_filtered.dropna()
            sell_to_be_filtered=sell_to_be_filtered.dropna()
            wait_to_be_filtered=wait_to_be_filtered.dropna()

            df_final = pd.concat(
                [buy_to_be_filtered, sell_to_be_filtered, wait_to_be_filtered], ignore_index=True
            )
            return df_final

        initial_df = pd.DataFrame.from_dict(self.output_data)

        initial_df.drop("index", axis=1, inplace=True)
        df_out_IA_normalized = normalize_values_to_rated_values(initial_df)
        df_filtered_by_values = filter_by_mean_and_std(df_out_IA_normalized)

        qntOfBuys = len(
            df_filtered_by_values.loc[df_filtered_by_values["act"] == EnumAct.BUY]
        )
        qntOfSells = len(
            df_filtered_by_values.loc[df_filtered_by_values["act"] == EnumAct.SELL]
        )
        qntOfWait = len(
            df_filtered_by_values.loc[df_filtered_by_values["act"] == EnumAct.WAIT]
        )
        least_data = min(qntOfBuys, qntOfSells)
        print("before filter", qntOfBuys, qntOfSells, qntOfWait)

        df_filtered_by_quantity = normalize_quantity_of_data(
            df_filtered_by_values, least_data
        )

        df_out = df_filtered_by_quantity
        qntOfBuysAfter = len(df_out.loc[df_out["act"] == EnumAct.BUY])
        qntOfSellsAfter = len(df_out.loc[df_out["act"] == EnumAct.SELL])
        qntOfWaitAfter = len(df_out.loc[df_out["act"] == EnumAct.WAIT])
        print("after filter", qntOfBuysAfter, qntOfSellsAfter, qntOfWaitAfter)

        return df_out
