import time
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, Response
from pydantic import BaseModel, Field

MOCK_DISCLAIMER = "MOCK - NOT A REAL GOVERNMENT SYSTEM"

app = FastAPI(
    title="Mock NCRP/SAHYOG API Service",
    description="Simulated government cybercrime integration endpoint for SIH26183 Acetone.",
    version="1.0.0"
)

class CaseSyncRequest(BaseModel):
    case_number: str = Field(..., description="Acetone internal case ID")
    victim_wallet: str = Field(..., description="Reported wallet address")
    suspect_wallet: Optional[str] = Field(default=None, description="Traced target wallet")
    total_stolen_amount: float = Field(..., gt=0)
    asset: str = Field(default="ETH")
    investigator_badge_id: str = Field(..., min_length=3)
    risk_score: float = Field(..., ge=0, le=100)

class CaseSyncResponse(BaseModel):
    acknowledgment_id: str
    case_number: str
    status: str
    received_at: datetime
    simulated_portal: str
    disclaimer: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "mock-ncrp", "disclaimer": MOCK_DISCLAIMER}

@app.post("/mock-ncrp/case-sync", response_model=CaseSyncResponse, status_code=201)
def sync_case_to_ncrp(payload: CaseSyncRequest, response: Response):
    time.sleep(0.3)
    response.headers["X-Disclaimer"] = MOCK_DISCLAIMER
    
    ack_id = f"NCRP-SAHYOG-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    
    return CaseSyncResponse(
        acknowledgment_id=ack_id,
        case_number=payload.case_number,
        status="ACKNOWLEDGED_UNDER_REVIEW",
        received_at=datetime.now(timezone.utc),
        simulated_portal="National Cyber Crime Reporting Portal (SAHYOG Gateway)",
        disclaimer=MOCK_DISCLAIMER
    )