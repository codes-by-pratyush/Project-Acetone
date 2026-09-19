from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Removed the "backend." prefix so it runs correctly in Docker
from app.routers.endpoints import router as api_router
from app.routers import cases, wallets, auth

app = FastAPI(
    title="Crypto Investigation API",
    version="1.0.0",
    description="API contract specifications for cases, wallet tracing, risk, and alerts.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core routes & M4 Database API
app.include_router(api_router)

# Mock routes & Authentication
app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(wallets.router)

if __name__ == "__main__":
    import uvicorn
    # Updated uvicorn path to match the standard Docker environment
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)