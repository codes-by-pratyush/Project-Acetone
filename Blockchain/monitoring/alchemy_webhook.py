from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/webhooks",
    tags=["Blockchain Monitoring"]
)


@router.post("/alchemy")
async def alchemy_webhook(request: Request):
    """
    Receive blockchain activity notifications from Alchemy.

    For now, this endpoint only receives and logs the
    incoming event. Transaction processing will be added later.
    """

    payload = await request.json()

    print("\n======================================")
    print("ALCHEMY WEBHOOK RECEIVED")
    print("======================================")
    print(payload)

    return {
        "status": "received"
    }