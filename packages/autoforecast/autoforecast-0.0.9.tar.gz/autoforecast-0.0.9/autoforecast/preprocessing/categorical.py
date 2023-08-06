"""
encoding categorical features
"""


def encode_one_col(data, col: str):
    map_col_to_col_id = {col: col_id for col_id, col in enumerate(data[col].unique())}
    data[f"{col}_token"] = data[col].map(map_col_to_col_id)
    return data, map_col_to_col_id


def encode(data, list_col):
    dict_map = {}
    for col in list_col:
        data, map_col_to_col_id = encode_one_col(data, col)
        dict_map[col] = map_col_to_col_id
    return data, dict_map


def split_date(df, date_col):
    """
    split YYYY-mm-dd date into year, month, day
    """
    list_date = df[date_col].tolist()
    list_year = [int(date[:4]) for date in list_date]
    list_month = [int(date[5:7]) for date in list_date]
    list_day = [int(date[8:]) for date in list_date]
    df["year"] = list_year
    df["month"] = list_month
    df["day"] = list_day
    return df


def run(df, list_cat_feat, date_col):
    if date_col:
        df = split_date(df, date_col)
        list_cat_feat += ["year", "month", "day"]
    df, dict_map = encode(data=df, list_col=list_cat_feat)
    list_cat_feat_token = [f"{col}_token" for col in list_cat_feat]
    return df[list_cat_feat_token].values
