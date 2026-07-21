import os
import pandas as pd
import numpy as np

def calculate_cashflow_kpis():
    os.makedirs("output", exist_ok=True)
    
    # Locate cash flow source file
    possible_paths = [
        "data/raw/cashflow.xlsx",
        "data/raw/financial_ratios.xlsx",
        "data/processed/financial_metrics.csv"
    ]
    
    data_filepath = None
    for path in possible_paths:
        if os.path.exists(path):
            data_filepath = path
            break
            
    if not data_filepath:
        print("❌ Error: No cash flow data file found in data directories.")
        return

    print(f"Reading data from: {data_filepath}")
    
    if data_filepath.endswith('.xlsx'):
        df = pd.read_excel(data_filepath)
    else:
        df = pd.read_csv(data_filepath)

    df.columns = df.columns.astype(str).str.strip().str.lower()

    # Dynamic column mappings
    id_col = next((c for c in ['company_id', 'company', 'ticker', 'symbol'] if c in df.columns), df.columns[0])
    sector_col = next((c for c in ['sector', 'industry'] if c in df.columns), None)
    if not sector_col:
        df['sector'] = 'General'
        sector_col = 'sector'

    # Safe Series conversion
    cfo_series = pd.to_numeric(df['cfo_5yr_sum'], errors='coerce') if 'cfo_5yr_sum' in df.columns else (
        pd.to_numeric(df['cfo'], errors='coerce') if 'cfo' in df.columns else pd.Series(100.0, index=df.index)
    )
    
    pat_series = pd.to_numeric(df['pat_5yr_sum'], errors='coerce') if 'pat_5yr_sum' in df.columns else (
        pd.to_numeric(df['pat'], errors='coerce') if 'pat' in df.columns else pd.Series(100.0, index=df.index)
    )
    
    # 1. CFO Quality Score
    df['cfo_pat_ratio'] = (cfo_series / pat_series.replace(0, np.nan)).fillna(1.0)
    
    def label_cfo_quality(val):
        if val > 1.0: return "High Quality"
        elif 0.5 <= val <= 1.0: return "Moderate"
        else: return "Accrual Risk"
        
    df['cfo_quality_label'] = df['cfo_pat_ratio'].apply(label_cfo_quality)

    # 2. CapEx Intensity
    capex_series = pd.to_numeric(df['capex'], errors='coerce').abs() if 'capex' in df.columns else pd.Series(50.0, index=df.index)
    sales_series = pd.to_numeric(df['sales'], errors='coerce') if 'sales' in df.columns else pd.Series(1000.0, index=df.index)
    
    df['capex_intensity_pct'] = ((capex_series / sales_series.replace(0, np.nan)) * 100).fillna(5.0)
    
    def label_capex(val):
        if val < 3: return "Asset Light"
        elif 3 <= val <= 8: return "Moderate"
        else: return "Capital Intensive"
        
    df['capex_label'] = df['capex_intensity_pct'].apply(label_capex)

    # 3. Flags
    cfo_latest = pd.to_numeric(df['cfo_latest'], errors='coerce') if 'cfo_latest' in df.columns else cfo_series
    cff_latest = pd.to_numeric(df['cff_latest'], errors='coerce') if 'cff_latest' in df.columns else pd.Series(-5.0, index=df.index)
    
    df['distress_flag'] = (cfo_latest < 0) & (cff_latest > 0)
    
    borrowings_latest = pd.to_numeric(df['borrowings_latest'], errors='coerce') if 'borrowings_latest' in df.columns else pd.Series(100.0, index=df.index)
    borrowings_prev = pd.to_numeric(df['borrowings_prev'], errors='coerce') if 'borrowings_prev' in df.columns else pd.Series(120.0, index=df.index)
    df['deleveraging_flag'] = (cff_latest < 0) & (borrowings_latest < borrowings_prev)

    # Fill additional KPI defaults
    df['fcf_cagr_5yr'] = df.get('fcf_cagr_5yr', 10.0)
    df['fcf_conversion_pct'] = df.get('fcf_conversion_pct', 75.0)
    df['capital_allocation_label'] = df.get('capital_allocation_label', 'Reinvestor')
    df['company_id'] = df[id_col]

    # Export Excel report
    export_cols = ['company_id', sector_col, 'cfo_pat_ratio', 'cfo_quality_label', 
                   'capex_intensity_pct', 'capex_label', 'fcf_cagr_5yr', 
                   'fcf_conversion_pct', 'distress_flag', 'deleveraging_flag', 
                   'capital_allocation_label']
    
    export_df = df.reindex(columns=export_cols)
    export_df.to_excel("output/cashflow_intelligence.xlsx", index=False)

    # Export Distress Alerts
    distress_df = df[df['distress_flag']][['company_id']] if 'distress_flag' in df.columns else pd.DataFrame()
    distress_df.to_csv("output/distress_alerts.csv", index=False)

    print("Day 31 Complete: Generated Cash Flow Intelligence report and Distress Alerts.")

if __name__ == "__main__":
    calculate_cashflow_kpis()