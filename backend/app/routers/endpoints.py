from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Path, Query
from backend.app.schemas.api_contracts import (
    TraceResponse,
    CaseCreateRequest,
    CaseResponse
)

router = APIRouter()

@router.get("/wallets/{id}/trace", response_model=TraceResponse)
async def trace_wallet(id: str = Path(...), depth: int = Query(1, ge=1, le=10)):
    return TraceResponse(
        wallet_address=id,
        risk_score=85.5,
        associated_cases=["CASE-001", "CASE-002"],
        hop_depth=depth
    )

@router.post("/cases", response_model=CaseResponse)
async def create_case(payload: CaseCreateRequest):
    return CaseResponse(
        case_number=payload.case_number,
        title=payload.title,
        description=payload.description,
        investigator_id=payload.investigator_id,
        id=1,
        created_at=datetime.now(timezone.utc),
        status="OPEN"
    )

@router.get("/cases", response_model=List[CaseResponse])
async def list_cases():
    return [
        CaseResponse(
            case_number="CASE-001",
            title="Suspicious Outflow Case",
            description="Active investigation",
            investigator_id="INV-99",
            id=1,
            created_at=datetime.now(timezone.utc),
            status="OPEN"
        )
    ]