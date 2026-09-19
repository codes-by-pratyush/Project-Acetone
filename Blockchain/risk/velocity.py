from Blockchain.storage.neo4j_store import driver


def detect_rapid_forwarding(
    wallet_address,
    max_seconds=300,
):
    """
    Detect whether a wallet receives funds and then
    forwards funds within max_seconds.

    max_seconds defaults to 5 minutes.
    """

    wallet_address = wallet_address.strip()
    max_seconds = max(1, int(max_seconds))

    query = """
    MATCH (sender:Wallet)-[incoming:SENT]->(wallet:Wallet)
    MATCH (wallet:Wallet)-[outgoing:SENT]->(receiver:Wallet)

    WHERE toLower(wallet.address) = toLower($wallet_address)
      AND wallet.chain = $chain
      AND incoming.timestamp IS NOT NULL
      AND outgoing.timestamp IS NOT NULL
      AND outgoing.timestamp >= incoming.timestamp
      AND outgoing.timestamp <= incoming.timestamp + duration({seconds: $max_seconds})

    RETURN
        incoming.hash AS incoming_hash,
        incoming.amount AS incoming_amount,
        incoming.timestamp AS incoming_timestamp,
        sender.address AS sender,

        outgoing.hash AS outgoing_hash,
        outgoing.amount AS outgoing_amount,
        outgoing.timestamp AS outgoing_timestamp,
        receiver.address AS receiver,

        duration.between(
            incoming.timestamp,
            outgoing.timestamp
        ).seconds AS delay_seconds
    """

    with driver.session() as session:
        result = session.run(
            query,
            wallet_address=wallet_address,
            chain="sepolia",
            max_seconds=max_seconds,
        )

        rapid_transactions = []

        for record in result:
            rapid_transactions.append({
                "incoming_hash": record["incoming_hash"],
                "incoming_amount": record["incoming_amount"],
                "incoming_timestamp": record["incoming_timestamp"],
                "sender": record["sender"],
                "outgoing_hash": record["outgoing_hash"],
                "outgoing_amount": record["outgoing_amount"],
                "outgoing_timestamp": record["outgoing_timestamp"],
                "receiver": record["receiver"],
                "delay_seconds": record["delay_seconds"],
            })

    return {
        "wallet": wallet_address.lower(),
        "pattern": "rapid_forwarding",
        "detected": bool(rapid_transactions),
        "match_count": len(rapid_transactions),
        "transactions": rapid_transactions,
    }