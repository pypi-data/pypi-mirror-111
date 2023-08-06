import xgboost as xgb
from autoforecast.models.naive import BaselineLastValue, BaselineMean, BaselineMedian
from autoforecast.models.neural_net import BaseKeras, LSTMKeras
from autoforecast.models.time_series import ARMA, Prophet
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, SGDRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR, LinearSVR, NuSVR
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor


def get_dict_models():
    dict_models = {
        "BaseKeras": BaseKeras(),
        "LSTMKeras": LSTMKeras(),
        "XGBRegressor": xgb.XGBRegressor(),
        "RandomForestRegressor": RandomForestRegressor(),
        "GradientBoostingRegressor": GradientBoostingRegressor(),
        "AdaBoostRegressor": AdaBoostRegressor(),
        "LinearRegression": LinearRegression(),
        "Ridge": Ridge(),
        "SGDRegressor": SGDRegressor(),
        "LinearSVR": LinearSVR(),
        "SVR": SVR(),
        "NuSVR": NuSVR(),
        "DecisionTreeRegressor": DecisionTreeRegressor(),
        "ExtraTreeRegressor": ExtraTreeRegressor(),
        "MLPRegressor": MLPRegressor(),
        "KNeighborsRegressor": KNeighborsRegressor(),
        "ARMA": ARMA(),
        #  'BaselineLastYear': BaselineLastYear(),
        "BaselineLastValue": BaselineLastValue(),
        "BaselineMean": BaselineMean(),
        "BaselineMedian": BaselineMedian(),
        "Prophet": Prophet(),
    }
    return dict_models
