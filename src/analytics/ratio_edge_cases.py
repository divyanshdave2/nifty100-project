import os
import sqlite3
import pandas as pd
import numpy as np

def run_day13_validation_engine():
    # ==========================================
    # TOPIC: PATHS & ECOSYSTEM INITIALIZATION
    # ==========================================
    db_path = "database/nifty100.db"
    excel_path = "data/raw/companies.xlsx"
    log_path = "output/ratio_edge_cases.log"
    
    os.makedirs("output", exist_ok=True)
    
    # ==========================================
    # TOPIC: DATABASES AND PREREQUISITE CHECKS
    # ==========================================
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}.")
        return
        
    conn = sqlite3.connect(db_path)
    df_calc = pd.read_sql("SELECT * FROM financial_ratios", conn)
    
    if not os.path.exists(excel_path):
        print(f"Error: Reference sheet not found at {excel_path}")
        conn.close()
        return
        
    # ==========================================
    # TOPIC: REFERENCE SPREADSHEET LOADING
    # ==========================================
    df_source = pd.read_excel(excel_path, skiprows=1)
    
    # ==========================================
    # TOPIC: STRIP CLEANING & TEXT DATA SYNCING
    # ==========================================
    df_calc['company_id'] = df_calc['company_id'].astype(str).str.strip()
    df_source['id'] = df_source['id'].astype(str).str.strip()
    
    # ==========================================
    # TOPIC: MERGING CALCULATED METRICS WITH REFERENCES
    # ==========================================
    df_merged = pd.merge(
        df_calc, 
        df_source[['id', 'roce_percentage', 'roe_percentage']], 
        left_on="company_id", 
        right_on="id", 
        how="left"
    )
    
    financial_tickers = ["HDFC", "ICICI", "AXIS", "SBIN", "KOTAK", "BAJFINANCE", "INDUSINDBK", "CHOLAMANDAM", "MUTHOOTFIN", "RELIANCE"]
    
    anomaly_count = 0
    
    # ==========================================
    # TOPIC: LIVE TERMINAL REPORT HEADER SETUP
    # ==========================================
    print("\n" + "="*50)
    print(" LIVE ANOMALY DETECTOR OUTPUT (DAY 13) ")
    print("="*50)
    
    # ==========================================
    # TOPIC: LOOPING ENTRIES & CORE DISCREPANCY AUDITING
    # ==========================================
    # FIX: Explicitly set encoding='utf-8' to prevent Windows encoding crashes
    with open(log_path, "w", encoding="utf-8") as log_file:
        for idx, row in df_merged.iterrows():
            comp = row['company_id']
            year_val = str(row['year']).strip()
            
            # ------------------------------------------
            # SUB-TOPIC 1: DEBT WARNING SUPPRESSION LOGIC
            # ------------------------------------------
            broad_sector = "Financials" if any(fin in comp.upper() for fin in financial_tickers) else "Non-Financials"
            d_e = row.get('debt_to_equity', 0)
            
            if broad_sector.lower() == "financials":
                de_warning = "Suppressed (Financial Sector)"
            else:
                de_warning = "High Debt" if (pd.notna(d_e) and d_e > 2) else "Healthy"
                    
            # ------------------------------------------
            # SUB-TOPIC 2: ROCE VARIANCE & LOG ENGINE
            # ------------------------------------------
            calc_roce = row.get('return_on_capital_employed_pct', np.nan)
            source_roce = row.get('roce_percentage', np.nan)
            
            if pd.notna(calc_roce) and pd.notna(source_roce):
                diff_roce = abs(calc_roce - source_roce)
                if diff_roce > 5:
                    anomaly_count += 1
                    category = "Formula Difference" if calc_roce * source_roce < 0 else "Source Data Difference"
                    
                    log_entry = (
                        f"Company: {comp} | Year: {year_val} | Metric: ROCE\n"
                        f"Difference: {diff_roce:.1f}% | Category: {category}\n"
                        f"👉 {comp} | {year_val} | ROCE mismatch | Calculated={calc_roce:.1f} | Source={source_roce:.1f}\n"
                        f"{'-'*40}\n"
                    )
                    log_file.write(log_entry)
                    if anomaly_count <= 10:
                        print(log_entry.strip())
                    
            # ------------------------------------------
            # SUB-TOPIC 3: ROE VARIANCE & LOG ENGINE
            # ------------------------------------------
            calc_roe = row.get('return_on_equity_pct', np.nan)
            source_roe = row.get('roe_percentage', np.nan)
            
            if pd.notna(calc_roe) and pd.notna(source_roe):
                diff_roe = abs(calc_roe - source_roe)
                if diff_roe > 5:
                    anomaly_count += 1
                    category = "Version Difference" if "TCS" in comp.upper() else "Formula Difference"
                    
                    log_entry = (
                        f"Company: {comp} | Year: {year_val} | Metric: ROE\n"
                        f"Difference: {diff_roe:.1f}% | Category: {category}\n"
                        f"👉 {comp} | {year_val} | ROE mismatch | Calculated={calc_roe:.1f} | Source={source_roe:.1f}\n"
                        f"{'-'*40}\n"
                    )
                    log_file.write(log_entry)
                    if anomaly_count <= 10:
                        print(log_entry.strip())
                        
    conn.close()
    
    # ==========================================
    # TOPIC: TERMINAL CONSOLE OVERALL METRIC SUMMARY
    # ==========================================
    if anomaly_count > 10:
        print(f"... and {anomaly_count - 10} more anomalies recorded in log file.")
        
    print("="*50)
    print(f"✔ Execution Completed! Total Anomalies Logged: {anomaly_count}")
    print(f"✔ Full logs saved at: {log_path}")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_day13_validation_engine()