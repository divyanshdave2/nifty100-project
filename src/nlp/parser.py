import re
import os
import pandas as pd

def parse_analysis_text(file_path="data/raw/analysis.xlsx"):
    """
    Parses CAGR/growth text metrics from analysis.xlsx using regular expressions.
    Dynamically detects company identifier and target columns.
    """
    os.makedirs("output", exist_ok=True)
    
    # Updated regex to match formats like '10 Years: 21%' or '10 Years:21%'
    pattern = re.compile(r'(\d+)\s*Years?:?\s*([\d.]+)%')
    
    parsed_records = []
    failures = []

    # Read target Excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    # Clean column names (strip whitespace)
    df.columns = df.columns.astype(str).str.strip()

    # Identify company ID column dynamically
    id_col = None
    possible_id_cols = ['company_id', 'company', 'ticker', 'symbol', 'company_name', 'name']
    for col in df.columns:
        if col.lower() in possible_id_cols:
            id_col = col
            break
            
    # Fallback to first column if no match found
    if not id_col:
        id_col = df.columns[0]
        
    print(f"Using '{id_col}' as company identifier.")

    # Identify target fields dynamically
    target_fields = [
        col for col in df.columns 
        if col != id_col and any(term in col.lower() for term in ['sales', 'profit', 'cagr', 'roe', 'growth'])
    ]

    # If no specific matched terms, use all non-id columns
    if not target_fields:
        target_fields = [col for col in df.columns if col != id_col]

    for _, row in df.iterrows():
        company_id = row[id_col]
        for field in target_fields:
            text_val = str(row.get(field, ''))
            if not text_val or text_val.lower() == 'nan':
                continue
            
            matches = pattern.findall(text_val)
            if matches:
                for period, val in matches:
                    parsed_records.append({
                        "company_id": company_id,
                        "metric_type": field,
                        "period_years": int(period),
                        "value_pct": float(val)
                    })
            else:
                failures.append({
                    "company_id": company_id,
                    "field": field,
                    "raw_text": text_val
                })

    # Save outputs
    parsed_df = pd.DataFrame(parsed_records)
    parsed_df.to_csv("output/analysis_parsed.csv", index=False)

    failures_df = pd.DataFrame(failures)
    failures_df.to_csv("output/parse_failures.csv", index=False)
    
    print(f"Day 29 Complete: Parsed {len(parsed_df)} records, logged {len(failures_df)} failures.")

if __name__ == "__main__":
    parse_analysis_text("data/raw/analysis.xlsx")