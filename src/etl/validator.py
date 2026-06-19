import pandas as pd

def check_nulls(df, name):

    nulls = df.isnull().sum()

    print(f"\n{name}")

    print(nulls[nulls > 0])


def remove_duplicates(df):

    return df.drop_duplicates()


def check_duplicates(df):

    return df.duplicated().sum()


def validate_dataframe(df, name):

    print(f"\n===== {name} =====")

    print("\nNull Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(check_duplicates(df))