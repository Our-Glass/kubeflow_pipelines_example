import pandas as pd


def parse_df(x_train, x_test, y_train, y_test):
    x_train = x_train.reset_index(drop=True)
    x_test = x_test.reset_index(drop=True)
    y_train = y_train.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)
    
    # Concatenate X and y
    x_train = pd.concat([x_train, y_train], axis=1)
    x_test = pd.concat([x_test, y_test], axis=1)
    return x_train, x_test

