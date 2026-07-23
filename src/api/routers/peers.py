from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/peers/{group_name}")
def get_peer_percentiles(group_name: str):
    return {"peer_group": group_name, "percentiles": {"TCS": 95, "INFY": 88}}

@router.get("/companies/{ticker}/peers/compare")
def compare_peers(ticker: str):
    return {"ticker": ticker.upper(), "peer_average": {"roe": 20.0}, "company": {"roe": 25.0}}