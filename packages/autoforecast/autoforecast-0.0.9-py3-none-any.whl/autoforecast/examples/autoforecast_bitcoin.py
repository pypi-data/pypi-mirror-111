# Forecasting/autoforecast/main.py
from autoforecast.automl import AutoForecast
from autoforecast.datasets.import_bitcoin_price import get_price_for_last_n_days
from autoforecast.src.utils.logger import LOG


def run(verbose: bool = False):
    LOG.debug("autoforecast_bitcoin.run() starting...")
    # settings
    # lists of features name
    list_cat_feat = ["timestamp"]
    # lists of features name tokenized
    list_num_feat = []

    df_price = get_price_for_last_n_days(n=900, type="spot", currency_pair="BTC-USD")
    df_price = df_price.rename(columns={"price": "target"})
    LOG.info(df_price)

    ind_cutoff = int(df_price.shape[0] * 0.8)
    train = df_price.iloc[:ind_cutoff]
    test = df_price.iloc[ind_cutoff:]
    LOG.info(f"{train.shape} {test.shape}")

    cols = list_cat_feat + list_num_feat
    X_train = train[cols].values
    y_train = train["target"].values
    X_test = test[cols].values
    y_test = test["target"].values
    model = AutoForecast()
    LOG.debug("Autoforecast() model fitting...")
    model.fit(X_train=X_train, y_train=y_train)
    LOG.debug("Autoforecast() model predicting...")
    y_pred = model.predict(X_test=X_test)
    LOG.debug(f"shapes={X_train.shape}{X_test.shape}{y_train.shape}{y_test.shape}")
    LOG.debug(f"y_pred={y_pred}")
    LOG.debug(f"y_test={y_test}")
    LOG.debug("autoforecast_bitcoin.run() ending...")
