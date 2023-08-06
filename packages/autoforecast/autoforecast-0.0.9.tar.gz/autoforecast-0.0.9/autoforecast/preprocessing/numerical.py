from sklearn.preprocessing import MinMaxScaler


def scale_transform(train, test=None):
    scaler = MinMaxScaler()
    scaler.fit(train)
    train = scaler.transform(train)
    if test is not None:
        test = scaler.transform(test)
    return train, test, scaler


def run(df, list_num_feat):
    train, test, scaler = scale_transform(train=df[list_num_feat])
    return train, test, scaler
