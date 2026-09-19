from fastapi import FastAPI

from backend.app.routers.endpoints import router as api_router
from backend.app.routers import cases, wallets, auth

from Blockchain.monitoring.alchemy_webhook import router as alchemy_webhook_router


app = FastAPI(
    title="Crypto Investigation API",
    version="1.0.0",
    description="API contract specifications for cases, wallet tracing, risk, and alerts.",
)

# Core routes & M4 Database API
app.include_router(api_router)

# Mock routes & Authentication
app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(wallets.router)

# Blockchain monitoring / Alchemy webhook
app.include_router(alchemy_webhook_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )