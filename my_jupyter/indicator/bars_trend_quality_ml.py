from my_jupyter.modules.backtest_for_ml_module import BacktestForMLModule
from my_jupyter.modules.backtest_module import BacktestModule
from my_jupyter.strategies.counter_bar_strategy import CounterBarStrategy
from my_jupyter.filters.directioned_bars_filter import DirectionedBarsFilter
from my_jupyter.indicator.directioned_bars_counter import (
    DirectionedBarsCounterIndicator,
)
from my_jupyter.strategies.strategy_base import StrategyBase

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


class BarsTrendQualityML:
    def __init__(self, quantity_of_bars_in_thousands=4):
        
        self.quantity_of_bars_in_thousands = quantity_of_bars_in_thousands

    def extract_data_for_modelling(
        self,
        from_file="",
        from_stock_market_data=None,
        quantity_previous_bar=5,
        take_action=None,
    ):
        bt = BacktestForMLModule(CounterBarStrategy(period=3))
        bt.run_bt(
            from_file=from_file,
            from_stock_market_data=from_stock_market_data,
            quantity_of_bars_in_thousands=self.quantity_of_bars_in_thousands,
            quantity_previous_bar=quantity_previous_bar,
            take_action=take_action,
        )
        self.quantity_previous_bar = quantity_previous_bar
        data = bt.get_result_for_ia()
        self.df = data


class NeuralNetworkModule:
    def __init__(self):
        self.scaler = MinMaxScaler()

    def generate_model(self, data, quantity_previous_bar=5, epochs=10):
        self.quantity_previous_bar = quantity_previous_bar
        X, y = self.split_X_y(data)
        X = self.scaler.fit_transform(X)

        # Dividir os dados em conjuntos de treinamento e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.1, random_state=42
        )
        # Criar um modelo sequencial simples usando TensorFlow/Keras
        model = self.create_model()

        # Treinar o modelo
        model.fit(
            X_train,
            y_train,
            epochs=epochs,
            batch_size=32,
            validation_split=0.1,
            verbose=0,
        )

        # # Avaliar o modelo
        # test_loss, test_accuracy = model.evaluate(X_test, y_test)
        # print(f"Acurácia do modelo nos dados de teste: {test_accuracy}")

        self.model = model
        return model

    def split_X_y(self, data):
        # Dividir os dados em recursos (X) e rótulos (y)
        X = data.drop("close-1", axis=1)
        X = X.drop("act", axis=1)
        y = data["close-1"]
        return X.values, y.values

    def create_model(self):
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Input(shape=(self.quantity_previous_bar - 1,)),
                # tf.keras.layers.Dense(128, activation="relu"),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(
                    1
                )  # Output layer (linear activation for regression)
                # tf.keras.layers.Dense(3, activation="sigmoid")
                # tf.keras.layers.Dense(3, activation='softmax')  # Camada de saída com ativação softmax (3 classes)
            ]
        )

        # Compilar o modelo
        # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        # model.compile(
        #     optimizer="adam",
        #     loss="sparse_categorical_crossentropy",  # Função de perda para classificação multiclasse
        #     metrics=["accuracy"],
        # )

        # Compile the model
        model.compile(
            optimizer="adam", loss="mean_squared_error"
        )  # Mean squared error loss for regression

        return model

    def output(self, sample_input):
        # Normalizar os recursos
        # closes = sample_input["close"]
        result = self.predict(sample_input)
        return result

    def predict(self, sample):
        # Exemplo de como usar o modelo para fazer previsões
        # sample_input = np.array([[0.7, 0.8, 0.6]])  # Substitua pelos seus próprios valores
        if not isinstance(sample[0], list) and not  isinstance(sample[0], np.ndarray):
            sample = [sample]
        sample_array = np.array(sample)
        sample_input_normalized = self.scaler.transform(sample_array)
        predictions = self.model.predict(sample_input_normalized, verbose=0)
        return predictions

    def __analyse_result_of_the_machine_learning(self):
        from my_jupyter.market_data_repository import MarketDataRepository
        from datetime import datetime as dt

        mt_rep = MarketDataRepository()
        ohlc = mt_rep.read_data("WINV23", mt_rep.mt.TIMEFRAME_M1, 6)
        ohlc = mt_rep.mt.copy_rates_from_pos("WINV23", mt_rep.mt.TIMEFRAME_M1, 0, 60)
        ohlc_0_based = ohlc[::-1]
        # print([ dt.fromtimestamp(i[0]) for i in ohlc_0_based])
        # bars_trend_ml.output(ohlc_0_based[1:])
        import numpy as np

        to_timestamp = lambda x: dt.fromtimestamp(x)
        ohlc_transform = [
            (ohlc_0_based[i : i + 5]["close"], to_timestamp(ohlc_0_based[i]["time"]))
            for i in range(1, len(ohlc_0_based) - 5)
        ]
        # ohlc_transform = [ i - min(i) for i in ohlc_transform ]
        ohlc_transform = [
            (
                ohlc_transform[i][0] - ohlc_transform[i][0][-1],
                ohlc_transform[i][1],
                ohlc_transform[i][0],
            )
            for i in range(len(ohlc_transform))
        ]

        results = []
        df = pd.DataFrame()
        for i in range(0, len(ohlc_transform)):
            res = np.round(self.output(ohlc_transform[i][0]) * 100)
            results.append(
                {
                    "out": res[0],
                    "in": ohlc_transform[i][2],
                    "time": ohlc_transform[i][1],
                }
            )

        analyze = 0
        res = sorted(results, key=lambda x: -x["out"][analyze])
        # print(">>>>>>>>>>", *res,sep="\n")
        for i in range(len(res)):
            # if res[i][0][2]> 50:
            if res[i]["out"][analyze] == max(res[i]["out"]):
                print(res[i])
                pd.Series(res[i]["in"]).plot()
