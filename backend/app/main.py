from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.middleware.audit import AuditLogMiddleware
from backend.app.routers import cases, wallets, auth

app = FastAPI(
    title="Project Acetone Security Engine",
    version="1.0.0"
)

# Security Audit Trail Middleware
app.add_middleware(AuditLogMiddleware)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(cases.router, prefix="/cases", tags=["Cases"])
app.include_router(wallets.router, prefix="/wallets", tags=["Wallets"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "Acetone Backend Security Engine Active"}
