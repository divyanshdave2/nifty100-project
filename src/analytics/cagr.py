def calculate_cagr(start: float, end: float, years: int):
    """
    Calculate Compound Annual Growth Rate (CAGR).
    Returns CAGR and status flag.
    """

    if years <= 0:
        return {"cagr": None, "flag": "INSUFFICIENT_DATA"}

    if start == 0:
        return {"cagr": None, "flag": "ZERO_BASE"}

    if start < 0 and end < 0:
        return {"cagr": None, "flag": "NEGATIVE"}

    if start < 0 and end > 0:
        return {"cagr": None, "flag": "TURNAROUND"}

    if start > 0 and end < 0:
        return {"cagr": None, "flag": "DECLINE_TO_LOSS"}

    cagr = ((end / start) ** (1 / years) - 1) * 100

    return {
        "cagr": cagr,
        "flag": None
    }

# Revenue CAGR
def calculate_revenue_cagr_3y(start, end):
    return calculate_cagr(start, end, 3)


def calculate_revenue_cagr_5y(start, end):
    return calculate_cagr(start, end, 5)


def calculate_revenue_cagr_10y(start, end):
    return calculate_cagr(start, end, 10)


# PAT CAGR
def calculate_pat_cagr_3y(start, end):
    return calculate_cagr(start, end, 3)


def calculate_pat_cagr_5y(start, end):
    return calculate_cagr(start, end, 5)


def calculate_pat_cagr_10y(start, end):
    return calculate_cagr(start, end, 10)


# EPS CAGR
def calculate_eps_cagr_3y(start, end):
    return calculate_cagr(start, end, 3)


def calculate_eps_cagr_5y(start, end):
    return calculate_cagr(start, end, 5)


def calculate_eps_cagr_10y(start, end):
    return calculate_cagr(start, end, 10)