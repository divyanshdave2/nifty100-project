from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/sectors")
def get_sectors():
    return [
        {"sector": "IT", "company_count": 10, "median_roe": 25.0},
        {"sector": "Banking", "company_count": 12, "median_roe": 15.0}
    ]

@router.get("/sectors/{sector}/companies")
def get_sector_companies(sector: str):
    if sector.upper() not in ["IT", "BANKING", "FINANCE", "CONSUMER"]:
        raise HTTPException(status_code=404, detail="Unknown sector")
    return [{"ticker": "TCS", "sector": sector}]