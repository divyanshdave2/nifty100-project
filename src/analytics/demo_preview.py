import sqlite3
import pandas as pd

def preview_lead_demo():
    conn = sqlite3.connect("database/nifty100.db")
    df = pd.read_sql("SELECT * FROM financial_ratios LIMIT 5", conn)
    conn.close()
    
    print("\n" + "="*60)
    print(" 🏢 TEAM LEAD DEMO DATA PREVIEW (SAMPLE RECORDS) ")
    print("="*60)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df.to_string(index=False))
    print("="*60 + "\n")

if __name__ == "__main__":
    preview_lead_demo()