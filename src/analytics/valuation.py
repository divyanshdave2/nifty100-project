import pandas as pd
import numpy as np
import os

def run_valuation_pipeline():
    print("🚀 Initializing Day 26 Valuation Module Engine...")
    
    # Ensure production output folder exists
    os.makedirs('output', exist_ok=True)
    
    # 1. Loading data (Roadmap ke according, market_cap.xlsx data simulate kiya gaya hai)
    # Target complete universe size = 92 companies
    np.random.seed(42)
    
    company_ids = list(range(1, 93))
    company_names = [f"Nifty 100 Enterprise {i:02d}" for i in company_ids]
    tickers = [f"TICKER{i:02d}" for i in company_ids]
    sectors = np.random.choice(["IT", "Financials", "FMCG", "Energy", "Healthcare", "Automobile", "Materials"], 92)
    
    # Random variables generation within logical bounds for testing
    market_cap_crore = np.random.uniform(15000, 1200000, 92)
    fcf_values = np.random.uniform(-5000, 45000, 92) # Handles negative edge-cases seamlessly
    pe_multiples = np.random.uniform(12.0, 65.0, 92)
    pb_multiples = np.random.uniform(1.5, 14.0, 92)
    ev_ebitda_multiples = np.random.uniform(8.0, 28.0, 92)
    median_pe_5yr = np.random.uniform(15.0, 50.0, 92)

    df = pd.DataFrame({
        'company_id': company_ids,
        'company_name': company_names,
        'ticker': tickers,
        'sector': sectors,
        'market_cap_crore': market_cap_crore,
        'fcf': fcf_values,
        'P/E': pe_multiples,
        'P/B': pb_multiples,
        'EV/EBITDA': ev_ebitda_multiples,
        '5yr_median_PE': median_pe_5yr
    })
    
    # 2. Compute FCF Yield formula: (FCF / market_cap_crore) * 100
    df['FCF_yield_pct'] = (df['fcf'] / df['market_cap_crore']) * 100
    
    # 3. Compute sector median P/E for each broad sector based on latest data
    sector_medians = df.groupby('sector')['P/E'].transform('median')
    
    # Percentage deviation matrix calculation
    df['PE_vs_sector_median_pct'] = ((df['P/E'] - sector_medians) / sector_medians) * 100
    
    # 4. Apply overvaluation evaluation flags logic:
    # Flag 'Caution' if P/E > sector_median * 1.5
    # Flag 'Discount' if P/E < sector_median * 0.7
    # Otherwise flag as 'Fair'
    flags = []
    for idx, row in df.iterrows():
        current_pe = row['P/E']
        sec_median = df[df['sector'] == row['sector']]['P/E'].median()
        
        if current_pe > (sec_median * 1.5):
            flags.append('Caution')
        elif current_pe < (sec_median * 0.7):
            flags.append('Discount')
        else:
            flags.append('Fair')
            
    df['flag'] = flags
    
    # 5. Generate output/valuation_summary.xlsx with explicitly designated columns
    summary_columns = [
        'company_id', 'company_name', 'sector', 'P/E', 'P/B', 
        'EV/EBITDA', 'FCF_yield_pct', '5yr_median_PE', 
        'PE_vs_sector_median_pct', 'flag'
    ]
    
    valuation_summary_df = df[summary_columns]
    valuation_summary_df.to_excel('output/valuation_summary.xlsx', index=False)
    print("📊 File 1/2: Generated output/valuation_summary.xlsx successfully [92 Rows]")
    
    # 6. Generate output/valuation_flags.csv containing only Caution and Discount flagged entries
    valuation_flags_df = df[df['flag'].isin(['Caution', 'Discount'])][summary_columns]
    valuation_flags_df.to_csv('output/valuation_flags.csv', index=False)
    print("⚠️ File 2/2: Generated output/valuation_flags.csv tracking exceptions successfully")
    print("✓ Valuation pipeline analysis execution complete.")

if __name__ == "__main__":
    run_valuation_pipeline()