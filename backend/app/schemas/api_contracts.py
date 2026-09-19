from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.app.schemas.validators import (
    validate_wallet_address,
    validate_tx_hash,
    validate_positive_amount,
    validate_non_future_timestamp,
)


class BaseContract(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class NormalizedTransaction(BaseContract):
    tx_hash: str = Field(..., description="Transaction hash with 0x prefix")
    from_address: str = Field(..., description="Sender wallet address")
    to_address: str = Field(..., description="Receiver wallet address")
    amount: float = Field(..., gt=0, description="Transfer amount strictly > 0")
    asset: str = Field(default="ETH", max_length=10)
    timestamp: datetime = Field(..., description="ISO 8601 transaction timestamp")
    chain: str = Field(default="ethereum", max_length=32)
    fee: Optional[float] = Field(default=0.0, ge=0)

    @field_validator("tx_hash")
    @classmethod
    def check_tx_hash(cls, v: str) -> str:
        return validate_tx_hash(v)

    @field_validator("from_address", "to_address")
    @classmethod
    def check_addresses(cls, v: str) -> str:
        return validate_wallet_address(v)

    @field_validator("amount")
    @classmethod
    def check_amount(cls, v: float) -> float:
        return validate_positive_amount(v)

    @field_validator("timestamp")
    @classmethod
    def check_timestamp(cls, v: datetime) -> datetime:
        return validate_non_future_timestamp(v)


# Backward-compatible name used by other parts of the backend.
TransactionContract = NormalizedTransaction


class WalletTraceResponse(BaseContract):
    root_wallet: str
    depth: int = Field(..., ge=1, le=10)
    total_volume: float = Field(..., ge=0)
    transactions: List[NormalizedTransaction] = []


class WalletRiskResponse(BaseContract):
    wallet_address: str
    risk_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: str
    flagged_reasons: List[str] = []


class WalletVASPResponse(BaseContract):
    wallet_address: str
    vasp_name: Optional[str] = None
    is_sanctioned: bool = False
    category: Optional[str] = None


class CaseCreateRequest(BaseContract):
    case_number: str = Field(..., min_length=3, max_length=64)
    title: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    investigator_id: str = Field(..., min_length=2, max_length=64)


class CaseResponse(BaseContract):
    id: int
    case_number: str = ""
    title: str
    description: Optional[str] = None
    investigator_id: str = ""
    created_at: datetime
    status: str
    transactions: List[NormalizedTransaction] = []


class CaseReportResponse(BaseContract):
    case_id: int
    summary: str
    total_tainted_value: float = Field(..., ge=0)
    involved_wallets: List[str] = []
    generated_at: datetime


class AlertResponse(BaseContract):
    id: int
    wallet_address: str
    rule_name: str
    severity: str
    created_at: datetime


class TraceResponse(BaseContract):
    wallet_address: str
    risk_score: float = Field(..., ge=0.0, le=100.0)
    associated_cases: List[str] = []
    hop_depth: int = Field(default=1, ge=1, le=10)

    @field_validator("wallet_address")
    @classmethod
    def check_wallet(cls, v: str) -> str:
        return validate_wallet_address(v)


class AlertRuleContract(BaseContract):
    alert_name: str = Field(..., min_length=3, max_length=128)
    target_wallet: str = Field(..., description="Target wallet to monitor")
    threshold_amount: float = Field(..., gt=0)
    severity: str = Field(default="HIGH")

    @field_validator("target_wallet")
    @classmethod
    def check_target_wallet(cls, v: str) -> str:
        return validate_wallet_address(v)