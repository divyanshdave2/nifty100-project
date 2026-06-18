import pandas as pd

def check_nulls(df,name):

    nulls = df.isnull().sum()

    print(f"\n{name}")

    print(nulls[nulls>0])

def remove_duplicates(df):

    return df.drop_duplicates()