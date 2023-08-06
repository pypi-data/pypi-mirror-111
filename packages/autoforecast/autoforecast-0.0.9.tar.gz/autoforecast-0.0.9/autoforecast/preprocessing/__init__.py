from typing import List, Optional

from autoforecast.preprocessing import categorical, engineering, features_selection, numerical


def preprocessing(
    df,
    target_name: List[str],
    categoricals: List[str],
    numericals: List[str],
    date_col: Optional[str] = None,
    train_size: float = 0.7,
    engineering: bool = True,
    selection: bool = True,
):
    cutoff = int(len(df) * train_size)
    train, test = df[:cutoff], df[cutoff:]
    X_train, y_train, X_test, y_test = None
    return X_train, y_train, X_test, y_test
