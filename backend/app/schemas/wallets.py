from pydantic import BaseModel, Field
from typing import List, Optional

class WalletTraceRequest(BaseModel):
    wallet_address: str = Field(..., description="The blockchain wallet address to trace.")
    chain: Optional[str] = Field("ethereum", description="The blockchain network.")

class TransactionNode(BaseModel):
    tx_hash: str
    from_address: str
    to_address: str
    amount: float
    timestamp: str

class WalletTraceResponse(BaseModel):
    wallet_address: str
    risk_score: int = Field(..., ge=0, le=100)
    suspicious_peers: List[str]
    recent_transactions: List[TransactionNode]