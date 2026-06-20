import pandas as pd

def clean_text(df):
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    return df

def fill_missing(df):
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("Unknown")
        else:
            df[col] = df[col].fillna(0)
    return df

def remove_duplicates(df):
    return df.drop_duplicates()