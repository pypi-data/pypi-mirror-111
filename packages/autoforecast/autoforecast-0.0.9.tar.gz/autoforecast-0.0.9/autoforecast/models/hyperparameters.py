from typing import Callable

from skopt import gp_minimize
from skopt.utils import use_named_args


class HyperparametersTuner:
    def __init__(
        self,
        model: Callable,
        search_space: list,
        x0: list,
        metric: Callable,
        X_train,
        X_test,
        y_train,
        y_test,
    ):
        self.model = model
        self.search_space = search_space
        self.x0 = x0
        self.metric = metric
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def __call__(self):
        return self.optimize()

    def optimize(
        self, n_calls: int = 10, n_random_starts: int = 3, random_state: int = 666
    ):
        dimensions = self.search_space
        print(dimensions)

        @use_named_args(dimensions=dimensions)
        def fitness(**params):
            print(f"params={params}")
            model = self.model()
            model.fit(self.X_train, self.y_train, **params)

            y_pred = model.predict(self.X_test)
            metric_value = self.metric(self.y_test, y_pred)
            print(f"metric_value={metric_value}")
            return metric_value

        res = gp_minimize(
            func=fitness,
            dimensions=dimensions,
            acq_func="EI",  # Expected Improvement.
            x0=self.x0,
            n_calls=n_calls,
            n_random_starts=n_random_starts,
            random_state=random_state,
        )
        print(f"best accuracy={-1.0 * res.fun} with {res.x}")
        param_name = [space.name for space in self.search_space]
        best_params = dict(zip(param_name, res.x))
        return res, best_params
