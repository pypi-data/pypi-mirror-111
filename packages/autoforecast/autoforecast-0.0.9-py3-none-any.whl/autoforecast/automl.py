# Forecasting/autoforecast/main.py
import time

import numpy as np
from tqdm import tqdm

from autoforecast.metrics import get_metrics
from autoforecast.models.models import get_dict_models
from autoforecast.src.utils.logger import LOG


class AutoForecast:
    def __init__(self, metrics=None):
        """
        metrics: str, metric to optimize
        """
        self.dict_models = get_dict_models()
        self.model = None

    def fit(self, X_train, y_train):
        # given X_train, y_train find the best model
        cutoff = int(len(X_train) * 0.7)
        X_train_ = X_train[:cutoff]
        y_train_ = y_train[:cutoff]
        X_test_ = X_train[cutoff:]
        y_test_ = y_train[cutoff:]
        res_auto_forecast = self.run_auto_forecast(
            X_train=X_train_,
            y_train=y_train_,
            X_test=X_test_,
            y_test=y_test_,
            verbose=False,
            max_time_in_sec=360,
        )
        self.model = res_auto_forecast["best_model"]["model"]
        best_param = res_auto_forecast["best_model"]["best_param"]
        self.model.fit(X_train, y_train, **best_param)

    def predict(self, X_test):
        y_pred = self.model.predict(X_test)
        return y_pred

    # custom AutoForecast
    def run_auto_forecast(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        verbose: bool = False,
        max_time_in_sec: int = 360,
    ):
        """
        Args:
            :X_train: np.ndarray
            :y_train: np.ndarray
            :X_test: np.ndarray
            :y_test: np.ndarray
            :verbose: bool = False
            :max_time_in_sec: int = 360
        """
        LOG.debug("AutoForecast starting...")
        start = time.time()
        dict_metrics = {}
        dict_pred = {}
        dict_trained_model = {}
        for model_str, model in tqdm(self.dict_models.items()):
            LOG.debug(model_str)
            dict_trained_model[model_str] = {}
            dict_trained_model[model_str]["model"] = model
            best_param = {}
            try:
                LOG.debug("start optimize hyperparameters")
                res_opt, best_param = model.optimize(
                    X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test
                )
                LOG.debug(res_opt)
                LOG.debug(best_param)
            except AttributeError as err:
                LOG.debug(f"except: {err}")
            model.fit(X_train, y_train, **best_param)
            dict_trained_model[model_str]["best_param"] = best_param
            y_pred = model.predict(X_test)
            dict_pred[model_str] = y_pred
            if verbose:
                LOG.debug(model_str)
                LOG.debug(f"pred={y_pred}")
            metrics = get_metrics(y_test=y_test, y_pred=y_pred)
            dict_metrics[model_str] = metrics
            if start - time.time() >= max_time_in_sec:
                break
        # log best models
        # SMAPE
        LOG.debug("Best models according to SMAPE metrics:")
        dict_metrics_smape = {k: v["smape"] for k, v in dict_metrics.items()}
        # sorted dict
        dict_metrics_smape = dict(sorted(dict_metrics_smape.items(), key=lambda item: item[1]))
        LOG.debug(dict_metrics_smape)
        # RMSE
        LOG.debug("Best models according to RMSE metrics:")
        dict_metrics_rmse = {k: v["rmse"] for k, v in dict_metrics.items()}
        # sorted dict
        dict_metrics_rmse = dict(sorted(dict_metrics_rmse.items(), key=lambda item: item[1]))
        LOG.debug(dict_metrics_rmse)
        LOG.debug("Best models according to MAPE metrics:")
        # MAPE
        dict_metrics_mape = {k: v["mape"] for k, v in dict_metrics.items()}
        # sorted dict
        dict_metrics_mape = dict(sorted(dict_metrics_mape.items(), key=lambda item: item[1]))
        LOG.debug(dict_metrics_mape)
        LOG.debug(f"AutoForecast done in {round(time.time()-start, 2)}s.")
        best_model_str = list(dict_metrics_smape.keys())[0]
        return {
            "dict_metrics": dict_metrics,
            "dict_pred": dict_pred,
            "best_model": dict_trained_model[best_model_str],
        }
