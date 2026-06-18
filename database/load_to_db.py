import pandas as pd
import sqlite3
import os

conn = sqlite3.connect("database/nifty100.db")

folder = "data/raw"

for file in os.listdir(folder):

    if file.endswith(".xlsx"):

        table_name = file.replace(".xlsx","")

        df = pd.read_excel(
            os.path.join(folder,file)
        )

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"{table_name} loaded")

conn.close()