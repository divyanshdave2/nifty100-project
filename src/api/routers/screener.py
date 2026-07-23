from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get("/screener")
def run_screener(min_roe: float = Query(0.0), max_de: float = Query(5.0), sector: str = None):
    if min_roe < 0 or max_de < 0:
        raise HTTPException(status_code=400, detail="Invalid screening parameters")
    return [
        {"ticker": "TCS", "name": "Tata Consultancy Services", "roe": 45.0, "de": 0.0},
        {"ticker": "RELIANCE", "name": "Reliance Industries", "roe": 12.5, "de": 0.4}
    ]