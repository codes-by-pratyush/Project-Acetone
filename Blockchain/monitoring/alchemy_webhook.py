from fastapi import APIRouter, Request

from Blockchain.monitoring.monitor import WalletMonitor


router = APIRouter(
    prefix="/webhooks",
    tags=["Blockchain Monitoring"]
)


# Shared wallet monitor for incoming webhook events
wallet_monitor = WalletMonitor()


@router.post("/alchemy")
async def alchemy_webhook(request: Request):
    """
    Receive blockchain activity notifications from Alchemy
    and process the affected watched wallet.
    """

    payload = await request.json()

    print("\n======================================")
    print("ALCHEMY WEBHOOK RECEIVED")
    print("======================================")
    print(payload)

    wallet_address = payload.get("wallet")

    if not wallet_address:
        return {
            "status": "ignored",
            "reason": "wallet address not provided"
        }

    transfers, latest_block = wallet_monitor.check_wallet(wallet_address)

    return {
        "status": "processed",
        "wallet": wallet_address,
        "transfers": transfers,
        "latest_block": latest_block
    }