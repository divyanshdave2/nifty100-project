import pandas as pd
from src.etl.cleaner import *

data = {
    "company": [" Reliance ", "TCS", None],
    "price": [100, None, 300]
}

df = pd.DataFrame(data)

df = clean_text(df)
df = fill_missing(df)

print(df)