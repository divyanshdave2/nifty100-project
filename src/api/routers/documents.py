from fastapi import APIRouter

router = APIRouter()

@router.get("/companies/{ticker}/documents")
def get_annual_reports(ticker: str):
    return [{"year": 2024, "url": f"https://example.com/reports/{ticker}_2024.pdf", "is_url_valid": True}]