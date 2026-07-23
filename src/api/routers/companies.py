import os
import pandas as pd
import numpy as np
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

router = APIRouter()

def load_data():
    path = "data/raw/companies.xlsx" if os.path.exists("data/raw/companies.xlsx") else "output/pros_cons_generated.csv"
    if os.path.exists(path):
        df = pd.read_excel(path) if path.endswith('.xlsx') else pd.read_csv(path)
        # Convert all NaNs to None (valid JSON nulls)
        df = df.replace({np.nan: None})
        return df
    return pd.DataFrame()

@router.get("/companies")
def get_companies(sector: str = None, search: str = None):
    df = load_data()
    if df.empty:
        return []
    
    # Safe dictionary conversion
    records = df.to_dict(orient='records')
    
    # Extra check for any lingering NaN values
    cleaned_records = []
    for row in records:
        cleaned_row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
        cleaned_records.append(cleaned_row)
        
    if sector:
        cleaned_records = [r for r in cleaned_records if str(r.get('sector', '')).lower() == sector.lower()]
    if search:
        cleaned_records = [r for r in cleaned_records if search.lower() in str(r.get('ticker', '')).lower() or search.lower() in str(r.get('name', '')).lower()]
    
    return cleaned_records

@router.get("/companies/{ticker}")
def get_company_profile(ticker: str):
    df = load_data()
    if df.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    
    df.columns = df.columns.astype(str).str.strip().str.lower()
    ticker_col = next((c for c in ['ticker', 'symbol', 'company_id'] if c in df.columns), df.columns[0])
    
    match = df[df[ticker_col].astype(str).str.upper() == ticker.upper()]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Company {ticker} not found")
    
    row_dict = match.iloc[0].to_dict()
    return {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}

@router.get("/companies/{ticker}/pl")
def get_pl_history(ticker: str):
    return {"ticker": ticker.upper(), "pl_history": [{"year": 2024, "revenue": 1000, "pat": 150}]}

@router.get("/companies/{ticker}/bs")
def get_bs_history(ticker: str):
    return {"ticker": ticker.upper(), "balance_sheet": [{"year": 2024, "assets": 5000, "equity": 3000}]}

@router.get("/companies/{ticker}/cashflow")
def get_cf_history(ticker: str):
    return {"ticker": ticker.upper(), "cash_flow": [{"year": 2024, "cfo": 200, "capex": -50}]}

@router.get("/companies/{ticker}/ratios")
def get_ratios(ticker: str):
    return {"ticker": ticker.upper(), "ratios": {"roe": 18.5, "roce": 22.0, "pe": 25.4, "de": 0.1}}

@router.get("/companies/{ticker}/tearsheet")
def download_tearsheet(ticker: str):
    pdf_path = f"reports/tearsheets/{ticker.upper()}_tearsheet.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type="application/pdf", filename=f"{ticker}_tearsheet.pdf")
    raise HTTPException(status_code=404, detail="Tearsheet PDF not found")