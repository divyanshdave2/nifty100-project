import pandas as pd

df = pd.read_excel("data/raw/companies.xlsx")

print(df.shape)
print(df.head())