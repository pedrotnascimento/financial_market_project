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
    def __init__(self):
        self.scaler = MinMaxScaler()

    def set_machine_learning_model(self, from_file="",from_stock_market_data=None):
        bt = BacktestModule(CounterBarStrategy())
        bt.run_bt(from_file=from_file,from_stock_market_data=from_stock_market_data)
        df = bt.get_result_for_ia()
        self.df = df
        data = self.process_dataframe()
        self.generate_model(data)

    def output(self, sample_input):
        # Normalizar os recursos
        # closes = sample_input["close"]
        result = self.predict(sample_input)
        return result

    def generate_model(self, data):
        X, y = self.split_X_y(data)
        X = self.scaler.fit_transform(X)

        # Dividir os dados em conjuntos de treinamento e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.1, random_state=42
        )
        # Criar um modelo sequencial simples usando TensorFlow/Keras
        model = self.create_model()

        # Treinar o modelo
        model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

        # Avaliar o modelo
        test_loss, test_accuracy = model.evaluate(X_test, y_test)
        print(f"Acurácia do modelo nos dados de teste: {test_accuracy}")

        self.model = model
        return model

    def create_model(self):
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Input(shape=(5,)),
                tf.keras.layers.Dense(128, activation="relu"),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(3, activation="sigmoid")
                # tf.keras.layers.Dense(3, activation='softmax')  # Camada de saída com ativação softmax (3 classes)
            ]
        )

        # Compilar o modelo
        # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",  # Função de perda para classificação multiclasse
            metrics=["accuracy"],
        )

        return model

    def predict(self, sample):
        # Exemplo de como usar o modelo para fazer previsões
        # sample_input = np.array([[0.7, 0.8, 0.6]])  # Substitua pelos seus próprios valores
        sample_array = np.array([sample])
        sample_input_normalized = self.scaler.transform(sample_array)
        predictions = self.model.predict(sample_input_normalized)
        return predictions

    def process_dataframe(self):
        data = self.df
        data.drop("index", axis=1, inplace=True)
        # data.drop("Unnamed: 0", axis=1, inplace=True)
        # data.drop("counting_bar", axis=1, inplace=True)
        # data.drop("close-0", axis=1, inplace=True)
        # data.drop("date", axis=1, inplace=True)

        qntOfBuys = len(data.loc[data["act"] == 2])
        qntOfSells = len(data.loc[data["act"] == 0])
        least_data = min(qntOfBuys, qntOfSells)
        indexRemove = data.loc[data["act"] == 0].index[least_data + 2 :]
        data.drop(indexRemove, inplace=True)
        indexRemove = data.loc[data["act"] == 1].index[least_data + 2 :]
        data.drop(indexRemove, inplace=True)
        print(qntOfBuys, qntOfSells)
        return data

    def split_X_y(self, data):
        # Dividir os dados em recursos (X) e rótulos (y)
        X = data.drop("act", axis=1)
        y = data["act"].values

        return X, y
