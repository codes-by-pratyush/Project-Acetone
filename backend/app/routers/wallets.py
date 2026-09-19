from fastapi import APIRouter
from celery.result import AsyncResult

from Blockchain.tasks.celery_app import celery_app
from Blockchain.tasks.blockchain_tasks import analyze_wallet


router = APIRouter(
    prefix="/wallets",
    tags=["Wallets"],
)


@router.get("/task/{task_id}")
def get_analysis_task(task_id: str):
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
def get_mock_trace(address: str, max_hops: int = 4):

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
def get_mock_risk(address: str):

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


@router.post("/{address}/analyze")
def analyze_wallet_endpoint(address: str):
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