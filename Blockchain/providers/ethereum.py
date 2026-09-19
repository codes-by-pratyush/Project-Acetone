import os
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from web3 import Web3


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")

if not ALCHEMY_API_KEY:
    raise RuntimeError(
        "ALCHEMY_API_KEY is not set in the environment."
    )


# ============================================================
# ALCHEMY / WEB3 CONNECTION
# ============================================================

ALCHEMY_URL = (
    f"https://eth-sepolia.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
)

w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))


if not w3.is_connected():
    raise RuntimeError(
        "Could not connect to Ethereum Sepolia through Alchemy."
    )


print("Connected to Ethereum Sepolia through Alchemy!")
print(f"Latest block: {w3.eth.block_number}")


# ============================================================
# HTTP RETRY STRATEGY
# ============================================================

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[
        429,
        500,
        502,
        503,
        504,
    ],
    allowed_methods=["POST"],
)

http_session = requests.Session()

adapter = HTTPAdapter(
    max_retries=retry_strategy
)

http_session.mount(
    "https://",
    adapter,
)


# ============================================================
# LOCAL RATE LIMITING
# ============================================================

MIN_REQUEST_INTERVAL = 0.25

_last_request_time = 0.0


def rate_limit():
    global _last_request_time

    current_time = time.time()

    elapsed = current_time - _last_request_time

    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(
            MIN_REQUEST_INTERVAL - elapsed
        )

    _last_request_time = time.time()


# ============================================================
# TRANSFER CACHE
# ============================================================

TRANSFER_CACHE = {}

CACHE_TTL_SECONDS = 60


def get_cached_transfers(wallet_address):
    wallet_address = wallet_address.lower()

    cached = TRANSFER_CACHE.get(wallet_address)

    if not cached:
        return None

    cached_time = cached["timestamp"]

    if time.time() - cached_time > CACHE_TTL_SECONDS:
        del TRANSFER_CACHE[wallet_address]
        return None

    return cached["transfers"]


def cache_transfers(
    wallet_address,
    transfers,
):
    wallet_address = wallet_address.lower()

    TRANSFER_CACHE[wallet_address] = {
        "timestamp": time.time(),
        "transfers": transfers,
    }

    print(
        f"Cached {len(transfers)} transfers "
        f"for {CACHE_TTL_SECONDS} seconds."
    )


def clear_transfer_cache(wallet_address=None):
    if wallet_address is None:
        TRANSFER_CACHE.clear()
        return

    wallet_address = wallet_address.lower()

    TRANSFER_CACHE.pop(
        wallet_address,
        None,
    )


# ============================================================
# ALCHEMY TRANSFER API
# ============================================================

def post_to_provider(method, params):
    rate_limit()

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }

    response = http_session.post(
        ALCHEMY_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(
            f"Alchemy API error: {data['error']}"
        )

    return data


def get_wallet_transfers(wallet_address):
    wallet_address = wallet_address.lower()

    cached_transfers = get_cached_transfers(
        wallet_address
    )

    if cached_transfers is not None:
        print(
            f"Cache hit: {wallet_address}"
        )
        return cached_transfers

    print(
        f"Cache miss: {wallet_address}"
    )

    print(
        "Fetching wallet transfers from Alchemy..."
    )

    transfers = []

    categories = [
        "external",
        "internal",
        "erc20",
        "erc721",
        "erc1155",
    ]

    for category in categories:

        params = [
            {
                "fromAddress": wallet_address,
                "category": [category],
                "withMetadata": True,
            }
        ]

        try:
            data = post_to_provider(
                "alchemy_getAssetTransfers",
                params,
            )

            result = data.get(
                "result",
                {},
            )

            transfers.extend(
                result.get(
                    "transfers",
                    [],
                )
            )

        except Exception as error:
            print(
                f"Failed fetching outgoing "
                f"{category} transfers: {error}"
            )

        params = [
            {
                "toAddress": wallet_address,
                "category": [category],
                "withMetadata": True,
            }
        ]

        try:
            data = post_to_provider(
                "alchemy_getAssetTransfers",
                params,
            )

            result = data.get(
                "result",
                {},
            )

            transfers.extend(
                result.get(
                    "transfers",
                    [],
                )
            )

        except Exception as error:
            print(
                f"Failed fetching incoming "
                f"{category} transfers: {error}"
            )

    cache_transfers(
        wallet_address,
        transfers,
    )

    return transfers


# ============================================================
# LATEST WALLET TRANSFERS
# ============================================================

def get_latest_wallet_transfers(
    wallet_address,
    from_block="0x0",
):
    wallet_address = wallet_address.lower()

    transfers = []

    categories = [
        "external",
        "internal",
        "erc20",
        "erc721",
        "erc1155",
    ]

    latest_block = w3.eth.block_number

    for category in categories:

        params = [
            {
                "fromAddress": wallet_address,
                "fromBlock": from_block,
                "toBlock": hex(latest_block),
                "category": [category],
                "withMetadata": True,
            }
        ]

        try:
            data = post_to_provider(
                "alchemy_getAssetTransfers",
                params,
            )

            result = data.get(
                "result",
                {},
            )

            transfers.extend(
                result.get(
                    "transfers",
                    [],
                )
            )

        except Exception as error:
            print(
                f"Failed fetching latest "
                f"{category} transfers: {error}"
            )

        params = [
            {
                "toAddress": wallet_address,
                "fromBlock": from_block,
                "toBlock": hex(latest_block),
                "category": [category],
                "withMetadata": True,
            }
        ]

        try:
            data = post_to_provider(
                "alchemy_getAssetTransfers",
                params,
            )

            result = data.get(
                "result",
                {},
            )

            transfers.extend(
                result.get(
                    "transfers",
                    [],
                )
            )

        except Exception as error:
            print(
                f"Failed fetching incoming "
                f"latest {category} transfers: {error}"
            )

    return transfers


# ============================================================
# NEW WALLET TRANSFERS
# ============================================================

def get_new_wallet_transfers(
    wallet_address,
    last_checked_block,
):
    latest_block = w3.eth.block_number

    from_block = max(
        int(last_checked_block),
        0,
    )

    if from_block > latest_block:
        return [], latest_block

    transfers = get_latest_wallet_transfers(
        wallet_address,
        from_block=hex(from_block),
    )

    return transfers, latest_block


# ============================================================
# TRANSACTION FEE
# ============================================================

def get_transaction_fee(transaction_hash):
    if not transaction_hash:
        return 0.0

    try:
        transaction = w3.eth.get_transaction(
            transaction_hash
        )

        receipt = w3.eth.get_transaction_receipt(
            transaction_hash
        )

        gas_used = receipt.gasUsed

        gas_price = transaction.gasPrice

        fee_wei = gas_used * gas_price

        fee_eth = w3.from_wei(
            fee_wei,
            "ether",
        )

        return float(fee_eth)

    except Exception as error:
        print(
            f"Could not calculate transaction fee "
            f"for {transaction_hash}: {error}"
        )

        return 0.0


# ============================================================
# TRANSFER NORMALIZATION
# ============================================================

def normalize_transfer(transfer):
    metadata = transfer.get(
        "metadata"
    ) or {}

    timestamp = metadata.get(
        "blockTimestamp"
    )

    if isinstance(timestamp, str):

        timestamp = datetime.fromisoformat(
            timestamp.replace(
                "Z",
                "+00:00",
            )
        )

        if timestamp.tzinfo is not None:

            timestamp = (
                timestamp.astimezone(
                    timezone.utc
                )
                .replace(
                    tzinfo=None
                )
            )

    transaction_hash = transfer.get(
        "hash"
    )

    amount = transfer.get(
        "value"
    )

    asset = transfer.get(
        "asset"
    )

    category = transfer.get(
        "category"
    )

    # --------------------------------------------------------
    # Skip transfers that cannot currently be normalized.
    #
    # For the current MVP we process transfers with a usable
    # amount. ERC-20 records that do not expose a usable value
    # are skipped instead of causing a database failure.
    # --------------------------------------------------------

    if amount is None:

        print(
            f"Skipping unnormalizable transfer: "
            f"{transaction_hash} "
            f"(category={category}, asset={asset})"
        )

        return None

    return {
        "from_address": transfer.get(
            "from"
        ),

        "to_address": transfer.get(
            "to"
        ),

        "amount": amount,

        "asset": asset or "ETH",

        "timestamp": timestamp,

        "transaction_hash": transaction_hash,

        "chain": "sepolia",

        "fee": (
            get_transaction_fee(
                transaction_hash
            )
            if transaction_hash
            else 0.0
        ),
    }


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    test_wallet = (
        "0x3cfDc212769c890907bcE93D3d8C2c53dE6a7a89"
    )

    print(
        "\n==== FIRST REQUEST ===="
    )

    transfers = get_wallet_transfers(
        test_wallet
    )

    print(
        f"Transfers: {len(transfers)}"
    )

    if transfers:

        normalized = normalize_transfer(
            transfers[0]
        )

        print(
            "Normalized transfer:"
        )

        print(
            normalized
        )

    print(
        "\n==== SECOND REQUEST ===="
    )

    transfers = get_wallet_transfers(
        test_wallet
    )

    print(
        f"Transfers: {len(transfers)}"
    )