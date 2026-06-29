import logging

# Configure anomaly logging
logger = logging.getLogger("ratio_engine")
logger.setLevel(logging.WARNING)
# Ensure handlers don't duplicate logs if configured elsewhere
if not logger.handlers:
    handler = logging.FileHandler("output/ratio_edge_cases.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def calculate_net_profit_margin(net_profit: float, sales: float) -> float | None:
    """Calculate Net Profit Margin. Returns None if sales is 0."""
    if sales <= 0:
        return None
    return (net_profit / sales) * 100

def calculate_opm_with_cross_check(operating_profit: float, sales: float, pre_existing_opm: float, company_name: str, year: int) -> float | None:
    """
    Calculates OPM and cross-checks it against a pre-existing field.
    Logs an anomaly if the variance is greater than 1%.
    """
    if sales <= 0:
        return None
    
    calculated_opm = (operating_profit / sales) * 100
    
    # Cross-check anomaly logic
    if abs(calculated_opm - pre_existing_opm) > 1.0:
        logger.warning(
            f"OPM Mismatch for {company_name} ({year}): "
            f"Calculated={calculated_opm:.2f}%, "
            f"Pre-existing={pre_existing_opm:.2f}%"
        )
        
    return calculated_opm

def calculate_roe(net_profit: float, equity_capital: float, reserves: float) -> float | None:
    """Calculate Return on Equity. Returns None if total equity <= 0."""
    total_equity = equity_capital + reserves
    if total_equity <= 0:
        return None
    return (net_profit / total_equity) * 100

def calculate_roce(ebit: float, equity: float, reserves: float, borrowings: float, broad_sector: str) -> dict:
    """
    Calculate ROCE and apply sector tracking logic.
    For 'Financials', tags evaluation with a relative benchmark.
    """
    capital_employed = equity + reserves + borrowings
    
    # Standard check for valid denominator
    if capital_employed <= 0:
        return {"roce": None, "evaluation_mode": "Invalid Capital"}
        
    roce_value = (ebit / capital_employed) * 100
    
    # Financial sector branch modification
    if broad_sector.strip().lower() == "financials":
        return {"roce": roce_value, "evaluation_mode": "Sector-Relative Benchmark"}
        
    return {"roce": roce_value, "evaluation_mode": "Absolute Threshold"}

def calculate_roa(net_profit: float, total_assets: float) -> float | None:
    """Calculate Return on Assets. Returns None if total_assets is 0."""
    if total_assets <= 0:
        return None
    return (net_profit / total_assets) * 100

def calculate_debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float
) -> float | None:
    """
    Calculate Debt-to-Equity Ratio.
    Returns None if total equity <= 0.
    Returns 0 for debt-free companies.
    """

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    if borrowings == 0:
        return 0

    return borrowings / total_equity

def calculate_interest_coverage_ratio(
    operating_profit: float,
    other_income: float,
    interest: float
) -> dict:
    """
    Calculate Interest Coverage Ratio (ICR).
    """

    if interest <= 0:
        return {
            "icr": None,
            "status": "Debt Free"
        }

    icr = (operating_profit + other_income) / interest

    if icr < 1.5:
        return {
            "icr": icr,
            "status": "Weak Coverage"
        }

    return {
        "icr": icr,
        "status": "Healthy"
    }

def calculate_net_debt(
    borrowings: float,
    investments: float
) -> float:
    """
    Calculate Net Debt.
    """

    return borrowings - investments

def calculate_asset_turnover(
    sales: float,
    total_assets: float
) -> float | None:
    """
    Calculate Asset Turnover Ratio.
    """

    if total_assets <= 0:
        return None

    return sales / total_assets