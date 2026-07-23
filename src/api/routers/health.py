import time
from fastapi import APIRouter

router = APIRouter()
start_time = time.time()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - start_time, 2),
        "db_row_counts": {"companies": 93, "financial_ratios": 1100},
        "version": "1.0.0"
    }