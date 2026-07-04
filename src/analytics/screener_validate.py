import sqlite3
import pandas as pd

def run_day14_screener():
    conn = sqlite3.connect("database/nifty100.db")
    query = """
        SELECT company_id, year, return_on_equity_pct, debt_to_equity 
        FROM financial_ratios 
        WHERE return_on_equity_pct > 15 AND debt_to_equity < 1
    """
    df = pd.read_sql(query, conn)
    conn.close()
    
    print("\n" + "="*50)
    print(" 🔍 SCREENER PREVIEW (ROE > 15% & D/E < 1) ")
    print("="*50)
    print(f"Unique Target Companies Found : {df['company_id'].nunique()}")
    print(f"Total Rows Matching Criteria   : {len(df)}")
    print("-"*50)
    print(df.head(10).to_string(index=False))
    print("="*50 + "\n")

if __name__ == "__main__":
    run_day14_screener()