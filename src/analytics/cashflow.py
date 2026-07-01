def calculate_free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    Free Cash Flow (FCF)

    Formula:
    FCF = Operating Cash Flow + Investing Cash Flow

    Investing cash flow is usually negative.
    """

    return operating_activity + investing_activity


def classify_fcf_quality(fcf_values: list[float]) -> str:
    """
    Classify average Free Cash Flow quality over multiple years.

    High Quality  : Average FCF > 0
    Moderate      : Average FCF = 0
    Poor          : Average FCF < 0
    """

    if len(fcf_values) == 0:
        return "No Data"

    average_fcf = sum(fcf_values) / len(fcf_values)

    if average_fcf > 0:
        return "High Quality"

    elif average_fcf == 0:
        return "Moderate"

    else:
        return "Poor"
    
def calculate_cfo_pat_ratio(
    operating_activity: float,
    net_profit: float
) -> float | None:
    """
    CFO / PAT Ratio

    Interpretation:
    >1.0  -> High Quality Earnings
    0.5-1 -> Moderate
    <0.5  -> Weak
    """

    if net_profit == 0:
        return None

    return operating_activity / net_profit


def calculate_capex_intensity(
    investing_activity: float,
    sales: float
) -> float | None:
    """
    CAPEX Intensity Ratio

    Formula:
    abs(Investing Cash Flow) / Sales × 100

    Lower value = Asset Light
    Higher value = Capital Intensive
    """

    if sales <= 0:
        return None

    return (abs(investing_activity) / sales) * 100


def classify_capital_allocation(
    operating_activity: float,
    investing_activity: float,
    financing_activity: float
) -> str:
    """
    Classify the company's capital allocation pattern.

    Returns one of:
    - Growth
    - Mature
    - Distressed
    """

    # Company is generating cash and investing heavily
    if operating_activity > 0 and investing_activity < 0:
        return "Growth"

    # Company generates cash but returns it to shareholders
    if operating_activity > 0 and financing_activity < 0:
        return "Mature"

    # Company has weak operating cash flow
    if operating_activity <= 0:
        return "Distressed"

    return "Unclassified"