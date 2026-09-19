from Blockchain.storage.neo4j_store import save_transaction_to_graph
from backend.app.database import SessionLocal
from backend.app.models.relational import TransactionModel


def save_transaction(transaction):
    """
    Save a normalized blockchain transaction into PostgreSQL
    and Neo4j.
    """

    db = SessionLocal()

    try:
        existing = db.query(TransactionModel).filter(
            TransactionModel.tx_hash == transaction["transaction_hash"]
        ).first()

        if existing:
            return existing

        record = TransactionModel(
            tx_hash=transaction["transaction_hash"],
            from_address=transaction["from_address"],
            to_address=transaction["to_address"],
            amount=transaction["amount"],
            asset=transaction["asset"],
            timestamp=transaction["timestamp"],
            chain=transaction["chain"],
            fee=transaction["fee"],
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        save_transaction_to_graph(transaction)

        return record

    finally:
        db.close()