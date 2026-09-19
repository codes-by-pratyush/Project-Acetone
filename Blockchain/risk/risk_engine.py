from Blockchain.tracing.patterns import (
    detect_split,
    detect_consolidation,
)

from Blockchain.risk.rules import is_round_number
from Blockchain.risk.velocity import detect_rapid_forwarding
from Blockchain.risk.wallet_age import is_new_wallet
from Blockchain.storage.neo4j_store import driver


def get_wallet_transactions(wallet_address):
    """
    Get all incoming and outgoing transactions involving a wallet.
    """

    query = """
    MATCH (wallet:Wallet)-[tx:SENT]-(other:Wallet)
    WHERE toLower(wallet.address) = toLower($wallet_address)
      AND wallet.chain = $chain

    RETURN
        wallet.address AS wallet,
        tx.hash AS hash,
        tx.amount AS amount,
        tx.asset AS asset,
        tx.timestamp AS timestamp,
        startNode(tx).address AS sender,
        endNode(tx).address AS receiver
    """

    with driver.session() as session:
        result = session.run(
            query,
            wallet_address=wallet_address,
            chain="sepolia",
        )

        transactions = []

        for record in result:
            transactions.append({
                "wallet": record["wallet"],
                "hash": record["hash"],
                "amount": record["amount"],
                "asset": record["asset"],
                "timestamp": record["timestamp"],
                "sender": record["sender"],
                "receiver": record["receiver"],
            })

        return transactions


def calculate_wallet_risk(wallet_address):
    """
    Calculate an explainable rule-based risk result
    for a wallet.
    """

    split_result = detect_split(wallet_address)
    consolidation_result = detect_consolidation(wallet_address)
    rapid_forwarding_result = detect_rapid_forwarding(wallet_address)
    wallet_age_result = is_new_wallet(wallet_address)

    transactions = get_wallet_transactions(wallet_address)

    score = 0
    evidence = []

    # Fan-out / split
    if split_result["detected"]:
        score += 20

        evidence.append({
            "rule": "fan_out",
            "description": (
                "Wallet sent funds to multiple distinct "
                "destination wallets."
            ),
            "points": 20,
            "destination_count": split_result["destination_count"],
        })

    # Fan-in / consolidation
    if consolidation_result["detected"]:
        score += 20

        evidence.append({
            "rule": "fan_in",
            "description": (
                "Multiple distinct wallets sent funds "
                "to this wallet."
            ),
            "points": 20,
            "source_count": consolidation_result["source_count"],
        })

    # Rapid forwarding
    if rapid_forwarding_result["detected"]:
        score += 25

        evidence.append({
            "rule": "rapid_forwarding",
            "description": (
                "Wallet received funds and forwarded funds "
                "within the configured time window."
            ),
            "points": 25,
            "match_count": rapid_forwarding_result["match_count"],
            "transactions": rapid_forwarding_result["transactions"],
        })

    # New wallet
    if wallet_age_result["is_new"]:
        score += 10

        evidence.append({
            "rule": "new_wallet",
            "description": (
                "Wallet's observed transaction history "
                "spans less than the configured wallet-age threshold."
            ),
            "points": 10,
            "age_seconds": wallet_age_result["age_seconds"],
            "first_seen": wallet_age_result["first_seen"],
            "last_seen": wallet_age_result["last_seen"],
        })

    # Round-number transfers
    round_number_transactions = [
        transaction
        for transaction in transactions
        if is_round_number(transaction["amount"])
    ]

    if round_number_transactions:
        score += 10

        evidence.append({
            "rule": "round_number_transfer",
            "description": (
                "Wallet was involved in one or more "
                "round-number transfers."
            ),
            "points": 10,
            "transaction_count": len(round_number_transactions),
            "transactions": round_number_transactions,
        })

    return {
        "wallet": wallet_address.lower(),
        "score": score,
        "evidence": evidence,
        "signals": {
            "fan_out": split_result["detected"],
            "fan_in": consolidation_result["detected"],
            "rapid_forwarding": rapid_forwarding_result["detected"],
            "new_wallet": wallet_age_result["is_new"],
            "round_number_transfer": bool(
                round_number_transactions
            ),
        },
    }