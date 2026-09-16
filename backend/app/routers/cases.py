from fastapi import APIRouter

router = APIRouter(prefix="/cases", tags=["Cases"])

@router.get("/")
def get_mock_cases():
    # A fake list of cases so the frontend has something to display
    return [
        {
            "id": 101,
            "title": "Stolen Funds - Binance Transfer",
            "victim_wallet": "0x1234567890abcdef",
            "status": "Monitoring"
        },
        {
            "id": 102,
            "title": "Phishing Scam - Sepolia",
            "victim_wallet": "0xabcdef1234567890",
            "status": "Alert Raised"
        }
    ]

@router.post("/new")
def create_mock_case(victim_wallet: str):
    # Simulates creating a case
    return {
        "message": "Case successfully created",
        "case_id": 103,
        "victim_wallet": victim_wallet,
        "status": "Reported"
    }