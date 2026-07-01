from src.analytics.cashflow import (
    calculate_free_cash_flow,
    classify_fcf_quality,
    calculate_cfo_pat_ratio,
    calculate_capex_intensity,
    classify_capital_allocation
)

# Test 1
def test_normal_fcf():
    assert calculate_free_cash_flow(500, -150) == 350


# Test 2
def test_negative_fcf():
    assert calculate_free_cash_flow(100, -250) == -150


# Test 3
def test_zero_fcf():
    assert calculate_free_cash_flow(200, -200) == 0

# Test 4
def test_high_quality_fcf():
    assert classify_fcf_quality([100, 150, 200]) == "High Quality"


# Test 5
def test_moderate_quality_fcf():
    assert classify_fcf_quality([100, -100]) == "Moderate"


# Test 6
def test_poor_quality_fcf():
    assert classify_fcf_quality([-50, -100, -150]) == "Poor"


# Test 7
def test_no_data():
    assert classify_fcf_quality([]) == "No Data"

# Test 8
def test_cfo_pat_high():
    assert calculate_cfo_pat_ratio(120, 100) == 1.2


# Test 9
def test_cfo_pat_moderate():
    assert calculate_cfo_pat_ratio(80, 100) == 0.8


# Test 10
def test_cfo_pat_weak():
    assert calculate_cfo_pat_ratio(30, 100) == 0.3


# Test 11
def test_cfo_pat_zero_profit():
    assert calculate_cfo_pat_ratio(100, 0) is None

# Test 12
def test_capex_intensity_asset_light():
    assert calculate_capex_intensity(-20, 1000) == 2.0


# Test 13
def test_capex_intensity_moderate():
    assert calculate_capex_intensity(-60, 1000) == 6.0


# Test 14
def test_capex_intensity_capital_intensive():
    assert calculate_capex_intensity(-100, 1000) == 10.0


# Test 15
def test_capex_intensity_zero_sales():
    assert calculate_capex_intensity(-100, 0) is None


# Test 16
def test_growth_company():
    assert classify_capital_allocation(500, -300, 100) == "Growth"


# Test 17
def test_mature_company():
    assert classify_capital_allocation(500, 100, -200) == "Mature"


# Test 18
def test_distressed_company():
    assert classify_capital_allocation(-100, -50, 200) == "Distressed"


# Test 19
def test_unclassified_company():
    assert classify_capital_allocation(100, 50, 50) == "Unclassified"