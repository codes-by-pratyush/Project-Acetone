from fastapi import APIRouter, Request

from Blockchain.monitoring.monitor import WalletMonitor


router = APIRouter(
    prefix="/webhooks",
    tags=["Blockchain Monitoring"],
)


# Shared wallet monitor used by both the API and Alchemy webhook
wallet_monitor = WalletMonitor()


@router.get("/wallets")
async def get_watched_wallets():
    return {
        "watched_wallets": wallet_monitor.get_watched_wallets()
    }


@router.post("/wallets/{wallet_address}")
async def add_watched_wallet(wallet_address: str):
    wallet_monitor.add_wallet(
        wallet_address,
        start_block=0,
    )

    return {
        "status": "monitoring",
        "wallet": wallet_address.lower(),
    }


@router.delete("/wallets/{wallet_address}")
async def remove_watched_wallet(wallet_address: str):
    wallet_monitor.remove_wallet(wallet_address)

    return {
        "status": "removed",
        "wallet": wallet_address.lower(),
    }


@router.post("/alchemy")
async def alchemy_webhook(request: Request):
    """
    Receive Address Activity notifications from Alchemy.

    Alchemy sends transfer activity inside:
        payload["event"]["activity"]
    """

    payload = await request.json()

    print("\n======================================")
    print("ALCHEMY WEBHOOK RECEIVED")
    print("======================================")
    print(payload)

    # --------------------------------------------------------
    # Validate webhook type
    # --------------------------------------------------------

    webhook_type = payload.get("type")

    if webhook_type != "ADDRESS_ACTIVITY":
        return {
            "status": "ignored",
            "reason": "unsupported webhook type",
            "type": webhook_type,
        }

    # --------------------------------------------------------
    # Extract event
    # --------------------------------------------------------

    event = payload.get("event", {})
    activity = event.get("activity", [])

    if not activity:
        return {
            "status": "ignored",
            "reason": "no activity found",
        }

    # --------------------------------------------------------
    # Find wallets affected by the webhook
    # --------------------------------------------------------

    affected_wallets = set()

    for transfer in activity:
        from_address = transfer.get("fromAddress")
        to_address = transfer.get("toAddress")

        if from_address:
            affected_wallets.add(
                from_address.lower()
            )

        if to_address:
            affected_wallets.add(
                to_address.lower()
            )

    # --------------------------------------------------------
    # Process watched wallets
    # --------------------------------------------------------

    processed_wallets = []
    ignored_wallets = []

    all_transfers = []
    latest_blocks = {}

    for wallet_address in affected_wallets:

        if not wallet_monitor.is_watched(
            wallet_address
        ):
            ignored_wallets.append(
                wallet_address
            )
            continue

        transfers, latest_block = (
            wallet_monitor.check_wallet(
                wallet_address
            )
        )

        processed_wallets.append(
            wallet_address
        )

        if latest_block is not None:
            latest_blocks[
                wallet_address
            ] = latest_block

        all_transfers.extend(
            transfers
        )

    # --------------------------------------------------------
    # Return processing result
    # --------------------------------------------------------

    return {
        "status": "processed",
        "webhook_type": webhook_type,
        "event_id": payload.get("id"),
        "network": event.get("network"),
        "activity_count": len(activity),
        "affected_wallets": list(
            affected_wallets
        ),
        "processed_wallets": processed_wallets,
        "ignored_wallets": ignored_wallets,
        "transfers": all_transfers,
        "latest_blocks": latest_blocks,
    }