import pytest
from src.analytics.cagr import (
    calculate_cagr,
    calculate_revenue_cagr_3y,
    calculate_pat_cagr_5y,
    calculate_eps_cagr_10y
)

def test_normal_cagr():
    result = calculate_cagr(100, 200, 5)

    assert round(result["cagr"], 2) == 14.87
    assert result["flag"] is None

# Test 2: Zero Base
def test_zero_base():
    result = calculate_cagr(0, 100, 5)

    assert result["cagr"] is None
    assert result["flag"] == "ZERO_BASE"


# Test 3: Turnaround
def test_turnaround():
    result = calculate_cagr(-100, 100, 5)

    assert result["cagr"] is None
    assert result["flag"] == "TURNAROUND"


# Test 4: Decline to Loss
def test_decline_to_loss():
    result = calculate_cagr(100, -100, 5)

    assert result["cagr"] is None
    assert result["flag"] == "DECLINE_TO_LOSS"


# Test 5: Negative to Negative
def test_negative():
    result = calculate_cagr(-100, -50, 5)

    assert result["cagr"] is None
    assert result["flag"] == "NEGATIVE"


# Test 6: Insufficient Data
def test_insufficient_data():
    result = calculate_cagr(100, 200, 0)

    assert result["cagr"] is None
    assert result["flag"] == "INSUFFICIENT_DATA"

# Test 7: Revenue CAGR
def test_revenue_cagr():
    result = calculate_revenue_cagr_3y(100, 150)

    assert result["flag"] is None
    assert round(result["cagr"], 2) == 14.47


# Test 8: PAT CAGR
def test_pat_cagr():
    result = calculate_pat_cagr_5y(100, 200)

    assert result["flag"] is None
    assert round(result["cagr"], 2) == 14.87


# Test 9: EPS CAGR
def test_eps_cagr():
    result = calculate_eps_cagr_10y(100, 300)

    assert result["flag"] is None
    assert round(result["cagr"], 2) == 11.61