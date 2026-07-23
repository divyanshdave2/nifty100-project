import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import health, companies, screener, sectors, peers, valuation, portfolio, documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: Export OpenAPI spec
    os.makedirs("docs", exist_ok=True)
    with open("docs/openapi.json", "w") as f:
        json.dump(app.openapi(), f, indent=2)
    print("Exported OpenAPI spec to docs/openapi.json")
    yield
    # Shutdown logic (if needed in future)

app = FastAPI(
    title="NIFTY 100 Financial Intelligence API",
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"--> {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"<-- Status {response.status_code}")
    return response

# Root Route
@app.get("/")
def root():
    return {
        "message": "Welcome to NIFTY 100 Financial Intelligence API",
        "documentation": "/docs",
        "health_check": "/api/v1/health"
    }

# Include Routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(companies.router, prefix="/api/v1", tags=["Companies"])
app.include_router(screener.router, prefix="/api/v1", tags=["Screener"])
app.include_router(sectors.router, prefix="/api/v1", tags=["Sectors"])
app.include_router(peers.router, prefix="/api/v1", tags=["Peers"])
app.include_router(valuation.router, prefix="/api/v1", tags=["Valuation"])
app.include_router(portfolio.router, prefix="/api/v1", tags=["Portfolio"])
app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=True)