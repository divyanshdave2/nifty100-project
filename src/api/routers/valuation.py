from fastapi import APIRouter

router = APIRouter()

@router.get("/market-cap/{ticker}")
def get_valuation_history(ticker: str):
    return {"ticker": ticker.upper(), "historical_pe": [{"year": 2024, "pe": 28.5}]}