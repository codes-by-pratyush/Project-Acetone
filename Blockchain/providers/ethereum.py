import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv
from web3 import Web3


# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")

if not ALCHEMY_API_KEY:
    raise ValueError("ALCHEMY_API_KEY was not found in .env")


RPC_URL = f"https://eth-sepolia.g.alchemy.com/v2/{ALCHEMY_API_KEY}"


# ============================================================
# HTTP RETRY CONFIGURATION
# ============================================================

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["POST"],
)

adapter = HTTPAdapter(max_retries=retry_strategy)

http_session = requests.Session()
http_session.mount("https://", adapter)
http_session.mount("http://", adapter)


# ============================================================
# RATE LIMITING
# ============================================================

MIN_REQUEST_INTERVAL = 0.25
_last_request_time = 0.0


def wait_for_rate_limit():
    global _last_request_time

    current_time = time.monotonic()
    elapsed = current_time - _last_request_time

    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)

    _last_request_time = time.monotonic()


def post_to_provider(request_body):
    wait_for_rate_limit()

    response = http_session.post(
        RPC_URL,
        json=request_body,
        timeout=30,
    )

    response.raise_for_status()

    return response


# ============================================================
# WEB3 CONNECTION
# ============================================================

web3 = Web3(Web3.HTTPProvider(RPC_URL))

if web3.is_connected():
    print("Connected to Ethereum Sepolia through Alchemy!")
    print("Latest block:", web3.eth.block_number)
else:
    print("Connection failed.")


# ============================================================
# TRANSFER CACHE
# ============================================================

TRANSFER_CACHE = {}

CACHE_TTL_SECONDS = 60


def get_cached_transfers(wallet_address):
    wallet_address = wallet_address.lower()

    cached = TRANSFER_CACHE.get(wallet_address)

    if cached is None:
        return None

    cached_data, cached_time = cached

    if time.monotonic() - cached_time > CACHE_TTL_SECONDS:
        del TRANSFER_CACHE[wallet_address]
        return None

    return cached_data


def cache_transfers(wallet_address, transfers):
    wallet_address = wallet_address.lower()

    TRANSFER_CACHE[wallet_address] = (
        transfers,
        time.monotonic(),
    )


def clear_transfer_cache(wallet_address=None):
    """
    Clear cached transfer data.

    If wallet_address is provided, only that wallet's cache
    is cleared.

    If wallet_address is None, the entire cache is cleared.
    """

    if wallet_address is None:
        TRANSFER_CACHE.clear()
    else:
        TRANSFER_CACHE.pop(wallet_address.lower(), None)


# ============================================================
# FULL WALLET TRANSFER HISTORY
# ============================================================

def get_wallet_transfers(wallet_address):
    wallet_address = wallet_address.lower()

    # Check cache first
    cached_transfers = get_cached_transfers(wallet_address)

    if cached_transfers is not None:
        print(f"Cache hit: {wallet_address}")
        return cached_transfers

    print(f"Cache miss: {wallet_address}")
    print("Fetching wallet transfers from Alchemy...")

    all_transfers = []
    page_key = None

    while True:
        request_params = {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "fromAddress": wallet_address,
            "category": ["external", "erc20"],
            "withMetadata": True,
            "excludeZeroValue": True,
        }

        if page_key:
            request_params["pageKey"] = page_key

        request_body = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "alchemy_getAssetTransfers",
            "params": [request_params],
        }

        response = post_to_provider(request_body)

        data = response.json()

        if "error" in data:
            raise RuntimeError(data["error"])

        result = data["result"]

        all_transfers.extend(result["transfers"])

        page_key = result.get("pageKey")

        if not page_key:
            break

    # Store result in cache
    cache_transfers(wallet_address, all_transfers)

    print(
        f"Cached {len(all_transfers)} transfers "
        f"for {CACHE_TTL_SECONDS} seconds."
    )

    return all_transfers


# ============================================================
# LATEST WALLET TRANSFERS
# ============================================================

def get_latest_wallet_transfers(wallet_address, from_block="0x0"):
    wallet_address = wallet_address.lower()

    all_transfers = []

    for direction in ["outgoing", "incoming"]:

        page_key = None

        while True:

            request_params = {
                "fromBlock": from_block,
                "toBlock": "latest",
                "category": ["external", "erc20"],
                "withMetadata": True,
                "excludeZeroValue": True,
                "maxCount": "0x64",
            }

            if direction == "outgoing":
                request_params["fromAddress"] = wallet_address
            else:
                request_params["toAddress"] = wallet_address

            if page_key:
                request_params["pageKey"] = page_key

            request_body = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "alchemy_getAssetTransfers",
                "params": [request_params],
            }

            response = post_to_provider(request_body)

            data = response.json()

            if "error" in data:
                raise RuntimeError(data["error"])

            result = data["result"]

            all_transfers.extend(result["transfers"])

            page_key = result.get("pageKey")

            if not page_key:
                break

    return all_transfers


# ============================================================
# NEW TRANSFERS SINCE LAST CHECKED BLOCK
# ============================================================

def get_new_wallet_transfers(wallet_address, last_checked_block):
    latest_block = web3.eth.block_number

    if last_checked_block >= latest_block:
        return [], latest_block

    from_block = hex(last_checked_block + 1)

    transfers = get_latest_wallet_transfers(
        wallet_address,
        from_block=from_block,
    )

    return transfers, latest_block


# ============================================================
# TRANSACTION FEE
# ============================================================

def get_transaction_fee(transaction_hash):
    transaction = web3.eth.get_transaction(transaction_hash)

    receipt = web3.eth.get_transaction_receipt(transaction_hash)

    gas_used = receipt["gasUsed"]

    gas_price = transaction["gasPrice"]

    fee_wei = gas_used * gas_price

    fee_eth = web3.from_wei(
        fee_wei,
        "ether",
    )

    return float(fee_eth)


# ============================================================
# TRANSFER NORMALIZATION
# ============================================================

def normalize_transfer(transfer):
    timestamp = transfer.get("metadata", {}).get(
        "blockTimestamp"
    )

    if isinstance(timestamp, str):

        timestamp = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

        if timestamp.tzinfo is not None:

            timestamp = timestamp.astimezone(
                timezone.utc
            ).replace(tzinfo=None)

    return {
        "from_address": transfer.get("from"),
        "to_address": transfer.get("to"),
        "amount": transfer.get("value"),
        "asset": transfer.get("asset"),
        "timestamp": timestamp,
        "transaction_hash": transfer.get("hash"),
        "chain": "sepolia",
        "fee": get_transaction_fee(
            transfer.get("hash")
        ),
    }


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    test_wallet = (
        "0x3cfDc212769c890907bcE93D3d8C2c53dE6a7a89"
    )

    print("\n==== FIRST REQUEST ====")

    transfers = get_wallet_transfers(test_wallet)

    print(
        f"Found {len(transfers)} transfers"
    )

    print("\n==== SECOND REQUEST ====")

    transfers_again = get_wallet_transfers(
        test_wallet
    )

    print(
        f"Found {len(transfers_again)} transfers"
    )

    print(
        "\nCache test complete."
    )

    print("\n==== LATEST TRANSFERS TEST ====")

    latest_transfers = get_latest_wallet_transfers(
        test_wallet
    )

    print(
        "Latest transfers found:",
        len(latest_transfers),
    )

    print("\n==== NEW TRANSFERS TEST ====")

    last_checked_block = 0

    new_transfers, latest_block = (
        get_new_wallet_transfers(
            test_wallet,
            last_checked_block,
        )
    )

    print(
        "New transfers found:",
        len(new_transfers),
    )

    print(
        "Latest block:",
        latest_block,
    )