from Blockchain.storage.neo4j_store import driver


def test_ffff_trace_data():
    wallet = "0xffffffffffffffffffffffffffffffffffffffff"

    query = """
    MATCH (wallet:Wallet)
    WHERE toLower(wallet.address) = $wallet
    OPTIONAL MATCH (wallet)-[tx:SENT]->(destination:Wallet)
    RETURN
        wallet.address AS wallet_address,
        wallet.chain AS chain,
        count(tx) AS outgoing_count,
        collect({
            to: destination.address,
            amount: tx.amount,
            hash: tx.hash
        }) AS transactions
    """

    with driver.session() as session:
        result = session.run(
            query,
            wallet=wallet,
        )

        record = result.single()

    print("\n=== FFFF NEO4J DATA ===")

    if record is None:
        print("FFFF wallet does NOT exist in Neo4j.")
        return

    print("Wallet:", record["wallet_address"])
    print("Chain:", record["chain"])
    print("Outgoing transactions:", record["outgoing_count"])
    print("Transactions:")

    for transaction in record["transactions"]:
        print(transaction)


if __name__ == "__main__":
    test_ffff_trace_data()