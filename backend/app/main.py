from fastapi import FastAPI
from app.routers import cases, wallets, auth

app = FastAPI(title="Project Acetone API", version="1.0.0")

# Register the mock routers
app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(wallets.router)

@app.get("/health")
def health_check():
    return {"status": "Acetone Backend is running"}