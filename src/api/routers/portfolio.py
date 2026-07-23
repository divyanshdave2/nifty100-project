from fastapi import APIRouter

router = APIRouter()

@router.get("/portfolio/stats")
def get_portfolio_stats():
    return {"P10": 10.2, "P50": 18.5, "P90": 32.1}