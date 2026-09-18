import re
from datetime import datetime, timezone

# EVM (0x + 40 hex chars), BTC (Legacy/SegWit/Taproot), TRON (T + 33 base58)
EVM_REGEX = re.compile(r"^0x[a-fA-F0-9]{40}$")
BTC_REGEX = re.compile(r"^(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{25,90})$")
TRON_REGEX = re.compile(r"^T[a-zA-HJ-NP-Z1-9]{33}$")
TX_HASH_REGEX = re.compile(r"^0x[a-fA-F0-9]{64}$")

def validate_wallet_address(address: str) -> str:
    cleaned = address.strip()
    if EVM_REGEX.match(cleaned) or BTC_REGEX.match(cleaned) or TRON_REGEX.match(cleaned):
        return cleaned
    raise ValueError(f"Invalid blockchain wallet address format: '{address}'. Must be valid EVM (0x...), BTC, or TRC20 address.")

def validate_tx_hash(tx_hash: str) -> str:
    cleaned = tx_hash.strip()
    if TX_HASH_REGEX.match(cleaned):
        return cleaned.lower()
    raise ValueError(f"Invalid transaction hash format: '{tx_hash}'. Must be a 66-character 0x-prefixed hex string.")

def validate_positive_amount(amount: float) -> float:
    if amount <= 0:
        raise ValueError(f"Transaction amount must be strictly positive (> 0), got: {amount}")
    return amount

def validate_non_future_timestamp(ts: datetime) -> datetime:
    current = datetime.now(timezone.utc)
    target = ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
    if target > current:
        raise ValueError(f"Timestamp cannot be in the future. Received: {ts}")
    return ts