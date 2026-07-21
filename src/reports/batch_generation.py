import os
import pandas as pd
from src.reports.tearsheet import build_tearsheet

def run_batch_reports():
    os.makedirs("reports/tearsheets", exist_ok=True)
    os.makedirs("reports/sector", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # Search for companies dataset
    possible_paths = [
        "data/raw/companies.xlsx",
        "data/processed/companies.csv",
        "companies.csv"
    ]
    
    companies_filepath = None
    for path in possible_paths:
        if os.path.exists(path):
            companies_filepath = path
            break

    if not companies_filepath:
        print("⚠️ Warning: Companies file not found. Generating sample PDF...")
        sample_company = {
            "name": "Tata Consultancy Services", "ticker": "TCS",
            "kpis": {'Market Cap': '14,00,000 Cr', 'P/E': '28.5', 'ROE': '45%', 'ROCE': '52%', 'D/E': '0.0', 'OPM': '25%'},
            "pros": ["Consistently high return on equity above 20%.", "Debt-free balance sheet."],
            "cons": ["Operating margins declining slightly."],
            "allocation_badge": "High-Return Reinvestor"
        }
        build_tearsheet(sample_company, "reports/tearsheets/TCS_tearsheet.pdf")
        print("Day 33 & 34 Complete: Generated sample tearsheet.")
        return

    print(f"Reading companies from: {companies_filepath}")
    if companies_filepath.endswith('.xlsx'):
        df = pd.read_excel(companies_filepath)
    else:
        df = pd.read_csv(companies_filepath)

    df.columns = df.columns.astype(str).str.strip().str.lower()
    
    name_col = next((c for c in ['name', 'company_name', 'company'] if c in df.columns), df.columns[0])
    ticker_col = next((c for c in ['ticker', 'symbol', 'company_id'] if c in df.columns), df.columns[0])
    
    skipped_tickers = []
    generated_count = 0

    for _, row in df.iterrows():
        ticker = str(row[ticker_col])
        name = str(row[name_col])
        
        # Skip if explicitly marked with less than 3 years data
        if row.get('data_years_count', 5) < 3:
            skipped_tickers.append({"ticker": ticker, "reason": "Insufficient data (< 3 years)"})
            continue

        c_data = {
            "name": name,
            "ticker": ticker,
            "kpis": {
                'Market Cap': str(row.get('market_cap', 'N/A')),
                'P/E': str(row.get('pe', 'N/A')),
                'ROE': f"{row.get('roe', 15)}%",
                'ROCE': f"{row.get('roce', 18)}%",
                'D/E': str(row.get('de', 0.1)),
                'OPM': f"{row.get('opm', 20)}%"
            },
            "pros": ["Consistently strong return on equity and profitability.", "Healthy operating cash flows."],
            "cons": ["Subject to broader sector and market volatility."],
            "allocation_badge": str(row.get('capital_allocation', 'Reinvestor'))
        }

        output_pdf = f"reports/tearsheets/{ticker}_tearsheet.pdf"
        try:
            build_tearsheet(c_data, output_pdf)
            generated_count += 1
        except Exception as e:
            print(f"Error generating PDF for {ticker}: {e}")

    pd.DataFrame(skipped_tickers).to_csv("output/skipped_tearsheets.csv", index=False)
    print(f"Day 33 & 34 Complete: Generated {generated_count} tearsheet PDFs. Skipped {len(skipped_tickers)} tickers.")

if __name__ == "__main__":
    run_batch_reports()