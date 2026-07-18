import streamlit as st
import pandas as pd
import numpy as np

# Day 22: Shared data loader with @st.cache_data(ttl=600) for performance
@st.cache_data(ttl=600)
def get_companies():
    """Nifty 100 Companies directory context return karta hai."""
    data = {
        "company_id": list(range(1, 6)),
        "name": ["Reliance Industries", "TCS", "HDFC Bank", "Infosys", "ICICI Bank"],
        "ticker": ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK"],
        "sector": ["Energy", "IT", "Financials", "IT", "Financials"],
        "sub_sector": ["Oil & Gas", "IT Services", "Banking", "IT Services", "Banking"],
        "description": ["Energy conglomerate...", "IT services provider...", "Private bank...", "Global tech services...", "Private sector banking..."]
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    """Dynamic ratio generation for specific tickers."""
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    data = []
    for y in years:
        data.append({
            "ticker": ticker,
            "year": y,
            "roe": np.random.uniform(10, 25),
            "roce": np.random.uniform(12, 28),
            "net_profit_margin": np.random.uniform(8, 20),
            "de": np.random.uniform(0.1, 1.5),
            "revenue_cagr_5yr": np.random.uniform(5, 15),
            "fcf": np.random.uniform(1000, 5000),
            "pe": np.random.uniform(15, 45),
            "pb": np.random.uniform(2, 8),
            "ev_ebitda": np.random.uniform(10, 25),
            "dividend_yield": np.random.uniform(0.5, 3.0),
            "icr": np.random.uniform(3, 15)
        })
    df = pd.DataFrame(data)
    if year:
        return df[df['year'] == year]
    return df

@st.cache_data(ttl=600)
def get_pl(ticker):
    """Profit and Loss dynamic records."""
    return pd.DataFrame({
        "year": [2019, 2020, 2021, 2022, 2023, 2024],
        "Revenue": np.random.uniform(50000, 100000, 6),
        "Net_Profit": np.random.uniform(5000, 15000, 6)
    })

@st.cache_data(ttl=600)
def get_bs(ticker):
    """Balance Sheet data loader."""
    return pd.DataFrame({"Metric": ["Total Assets", "Total Liabilities"], "Value": [500000, 300000]})

@st.cache_data(ttl=600)
def get_cf(ticker):
    """Cash Flow metrics."""
    return pd.DataFrame({"year": [2024], "Operating_CF": [12000], "Capital_Exp": [4000]})

@st.cache_data(ttl=600)
def get_sectors():
    """All broad sectors list lookup."""
    return ["IT", "Financials", "FMCG", "Energy", "Healthcare"]

@st.cache_data(ttl=600)
def get_peers(group_name):
    """Filter group members by sector."""
    companies = get_companies()
    return companies[companies['sector'] == group_name]

@st.cache_data(ttl=600)
def get_valuation(ticker):
    """Quick valuation metric data fetch."""
    return {"ticker": ticker, "current_pe": np.random.uniform(15, 50)}