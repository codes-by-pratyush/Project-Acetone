from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Integer, Index
from sqlalchemy.orm import relationship
from backend.app.database import Base

class TransactionModel(Base):
    __tablename__ = "transactions"

    tx_hash = Column(String(66), primary_key=True, index=True)
    from_address = Column(String(128), nullable=False, index=True)
    to_address = Column(String(128), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    asset = Column(String(32), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    chain = Column(String(32), nullable=False, index=True)
    fee = Column(Float, default=0.0, nullable=True)

    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)
    case = relationship("CaseModel", back_populates="transactions")

class CaseModel(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("TransactionModel", back_populates="case")

class AlertModel(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_address = Column(String(128), nullable=False, index=True)
    rule_name = Column(String(100), nullable=False)
    severity = Column(String(20), default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)

Index("idx_chain_timestamp", TransactionModel.chain, TransactionModel.timestamp)