from fastapi import APIRouter

router = APIRouter(prefix="/wallets", tags=["Wallets"])

@router.get("/{address}/trace")
def get_mock_trace(address: str, max_hops: int = 4):
    # Returns a fake graph format that Cytoscape.js expects
    return {
        "nodes": [
            {"data": {"id": address, "label": "Victim", "risk_score": 0.1}},
            {"data": {"id": "0xExchangeWallet", "label": "Binance Hot Wallet", "risk_score": 0.9}}
        ],
        "edges": [
            {"data": {"source": address, "target": "0xExchangeWallet", "amount": 1.5, "asset": "ETH"}}
        ]
    }

@router.get("/{address}/risk")
def get_mock_risk(address: str):
    # Returns a fake risk score and the reasons for it
    return {
        "address": address,
        "overall_risk_score": 0.85,
        "flags": [
            {"rule": "High Velocity", "weight": 0.5, "evidence": "Funds moved within 3 minutes"},
            {"rule": "Fan-Out", "weight": 0.35, "evidence": "Split into 5 different wallets"}
        ]
    }