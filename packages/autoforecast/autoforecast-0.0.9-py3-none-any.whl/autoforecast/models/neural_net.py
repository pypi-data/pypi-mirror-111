# Forecasting/autoforecast/src/models/keras_models.py
import numpy as np
import tensorflow as tf
from autoforecast import metrics
from autoforecast.configs.configspace.neural_net_space import (
    base_keras_space,
    base_keras_x0,
    lstm_keras_space,
    lstm_keras_x0,
)
from autoforecast.models.hyperparameters import HyperparametersTuner
from keras import Model
from keras.layers import LSTM, Dense, Input


class BaseKeras:
    def __init__(self, n_input=12, n_features=1):
        self.n_input = n_input
        self.n_features = 1

    def fit(self, X_train, y_train, **params):
        self.X_train = np.array(
            [y_train[i : i + self.n_input] for i in range(len(y_train) - self.n_input)]
        )
        self.y_train = np.array(
            [y_train[i + 1 : i + self.n_input + 1] for i in range(len(y_train) - self.n_input)]
        )

        self.model = self.keras_model(self.n_input, self.n_features, **params)
        self.model.fit(self.X_train, self.y_train, epochs=10, validation_split=0.1, verbose=0)

    def predict(self, X_test, *args):
        self.n_input = len(X_test)
        pred_list = self.predict_by_batch(self.model, self.X_train, self.n_input, self.n_features)
        return pred_list

    @staticmethod
    def keras_model(n_input, n_features, hidden_size_dense=3):
        inputs = Input(shape=(n_input, n_features))
        x = Dense(hidden_size_dense, activation="relu")(inputs)
        outputs = Dense(units=1)(x)
        model = Model(inputs=inputs, outputs=outputs)
        loss = tf.keras.losses.MeanAbsolutePercentageError()
        optimizer = tf.keras.optimizers.Adam()
        model.compile(loss=loss, optimizer=optimizer)
        return model

    @staticmethod
    def predict_by_batch(model, X_train, n_input, n_features):
        pred_list = []
        batch = X_train[-1].reshape(-1, 1)
        for i in range(n_input):
            pred_list.append(model.predict(batch)[0])
            batch = np.append(batch[1:], pred_list[i].reshape(-1, 1), axis=0)
        pred_list = np.concatenate([i for i in pred_list]).reshape(-1, 1)
        return np.concatenate(pred_list)

    def optimize(self, X_train, X_test, y_train, y_test):
        return HyperparametersTuner(
            model=BaseKeras,
            search_space=base_keras_space,
            x0=base_keras_x0,
            metric=metrics.smape_score,
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
        )()


class LSTMKeras(BaseKeras):
    def __init__(self):
        return super().__init__()

    def fit(self, X_train, y_train, **params):
        return super().fit(X_train, y_train, **params)

    def predict(self, *args):
        return super().predict(*args)

    @staticmethod
    def keras_model(n_input, n_features, hidden_size_lstm=3):
        inputs = Input(shape=(n_input, n_features))
        x = LSTM(hidden_size_lstm, activation="relu")(inputs)
        outputs = Dense(units=1)(x)
        model = Model(inputs=inputs, outputs=outputs)
        loss = tf.keras.losses.MeanAbsolutePercentageError()
        optimizer = tf.keras.optimizers.Adam()
        model.compile(loss=loss, optimizer=optimizer)
        return model

    def optimize(self, X_train, X_test, y_train, y_test):
        return HyperparametersTuner(
            model=LSTMKeras,
            search_space=lstm_keras_space,
            x0=lstm_keras_x0,
            metric=metrics.smape_score,
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
        )()
