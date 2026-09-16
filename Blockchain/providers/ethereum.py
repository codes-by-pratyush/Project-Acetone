import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from web3 import Web3


# Find the .env file in the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


# Get the Alchemy API key
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")

if not ALCHEMY_API_KEY:
    raise ValueError("ALCHEMY_API_KEY was not found in .env")


# Alchemy Sepolia RPC endpoint
RPC_URL = f"https://eth-sepolia.g.alchemy.com/v2/{ALCHEMY_API_KEY}"


# Create Web3 connection
web3 = Web3(Web3.HTTPProvider(RPC_URL))


# Check connection
if web3.is_connected():
    print("Connected to Ethereum Sepolia through Alchemy!")
    print("Latest block:", web3.eth.block_number)
else:
    print("Connection failed.")


# ---------------------------------------------------------
# Get wallet transfer history using Alchemy Transfers API
# ---------------------------------------------------------

def get_wallet_transfers(wallet_address):
     """Get all Sepolia transfers involving a wallet address."""

     all_transfers = []
     page_key = None

     while True:

        request_params = {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "fromAddress": wallet_address,
            "category": [
                "external",
                "erc20"
            ],
            "withMetadata": True,
            "excludeZeroValue": True,
        }

        # Add pageKey only when Alchemy gives us one
        if page_key:
            request_params["pageKey"] = page_key

        request_body = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "alchemy_getAssetTransfers",
            "params": [request_params],
        }

        response = requests.post(
            RPC_URL,
            json=request_body,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:
            raise RuntimeError(data["error"])

        result = data["result"]

        # Add this page's transfers
        all_transfers.extend(result["transfers"])

        # Check whether another page exists
        page_key = result.get("pageKey")

        if not page_key:
            break

     return all_transfers
# ---------------------------------------------------------
# Normalize Alchemy transfer data
# ---------------------------------------------------------
def get_latest_wallet_transfers(wallet_address, from_block="0x0"):
    """Get incoming and outgoing Sepolia transfers involving a wallet."""

    all_transfers = []

    for direction in ["outgoing", "incoming"]:

        page_key = None

        while True:

            request_params = {
                "fromBlock": from_block,
                "toBlock": "latest",
                "category": [
                    "external",
                    "erc20"
                ],
                "withMetadata": True,
                "excludeZeroValue": True,
                "maxCount": "0x64"
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

            response = requests.post(
                RPC_URL,
                json=request_body,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            if "error" in data:
                raise RuntimeError(data["error"])

            result = data["result"]

            all_transfers.extend(result["transfers"])

            page_key = result.get("pageKey")

            if not page_key:
                break

    return all_transfers
#---------------------------------------------------------
def get_new_wallet_transfers(wallet_address, last_checked_block):
    """Get wallet transfers from the block after the last checked block."""

    latest_block = web3.eth.block_number

    if last_checked_block >= latest_block:
        return [], latest_block

    from_block = hex(last_checked_block + 1)

    transfers = get_latest_wallet_transfers(
        wallet_address,
        from_block=from_block
    )

    return transfers, latest_block

#---------------------------------------------------------
#---------------------------------------------------------

def get_transaction_fee(transaction_hash):
    """Get the transaction fee in ETH."""

    transaction = web3.eth.get_transaction(transaction_hash)
    receipt = web3.eth.get_transaction_receipt(transaction_hash)

    gas_used = receipt["gasUsed"]
    gas_price = transaction["gasPrice"]

    fee_wei = gas_used * gas_price
    fee_eth = web3.from_wei(fee_wei, "ether")

    return float(fee_eth)
def normalize_transfer(transfer):
    """Convert Alchemy transfer data into ACETONE's standard format."""

    return {
        "from_address": transfer.get("from"),
        "to_address": transfer.get("to"),
        "amount": transfer.get("value"),
        "asset": transfer.get("asset"),
        "timestamp": transfer.get("metadata", {}).get("blockTimestamp"),
        "transaction_hash": transfer.get("hash"),
        "chain": "sepolia",
        "fee": get_transaction_fee(transfer.get("hash")),
    }


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    test_wallet = "0x3cfDc212769c890907bcE93D3d8C2c53dE6a7a89"

    transfers = get_wallet_transfers(test_wallet)

    print(f"Found {len(transfers)} transfers")

    for transfer in transfers:
       normalized = normalize_transfer(transfer)

       print("\n-----------------------------")
       print("From:", normalized["from_address"])
       print("To:", normalized["to_address"])
       print("Amount:", normalized["amount"])
       print("Asset:", normalized["asset"])
       print("Timestamp:", normalized["timestamp"])
       print("Transaction Hash:", normalized["transaction_hash"])
       print("Chain:", normalized["chain"])
       print("Fee:", normalized["fee"])
       
    print("\n====LATEST TRANSFERS TEST====")
    latest_transfers = get_latest_wallet_transfers(test_wallet)
    print("Latest transfers found:", len(latest_transfers))
    
    print("\n====NEW TRANSFERS TEST====")
    last_checked_block = 0
    new_transfers, latest_block = get_new_wallet_transfers(test_wallet, last_checked_block)
    print("New transfers found:", len(new_transfers))


