from fastapi import APIRouter, Depends
from celery.result import AsyncResult

from app.schemas.wallets import WalletTraceRequest, WalletTraceResponse
from app.dependencies.auth import get_current_investigator
from Blockchain.tasks.celery_app import celery_app
from Blockchain.tasks.blockchain_tasks import analyze_wallet

router = APIRouter(
    prefix="/wallets",
    tags=["Wallet Tracing"],
)

@router.post("/trace", response_model=WalletTraceResponse)
def trace_wallet_activity(
    request: WalletTraceRequest,
    investigator: dict = Depends(get_current_investigator)
):
    """
    Standard contract endpoint for structured wallet tracing.
    """
    return WalletTraceResponse(
        wallet_address=request.wallet_address,
        risk_score=85,
        suspicious_peers=["0xBadGuyWallet1", "0xScammerWallet2"],
        recent_transactions=[
            {
                "tx_hash": "0xabc123...",
                "from_address": request.wallet_address,
                "to_address": "0xBadGuyWallet1",
                "amount": 5.5,
                "timestamp": "2026-09-19T10:00:00Z"
            }
        ]
    )

@router.post("/{address}/analyze")
def analyze_wallet_endpoint(
    address: str,
    investigator: dict = Depends(get_current_investigator)
):
    """
    Start background blockchain analysis for a wallet.
    Returns immediately with a Celery task ID.
    """
    task = analyze_wallet.delay(address)
    return {
        "status": "submitted",
        "wallet": address.lower(),
        "task_id": task.id,
    }

@router.get("/task/{task_id}")
def get_analysis_task(
    task_id: str,
    investigator: dict = Depends(get_current_investigator)
):
    """
    Get the status or result of a background wallet analysis task.
    """
    task = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "status": task.status,
    }

    if task.successful():
        response["result"] = task.result
    elif task.failed():
        response["error"] = str(task.result)

    return response

@router.get("/{address}/trace")
def get_mock_trace(
    address: str,
    max_hops: int = 4,
    investigator: dict = Depends(get_current_investigator)
):
    """
    Returns graph node and edge visualization data for frontend graph rendering.
    """
    return {
        "nodes": [
            {
                "data": {
                    "id": address,
                    "label": "Victim",
                    "risk_score": 0.1,
                }
            },
            {
                "data": {
                    "id": "0xExchangeWallet",
                    "label": "Binance Hot Wallet",
                    "risk_score": 0.9,
                }
            },
        ],
        "edges": [
            {
                "data": {
                    "source": address,
                    "target": "0xExchangeWallet",
                    "amount": 1.5,
                    "asset": "ETH",
                }
            }
        ],
    }

@router.get("/{address}/risk")
def get_mock_risk(
    address: str,
    investigator: dict = Depends(get_current_investigator)
):
    """
    Returns heuristic risk scoring and triggered detection rules.
    """
    return {
        "address": address,
        "overall_risk_score": 0.85,
        "flags": [
            {
                "rule": "High Velocity",
                "weight": 0.5,
                "evidence": "Funds moved within 3 minutes",
            },
            {
                "rule": "Fan-Out",
                "weight": 0.35,
                "evidence": "Split into 5 different wallets",
            },
        ],
    }