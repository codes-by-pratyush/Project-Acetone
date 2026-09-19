import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "acetone_password")


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def save_transaction_to_graph(transaction):
    """
    Save a normalized transaction as:

    (Wallet) -[:SENT]-> (Wallet)
    """

    query = """
    MERGE (sender:Wallet {address: $from_address, chain: $chain})
    MERGE (receiver:Wallet {address: $to_address, chain: $chain})

    MERGE (sender)-[tx:SENT {hash: $transaction_hash}]->(receiver)

    SET tx.amount = $amount,
        tx.asset = $asset,
        tx.timestamp = $timestamp,
        tx.fee = $fee

    RETURN sender, tx, receiver
    """

    with driver.session() as session:
        result = session.run(
            query,
            from_address=transaction["from_address"].lower(),
            to_address=transaction["to_address"].lower(),
            chain=transaction["chain"],
            transaction_hash=transaction["transaction_hash"],
            amount=transaction["amount"],
            asset=transaction["asset"],
            timestamp=transaction["timestamp"],
            fee=transaction["fee"],
        )

        return result.single()


def close_driver():
    driver.close()