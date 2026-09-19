from Blockchain.storage.neo4j_store import driver


def get_wallet_age(wallet_address):
    """
    Calculate the observed age of a wallet from its earliest
    transaction in the Neo4j graph.

    Returns the age in seconds based on the earliest observed
    transaction timestamp and the latest observed transaction
    timestamp.
    """

    wallet_address = wallet_address.strip()

    query = """
    MATCH (wallet:Wallet)-[tx:SENT]-(other:Wallet)
    WHERE toLower(wallet.address) = toLower($wallet_address)
      AND wallet.chain = $chain
      AND tx.timestamp IS NOT NULL

    WITH
        min(tx.timestamp) AS first_seen,
        max(tx.timestamp) AS last_seen

    RETURN
        first_seen,
        last_seen,
        duration.between(first_seen, last_seen).seconds AS age_seconds
    """

    with driver.session() as session:
        result = session.run(
            query,
            wallet_address=wallet_address,
            chain="sepolia",
        )

        record = result.single()

    if not record or record["first_seen"] is None:
        return {
            "wallet": wallet_address.lower(),
            "first_seen": None,
            "last_seen": None,
            "age_seconds": None,
        }

    return {
        "wallet": wallet_address.lower(),
        "first_seen": record["first_seen"],
        "last_seen": record["last_seen"],
        "age_seconds": record["age_seconds"],
    }


def is_new_wallet(wallet_address, max_age_seconds=86400):
    """
    Determine whether a wallet's observed activity spans less
    than max_age_seconds.

    Default threshold: 24 hours.
    """

    result = get_wallet_age(wallet_address)

    if result["age_seconds"] is None:
        return {
            **result,
            "is_new": False,
        }

    return {
        **result,
        "is_new": result["age_seconds"] <= max_age_seconds,
    }