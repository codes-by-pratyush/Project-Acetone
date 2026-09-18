from datetime import datetime
from typing import List
from fastapi import APIRouter, Path, Query
from backend.app.schemas.api_contracts import (
    NormalizedTransaction,
    WalletTraceResponse,
    WalletRiskResponse,
    WalletVASPResponse,
    CaseCreateRequest,
    CaseResponse,
    CaseReportResponse,
    AlertResponse,
)

router = APIRouter()

@router.get("/wallets/{id}/trace", response_model=WalletTraceResponse)
async def trace_wallet(id: str = Path(...), depth: int = Query(2, le=5)):
    return WalletTraceResponse(
        root_wallet=id,
        depth=depth,
        total_volume=1.5,
        transactions=[
            NormalizedTransaction(
                from_address=id,
                to_address="0xTargetAddress",
                amount=1.5,
                asset="ETH",
                timestamp=datetime.utcnow(),
                tx_hash="0xabc123456789",
                chain="ethereum",
                fee=0.002,
            )
        ],
    )

@router.get("/wallets/{id}/risk", response_model=WalletRiskResponse)
async def get_wallet_risk(id: str = Path(...)):
    return WalletRiskResponse(
        wallet_address=id,
        risk_score=75.5,
        risk_level="High",
        flagged_reasons=["Transfer from sanctioned mixer"],
    )

@router.get("/wallets/{id}/vasp", response_model=WalletVASPResponse)
async def get_wallet_vasp(id: str = Path(...)):
    return WalletVASPResponse(
        wallet_address=id,
        vasp_name="Tornado Cash",
        is_sanctioned=True,
        category="Mixer",
    )

@router.post("/cases", response_model=CaseResponse)
async def create_case(payload: CaseCreateRequest):
    return CaseResponse(
        id=1,
        title=payload.title,
        description=payload.description,
        status="open",
        created_at=datetime.utcnow(),
        transactions=[],
    )

@router.get("/cases", response_model=List[CaseResponse])
async def list_cases():
    return [
        CaseResponse(
            id=1,
            title="Suspicious Outflow Case",
            description="Active investigation",
            status="open",
            created_at=datetime.utcnow(),
            transactions=[],
        )
    ]

@router.get("/reports/{case_id}", response_model=CaseReportResponse)
async def generate_case_report(case_id: int = Path(...)):
    return CaseReportResponse(
        case_id=case_id,
        summary="Automated forensic case audit completed.",
        total_tainted_value=125000.0,
        involved_wallets=["0xAddress1", "0xAddress2"],
        generated_at=datetime.utcnow(),
    )

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts():
    return [
        AlertResponse(
            id=1,
            wallet_address="0xSuspiciousAddress",
            rule_name="High Velocity Hop Detected",
            severity="critical",
            created_at=datetime.utcnow(),
        )
    ]