# src/utils/utils.py
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def encode(data, col="bank"):
    map_col_to_col_id = {col: col_id for col_id, col in enumerate(data[col].unique())}
    data[f"{col}_token"] = data[col].map(map_col_to_col_id)
    return data, map_col_to_col_id


def split_n_last_timestep(df, n=12):
    train, test = df.iloc[:-n], df.iloc[-n:]
    return train, test


def scale_transform(train, test=None):
    scaler = MinMaxScaler()
    scaler.fit(train)
    train = scaler.transform(train)
    if test is not None:
        test = scaler.transform(test)
    return train, test, scaler


def prepare_for_training(df, cols_to_drop=["heading_id", "company_id"]):
    df = df.drop(cols_to_drop, axis=1)
    df.date = pd.to_datetime(df.date)
    df = df.set_index("date")
    if "month" not in cols_to_drop:
        df["month"] = df["month"].astype("float64")
    return df


def train_test_split(df):
    train, test = split_n_last_timestep(df, n=12)
    return train, test
