import sqlite3
import pandas as pd
import numpy as np
import os

# Import functions from your analytics modules
from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_roe,
    calculate_debt_to_equity,
    calculate_interest_coverage_ratio,
    calculate_asset_turnover
)

from src.analytics.cashflow import (
    calculate_free_cash_flow
)

from src.analytics.cagr import (
    calculate_cagr
)

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# ======================================
# Database Connection
# ======================================
conn = sqlite3.connect("database/nifty100.db")

# ======================================
# Load Profit & Loss
# ======================================
pl = pd.read_sql("SELECT * FROM profitandloss", conn)
pl.columns = pl.iloc[0]
pl = pl.iloc[1:].reset_index(drop=True)

numeric_cols = [
    "sales", "operating_profit", "other_income", 
    "interest", "net_profit", "eps", "dividend_payout"
]
for col in numeric_cols:
    pl[col] = pd.to_numeric(pl[col], errors="coerce")

print("Profit & Loss Loaded")

# ======================================
# Load Balance Sheet
# ======================================
bs = pd.read_sql("SELECT * FROM balancesheet", conn)
bs.columns = bs.iloc[0]
bs = bs.iloc[1:].reset_index(drop=True)
bs = bs.drop_duplicates(subset=["company_id", "year"])

bs_numeric = ["equity_capital", "reserves", "borrowings", "total_assets"]
for col in bs_numeric:
    bs[col] = pd.to_numeric(bs[col], errors="coerce")

print("Balance Sheet Loaded")

# ======================================
# Merge PL + BS
# ======================================
# Pehle PL aur BS ka data saaf karo taaki extra spaces ki wajah se data drop na ho
pl['company_id'] = pl['company_id'].astype(str).str.strip()
pl['year'] = pl['year'].astype(str).str.strip()

bs['company_id'] = bs['company_id'].astype(str).str.strip()
bs['year'] = bs['year'].astype(str).str.strip()

# 'left' join use kar rahe hain taaki >= 1100 rows ka target poora ho sake
merged_df = pd.merge(
    pl,
    bs,
    on=["company_id", "year"],
    how="left"
)

print("Rows after BS Merge :", len(merged_df))

# ======================================
# Load Cash Flow
# ======================================
cf = pd.read_sql("SELECT * FROM cashflow", conn)
cf.columns = cf.iloc[0]
cf = cf.iloc[1:].reset_index(drop=True)
cf = cf.drop_duplicates(subset=["company_id", "year"])

cf_numeric = ["operating_activity", "investing_activity", "financing_activity", "net_cash_flow"]
for col in cf_numeric:
    cf[col] = pd.to_numeric(cf[col], errors="coerce")

print("Cash Flow Loaded")

# ======================================
# Merge Cash Flow
# ======================================
# CF ka data saaf karo
cf['company_id'] = cf['company_id'].astype(str).str.strip()
cf['year'] = cf['year'].astype(str).str.strip()

merged_df = pd.merge(
    merged_df,
    cf,
    on=["company_id", "year"],
    how="left"
)

print("Rows after Cashflow Merge :", len(merged_df))

# Sort data sequentially for correct shift-based CAGR metrics
merged_df = merged_df.sort_values(["company_id", "year"]).reset_index(drop=True)

# ======================================
# Compute Required KPIs
# ======================================

# 1. Net Profit Margin %
merged_df["net_profit_margin_pct"] = merged_df.apply(
    lambda x: calculate_net_profit_margin(x["net_profit"], x["sales"]), axis=1
)

# 2. Operating Profit Margin %
merged_df["operating_profit_margin_pct"] = (merged_df["operating_profit"] / merged_df["sales"]) * 100

# 3. Return on Equity %
merged_df["return_on_equity_pct"] = merged_df.apply(
    lambda x: calculate_roe(x["net_profit"], x["equity_capital"], x["reserves"]), axis=1
)

# 4. Debt to Equity
merged_df["debt_to_equity"] = merged_df.apply(
    lambda x: calculate_debt_to_equity(x["borrowings"], x["equity_capital"], x["reserves"]), axis=1
)

# 5. Interest Coverage
merged_df["interest_coverage"] = merged_df.apply(
    lambda x: calculate_interest_coverage_ratio(x["operating_profit"], x["other_income"], x["interest"])["icr"], axis=1
)

# 6. Asset Turnover
merged_df["asset_turnover"] = merged_df.apply(
    lambda x: calculate_asset_turnover(x["sales"], x["total_assets"]), axis=1
)

# 7. Free Cash Flow (Cr)
merged_df["free_cash_flow_cr"] = merged_df.apply(
    lambda x: calculate_free_cash_flow(x["operating_activity"], x["investing_activity"]), axis=1
)

# 8. Capex (Cr) - Absolute value of investing cash outflow
merged_df["capex_cr"] = merged_df["investing_activity"].abs()

# 9. Earnings Per Share
merged_df["earnings_per_share"] = merged_df["eps"]

# 10. Book Value Per Share
merged_df["book_value_per_share"] = (merged_df["equity_capital"] + merged_df["reserves"]) / merged_df["equity_capital"]

# 11. Dividend Payout Ratio %
merged_df["dividend_payout_ratio_pct"] = merged_df["dividend_payout"]

# 12. Cash From Operations (Cr)
merged_df["cash_from_operations_cr"] = merged_df["operating_activity"]

# 13. Total Debt (Cr)
merged_df["total_debt_cr"] = merged_df["borrowings"]


# ======================================
# 5-Year True CAGR Calculations
# ======================================
# Create 5-year historical shift columns per company
merged_df["sales_5yr_ago"] = merged_df.groupby("company_id")["sales"].shift(5)
merged_df["net_profit_5yr_ago"] = merged_df.groupby("company_id")["net_profit"].shift(5)
merged_df["eps_5yr_ago"] = merged_df.groupby("company_id")["eps"].shift(5)

# 14. Revenue CAGR 5Yr
merged_df["revenue_cagr_5yr"] = merged_df.apply(
    lambda x: calculate_cagr(x["sales_5yr_ago"], x["sales"], 5)["cagr"] if pd.notna(x["sales_5yr_ago"]) else None, axis=1
)

# 15. PAT CAGR 5Yr
merged_df["pat_cagr_5yr"] = merged_df.apply(
    lambda x: calculate_cagr(x["net_profit_5yr_ago"], x["net_profit"], 5)["cagr"] if pd.notna(x["net_profit_5yr_ago"]) else None, axis=1
)

# 16. EPS CAGR 5Yr
merged_df["eps_cagr_5yr"] = merged_df.apply(
    lambda x: calculate_cagr(x["eps_5yr_ago"], x["eps"], 5)["cagr"] if pd.notna(x["eps_5yr_ago"]) else None, axis=1
)


# ======================================
# 17. Composite Quality Score
# ======================================
def compute_quality_score(row):
    score = 0
    if pd.notna(row["return_on_equity_pct"]) and row["return_on_equity_pct"] > 15: score += 1
    if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] < 1.0: score += 1
    if pd.notna(row["free_cash_flow_cr"]) and row["free_cash_flow_cr"] > 0: score += 1
    if pd.notna(row["interest_coverage"]) and row["interest_coverage"] > 2.0: score += 1
    if pd.notna(row["net_profit_margin_pct"]) and row["net_profit_margin_pct"] > 10: score += 1
    return score

merged_df["composite_quality_score"] = merged_df.apply(compute_quality_score, axis=1)


# ======================================
# 18. FCF Conversion Rate (Mandatory Task Sub-point)
# ======================================
merged_df["fcf_conversion_rate"] = merged_df.apply(
    lambda x: (x["free_cash_flow_cr"] / x["operating_profit"]) * 100 if pd.notna(x["operating_profit"]) and x["operating_profit"] != 0 else None, 
    axis=1
)


# ======================================
# 19. Capital Allocation 8-Pattern Classifier Engine
# ======================================
def get_pattern_label(row):
    cfo, cfi, cff = row["operating_activity"], row["investing_activity"], row["financing_activity"]
    if pd.isna(cfo) or pd.isna(cfi) or pd.isna(cff): return "Mixed"
    
    # Check exact quadrant patterns (+ or - signs)
    signs = ("+" if cfo >= 0 else "-", "+" if cfi >= 0 else "-", "+" if cff >= 0 else "-")
    patterns = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "-"): "Shareholder Returns",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "+"): "Pre-Revenue",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "-"): "Liquidating Assets"
    }
    return patterns.get(signs, "Mixed")

merged_df["pattern_label"] = merged_df.apply(get_pattern_label, axis=1)


# ======================================
# Final DataFrame Selection & Export (Main Table)
# ======================================
final_columns = [
    "company_id", "year", "net_profit_margin_pct", "operating_profit_margin_pct", 
    "return_on_equity_pct", "debt_to_equity", "interest_coverage", "asset_turnover", 
    "free_cash_flow_cr", "capex_cr", "earnings_per_share", "book_value_per_share", 
    "dividend_payout_ratio_pct", "cash_from_operations_cr", "total_debt_cr", 
    "revenue_cagr_5yr", "pat_cagr_5yr", "eps_cagr_5yr", "composite_quality_score"
]

final_df = merged_df[final_columns]

# Save Main Ratios to SQLite Database
final_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print(f"\nFinancial Ratios Table Created Successfully with {len(final_df)} rows!")
print(final_df.head())


# ======================================
# Generate output/capital_allocation.csv (Mandatory File Export)
# ======================================
cap_alloc_df = merged_df[["company_id", "year", "operating_activity", "investing_activity", "financing_activity", "pattern_label"]].copy()
for col in ["operating_activity", "investing_activity", "financing_activity"]:
    cap_alloc_df[col] = cap_alloc_df[col].apply(lambda x: "+" if x >= 0 else "-")

cap_alloc_df.columns = ["company_id", "year", "cfo_sign", "cfi_sign", "cff_sign", "pattern_label"]
cap_alloc_df.to_csv("output/capital_allocation.csv", index=False)
print("✔ output/capital_allocation.csv Generated Successfully!")

conn.close()