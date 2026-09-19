from Blockchain.storage.neo4j_store import driver


def detect_split(wallet_address, min_destinations=2):
    """
    Detect whether a wallet sends funds to multiple
    distinct destination wallets.

    Returns a structured result describing the split.
    """

    wallet_address = wallet_address.strip()
    min_destinations = max(2, int(min_destinations))

    query = """
    MATCH (wallet:Wallet)-[tx:SENT]->(destination:Wallet)
    WHERE toLower(wallet.address) = toLower($wallet_address)
      AND wallet.chain = $chain

    RETURN
        destination.address AS destination,
        tx.hash AS hash,
        tx.amount AS amount,
        tx.asset AS asset,
        tx.timestamp AS timestamp
    ORDER BY tx.amount DESC
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
                "destination": record["destination"],
                "hash": record["hash"],
                "amount": record["amount"],
                "asset": record["asset"],
                "timestamp": record["timestamp"],
            })

    destinations = {
        transaction["destination"].lower()
        for transaction in transactions
        if transaction["destination"]
    }

    return {
        "wallet": wallet_address.lower(),
        "pattern": "split",
        "detected": len(destinations) >= min_destinations,
        "destination_count": len(destinations),
        "transactions": transactions,
    }


def detect_consolidation(wallet_address, min_sources=2):
    """
    Detect whether multiple distinct wallets send funds
    to the same wallet.

    Returns a structured result describing the consolidation.
    """

    wallet_address = wallet_address.strip()
    min_sources = max(2, int(min_sources))

    query = """
    MATCH (source:Wallet)-[tx:SENT]->(wallet:Wallet)
    WHERE toLower(wallet.address) = toLower($wallet_address)
      AND wallet.chain = $chain

    RETURN
        source.address AS source,
        tx.hash AS hash,
        tx.amount AS amount,
        tx.asset AS asset,
        tx.timestamp AS timestamp
    ORDER BY tx.amount DESC
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
                "source": record["source"],
                "hash": record["hash"],
                "amount": record["amount"],
                "asset": record["asset"],
                "timestamp": record["timestamp"],
            })

    sources = {
        transaction["source"].lower()
        for transaction in transactions
        if transaction["source"]
    }

    return {
        "wallet": wallet_address.lower(),
        "pattern": "consolidation",
        "detected": len(sources) >= min_sources,
        "source_count": len(sources),
        "transactions": transactions,
    }