from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class NormalizedTransaction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_address: str = Field(..., alias="from")
    to_address: str = Field(..., alias="to")
    amount: float
    asset: str
    timestamp: datetime
    tx_hash: str
    chain: str
    fee: Optional[float] = 0.0

class WalletTraceResponse(BaseModel):
    root_wallet: str
    depth: int
    total_volume: float
    transactions: List[NormalizedTransaction]

class WalletRiskResponse(BaseModel):
    wallet_address: str
    risk_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: str
    flagged_reasons: List[str]

class WalletVASPResponse(BaseModel):
    wallet_address: str
    vasp_name: Optional[str] = None
    is_sanctioned: bool = False
    category: str

class CaseCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None

class CaseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    transactions: List[NormalizedTransaction] = []

class CaseReportResponse(BaseModel):
    case_id: int
    summary: str
    total_tainted_value: float
    involved_wallets: List[str]
    generated_at: datetime

class AlertResponse(BaseModel):
    id: int
    wallet_address: str
    rule_name: str
    severity: str
    created_at: datetime