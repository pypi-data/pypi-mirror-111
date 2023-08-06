from autoforecast import metrics
from autoforecast.models.hyperparameters import HyperparametersTuner


class BaseMLRegressor:
    def __init__(self):
        pass

    def fit(self):
        self.model.fit()

    def predic(self):
        self.model.predict()

    def optimize(self, X_train, X_test, y_train, y_test):
        return HyperparametersTuner(
            model=None,
            search_space=None,
            x0=None,
            metric=metrics.smape_score,
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
        )()
