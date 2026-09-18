from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from backend.app.database import Base

class VASPLabel(Base):
    __tablename__ = "vasp_labels"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(128), unique=True, nullable=False, index=True)
    vasp_name = Column(String(100), nullable=False, index=True)
    category = Column(String(50), default="hot_wallet")  # hot_wallet, deposit, cold_storage
    chain = Column(String(32), default="ethereum", nullable=False)
    confidence_score = Column(Float, nullable=False, default=0.90)
    source = Column(String(100), default="public_records")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_vasp_lookup", "address", "chain"),
    )