def normalize_year(year):

    try:
        return int(year)

    except:
        return None


def normalize_ticker(ticker):

    if ticker is None:
        return None

    return str(ticker).strip().upper()