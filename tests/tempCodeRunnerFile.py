import sys
import os

sys.path.append(os.path.abspath("."))

import pandas as pd
from src.etl.validator import validate_dataframe

df = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

validate_dataframe(df, "companies.xlsx")


import pandas as pd

df = pd.read_excel("data/raw/companies.xlsx", header=1)

print(df.head())
print(df.columns)