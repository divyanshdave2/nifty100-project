import pytest
import logging
from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_opm_with_cross_check,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    calculate_interest_coverage_ratio,
    calculate_net_debt,
    calculate_asset_turnover
)

# Test 1: Normal Case (Standard Profitable Company)
def test_profitability_ratios_normal_case():
    # standard 10% net margin evaluation
    npm = calculate_net_profit_margin(10, 100)
    assert npm == 10.0
    
    roa = calculate_roa(15, 100)
    assert roa == 15.0

# Test 2: Zero Denominator (Sales)
def test_zero_sales_returns_none():
    assert calculate_net_profit_margin(50, 0) is None
    assert calculate_opm_with_cross_check(20, 0, 15.0, "Test Corp", 2026) is None

# Test 3: Zero Denominator (Assets)
def test_zero_assets_returns_none():
    assert calculate_roa(25, 0) is None

# Test 4: Negative Equity Safeguard
def test_negative_or_zero_equity_returns_none():
    # Equity + reserves = 0
    assert calculate_roe(10, 0, 0) is None
    # Equity + reserves < 0
    assert calculate_roe(10, 100, -150) is None

# Test 5: OPM Mismatch Triggering Logger
def test_opm_mismatch_logging(caplog):
    with caplog.at_level(logging.WARNING):
        # Calculated: (30 / 100) * 100 = 30%. Provided: 10%. Delta = 20% (> 1%)
        calculate_opm_with_cross_check(30, 100, 10.0, "Anomaly Inc", 2026)
        assert len(caplog.records) == 1
        assert "OPM Mismatch for Anomaly Inc" in caplog.text

# Test 6: Financial Sector Broad Path Verification
def test_financials_sector_benchmark_mode():
    result = calculate_roce(20, 50, 50, 50, "Financials")
    assert result["evaluation_mode"] == "Sector-Relative Benchmark"
    assert result["roce"] == (20 / 150) * 100

# Test 7: Standard Exact Value Match (ROE)
def test_standard_roe_exact_calculation():
    # Net profit=20, Equity Capital=50, Reserves=50 -> ROE = 20/100 * 100 = 20%
    res = calculate_roe(20, 50, 50)
    assert res == 20.0

# Test 8: Standard Exact Value Match (ROCE)
def test_standard_roce_exact_calculation():
    # EBIT=30, CapEmployed=150 -> ROCE = 30/150 * 100 = 20%
    result = calculate_roce(30, 50, 50, 50, "IT Services")
    assert result["roce"] == 20.0
    assert result["evaluation_mode"] == "Absolute Threshold"

# Test 9: Debt-Free Company
def test_debt_to_equity_debt_free():
    assert calculate_debt_to_equity(0, 100, 50) == 0


# Test 10: Normal Debt-to-Equity
def test_debt_to_equity_normal():
    assert calculate_debt_to_equity(75, 100, 50) == 0.5


# Test 11: Invalid Equity
def test_debt_to_equity_invalid():
    assert calculate_debt_to_equity(100, 0, 0) is None


# Test 12: Negative Equity
def test_debt_to_equity_negative():
    assert calculate_debt_to_equity(100, 50, -100) is None

# Test 13: Interest Coverage Normal
def test_interest_coverage_normal():
    result = calculate_interest_coverage_ratio(100, 20, 40)

    assert result["icr"] == 3.0
    assert result["status"] == "Healthy"


# Test 14: Debt Free Company
def test_interest_coverage_debt_free():
    result = calculate_interest_coverage_ratio(100, 20, 0)

    assert result["icr"] is None
    assert result["status"] == "Debt Free"


# Test 15: Weak Coverage
def test_interest_coverage_weak():
    result = calculate_interest_coverage_ratio(10, 0, 10)

    assert result["icr"] == 1.0
    assert result["status"] == "Weak Coverage"

# Test 16: Net Debt
def test_net_debt():
    assert calculate_net_debt(500, 200) == 300

# Test 17: Asset Turnover Normal
def test_asset_turnover_normal():
    assert calculate_asset_turnover(500, 250) == 2.0


# Test 18: Asset Turnover Zero Assets
def test_asset_turnover_zero_assets():
    assert calculate_asset_turnover(500, 0) is None