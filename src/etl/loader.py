import pandas as pd
import os

DATA_PATH = "data/raw"

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx",
    "market_cap.xlsx",
    "financial_ratios.xlsx",
    "peer_groups.xlsx"
]

dataframes = {}

for file in files:
    path = os.path.join(DATA_PATH, file)

    try:
        df = pd.read_excel(path)
        dataframes[file] = df

        print(f"{file}")
        print(df.shape)

    except Exception as e:
        print(f"Error in {file}: {e}")