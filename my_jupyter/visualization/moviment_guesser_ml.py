from my_jupyter.indicator.bars_trend_quality_ml import (
    BarsTrendQualityML,
    NeuralNetworkModule,
)
from my_jupyter.market_data_repository import MarketDataRepository
from datetime import datetime as dt
import pandas as pd

from my_jupyter.modules.backtest_for_ml_module import EnumAct
from matplotlib import pyplot as plt


class MovimentGuesserML:
    skips = 0
    lasts = 0

    def __init__(self, stock, previous_bar_to_consider=5):
        self.stock = stock
        self.previous_bar_to_consider = previous_bar_to_consider

    def extract_data(self, quantity_of_bars_to_extract_in_thousands=5):
        bars_trend_ml = BarsTrendQualityML(
            quantity_of_bars_in_thousands=quantity_of_bars_to_extract_in_thousands
        )
        bars_trend_ml.extract_data_for_modelling(
            from_stock_market_data=self.stock,
            quantity_previous_bar=self.previous_bar_to_consider,
        )
        self.df = bars_trend_ml.df

    def generate_model(self, enum):
        model = NeuralNetworkModule()
        model.generate_model(
            self.df[self.df["act"] == enum],
            self.previous_bar_to_consider,
            epochs=20,
        )
        return model

    def display(self):
        self.extract_data()
        model_buy = self.generate_model(EnumAct.BUY)
        model_sell = self.generate_model(EnumAct.SELL)
        model_wait = self.generate_model(EnumAct.WAIT)

        ohlc_transform, ohlc_0_based = self._generate_inputs()
        output_buy = self._predict_on_to_model(ohlc_transform, model_buy)
        output_sell = self._predict_on_to_model(ohlc_transform, model_sell)
        output_wait = self._predict_on_to_model(ohlc_transform, model_wait)

        series_buy = self._get_series_for_plot(output_buy)
        series_wait = self._get_series_for_plot(output_wait)
        series_sell = self._get_series_for_plot(output_sell)
        serie_real_time = self._get_real_time_serie(ohlc_0_based)

        
        self._plot_all_series(series_buy, series_wait, series_sell, serie_real_time)

    def _plot_all_series(self, series_buy, series_wait, series_sell, serie_real_time):
        ohlc_s_diff = serie_real_time.diff().cumsum().dropna()
        ohlc_norm = (ohlc_s_diff - min(ohlc_s_diff)) / (max(ohlc_s_diff) - min(ohlc_s_diff))
        cumsum_buy = (series_buy + ohlc_s_diff).dropna()
        cumsum_wait = (series_wait + ohlc_s_diff).dropna()
        cumsum_sell = (series_sell +ohlc_s_diff).dropna()
        norm_buy = (cumsum_buy - min(cumsum_buy)) / (max(cumsum_buy) - min(cumsum_buy)) 
        norm_wait = (cumsum_wait - min(cumsum_wait)) / (max(cumsum_wait) - min(cumsum_wait)) 
        norm_sell = (cumsum_sell - min(cumsum_sell)) / (max(cumsum_sell) - min(cumsum_sell))
        average =  ((norm_buy + norm_wait + norm_sell + ohlc_norm)/4).rolling(9).mean()
        plt.plot(ohlc_norm, "xm", ohlc_norm,"m")
        plt.plot(norm_buy , "xg", norm_buy , "g")
        plt.plot(norm_wait, "xb", norm_wait, "b")
        plt.plot(norm_sell, "xr", norm_sell, "r")
        plt.plot(average, "xk", average, "k")
        plt.show()

    def _get_real_time_data(self):
        mt_rep = MarketDataRepository()
        ohlc = mt_rep.mt.copy_rates_from_pos(self.stock, mt_rep.mt.TIMEFRAME_M1, 0, 200)
        ohlc_0_based = ohlc[::-1]
        self.ohlc_0_based = ohlc_0_based

        return ohlc_0_based

    def _generate_inputs(self):
        ohlc_0_based = self._get_real_time_data()
        length_inputs = self.previous_bar_to_consider - 1
        ohlc_transform = [
            (
                ohlc_0_based[i : i + length_inputs]["close"],
                self._to_timestamp_helper(ohlc_0_based[i]["time"]),
            )
            for i in range(0, len(ohlc_0_based) - length_inputs)
        ]
        # ohlc_transform = [ i - min(i) for i in ohlc_transform ]
        ohlc_transform = [
            {
                "in": ohlc_transform[i][0] - ohlc_transform[i][0][-1],
                "prices": ohlc_transform[i][0],
                "time": ohlc_transform[i][1],
            }
            for i in range(len(ohlc_transform))
        ]
        return ohlc_transform, ohlc_0_based

    def _predict_on_to_model(self, ohlc_transform, model: NeuralNetworkModule):
        results = []
        input_on_model = [i["in"] for i in ohlc_transform]
        outputs = model.output(input_on_model)
        for i in range(0, len(outputs)):
            results.append(
                {
                    "out": outputs[i][0],
                    "in": ohlc_transform[i]["prices"],
                    "time": ohlc_transform[i]["time"],
                }
            )
        return results

    def _to_timestamp_helper(self, x):
        return dt.fromtimestamp(x)

    def _get_series_for_plot(self, results):
        res_out = [results[i]["out"] for i in range(len(results))][::-1]
        res_out_time = [results[i]["time"] for i in range(len(results))][::-1]
        serie = pd.Series(res_out, res_out_time)[: len(results) - self.skips][
            -self.lasts :
        ]
        return serie

    def _get_real_time_serie(self, ohlc_0_based):
        ohlc_non_zero_based = ohlc_0_based[::-1][self.previous_bar_to_consider :]["close"]
        ohlc_non_zero_based_time = list(
            map(
                self._to_timestamp_helper,
                ohlc_0_based[::-1][self.previous_bar_to_consider :]["time"],
            )
        )

        ohlc_s = pd.Series(ohlc_non_zero_based, ohlc_non_zero_based_time)[
            : len(ohlc_non_zero_based) - self.skips
        ][-self.lasts :]
        return ohlc_s
