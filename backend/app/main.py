from fastapi import FastAPI
from backend.app.routers.endpoints import router as api_router

app = FastAPI(
    title="Crypto Investigation API",
    version="1.0.0",
    description="API contract specifications for cases, wallet tracing, risk, and alerts.",
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
